import logging
import random
import re
import time
import uuid
from threading import RLock

from lxdbapi.balanced_connection_manager import BalancedConnectionManager
from lxdbapi.connection_manager import ConnectionManager, MultiConnectionI, ServiceConnectionI

try:
    import urlparse
except ImportError:
    import urllib.parse as urlparse

from lxdbapi.client import AvaticaClient
from lxdbapi.connection import Connection

__all__ = ['connection_manager_info', 'connection_manager_stop', 'MultiConnection', 'MultiCursor']

logger = logging.getLogger(__name__)


class ConnectionManagerHolder(ConnectionManager):
    _delegator = None

    def is_inited(self):
        return self._delegator is not None

    def init_url(self, url, info: dict):
        if url and self._delegator is None:
            service_info = info.copy()
            service_info.pop('distribute', None)
            conn = ServiceConnection(url, service_info)
            self._delegator = BalancedConnectionManager(conn)
            self._delegator.add_connection(conn)  # Adding service connection to CM. Maybe we shouldn't

    def add_connection(self, conn):
        if self._delegator:
            self._delegator.add_connection(conn)

    def remove_connection(self, conn):
        if self._delegator:
            self._delegator.remove_connection(conn)

    def reconnect(self, conn):
        if self._delegator:
            return self._delegator.reconnect(conn)
        else:
            raise RuntimeError("No Connection manager")

    def update(self, addresses: set):
        if self._delegator:
            self._delegator.update(addresses)

    def next_qe(self):
        if self._delegator:
            return self._delegator.next_qe()
        return None

    def invalidate_address(self, addr: str):
        if self._delegator:
            self._delegator.invalidate_address(addr)

    def validate_address(self, addr: str):
        if self._delegator:
            self._delegator.validate_address(addr)

    def is_valid_address(self, addr: str):
        if self._delegator:
            return self._delegator.is_valid_address(addr)
        return True

    def is_stopped(self):
        if self._delegator:
            return self._delegator.is_stopped()
        return False

    def stop(self):
        if self._delegator:
            self._delegator.stop()

    def info(self):
        if self._delegator:
            return self._delegator.info()
        return "No connection manager"


_connection_manager = ConnectionManagerHolder()


def connection_manager(url=None, info=None):
    if url:
        _connection_manager.init_url(url, info)
    return _connection_manager


def connection_manager_info():
    return connection_manager().info()


def connection_manager_stop():
    return connection_manager().stop()


def _invoke_with_reconnect(multi_conn, cursor, func):
    manager = connection_manager(None)
    if multi_conn.is_do_reconnect():
        is_reconnected = manager.reconnect(multi_conn)
        if is_reconnected:
            if cursor:
                cursor.reset()
        else:
            logger.debug('Not reconnected but retry on current one: {}'.format(multi_conn.qe_address()))
    retry = 4
    result = None
    while retry > 0:
        retry -= 1
        try:
            result = func()
            manager.validate_address(multi_conn.qe_address())
            break
        except BaseException as ex:
            msg = str(ex)
            if 'Broken pipe' in msg or 'IO Error' in msg or 'Connection refused' in msg \
                    or 'Connection closed' in msg \
                    or 'Connection reset by peer' in msg or 'Cannot create cursor' in msg:
                logger.debug('reconnect cause of: {}'.format(msg))
                if manager.is_inited() and not manager.is_stopped():
                    manager.invalidate_address(multi_conn.qe_address())
                    is_reconnected = manager.reconnect(multi_conn)
                    if is_reconnected:
                        if cursor:
                            cursor.reset()
                    else:
                        raise RuntimeError("Cannot reconnect {}: {}".format(multi_conn.id(), ex), ex)
                else:
                    multi_conn.reconnect()
                    if cursor:
                        cursor.reset()
            elif 'the cursor is already closed' in msg and not cursor.closed:
                logger.debug('Delegator closed so retry it again: {}'.format(ex))
                cursor.reset()
            elif 'Connection already exists' in msg \
                    or 'Error parsing message' in msg or 'Bad file descriptor' in msg \
                    or 'RPC request failed on ParseResult' in msg \
                    or '\'NoneType\' object has no attribute \'makefile\'' in msg \
                    or '\'NoneType\' object has no attribute \'setsockopt\'' in msg \
                    or 'unexpected response type ' \
                       '"org.apache.calcite.avatica.proto.Responses$CloseStatementResponse"' in msg:
                if logger.isEnabledFor(logging.DEBUG):
                    logger.exception(ex)
                logger.debug('Ignore exception and retry again: {}'.format(ex))
            else:
                raise ex
    return result


