import threading
from queue import Queue
from tests.test_base import TestBaseWithoutBeforeAfter, connect_dbapi, Logger

logger = Logger()
q = Queue()


class TestThreads(TestBaseWithoutBeforeAfter):
    def connect_and_execute(self, num, con):
        cur = con.cursor()
        cur.execute("select {}".format(num))
        res = cur.fetchall()
        q.put(res)
        cur.close()

    def test_threads(self):
        con = connect_dbapi(self.ip, clustered=self.clustered, use_ssl=self.use_ssl, port=self.port,
                            picker_port=self.picker_port, database=self.database,
                            username=self.username, password=self.password)

        logger.info("Thread tests - concurrent inserts with multiple threads through cursor")
        t1 = threading.Thread(target=self.connect_and_execute, args=(3, con,))
        t2 = threading.Thread(target=self.connect_and_execute, args=(3, con,))
        t1.start()
        t2.start()
        t1.join()
        t2.join()
        res1 = q.get()[0][0]
        res2 = q.get()[0][0]
        con.close()

        assert res1 == res2, f"expected to get equal values. instead got res1: {res1} and res2: {res2}"
