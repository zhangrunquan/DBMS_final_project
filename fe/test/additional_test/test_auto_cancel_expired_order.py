import unittest
import _thread
import time
from threading import Thread

from be.model.order_manager import ExpiredOrderCanceler
from be.model.store import Store


class TestCase(unittest.TestCase):
    def test_something(self):
        """测试自动取消超时订单"""
        Store.init_tables()
        conn=Store.get_db_conn()
        cursor=conn.cursor()
        sql='insert into pending_order(order_id,create_ts) values(1,timestamp \'2010-10-10\' );'
        cursor.execute(sql)
        conn.commit()
        interval=5
        # 启动自动清理线程
        t=Thread(target=ExpiredOrderCanceler.work,args=(15,interval),daemon=True)
        t.start()
        time.sleep(5)
        # 测试pending order表为空
        sql='select * from pending_order;'
        cursor.execute(sql)
        self.assertEqual(cursor.rowcount, 0)

    def test_foo(self):
        conn=Store.get_db_conn()


if __name__ == '__main__':
    unittest.main()
