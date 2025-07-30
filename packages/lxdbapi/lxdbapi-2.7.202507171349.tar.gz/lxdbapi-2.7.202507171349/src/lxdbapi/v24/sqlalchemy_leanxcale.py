# Copyright 2017 Dimitri Capitaine
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
from ._vendor.future.standard_library import install_aliases
install_aliases()

import urllib.parse
import lxdbapi

from sqlalchemy.engine.default import DefaultDialect

from sqlalchemy.sql.compiler import DDLCompiler, SQLCompiler
from sqlalchemy.sql import compiler
from sqlalchemy.engine import default

from sqlalchemy import types, BigInteger, Float
from sqlalchemy.types import INTEGER, BIGINT, SMALLINT, VARCHAR, CHAR, \
    FLOAT, DATE, BOOLEAN, DECIMAL, TIMESTAMP, TIME, VARBINARY


class LeanxcaleCompiler(SQLCompiler):
    def visit_sequence(self, seq):
        return "NEXT VALUE FOR %s" % seq.name

class LeanxcaleDDLCompiler(DDLCompiler):

    def visit_primary_key_constraint(self, constraint):
        # if constraint.name is None:
        #    raise CompileError("can't create primary key without a name")
        return DDLCompiler.visit_primary_key_constraint(self, constraint)

    def visit_sequence(self, seq):
        return "NEXT VALUE FOR %s" % seq.name

class LeanxcaleExecutionContext(default.DefaultExecutionContext):

    def should_autocommit_text(self, statement):
        pass

    def create_server_side_cursor(self):
        pass

    def fire_sequence(self, seq, type_):
        return self._execute_scalar(
            (
                    "SELECT NEXT VALUE FOR %s"
                    % seq.name
            ),
            type_
        )


class LeanXcaleIdentifierPreparer(compiler.IdentifierPreparer):

    def __init__(self, dialect, server_ansiquotes=False, **kw):

        quote = '"'

        super(LeanXcaleIdentifierPreparer, self).__init__(
            dialect, initial_quote=quote, escape_quote=quote
        )

    def _quote_free_identifiers(self, *ids):
        """Unilaterally identifier-quote any number of strings."""

        return tuple([self.quote_identifier(i) for i in ids if i is not None])

class LeanXcaleGenericTypeCompiler(compiler.GenericTypeCompiler):
    def visit_ARRAY(self, type_, **kw):
        if type_.item_type.python_type == int:
            return "BIGINT ARRAY"
        elif type_.item_type.python_type == float:
            return "DOUBLE ARRAY"
        elif type_.item_type.python_type == str:
            return "VARCHAR ARRAY"
        else:
            raise Exception("ARRAY of type {} is not supported".format(str(type_)))


