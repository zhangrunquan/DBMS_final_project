import unittest
from be.model.db_conn import DBConn
from be.model.store import Store


class MyTestCase(unittest.TestCase):
    def test_db_initialization(self):
        Store.init_tables()



if __name__ == '__main__':
    unittest.main()
