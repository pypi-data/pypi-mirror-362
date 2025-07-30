import pytest
import numpy as np
from decimal import Decimal
from datetime import datetime
from pysqream.column_packers.packer_factory import get_packer
from pysqream.column_packers.column_packer import ColumnMetadata, PackingError
from pysqream.column_packers.number_packers.number_packer import NumberPacker
from pysqream.column_packers.number_packers.decimal_packer import DecimalPacker
from pysqream.column_packers.chars_packers.blob_packer import BlobPacker
from pysqream.column_packers.chars_packers.varchar_packer import VarcharPacker
from pysqream.column_packers.date_packers.date_packer import DatePacker
from pysqream.column_packers.date_packers.datetime_packer import DateTimePacker
from pysqream.column_packers.date_packers.timestamptz_packer import TimestampTzPacker
from pysqream.column_packers.array_packers.array_packer import ArrayPacker
from pysqream.column_packers.array_packers.numpy_array_packer import NumpyArrayPacker


class TestGetPacker:
    """Test suite for get_packer factory"""

    def test_array_type(self):
        """Test ftArray type returns ArrayPacker"""
        data = [[1, 2, 3], [4, 5, 6]]
        metadata = ColumnMetadata(0, ['ftArray', 'ftInt'], 4, True, False, 0)
        packer = get_packer(metadata, data=data)

        assert isinstance(packer, ArrayPacker)
        assert packer.metadata == metadata

    def test_numpy_array(self):
        """Test numpy array returns NumpyArrayPacker"""
        pytest.skip("Skipping this test until numpy array packer is fixed in column_buffer and uncommented in packer factory")
        data = [np.array([1, 2, 3])]
        metadata = ColumnMetadata(0, 'ftInt', 4, True, False, 0)
        packer = get_packer(metadata, data=data)

        assert isinstance(packer, NumpyArrayPacker)
        assert packer.metadata == metadata

    def test_basic_numeric_types(self):
        """Test all numeric types return NumberPacker"""
        numeric_types = [
            'ftBool', 'ftUByte', 'ftShort', 'ftInt',
            'ftLong', 'ftFloat', 'ftDouble'
        ]
        for col_type in numeric_types:
            data = [1, 2, 3]
            metadata = ColumnMetadata(0, col_type, 4, True, False, 0)
            packer = get_packer(metadata, data=data)

            assert isinstance(packer, NumberPacker), f"Failed for type {col_type}"
            assert packer.metadata == metadata

    def test_varchar_type(self):
        """Test varchar type returns VarcharPacker"""
        data = ["test1", "test2"]
        metadata = ColumnMetadata(0, 'ftVarchar', 4, True, False, 0)
        packer = get_packer(metadata, data=data)

        assert isinstance(packer, VarcharPacker)
        assert packer.metadata == metadata

    def test_blob_type(self):
        """Test blob type returns BlobPacker"""
        data = ["blob1", "blob2"]
        metadata = ColumnMetadata(0, 'ftBlob', 4, True, True, 0)
        packer = get_packer(metadata, data=data)

        assert isinstance(packer, BlobPacker)
        assert packer.metadata == metadata

    def test_date_types(self):
        """Test date and datetime types return correct packers"""
        date_types = {
            'ftDate': DatePacker,
            'ftDateTime': DateTimePacker,
            'ftTimestampTz': TimestampTzPacker
        }

        for col_type, expected_packer in date_types.items():
            data = [datetime.now()]
            metadata = ColumnMetadata(0, col_type, 4, True, False, 0)
            packer = get_packer(metadata, data=data)

            assert isinstance(packer, expected_packer), f"Failed for type {col_type}"
            assert packer.metadata == metadata

    def test_numeric_type(self):
        """Test numeric/decimal type returns DecimalPacker"""
        data = [Decimal('123.45')]
        metadata = ColumnMetadata(0, 'ftNumeric', 4, True, False, 2)
        packer = get_packer(metadata, data=data)

        assert isinstance(packer, DecimalPacker)
        assert packer.metadata == metadata

    def test_unsupported_type(self):
        """Test unsupported type raises PackingError"""
        data = []
        metadata = ColumnMetadata(0, 'Unsupported', 4, True, False, 0)
        expected_message = "Error packing column 1 of type 'Unsupported', error is: Unsupported column type"

        with pytest.raises(PackingError) as exc_info:
            get_packer(metadata, data=data)

        assert exc_info.value.message == expected_message

    def test_invalid_array_type(self):
        """Test invalid array type configuration raises PackingError"""
        data = []
        metadata = ColumnMetadata(0, ['ftArray'], 4, True, False, 0)  # array is missing second element
        expected_message = "Error packing column 1 of type '['ftArray']', error is: Invalid array type specification"

        with pytest.raises(PackingError) as exc_info:
            get_packer(metadata, data=data)

        assert exc_info.value.message == expected_message

    def test_none_type(self):
        """Test None type raises PackingError"""
        data = []
        metadata = ColumnMetadata(0, None, 4, True, False, 0)

        with pytest.raises(PackingError) as exc_info:
            get_packer(metadata, data=data)

        assert exc_info.value.message == "Unsupported column type"