class LeanxcaleDialect(DefaultDialect):
    name = "leanxcale"

    driver = "lxdbapi"

    ddl_compiler = LeanxcaleDDLCompiler
    preparer = LeanXcaleIdentifierPreparer
    statement_compiler = LeanxcaleCompiler
    type_compiler = LeanXcaleGenericTypeCompiler

    supports_sequences = True
    sequences_optional = True
    supports_multivalues_insert = True

    execution_ctx_cls = LeanxcaleExecutionContext

    preexecute_autoincrement_sequences = True

    @classmethod
    def dbapi(cls):

        return lxdbapi

    def create_connect_args(self, url):

        # Deal with PARALLEL option
        parallel = url.query.get('parallel')

        # Deal with SECURE option
        secure = url.query.get('secure')

        distribute = url.query.get('distribute')

        appTimeZone = url.query.get('appTimeZone')

        schname = url.query.get('schema')

        leanxcale_url = urllib.parse.urlunsplit(urllib.parse.SplitResult(
            scheme='http',
            netloc='{}:{}'.format(url.host, url.port or 8765),
            path='/',
            query=urllib.parse.urlencode(url.query),
            fragment='',
        ))
        if url.query.get('autocommit') == 'False':
            autocommit = False
        else:
            autocommit = True

        params = {'autocommit': autocommit, 'user': url.username}
        if parallel is not None:
            params.update({'parallel': parallel})
        if secure is not None:
            params.update({'secure': secure})
        if distribute is not None:
            params.update({'distribute': distribute})
        if url.password is not None:
            params.update({'password': url.password})
        if appTimeZone is not None:
            params.update({'appTimeZone': appTimeZone})
        if schname is not None:
            params.update({'schema': schname})

        params.update({'database': url.database})
        return [leanxcale_url], params

    def do_rollback(self, dbapi_conection):
        dbapi_conection.rollback()

    def do_commit(self, dbapi_conection):
        dbapi_conection.commit()

    def has_sequence(self, connection, sequence_name, schema=None, **kw):
        return sequence_name in self.get_sequence_names(connection, schema)

    def get_sequence_names(self, connection, schema=None, **kw):
        schema = schema if schema is not None else self.default_schema_name
        params = []
        sql = "SELECT DISTINCT(tableName) from LXSYS.TABLES where tableSchem <> 'LXSYS'"
        sql += " AND tableType = 'SEQUENCE'"
        if schema:
            sql += " AND tableSchem = '?'"
            params.append(str(schema))
        dbapi_con = connection.connection
        cursor = dbapi_con.cursor()
        cursor.execute(sql, params)
        result = []
        row = cursor.fetchone()
        while row is not None:
            result.append(row[0])
            row = cursor.fetchone()
        return result

    def has_table(self, connection, table_name, schema=None, **kw):
        return table_name in self.get_table_names(connection, schema)

    def _get_default_schema_name(self, connection):
        sql = "select schema from LXSYS.CONNECTIONS where iscurrent"
        dbapi_con = connection.connection
        cursor = dbapi_con.cursor()
        cursor.execute(sql)
        row = cursor.fetchone()
        if row:
            return row[0]
        return None

    def get_schema_names(self, connection, **kw):
        sql = "select distinct(tableSchem) from LXSYS.TABLES where tableSchem <> 'LXSYS'"
        dbapi_con = connection.connection
        cursor = dbapi_con.cursor()
        cursor.execute(sql)
        result = []
        schema = cursor.fetchone()
        while schema is not None:
            result.append(str(schema[0]))
            schema = cursor.fetchone()
        return result

    def get_table_names(self, connection, schema=None, **kw):
        schema = schema if schema is not None else self.default_schema_name
        params = []
        sql = "SELECT DISTINCT(tableName) from LXSYS.TABLES where tableSchem <> 'LXSYS'"
        sql += " AND tableType IN ('TABLE', 'MATERIALIZED QUERY TABLE')"
        if schema:
            sql += " AND tableSchem = ?"
            params.append(str(schema))
        if 'tableNamePattern' in kw.keys():
            tableNamePattern = kw.get('tableNamePattern')
            sql += " AND tableName LIKE ?"
            params.append(str(tableNamePattern))
        dbapi_con = connection.connection
        cursor = dbapi_con.cursor()
        cursor.execute(sql, params)
        result = []
        row = cursor.fetchone()
        while row is not None:
            result.append(str(row[0]))
            row = cursor.fetchone()
        return result

    def get_columns(self, connection, table_name=None, schema=None, catalog=None, column_name=None, **kw):
        params = []
        sql = "select columnName, dataType, typeName, nullable, columnDef from LXSYS.COLUMNS"
        schema = schema if schema is not None else self.default_schema_name
        has_where = False
        if catalog:
            sql += " WHERE tableCat = ?"
            has_where = True
            params.append(str(catalog))
        if schema:
            if has_where:
                sql += " AND "
            else:
                sql += " WHERE "
                has_where = True
            sql += "tableSchem = ?"
            params.append(str(schema))
        if table_name:
            if has_where:
                sql += " AND "
            else:
                sql += " WHERE "
                has_where = True
            sql += "tableName = ?"
            params.append(str(table_name))
        if column_name:
            if has_where:
                sql += " AND "
            else:
                sql += " WHERE "
            sql += "columnName = ?"
            params.append(str(column_name))
        dbapi_con = connection.connection
        cursor = dbapi_con.cursor()
        cursor.execute(sql, params)
        result = []
        row = cursor.fetchone()
        while row is not None:
            col_d = {}
            col_d.update({'name': row[0]})
            if row[1] == 2003:
                if row[2].split()[0] == 'BIGINT':
                    col_d.update({'item_type': BigInteger})
                elif row[2].split()[0] == 'DOUBLE':
                    col_d.update({'item_type': Float})
                elif row[2].split()[0] == 'VARCHAR':
                    col_d.update({'item_type': VARCHAR})
                col_d.update({'type': ARRAY(row[5])})
            elif row[1] == 2104:
                col_d.update({'item_type': BigInteger})
                col_d.update({'type': ARRAY(row[5])})
            elif row[1] == 2108:
                col_d.update({'item_type': Float})
                col_d.update({'type': ARRAY(row[5])})
            elif row[1] == 2112:
                col_d.update({'item_type': VARCHAR})
                col_d.update({'type': ARRAY(row[5])})
            else:
                col_d.update({'type': COLUMN_DATA_TYPE[row[1]]})
            col_d.update({'nullable': row[3] == 1 if True else False})
            col_d.update({'default': row[4]})
            result.append(col_d)
            row = cursor.fetchone()

        return result

    def get_view_names(self, connection, schema=None, **kw):
        params = []
        schema = schema if schema is not None else self.default_schema_name
        sql = "SELECT DISTINCT(tableName) from LXSYS.TABLES where tableSchem <> 'LXSYS'"
        sql += " AND tableType = 'VIEW'"
        if schema:
            sql += " AND tableSchem = ?"
            params.append(str(schema))
        dbapi_con = connection.connection
        cursor = dbapi_con.cursor()
        cursor.execute(sql, params)
        result = []
        row = cursor.fetchone()
        while row is not None:
            result.append(row[0])
            row = cursor.fetchone()
        return result

    def get_pk_constraint(self, connection, table_name, schema=None, **kw):
        params = []
        sql = "SELECT columnName FROM LXSYS.PRIMARY_KEYS WHERE TABLENAME = ? ORDER BY keyseq"
        params.append(str(table_name))
        dbapi_con = connection.connection
        cursor = dbapi_con.cursor()
        cursor.execute(sql, params)
        cols = []
        row = cursor.fetchone()
        while row is not None:
            cols.append(row[0])
            row = cursor.fetchone()

        result = {
            'constrained_columns': cols,
        }
        return result

