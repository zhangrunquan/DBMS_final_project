"""为测试提供工具函数"""
from be.model.constants import Constants as C


class TestTool:

    @staticmethod
    def add_order(conn, buyer_id, order_id):
        sql = 'insert into finished_order(order_id,buyer_id) ' \
              'values ({0},\'{1}\');'.format(order_id, buyer_id)
        TestTool.execute_sql(sql)

    @staticmethod
    def add_user(conn, user_id):
        sql = 'insert into usr(user_id,password) values (\'{0}\',\'{1}\')' \
            .format(user_id,C.TEST_DEFAULT_USER_PASSWORD)
        TestTool.execute_sql(sql)

    @staticmethod
    def execute_sql(conn, sql):
        cursor = conn.cursor()
        cursor.execute(sql)
        conn.commit()
