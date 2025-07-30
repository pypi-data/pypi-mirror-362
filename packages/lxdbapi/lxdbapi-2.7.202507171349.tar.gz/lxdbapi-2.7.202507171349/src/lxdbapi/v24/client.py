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

"""Implementation of the JSON-over-HTTP RPC protocol used by Avatica."""

import pprint
import logging

from lxdbapi import errors, responses_pb2, requests_pb2
from lxdbapi.types import native_2_typed_value, typed_value_2_native
from lxdbapi.network_avatica_connection import TcpAvaticaConnection, NetAvaticaConnection
from lxdbapi import common_pb2
from importlib import import_module

from lxdbapi import versions

try:
    import urlparse
except ImportError:
    import urllib.parse as urlparse

try:
    from HTMLParser import HTMLParser
except ImportError:
    from html.parser import HTMLParser

__all__ = ['AvaticaClient', 'native_2_typed_value', 'typed_value_2_native']

logger = logging.getLogger(__name__)
AVATICA_CLASS_BASE = "org.apache.calcite.avatica.proto"

clivers = f'{versions.MAJOR_VERSION}.{versions.MINOR_VERSION}'


def get_class(kls):
    """Get class given a fully qualified name of a class"""
    parts = kls.split('$')
    class_ = getattr(import_module("lxdbapi.responses_pb2"), parts[1])
    rv = class_()
    return rv


def parse_url(url):
    url = urlparse.urlparse(url)
    if not url.scheme and not url.netloc and url.path:
        netloc = url.path
        if ':' not in netloc:
            netloc = '{}:8765'.format(netloc)
        return urlparse.ParseResult('http', netloc, '/', '', '', '')
    return url


# Defined in phoenix-core/src/main/java/org/apache/phoenix/exception/SQLExceptionCode.java
SQLSTATE_ERROR_CLASSES = [
    ('08', errors.OperationalError),  # Connection Exception
    ('22018', errors.IntegrityError),  # Constraint violatioin.
    ('22', errors.DataError),  # Data Exception
    ('23', errors.IntegrityError),  # Constraint Violation
    ('24', errors.InternalError),  # Invalid Cursor State
    ('25', errors.InternalError),  # Invalid Transaction State
    ('42', errors.ProgrammingError),  # Syntax Error or Access Rule Violation
    ('XLC', errors.OperationalError),  # Execution exceptions
    ('INT', errors.InternalError),  # Phoenix internal error
]

# Relevant properties as defined by https://calcite.apache.org/avatica/docs/client_reference.html
OPEN_CONNECTION_PROPERTIES = (
    'database',
    'schema',
    'databaseName',
    'user',  # User for the database connection
    'password',  # Password for the user
    'parallel',
    'txn_mode',
    'is_kryo',
    'autoCommit',
    'appTimeZone'
)

ONLY_CLIENT_PROPERTIES = ('distribute', 'encoding')


