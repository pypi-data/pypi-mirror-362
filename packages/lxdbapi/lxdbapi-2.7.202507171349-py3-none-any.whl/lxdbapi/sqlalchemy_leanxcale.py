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

import urllib.parse

from sqlalchemy.connectors.pyodbc import PyODBCConnector
from sqlalchemy.engine.default import DefaultDialect
from sqlalchemy.sql.compiler import DDLCompiler, SQLCompiler
from sqlalchemy.sql import compiler
from sqlalchemy.engine import default

from sqlalchemy import types, BigInteger, Float
from sqlalchemy.types import INTEGER, BIGINT, SMALLINT, VARCHAR, CHAR, \
    FLOAT, REAL, DATE, BOOLEAN, DECIMAL, TIMESTAMP, TIME, VARBINARY
# TO DO: LXARRAY?

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


class LeanxcaleDialect(PyODBCConnector, DefaultDialect):

    name = "leanxcale"

    pyodbc_driver_name = "LeanXcaleODBCDriver"

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
    def import_dbapi(cls):
        import lxpyodbc as pyodbc

        # pyodbc.pooling = (
        #     False  # required for Access databases with ODBC linked tables
        # )
        return pyodbc

    @classmethod
    def dbapi(cls):
        import lxpyodbc as pyodbc
        # pyodbc.pooling = (
        #     False  # required for Access databases with ODBC linked tables
        # )
        return pyodbc

    def on_connect(self):
        def do_on_connect(c):
            import lxpyodbc as pyodbc
            c.maxwrite = 1024 * 1024 * 1024
            c.setdecoding(pyodbc.SQL_CHAR, encoding='utf-8')
            c.setdecoding(pyodbc.SQL_WCHAR, encoding='utf-8')
            c.setencoding(encoding='utf-8')

        return do_on_connect

    def do_rollback(self, dbconn):
        dbconn.rollback()

    def do_commit(self, dbconn):
        dbconn.commit()

    def has_sequence(self, connection, sequence_name, schema=None, **kw):
        return sequence_name in self.get_sequence_names(connection, schema)

    def get_sequence_names(self, connection, schema=None, **kw):
        schema = schema if schema is not None else self.default_schema_name
        params = []
        sql = "SELECT DISTINCT(table_name) from LXSYS.TABLES where table_schem <> 'LXSYS'"
        sql += " AND table_type = 'SEQUENCE'"
        if schema:
            sql += " AND table_schem = '?'"
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
        sql = "select table_schem from LXSYS.CONNECTIONS where current"
        dbapi_con = connection.connection
        cursor = dbapi_con.cursor()
        cursor.execute(sql)
        row = cursor.fetchone()
        if row:
            return row[0]
        return None

    def get_schema_names(self, connection, **kw):
        sql = "select distinct(table_schem) from LXSYS.TABLES where table_schem <> 'LXSYS'"
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
        sql = "SELECT DISTINCT(table_name) from LXSYS.TABLES where table_schem <> 'LXSYS'"
        sql += " AND table_type IN ('TABLE', 'MATERIALIZED QUERY TABLE')"
        if schema:
            sql += " AND table_schem = ?"
            params.append(str(schema))
        if 'tableNamePattern' in kw.keys():
            tableNamePattern = kw.get('tableNamePattern')
            sql += " AND table_name LIKE ?"
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

# table_cat   table_schem   table_name   column_name   data_type   type_name   column_size   buffer_length   decimal_digits   num_prec_radix   nullable   remarks   column_def   sql_data_type   sql_datetime_sub   char_octet_length   ordinal_position   is_nullable   scope_cat   scope_schem   scope_table   source_data_type   is_autoincrement   is_generated_column  

    def get_columns(self, connection, table_name=None, schema=None, catalog=None, column_name=None, **kw):
        params = []
        sql = "select column_name, data_type, type_name, nullable, column_def from LXSYS.COLUMNS WHERE 1 = 1"
        schema = schema if schema is not None else self.default_schema_name
        if catalog:
            sql += " AND table_cat = ?"
            params.append(str(catalog))
        if schema:
            sql += "AND table_schem = ?"
            params.append(str(schema))
        if table_name:
            sql += "AND table_name = ?"
            params.append(str(table_name))
        if column_name:
            sql += "AND column_name = ?"
            params.append(str(column_name))
        dbapi_con = connection.connection
        cursor = dbapi_con.cursor()
        cursor.execute(sql, params)
        result = []
        row = cursor.fetchone()
        while row is not None:
            col_d = {}
            col_d.update({'name': row[0]})
            if row[1] == ARRAY_CODE:	## TODO
                if row[2].split()[0] == 'BIGINT':
                    col_d.update({'item_type': BigInteger})
                elif row[2].split()[0] == 'DOUBLE':
                    col_d.update({'item_type': Float})
                elif row[2].split()[0] == 'VARCHAR':
                    col_d.update({'item_type': VARCHAR})
                col_d.update({'type': ARRAY(row[5])})
            elif row[1] == ARYI_CODE:	## TODO
                col_d.update({'item_type': BigInteger})
                col_d.update({'type': ARRAY(row[5])})
            elif row[1] == ARYF_CODE:	## TODO
                col_d.update({'item_type': Float})
                col_d.update({'type': ARRAY(row[5])})
            elif row[1] == ARYS_CODE:	## TODO
                col_d.update({'item_type': VARCHAR})
                col_d.update({'type': ARRAY(row[5])})
            else:
                col_d.update({'type': COLUMN_DATA_TYPE[row[1]]})
            col_d.update({'nullable': row[3] == 1 if True else False})
            col_d.update({'default': row[4]})
            if row[0] != '_UUID_':
                result.append(col_d)
            row = cursor.fetchone()

        return result

    def get_view_names(self, connection, schema=None, **kw):
        params = []
        schema = schema if schema is not None else self.default_schema_name
        sql = "SELECT DISTINCT(table_name) from LXSYS.TABLES where table_schem <> 'LXSYS'"
        sql += " AND table_type = 'VIEW'"
        if schema:
            sql += " AND table_schem = ?"
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
        sql = "SELECT column_name FROM LXSYS.PRIMARY_KEYS WHERE table_name = ? ORDER BY key_seq"
        params.append(str(table_name))
        dbapi_con = connection.connection
        cursor = dbapi_con.cursor()
        cursor.execute(sql, params)
        cols = []
        row = cursor.fetchone()
        while row is not None:
            if row[0] != '_UUID_':
                cols.append(row[0])
            row = cursor.fetchone()

        result = {
            'constrained_columns': cols,
        }
        return result
 
