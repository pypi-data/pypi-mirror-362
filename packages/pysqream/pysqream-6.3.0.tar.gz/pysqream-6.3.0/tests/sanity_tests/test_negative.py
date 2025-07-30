import sys
import pytest
from queue import Queue
from decimal import getcontext
from numpy.random import randint
from tests.test_base import TestBase, Logger

q = Queue()
varchar_length = 10
nvarchar_length = 10
precision = 38
scale = 10
max_bigint = sys.maxsize if sys.platform not in ('win32', 'cygwin') else 2147483647
logger = Logger()
getcontext().prec = 38


def generate_varchar(length):
    return ''.join(chr(num) for num in randint(32, 128, length))


col_types = ['bool', 'tinyint', 'smallint', 'int', 'bigint', 'real', 'double', 'date', 'datetime',
             'datetime2', 'varchar({})'.format(varchar_length), 'nvarchar({})'.format(varchar_length),
             'numeric({},{})'.format(precision, scale), 'text']

neg_test_vals = {'tinyint': (258, 3.6, 'test',  (1997, 5, 9), (1997, 12, 12, 10, 10, 10)),
                 'smallint': (40000, 3.6, 'test', (1997, 5, 9), (1997, 12, 12, 10, 10, 10)),
                 'int': (9999999999, 3.6, 'test',  (1997, 5, 9), (1997, 12, 12, 10, 10, 10)),
                 'bigint': (92233720368547758070, 3.6, 'test', (1997, 12, 12, 10, 10, 10)),
                 'real': ('test', (1997, 12, 12, 10, 10, 10)),
                 'double': ('test', (1997, 12, 12, 10, 10, 10)),
                 'date': (5, 3.6, (-8, 9, 1), (2012, 15, 6), (2012, 9, 45), 'test', False, True),
                 'datetime': (5, 3.6, (-8, 9, 1, 0, 0, 0), (2012, 15, 6, 0, 0, 0), (2012, 9, 45, 0, 0, 0), (2012, 9, 14, 26, 0, 0), (2012, 9, 14, 13, 89, 0), 'test', False, True),
                 'datetime2': (5, 3.6, ('a', 9, 1, 0), (2012, 15, 6, 0, 0, 0), (2012, 9, 45, 0, 0, 0), 'test', False, True),
                 'varchar': (5, 3.6, (1, 2), (1997, 12, 12, 10, 10, 10), False, True),
                 'nvarchar': (5, 3.6, (1, 2), (1997, 12, 12, 10, 10, 10), False, True),
                 'text': (5, 3.6, (1, 2), (1997, 12, 12, 10, 10, 10), False, True),
                 'numeric': ('a', )}


class TestNegative(TestBase):

    @pytest.mark.parametrize("col_type", col_types)
    def test_negative(self, col_type):
        """Negative Set/Get tests"""

        cur = self.con.cursor()
        logger.info("Negative tests")

        if col_type == 'bool':
            pytest.skip("Skipping boolean negative test")

        trimmed_col_type = col_type.split('(')[0]
        cur.execute("create or replace table test (t_{} {})".format(trimmed_col_type, col_type))
        for val in neg_test_vals[trimmed_col_type]:
            rows = [(val,)]
            with pytest.raises(Exception) as e:
                cur.executemany("insert into test values (?)", rows)
            assert "Error packing columns. Check that all types match the respective column types" in str(e.value)

    def test_inconsistent_sizes(self):
        cur = self.con.cursor()
        logger.info("Inconsistent sizes test")
        cur.execute("create or replace table test (xint int, yint int)")

        with pytest.raises(Exception) as e:
            cur.executemany('insert into test values (?, ?)', [(5,), (6, 9), (7, 8)])

        assert "Inconsistent data sequences passed for inserting. Please use rows/columns of consistent length" in str(e.value)

    def test_varchar_conversion(self):
        cur = self.con.cursor()
        logger.info("Varchar - Conversion of a varchar to a smaller length")
        cur.execute("create or replace table test (test varchar(10))")

        with pytest.raises(Exception) as e:
            cur.executemany("insert into test values ('aa12345678910')")

        assert "expected response statementPrepared but got" in str(e.value)

    def test_nvarchar_conversion(self):
        cur = self.con.cursor()
        logger.info("Nvarchar - Conversion of a varchar to a smaller length")
        cur.execute("create or replace table test (test nvarchar(10))")

        with pytest.raises(Exception) as e:
            cur.executemany("insert into test values ('aa12345678910')")

        assert "expected response executed but got" in str(e.value)

    def test_incorrect_fetchmany(self):
        cur = self.con.cursor()
        logger.info("Incorrect usage of fetchmany - fetch without a statement")
        cur.execute("create or replace table test (xint int)")

        with pytest.raises(Exception) as e:
            cur.fetchmany(2)

        assert "No open statement while attempting fetch operation" in str(e.value)

    def test_incorrect_fetchall(self):
        cur = self.con.cursor()
        logger.info("Incorrect usage of fetchall")
        cur.execute("create or replace table test (xint int)")
        cur.executemany("select * from test")

        with pytest.raises(Exception) as e:
            cur.fetchall(5)

        assert "Bad argument to fetchall" in str(e.value)

    def test_incorrect_fetchone(self):
        cur = self.con.cursor()
        logger.info("Incorrect usage of fetchone")
        cur.execute("create or replace table test (xint int)")
        cur.executemany("select * from test")

        with pytest.raises(Exception) as e:
            cur.fetchone(5)

        assert "Bad argument to fetchone" in str(e.value)

    def test_multi_statement(self):
        cur = self.con.cursor()
        logger.info("Multi statements test")

        with pytest.raises(Exception) as e:
            cur.execute("select 1; select 1;")

        assert "expected one statement, got" in str(e.value)

    def test_execute_closed_cursor(self):
        cur = self.con.cursor()
        logger.info("running execute on a closed cursor")
        cur.close()

        with pytest.raises(Exception) as e:
            cur.execute("select 1")

        assert "Cursor has been closed" in str(e.value)
