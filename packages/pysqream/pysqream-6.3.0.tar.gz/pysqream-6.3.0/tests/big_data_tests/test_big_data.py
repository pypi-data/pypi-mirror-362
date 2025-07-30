import pytest
import pandas as pd
from faker import Faker
from tests.test_base import TestBase, Logger
from numpy.random import randint, uniform, random, choice, default_rng

logger = Logger()


class TestBigData(TestBase):

    def load_ddl(self, ddl_file_path):
        logger.info("Load DDL")
        cur = self.con.cursor()
        with open(ddl_file_path, 'r') as file:
            ddl_string = file.read()
        cur.execute(ddl_string)
        cur.close()

    def generate_data(self):
        logger.info("Generate Data")
        fake = Faker()
        data = {
            "column1": randint(-2147483648, 2147483647, self.num_rows),
            "column2": default_rng().integers(low=-9223372036854775808, high=9223372036854775807, size=self.num_rows, dtype='int64'),
            "column3": randint(-32768, 32767, self.num_rows),
            "column4": [round(random(), 38) for _ in range(self.num_rows)],
            "column5": [round(random() * 10 ** 10, 10) for _ in range(self.num_rows)],
            "column6": [fake.date_time_this_decade() for _ in range(self.num_rows)],
            "column7": [fake.date_this_decade() for _ in range(self.num_rows)],
            "column8": [choice([True, False]) for _ in range(self.num_rows)],
            "column9": randint(0, 256, self.num_rows),
            "column10": uniform(-1e5, 1e5, self.num_rows),
            "column11": uniform(-3.4e38, 3.4e38, self.num_rows)
        }
        for i in range(12, 101):
            data[f"column{i}"] = [fake.text(max_nb_chars=100) for _ in range(self.num_rows)]
        df = pd.DataFrame(data)
        duplicated_df = df.loc[df.index.repeat(self.repeat)].reset_index(drop=True)
        return list(duplicated_df.itertuples(index=False, name=None))

    def start_execute_network_insert(self):
        logger.info("Start to execute network insert")
        num_values = ", ".join(["?" for i in range(100)])
        insert_query = f"insert into big_data values ({num_values})"
        cur = self.con.cursor()
        cur.executemany(insert_query, self.data)
        cur.close()

    def compare_results(self):
        logger.info("Compare results")
        cur = self.con.cursor()
        cur.execute("SELECT COUNT(*) FROM big_data")
        res = cur.fetchall()[0][0]

        assert res == self.expected_rows, f"Expected to get result {self.expected_rows}, instead got {res}"

    @pytest.mark.long
    def test_network_insert_big_data_sq_18040(self, big_data_ddl_path, request):
        if request.config.getoption("--skip-long"):
            pytest.skip("Skipping long-running test")
        self.repeat = 1500
        self.num_rows = 1000
        self.expected_rows = self.num_rows * self.repeat
        self.load_ddl(ddl_file_path=big_data_ddl_path)
        self.data = self.generate_data()
        self.start_execute_network_insert()
        self.compare_results()
