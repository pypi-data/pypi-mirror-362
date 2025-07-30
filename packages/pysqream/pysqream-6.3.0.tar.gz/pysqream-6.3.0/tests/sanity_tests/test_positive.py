import sys
import pandas as pd
import pytz
import pytest
from datetime import datetime, date, timezone
from decimal import Decimal, getcontext
from numpy.random import randint, uniform
from queue import Queue
from time import sleep
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
             'numeric({},{})'.format(precision, scale), 'text', 'int[]']

pos_test_vals = {'bool': (0, 1, True, False, 2, 3.6, 'test', (1997, 5, 9), (1997, 12, 12, 10, 10, 10)),
                 'tinyint': (randint(0, 255), randint(0, 255), 0, 255, True, False),
                 'smallint': (randint(-32768, 32767), 0, -32768, 32767, True, False),
                 'int': (randint(-2147483648, 2147483647), 0, -2147483648, 2147483647, True, False),
                 'int_arr': [[1, 0]],
                 'bigint': (randint(1-max_bigint, max_bigint), 0, 1-max_bigint, max_bigint, True, False),
                 'real': (float('inf'), float('-inf'), float('+0'), float('-0'), round(uniform(1e-6, 1e6), 5), 837326.52428, True, False),   # float('nan')
                 'double': (float('inf'), float('-inf'), float('+0'), float('-0'), uniform(1e-6, 1e6), True, False),  # float('nan')
                 'date': (date(1998, 9, 24), date(2020, 12, 1), date(1997, 5, 9), date(1993, 7, 13)),
                 'datetime': (datetime(1001, 1, 1, 10, 10, 10), datetime(1997, 11, 30, 10, 10, 10), datetime(1987, 7, 27, 20, 15, 45), datetime(1993, 12, 20, 17, 25, 46)),
                 'datetime2': (pd.Timestamp('1001-01-01 10:10:10+00:00'),
                               pd.Timestamp('1997-11-30 10:10:10+01:00'),
                               pd.Timestamp('1987-07-27 20:15:45+02:30'),
                               pd.Timestamp('1993-12-20 17:25:46-05:00')),
                 'varchar': (generate_varchar(varchar_length), generate_varchar(varchar_length), generate_varchar(varchar_length), 'b   '),
                 'nvarchar': ('א', 'א  ', '', 'ab א'),
                 'text': ('א', 'א  ', '', 'ab א'),
                 'numeric': (Decimal("0"), Decimal("1"), Decimal("1.1"), Decimal("-1"), Decimal("-1.0"),
                             Decimal("12345678901234567890.0123456789"))}