#   TABLE_CAT   TABLE_SCHEM   TABLE_NAME   COLUMN_NAME   DATA_TYPE   TYPE_NAME   COLUMN_SIZE   BUFFER_LENGTH   DECIMAL_DIGITS   NUM_PREC_RADIX   NULLABLE   REMARKS   COLUMN_DEF   SQL_DATA_TYPE   SQL_DATETIME_SUB   CHAR_OCTET_LENGTH   ORDINAL_POSITION   IS_NULLABLE   SCOPE_CATALOG   SCOPE_SCHEMA   SCOPE_TABLE   SOURCE_DATA_TYPE   IS_AUTOINCREMENT   IS_GENERATEDCOLUMN  

    def get_foreign_keys(self, connection, table_name, schema=None, **kw):
        params = []
        sql = "SELECT fktableSchem, fktableName, fkName, pktableSchem, pktableName, pkcolumnName, fkcolumnName, keySeq"\
              " from LXSYS.FOREIGN_KEYS" \
              " WHERE fktableName = ?"
        params.append(str(table_name))
        if schema:
            sql += " and fktableSchem = ?"
            params.append(str(schema))
        sql += " order by fktableSchem, fktableName, fkName, keySeq"
        dbapi_con = connection.connection
        cursor = dbapi_con.cursor()
        cursor.execute(sql, params)
        result = []
        fksch = None
        fktbl = None
        fkname = None
        pksch = None
        pktbl = None
        fkcols = None
        pkcols = None
        row = cursor.fetchone()
        while row is not None:
            if fkname != row[2] or fktbl != row[1] or fksch != row[0]:
                if fkname:
                    fk_info = {
                        "constrained_columns": fkcols,
                        "referred_schema": pksch,
                        "referred_table": pktbl,
                        "referred_columns": pkcols,
                        "name": fkname,
                    }
                    result.append(fk_info)
                fksch = row[0]
                fktbl = row[1]
                fkname = row[2]
                pksch = row[3]
                pktbl = row[4]
                fkcols = []
                pkcols = []
            pkcols.append(row[5])
            fkcols.append(row[6])
            row = cursor.fetchone()

        if fkname:
            fk_info = {
                "constrained_columns": fkcols,
                "referred_schema": pksch,
                "referred_table": pktbl,
                "referred_columns": pkcols,
                "name": fkname,
            }
            result.append(fk_info)
        return result

    def get_indexes(self, connection, table_name, schema=None, **kw):
        params = []
        sql = "SELECT indexName, columnName, cast(nonUnique as INTEGER) FROM LXSYS.INDEX_COLUMNS WHERE TABLENAME = ?"
        params.append(str(table_name))
        if schema:
            sql += " and tableSchem = ?"
            params.append(str(schema))
        sql += " order by indexname, ordinalposition"
        dbapi_con = connection.connection
        cursor = dbapi_con.cursor()
        cursor.execute(sql, params)
        result = []
        name = None
        cols = None
        nonUnique = None
        row = cursor.fetchone()
        while row is not None:
            if name != row[0]:
                if name is not None:
                    item = {
                        'name': name,
                        'column_names': cols,
                        'unique': not nonUnique
                    }
                    result.append(item)
                name = row[0]
                cols = []
                if row[2] is None or int(row[2]) == 0:
                    nonUnique = False
                else:
                    nonUnique = True
            cols.append(row[1])
            row = cursor.fetchone()

        if name is not None:
            item = {
                'name': name,
                'column_names': cols,
                'unique': not nonUnique
            }
            result.append(item)
        return result

