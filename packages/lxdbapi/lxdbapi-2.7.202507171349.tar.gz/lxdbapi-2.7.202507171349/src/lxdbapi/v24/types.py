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

import time
import base64
import datetime
from codecs import IncrementalEncoder, CodecInfo, BufferedIncrementalEncoder
from decimal import Decimal
from io import RawIOBase, TextIOBase, UnsupportedOperation, IOBase

from lxdbapi.common_pb2 import Rep, TypedValue
from lxdbapi.errors import ArrayTypeException
from lxdbapi import common_pb2

__all__ = [
	'Date', 'Time', 'Timestamp', 'DateFromTicks', 'TimeFromTicks', 'TimestampFromTicks',
	'Binary', 'STRING', 'BINARY', 'NUMBER', 'DATETIME', 'ROWID', 'BOOLEAN', 'javaTypetoNative',
	'nativeToParamType', 'LXARRAY', 'typed_value_2_native', 'native_2_typed_value', 'LxRawReader', 'LxTextReader'
]


def Date(year, month, day):
	"""Constructs an object holding a date value."""
	return datetime.date(year, month, day)


def Time(hour, minute, second):
	"""Constructs an object holding a time value."""
	return datetime.time(hour, minute, second)


def Timestamp(year, month, day, hour, minute, second):
	"""Constructs an object holding a datetime/timestamp value."""
	return datetime.datetime(year, month, day, hour, minute, second)


def DateFromTicks(ticks):
	"""Constructs an object holding a date value from the given UNIX timestamp."""
	return Date(*time.localtime(ticks)[:3])


def TimeFromTicks(ticks):
	"""Constructs an object holding a time value from the given UNIX timestamp."""
	return Time(*time.localtime(ticks)[3:6])


def TimestampFromTicks(ticks):
	"""Constructs an object holding a datetime/timestamp value from the given UNIX timestamp."""
	return Timestamp(*time.localtime(ticks)[:6])


def Binary(value):
	"""Constructs an object capable of holding a binary (long) string value."""
	if isinstance(value, _BinaryString):
		return value
	return _BinaryString(base64.b64encode(value))


def time_from_java_sql_time(n):
	dt = datetime.datetime(1970, 1, 1) + datetime.timedelta(milliseconds=n)
	return dt.time()


def time_to_java_sql_time(t):
	return int(((t.hour * 60 + t.minute) * 60 + t.second) * 1000 + t.microsecond / 1000)


def date_from_java_sql_date(n):
	return datetime.date(1970, 1, 1) + datetime.timedelta(days=n)


def date_to_java_sql_date(d):
	if isinstance(d, datetime.datetime):
		d = d.date()
	td = d - datetime.date(1970, 1, 1)
	return td.days


def datetime_from_java_sql_timestamp(n):
	return datetime.datetime(1970, 1, 1, tzinfo=datetime.timezone.utc) + datetime.timedelta(milliseconds=n)


def datetime_to_java_sql_timestamp(d):
	td = d - datetime.datetime(1970, 1, 1).replace(tzinfo=datetime.timezone.utc)
	return int(td.microseconds / 1000 + (td.seconds + td.days * 24 * 3600) * 1000)


class _BinaryString(str):
	pass


class ColumnType(object):

	def __init__(self, eq_types):
		self.eq_types = tuple(eq_types)
		self.eq_types_set = set(eq_types)

	def __cmp__(self, other):
		if other in self.eq_types_set:
			return 0
		if other < self.eq_types:
			return 1
		else:
			return -1


STRING = ColumnType(['VARCHAR', 'CHAR'])
"""Type object that can be used to describe string-based columns."""

BINARY = ColumnType(['BINARY', 'VARBINARY'])
"""Type object that can be used to describe (long) binary columns."""

