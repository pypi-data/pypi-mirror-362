import pytest
import datetime
import pandas as pd
from decimal import Decimal
from tests.test_base import TestBaseWithoutBeforeAfter
from pysqream.utils import ProgrammingError
from pysqream.column_buffer import ColumnsBuffer
from pysqream.column_packers.chars_packers.varchar_packer import VarcharPacker
from pysqream.column_packers.column_packer import ColumnMetadata
from pysqream.type_mapper import TypeMapper
from pysqream.logger import ContextLogger


@pytest.fixture
def column_buffer():
    """Fixture for a clean instance of ColumnBuffer."""
    return ColumnsBuffer(ContextLogger())


@pytest.fixture
def type_mapper():
    """Fixture for a clean instance of TypeMapper."""
    return TypeMapper()


class TestColumnBufferUnitTests(TestBaseWithoutBeforeAfter):
    def test_pack_columns_basic(self, column_buffer):
        """Test basic column packing with simple integer data."""
        cols = [[1, 2, 3]]
        col_types = ['ftInt']
        col_sizes = [4]
        col_nul = [False]
        col_tvc = [False]
        col_scales = [0]

        packed = column_buffer.pack_columns(cols, capacity=3, col_types=col_types,
                                            col_sizes=col_sizes, col_nul=col_nul,
                                            col_tvc=col_tvc, col_scales=col_scales)
        assert len(packed) == 1
        assert isinstance(packed[0], bytes)
        assert len(packed[0]) > 0

    def test_pack_nullable_column(self, column_buffer):
        """Test packing with nullable values."""
        cols = [[1, None, 3]]
        col_types = ['ftInt']
        col_sizes = [4]
        col_nul = [True]
        col_tvc = [False]
        col_scales = [0]

        packed = column_buffer.pack_columns(cols, capacity=3, col_types=col_types,
                                            col_sizes=col_sizes, col_nul=col_nul,
                                            col_tvc=col_tvc, col_scales=col_scales)
        assert len(packed) == 1
        assert isinstance(packed[0], bytes)
        assert len(packed[0]) > 0

    def test_clear_buffer(self, column_buffer):
        """Test clearing the buffer."""
        column_buffer.current_packers.append(VarcharPacker(ColumnMetadata(1, 'ftVarchar', 10, False, False, 0)))
        column_buffer.clear()

        assert len(column_buffer.current_packers) == 0

    def test_pack_invalid_data(self, column_buffer):
        """Test handling of invalid data types."""
        cols = [[Decimal('10.5')]]
        col_types = ['ftInt']
        col_sizes = [4]
        col_nul = [False]
        col_tvc = [False]
        col_scales = [0]

        with pytest.raises(ProgrammingError):
            column_buffer.pack_columns(cols, capacity=1, col_types=col_types,
                                       col_sizes=col_sizes, col_nul=col_nul,
                                       col_tvc=col_tvc, col_scales=col_scales)

    def test_column_buffer_empty_columns(self, column_buffer):
        """Test handling of empty columns."""
        cols = [[]]
        col_types = ['ftInt']
        col_sizes = [4]
        col_nul = [False]
        col_tvc = [False]
        col_scales = [0]

        packed = column_buffer.pack_columns(cols, capacity=0, col_types=col_types,
                                            col_sizes=col_sizes, col_nul=col_nul,
                                            col_tvc=col_tvc, col_scales=col_scales)
        assert len(packed) == 1
        assert isinstance(packed[0], bytes)
        assert len(packed[0]) == 0

    def test_complex_nullable_column_packing(self, column_buffer):
        """Test packing of complex nullable columns with mixed data types."""
        cols = [
            [1, None, 3],
            ['hello', None, 'world'],
            [Decimal('10.5'), None, Decimal('20.7')]
        ]
        col_types = ['ftInt', 'ftVarchar', 'ftNumeric']
        col_sizes = [4, 10, 16]
        col_nul = [True, True, True]
        col_tvc = [False, False, False]
        col_scales = [0, 0, 2]

        packed = column_buffer.pack_columns(cols, capacity=3, col_types=col_types,
                                            col_sizes=col_sizes, col_nul=col_nul,
                                            col_tvc=col_tvc, col_scales=col_scales)

        assert len(packed) == 3

        for packed_col in packed:
            assert isinstance(packed_col, bytes)
            assert len(packed_col) > 0

    def test_unpack_bool_not_null(self, column_buffer, type_mapper):
        unsorted_data_columns = [memoryview(b'\x01\x00\x01')]
        col_types = ['ftBool']
        col_sizes = [1]
        col_nul = [False]
        col_tvc = [False]
        col_scales = [0]

        unpacked = column_buffer.unpack_columns(unsorted_data_columns, col_types, col_sizes, col_nul, col_tvc, col_scales)
        res = []
        res.extend(zip(*unpacked))

        assert len(res) == 3
        assert res == [(True,), (False,), (True,)]

    def test_unpack_bool_nullable(self, column_buffer, type_mapper):
        unsorted_data_columns = [memoryview(b'\x00\x00\x00\x01'), memoryview(b'\x01\x00\x01\x00')]
        col_types = ['ftBool']
        col_sizes = [1]
        col_nul = [True]
        col_tvc = [False]
        col_scales = [0]

        unpacked = column_buffer.unpack_columns(unsorted_data_columns, col_types, col_sizes, col_nul, col_tvc, col_scales)
        res = []
        res.extend(zip(*unpacked))

        assert len(res) == 4
        assert res == [(True,), (False,), (True,), (None,)]

    def test_unpack_ubyte_not_null(self, column_buffer, type_mapper):
        unsorted_data_columns = [memoryview(b'\x01\xff\x7f')]
        col_types = ['ftUByte']
        col_sizes = [1]
        col_nul = [False]
        col_tvc = [False]
        col_scales = [0]

        unpacked = column_buffer.unpack_columns(unsorted_data_columns, col_types, col_sizes, col_nul, col_tvc, col_scales)
        res = []
        res.extend(zip(*unpacked))

        assert len(res) == 3
        assert res == [(1,), (255,), (127,)]

    def test_unpack_ubyte_nullable(self, column_buffer, type_mapper):
        unsorted_data_columns = [memoryview(b'\x00\x00\x00\x01'), memoryview(b'\x01\xff\x7f\x00')]
        col_types = ['ftUByte']
        col_sizes = [1]
        col_nul = [True]
        col_tvc = [False]
        col_scales = [0]

        unpacked = column_buffer.unpack_columns(unsorted_data_columns, col_types, col_sizes, col_nul, col_tvc, col_scales)
        res = []
        res.extend(zip(*unpacked))

        assert len(res) == 4
        assert res == [(1,), (255,), (127,), (None,)]

    def test_unpack_short_not_null(self, column_buffer, type_mapper):
        unsorted_data_columns = [memoryview(b'\x01\x00\xff\xff')]
        col_types = ['ftShort']
        col_sizes = [2]
        col_nul = [False]
        col_tvc = [False]
        col_scales = [0]

        unpacked = column_buffer.unpack_columns(unsorted_data_columns, col_types, col_sizes, col_nul, col_tvc, col_scales)
        res = []
        res.extend(zip(*unpacked))

        assert len(res) == 2
        assert res == [(1,), (-1,)]

    def test_unpack_short_nullable(self, column_buffer, type_mapper):
        unsorted_data_columns = [memoryview(b'\x00\x00\x01'), memoryview(b'\x01\x00\xff\xff\x00\x00')]
        col_types = ['ftShort']
        col_sizes = [2]
        col_nul = [True]
        col_tvc = [False]
        col_scales = [0]

        unpacked = column_buffer.unpack_columns(unsorted_data_columns, col_types, col_sizes, col_nul, col_tvc, col_scales)
        res = []
        res.extend(zip(*unpacked))

        assert len(res) == 3
        assert res == [(1,), (-1,), (None,)]

    def test_unpack_columns_int_not_null(self, column_buffer, type_mapper):
        """Test basic column unpacking with integer data."""
        unsorted_data_columns = [memoryview(b'\x01\x00\x00\x00\x02\x00\x00\x00\x03\x00\x00\x00')]
        col_types = ['ftInt']
        col_sizes = [4]
        col_nul = [False]
        col_tvc = [False]
        col_scales = [0]

        unpacked = column_buffer.unpack_columns(unsorted_data_columns, col_types, col_sizes, col_nul, col_tvc, col_scales)
        res = []
        res.extend(zip(*unpacked))

        assert len(res) == 3
        assert res == [(1,), (2,), (3,)]

    def test_unpack_int_nullable(self, column_buffer, type_mapper):
        """Test unpacking columns with null values."""
        unsorted_data_columns = [memoryview(b'\x00\x01\x00'), memoryview(b'\x01\x00\x00\x00\x00\x00\x00\x00\x03\x00\x00\x00')]
        col_types = ['ftInt']
        col_sizes = [4]
        col_nul = [True]
        col_tvc = [False]
        col_scales = [0]

        unpacked = column_buffer.unpack_columns(unsorted_data_columns, col_types, col_sizes, col_nul, col_tvc, col_scales)
        res = []
        res.extend(zip(*unpacked))

        assert len(res) == 3
        assert res == [(1,), (None,), (3,)]

    def test_unpack_long_not_null(self, column_buffer, type_mapper):
        unsorted_data_columns = [memoryview(b'\x01\x00\x00\x00\x00\x00\x00\x00')]
        col_types = ['ftLong']
        col_sizes = [8]
        col_nul = [False]
        col_tvc = [False]
        col_scales = [0]

        unpacked = column_buffer.unpack_columns(unsorted_data_columns, col_types, col_sizes, col_nul, col_tvc, col_scales)
        res = []
        res.extend(zip(*unpacked))

        assert len(res) == 1
        assert res == [(1,)]

    def test_unpack_long_nullable(self, column_buffer, type_mapper):
        unsorted_data_columns = [memoryview(b'\x00\x01'), memoryview(b'\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00')]
        col_types = ['ftLong']
        col_sizes = [8]
        col_nul = [True]
        col_tvc = [False]
        col_scales = [0]

        unpacked = column_buffer.unpack_columns(unsorted_data_columns, col_types, col_sizes, col_nul, col_tvc, col_scales)
        res = []
        res.extend(zip(*unpacked))

        assert len(res) == 2
        assert res == [(1,), (None,)]

    def test_unpack_varchar_not_null(self, column_buffer, type_mapper):
        """Test unpacking varchar columns."""
        unsorted_data_columns = [memoryview(b'test1test2')]
        col_types = ['ftVarchar']
        col_sizes = [5]
        col_nul = [False]
        col_tvc = [False]
        col_scales = [0]

        unpacked = column_buffer.unpack_columns(unsorted_data_columns, col_types, col_sizes, col_nul, col_tvc, col_scales)
        res = []
        res.extend(zip(*unpacked))

        assert len(res) == 2
        assert res == [('test1',), ('test2',)]

    def test_unpack_varchar_nullable(self, column_buffer, type_mapper):
        """Test unpacking varchar columns."""
        unsorted_data_columns = [memoryview(b'\x00\x00\x01'), memoryview(b'test1test2')]
        col_types = ['ftVarchar']
        col_sizes = [5]
        col_nul = [True]
        col_tvc = [False]
        col_scales = [0]

        unpacked = column_buffer.unpack_columns(unsorted_data_columns, col_types, col_sizes, col_nul, col_tvc, col_scales)
        res = []
        res.extend(zip(*unpacked))

        assert len(res) == 3
        assert res == [('test1',), ('test2',), (None,)]

    def test_unpack_text_not_null(self, column_buffer, type_mapper):
        """Test unpacking text columns."""
        unsorted_data_columns = [memoryview(b'\x05\x00\x00\x00\x05\x00\x00\x00'), memoryview(b'test1test2')]
        col_types = ['ftBlob']
        col_sizes = [5]
        col_nul = [False]
        col_tvc = [True]
        col_scales = [0]

        unpacked = column_buffer.unpack_columns(unsorted_data_columns, col_types, col_sizes, col_nul, col_tvc, col_scales)
        res = []
        res.extend(zip(*unpacked))

        assert len(res) == 2
        assert res == [('test1',), ('test2',)]

    def test_unpack_text_nullable(self, column_buffer, type_mapper):
        """Test unpacking text columns."""
        unsorted_data_columns = [memoryview(b'\x00\x00\x01'), memoryview(b'\x05\x00\x00\x00\x05\x00\x00\x00\x00\x00\x00\x00'), memoryview(b'test1test2')]
        col_types = ['ftBlob']
        col_sizes = [5]
        col_nul = [True]
        col_tvc = [True]
        col_scales = [0]

        unpacked = column_buffer.unpack_columns(unsorted_data_columns, col_types, col_sizes, col_nul, col_tvc, col_scales)
        res = []
        res.extend(zip(*unpacked))

        assert len(res) == 3
        assert res == [('test1',), ('test2',), (None,)]

    def test_unpack_numeric_not_null(self, column_buffer, type_mapper):
        """Test unpacking numeric values with scale."""
        unsorted_data_columns = [memoryview(b'\x01\xae\xa6\x8f\x02\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00')]
        col_types = ['ftNumeric']
        col_sizes = [16]
        col_nul = [False]
        col_tvc = [False]
        col_scales = [10]

        unpacked = column_buffer.unpack_columns(unsorted_data_columns, col_types, col_sizes, col_nul, col_tvc, col_scales)
        res = []
        res.extend(zip(*unpacked))

        assert len(res) == 1
        assert res == [(Decimal('1.1000000001'),)]

    def test_unpack_numeric_nullable(self, column_buffer, type_mapper):
        """Test unpacking numeric values with scale."""
        unsorted_data_columns = [memoryview(b'\x00\x01'), memoryview(b'\x01\xae\xa6\x8f\x02\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00')]
        col_types = ['ftNumeric']
        col_sizes = [16]
        col_nul = [True]
        col_tvc = [False]
        col_scales = [10]

        unpacked = column_buffer.unpack_columns(unsorted_data_columns, col_types, col_sizes, col_nul, col_tvc, col_scales)
        res = []
        res.extend(zip(*unpacked))

        assert len(res) == 2
        assert res == [(Decimal('1.1000000001'),), (None,)]

    def test_unpack_double_not_null(self, column_buffer, type_mapper):
        unsorted_data_columns = [memoryview(b'\x9a\x99\x99\x99\x99\x99\xf1?')]
        col_types = ['ftDouble']
        col_sizes = [8]
        col_nul = [False]
        col_tvc = [False]
        col_scales = [0]

        unpacked = column_buffer.unpack_columns(unsorted_data_columns, col_types, col_sizes, col_nul, col_tvc, col_scales)
        res = []
        res.extend(zip(*unpacked))

        assert len(res) == 1
        assert res == [(1.1,)]

    def test_unpack_double_nullable(self, column_buffer, type_mapper):
        unsorted_data_columns = [memoryview(b'\x00\x01'), memoryview(b'\x9a\x99\x99\x99\x99\x99\xf1?\x00\x00\x00\x00\x00\x00\x00\x00')]
        col_types = ['ftDouble']
        col_sizes = [8]
        col_nul = [True]
        col_tvc = [False]
        col_scales = [0]

        unpacked = column_buffer.unpack_columns(unsorted_data_columns, col_types, col_sizes, col_nul, col_tvc, col_scales)
        res = []
        res.extend(zip(*unpacked))

        assert len(res) == 2
        assert res == [(1.1,), (None,)]

    def test_unpack_float_not_null(self, column_buffer, type_mapper):
        unsorted_data_columns = [memoryview(b'\xcd\xcc\x8c?')]
        col_types = ['ftFloat']
        col_sizes = [4]
        col_nul = [False]
        col_tvc = [False]
        col_scales = [0]

        unpacked = column_buffer.unpack_columns(unsorted_data_columns, col_types, col_sizes, col_nul, col_tvc, col_scales)
        res = []
        res.extend(zip(*unpacked))

        assert len(res) == 1
        assert res == [(1.100000023841858,)]

    def test_unpack_float_nullable(self, column_buffer, type_mapper):
        unsorted_data_columns = [memoryview(b'\x00\x01'), memoryview(b'\xcd\xcc\x8c?\x00\x00\x00\x00')]
        col_types = ['ftFloat']
        col_sizes = [4]
        col_nul = [True]
        col_tvc = [False]
        col_scales = [0]

        unpacked = column_buffer.unpack_columns(unsorted_data_columns, col_types, col_sizes, col_nul, col_tvc, col_scales)
        res = []
        res.extend(zip(*unpacked))

        assert len(res) == 2
        assert res == [(1.100000023841858,), (None,)]

    def test_unpack_date_not_null(self, column_buffer, type_mapper):
        unsorted_data_columns = [memoryview(b'\xd7D\x0b\x00')]
        col_types = ['ftDate']
        col_sizes = [4]
        col_nul = [False]
        col_tvc = [False]
        col_scales = [0]

        unpacked = column_buffer.unpack_columns(unsorted_data_columns, col_types, col_sizes, col_nul, col_tvc, col_scales)
        res = []
        res.extend(zip(*unpacked))

        assert len(res) == 1
        assert res == [(datetime.date(2022, 2, 28),)]

    def test_unpack_date_nullable(self, column_buffer, type_mapper):
        unsorted_data_columns = [memoryview(b'\x00\x01'), memoryview(b'\xd7D\x0b\x00\x00\x00\x00\x00')]
        col_types = ['ftDate']
        col_sizes = [4]
        col_nul = [True]
        col_tvc = [False]
        col_scales = [0]

        unpacked = column_buffer.unpack_columns(unsorted_data_columns, col_types, col_sizes, col_nul, col_tvc, col_scales)
        res = []
        res.extend(zip(*unpacked))

        assert len(res) == 2
        assert res == [(datetime.date(2022, 2, 28),), (None,)]

    def test_unpack_datetime_not_null(self, column_buffer, type_mapper):
        unsorted_data_columns = [memoryview(b'\xcbX\xf7\x00r!\x0b\x00')]
        col_types = ['ftDateTime']
        col_sizes = [8]
        col_nul = [False]
        col_tvc = [False]
        col_scales = [0]

        unpacked = column_buffer.unpack_columns(unsorted_data_columns, col_types, col_sizes, col_nul, col_tvc, col_scales)
        res = []
        res.extend(zip(*unpacked))

        assert len(res) == 1
        assert res == [(datetime.datetime(1997, 5, 9, 4, 30, 10, 123000),)]

    def test_unpack_datetime_nullable(self, column_buffer, type_mapper):
        unsorted_data_columns = [memoryview(b'\x00\x01'), memoryview(b'\xcbX\xf7\x00r!\x0b\x00\x00\x00\x00\x00\x00\x00\x00\x00')]
        col_types = ['ftDateTime']
        col_sizes = [8]
        col_nul = [True]
        col_tvc = [False]
        col_scales = [0]

        unpacked = column_buffer.unpack_columns(unsorted_data_columns, col_types, col_sizes, col_nul, col_tvc, col_scales)
        res = []
        res.extend(zip(*unpacked))

        assert len(res) == 2
        assert res == [(datetime.datetime(1997, 5, 9, 4, 30, 10, 123000),), (None,)]

    def test_unpack_datetime2_not_null(self, column_buffer, type_mapper):
        unsorted_data_columns = [memoryview(b'\x00\x00\x00\x00U\xf8\x06\x00\x93X&\x05^"\x0b\x00')]
        col_types = ['ftTimestampTz']
        col_sizes = [16]
        col_nul = [False]
        col_tvc = [False]
        col_scales = [0]

        unpacked = column_buffer.unpack_columns(unsorted_data_columns, col_types, col_sizes, col_nul, col_tvc, col_scales)
        res = []
        res.extend(zip(*unpacked))

        assert len(res) == 1
        assert res == [(pd.Timestamp("1997-12-31 23:59:59.123456789+00:00"), )]

    def test_unpack_datetime2_nullable(self, column_buffer, type_mapper):
        unsorted_data_columns = [memoryview(b'\x00\x01'), memoryview(b'\x00\x00\x00\x00U\xf8\x06\x00\x93X&\x05^"\x0b\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00')]
        col_types = ['ftTimestampTz']
        col_sizes = [16]
        col_nul = [True]
        col_tvc = [False]
        col_scales = [0]

        unpacked = column_buffer.unpack_columns(unsorted_data_columns, col_types, col_sizes, col_nul, col_tvc, col_scales)
        res = []
        res.extend(zip(*unpacked))

        assert len(res) == 2
        assert res == [(pd.Timestamp("1997-12-31 23:59:59.123456789+00:00"), ), (None,)]

    def test_unpack_multiple_columns(self, column_buffer, type_mapper):
        """Test unpacking multiple columns of different types."""
        unsorted_data_columns = [memoryview(b'\x01\x00\x00\x00\x02\x00\x00\x00'),  # column 1, only data no nullable buffer
                                 memoryview(b'\x00\x01'), memoryview(b'\x03\x00\x00\x00\x00\x00\x00\x00')]  # column 2, has nullable so two buffers
        col_types = ['ftInt', 'ftInt']
        col_sizes = [4, 4]
        col_nul = [False, True]
        col_tvc = [False, False]
        col_scales = [0, 0]

        unpacked = column_buffer.unpack_columns(unsorted_data_columns, col_types, col_sizes, col_nul, col_tvc, col_scales)
        res = []
        res.extend(zip(*unpacked))

        assert len(res) == 2
        assert res == [(1, 3), (2, None)]

    def test_unpack_empty_data(self, column_buffer, type_mapper):
        """Test unpacking empty data."""
        unsorted_data_columns = [memoryview(b'')]
        col_types = ['ftInt']
        col_sizes = [4]
        col_nul = [False]
        col_tvc = [False]
        col_scales = [0]

        unpacked = column_buffer.unpack_columns(unsorted_data_columns, col_types, col_sizes, col_nul, col_tvc, col_scales)
        res = []
        res.extend(zip(*unpacked))

        assert len(res) == 0

    def test_unpack_array_data_not_null(self, column_buffer, type_mapper):
        """Test unpacking array data."""
        unsorted_data_columns = [memoryview(b'\x18\x00\x00\x00'), memoryview(b'\x00\x00\x00\x00\x00\x00\x00\x00\x01\x00\x00\x00\x02\x00\x00\x00\x03\x00\x00\x00\x04\x00\x00\x00')]
        col_types = [['ftArray', 'ftInt']]
        col_sizes = [4]
        col_nul = [False]
        col_tvc = [False]
        col_scales = [0]

        unpacked = column_buffer.unpack_columns(unsorted_data_columns, col_types, col_sizes, col_nul, col_tvc, col_scales)
        res = []
        res.extend(zip(*unpacked))

        assert len(res) == 1
        assert res == [([1, 2, 3, 4],)]

    def test_unpack_array_data_nullable(self, column_buffer, type_mapper):
        """Test unpacking array data."""
        unsorted_data_columns = [memoryview(b'\x00\x00\x01'), memoryview(b'\x18\x00\x00\x00\x0c\x00\x00\x00\x00\x00\x00\x00'), memoryview(b'\x00\x00\x00\x00\x00\x00\x00\x00\x01\x00\x00\x00\x02\x00\x00\x00\x03\x00\x00\x00\x04\x00\x00\x00\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00')]
        col_types = [['ftArray', 'ftInt']]
        col_sizes = [4]
        col_nul = [True]
        col_tvc = [False]
        col_scales = [0]

        unpacked = column_buffer.unpack_columns(unsorted_data_columns, col_types, col_sizes, col_nul, col_tvc, col_scales)
        res = []
        res.extend(zip(*unpacked))

        assert len(res) == 3
        assert res == [([1, 2, 3, 4],), ([None],), (None,)]
