# Copyright 2015 Lukas Lalinsky
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import logging
import collections

from lxdbapi.types import javaTypetoNative, LXARRAY, typed_value_2_native, native_2_typed_value, LxRawReader, \
    LxTextReader, native_2_typed_value, BUF_SZ, LxBlobReader
from lxdbapi.errors import ProgrammingError, ArrayTypeException
from lxdbapi import common_pb2
import datetime

__all__ = ['Cursor', 'ColumnDescription', 'DictCursor']

logger = logging.getLogger(__name__)

# TODO see note in Cursor.rowcount()
MAX_INT = 2 ** 64 - 1

ColumnDescription = collections.namedtuple('ColumnDescription', 'name type_code display_size internal_size precision scale null_ok')
"""Named tuple for representing results from :attr:`Cursor.description`."""


class Cursor(object):
    """Database cursor for executing queries and iterating over results.

    You should not construct this object manually, use :meth:`Connection.cursor() <phoenixdb.connection.Connection.cursor>` instead.
    """

    arraysize = 1
    """
    Read/write attribute specifying the number of rows to fetch
    at a time with :meth:`fetchmany`. It defaults to 1 meaning to
    fetch a single row at a time.
    """

    itersize = 2000
    """
    Read/write attribute specifying the number of rows to fetch
    from the backend at each network roundtrip during iteration
    on the cursor. The default is 2000.
    """

    def __init__(self, connection):
        self.blobidgen = 0
        self._connection = connection
        self._xid = None
        self._id = None
        self._blob_map = dict()
        self._old_id = None
        self._prepared_sql = None
        self._signature = None
        self._column_data_types = []
        self._opened_blobs = dict()
        self._frame = None
        self._pos = None
        self._closed = False
        self.arraysize = self.__class__.arraysize
        self.itersize = self.__class__.itersize
        self._updatecount = -1
        self.lastrowid = None

    def __del__(self):
        if not self._connection.closed and not self._closed:
            try:
                self.close()
            except BaseException as ex:
                logger.debug("Ignoring exception while closing: {}".format(ex))
            finally:
                self._closed = True
                logger.debug("del: Closed cursor {}".format(self._xid))

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        if not self._closed:
            try:
                self.close()
            except BaseException as ex:
                logger.debug("Ignoring exception while closing: {}".format(ex))
            finally:
                self._closed = True
                logger.debug("exit: Closed cursor {}".format(self._xid))

    def __iter__(self):
        return self

    def __next__(self):
        row = self.fetchone()
        if row is None:
            raise StopIteration
        return row

    next = __next__

    def close(self):
        """Closes the cursor.
        No further operations are allowed once the cursor is closed.

        If the cursor is used in a ``with`` statement, this method will
        be automatically called at the end of the ``with`` block.
        """
        if self._closed:
            return
        if self._id is not None:
            try:
                self._connection._client.close_statement(self._connection._id, self._id)
            except BaseException as ex:
                logger.debug('Ignoring exception: {}'.format(ex))
            self._old_id = self._id
            self._id = None
            self._prepared_sql = None
        self._signature = None
        self._column_data_types = []
        self._reset_blobs()
        self._frame = None
        self._pos = None
        self._closed = True

    @property
    def closed(self):
        """Read-only attribute specifying if the cursor is closed or not."""
        return self._closed

    @property
    def description(self):
        if self._signature is None:
            return None
        description = []
        for column in self._signature.columns:
            description.append(ColumnDescription(
                column.column_name,
                column.type.name,
                column.display_size,
                None,
                column.precision,
                column.scale,
                None if column.nullable == 2 else bool(column.nullable),
            ))
        return description

    def set_xid(self, xid):
        self._xid = xid
        logger.debug('new xid [{}-{}]'. format(self._xid, self._id))

    def _reset_blobs(self):
        for bid, b in self._opened_blobs.items():
            b.close()
        self._opened_blobs.clear()
        for bid, b in self._blob_map.items():
            b.close(False)
        self._blob_map.clear()

    def _set_id(self, id):
        self._reset_blobs()
        if self._id is not None and self._id != id:
            logger.debug('[{}]Closing statement {}'.format(self._xid, self._id))
            self._prepared_sql = None
            self._connection._client.close_statement(self._connection._id, self._id)
        logger.debug('[{}]Setting statement id {}'.format(self._xid, id))
        self._old_id = self._id
        self._id = id

    def _set_signature(self, signature):
        self._signature = signature
        self._column_data_types = []
        if signature is None:
            return

        for column in signature.columns:
            cn = getattr(column, 'column_class_name')
            tp = getattr(column, 'type')
            sqltype = getattr(tp, 'id')
            nat = javaTypetoNative(cn, sqltype)
            self._column_data_types.append(nat)


    def _set_frame(self, frame):
        self._log_frame("set frame(previous): ")
        self._frame = frame
        self._pos = None
        self._reset_blobs()

        if frame is not None:
            if frame.rows:
                self._pos = 0
            #elif not frame.done:
                #print('got an empty frame, but the statement is not done yet')
                #raise InternalError('got an empty frame, but the statement is not done yet')
        self._log_frame("set frame: ")

    def _log_frame(self, prefix):
        if logger.isEnabledFor(logging.DEBUG):
            if self._frame:
                if self._frame.rows:
                    nlines = str(len(self._frame.rows))
                else:
                    nlines = 'frame.rows is null'
            else:
                nlines = 'frame is null'
            logger.debug('{} statement [{}-{}], pos [{}], frame length [{}]'.
                         format(prefix, self._xid, self._id, self._pos, nlines))

    def _fetch_next_frame(self):
        offset = self._frame.offset + len(self._frame.rows)
        logger.debug('next frame: statement [{}-{}], pos [{}], offset [{}]'.
                     format(self._xid, self._id, self._pos, offset))
        frame = self._connection._client.fetch(
            self._connection._id, self._id,
            offset=offset, frame_max_size=self.itersize)
        self._set_frame(frame)

    def _process_results(self, results):
        if results:
            result = results[0]
            if result.own_statement:
                logger.debug('Own statement: {}'.format(result.statement_id))
                self._set_id(result.statement_id)
            logger.debug('first frame for statement [{}]'.format(self._id))
            self._set_signature(result.signature)
            self._set_frame(result.first_frame)
            self._updatecount = result.update_count
        else:
            logger.debug('no results for cursor [{}]'.format(self._xid))

    def _transform_parameters(self, parameters):
        res = []
        parameters_list = list(parameters)
        for idx, param in enumerate(parameters_list):
            tv = native_2_typed_value(param, self)
            res.append(tv)
        return res


    def get_tables(self, catalog=None, schemaPattern=None, tableNamePattern=None, typeList=None):
        if self._closed:
            raise ProgrammingError('the cursor is already closed(get_tables)')
        results = self._connection._client.get_tables(self._connection._id, catalog,
                                                      schemaPattern, tableNamePattern, typeList)

        self._process_results([results])

    def get_schemas(self, catalog=None, schemaPattern=None):
        if self._closed:
            raise ProgrammingError('the cursor is already closed(get_schemas)')
        results = self._connection._client.get_schemas(
            self._connection._id, catalog, schemaPattern)

        self._process_results([results])

    def get_catalogs(self):
        if self._closed:
            raise ProgrammingError('the cursor is already closed(get_catalogs)')
        results = self._connection._client.get_catalogs(
            self._connection._id)

        self._process_results([results])

    def get_columns(self, catalog=None, schemaPattern=None, tableNamePattern=None, columnNamePattern=None):
        if self._closed:
            raise ProgrammingError('the cursor is already closed(get_columns)')

        results = self._connection._client.get_columns(self._connection._id, catalog,
                                                      schemaPattern, tableNamePattern, columnNamePattern)
        self._process_results([results])

    def get_table_types(self):
        if self._closed:
            raise ProgrammingError('the cursor is already closed(get_table_types)')
        results = self._connection._client.get_table_types(
            self._connection._id)

        self._process_results([results])

    def get_type_info(self):
        if self._closed:
            raise ProgrammingError('the cursor is already closed(get_type_info)')
        results = self._connection._client.get_type_info(
            self._connection._id)

        self._process_results([results])

    def add_blob(self, b: LxRawReader):
        if self.closed:
            raise RuntimeError('the cursor is already closed(execute)')
        bid = self.blobidgen
        self.blobidgen += 1
        self._opened_blobs[bid] = b
        return bid

    def add_blob_reader(self, b: LxBlobReader):
        if self.closed:
            raise RuntimeError('the cursor is already closed(execute)')
        self._blob_map[b.first.info.id] = b

    def read_blob(self, bid, offset):
        if self.closed:
            raise RuntimeError('the cursor is already closed(execute)')
        if self._connection is None or self._connection._id is None:
            raise RuntimeError('No connection to read the blob from')
        if self._id is None:
            raise RuntimeError('No statement to read the blob from')
        cid = self._connection._id
        stid = self._id
        return self._connection._client.read_blob(cid, stid, bid, offset)


    def execute(self, operation, parameters=None):
        if self._closed:
            raise ProgrammingError('the cursor is already closed(execute)')
        self._updatecount = -1
        self._set_frame(None)
        if parameters is None or len(parameters) == 0:
            if self._id is None or self._prepared_sql is not None:
                logger.debug('(execute)Creating statement')
                self._set_id(self._connection._client.create_statement(self._connection._id))
            logger.debug('(execute)Prepare and Execute statement {}: {}'.format(self._id, operation))
            results = self._connection._client.prepare_and_execute(
                self._connection._id, self._id,
                operation, -1, self.itersize)
            self._process_results(results)
        else:
            if operation is not self._prepared_sql:
                statement = self._connection._client.prepare(self._connection._id, operation, -1)
                logger.debug('(execute)Prepared statement {}: {}'.format(statement.id, operation))
                self._set_id(statement.id)
                self._set_signature(statement.signature)
                self._prepared_sql = operation

            logger.debug('(execute)Executing statement {}'.format(self._id))

            execresp = self._connection._client.execute(
                self._connection._id, self._id, self._signature, self._transform_parameters(parameters),
                first_frame_max_size=self.itersize)
            execresp = self._sendpendingblobs(execresp)
            self._process_results(execresp.results)

    def _nextbmsg(self, bi):
        lxblob = self._opened_blobs.get(bi.id, None)
        if lxblob is None:
            raise ProgrammingError(f"blob {bi.id} doesn't exist")
        bmsg = common_pb2.LxBlobMsg()
        bmsg.info.id = bi.id
        if lxblob.closed:
            bmsg.info.done = True
            bmsg.info.offset = lxblob.offset
            bmsg.bytes_value = bytearray(0)
            return bmsg
        bv = lxblob.read(BUF_SZ)
        if bv is None:
            bmsg.bytes_value = bytes(0)
        else:
            bmsg.bytes_value = bv
        bmsg.info.done = lxblob.closed
        bmsg.info.offset = lxblob.offset
        return bmsg

    def _sendpendingblobs(self, execresp):
        while execresp is not None:
            pending = list()
            for rs in execresp.results:
                for bi in rs.pending_blobs:
                    bmsg = self._nextbmsg(bi)
                    pending.append(bmsg)
            if len(pending) == 0:
                break
            execresp = self._connection._client.writeBlob(self._connection._id, self._id, pending)
        return execresp

    def _batchsendpendingblobs(self, execresp):
        while execresp is not None:
            pending = list()
            for bi in execresp.pending_blobs:
                bmsg = self._nextbmsg(bi)
                pending.append(bmsg)
            if len(pending) == 0:
                break
            execresp = self._connection._client.writeBlobBatch(self._connection._id, self._id, pending)
        return execresp

    def executemany(self, operation, seq_of_parameters):
        if self._closed:
            raise ProgrammingError('the cursor is already closed(executemany)')
        op = operation.split()[0]
        if op.upper() == "SELECT":
            raise ProgrammingError('You cannot execute SELECT statements in executemany()')
        self._updatecount = -1
        self._set_frame(None)
        if operation is not self._prepared_sql:
            statement = self._connection._client.prepare(self._connection._id, operation, max_rows_total=-1)
            logger.debug('(executemany)Prepared statement id {}: {}'.format(statement.id, operation))
            self._set_id(statement.id)
            self._set_signature(statement.signature)
            self._prepared_sql = operation
        logger.debug('(executemany)Executing statement id {}'.format(self._id))
        resp = self._connection._client.executeBatch(self._connection._id, self._id, self._signature,
                                         [self._transform_parameters(parameters) for parameters in seq_of_parameters], first_frame_max_size=self.itersize)

        resp = self._batchsendpendingblobs(resp)
        return resp.update_counts

    def executemany2(self, operation, seq_of_parameters):
        if self._closed:
            raise ProgrammingError('the cursor is already closed(executemany2)')
        self._updatecount = -1
        self._set_frame(None)
        statement = self._connection._client.prepare(
            self._connection._id, operation, 0)
        stmt_id = statement.get('id')
        logger.debug('(executemany2) Prepared statement {}: {}'.format(stmt_id, operation))
        self._set_id(stmt_id)
        self._set_signature(statement.get('signature'))
        for parameters in seq_of_parameters:
            logger.debug('(executemany2) Executing statement: {}'.format(stmt_id))
            self._connection._client.execute(
                statement, self.itersize,
                [parameters])

    def _transform_row(self, row):
        """Transforms a Row into Python values.

        :param row:
            A ``common_pb2.Row`` object.

        :returns:
            A list of values casted into the correct Python types.

        :raises:
            NotImplementedError
        """
        tmp_row = []

        for i, column in enumerate(row.value):
            if column.has_array_value:
                raise NotImplementedError('array types are not supported')
            elif column.scalar_value.null:
                tmp_row.append(None)
            else:
                field_name, rep, mutate_to, cast_from = self._column_data_types[i]

                # get the value from the field_name
                value = getattr(column.scalar_value, field_name)

                # cast the value
                if cast_from is not None:
                    value = cast_from(value)

                tmp_row.append(value)
        return tmp_row

    def fetchone(self):
        result_row = []
        self._log_frame("fetchone: ")
        if self._frame is None:
            logger.debug('fetchone from null frame: id [{}-{}], previous id [{}]'.
                         format(self._xid, self._id, self._old_id))
            return None
        if self._pos is None:
            return None
        rows = self._frame.rows
        row = rows[self._pos]
        self._pos += 1
        if self._pos >= len(rows):
            self._pos = None
            if not self._frame.done:
                self._fetch_next_frame()
        for value, data_type in zip(row.value, self._column_data_types):
            if value.scalar_value.null:
                result_row.append(None)
            else:
                if data_type[1] is not None:
                    val = data_type[1](getattr(value.scalar_value, data_type[2]))
                    if isinstance(val, datetime.datetime):
                        val = val.astimezone()
                    result_row.append(val)
                else:
                    nat = typed_value_2_native(value.scalar_value, self)
                    if data_type[3] == 2005:
                        if isinstance(nat, LxRawReader):
                            nat = LxTextReader(nat, self._connection.codeci)
                        else:
                            nat = self._connection.codeci.decode(nat)[0]
                    result_row.append(nat)

        return tuple(result_row)

    def fetchone2(self):
        self._log_frame("fetchone2: ")
        if self._frame is None:
            logger.debug('fetchone2 from null frame: id [{}-{}], previous id [{}]'.
                         format(self._xid, self._id, self._old_id))
            return None
        if self._pos is None:
            return None
        rows = self._frame.rows
        row = rows[self._pos]
        #row = self._transform_row(rows[self._pos])
        self._pos += 1
        if self._pos >= len(rows):
            self._pos = None
            if not self._frame.done:
                self._fetch_next_frame()
        return [row]

    def fetchmany(self, size=None):
        if size is None:
            size = self.arraysize
        rows = []
        while size > 0:
            row = self.fetchone()
            if row is None:
                break
            rows.append(row)
            size -= 1
        return rows

    def fetchall(self):
        rows = []
        while True:
            row = self.fetchone()
            if row is None:
                break
            rows.append(row)
        return rows

    def setinputsizes(self, sizes):
        pass

    def setoutputsize(self, size, column=None):
        pass

    @property
    def connection(self):
        """Read-only attribute providing access to the :class:`Connection <phoenixdb.connection.Connection>`
        object this cursor was created from."""
        return self._connection

    @property
    def rowcount(self):
        """Read-only attribute specifying the number of rows affected by
        the last executed DML statement or -1 if the number cannot be
        determined. Note that this will always be set to -1 for select
        queries."""
        # TODO instead of -1, this ends up being set to Integer.MAX_VALUE
        if self._updatecount == MAX_INT:
            return -1
        return self._updatecount

    @property
    def rownumber(self):
        """Read-only attribute providing the current 0-based index of the
        cursor in the result set or ``None`` if the index cannot be
        determined.

        The index can be seen as index of the cursor in a sequence
        (the result set). The next fetch operation will fetch the
        row indexed by :attr:`rownumber` in that sequence.
        """
        if self._frame is not None and self._pos is not None:
            return self._frame.offset + self._pos
        return self._pos


class DictCursor(Cursor):
    """A cursor which returns results as a dictionary"""

    def _transform_row(self, row):
        row = super(DictCursor, self)._transform_row(row)
        d = {}
        for ind, val in enumerate(row):
            d[self._signature.columns[ind].column_name] = val
        return d