NUMBER = ColumnType(['INTEGER', 'UNSIGNED_INT', 'BIGINT', 'UNSIGNED_LONG', 'TINYINT', 'UNSIGNED_TINYINT', 'SMALLINT',
					 'UNSIGNED_SMALLINT', 'FLOAT', 'UNSIGNED_FLOAT', 'DOUBLE', 'UNSIGNED_DOUBLE', 'DECIMAL'])
"""Type object that can be used to describe numeric columns."""

DATETIME = ColumnType(['TIME', 'DATE', 'TIMESTAMP', 'UNSIGNED_TIME', 'UNSIGNED_DATE', 'UNSIGNED_TIMESTAMP'])
"""Type object that can be used to describe date/time columns."""

ROWID = ColumnType([])
"""Only implemented for DB API 2.0 compatibility, not used."""

BOOLEAN = ColumnType(['BOOLEAN'])
"""Type object that can be used to describe boolean columns. This is a lxdbapi-specific extension."""


# XXX ARRAY
class LXARRAY():
	__value = []
	__type = None

	def __init__(self, value, type):
		self.__value = value
		self.__type = type

	def __str__(self):
		return f'({self.__type}){self.__value}'

	def getvalue(self):
		return self.__value

	def setvalue(self, value):
		self.__value = value

	def gettype(self):
		return self.__type

	def settype(self, type):
		self.__type = type


BUF_SZ = 65536


class LxRawReader(RawIOBase):
	"""
	API to read bytes from any object.
	Need to provide the read and close functions that performs the action over the byte source object.

	The constructor has the following arguments:
		- obj: the object where to read the bytes from
		- readf: function that will read bytes from obj into a pre-allocated, writable bytes-like object. Its signature
		 should be:
			+ <fname>(buf:WritableBuffer, offset, obj, len) where :
				- buf is a WritableBuffer object (probably a memoryview) where to write the bytes read from obj
				- obj is the object to read bytes from
				- It return the number of bytes read. None when eof is reached or no more bytes are available.
		- closef: function that will close obj when needed. Could be None when not needed. Its signature should be:
			+ <fname>(obj) where obj is the object to read bytes from

	Note that this API won't allow reading all the bytes at once.
	"""

	def __init__(self, obj, readf=None, closef=None):
		self.obj = obj
		if readf is None:
			self.readf = lambda buf, o: o.readinto(buf)
		else:
			self.readf = readf
		if closef is None:
			self.closef = lambda o: o.close()
		else:
			self.closef = closef
		self._closed = False
		self.offset = 0

	def __enter__(self):
		return self

	def __del__(self):
		self.close()

	def __exit__(self, exc_type, exc_val, exc_tb):
		self.close()

	def close(self) -> None:
		if not self._closed:
			self._closed = True
			if self.closef is not None:
				self.closef(self.obj)

	@property
	def closed(self):
		return self._closed

	def read(self, __size=...):
		if self._closed:
			return None
		if __size is None:
			raise RuntimeError("Read all not allowed. Use size argument")
		if __size < 0:
			raise RuntimeError("Read all not allowed. Use size argument")
		if __size == 0:
			return bytes(0)
		if __size > BUF_SZ:
			raise RuntimeError(f"Can read at most {BUF_SZ} bytes")
		offset = 0
		buf = bytearray(__size)
		mv = memoryview(buf)
		while offset < __size:
			n = self.readf(mv[offset:], self.obj)
			if n is None or n <= 0:
				self.close()
				break
			offset += n
		self.offset += offset
		if offset == 0:
			return None
		if offset == __size:
			return bytes(buf)
		return bytes(buf[:offset])

	def readall(self):
		raise RuntimeError("Read all not allowed")

	def readinto(self, buf):
		if self._closed:
			return None
		if buf is None:
			return 0
		n = self.readf(buf, self.obj)
		self.offset += n
		return n

	def fileno(self):
		raise OSError("No fileno")

	def readlines(self, __hint=...):
		raise OSError("Not allowed. Use readinto")

	def readline(self, __size=...) -> bytes:
		raise OSError("Not allowed. Use readinto")

	def isatty(self) -> bool:
		return False

	def flush(self) -> None:
		return None

	def readable(self) -> bool:
		return True

	def seekable(self) -> bool:
		return False

	def seek(self, __offset: int, __whence=...):
		raise OSError("Not seekable")

	def tell(self) -> int:
		raise OSError("Not seekable")

	def truncate(self, __size=...):
		raise OSError("Not seekable")

	def writable(self) -> bool:
		return False

	def write(self, __b):
		raise OSError("Not writeable")

	def writelines(self, __lines):
		raise OSError("Not writeable")


