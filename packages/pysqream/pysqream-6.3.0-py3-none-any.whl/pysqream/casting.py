"""
Support functions for converting py values to sqream compatible values
and vice versa
"""

from __future__ import annotations

import pytz
import pandas as pd
from datetime import datetime, date
from decimal import Decimal, getcontext
from math import floor, ceil, pow
from typing import Union
from .globals import SQREAM_OLDEST_DATE_LONG, SQREAM_OLDEST_DATETIME_LONG, SQREAM_OLDEST_DATETIME2, TYPE_MAPPER
from struct import unpack


def pad_dates(num):
    return ('0' if num < 10 else '') + str(num)


def sq_date_to_py_date(sqream_date, is_null=False, date_convert_func=date):

    if is_null:
        return None

    year = (10000 * sqream_date + 14780) // 3652425
    intermed_1 = 365 * year + year // 4 - year // 100 + year // 400
    intermed_2 = sqream_date - intermed_1
    if intermed_2 < 0:
        year = year - 1
        intermed_2 = sqream_date - (365 * year + year // 4 - year // 100 +
                                    year // 400)
    intermed_3 = (100 * intermed_2 + 52) // 3060

    year = year + (intermed_3 + 2) // 12
    month = int((intermed_3 + 2) % 12) + 1
    day = int(intermed_2 - (intermed_3 * 306 + 5) // 10 + 1)

    return date_convert_func(year, month, day)


def sq_datetime_to_py_datetime(sqream_datetime, is_null=False, dt_convert_func=datetime):
    """
    Getting the datetime items involves breaking the long into the date int and time it holds
    The date is extracted in the above, while the time is extracted here
    """

    if is_null:
        return None

    date_part = sqream_datetime >> 32
    time_part = sqream_datetime & 0xffffffff
    date_part = sq_date_to_py_date(date_part, is_null=is_null)

    if date_part is None:
        return None

    msec = time_part % 1000
    sec = (time_part // 1000) % 60
    mins = (time_part // 1000 // 60) % 60
    hour = time_part // 1000 // 60 // 60
    return dt_convert_func(date_part.year, date_part.month, date_part.day,
                           hour, mins, sec, msec * int(pow(10, 3)))  # native python datetime has 6 digits precision (microseconds)
    # while sqream's datetime works with 3 digits precision (milliseconds)


def sq_datetime2_to_pandas_timestamp(datetime2_as_bytes: bytes, is_null: bool = False) -> [Decimal, None]:
    """
    Converts SQream's datetime2 (ftTimestampTz which has nanosecond precision) to pandas timestamp (native python datetime supports microseconds, not nanoseconds).
    SQream's datetime2 stores 4 integers (each is 32 bits/4 bytes):
      - 1. date (year, month, day)
      - 2. time (with milliseconds precision)
      - 3. nanoseconds
      - 4. TimeZone

    The strategy is to unpack the 4 integers and construct pandas timestamp object which supports nanoseconds precision and timezones
    """

    if is_null:
        return None

    utc_offset_seconds, nano_seconds, time_as_int, date_as_int = unpack(TYPE_MAPPER.get_pack_code("ftTimestampTz"), datetime2_as_bytes)

    date_part = sq_date_to_py_date(date_as_int, is_null)
    if date_part is None:
        return None

    hours, remainder = divmod(time_as_int, 3_600_000)  # 1 hour = 3,600,000 ms
    minutes, remainder = divmod(remainder, 60_000)     # 1 minute = 60,000 ms
    seconds, milliseconds = divmod(remainder, 1_000)   # 1 second = 1,000 ms

    microseconds = (milliseconds * 1_000) + (nano_seconds // 1_000)  # Convert nano to micro
    nanoseconds = nano_seconds % 1_000  # Remainder is actual nanoseconds

    utc_timestamp = pd.Timestamp(
        year=date_part.year,
        month=date_part.month,
        day=date_part.day,
        hour=hours,
        minute=minutes,
        second=seconds,
        microsecond=microseconds,
        nanosecond=nanoseconds,
        tz="UTC"
    )
    return utc_timestamp.tz_convert(pytz.FixedOffset(utc_offset_seconds // 60))


def sq_time_to_ns_since_midnight(time_as_int: int, nano_seconds: int):
    """
    Convert SQream integer time and nanoseconds to total nanoseconds since midnight
    """

    hours, remainder = divmod(time_as_int, 1000 * 60 * 60)
    minutes, remainder = divmod(remainder, 1000 * 60)
    seconds, milliseconds = divmod(remainder, 1000)

    return (
            hours * 3_600_000_000_000 +
            minutes * 60_000_000_000 +
            seconds * 1_000_000_000 +
            milliseconds * 1_000_000 +
            nano_seconds
    )


def pandas_timestamp_to_sq_datetime2(ts: Union[pd.Timestamp, None]) -> tuple[int, int, int, int]:
    """
    Converts pandas Timestamp to SQream's datetime2 representation as 4 integers.
    The output contains 4 integers (each 4 bytes):
    - UTC offset in seconds
    - Nanoseconds (only the sub-millisecond part)
    - Time as int (including milliseconds)
    - Date as int
    """

    if ts is None:
        return SQREAM_OLDEST_DATETIME2

    utc_offset_seconds = int(ts.utcoffset().total_seconds()) if ts.tzinfo else 0
    utc_ts = ts.tz_convert('UTC') if ts.tzinfo else ts.tz_localize('UTC')

    total_ns_since_midnight = (utc_ts.hour * 3_600_000_000_000 +
                               utc_ts.minute * 60_000_000_000 +
                               utc_ts.second * 1_000_000_000 +
                               utc_ts.microsecond * 1_000 +
                               utc_ts.nanosecond)

    time_as_int = total_ns_since_midnight // 1_000_000
    nano_seconds = total_ns_since_midnight % 1_000_000

    date_as_int = date_to_int(utc_ts.date())

    return utc_offset_seconds, nano_seconds, time_as_int, date_as_int


def _get_date_int(year: int, month: int, day: int) -> int:
    """
    Convert year, month and day to integer compatible with SQREAM
    """

    month: int = (month + 9) % 12
    year: int = year - month // 10
    return (
        365 * year + year // 4 - year // 100 + year // 400
        + (month * 306 + 5) // 10 + (day - 1)
    )


def date_to_int(dat: date) -> int:
    """
    Convert datetime.date to integer compatible with SQREAM interface
    """

    # datetime is also supported because it is descendant of date
    # date_to_int(date(1900, 1, 1)) is 693901 which is the oldest date that
    # sqream supports, so for None use the same
    return SQREAM_OLDEST_DATE_LONG if dat is None else _get_date_int(*dat.timetuple()[:3])


def datetime_to_long(dat: datetime) -> int:
    """
    Convert datetime.datetime to integer (LONG) compatible with SQREAM
    """

    if dat is None:
        # datetime_to_long(datetime(1900, 1, 1)) is 2980282101661696 which is
        # the oldest date that sqream supports, so for None use the same
        return SQREAM_OLDEST_DATETIME_LONG
    year, month, day, hour, minute, second = dat.timetuple()[:6]
    msec = dat.microsecond

    date_int: int = _get_date_int(year, month, day)
    time_int: int = 1000 * (hour * 3600 + minute * 60 + second) + round(msec / 1000)

    return (date_int << 32) + time_int


tenth = Decimal("0.1")
if getcontext().prec < 38:
    getcontext().prec = 38


def sq_numeric_to_decimal(bigint_as_bytes: bytes, scale: int, is_null=False) -> [Decimal, None]:
    if is_null:
        return None

    getcontext().prec = 38
    c = memoryview(bigint_as_bytes).cast('i')
    bigint = ((c[3] << 96) + ((c[2] & 0xffffffff) << 64) + ((c[1] & 0xffffffff) << 32) + (c[0] & 0xffffffff))

    return Decimal(bigint) * (tenth ** scale)


def decimal_to_sq_numeric(dec: Decimal, scale: int) -> int:  # returns bigint
    if getcontext().prec < 38:
        getcontext().prec = 38
    res = dec * (10 ** scale)
    return ceil(res) if res > 0 else floor(res)


def lengths_to_pairs(nvarc_lengths):
    """
    Accumulative sum generator, used for parsing nvarchar columns
    """

    idx = new_idx = 0
    for length in nvarc_lengths:
        new_idx += length
        yield idx, new_idx
        idx = new_idx


def arr_lengths_to_pairs(text_lengths):
    """
    Generator for parsing ARRAY TEXT columns' data
    """

    start = 0
    for length in text_lengths:
        yield start, length
        start = length + (8 - length % 8) % 8
