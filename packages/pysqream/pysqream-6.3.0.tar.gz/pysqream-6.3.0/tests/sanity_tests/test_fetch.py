from tests.test_base import TestBase


class TestFetch(TestBase):

    def test_fetch(self):
        cur = self.con.cursor()
        cur.execute("create or replace table test (xint int)")
        cur.executemany('insert into test values (?)', [(1,), (2,), (3,), (4,), (5,), (6,), (7,), (8,), (9,), (10,)])
        # fetchmany(1) vs fetchone()
        cur.execute("select * from test")
        res = cur.fetchmany(1)[0][0]
        cur.execute("select * from test")
        res2 = cur.fetchone()[0]
        cur.close()
        assert res == res2

        # fetchmany(-1) vs fetchall()
        cur = self.con.cursor()
        cur.execute("select * from test")
        res3 = cur.fetchmany(-1)
        cur.execute("select * from test")
        res4 = cur.fetchall()
        cur.close()
        assert res3 == res4

        # fetchone() loop
        cur = self.con.cursor()
        cur.execute("select * from test")
        for i in range(1, 11):
            x = cur.fetchone()[0]
            assert x == i
        cur.close()

    def test_combined_fetch(self):
        cur = self.con.cursor()
        cur.execute("create or replace table test (xint int)")
        cur.executemany('insert into test values (?)', [(1,), (2,), (3,), (4,), (5,), (6,), (7,), (8,), (9,), (10,)])
        cur.execute("select * from test")
        expected_list = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        res_list = []
        res_list.append(cur.fetchone()[0])
        res_list += [x[0] for x in cur.fetchmany(2)]
        res_list.append(cur.fetchone()[0])
        res_list += [x[0] for x in cur.fetchall()]
        cur.close()

        assert expected_list == res_list

    def test_fetch_after_data_read(self):
        cur = self.con.cursor()
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