class TestPositive(TestBase):

    @pytest.mark.parametrize("col_type", col_types)
    def test_positive(self, col_type):
        cur = self.con.cursor()
        trimmed_col_type = col_type.split('(')[0].replace('[]', '_arr')
        logger.info(f"Inserting values for {col_type}")

        cur.execute(f"create or replace table test (t_{trimmed_col_type} {col_type})")

        for val in pos_test_vals[trimmed_col_type]:
            cur.execute("truncate table test")
            cur.executemany("insert into test values (?)", [(val,)])
            res = cur.execute("select * from test").fetchall()[0][0]

            assert (
                    val == res or
                    (val != res and trimmed_col_type == 'bool' and val != 0 and res is True) or
                    (val != res and trimmed_col_type == 'varchar' and val != 0 and val.strip() == res) or
                    (val != res and trimmed_col_type == 'real' and val != 0 and abs(res - val) <= 0.1)
            )

        cur.close()

    @pytest.mark.parametrize("col_type", col_types)
    def test_positive_nulls(self, col_type):
        cur = self.con.cursor()
        trimmed_col_type = col_type.split('(')[0].replace('[]', '_arr')
        logger.info(f"Positive tests - Null test for column type: {col_type}")
        cur.execute(f"create or replace table test (t_{trimmed_col_type} {col_type})")
        cur.executemany("insert into test values (?)", [(None,)])
        res = cur.execute("select * from test").fetchall()[0][0]

        assert res is None, f"Error setting null on column type: {trimmed_col_type}. Got: {res}, {type(res)}"

    def test_single_column_multiple_rows_with_nulls(self):
        cur = self.con.cursor()
        cur.execute("create or replace table test (xint int)")
        cur.executemany('insert into test values (?)', [(5,), (None,), (6,), (7,), (None,), (8,), (None,)])
        cur.executemany("select case when xint is null then 1 else 0 end from test")
        expected_list = [0, 1, 0, 0, 1, 0, 1]
        res_list = []
        res_list += [x[0] for x in cur.fetchall()]

        assert expected_list == res_list, "expected to get {}, instead got {}".format(expected_list, res_list)

    def test_multiple_columns_multiple_rows_with_nulls(self):
        cur = self.con.cursor()

        rows_num = 3
        cols_num = len(col_types)
        columns = []
        test_values = []
        column_names = []

        for i in range(cols_num):
            col_type = col_types[i % len(col_types)]
            col_name = f'col_{i+1}'

            columns.append(f'{col_name} {col_type}')
            column_names.append(col_name)
            test_type = col_type.split('(')[0].replace('[]', '_arr')
            test_values.append(pos_test_vals[test_type][0])

        create_sql = f"create or replace table test (\n    " + ",\n    ".join(columns) + "\n)"
        cur.execute(create_sql)

        test_data = []

        for row in range(rows_num):
            if row % 2 == 0:  # Alternate between values and nulls
                row_values = []
                for i in range(cols_num):
                    test_type = col_types[i % len(col_types)].split('(')[0].replace('[]', '_arr')
                    # Use different values from pos_test_vals based on row number
                    val_index = row % len(pos_test_vals[test_type])
                    row_values.append(pos_test_vals[test_type][val_index])
                test_data.append(tuple(row_values))
            else:
                test_data.append(tuple([None] * cols_num))

        placeholders = ','.join(['?'] * cols_num)
        cur.executemany(f'insert into test values ({placeholders})', test_data)

        for col in column_names:
            cur.execute(f"select case when {col} is null then null else 0 end from test")
            res_list = [x[0] for x in cur.fetchall()]
            expected_list = [None if row % 2 else 0 for row in range(rows_num)]

            assert expected_list == res_list, f"Column {col}: expected {expected_list}, got {res_list}"

    def test_select_literal_bool_1(self):
        cur = self.con.cursor()
        cur.execute("select false")
        res = cur.fetchall()[0][0]

        assert res == 0, "Expected to get result 0, instead got {}".format(res)

    def test_select_literal_bool_2(self):
        cur = self.con.cursor()
        cur.execute("select true")
        res = cur.fetchall()[0][0]

        assert res == 1, "Expected to get result 1, instead got {}".format(res)

    def test_select_when_there_is_an_open_statement(self):
        cur = self.con.cursor()
        cur.execute("select 1")
        sleep(5)
        res = cur.execute("select 1").fetchall()[0][0]

        assert res == 1, f"expected to get result 1, instead got {res}"

    def test_datetime(self):
        cur = self.con.cursor()
        logger.info("Datetime tests - insert different timezones datetime")
        t1 = datetime.strptime(datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M"), '%Y-%m-%d %H:%M')
        t2 = datetime.strptime(datetime.now(pytz.timezone('Asia/Tokyo')).strftime("%Y-%m-%d %H:%M"), '%Y-%m-%d %H:%M')
        cur.execute("create or replace table test (xdatetime datetime)")
        cur.executemany('insert into test values (?)', [(t1,), (t2,)])
        cur.execute("select * from test")
        res = cur.fetchall()

        assert res[0][0] != res[1][0], f"expected to get different datetimes. res1: {res[0][0]}, res2: {res[1][0]}"

        logger.info("Datetime tests - insert datetime with microseconds")
        t1 = datetime(1997, 5, 9, 4, 30, 10, 123456)
        t2 = datetime(1997, 5, 9, 4, 30, 10, 987654)
        cur.execute("create or replace table test (xdatetime datetime)")
        cur.executemany('insert into test values (?)', [(t1,), (t2,)])

        cur.close()

    def test_datetime2(self):
        cur = self.con.cursor()
        cur.execute(f"create or replace table t (t_datetime2 datetime2)")
        cur.executemany("insert into t values ('1997-12-31 23:59:59.123456789')")
        rows = [(pd.Timestamp('1997-12-31 23:59:59.123456789'), ), (pd.Timestamp('1970-01-17 18:56:04.205'), )]
        cur.executemany("insert into t values (?)", rows)
        cur.execute("select * from t")
        res = cur.fetchall()
        expected_result = [(pd.Timestamp('1997-12-31 23:59:59.123456789+00:00'),),
                           (pd.Timestamp('1997-12-31 23:59:59.123456789+00:00'),),
                           (pd.Timestamp('1970-01-17 18:56:04.205000000+00:00'),)]
        cur.close()

        assert res == expected_result, f"Expected results: {expected_result}, actual result: {res}"

    def test_datetime2_array(self):
        cur = self.con.cursor()
        cur.execute(f"create or replace table t_arr (t_arr datetime2[])")
        data = pd.Timestamp('1997-12-31 23:59:59.123456789')
        data2 = pd.Timestamp('1997-12-31 23:59:59.123456789')
        cur.executemany("insert into t_arr values (?)", [([data, data2, None], )])
        cur.execute("select * from t_arr")
        res = cur.fetchall()
        expected_result = [([pd.Timestamp('1997-12-31 23:59:59.123456789+00:00'), pd.Timestamp('1997-12-31 23:59:59.123456789+00:00'), None],)]
        cur.close()

        assert res == expected_result, f"Expected results: {expected_result}, actual result: {res}"

    def test_insert_return_utf8(self):
        cur = self.con.cursor()
        cur.execute("create or replace table test (xvarchar varchar(20))")
        cur.executemany('insert into test values (?)', [(u"hello world",), ("hello world",)])
        cur.execute("select * from test")
        res = cur.fetchall()
        cur.close()

        assert res[0][0] == res[1][0]

    def test_strings_with_escaped_chars(self):
        cur = self.con.cursor()
        cur.execute("create or replace table test (xvarchar varchar(20))")
        values = [("\t",), ("\n",), ("\\n",), ("\\\n",), (" \\",), ("\\\\",), (" \nt",), ("'abd''ef'",), ("abd""ef",),
                  ("abd\"ef",)]
        cur.executemany('insert into test values (?)', values)
        cur.executemany("select * from test")
        expected_list = ['', '', '\\n', '\\', ' \\', '\\\\', ' \nt', "'abd''ef'", 'abdef', 'abd"ef']
        res_list = []
        res_list += [x[0] for x in cur.fetchall()]
        cur.close()

        assert expected_list == res_list

    def test_stop_statement(self):
        cur = self.con.cursor()
        cur2 = self.con.cursor()

        cur.execute("create or replace table t (x text, y text)")
        cur.execute("insert into t values ('a','a'), ('b','b'), ('c','c'), ('d','d'), ('e','e'), ('f','f'), ('g','g'),('h','h'),('i','i'),"
                    "('zz','zz'),('zz','zz'),('zz','zz'),('zz','zz'),('zz','zz'),('zz','zz'),('zz','zz'),('zz','zz'),('zz','zz'),('zz','zz'),"
                    "('zz','zz'),('zz','zz'),('zz','zz'),('zz','zz'),('zz','zz'),('zz','zz'),('zz','zz'),('zz','zz'),('zz','zz'),('zz','zz'),"
                    "('zz','zz'),('zz','zz'),('zz','zz'),('zz','zz'),('zz','zz'),('zz','zz'),('zz','zz'),('zz','zz'),('zz','zz'),('zz','zz'),"
                    "('zz','zz'),('zz','zz'),('zz','zz')")

        for _ in range(10):
            cur.execute("insert into t select * from t")

        long_execution_query = """select t2.x,t3.y from t inner join (select * from t) t2 on t.x > t2.x 
        inner join (select * from t) t3 on t2.x > t3.x 
        inner join (select * from t) t4 on t3.y < t4.x"""

        cur.execute(long_execution_query)
        cur2.execute("select show_server_status()")
        show_server_status_result = cur2.fetchall()
        assert len(show_server_status_result) == 2

        stmt_id = show_server_status_result[0][8]
        cur2.execute(f"select stop_statement({stmt_id})")
        cur2.execute("select show_server_status()")
        show_server_status_result = cur2.fetchall()
        assert len(show_server_status_result) == 1

        with pytest.raises(Exception) as e:
            cur.fetchall()  # should fail, pysqream should close the statement

        assert '"error":"Stopping Statement' in str(e.value)
        # no need to close the cursors, we call connection.close in test_setup_teardown which closes all sub connections and cursors.
