from be.model import db_conn, error
from be.model.constants import Constants as C
import datetime
import time

from be.model.store import Store


class OrderManager(db_conn.DBConn):
    """提供与订单有关的功能
    所有参数的有效性由调用者检查,commit由调用者负责
    """

    def __init__(self, conn=None):
        if conn is not None:  # OM作为服务提供者,可以使用调用者提供的数据库连接
            self.conn = conn
        else:
            db_conn.DBConn.__init__(self)

    def user_history_order(self, user_id):
        """查询用户的所有已完成订单

        Returns:
            cursor returned by psycopg2.cursor.fetchall()
            containing tuples like (order_id,seller_id,store_id,order_info,price)

        Raises:
            Exception

        """
        cursor = self.conn.cursor()
        # 查询订单并返回
        sql = 'select order_id,seller_id,store_id,order_info,price ' \
              'from finished_order ' \
              'where buyer_id=\'{0}\';'.format(user_id)
        try:
            cursor.execute(sql)
        except Exception:
            raise
        return cursor.fetchall()

    def cancel_order(self, user_id, order_id):
        """取消订单
        will rollback if exception happened

        Returns:
            deleted row num

        Raises:
            any Exception

        """

        cursor = self.conn.cursor()
        sql = 'delete from pending_order where buyer_id=\'{0}\' and order_id=\'{1}\';'.format(user_id, order_id)
        try:
            cursor.execute(sql)
        except Exception:
            self.conn.rollback()
            raise
        return cursor.rowcount

    def update_order_status(self,order_id,status:int):
        """修改订单状态

        Returns:
            updated row num

        Raises:
            any Exception

        """
        cursor=self.conn.cursor()
        sql='update pending_order set status={0} where order_id=\'{1}\';'.format(status,order_id)
        try:
            cursor.execute(sql)
        except Exception:
            self.conn.rollback()
            raise
        return cursor.rowcount

    def move_to_finished(self,order_id:str):
        """将订单移至已完成

        Returns:
            True on success,False on failure

        Raises:
            any Exception

        """
        cursor=self.conn.cursor()
        # 获取订单信息
        sql='select order_id,buyer_id,seller_id,store_id,price,order_info from pending_order ' \
            'where order_id=\'{0}\';'.format(order_id)
        cursor.execute(sql)
        row=cursor.fetchone()
        if row is None:
            return error.error_invalid_order_id(order_id)

        # buyer_id,seller_id,store_id,order_info,price=row
        # 删除pending_order中的订单
        sql='delete from pending_order where order_id=\'{0}\';'.format(order_id)
        sql+='insert into finished_order(order_id,buyer_id, seller_id, store_id, price, order_info)' \
             ' values (\'{0}\',\'{1}\',\'{2}\',\'{3}\',{4},\'{5}\');'.format(*row)
        # finished_order添加订单
        cursor.execute(sql)
        return True




class ExpiredOrderCanceler():
    """自动取消过期订单"""

    @staticmethod
    def cancel_expired_order(conn, valid_time=15):
        """删除过期订单

        Args:
            conn:db connection
            valid_time:订单有效时间,秒为单位

        Returns:
            deleted row count

        Raises:
            Exception

        """
        now = datetime.datetime.now()
        min_dt = now - datetime.timedelta(seconds=valid_time)
        dt_str = min_dt.strftime("%Y-%m-%d %H:%M:%S")
        sql = 'delete from pending_order where create_ts<timestamp \'{0}\';'.format(dt_str)
        try:
            cursor = conn.cursor()
            cursor.execute(sql)
        except Exception:
            conn.rollback()
            raise
        return cursor.rowcount

    @staticmethod
    def work(valid_time=15, interval=10):
        """循环运行"""
        while 1:
            try:
                conn = Store.get_db_conn()
                ExpiredOrderCanceler.cancel_expired_order(conn, valid_time)
                conn.commit()
                conn.close()
            except Exception:
                raise

            time.sleep(interval)