# table_cat   table_schem   table_name   column_name   key_name   key_seq   ptable_cat   ptable_schem   ptable_name   pcolumn_name   enable   validate   on_delete  
#  TABLE_CAT   TABLE_SCHEM   TABLE_NAME   COLUMN_NAME   DATA_TYPE   TYPE_NAME   COLUMN_SIZE   BUFFER_LENGTH   DECIMAL_DIGITS   NUM_PREC_RADIX   NULLABLE   REMARKS   COLUMN_DEF   SQL_DATA_TYPE   SQL_DATETIME_SUB   CHAR_OCTET_LENGTH   ORDINAL_POSITION   IS_NULLABLE   SCOPE_CATALOG   SCOPE_SCHEMA   SCOPE_TABLE   SOURCE_DATA_TYPE   IS_AUTOINCREMENT   IS_GENERATEDCOLUMN  

    def get_foreign_keys(self, connection, table_name, schema=None, **kw):
        params = []
        sql = "SELECT table_schem, table_name, key_name, ptable_schem, ptable_name, pcolumn_name, column_name, key_seq"\
              " from LXSYS.FOREIGN_KEYS" \
              " WHERE table_name = ?"
        params.append(str(table_name))
        if schema:
            sql += " and table_schem = ?"
            params.append(str(schema))
        sql += " order by table_schem, table_name, key_name, key_seq"
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

#  non_unique   index_qualifier   index_name   type   ordinal_position   column_name   asc_or_desc   cardinality   pages   filter_condition   table_cat   table_schem   table_name  

    def get_indexes(self, connection, table_name, schema=None, **kw):
        params = []
        sql = "SELECT index_name, column_name, cast(non_unique as INTEGER) FROM LXSYS.INDEX_COLUMNS WHERE table_name = ?"
        params.append(str(table_name))
        if schema:
            sql += " AND table_schem = ?"
            params.append(str(schema))
        sql += " order by index_name, ordinal_position"
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

class BOOLEAN(types.Boolean):
    __visit_name__ = "BOOLEAN"

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

class ARRAY(types.ARRAY):	## TODO
    __visit_name__ = "ARRAY"
    def __init__(self, type):
        types.ARRAY.__init__(self, type)

class CIDR(types.String):
    __visit_name__ = "CIDR"

class REAL(types.REAL):
    __visit_name__ = "REAL"

# CIDR, TIMESTAMP_LTZ

# lx=specific codes
CIDR_CODE = 3000
TSLTZ_CODE = 3001
ARYI_CODE = 2104
ARYF_CODE = 2108
ARYS_CODE= 2112
TSTZ_CODE = 2014
ARRAY_CODE = 2003
 
# 16: BOOLEAN,
# -6: TINYINT,
# 5: SMALLINT,
# 4: INTEGER,
# -5: BIGINT,
# 3: DECIMAL,
# 6: FLOAT,
# 7: REAL,
# 8: DOUBLE,
# 91: DATE,
# 92: TIME,
# 2014: TIMESTAMP_TZ,
# 93: TIMESTAMP,
# 3001: TIMESTAMP_LTZ,
# #1111: INTERVAL,
# 1: CHAR,
# 12: VARCHAR,
# 2005: CLOB,
# -2: BINARY,
# -3: VARBINARY,
# 2004: BLOB,
# 2003: MULTISET,
# 2003: ARRAY,
# 1111: MAP,
# 2001: DISTINCT,
# 2002: STRUCTURED,
# 2002: ROW,
# 1111: OTHER,
# 2012: CURSOR,
# 1113: COLUMN_LIST,
# 2015: GEOMETRY,
# 3000: CIDR,

COLUMN_DATA_TYPE = {
    -6: TINYINT,
    -5: BIGINT,
    -3: VARBINARY,
    1: CHAR,
    3: DECIMAL,
    4: INTEGER,
    5: SMALLINT,
    6: FLOAT,
    7: REAL,
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
    93: TIMESTAMP,
#  ARYI_CODE
# ARYF_CODE
# ARYS_CODE
    TSTZ_CODE: TIMESTAMP,
    CIDR_CODE: CIDR,
    TSLTZ_CODE: TIMESTAMP,
    ## TODO array types
}
