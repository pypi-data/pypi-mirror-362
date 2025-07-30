import pytest
import struct
import pandas as pd
from pysqream import casting
from datetime import datetime
from tests.test_base import TestBaseWithoutBeforeAfter


class TestDatetimeUnitTest(TestBaseWithoutBeforeAfter):

    def test_zero_date(self):
        with pytest.raises(Exception, match="year 0 is out of range"):
            casting.sq_date_to_py_date(0, is_null=False)

    def test_zero_datetime(self):
        with pytest.raises(Exception, match="year 0 is out of range"):
            casting.sq_datetime_to_py_datetime(0, is_null=False)

    def test_negative_date(self):
        with pytest.raises(Exception, match="year -9 is out of range"):
            casting.sq_date_to_py_date(-3000, is_null=False)

    def test_negative_datetime(self):
        with pytest.raises(Exception, match="year 0 is out of range"):
            casting.sq_datetime_to_py_datetime(-3000, is_null=False)

    def test_null_date(self):
        res = casting.sq_date_to_py_date(-3000, is_null=True)
        assert res is None, f"Excepted to get None, but got [{res}]"

    def test_null_datetime(self):
        res = casting.sq_datetime_to_py_datetime(-3000, is_null=True)
        assert res is None, f"Excepted to get None, but got [{res}]"

    insert_data = [
        datetime(2015, 12, 24, 13, 11, 23, 0),
        datetime(2015, 12, 31, 23, 59, 59, 999),
        datetime(2015, 12, 24, 13, 11, 23, 1000),
        datetime(2015, 12, 24, 13, 11, 23, 1500),
        datetime(2015, 12, 31, 23, 59, 59, 2000),
    ]
    expected_result = [
        datetime(2015, 12, 24, 13, 11, 23),
        datetime(2015, 12, 31, 23, 59, 59, 1000),
        datetime(2015, 12, 24, 13, 11, 23, 1000),
        datetime(2015, 12, 24, 13, 11, 23, 2000),
        datetime(2015, 12, 31, 23, 59, 59, 2000),
    ]

    @pytest.mark.parametrize("input_datetime, expected_result", zip(insert_data, expected_result))
    def test_datetime_milliseconds_round(self, input_datetime, expected_result):
        """test case for SQ-13969"""

        dt_as_long = casting.datetime_to_long(input_datetime)
        long_as_dt = casting.sq_datetime_to_py_datetime(dt_as_long)

        assert long_as_dt == expected_result


class TestDatetime2UnitTest(TestBaseWithoutBeforeAfter):

    def test_pandas_timestamp_to_sq_datetime2(self):
        # Test regular datetime conversion
        dt = pd.Timestamp("1997-12-31 23:59:59.123456789")
        utc_offset, nanos, time_int, date_int = casting.pandas_timestamp_to_sq_datetime2(dt)

        assert utc_offset == 0
        assert nanos == 456789  # Only sub-millisecond part
        assert time_int == 86399123  # 23:59:59.123
        assert date_int == 729694  # 1997-12-31

        # Test None input
        result = casting.pandas_timestamp_to_sq_datetime2(None)
        assert result == casting.SQREAM_OLDEST_DATETIME2

        # Test midnight
        dt = pd.Timestamp("2000-01-01 00:00:00")
        utc_offset, nanos, time_int, date_int = casting.pandas_timestamp_to_sq_datetime2(dt)
        assert time_int == 0
        assert nanos == 0

    def test_sq_datetime2_to_pandas_timestamp(self):
        """Test that converts bytes coming from SQream to pandas timestamp and back to bytes"""
        example_bytes = b'\x00\x00\x00\x00U\xf8\x06\x00\x93X&\x05^"\x0b\x00'
        result = casting.sq_datetime2_to_pandas_timestamp(example_bytes, False)

        components = casting.pandas_timestamp_to_sq_datetime2(result)
        datetime2_bytes = struct.pack('<iiii', *components)
        assert datetime2_bytes == example_bytes

        # Test null case
        assert casting.sq_datetime2_to_pandas_timestamp(example_bytes, True) is None

    def test_roundtrip_conversion(self):
        """Test that converting to SQream format and back gives the same datetime"""
        original_dt = pd.Timestamp("1997-12-31 23:59:59.123456789")

        components = casting.pandas_timestamp_to_sq_datetime2(original_dt)
        datetime2_bytes = struct.pack('<iiii', *components)

        result_dt = casting.sq_datetime2_to_pandas_timestamp(datetime2_bytes, False)

        assert str(result_dt) == str(original_dt) + "+00:00"

    @pytest.mark.parametrize("dt", [
        pd.Timestamp("1970-01-17 18:56:04.205739Z"),
        pd.Timestamp("1970-01-17 18:56:04.205739789+00:00"),
        pd.Timestamp("1970-01-17 18:56:04.205739789+02:00"),
        pd.Timestamp("1970-01-17 18:56:04.205739789 +05:30"),
        pd.Timestamp("1970-01-17 18:56:04.205739789-05:00"),
        pd.Timestamp("1970-01-17 18:56:04.205739789 -08:00"),
    ])
    def test_datetime2_timezone_conversions(self, dt):
        """
        checking UTC time, Positive time zone offsets and Negative time zone offsets
        Verifies timezone information is preserved through conversion
        """

        components = casting.pandas_timestamp_to_sq_datetime2(dt)
        datetime2_bytes = struct.pack('<iiii', *components)
        result_dt = casting.sq_datetime2_to_pandas_timestamp(datetime2_bytes, False)

        assert str(result_dt) == str(dt)