class LxText2Bin(object):
	def __init__(self, io: TextIOBase, codeci: CodecInfo):
		self.io = io
		self.iencoder = codeci.incrementalencoder()
		self.pending = None
		self.current = ""
		self.done = False
		self._next()
		self.first = self.current

	def _next(self):
		self.current = ""
		offset = 0
		while offset < BUF_SZ:
			s = self.io.read(BUF_SZ - offset)
			if s is None:
				self.done = True
				break
			l = len(s)
			if l <= 0:
				self.done = True
				break
			self.current += s
			offset += l

	def close(self):
		self.io.close()
		self.io = None

	def _pendingreadinto(self, buf, offset, l):
		n = 0
		if self.pending is not None:
			sz = len(self.pending)
			if sz > l:
				last = offset + l
				buf[offset:last] = self.pending[0:l]
				self.pending = self.pending[l:]
				n += l
				return n
			last = offset + sz
			buf[offset:last] = self.pending[0:]
			self.pending = None
			n += sz
		return n

	def readinto(self, buf):
		if buf is None:
			return 0
		sz = len(buf)
		if sz == 0:
			return 0
		n = self._pendingreadinto(buf, 0, sz)

		while n < sz:
			slen = len(self.current)
			if slen <= 0:
				if self.done:
					break
				self._next()
			b = self.iencoder.encode(self.current, self.done)
			self._next()
			self.pending = b
			l = sz - n
			nn = self._pendingreadinto(buf, n, l)
			n += nn
			if nn >= l:
				break
		return n


class LxTextReader(TextIOBase):

	def __init__(self, binr: RawIOBase, codeci: CodecInfo):
		self.idecoder = codeci.incrementaldecoder()
		self.binr = binr
		self._closed = False
		self.buf = bytearray(BUF_SZ)
		self.bmv = memoryview(self.buf)
		self.bsz = self._load_buf(self.bmv)
		self.str = self._next()
		self.slen = len(self.str)
		self.soffset = 0

	def _load_buf(self, buf: memoryview):
		n = self.binr.readinto(buf)
		if n is None or n <= 0:
			n = 0
			self.close()
		return n

	def _next(self):
		if self.bsz <= 0:
			return ""
		b = self.buf[:self.bsz]
		self.bsz = self._load_buf(self.bmv)
		final = self.bsz <= 0
		return self.idecoder.decode(b, final)

	def __enter__(self):
		return self

	def __del__(self):
		self.close()

	def __exit__(self, exc_type, exc_val, exc_tb):
		self.close()

	def close(self):
		if not self._closed:
			self._closed = True
			self.binr.close()

	@property
	def closed(self):
		return self._closed

	@property
	def encoding(self):
		return self._encoding

	def read(self, __size=...):
		if self._closed:
			return ""
		if __size is None:
			raise RuntimeError("Read all not allowed. Use size argument")
		if __size < 0:
			raise RuntimeError("Read all not allowed. Use size argument")
		if __size == 0:
			return ""
		if __size > self.bsz:
			raise RuntimeError(f"Can read at most {BUF_SZ} bytes")
		if self.soffset >= self.slen:
			self.str = self._next()
			if self.str == "":
				return ""
		res = ""
		sz = __size
		while sz > 0:
			len = self.slen - self.soffset
			if len > sz:
				last = self.soffset + sz
				res += self.str[self.soffset:last]
				self.soffset = last
				break
			else:
				res += self.str[self.soffset:]
				sz -= len
				self.str = self._next()
				if self.str == "":
					break
				self.slen = len(self.str)
				self.soffset = 0

		return res

	def detach(self):
		raise UnsupportedOperation("detach")

	def readline(self, __size=...):
		raise RuntimeError("Use read(sz)")

	def seek(self, __offset, __whence=...):
		raise OSError("Not seekable")

	def tell(self):
		raise OSError("Not seekable")

	def fileno(self):
		raise OSError("No fileno")

	def readlines(self, __hint=...):
		raise OSError("Use read(sz)")

	def readline(self, __size=...):
		raise OSError("Use read(sz)")

	def isatty(self):
		return False

	def flush(self) -> None:
		return None

	def readable(self):
		return True

	def seekable(self):
		return False

	def seek(self, __offset, __whence=...):
		raise OSError("Not seekable")

	def tell(self):
		raise OSError("Not seekable")

	def truncate(self, __size=...):
		raise OSError("Not seekable")

	def writable(self):
		return False

	def write(self, __b):
		raise OSError("Not writeable")

	def writelines(self, __lines):
		raise OSError("Not writeable")