def change_url_address(url, addr):
    url_parsed = urlparse.urlparse(url)
    if addr == url_parsed.netloc:
        return url
    replaced = url_parsed._replace(netloc=addr)
    return urlparse.urlunparse(list(replaced))


class MultiConnection(MultiConnectionI):

    def __init__(self, url, info):
        self._delegator = None
        self._cursors = []
        self._qe_address = None
        self._do_reconnect_lock = RLock()
        self._is_abort_pending_txn = False
        self._is_pending_commit = False
        self._is_auto_commit = True
        self._do_reconnect = False
        self._force_reopen = False
        self._closed = False
        self._info = info
        self._url = url
        m = re.search(r'leanxcale://(.*)@', url)
        if m is not None:
            user = m.group(1)
            userpwdmatch = re.search(r'(.*):(.*)', user)
            if userpwdmatch is not None:
                userpwd = user.split(":")
                self._info['user'] = userpwdmatch.group(1)
                self._info['password'] = userpwdmatch.group(2)
            else:
                self._info['user'] = user
        pos = url.rfind('/')
        if pos >= 0:
            pos += 1
            db = url[pos:]
            if db:
                self._info['database'] = db
        self._id = str(uuid.uuid4())
        self._open()

    def _connect(self):
        logger.debug("Connecting to address {}. Url = {}".format(self._qe_address, str(self._url)))
        client = AvaticaClient(self._url, 5, None, **self._info)
        self._delegator = Connection(client, self.id(), **self._info)
        self._delegator.open()
        logger.debug("Connected to {}".format(client.url))
        for cursor in self._cursors:
            if cursor is not None and not cursor.closed:
                cursor.reset()

    def _open(self):  # call just once
        distribute = self._info.get('distribute', None)
        if distribute:
            distribute_lower = str(distribute).lower()
            if distribute_lower == 'yes' or distribute_lower == 'true' or distribute_lower == 'balanced':
                addr = connection_manager(self.url(), self._info).next_qe()
                if addr is None or addr == "":
                    self._qe_address = urlparse.urlparse(self.url()).netloc
                else:
                    self._url = change_url_address(self.url(), addr)
                    self._qe_address = addr
            else:
                self._qe_address = urlparse.urlparse(self.url()).netloc

        else:
            self._qe_address = urlparse.urlparse(self.url()).netloc
        logger.debug("connecting to {}".format(self._qe_address))
        self._connect()
        with self._do_reconnect_lock:
            self._is_auto_commit = self._delegator.autocommit
        connection_manager().add_connection(self)

    def __del__(self):
        if self._delegator and not self._closed:
            try:
                self.close()
            except BaseException as ex:
                logger.debug("Ignoring exception while closing: {}".format(ex))
            finally:
                self._closed = True

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        if self._delegator and not self._closed:
            self.close()

    def id(self):
        return self._id

    def url(self):
        return self._url

    def qe_address(self):
        return self._qe_address

    def info(self):
        return self._info

    def close(self):
        if not self._closed:
            self._closed = True
            connection_manager().remove_connection(self)
            try:
                for cursor in self._cursors:
                    if cursor is not None and not cursor.closed:
                        try:
                            cursor.close()
                        except BaseException as ex:
                            logger.debug('Ignoring exception and forcing cursor reset: {}'.format(ex))
                            cursor.reset()
            finally:
                self._delegator.close()

    @property
    def closed(self):
        return self._closed

    def commit(self):
        is_pending_changes = False
        with self._do_reconnect_lock:
            self._is_pending_commit = False
            if self._is_abort_pending_txn:
                is_pending_changes = True
            self._is_abort_pending_txn = False

        if is_pending_changes:
            raise RuntimeError("Pending changes when reconnected to " + self.qe_address())

        _invoke_with_reconnect(self, None, lambda: self._delegator.commit())

    def rollback(self):
        is_pending_changes = False
        with self._do_reconnect_lock:
            if self._is_abort_pending_txn:  # no need to abort pending txn
                self._is_abort_pending_txn = False
                self._is_pending_commit = False
                is_pending_changes = True

        if is_pending_changes is False:
            _invoke_with_reconnect(self, None, lambda: self._delegator.rollback())
        with self._do_reconnect_lock:
            self._is_pending_commit = False

    def cursor(self, cursor_factory=None):
        result = MultiCursor(self, cursor_factory)
        self._cursors.append(result)
        return result

    def set_session(self, autocommit=None, readonly=None):
        _invoke_with_reconnect(self, None, lambda: self._delegator.set_session(autocommit, readonly))
        if autocommit is not None:
            with self._do_reconnect_lock:
                self._is_auto_commit = self._delegator.autocommit

    @property
    def autocommit(self):
        with self._do_reconnect_lock:
            result = self._is_auto_commit
        return result

    @autocommit.setter
    def autocommit(self, value):
        if self.autocommit is not value:
            _invoke_with_reconnect(self, None, lambda: self._delegator.set_autocommit(value))
            with self._do_reconnect_lock:
                self._is_auto_commit = self._delegator.autocommit

    @property
    def readonly(self):
        return self.readonly

    @readonly.setter
    def readonly(self, value):
        _invoke_with_reconnect(self, None, lambda: self._delegator.readonly(value))

    @property
    def transactionisolation(self):
        return self._delegator.transactionisolation

    @property
    def encoding(self):
        self._delegator.encoding

    def reconnect(self, addr=None):
        already_connected = False
        if addr is not None:
            with self._do_reconnect_lock:
                if self._force_reopen is False and self._qe_address == addr:
                    logger.debug("Already connected to " + str(self._qe_address))
                    already_connected = True
                else:
                    if self._is_auto_commit is False and self._is_pending_commit:
                        self._is_abort_pending_txn = True
                self._is_pending_commit = False
        if already_connected is False:
            logger.debug("reconnecting to ({} or {})".format(addr, self._qe_address))
            if addr:
                self._url = change_url_address(self._url, addr)
                self._qe_address = addr
            self._connect()
            is_auto_commit = self.autocommit
            if is_auto_commit != self._delegator.autocommit:
                self._delegator.set_session(autocommit=is_auto_commit)
        connection_manager().add_connection(self)

    def is_abort_pending_txn(self):
        with self._do_reconnect_lock:
            result = self._is_abort_pending_txn
        return result

    def is_pending_commit(self):
        with self._do_reconnect_lock:
            result = self._is_pending_commit
        return result

    def is_do_reconnect(self):
        with self._do_reconnect_lock:
            result = self._do_reconnect and self._is_pending_commit is False
        return result

    def is_force_reopen(self):
        with self._do_reconnect_lock:
            result = self._force_reopen
        return result

    def txn_update(self):
        with self._do_reconnect_lock:
            if self._is_auto_commit is False and self._is_pending_commit is False:
                self._is_pending_commit = True

    def do_reconnect(self):
        with self._do_reconnect_lock:
            self._do_reconnect = True
            self._force_reopen = False

    def invalidate_address(self):
        with self._do_reconnect_lock:
            self._do_reconnect = True
            self._force_reopen = self._is_pending_commit is False

    def unset_do_reconnect(self):
        with self._do_reconnect_lock:
            self._do_reconnect = False
            self._force_reopen = False

    @property
    def delegator(self):
        return self._delegator

    def connection_manager_info(self):
        return connection_manager().info()


