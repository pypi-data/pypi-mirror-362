import struct
from struct import pack
from dataclasses import dataclass
from enum import Enum
from typing import Any, List, Union, Callable, Optional
from pysqream.utils import DataError, false_generator, get_array_size
from pysqream.globals import TYPE_MAPPER
from pysqream.casting import date_to_int, datetime_to_long, decimal_to_sq_numeric, pandas_timestamp_to_sq_datetime2, arr_lengths_to_pairs, sq_date_to_py_date, sq_datetime_to_py_datetime, sq_numeric_to_decimal, sq_datetime2_to_pandas_timestamp
from pysqream.column_packers.column_packer import ColumnPacker, PackingError, ColumnData


class ArrayDataType(Enum):
    FIXED = "FIXED"
    UNFIXED = "UNFIXED"


@dataclass
class ArrayMetadata:
    element_type: str
    nullable: bool
    scale: int
    data_size: int
    array_type: ArrayDataType


class ArrayPacker(ColumnPacker):
    """
    Handles packing and unpacking of array types for SQream database communication.
    Supports both fixed-size types (numbers, dates) and variable-size types (strings).
    """

    uses_standard_packing: bool = False

    def __init__(self, metadata):
        super().__init__(metadata)
        self.array_metadata: ArrayMetadata = self._initialize_array_metadata()

    def _initialize_array_metadata(self) -> ArrayMetadata:
        """Initialize metadata for array handling."""

        if not isinstance(self.metadata.col_type, list) or len(self.metadata.col_type) < 2 or self.metadata.col_type[0] != 'ftArray':
            raise PackingError("Invalid array type specification",
                               col_idx=self.metadata.col_idx,
                               col_type=self.metadata.col_type)

        element_type = self.metadata.col_type[1]
        typecode = TYPE_MAPPER.get_typecode(element_type)

        return ArrayMetadata(
            element_type=element_type,
            nullable=self.metadata.nullable,
            scale=self.metadata.scale,
            data_size=struct.calcsize(TYPE_MAPPER.get_pack_code(element_type)),
            array_type=ArrayDataType.UNFIXED if typecode == "STRING" else ArrayDataType.FIXED
        )

    def _pack_data(self, data: List[Any]) -> bytes:
        raise NotImplementedError("Standard packing not implemented for array packer")

    def _pack_custom(self, data: List[Union[List[Any], None]]) -> bytes:
        """
        Pack array of any data type to bytes for transmitting to SQREAM
        Acceptable format of bytes includes 3 parts connected together
        without any padding gaps between:
            part1: nulls if nullable just N elements without padding
            part2: lengths of data chunks in part3 for each N row
                just N integers without padding (mem N * 4)
            part3: data without padding (varies depend on type of array)
        Explanation on part3 for fixed SIZE data types:
            First come 1 byte that explains whether data at first index is
            a null or not, then come SIZE bytes with the value, then again
            1 byte and SIZE bytes etc. When row ends, then just new array
            started without padding by the same pattern.
            Example of ARRAY INT[] of 3 rows:
            array[1, null, 8], null, array[2, 5]
            Packed: `010  15000 0000 10000  0 1000 1 0000 0 8000  0 2000 0 5000`
                     ^    ^                 ^                     ^
                p1 nulls  p2 lengths        p3 data row1          row3
        Explanation on part3 for unfixed size data type (TEXT):
            After part1 & 2 (the same)
            Started with array size in first 4 bytes (INT value)
            Then for each N elements: 1 byte (is null), 4 byte - INT represents
            LENGTH of string at this index, then LENGTH bytes data of string
            itself. Then the same for each row
            Example of ARRAY TEXT[] of 3 rows:
            array['WORK', '', null, "IS DONE"], null, array['Ok', 'then']
            Full buffer:
                part1 and 2: `010  35 000 0000 20 000`
                              ^    ^
                         p1 nulls  p2 lengths
                row1: `4000  0 4000 WORK  0 0000  1 0000  0 7000 IS DONE`
                       ^     ^            ^       ^       ^
                Array size   idx=1        idx=2   idx=3   idx=4
                row2: ``  - empty because it is null
                row3: `2000  0 2000 Ok  0 4000 then`
                       ^     ^          ^
                Array size   idx=1      idx=2

        Returns:
            A bytes of packed array that could be sent to SQREAM

            Examples from description:
            1. b'\x00\x01\x00\x0f\x00\x00\x00\x00\x00\x00\x00\n\x00\x00\x00'
               b'\x00\x01\x00\x00\x00\x01\x00\x00\x00\x00\x00\x08\x00\x00'
               b'\x00\x00\x02\x00\x00\x00\x00\x05\x00\x00\x00'
            2. b'\x00\x01\x00#\x00\x00\x00\x00\x00\x00\x00\x14\x00\x00\x00'
               b'\x04\x00\x00\x00\x00\x04\x00\x00\x00WORK\x00\x00\x00\x00'
               b'\x00\x01\x00\x00\x00\x00\x00\x07\x00\x00\x00IS DONE\x02'
               b'\x00\x00\x00\x00\x02\x00\x00\x00Ok\x00\x04\x00\x00\x00then'
        """

        py_types = TYPE_MAPPER.get_python_types(self.array_metadata.element_type)
        transform_func = self._get_data_to_bytes_transform_func()

        nulls = []
        lengths = []
        data_list = []

        for row in data:
            if self.array_metadata.nullable:
                nulls.append(pack('?', row is None))
            elif row is None:
                raise DataError("Null value in non-nullable column")

            d_size = self._pack_row(row, py_types, transform_func, data_list)
            lengths.append(pack('i', d_size))

        return b''.join(nulls + lengths + data_list)

    def _pack_row(self, row: Optional[List[Any]], py_types: tuple,
                  transform_func: Callable, data_list: List[bytes]) -> int:
        """Pack a single row of array data."""

        if row is None or len(row) == 0:
            return 0

        d_size = 0

        if self.array_metadata.array_type == ArrayDataType.UNFIXED:
            data_list.append(pack('i', len(row)))
            d_size = 4

        for val in row:
            is_null = val is None
            if not is_null and not isinstance(val, py_types):
                raise DataError(f"Invalid type in array: {type(val)}. Expected: {py_types}")

            data_list.append(pack('?', is_null))
            data_list.append(transform_func(val))
            d_size += len(data_list[-1]) + 1

        return d_size

    def unpack(self, column_data: ColumnData) -> List[Optional[List[Any]]]:
        """Unpack array data from binary format."""

        column_data.array_lengths = column_data.array_lengths.cast('i')

        if self.array_metadata.array_type == ArrayDataType.UNFIXED:
            return self._unpack_unfixed_array(column_data)
        return self._unpack_fixed_array(column_data)

    def _unpack_fixed_array(self, column_data: ColumnData) -> List[Optional[List[Any]]]:
        """
        Extract array with data of fixed size
        Extract array from binary data of an Array with types of fixed
        size (BOOL, TINYINT, SMALLINT, INT, BIGINT, REAL, DOUBLE,
        NUMERIC, DATE, DATETIME, DATETIME2). But not with TEXT
        Raw data contains binary data of nulls at each index in array
        and data separated by optional padding (trailing zeros at the
        end for portions of data whose lengths are not dividable by 8)
        Example for binary data for 1 row of boolean array[true, null,
        false]:
        `010 00000 100` -> replace paddings with _ `010_____100` where
        `010` are flag of null data inside array. Then `00000` is a
        padding to make lengths of data about nulls to be dividable by 8
        in case of array of length 8, 16, 24, 32 ... there won't be a
        padding then `100` is a binary representation of 3 boolean
        values itself
        """

        transform_func = self._get_bytes_to_data_transform_func()
        result = []
        start = 0

        for buf_len, is_null in zip(column_data.array_lengths, column_data.nullable or false_generator()):
            if is_null:
                result.append(None)
            else:
                array_size = get_array_size(self.array_metadata.data_size, buf_len)
                padding = self.pad_array(array_size)

                data = column_data.data_column[start + array_size + padding:start + buf_len]
                nulls = column_data.data_column[start:start + array_size]

                array_data = [
                    transform_func(data[i * self.array_metadata.data_size:(i + 1) * self.array_metadata.data_size], nulls[i])
                    for i in range(array_size)
                ]
                result.append(array_data)
                start += buf_len

        return result

    def _unpack_unfixed_array(self, column_data: ColumnData) -> List[Optional[List[Any]]]:
        """
        Extract array with data of unfixed size
        Extract array from binary data of an Array with types of TEXT
        - unfixed size
        Contains 8 bytes (long) that contains length of whole array
        (including nulls), binary data of nulls at each index in array
        and data separated by optional padding. Data here represents
        chunked info of each element inside array
        At the beginning, the data contains **cumulative** lengths
        (however is better to say indexes of their ends at data buffer)
        of all data strings (+ their paddings) of array as integers.
        The number of those int lengths is equal to the array length
        (those was in 8 bytes above) and because int take 4 bytes it all
        takes N * 4 bytes. Then if it is not divisible by 8 -> + padding
        Then the strings data also separated by optional padding
        Example for binary data for 1 row of text array['ABC','ABCDEF',null]:
        (padding zeros replaced with _)
        Whole buffer data: `3000000 001_____ 3000 14000 16000 ____ `
                           `65 66 67 _____ 65 66 67 68 69 70 __`
        Length of array: `3000000` -> long 3
        Nulls: `001_____`
        Length of strings: `3000 14000 16000 ____` -> 3,14,16 + padding
        Strings: `65, 66, 67, _____ 65, 66, 67, 68, 69, 70, __`
        L1 = 3, so [0 - 3) is string `65 66 67` -> ABC, padding P1=5
        L2 = 14 (which is L1 + padding + current_length), so
        current_length = L2 - (L1 + P1) = 14 - (5 + 3) = 6, P2=2
        => [5 + 3, 14) is string `65, 66, 67, 68, 69, 70` -> ABCDEF
        L3 = 16 => current_length = L3 - (L2 + P2) = 16 - (14 + 2) = 0
        thus string is empty, and considering Nulls -> it is a null
        """

        result = []
        start = 0

        for buf_len, is_null in zip(column_data.array_lengths, column_data.nullable or false_generator()):
            if is_null:
                result.append(None)
            elif not buf_len:
                result.append([])
            else:
                array_size = column_data.data_column[start: start + 8].cast('q')[0]  # Long
                padding = self.pad_array(array_size)
                cur = start + 8 + array_size + padding
                # data lengths
                d_len = column_data.data_column[cur:cur + array_size * 4].cast('i')
                cur += (array_size + array_size % 2) * 4

                # Slices of memoryview do not copy underlying data
                data = column_data.data_column[cur:start + buf_len]
                nulls = column_data.data_column[start + 8:start + 8 + array_size]

                array_data = self._construct_string_array(nulls, d_len, data)
                result.append(array_data)
            start += buf_len

        return result

    @staticmethod
    def pad_array(array_size: int):
        """
        Calculate padding needed to align array data
        """

        return (8 - array_size % 8) % 8

    @staticmethod
    def _construct_string_array(nulls: memoryview, lengths: memoryview,
                                string_data: memoryview) -> List[Optional[str]]:
        """
        Construct string array from components using arr_lengths_to_pairs for proper length handling.

        Args:
            nulls: memoryview of null indicators
            lengths: memoryview of string lengths
            string_data: memoryview of actual string data

        Returns:
            List of strings or None values
        """

        result = []
        # Use arr_lengths_to_pairs to properly handle cumulative lengths
        for is_null, (start, end) in zip(nulls, arr_lengths_to_pairs(lengths)):
            if is_null:
                result.append(None)
            else:
                string_bytes = string_data[start:end]
                result.append(string_bytes.tobytes().decode('utf8'))
        return result

    def _get_data_to_bytes_transform_func(self) -> Callable[[Any], bytes]:
        """Get appropriate data transformation function based on type."""

        transform_funcs = {
            'ftNumeric': lambda data: (decimal_to_sq_numeric(data, self.array_metadata.scale)
                                       if data else 0).to_bytes(16, byteorder='little', signed=True),
            'ftDate': lambda data: pack(TYPE_MAPPER.get_pack_code('ftDate'),
                                        date_to_int(data) if data else 0),
            'ftDateTime': lambda data: pack(TYPE_MAPPER.get_pack_code('ftDateTime'),
                                            datetime_to_long(data) if data else 0),
            'ftTimestampTz': lambda data: pack(TYPE_MAPPER.get_pack_code('ftTimestampTz'),
                                               *pandas_timestamp_to_sq_datetime2(data)) if data else pack(TYPE_MAPPER.get_pack_code('ftTimestampTz'), 0, 0, 0, 0)
        }

        if self.array_metadata.array_type == ArrayDataType.UNFIXED:
            return lambda data: pack(f'i{len(data)}s', len(data),
                                     data.encode()) if data else b'\x00\x00\x00\x00'

        return transform_funcs.get(
            self.array_metadata.element_type,
            lambda data: pack(TYPE_MAPPER.get_pack_code(self.array_metadata.element_type),
                              data if data is not None else 0)
        )

    def _get_bytes_to_data_transform_func(self) -> Callable:
        """Get appropriate bytes to data transformation function."""
        element_type = self.array_metadata.element_type
        data_format = TYPE_MAPPER.get_pack_code(element_type)

        transform_funcs = {
            'ftNumeric': lambda data: sq_numeric_to_decimal(data, self.array_metadata.scale),
            'ftTimestampTz': lambda data: sq_datetime2_to_pandas_timestamp(data),
            'ftDate': lambda data: sq_date_to_py_date(data.cast(data_format)[0]),
            'ftDateTime': lambda data: sq_datetime_to_py_datetime(data.cast(data_format)[0]),
        }

        default_transform = lambda data: data.cast(data_format)[0]
        transform_func = transform_funcs.get(element_type, default_transform)

        return lambda mem, is_null=False: None if is_null else transform_func(mem)
