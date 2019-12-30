"""为测试提供工具函数"""
from be.model.constants import Constants as C
from be.model.user import jwt_encode


class TestTool:

    @staticmethod
    def add_order(conn, buyer_id, order_id,
                  seller_id=C.TEST_DEFAULT_SELLER
                  , price=C.TEST_DEFAULT_PRICE
                  , order_info=C.TEST_DEFAULT_ORDER_INFO
                  , status=C.PO_WAIT_PAYMENT
                  , create_ts='now()'
                  , store_id=C.TEST_DEFAULT_STORE_ID
                  ):
        sql = 'insert into pending_order(order_id,buyer_id,seller_id,price,order_info,status,create_ts,store_id) ' \
              'values (\'{0}\',\'{1}\',\'{2}\',{3},\'{4}\',{5},\'{6}\',\'{7}\');'.format(order_id, buyer_id, seller_id,
                                                                    price,order_info,status,create_ts,store_id)
        TestTool.execute_sql(conn, sql)

    @staticmethod
    def add_user(conn, user_id, password=C.TEST_DEFAULT_USER_PASSWORD):
        sql = 'insert into usr(user_id,password) values (\'{0}\',\'{1}\')' \
            .format(user_id, password)
        TestTool.execute_sql(conn, sql)

    @staticmethod
    def add_user_with_token(conn, user_id, password=C.TEST_DEFAULT_USER_PASSWORD):
        token = jwt_encode(str(user_id), C.TEST_DEFAULT_TERMINAL)
        sql = 'insert into usr(user_id,password,token) values (\'{0}\',\'{1}\',\'{2}\')' \
            .format(user_id, password, token)
        TestTool.execute_sql(conn, sql)
        return token

    @staticmethod
    def execute_sql(conn, sql):
        cursor = conn.cursor()
        cursor.execute(sql)
        conn.commit()
