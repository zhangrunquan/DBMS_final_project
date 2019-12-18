import unittest

from be.model.constants import Constants as C
from be.model.store import Store
from be.model.user import User
from fe.test.addtional_test.test_tool import TestTool


class MyTestCase(unittest.TestCase):


    def test_user_cancel_order(self):
        Store.init_tables()
        order_id, buyer_id = 1, 1
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

    def test_history_order(self):
        """测试用户查询已完成订单"""
        Store.init_tables()
        conn=Store.get_db_conn()
        user_id,order_id=1,1
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
        self.assertEqual(len(body),1)


if __name__ == '__main__':
    unittest.main()
