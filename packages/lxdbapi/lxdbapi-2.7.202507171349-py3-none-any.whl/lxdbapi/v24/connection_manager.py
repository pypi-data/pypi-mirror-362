import logging
import os
import time
from threading import RLock, Thread

__all__ = ['MultiConnectionI', 'ServiceConnectionI', 'ConnectionManager', 'RefreshableConnectionManager']

logger = logging.getLogger(__name__)


class MultiConnectionI(object):

    def id(self):
        raise NotImplementedError('Extend ConnectionManager')

    def reconnect(self, addr=None):
        raise NotImplementedError('Extend ConnectionManager')

    def qe_address(self):
        raise NotImplementedError('Extend ConnectionManager')

    def unset_do_reconnect(self):
        raise NotImplementedError('Extend ConnectionManager')

    def set_do_reconnect(self):
        raise NotImplementedError('Extend ConnectionManager')


class ServiceConnectionI(object):

    def qe_addresses(self):
        raise NotImplementedError('Extend ConnectionManager')


class ConnectionManager(object):

    def add_connection(self, conn: MultiConnectionI):
        raise NotImplementedError('Extend ConnectionManager')

    def remove_connection(self, conn: MultiConnectionI):
        raise NotImplementedError('Extend ConnectionManager')

    def reconnect(self, conn: MultiConnectionI):
        raise NotImplementedError('Extend ConnectionManager')

    def update(self, addresses: set):
        raise NotImplementedError('Extend ConnectionManager')

    def next_qe(self):
        return None

    def invalidate_address(self, addr: str):
        raise NotImplementedError('Extend ConnectionManager')

    def validate_address(self, addr: str):
        raise NotImplementedError('Extend ConnectionManager')

    def is_valid_address(self, addr: str):
        return True

    def is_stopped(self):
        raise NotImplementedError('Extend ConnectionManager')

    def stop(self):
        raise NotImplementedError('Extend ConnectionManager')

    def info(self):
        return None


class RefreshableConnectionManager(ConnectionManager):

    def __init__(self, service_connection: ServiceConnectionI):
        self._stopped = False
        self._stopped_lock = RLock()
        self._service_connection = service_connection
        self._thread = Thread(target=refresh_conn_mgr, args=[self], daemon=True)
        self._thread.start()

    def add_connection(self, conn: MultiConnectionI):
        super().add_connection(conn)

    def remove_connection(self, conn: MultiConnectionI):
        super().remove_connection(conn)

    def update(self, addresses: set):
        super().update(*addresses)

    def next_qe(self):
        return super().next_qe()

    def invalidate_address(self, addr: str):
        super().invalidate_address(addr)

    def validate_address(self, addr: str):
        super().validate_address(addr)

    def is_valid_address(self, addr: str):
        return super().is_valid_address(addr)

    def reconnect_address(self, addr: str, connection: MultiConnectionI):
        is_reconnected = False
        logger.debug("Reconnecting connection {} to QE {}".format(connection.id(), addr))
        try:
            connection.reconnect(addr)
            # self.add_connection(connection)
            is_reconnected = True
        except Exception as ex:
            msg = str(ex)
            if 'Connection already exists' in msg:
                logger.debug("Connection {} already exists in {}".format(connection.id(), addr))
                logger.debug("Connection {} already exists in {}: {}".format(connection.id(), addr, ex))
                is_reconnected = True
            else:
                logger.error("Cannot reconnect {} to {}: {}".format(connection.id(), addr, ex))
        return is_reconnected

    def reconnect_retries(self):
        raise NotImplementedError('Extend RefreshableConnectionManager')

    def get_service_connection(self):
        return self._service_connection

    def is_stopped(self):
        with self._stopped_lock:
            result = self._stopped
        return result

    def stop(self):
        with self._stopped_lock:
            self._stopped = True

    def reconnect(self, connection: MultiConnectionI):
        addr = connection.qe_address()
        is_reconnected = False
        retries = self.reconnect_retries()
        self.remove_connection(connection)
        while is_reconnected is False and retries >= 0:
            retries -= 1
            new_addr = self.next_qe()
            if new_addr is None:
                logger.error("No other address but {}. Retry once".format(addr))
                retries = -1
                new_addr = addr

            if self.reconnect_address(new_addr, connection):
                is_reconnected = True
                connection.unset_do_reconnect()
            else:
                self.invalidate_address(new_addr)
                logger.error("Failed reconnection from {} to {}".format(addr, new_addr))
        return is_reconnected

    def info(self):
        with self._stopped_lock:
            result = 'is stopped: ' + str(self._stopped)
        return result


def refresh_conn_mgr(manager: RefreshableConnectionManager):
    period = int(os.environ.get("LX_CM_PERIOD", 1))
    while not manager.is_stopped():
        try:
            service = manager.get_service_connection()
            qe_addresses = None
            if service is not None:
                addrs = service.qe_addresses()
                if addrs is not None:
                    logger.debug("Qe addresses: {}".format(addrs))
                    qe_addresses = set(addrs)
            if qe_addresses is None:
                logger.warning("No available Qe addresses found")
            else:
                manager.update(qe_addresses)
        except BaseException as ex:
            logger.error("server refresh failed: {}".format(ex))
            manager.stop()
            raise ex
        time.sleep(period)
