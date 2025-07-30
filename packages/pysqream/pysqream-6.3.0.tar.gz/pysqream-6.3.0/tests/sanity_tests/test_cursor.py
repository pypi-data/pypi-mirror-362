import pysqream
from time import sleep
from tests.test_base import TestBaseWithoutBeforeAfter, connect_dbapi


class TestCursor(TestBaseWithoutBeforeAfter):

    def test_cursor_through_clustered(self):
        con_clustered = pysqream.connect(self.ip, self.picker_port, self.database, self.username, self.password, clustered=True, log=True)
        cur = con_clustered.cursor()
        assert cur.execute("select 1").fetchall()[0][0] == 1
        cur.close()

    def test_two_statements_same_cursor(self):
        vals = [1]
        con = connect_dbapi(self.ip)
        cur = con.cursor()
        cur.execute("select 1")
        res1 = cur.fetchall()[0][0]
        vals.append(res1)
        cur.execute("select 1")
        res2 = cur.fetchall()[0][0]
        vals.append(res2)
        cur.close()
        con.close()
        assert all(x == vals[0] for x in vals)

    def test_cursor_when_open_statement(self):
        con = connect_dbapi(self.ip)
        cur = con.cursor()
        cur.execute("select 1")
        sleep(5)
        cur.execute("select 1")
        res = cur.fetchall()[0][0]
        cur.close()
        con.close()
        assert res == 1

    def test_fetch_after_all_read(self):
        con = connect_dbapi(self.ip)
        cur = con.cursor()
        cur.execute("create or replace table test (xint int)")
        cur.executemany('insert into test values (?)', [(1,)])
        cur.execute("select * from test")
        x = cur.fetchone()[0]
        res = cur.fetchone()
        assert res is None

        res = cur.fetchall()
        assert res == []

        res = cur.fetchmany(1)
        assert res == []
        cur.close()
        con.close()