class MultiCursor(object):

    def __init__(self, conn: MultiConnection, cursor_factory):
        self._closed = False
        self._connection = conn
        self._id = random.randint(0, 9999999)
        self._cursor_factory = cursor_factory
        self._delegator = None

    def __del__(self):
        if not self._connection.closed and not self._closed:
            try:
                self.close()
            except BaseException as ex:
                logger.debug("Ignoring exception while closing: {}".format(ex))
            finally:
                self._closed = True

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        try:
            if not self.closed:
                self.close()
        finally:
            self._closed = True

    def __iter__(self):
        return self

    def __next__(self):
        row = self.fetchone()
        if row is None:
            raise StopIteration
        return row

    next = __next__

    def get_connection(self):
        return self._connection

    def _get_delegator(self):
        if self._delegator is not None and self._delegator.closed and not self._closed:
            logger.debug("recreate cursor {}".format(self._id))
            self._delegator = None
        retries = 5
        while self._delegator is None and retries > 0:
            retries -= 1
            if self._connection.closed:
                raise RuntimeError('Connection is closed. No cursor available')
            try:
                self._delegator = self._connection.delegator.cursor(self._cursor_factory)
                self._delegator.set_xid(self._id)
            except BaseException as ex:
                logger.warning("Couldn't create cursor. Retrying.\n {}".format(ex))
                time.sleep(2 / 10)  # TODO make it configurable

        if self._delegator is None:
            raise RuntimeError('Cannot create cursor')
        return self._delegator

    def reset(self):
        logger.debug("reset cursor {}".format(self._id))
        self._delegator = None

    def close(self):
        try:
            _invoke_with_reconnect(self.get_connection(), self, lambda: self._get_delegator().close())
        finally:
            self._closed = True

    @property
    def closed(self):
        return self._closed

    @property
    def description(self):
        return self._get_delegator().description

    def get_tables(self, catalog=None, schemaPattern=None, tableNamePattern=None, typeList=None):
        return _invoke_with_reconnect(self.get_connection(), self,
                                             lambda: self._get_delegator().get_tables(catalog, schemaPattern,
                                                                                      tableNamePattern,
                                                                                      typeList))

    def get_schemas(self, catalog=None, schemaPattern=None):
        return _invoke_with_reconnect(self.get_connection(), self,
                                             lambda: self._get_delegator().get_schemas(catalog, schemaPattern))

    def get_catalogs(self):
        return _invoke_with_reconnect(self.get_connection(), self, lambda: self._get_delegator().get_catalogs())

    def get_columns(self, catalog=None, schemaPattern=None, tableNamePattern=None, columnNamePattern=None):
        return _invoke_with_reconnect(self.get_connection(), self,
                                             lambda: self._get_delegator().get_columns(catalog, schemaPattern,
                                                                                       tableNamePattern,
                                                                                       columnNamePattern))

    def get_table_types(self):
        return _invoke_with_reconnect(self.get_connection(), self, lambda: self._get_delegator().get_table_types())

    def get_type_info(self):
        return _invoke_with_reconnect(self.get_connection(), self, lambda: self._get_delegator().get_type_info())

    def execute(self, operation, parameters=None):
        result = _invoke_with_reconnect(self.get_connection(), self, lambda: self._get_delegator().execute(operation, parameters))
        self._connection.txn_update()
        return result

    def executemany(self, operation, seq_of_parameters):
        result = _invoke_with_reconnect(self.get_connection(), self,
                                               lambda: self._get_delegator().executemany(operation, seq_of_parameters))
        self._connection.txn_update()
        return result

    def executemany2(self, operation, seq_of_parameters):
        result = _invoke_with_reconnect(self.get_connection(), self,
                                               lambda: self._get_delegator().executemany2(operation, seq_of_parameters))
        self._connection.txn_update()
        return result

    def fetchone(self):
        return self._get_delegator().fetchone()

    def fetchone2(self):
        return self._get_delegator().fetchone2()

    def fetchmany(self, size=None):
        return self._get_delegator().fetchmany(size)

    def fetchall(self):
        return self._get_delegator().fetchall()

    def setinputsizes(self, sizes):
        self._get_delegator().setinputsizes(sizes)

    def setoutputsize(self, size, column=None):
        self._get_delegator().setoutputsize(size, column)

    @property
    def connection(self):
        return self._connection

    @property
    def rowcount(self):
        return self._get_delegator().rowcount

    @property
    def rownumber(self):
        return self._get_delegator().rownumber


class ServiceConnection(MultiConnection, ServiceConnectionI):

    def __init__(self, url, info):
        super().__init__(url, info)

    def unset_do_reconnect(self):
        with self._do_reconnect_lock:
            self._qe_address = None
            self._do_reconnect = False
            self._force_reopen = False

    def qe_addresses(self):
        if self is not None:
            raise RuntimeError('QE addresses service not implemented')
        res = _invoke_with_reconnect(self, None, lambda: self._delegator.serve_lx_action('QE_ADDRESSES'))
        if res:
            error = res.pop('ERROR', None)
            if error is None:
                return res['RESULT'].split(',')
            raise RuntimeError('Cannot get QE addresses: ' + error)
        raise IOError('Cannot get QE addresses')
