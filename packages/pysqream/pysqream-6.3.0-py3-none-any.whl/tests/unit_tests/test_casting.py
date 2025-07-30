import pytest
import struct
import pandas as pd
from decimal import Decimal
from datetime import date, datetime
from math import ceil
from pysqream.casting import (
    _get_date_int,
    date_to_int,
    datetime_to_long,
    sq_numeric_to_decimal,
    decimal_to_sq_numeric,
    lengths_to_pairs,
    arr_lengths_to_pairs,
    SQREAM_OLDEST_DATETIME_LONG,
    SQREAM_OLDEST_DATE_LONG,
    SQREAM_OLDEST_DATETIME2,
    sq_date_to_py_date,
    sq_datetime_to_py_datetime,
    pandas_timestamp_to_sq_datetime2,
    sq_datetime2_to_pandas_timestamp
)


class TestCasting:

    def test__get_date_int_known_date(self):
        assert _get_date_int(1900, 1, 1) == SQREAM_OLDEST_DATE_LONG

    def test__get_date_int_leap_year(self):
        assert _get_date_int(2000, 2, 29) == _get_date_int(2000, 2, 28) + 1

    def test__get_date_int_oldest_supported(self):
        assert _get_date_int(1900, 1, 1) == SQREAM_OLDEST_DATE_LONG

    def test__get_date_int_new_century(self):
        assert _get_date_int(2000, 1, 1) < _get_date_int(2024, 1, 1)

    def test__get_date_int_start_end_of_year(self):
        jan = _get_date_int(2024, 1, 1)
        dec = _get_date_int(2024, 12, 31)
        assert dec > jan

    def test__get_date_int_year_boundary(self):
        assert _get_date_int(1, 1, 1) < _get_date_int(1000, 1, 1)

    def test_date_to_int_various_dates(self):
        dates = [
            date(1900, 1, 1),
            date(2024, 4, 7),
            date(1999, 12, 31),
            date(2000, 2, 29),  # leap day
        ]
        for d in dates:
            assert date_to_int(d) == _get_date_int(d.year, d.month, d.day)

    def test_date_to_int_none(self):
        assert date_to_int(None) == SQREAM_OLDEST_DATE_LONG

    def test_date_to_int_known(self):
        assert date_to_int(date(1900, 1, 1)) == SQREAM_OLDEST_DATE_LONG
        assert date_to_int(date(2024, 4, 1)) == _get_date_int(2024, 4, 1)

    def test_datetime_to_long_none(self):
        assert datetime_to_long(None) == SQREAM_OLDEST_DATETIME_LONG

    def test_datetime_to_long_midnight(self):
        dt = datetime(2024, 4, 7, 0, 0, 0, 0)
        expected = (_get_date_int(2024, 4, 7) << 32)
        assert datetime_to_long(dt) == expected

    def test_datetime_to_long_with_microseconds_rounding(self):
        dt = datetime(2024, 4, 7, 1, 2, 3, 789123)
        date_part = _get_date_int(2024, 4, 7)
        time_part = 1000 * (1 * 3600 + 2 * 60 + 3) + round(789123 / 1000)
        expected = (date_part << 32) + time_part
        assert datetime_to_long(dt) == expected

    def test_datetime_to_long_known(self):
        dt = datetime(1900, 1, 1, 0, 0, 0)
        assert datetime_to_long(dt) == SQREAM_OLDEST_DATETIME_LONG

        dt2 = datetime(2024, 4, 1, 12, 30, 15, 123000)
        result = datetime_to_long(dt2)
        date_part = _get_date_int(2024, 4, 1)
        time_part = 1000 * (12 * 3600 + 30 * 60 + 15) + 123
        expected = (date_part << 32) + time_part
        assert result == expected

    def test_sq_numeric_to_decimal_non_null(self):
        # Simulate a little endian 128-bit integer: 1
        raw = (1).to_bytes(16, 'little', signed=False)
        dec = sq_numeric_to_decimal(raw, scale=0)
        assert dec == Decimal(1)

    def test_sq_numeric_to_decimal_with_scale(self):
        raw = (123456).to_bytes(16, 'little', signed=False)
        dec = sq_numeric_to_decimal(raw, scale=2)
        assert dec == Decimal('1234.56')

    def test_sq_numeric_to_decimal_null(self):
        assert sq_numeric_to_decimal(b"", scale=2, is_null=True) is None

    def test_sq_numeric_to_decimal_zero(self):
        raw = (0).to_bytes(16, 'little', signed=False)
        assert sq_numeric_to_decimal(raw, 0) == Decimal(0)

    def test_sq_numeric_to_decimal_negative(self):
        negative_bigint = (-123456789).to_bytes(16, 'little', signed=True)
        result = sq_numeric_to_decimal(negative_bigint, 2)
        assert result == Decimal("-1234567.89")

    def test_sq_numeric_to_decimal_large_value(self):
        val = 10**30
        raw = val.to_bytes(16, 'little', signed=False)
        assert sq_numeric_to_decimal(raw, 0) == Decimal(val)

    def test_sq_numeric_to_decimal_signed_interpretation(self):
        val = -10**9
        raw = val.to_bytes(16, 'little', signed=True)
        dec = sq_numeric_to_decimal(raw, 0)
        assert dec == Decimal(val)

    def test_decimal_to_sq_numeric_zero_scale(self):
        assert decimal_to_sq_numeric(Decimal("12345"), 0) == 12345

    def test_decimal_to_sq_numeric_positive(self):
        dec = Decimal("123.45")
        result = decimal_to_sq_numeric(dec, 2)
        assert result == 12345

    def test_decimal_to_sq_numeric_negative(self):
        dec = Decimal("-123.45")
        result = decimal_to_sq_numeric(dec, 2)
        assert result == -12345

    def test_decimal_to_sq_numeric_rounding(self):
        assert decimal_to_sq_numeric(Decimal("1.001"), 2) == 101
        assert decimal_to_sq_numeric(Decimal("-1.001"), 2) == -101

    def test_decimal_to_sq_numeric_large(self):
        val = Decimal("999999999999999.999")
        res = decimal_to_sq_numeric(val, 3)
        assert res == 999999999999999999

    def test_decimal_to_sq_numeric_high_precision(self):
        dec = Decimal("3.141592653589793238462643383279")
        assert decimal_to_sq_numeric(dec, 20) == int(ceil(dec * Decimal(10**20)))

    def test_lengths_to_pairs_basic(self):
        lengths = [3, 5, 2]
        result = list(lengths_to_pairs(lengths))
        assert result == [(0, 3), (3, 8), (8, 10)]

    def test_lengths_to_pairs_single_value(self):
        assert list(lengths_to_pairs([10])) == [(0, 10)]

    def test_lengths_to_pairs_multiple_values(self):
        lengths = [2, 4, 6]
        expected = [(0, 2), (2, 6), (6, 12)]
        assert list(lengths_to_pairs(lengths)) == expected

    def test_lengths_to_pairs_zero_length(self):
        assert list(lengths_to_pairs([0, 0, 0])) == [(0, 0), (0, 0), (0, 0)]

    def test_lengths_to_pairs_empty(self):
        assert list(lengths_to_pairs([])) == []

    def test_arr_lengths_to_pairs_basic(self):
        lengths = [3, 5]
        result = list(arr_lengths_to_pairs(lengths))
        assert result == [(0, 3), (8, 5)]

    def test_arr_lengths_to_pairs_padding(self):
        lengths = [7, 8]  # Padding for 7 is 1, for 8 is 0
        result = list(arr_lengths_to_pairs(lengths))
        assert result == [(0, 7), (8, 8)]

    def test_arr_lengths_to_pairs_no_padding(self):
        lengths = [8, 16]
        assert list(arr_lengths_to_pairs(lengths)) == [(0, 8), (8, 16)]

    def test_arr_lengths_to_pairs_with_padding(self):
        lengths = [7, 5]  # paddings: 1 and 3
        result = list(arr_lengths_to_pairs(lengths))
        assert result == [(0, 7), (8, 5)]

    def test_arr_lengths_to_pairs_alignment_boundary(self):
        lengths = [0, 8, 1]
        result = list(arr_lengths_to_pairs(lengths))
        assert result == [(0, 0), (0, 8), (8, 1)]

    def test_zero_date(self):
        with pytest.raises(Exception, match="year 0 is out of range"):
            sq_date_to_py_date(0, is_null=False)

    def test_zero_datetime(self):
        with pytest.raises(Exception, match="year 0 is out of range"):
            sq_datetime_to_py_datetime(0, is_null=False)

    def test_negative_date(self):
        with pytest.raises(Exception, match="year -9 is out of range"):
            sq_date_to_py_date(-3000, is_null=False)

    def test_negative_datetime(self):
        with pytest.raises(Exception, match="year 0 is out of range"):
            sq_datetime_to_py_datetime(-3000, is_null=False)

    def test_null_date(self):
        res = sq_date_to_py_date(-3000, is_null=True)
        assert res is None, f"Excepted to get None, but got [{res}]"

    def test_null_datetime(self):
        res = sq_datetime_to_py_datetime(-3000, is_null=True)
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

        dt_as_long = datetime_to_long(input_datetime)
        long_as_dt = sq_datetime_to_py_datetime(dt_as_long)

        assert long_as_dt == expected_result

    def test_pandas_timestamp_to_sq_datetime2(self):
        # Test regular datetime conversion
        dt = pd.Timestamp("1997-12-31 23:59:59.123456789")
        utc_offset, nanos, time_int, date_int = pandas_timestamp_to_sq_datetime2(dt)

        assert utc_offset == 0
        assert nanos == 456789  # Only sub-millisecond part
        assert time_int == 86399123  # 23:59:59.123
        assert date_int == 729694  # 1997-12-31

        # Test None input
        result = pandas_timestamp_to_sq_datetime2(None)
        assert result == SQREAM_OLDEST_DATETIME2

        # Test midnight
        dt = pd.Timestamp("2000-01-01 00:00:00")
        utc_offset, nanos, time_int, date_int = pandas_timestamp_to_sq_datetime2(dt)
        assert time_int == 0
        assert nanos == 0

    def test_sq_datetime2_to_pandas_timestamp(self):
        """Test that converts bytes coming from SQream to pandas timestamp and back to bytes"""
        example_bytes = b'\x00\x00\x00\x00U\xf8\x06\x00\x93X&\x05^"\x0b\x00'
        result = sq_datetime2_to_pandas_timestamp(example_bytes, False)

        components = pandas_timestamp_to_sq_datetime2(result)
        datetime2_bytes = struct.pack('<iiii', *components)
        assert datetime2_bytes == example_bytes

        # Test null case
        assert sq_datetime2_to_pandas_timestamp(example_bytes, True) is None

    def test_roundtrip_conversion(self):
        """Test that converting to SQream format and back gives the same datetime"""
        original_dt = pd.Timestamp("1997-12-31 23:59:59.123456789")

        components = pandas_timestamp_to_sq_datetime2(original_dt)
        datetime2_bytes = struct.pack('<iiii', *components)

        result_dt = sq_datetime2_to_pandas_timestamp(datetime2_bytes, False)

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

        components = pandas_timestamp_to_sq_datetime2(dt)
        datetime2_bytes = struct.pack('<iiii', *components)
        result_dt = sq_datetime2_to_pandas_timestamp(datetime2_bytes, False)

        assert str(result_dt) == str(dt)
