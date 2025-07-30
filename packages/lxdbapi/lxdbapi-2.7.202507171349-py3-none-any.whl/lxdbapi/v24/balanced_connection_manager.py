import logging
from threading import RLock
from lxdbapi.connection_manager import RefreshableConnectionManager, MultiConnectionI, ServiceConnectionI

logger = logging.getLogger(__name__)


class CandidateTrack(object):
    _map_address = dict()
    _map_lock = RLock()

    def clear(self):
        with self._map_lock:
            self._map_address.clear()

    def candidates(self, addr: str):
        with self._map_lock:
            result = self._map_address.get(addr, None)
        if result is None:
            result = 0
        logger.debug("Candidates for %s: %s", addr, str(result))
        return result

    def add(self, addr: str):
        if addr is not None:
            with self._map_lock:
                num = self._map_address.get(addr, None)
                if num is None:
                    self._map_address[addr] = 1
                else:
                    self._map_address[addr] = num + 1

    def remove(self, addr: str):
        if addr is not None:
            with self._map_lock:
                num = self._map_address.get(addr, None)
                if num is not None:
                    if num <= 1:
                        self._map_address.pop(addr, None)
                    else:
                        self._map_address[addr] = num - 1


class BalancedConnectionManager(RefreshableConnectionManager):
    _qe_map = dict()
    _qe_map_lock = RLock()
    _qe_locks = dict()
    _candidate_track = CandidateTrack()
    _failed_addresses = set()

    def __init__(self, service_connection: ServiceConnectionI):
        super().__init__(service_connection)

    def reconnect_address(self, addr: str, connection: MultiConnectionI):
        return super().reconnect_address(addr, connection)

    def get_service_connection(self):
        return super().get_service_connection()

    def is_stopped(self):
        return super().is_stopped()

    def stop(self):
        super().stop()

    def reconnect(self, connection: MultiConnectionI):
        return super().reconnect(connection)

    def add_connection(self, connection: MultiConnectionI):
        addr = connection.qe_address()
        logger.debug('Adding connection {} to QE {}'.format(connection.id(), addr))
        self._candidate_track.remove(addr)
        with self._qe_map_lock:
            self._failed_addresses.discard(addr)
            conn_map = self._qe_map.get(addr, None)
            if conn_map is None:
                conn_map = dict()
                self._qe_map[addr] = conn_map
                addr_lock = RLock()
                self._qe_locks[addr] = addr_lock
                logger.debug('Address {} added to connection manager'.format(addr))
            else:
                addr_lock = self._qe_locks[addr]
        with addr_lock:
            conn = conn_map.get(connection.id(), None)
            if conn:
                raise RuntimeError('Connection {} already in address {}'.format(connection.id(), addr))
            conn_map[connection.id()] = connection
            logger.debug('Connection {} added to address {}'.format(connection.id(), addr))

    def remove_connection(self, connection: MultiConnectionI):
        addr = connection.qe_address()
        logger.debug("Removing connection {} from QE {}".format(connection.id(), addr))
        with self._qe_map_lock:
            conn_map = self._qe_map.get(addr, None)
            addr_lock = self._qe_locks.get(addr, None)
        if conn_map is not None:
            with addr_lock:
                conn_map.pop(connection.id(), None)
        logger.debug("Removed connection {} from QE {}".format(connection.id(), addr))

    def _unsafe_invalidate_address(self, addr: str):
        if addr:
            conn_map = self._qe_map.get(addr, None)
            if conn_map is None or len(conn_map) == 0:
                self._qe_map.pop(addr, None)
                self._qe_locks.pop(addr, None)
                self._failed_addresses.discard(addr)
            else:
                if addr not in self._failed_addresses:
                    for conn in conn_map.values():
                        conn.invalidate_address()
                    self._failed_addresses.add(addr)

    def _balanced_connections_per_server(self):
        total_servers = 0
        total_connections = 0
        for addr in self._qe_map:
            conn_map = self._qe_map.get(addr, None)
            if conn_map is not None:
                total_connections += len(conn_map)
            if addr not in self._failed_addresses:
                total_servers += 1
        logger.debug("totalConnections [%d], totalServers [%d]", total_connections, total_servers)
        return total_connections, total_servers

    def _balance(self):
        pair = self._balanced_connections_per_server()
        if 0 == pair[1]:
            return
        per_server, remainders = divmod(pair[0], pair[1])
        for addr in self._qe_map:
            conn_map = self._qe_map.get(addr, None)
            if conn_map is not None:
                map_len = len(conn_map)
                logger.debug("Per server [%d], size [%d]", per_server, map_len)
                if per_server >= map_len or 1 >= map_len:
                    continue
                current_per_server = per_server
                if 0 < remainders:
                    current_per_server += 1
                inx = 0
                for connId in conn_map:
                    actual_size = map_len - inx
                    inx += 1
                    if current_per_server > actual_size or 1 >= actual_size:
                        break
                    conn = conn_map[connId]
                    conn.do_reconnect()

    def update(self, addresses: set):
        self._candidate_track.clear()
        with self._qe_map_lock:
            need_balance = False
            invalids = list()
            for addr in self._qe_map:
                if addr not in addresses:
                    invalids.append(addr)
            for addr in invalids:
                self._unsafe_invalidate_address(addr)
            for addr in addresses:
                conn_map = self._qe_map.get(addr, None)
                if conn_map is None:
                    need_balance = True
                    self._qe_map[addr] = dict()
                    self._qe_locks[addr] = RLock()
                elif need_balance is False and addr in self._failed_addresses:
                    need_balance = True
            if need_balance:
                self._balance()

    def next_qe(self):
        result = None
        with self._qe_map_lock:
            size = -1
            for addr in self._qe_map:
                if addr in self._failed_addresses:
                    continue
                conn_map = self._qe_map.get(addr, None)
                addr_lock = self._qe_locks[addr]
                map_len = len(conn_map)
                with addr_lock:
                    inx_size = map_len + self._candidate_track.candidates(addr)
                logger.debug("QE %s size: %d", addr, inx_size)
                if 0 == inx_size:
                    result = addr
                    break
                elif result is None:
                    size = inx_size
                    result = addr
                elif size > inx_size:
                    size = inx_size
                    result = addr

        logger.debug("Next QE: %s", result)
        self._candidate_track.add(result)
        return result

    def invalidate_address(self, addr: str):
        with self._qe_map_lock:
            self._unsafe_invalidate_address(addr)

    def validate_address(self, addr: str):
        if self.is_valid_address(addr) is False:
            with self._qe_map_lock:
                self._failed_addresses.discard(addr)

    def is_valid_address(self, addr: str):
        with self._qe_map_lock:
            result = addr in self._qe_map and addr not in self._failed_addresses
        return result

    def reconnect_retries(self):
        with self._qe_map_lock:
            result = len(self._qe_map) - len(self._failed_addresses)
        return result

    def info(self):
        result = super().info()
        addr_size = dict()
        with self._qe_map_lock:
            result += ',\n\tFailed addresses ' + str(self._failed_addresses)
            for addr in self._qe_map:
                conn_map = self._qe_map[addr]
                addr_size[addr] = len(conn_map)
        result += ',\n\tConnections by address ' + str(addr_size)
        return result
