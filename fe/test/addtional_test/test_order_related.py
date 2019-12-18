import unittest

from be.model.store import Store


class MyTestCase(unittest.TestCase):
    def test_user_cancel_order(self):
        Store.init_tables()
        order_id,buyer_id=1,1
        MyTestCase.tool.add_order(buyer_id,order_id)

        self.assertEqual(True, False)

    def test_history_order(self):
        """测试用户查询已完成订单"""

    class tool:


if __name__ == '__main__':
    unittest.main()