class TINYINT(types.Integer):
    __visit_name__ = "INTEGER"


class UTINYINT(types.Integer):
    __visit_name__ = "INTEGER"


class UINTEGER(types.Integer):
    __visit_name__ = "INTEGER"


class DOUBLE(types.BIGINT):
    __visit_name__ = "BIGINT"


class DOUBLE(types.BIGINT):
    __visit_name__ = "BIGINT"


class UDOUBLE(types.BIGINT):
    __visit_name__ = "BIGINT"


class UFLOAT(types.FLOAT):
    __visit_name__ = "FLOAT"


class ULONG(types.BIGINT):
    __visit_name__ = "BIGINT"


class UTIME(types.TIME):
    __visit_name__ = "TIME"


class UDATE(types.DATE):
    __visit_name__ = "DATE"


class UTIMESTAMP(types.TIMESTAMP):
    __visit_name__ = "TIMESTAMP"


class ROWID(types.String):
    __visit_name__ = "VARCHAR"

class ARRAY(types.ARRAY):
    __visit_name__ = "ARRAY"
    def __init__(self, type):
        types.ARRAY.__init__(self, type)



COLUMN_DATA_TYPE = {
    -6: TINYINT,
    -5: BIGINT,
    -3: VARBINARY,
    1: CHAR,
    3: DECIMAL,
    4: INTEGER,
    5: SMALLINT,
    6: FLOAT,
    8: DOUBLE,
    9: UINTEGER,
    10: ULONG,
    11: UTINYINT,
    12: VARCHAR,
    13: ROWID,
    14: UFLOAT,
    15: UDOUBLE,
    16: BOOLEAN,
    18: UTIME,
    19: UDATE,
    20: UTIMESTAMP,
    91: DATE,
    92: TIME,
    93: TIMESTAMP
}