class LxBlobReader(object):
	def __init__(self, cursor, bmsg):
		self.cursor = cursor
		self.first = bmsg
		self.last = None
		self.offset = 0
		self.len = 0
		self.current = None
		self._set_current(self.first)
		self.cursor.add_blob_reader(self)

	def _set_current(self, bmsg):
		self.last = bmsg
		self.offset = 0
		if self.last is None:
			self.len = 0
			self.current = None
		else:
			self.len = len(self.last.bytes_value)
			self.current = memoryview(self.last.bytes_value)

	def _next(self):
		if self.last.info.done:
			return False
		offset = self.last.info.offset + len(self.last.bytes_value)
		bmsg = self.cursor.read_blob(self.first.info.id, offset)
		if bmsg is None:
			return False
		self._set_current(bmsg)
		return True

	def readinto(self, buf):
		if buf is None:
			return 0
		blen = len(buf)
		if self.offset >= self.len:
			if not self._next():
				return 0
		n = 0
		while n < blen:
			bl = blen - n
			ll = self.len - self.offset
			if bl == ll:
				buf[n:] = self.current[self.offset:]
				n += bl
				self.offset += n
				break
			if bl < ll:
				inx = self.offset + bl
				buf[n:] = self.current[self.offset:inx]
				n += bl
				self.offset += n
				break
			inx = n + ll
			buf[n:inx] = self.current[self.offset:]
			n += ll
			self.offset += n
			if self.offset >= self.len:
				if not self._next():
					break
		return n

	def reset(self):
		self._set_current(self.first)

	def close(self, reset=True):
		if reset:
			self.reset()
		else:
			self.cursor = None
			self.first = None
			self.last = None
			self.offset = 0
			self.len = 0
			self.current = None


def typedValueToNative(v):
	if Rep.Name(v.type) == "BOOLEAN" or Rep.Name(v.type) == "PRIMITIVE_BOOLEAN":
		return v.bool_value

	elif Rep.Name(v.type) == "STRING" or Rep.Name(v.type) == "PRIMITIVE_CHAR" or Rep.Name(
			v.type) == "CHARACTER" or Rep.Name(v.type) == "BIG_DECIMAL":
		return v.string_value

	elif Rep.Name(v.type) == "FLOAT" or Rep.Name(v.type) == "PRIMITIVE_FLOAT" or Rep.Name(
			v.type) == "DOUBLE" or Rep.Name(v.type) == "PRIMITIVE_DOUBLE":
		return v.double_value

	elif Rep.Name(v.type) == "LONG" or Rep.Name(v.type) == "PRIMITIVE_LONG" or Rep.Name(
			v.type) == "INTEGER" or Rep.Name(v.type) == "PRIMITIVE_INT" or \
			Rep.Name(v.type) == "BIG_INTEGER" or Rep.Name(v.type) == "NUMBER" or Rep.Name(v.type) == "BYTE" or Rep.Name(
		v.type) == "PRIMITIVE_BYTE" or \
			Rep.Name(v.type) == "SHORT" or Rep.Name(v.type) == "PRIMITIVE_SHORT":
		return v.number_value

	elif Rep.Name(v.type) == "BYTE_STRING":
		return v.bytes_value

	else:
		return None


