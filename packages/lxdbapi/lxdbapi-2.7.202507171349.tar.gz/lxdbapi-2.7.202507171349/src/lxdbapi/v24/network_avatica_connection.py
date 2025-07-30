import logging

import socket
from threading import RLock

from lxdbapi import errors, versions
import ssl

try:
    import httplib
except ImportError:
    import http.client as httplib

__all__ = ['TcpAvaticaConnection', 'NetAvaticaConnection']

logger = logging.getLogger(__name__)

SHDRSZ=12
HDRSZ=40
BODY_MAX_SZ=128*1024

class NetAvaticaConnection(object):
    def close(self):
        raise NotImplementedError('Extend NetAvaticaConnection')

    def request(self, body=None):
        raise NotImplementedError('Extend NetAvaticaConnection')

    def checkSerialization(self):
        raise NotImplementedError('Extend NetAvaticaConnection')


class TcpAvaticaConnection(NetAvaticaConnection):
    taggen = 0

    def __init__(self, url, secure, max_retries):
        """Opens a FTP connection to the RPC server."""
        self._close_lock = RLock()
        self.url = url
        self.secure =secure
        self.max_retries = max_retries if max_retries is not None else 3
        self._opened = False
        self._connect()

    def __del__(self):
        self._close()

    def __exit__(self):
        self._close()

    def _connect(self):
        if not self.secure:
            logger.debug("Using TCP")
            logger.debug("Opening connection to %s:%s", self.url.hostname, self.url.port)
            self.tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.tcp_socket.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)
            self.tcp_socket.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, True)
            self.tcp_socket.connect((self.url.hostname, self.url.port))
            self.tcpConn = self.tcp_socket
            self._opened = True
        else:
            logger.debug("Using TCP with SSL")
            logger.debug("Opening connection to %s:%s", self.url.hostname, self.url.port)
            self.tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.tcp_socket.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)
            self.tcp_socket.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, True)
            self.tcpConn = ssl.wrap_socket(self.tcp_socket)
            self.tcpConn.connect((self.url.hostname, self.url.port))
            self._opened = True

    def _close(self):
        with self._close_lock:
            if self._opened:
                self._opened = False
                self.tcpConn.close()

    def close(self):
        self._close()

    def sendrq(self, body=None):
        if body is None:
            return None
        tag = ++self.taggen
        tag = tag.to_bytes(4, 'little')
        twrap = 1
        twrap = twrap.to_bytes(1, 'little')
        pad = 0
        pad = pad.to_bytes(2, 'little')
        req_sz = len(body)
        n = 0
        while n < req_sz:
            flags = 0
            l = req_sz - n
            if l > BODY_MAX_SZ:
                flags = 1
                l = BODY_MAX_SZ
            logger.debug(f"sendrq: twrap: {twrap} sz: {l}, tag: {tag}, flags: {flags}")
            msg = bytearray()
            msg.extend(l.to_bytes(4, 'little'))
            msg.extend(tag)
            msg.extend(twrap)
            msg.extend(flags.to_bytes(1, 'little'))
            msg.extend(pad)
            msg.extend(body[n:(n+l)])
            self.tcpConn.sendall(msg)
            n += l


    def recvrq(self):
        response = bytearray()
        flags = 1
        while flags % 2 != 0:
            hdr = bytearray()
            while len(hdr) < 12:
                partial = self.tcpConn.recv(12 - len(hdr))
                if partial is None or len(partial) == 0:
                    logger.debug("No hdr")
                    return None
                hdr.extend(partial)
            resp_sz = int.from_bytes(hdr[:4], 'little')
            tag = int.from_bytes(hdr[4:8], 'little')
            twrap = hdr[8]
            flags = hdr[9]
            logger.debug(f"recvrq: twrap: {twrap} sz: {resp_sz}, tag: {tag}, flags: {flags}, hdr: {hdr}")
            if resp_sz < 0:
                logger.warning("negative msg size (sz {}) tag:{}".format(resp_sz, tag))
                raise IOError('IO Error on RPC request on {}. Got negative size [{}]'.format(self.url, resp_sz))
            if resp_sz == 0:
                return response
            pending = resp_sz
            offset = 0
            while pending > 0:
                partial = self.tcpConn.recv(pending)
                if partial is None:
                    raise IOError("No data. Connection closed")
                l = len(partial)
                if l <= 0:
                    raise IOError("No data. Connection closed")
                logger.debug(f"read {l} bytes")
                offset += l
                pending -= l
                response.extend(partial)
        return response

    def request(self, body=None):
        if body is None:
            return None
        self.sendrq(body)
        return self.recvrq()

    def checkSerialization(self):
        raise NotImplementedError('Should use server-info. Cotact support')