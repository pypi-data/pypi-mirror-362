import pandas as pd
import pytest
import numpy as np
from datetime import date, datetime
from decimal import Decimal
from tests.test_base import TestBaseWithoutBeforeAfter
from pysqream.utils import DataError
from pysqream.column_packers.number_packers.number_packer import NumberPacker
from pysqream.column_packers.number_packers.decimal_packer import DecimalPacker
from pysqream.column_packers.chars_packers.blob_packer import BlobPacker
from pysqream.column_packers.chars_packers.varchar_packer import VarcharPacker
from pysqream.column_packers.date_packers.date_packer import DatePacker
from pysqream.column_packers.date_packers.datetime_packer import DateTimePacker
from pysqream.column_packers.date_packers.timestamptz_packer import TimestampTzPacker
from pysqream.column_packers.array_packers.array_packer import ArrayPacker
from pysqream.column_packers.array_packers.numpy_array_packer import NumpyArrayPacker
from pysqream.column_packers.column_packer import ColumnMetadata


class TestColumnBufferUnitTests(TestBaseWithoutBeforeAfter):
    def test_pack_numpy_array(self):
        """Test handling of numpy arrays."""
        pytest.skip("Skipping this test until numpy array packer is fixed in column_buffer and uncommented in packer factory")
        arr = np.array([1.1, 2.2, 3.3])
        metadata = ColumnMetadata(1, 'ftFloat', 4, False, False, 0)
        packer = NumpyArrayPacker(metadata)
        packed = packer.pack(arr)

        assert isinstance(packed, bytes)
        assert len(packed) > 0

    def test_blob_packer_not_null(self):
        """Test that BlobPacker packs string data properly."""
        metadata = ColumnMetadata(1, 'ftBlob', 0, False, False, 0)
        packer = BlobPacker(metadata)
        data = ['Hello World']
        packed = packer.pack(data)
        expected_packed = b'\x0b\x00\x00\x00Hello World'

        assert packed == expected_packed

    def test_blob_packer_null(self):
        """Test that BlobPacker packs string data properly."""
        metadata = ColumnMetadata(1, 'ftBlob', 0, True, True, 0)
        packer = BlobPacker(metadata)
        data = ['Hello World']
        packed = packer.pack(data)
        expected_packed = b'\x00\x0b\x00\x00\x00Hello World'

        assert packed == expected_packed

    def test_varchar_packer_not_null(self):
        """Test that VarcharPacker packs fixed-size varchar data."""
        metadata = ColumnMetadata(1, 'ftVarchar', 10, False, False, 0)
        packer = VarcharPacker(metadata)
        data = ["short", "longerstring"]
        packed = packer.pack(data)
        expected_packed = b'short     longerstri'  # short is padded to 10 bytes while longer string is truncated to 10

        assert packed == expected_packed

    def test_varchar_packer_null(self):
        """Test that VarcharPacker packs fixed-size varchar data."""
        metadata = ColumnMetadata(1, 'ftVarchar', 10, True, False, 0)
        packer = VarcharPacker(metadata)
        data = ["short", "longerstring"]
        packed = packer.pack(data)
        expected_packed = b'\x00\x00short     longerstri'  # short is padded to 10 bytes while longer string is truncated to 10

        assert packed == expected_packed

    def test_number_packer_not_null(self):
        """Test that NumberPacker packs integer data correctly."""
        metadata = ColumnMetadata(1, 'ftInt', 4, False, False, 0)
        packer = NumberPacker(metadata)
        data = [1, 256, 1024]
        packed = packer.pack(data)
        expected_packed = b'\x01\x00\x00\x00\x00\x01\x00\x00\x00\x04\x00\x00'

        assert packed == expected_packed

    def test_number_packer_null(self):
        """Test that NumberPacker packs integer data correctly."""
        metadata = ColumnMetadata(1, 'ftInt', 4, True, False, 0)
        packer = NumberPacker(metadata)
        data = [1, 256, 1024]
        packed = packer.pack(data)
        expected_packed = b'\x00\x00\x00\x01\x00\x00\x00\x00\x01\x00\x00\x00\x04\x00\x00'

        assert packed == expected_packed

    def test_date_packer_not_null(self):
        """Test that DatePacker correctly packs date values."""
        metadata = ColumnMetadata(1, 'ftDate', 4, False, False, 0)
        packer = DatePacker(metadata)
        data = [date(2023, 2, 1), date(2020, 12, 25)]
        packed = packer.pack(data)
        expected_packed = b')F\x0b\x00)C\x0b\x00'
        assert len(packed) == 8 and packed == expected_packed  # 2 dates of 4 bytes each

    def test_date_packer_null(self):
        """Test that DatePacker correctly packs date values."""
        metadata = ColumnMetadata(1, 'ftDate', 4, True, False, 0)
        packer = DatePacker(metadata)
        data = [date(2023, 2, 1), date(2020, 12, 25)]
        packed = packer.pack(data)
        expected_packed = b'\x00\x00)F\x0b\x00)C\x0b\x00'

        assert len(packed) == 10 and packed == expected_packed  # 2 dates of 4 bytes each and 2 nulls

    def test_datetime_packer_not_null(self):
        """Test that DateTimePacker correctly packs datetime values."""
        metadata = ColumnMetadata(1, 'ftDateTime', 8, False, False, 0)
        packer = DateTimePacker(metadata)
        data = [datetime(2023, 2, 1, 14, 30, 0), datetime(2020, 12, 25, 9, 15, 45)]
        packed = packer.pack(data)
        expected_packed = b'@\x82\x1c\x03)F\x0b\x00\xe8\xcd\xfc\x01)C\x0b\x00'

        assert len(packed) == 16 and packed == expected_packed

    def test_datetime_packer_null(self):
        """Test that DateTimePacker correctly packs datetime values."""
        metadata = ColumnMetadata(1, 'ftDateTime', 8, True, False, 0)
        packer = DateTimePacker(metadata)
        data = [datetime(2023, 2, 1, 14, 30, 0), datetime(2020, 12, 25, 9, 15, 45)]
        packed = packer.pack(data)
        expected_packed = b'\x00\x00@\x82\x1c\x03)F\x0b\x00\xe8\xcd\xfc\x01)C\x0b\x00'

        assert len(packed) == 18 and packed == expected_packed

    def test_decimal_packer_not_null(self):
        """Test that DecimalPacker correctly packs decimal values."""
        metadata = ColumnMetadata(1, 'ftNumeric', 16, False, False, 2)
        packer = DecimalPacker(metadata)
        data = [Decimal('123.45'), Decimal('6789.01')]
        packed = packer.pack(data)
        expected_packed = b'90\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\xf5[\n\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'

        # Assert packed size is 32 bytes (2 decimals of 16 bytes each)
        assert len(packed) == 32
        assert isinstance(packed, bytes)
        assert expected_packed == packed

    def test_decimal_packer_null(self):
        """Test that DecimalPacker correctly packs decimal values."""
        metadata = ColumnMetadata(1, 'ftNumeric', 16, True, False, 2)
        packer = DecimalPacker(metadata)
        data = [Decimal('123.45'), Decimal('6789.01')]
        packed = packer.pack(data)
        expected_packed = b'\x00\x0090\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\xf5[\n\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'

        # Assert packed size is 34 bytes (2 decimals of 16 bytes each and 2 nulls)
        assert len(packed) == 34
        assert isinstance(packed, bytes)
        assert expected_packed == packed

    def test_array_packer(self):
        """Test that ArrayPacker packs integer arrays correctly."""
        metadata = ColumnMetadata(1, ['ftArray', 'ftInt'], 4, True, False, 0)
        packer = ArrayPacker(metadata)
        data = [[1, 2, 3], None, [4, 5]]
        packed = packer.pack(data)

        # Check the packed content includes lengths and values for arrays
        assert isinstance(packed, bytes)
        assert len(packed) > 0

    def test_timestamptz_packer_not_null(self):
        """Test that TimestampTzPacker correctly packs high-precision datetime values."""
        metadata = ColumnMetadata(1, 'ftTimestampTz', 16, False, False, 0)
        packer = TimestampTzPacker(metadata)

        # Sample datetime values, including nanosecond precision
        data = [pd.Timestamp('2023-02-01 14:30:00.123456789'),
                pd.Timestamp('2020-12-25T09:15:45.987654321')]

        packed = packer.pack(data)
        expected_packed = b'\x00\x00\x00\x00U\xf8\x06\x00\xbb\x82\x1c\x03)F\x0b\x00\x00\x00\x00\x00\xf1\xfb\t\x00\xc3\xd1\xfc\x01)C\x0b\x00'

        assert isinstance(packed, bytes)
        assert len(packed) == 32  # Two datetime2 values, each packed as 16 bytes
        assert packed == expected_packed

    def test_timestamptz_packer_null(self):
        """Test that TimestampTzPacker correctly packs high-precision datetime values."""
        metadata = ColumnMetadata(1, 'ftTimestampTz', 16, True, False, 0)
        packer = TimestampTzPacker(metadata)

        # Sample datetime values, including nanosecond precision
        data = [pd.Timestamp('2023-02-01 14:30:00.123456789'),
                pd.Timestamp('2020-12-25 09:15:45.987654321')]

        packed = packer.pack(data)
        expected_packed = b'\x00\x00\x00\x00\x00\x00U\xf8\x06\x00\xbb\x82\x1c\x03)F\x0b\x00\x00\x00\x00\x00\xf1\xfb\t\x00\xc3\xd1\xfc\x01)C\x0b\x00'

        assert isinstance(packed, bytes)
        assert len(packed) == 34  # Two datetime2 values, each packed as 16 bytes, and 2 nulls
        assert packed == expected_packed

    def test_blob_packer_invalid_data(self):
        """Test that BlobPacker raises an error for non-string data."""
        metadata = ColumnMetadata(1, 'ftBlob', 0, False, False, 0)
        packer = BlobPacker(metadata)

        with pytest.raises(AttributeError):
            packer.pack([123, None])

    def test_array_packer_invalid_type(self):
        """Test that ArrayPacker raises error for invalid element type."""
        metadata = ColumnMetadata(1, ['ftArray', 'ftInt'], 4, True, False, 0)
        packer = ArrayPacker(metadata)
        data = [[1, 'invalid', 3], [4, 5]]

        with pytest.raises(DataError):
            packer.pack(data)

    def test_handle_nulls(self):
        """Test that null handling works correctly in ColumnPacker."""
        metadata = ColumnMetadata(1, 'ftInt', 4, True, False, 0)
        packer = NumberPacker(metadata)
        data = [1, None, 3, None, 5, pd.NA, 'NA', np.NaN, 'NaN', pd.NaT]
        packer.allocate_buf_map()
        packer.handle_nulls(data)

        # Verify buffer content has null markers (0x01)
        nulls_written = packer.buf_map[:10]
        assert nulls_written == b'\x00\x01\x00\x01\x00\x01\x00\x01\x00\x01'

    def test_array_packer_empty_array(self):
        """Test ArrayPacker with empty arrays."""
        metadata = ColumnMetadata(1, ['ftArray', 'ftInt'], 4, True, False, 0)
        packer = ArrayPacker(metadata)
        data = [[]]
        packed = packer.pack(data)
        assert isinstance(packed, bytes)

    def test_array_packer_mixed_types(self):
        """Test ArrayPacker with mixed nullable and non-nullable arrays."""
        metadata = ColumnMetadata(1, ['ftArray', 'ftVarchar'], 10, True, False, 0)
        packer = ArrayPacker(metadata)
        data = [['hello', 'world'], None, ['test']]
        packed = packer.pack(data)
        assert isinstance(packed, bytes)

    def test_numpy_array_packer_mixed_types(self):
        """Test NumpyArrayPacker with different numpy data types."""
        pytest.skip("Skipping this test until numpy array packer is fixed in column_buffer and uncommented in packer factory")
        # Test string arrays
        str_metadata = ColumnMetadata(1, 'ftVarchar', 10, True, False, 0)
        str_packer = NumpyArrayPacker(str_metadata)
        str_data = np.array(['hello', 'world', 'test'])
        packed_str = str_packer.pack(str_data)
        assert isinstance(packed_str, bytes)

        # Test datetime arrays
        dt_metadata = ColumnMetadata(1, 'ftTimestampTz', 16, True, False, 0)
        dt_packer = NumpyArrayPacker(dt_metadata)
        dt_data = np.array([pd.Timestamp('2023-01-01'), pd.Timestamp('2023-02-02')])
        packed_dt = dt_packer.pack(dt_data)
        assert isinstance(packed_dt, bytes)

    def test_decimal_packer_extreme_values(self):
        """Test DecimalPacker with extreme decimal values."""
        metadata = ColumnMetadata(1, 'ftNumeric', 16, False, False, 2)
        packer = DecimalPacker(metadata)

        data = [Decimal('9999999999.99'), Decimal('-9999999999.99')]
        packed = packer.pack(data)

        assert isinstance(packed, bytes)
        assert len(packed) == 32

    def test_date_conversion_edge_cases(self):
        """Test date conversion with boundary dates."""
        metadata = ColumnMetadata(1, 'ftDate', 4, False, False, 0)
        packer = DatePacker(metadata)

        # Test minimum and maximum representable dates
        data = [date.min, date.max]
        packed = packer.pack(data)

        assert isinstance(packed, bytes)
        assert len(packed) == 8

    def test_datetime_conversion_timezone(self):
        """Test datetime packing with timezone-aware datetimes."""
        from datetime import timezone
        metadata = ColumnMetadata(1, 'ftDateTime', 8, False, False, 0)
        packer = DateTimePacker(metadata)

        # Test with timezone-aware datetime
        tz_datetime = datetime(2023, 1, 1, 12, 0, 0, tzinfo=timezone.utc)
        data = [tz_datetime]
        packed = packer.pack(data)

        assert isinstance(packed, bytes)