def javaTypetoNative(java_type, sql_type):
	if java_type == 'java.math.BigDecimal':
		return 'BIG_DECIMAL', None, "string_value", sql_type
	elif java_type == 'java.lang.Float':
		return 'FLOAT', float, "double_value", sql_type
	elif java_type == 'java.lang.Double':
		return 'DOUBLE', None, "double_value", sql_type
	elif java_type == 'java.lang.Long':
		return 'LONG', None, "number_value", sql_type
	elif java_type == 'java.lang.Integer':
		return 'INTEGER', int, "number_value", sql_type
	elif java_type == 'java.lang.Short':
		return 'SHORT', int, "number_value", sql_type
	elif java_type == 'java.lang.Byte':
		return 'BYTE', Binary, "bytes_value", sql_type
	elif java_type == 'java.lang.Boolean':
		return 'BOOLEAN', bool, "bool_value", sql_type
	elif java_type == 'java.lang.String':
		return 'STRING', None, "string_value", sql_type
	elif java_type == 'java.sql.Time':
		return 'JAVA_SQL_TIME', time_from_java_sql_time, "number_value", sql_type
	elif java_type == 'java.sql.Date':
		return 'JAVA_SQL_DATE', date_from_java_sql_date, "number_value", sql_type
	elif java_type == 'java.sql.Timestamp':
		return 'JAVA_SQL_TIMESTAMP', datetime_from_java_sql_timestamp, "number_value", sql_type
	elif java_type == '[B':
		return 'BYTE_STRING', bytes, "bytes_value", sql_type
	else:
		return 'NULL', None, None, sql_type


def nativeToParamType(value, isArray=False):
	if value is None:
		return 'NULL', None, "null"
	elif isinstance(value, int):
		if (abs(value) <= 0x7FFFFFFF and not isArray):
			return 'INTEGER', int, "number_value"
		else:
			return 'LONG', int, "number_value"
	elif isinstance(value, float):
		return 'DOUBLE', float, "double_value"
	elif isinstance(value, bool):
		return 'BOOLEAN', bool, "bool_value"
	elif isinstance(value, str):
		return 'STRING', str, "string_value"
	elif isinstance(value, datetime.time):
		return 'JAVA_SQL_TIME', time_to_java_sql_time, "number_value"
	elif isinstance(value,
					datetime.datetime):  # TODO check: important to put this case before datetime.date as datetimes also match in date clause
		return 'JAVA_SQL_TIMESTAMP', datetime_to_java_sql_timestamp, "number_value"
	elif isinstance(value, datetime.date):
		return 'JAVA_SQL_DATE', date_to_java_sql_date, "number_value"
	elif isinstance(value, bytes):
		return 'BYTE_STRING', bytes, "bytes_value"
	elif isinstance(value, LXARRAY):
		return 'ARRAY', None, "array_value"
	else:
		return 'STRING', str, "string_value"


def lxarray2tv(value: LXARRAY):
	result = common_pb2.TypedValue()  # parent typed value
	result.type = common_pb2.Rep.Value('ARRAY')
	if value.gettype() is int:
		result.component_type = common_pb2.Rep.Value("LONG")
	elif value.gettype() is float:
		result.component_type = common_pb2.Rep.Value("DOUBLE")
	elif value.gettype() is str:
		result.component_type = common_pb2.Rep.Value("STRING")
	else:
		raise ArrayTypeException("Array cannot be of type: {}".format(value.gettype()))

	for item in value.getvalue():
		type_param = nativeToParamType(item, isArray=True)  # int bigint varchar ???
		v_temp = common_pb2.TypedValue()
		v_temp.type = common_pb2.Rep.Value(type_param[0])
		if item != None:
			setattr(v_temp, type_param[2], type_param[1](item))
		else:
			setattr(v_temp, type_param[2], 1)  # 1 for True
		result.array_value.append(v_temp)
	return result


