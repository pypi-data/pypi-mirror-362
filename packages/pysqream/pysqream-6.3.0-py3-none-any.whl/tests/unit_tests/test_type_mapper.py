import pytest
import numbers
import numpy as np
import pandas as pd
from decimal import Decimal
from datetime import date, datetime
from pysqream.type_mapper import TypeMapper
from tests.test_base import TestBaseWithoutBeforeAfter


@pytest.fixture
def type_mapper():
    """Fixture for a clean instance of type_mapper"""
    return TypeMapper()


class TestColumnBufferUnitTests(TestBaseWithoutBeforeAfter):

    @pytest.mark.parametrize("sqream_type, expected_pack_code", [
        ("ftBool", "?"),
        ("ftUByte", "B"),
        ("ftShort", "h"),
        ("ftInt", "i"),
        ("ftLong", "q"),
        ("ftDouble", "d"),
        ("ftFloat", "f"),
        ("ftNumeric", "4i"),
        ("ftDate", "i"),
        ("ftDateTime", "q"),
        ("ftTimestampTz", "4i"),
        ("ftVarchar", "s"),
        ("ftBlob", "s"),
        ("ftArray", None),
    ])
    def test_get_pack_code(self, type_mapper, sqream_type, expected_pack_code):
        assert type_mapper.get_pack_code(sqream_type) == expected_pack_code

    @pytest.mark.parametrize("sqream_type, expected_typecode", [
        ("ftBool", "NUMBER"),
        ("ftUByte", "NUMBER"),
        ("ftShort", "NUMBER"),
        ("ftInt", "NUMBER"),
        ("ftLong", "NUMBER"),
        ("ftDouble", "NUMBER"),
        ("ftFloat", "NUMBER"),
        ("ftNumeric", "NUMBER"),
        ("ftDate", "DATETIME"),
        ("ftDateTime", "DATETIME"),
        ("ftTimestampTz", "DATETIME"),
        ("ftVarchar", "STRING"),
        ("ftBlob", "STRING"),
        ("ftArray", "ARRAY"),
    ])
    def test_get_typecode(self, type_mapper, sqream_type, expected_typecode):
        assert type_mapper.get_typecode(sqream_type) == expected_typecode

    @pytest.mark.parametrize("sqream_type, expected_python_types", [
        ("ftBool", (bool, np.bool_)),
        ("ftUByte", numbers.Integral),
        ("ftShort", numbers.Integral),
        ("ftInt", numbers.Integral),
        ("ftLong", numbers.Integral),
        ("ftDouble", numbers.Real),
        ("ftFloat", numbers.Real),
        ("ftNumeric", (Decimal, numbers.Real)),
        ("ftDate", date),
        ("ftDateTime", datetime),
        ("ftTimestampTz", pd.Timestamp),
        ("ftVarchar", str),
        ("ftBlob", str),
        ("ftArray", list),
    ])
    def test_get_python_types(self, type_mapper, sqream_type, expected_python_types):
        assert type_mapper.get_python_types(sqream_type) == expected_python_types

    @pytest.mark.parametrize("sqream_type, size, expected_default", [
        ("ftBool", 0, False),
        ("ftUByte", 0, 0),
        ("ftShort", 0, 0),
        ("ftInt", 0, 0),
        ("ftLong", 0, 0),
        ("ftDouble", 0, 0.0),
        ("ftFloat", 0, 0.0),
        ("ftNumeric", 0, Decimal("0")),
        ("ftDate", 0, None),
        ("ftDateTime", 0, None),
        ("ftTimestampTz", 0, None),
        ("ftVarchar", 5, "     "),
        ("ftBlob", 0, ""),
        ("ftArray", 0, None),
    ])
    def test_get_default_value(self, type_mapper, sqream_type, size, expected_default):
        assert type_mapper.get_default_value(sqream_type, size) == expected_default
