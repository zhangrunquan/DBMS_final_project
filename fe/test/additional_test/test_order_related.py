import unittest

from be.model.constants import Constants as C
from be.model.store import Store
from be.model.user import User
from fe.test.additional_test.test_tool import TestTool


class TestCase(unittest.TestCase):


    def test_user_cancel_order(self):
        Store.init_tables()
        order_id, buyer_id = C.TEST_DEFAULT_ORDER_ID, C.TEST_DEFAULT_BUYER
        passw=C.TEST_DEFAULT_USER_PASSWORD
        wrong_passw=1
        conn=Store.get_db_conn()
        # user不存在
        TestTool.add_order(conn,buyer_id, order_id)
        u=User()
        code,_=u.cancel_order(buyer_id,passw,order_id)
        self.assertNotEqual(code,200)
        # 密码错误
        TestTool.add_user(conn, buyer_id)
        code,_=u.cancel_order(buyer_id,wrong_passw,order_id)
        self.assertNotEqual(code,200)
        # 正常情况
        code,_=u.cancel_order(buyer_id,passw,order_id)
        self.assertEqual(code, 200)
        conn.close()

    def test_history_order(self):
        """测试用户查询已完成订单"""
        Store.init_tables()
        conn=Store.get_db_conn()
        user_id,order_id=C.TEST_DEFAULT_BUYER,C.TEST_DEFAULT_ORDER_ID
        token=TestTool.add_user_with_token(conn,user_id)
        TestTool.add_order(conn,user_id,order_id)
        dummy_token='1'
        # 伪造token
        u=User()
        code,_=u.history_order(user_id,dummy_token)
        self.assertNotEqual(code,200)
        # 正常情况
        code,body=u.history_order(user_id,token)
        self.assertEqual(code,200)
        conn.close()

    def test_seller_consign(self):
        """测试商家发货"""
        Store.init_tables()
        order_id, buyer_id = C.TEST_DEFAULT_ORDER_ID, C.TEST_DEFAULT_BUYER
        seller_id=C.TEST_DEFAULT_SELLER
        passw = C.TEST_DEFAULT_USER_PASSWORD
        wrong_passw = 1
        conn = Store.get_db_conn()
        # user不存在
        TestTool.add_order(conn, buyer_id, order_id,seller_id)
        u = User()
        code, _ = u.consign(seller_id,passw,order_id)
        self.assertNotEqual(code, 200)
        # 密码错误
        TestTool.add_user(conn, seller_id)
        code, _ = u.consign(seller_id,wrong_passw,order_id)
        self.assertNotEqual(code, 200)
        # 正常情况
        code, _ = u.consign(seller_id, passw, order_id)
        self.assertEqual(code, 200)
        conn.close()

    def test_buyer_receive(self):
        """测试买家收货"""
        Store.init_tables()
        order_id, buyer_id = C.TEST_DEFAULT_ORDER_ID, C.TEST_DEFAULT_BUYER
        passw = C.TEST_DEFAULT_USER_PASSWORD
        wrong_passw = 1
        conn = Store.get_db_conn()
        # user不存在
        TestTool.add_order(conn, buyer_id, order_id)
        u = User()
        code, _ = u.receive(buyer_id,passw,order_id)
        self.assertNotEqual(code, 200)
        # 密码错误
        TestTool.add_user(conn, buyer_id)
        code, _ = u.receive(buyer_id, wrong_passw, order_id)
        self.assertNotEqual(code, 200)
        # 正常情况
        code, _ = u.receive(buyer_id, passw, order_id)
        self.assertEqual(code, 200)
        conn.close()

if __name__ == '__main__':
    unittest.main()