def typed_value_2_native(typed_value: common_pb2.TypedValue, ctx):
	func = _rep_to_native_funcs[_rep_index_to_name[typed_value.type]]
	if func is None:
		_unsupported_typed_value(typed_value, ctx)
		return None
	return func(typed_value, ctx)


def _bool_value_2_native(typed_value: common_pb2.TypedValue, ctx):
	return bool(typed_value.bool_value)


def _string_value_2_native(typed_value: common_pb2.TypedValue, ctx):
	return str(typed_value.string_value)


def _big_decimal_value_2_native(typed_value: common_pb2.TypedValue, ctx):
	value = str(typed_value.string_value)
	if '.' not in value and ',' not in value:
		return int(value)
	return Decimal(value)


def _bytes_value_2_native(typed_value: common_pb2.TypedValue, ctx):
	return bytes(typed_value.bytes_value)


def _number_value_2_native(typed_value: common_pb2.TypedValue, ctx):
	return int(typed_value.number_value)


def _double_value_2_native(typed_value: common_pb2.TypedValue, ctx):
	return float(typed_value.double_value)


def _null_value_2_native(typed_value: common_pb2.TypedValue, ctx):
	return None


def _blob_value_2_native(typed_value: common_pb2.TypedValue, ctx):
	if typed_value.blob_info.done:
		return bytes(typed_value.bytes_value)
	bmsg = common_pb2.LxBlobMsg()
	bmsg.info.id = typed_value.blob_info.id
	bmsg.info.done = False
	bmsg.info.offset = 0
	bmsg.bytes_value = typed_value.bytes_value
	br = LxBlobReader(ctx, bmsg)
	return LxRawReader(br)


def _unsupported_typed_value(typed_value: common_pb2.TypedValue, ctx):
	raise NotImplementedError("Not supported: " + _rep_index_to_name[typed_value.type])


_rep_index_to_name = ['PRIMITIVE_BOOLEAN',
					  'PRIMITIVE_BYTE',
					  'PRIMITIVE_CHAR',
					  'PRIMITIVE_SHORT',
					  'PRIMITIVE_INT',
					  'PRIMITIVE_LONG',
					  'PRIMITIVE_FLOAT',
					  'PRIMITIVE_DOUBLE',
					  'BOOLEAN',
					  'BYTE',
					  'CHARACTER',
					  'SHORT',
					  'INTEGER',
					  'LONG',
					  'FLOAT',
					  'DOUBLE',
					  'JAVA_SQL_TIME',
					  'JAVA_SQL_TIMESTAMP',
					  'JAVA_SQL_DATE',
					  'JAVA_UTIL_DATE',
					  'BYTE_STRING',
					  'STRING',
					  'NUMBER',
					  'OBJECT',
					  'NULL',
					  'BIG_INTEGER',
					  'BIG_DECIMAL',
					  'ARRAY',
					  'STRUCT',
					  'MULTISET',
					  'ZONED_DATE_TIME',
					  'LXBLOB']