class AvaticaClient(object):
    """Client for Avatica's RPC server.

    This exposes all low-level functionality that the Avatica
    server provides, using the native terminology. You most likely
    do not want to use this class directly, but rather get connect
    to a server using :func:`connect`.
    """
    connection: NetAvaticaConnection = None

    def __init__(self, url, max_retries=None, avatica_con=None, **kwargs):
        """Constructs a new client object.

        :param url:
            URL of an Avatica RPC server.
        """
        self.url = parse_url(url)
        self.max_retries = max_retries if max_retries is not None else 3
        self.avatica_con = avatica_con
        if kwargs is None or 'secure' not in kwargs.keys():
            self.secure = False
        else:
            self.secure = kwargs['secure']

    def set_avatica_con(self, avatica_con):
        self.avatica_con = avatica_con

    def connect(self):
        self.connection = TcpAvaticaConnection(self.url, self.secure, self.max_retries)

    def close(self):
        if self.connection is not None:
            self.connection.close()

    def _apply(self, request_data):
        logger.debug("Sending request\n%s", request_data)
        if self.connection is None:
            raise IOError('No opened Connection')
        request_name = request_data.__class__.__name__

        req_message = common_pb2.WireMessage()
        req_message.name = AVATICA_CLASS_BASE + ".Requests$" + request_data.__class__.__name__
        req_message.wrapped_message = request_data.SerializeToString()

        body = req_message.SerializeToString()
        response_body = self.connection.request(body)
        if response_body is None:
            raise IOError(f"IO Error on [{self.url}] while expecting a response [{request_name}]")
        # deserialize WireMessage
        resp_message = common_pb2.WireMessage()
        resp_message.ParseFromString(response_body)

        logger.debug("Received response\n%s", resp_message)

        if resp_message.name == 'org.apache.calcite.avatica.proto.Responses$ErrorResponse':
            # Decode the error response to provide a full Error Message:

            errorresponse = get_class(resp_message.name)
            errorresponse.ParseFromString(resp_message.wrapped_message)

            for exception in errorresponse.exceptions:
                exceptionmessage = exception.split('\n')[0]
                if 'NoSuchConnectionException' in exceptionmessage:
                    if self.avatica_con is not None:
                        logger.debug("No such connection exception. Trying to reconnect...")
                        self.avatica_con.open()
                        logger.debug("Successfully opened a new connection")
                        self.set_avatica_con(self.avatica_con)
                        logger.debug("Sending request\n%s", pprint.pformat(request_data))
                        request_data.connection_id = self.avatica_con._id
                        request_name = request_data.__class__.__name__

                        req_message = common_pb2.WireMessage()
                        req_message.name = AVATICA_CLASS_BASE + ".Requests$" + request_data.__class__.__name__
                        req_message.wrapped_message = request_data.SerializeToString()

                        body = req_message.SerializeToString()
                        response_body = self.connection.request(body)
                        # deserialize WireMessage

                        resp_message = common_pb2.WireMessage()
                        resp_message.ParseFromString(response_body)

                        logger.debug("Received response\n%s", resp_message)
                    else:
                        raise errors.InterfaceError(errorresponse.error_message, code=errorresponse.error_code,
                                                    sqlstate=errorresponse.sql_state)
                    break
            if resp_message.name == 'org.apache.calcite.avatica.proto.Responses$ErrorResponse':
                # Decode the error response to provide a full Error Message:
                errorresponse = get_class(resp_message.name)
                errorresponse.ParseFromString(resp_message.wrapped_message)
                raise errors.InterfaceError(errorresponse.error_message, code=errorresponse.error_code,
                                            sqlstate=errorresponse.sql_state,
                                            cause=errorresponse.exceptions)

        return resp_message.wrapped_message

        '''# deserialize response
        response = get_class(wire_message.name)
        response.ParseFromString(wire_message.wrapped_message)'''

        '''if type(response) is responses_pb2.ErrorResponse():
            raise errors.InterfaceError(response.error_message, code=response.error_code, sqlstate=response.sql_state,
                                        cause=response.exceptions)
        return response'''

    def get_catalogs(self, connection_id):
        request = requests_pb2.CatalogsRequest()
        request.connection_id = connection_id
        response_data = self._apply(request)
        response = responses_pb2.ResultSetResponse()
        response.ParseFromString(response_data)
        return response

    def get_schemas(self, connection_id, catalog=None, schemaPattern=None):
        request = requests_pb2.SchemasRequest()
        request.connection_id = connection_id
        if catalog is not None:
            request.catalog = catalog
        if schemaPattern is not None:
            request.schema_pattern = schemaPattern
        response_data = self._apply(request)
        response = responses_pb2.ResultSetResponse()
        response.ParseFromString(response_data)
        return response

    def get_tables(self, connection_id, catalog=None, schemaPattern=None, tableNamePattern=None, typeList=None):
        request = requests_pb2.TablesRequest()
        request.connection_id = connection_id
        if catalog is not None:
            request.catalog = catalog
            request.has_catalog = True
        if schemaPattern is not None:
            request.schema_pattern = schemaPattern
            request.has_schema_pattern = True
        if tableNamePattern is not None:
            request.table_name_pattern = tableNamePattern
            request.has_table_name_pattern = True
        if typeList is not None:
            request.has_type_list = True
            request.type_list.extend(typeList)
        request.has_type_list = typeList is not None
        response_data = self._apply(request)
        response = responses_pb2.ResultSetResponse()
        response.ParseFromString(response_data)
        return response

    def get_columns(self, connection_id, catalog=None, schemaPattern=None, tableNamePattern=None,
                    columnNamePattern=None):
        request = requests_pb2.ColumnsRequest()
        request.connection_id = connection_id
        if catalog is not None:
            request.catalog = catalog
        if schemaPattern is not None:
            request.schema_pattern = schemaPattern
        if tableNamePattern is not None:
            request.table_name_pattern = tableNamePattern
        if columnNamePattern is not None:
            request.column_name_pattern = columnNamePattern
        response_data = self._apply(request)
        response = responses_pb2.ResultSetResponse()
        response.ParseFromString(response_data)
        return response

    def get_table_types(self, connection_id):
        request = requests_pb2.TableTypesRequest()
        request.connection_id = connection_id
        response_data = self._apply(request)
        response = responses_pb2.ResultSetResponse()
        response.ParseFromString(response_data)
        return response

    def get_type_info(self, connection_id):
        request = requests_pb2.TypeInfoRequest()
        request.connection_id = connection_id
        response_data = self._apply(request)
        response = responses_pb2.ResultSetResponse()
        response.ParseFromString(response_data)
        return response

    def connection_sync(self, connection_id, connProps=None):
        """Synchronizes connection properties with the server.

        :param connection_id:
            ID of the current connection.

        :param connProps:
            Dictionary with the properties that should be changed.

        :returns:
            A ``common_pb2.ConnectionProperties`` object.
        """
        if connProps is None:
            connProps = {}

        request = requests_pb2.ConnectionSyncRequest()
        request.connection_id = connection_id
        request.conn_props.auto_commit = connProps.get('autoCommit', False)
        request.conn_props.has_auto_commit = True
        request.conn_props.read_only = connProps.get('readOnly', False)
        request.conn_props.has_read_only = True
        request.conn_props.transaction_isolation = connProps.get('transactionIsolation', 0)
        request.conn_props.catalog = connProps.get('catalog', '')
        request.conn_props.schema = connProps.get('schema', '')

        response_data = self._apply(request)
        response = responses_pb2.ConnectionSyncResponse()
        response.ParseFromString(response_data)
        return response.conn_props

    def open_connection(self, connection_id, info=None):
        """Opens a new connection.

        :param connection_id:
            ID of the connection to open.
        """
        request = requests_pb2.OpenConnectionRequest()
        request.connection_id = connection_id
        if info is not None:
            # Info is a list of repeated pairs, setting a dict directly fails
            request.info["LXJDBCVERS"] = clivers
            for k, v in info.items():
                request.info[k] = v

        response_data = self._apply(request)
        response = responses_pb2.OpenConnectionResponse()
        response.ParseFromString(response_data)

    def close_connection(self, connection_id):
        """Closes a connection.

        :param connection_id:
            ID of the connection to close.
        """
        request = requests_pb2.CloseConnectionRequest()
        request.connection_id = connection_id
        self._apply(request)

    def create_statement(self, connection_id):
        """Creates a new statement.

        :param connection_id:
            ID of the current connection.

        :returns:
            New statement ID.
        """
        request = requests_pb2.CreateStatementRequest()
        request.connection_id = connection_id

        response_data = self._apply(request)
        response = responses_pb2.CreateStatementResponse()
        response.ParseFromString(response_data)
        return response.statement_id

    def close_statement(self, connection_id, statement_id):
        """Closes a statement.

        :param connection_id:
            ID of the current connection.

        :param statement_id:
            ID of the statement to close.
        """
        request = requests_pb2.CloseStatementRequest()
        request.connection_id = connection_id
        request.statement_id = statement_id

        self._apply(request)

    def prepare_and_execute(self, connection_id, statement_id, sql, max_rows_total=None, first_frame_max_size=None):
        """Prepares and immediately executes a statement.

        :param connection_id:
            ID of the current connection.

        :param statement_id:
            ID of the statement to prepare.

        :param sql:
            SQL query.

        :param max_rows_total:
            The maximum number of rows that will be allowed for this query.

        :param first_frame_max_size:
            The maximum number of rows that will be returned in the first Frame returned for this query.

        :returns:
            Result set with the signature of the prepared statement and the first frame data.
        """
        request = requests_pb2.PrepareAndExecuteRequest()
        request.connection_id = connection_id
        request.statement_id = statement_id
        request.sql = sql
        if max_rows_total is not None:
            request.max_rows_total = max_rows_total
        if first_frame_max_size is not None:
            request.first_frame_max_size = first_frame_max_size

        response_data = self._apply(request)
        response = responses_pb2.ExecuteResponse()
        response.ParseFromString(response_data)
        return response.results

    def prepare(self, connection_id, sql, max_rows_total=None):
        """Prepares a statement.

        :param connection_id:
            ID of the current connection.

        :param sql:
            SQL query.

        :param max_rows_total:
            The maximum number of rows that will be allowed for this query.

        :returns:
            Signature of the prepared statement.
        """
        request = requests_pb2.PrepareRequest()
        request.connection_id = connection_id
        request.sql = sql
        if max_rows_total is not None:
            request.max_rows_total = max_rows_total

        response_data = self._apply(request)
        response = responses_pb2.PrepareResponse()
        response.ParseFromString(response_data)
        return response.statement

    def switch(self, type):
        switcher = {
            'INTEGER': ['number_value', 12]

        }
        return switcher.get(type)

    def build_parameter_values(self, parameter_values, signature):
        parameters_typed = []
        for index, param in enumerate(parameter_values):
            param_data_type = signature.parameters[index].type_name
            valueTemp = common_pb2.TypedValue()
            if (self.switch(param_data_type)[0] == 'number_value'):
                valueTemp.number_value = param
            parameters_typed.append(valueTemp)
        return parameters_typed

    def execute(self, connection_id, statement_id, signature, parameter_values=None, first_frame_max_size=None):
        """Returns a frame of rows.

        The frame describes whether there may be another frame. If there is not
        another frame, the current iteration is done when we have finished the
        rows in the this frame.

        :param connection_id:
            ID of the current connection.

        :param statement_id:
            ID of the statement to fetch rows from.

        :param signature:
            common_pb2.Signature object

        :param parameter_values:
            A list of parameter values, if statement is to be executed; otherwise ``None``.

        :param first_frame_max_size:
            The maximum number of rows that will be returned in the first Frame returned for this query.

        :returns:
            ExecuteResponse
        """
        request = requests_pb2.ExecuteRequest()
        request.statementHandle.id = statement_id
        request.statementHandle.connection_id = connection_id
        request.statementHandle.signature.CopyFrom(signature)
        if parameter_values is not None:
            request.parameter_values.extend(parameter_values)
            request.has_parameter_values = True
        if first_frame_max_size is not None:
            request.first_frame_max_size = first_frame_max_size

        response_data = self._apply(request)
        response = responses_pb2.ExecuteResponse()
        response.ParseFromString(response_data)
        return response

    def writeBlob(self, connection_id, statement_id, blob_values):
        request = requests_pb2.WriteBlobRequest()
        request.connection_id = connection_id
        request.statement_id = statement_id
        for b in blob_values:
            request.blob_values.append(b)

        response_data = self._apply(request)
        response = responses_pb2.ExecuteResponse()
        response.ParseFromString(response_data)
        return response

    def executeBatch(self, connection_id, statement_id, signature, parameter_values=None, first_frame_max_size=None):
        """Returns a frame of rows

            The frame describes whether there may be another frame. If there is not
            another frame, the current iteration is done when we have finished the
            rows in the this frame.

            :param connection_id:
                ID of the current connection.

            :param statement_id:
                ID of the statement to fetch rows from.

            :param signature:
                common_pb2.Signature object

            :param parameter_values:
                A list of list of parameter values, if statement is to be executed; otherwise ``None``.

            :param first_frame_max_size:
                The maximum number of rows that will be returned in the first Frame returned for this query.

            :returns:
               ExecuteBatchResponse
        """
        request = requests_pb2.ExecuteBatchRequest()
        request.statement_id = statement_id
        request.connection_id = connection_id
        if parameter_values is not None:
            for parameter in parameter_values:
                updateBatch = requests_pb2.UpdateBatch()
                updateBatch.parameter_values.extend(parameter)
                request.updates.extend((updateBatch,))

        response_data = self._apply(request)
        response = responses_pb2.ExecuteBatchResponse()
        response.ParseFromString(response_data)
        return response

    def writeBlobBatch(self, connection_id, statement_id, blob_values):
        request = requests_pb2.WriteBlobBatchRequest()
        request.connection_id = connection_id
        request.statement_id = statement_id
        for b in blob_values:
            request.blob_values.append(b)

        response_data = self._apply(request)
        response = responses_pb2.ExecuteBatchResponse()
        response.ParseFromString(response_data)
        return response

    def fetch(self, connection_id, statement_id, offset=0, frame_max_size=None):
        """Returns a frame of rows.

        The frame describes whether there may be another frame. If there is not
        another frame, the current iteration is done when we have finished the
        rows in the this frame.

        :param connection_id:
            ID of the current connection.

        :param statement_id:
            ID of the statement to fetch rows from.

        :param offset:
            Zero-based offset of first row in the requested frame.

        :param frame_max_size:
            Maximum number of rows to return; negative means no limit.

        :returns:
            Frame data, or ``None`` if there are no more.
        """
        request = requests_pb2.FetchRequest()
        request.connection_id = connection_id
        request.statement_id = statement_id
        request.offset = offset
        if frame_max_size is not None:
            request.frame_max_size = frame_max_size
            # request.frame_max_size = -1

        response_data = self._apply(request)
        response = responses_pb2.FetchResponse()
        response.ParseFromString(response_data)
        return response.frame

    def commit(self, connectionId):
        request = requests_pb2.CommitRequest(connection_id=connectionId)

        response_data = self._apply(request)
        response = responses_pb2.CommitResponse()
        response.ParseFromString(response_data)

    def rollback(self, connectionId):
        request = requests_pb2.RollbackRequest(connection_id=connectionId)

        response_data = self._apply(request)
        response = responses_pb2.RollbackResponse()
        response.ParseFromString(response_data)

    def read_blob(self, connection_id, statement_id, blob_id, offset):
        request = requests_pb2.ReadBlobRequest()
        request.connection_id = connection_id
        request.statement_id = statement_id
        request.blob_info.id = blob_id
        request.blob_info.offset = offset
        request.blob_info.done = False
        response_data = self._apply(request)
        response = responses_pb2.ReadBlobResponse()
        response.ParseFromString(response_data)
        return response.blob_value

    def serve_lx_action(self, action, params=None):
        request = requests_pb2.LxActionRequest()
        request.action = action
        if params is not None:
            request.params = list()
            for k, v in params.items():
                param = common_pb2.KeyValuePair()
                param.key = k
                param.value = native_2_typed_value(v, None)
                request.params.append(param)
        response = None
        try:
            response_data = self._apply(request)
            if response_data:
                response = responses_pb2.LxActionResponse()
                response.ParseFromString(response_data)
        except BaseException as ex:
            raise ex

        result = {}
        if response and response.params:
            for info in response.params:
                result[info.key] = typed_value_2_native(info.value, None)
        else:
            logger.debug('No response for LxAction')

        return result