_rep_to_native_funcs = {'ARRAY': _unsupported_typed_value,
						'BIG_DECIMAL': _big_decimal_value_2_native,
						'BIG_INTEGER': _bytes_value_2_native,
						'BOOLEAN': _bool_value_2_native,
						'BYTE': _number_value_2_native,
						'BYTE_STRING': _bytes_value_2_native,
						'CHARACTER': _string_value_2_native,
						'DOUBLE': _double_value_2_native,
						'FLOAT': _double_value_2_native,
						'INTEGER': _number_value_2_native,
						'JAVA_SQL_DATE': _number_value_2_native,
						'JAVA_SQL_TIME': _number_value_2_native,
						'JAVA_SQL_TIMESTAMP': _number_value_2_native,
						'JAVA_UTIL_DATE': _number_value_2_native,
						'LONG': _number_value_2_native,
						'MULTISET': _unsupported_typed_value,
						'NULL': _null_value_2_native,
						'NUMBER': _number_value_2_native,
						'OBJECT': _unsupported_typed_value,
						'PRIMITIVE_BOOLEAN': _bool_value_2_native,
						'PRIMITIVE_BYTE': _number_value_2_native,
						'PRIMITIVE_CHAR': _string_value_2_native,
						'PRIMITIVE_DOUBLE': _number_value_2_native,
						'PRIMITIVE_FLOAT': _double_value_2_native,
						'PRIMITIVE_INT': _number_value_2_native,
						'PRIMITIVE_LONG': _number_value_2_native,
						'PRIMITIVE_SHORT': _number_value_2_native,
						'SHORT': _number_value_2_native,
						'STRING': _string_value_2_native,
						'STRUCT': _unsupported_typed_value,
						'LXBLOB': _blob_value_2_native}


def lxarray2tv(value: LXARRAY):
	result = common_pb2.TypedValue()  # parent typed value
	result.type = common_pb2.Rep.Value('ARRAY')
	if value.gettype() is int:
		result.component_type = common_pb2.Rep.Value("LONG")
	elif value.gettype() is float:
		result.component_type = common_pb2.Rep.Value("DOUBLE")
	elif value.gettype() is str:
		result.component_type = common_pb2.Rep.Value("STRING")
	else:
		raise ArrayTypeException("Array cannot be of type: {}".format(value.gettype()))

	for item in value.getvalue():
		type_param = nativeToParamType(item, isArray=True)  # int bigint varchar ???
		v_temp = common_pb2.TypedValue()
		v_temp.type = common_pb2.Rep.Value(type_param[0])
		if item != None:
			setattr(v_temp, type_param[2], type_param[1](item))
		else:
			setattr(v_temp, type_param[2], 1)  # 1 for True
		result.array_value.append(v_temp)
	return result


def blob2tv(value: IOBase, ctx):
	txt2bin = None
	if isinstance(value, TextIOBase):
		txt2bin = LxText2Bin(value, ctx._connection.codeci)
		lxblob = LxRawReader(txt2bin)
	elif isinstance(value, LxRawReader):
		lxblob = value
	else:
		lxblob = LxRawReader(value)

	result = common_pb2.TypedValue()
	bs = lxblob.read(BUF_SZ)
	if lxblob.closed:
		if txt2bin is None:
			result.bytes_value = bs
			result.type = common_pb2.Rep.Value('BYTE_STRING')
			return result
		result.type = common_pb2.Rep.Value('STRING')
		result.string_value = txt2bin.first
		return result
	result.type = common_pb2.Rep.Value('LXBLOB')
	result.bytes_value = bs
	bid = ctx.add_blob(lxblob)
	result.blob_info.id = bid
	result.blob_info.offset = 0
	result.blob_info.done = False
	return result


def native_2_typed_value(value, ctx):
	if value is None:
		return common_pb2.TypedValue(null=True, type=common_pb2.Rep.Value('NULL'))
	if isinstance(value, LXARRAY):
		return lxarray2tv(value)
	if isinstance(value, IOBase):
		return blob2tv(value, ctx)

	type_param = nativeToParamType(value)
	styp = type_param[0]
	result = common_pb2.TypedValue()
	result.type = common_pb2.Rep.Value(styp)
	if type_param[1] is not None:
		if isinstance(value, datetime.datetime):
			if value.tzinfo is None:
				value = value.astimezone(None)
		setattr(result, type_param[2], type_param[1](value))
		return result
	setattr(result, type_param[2], value)
	return result
