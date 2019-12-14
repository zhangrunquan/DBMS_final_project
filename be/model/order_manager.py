from be.model import db_conn


class OrderManager(db_conn.DBConn):
    """提供与订单有关的功能
    许多类都需要订单相关功能,应该抽象出来以避免重复实现相似功能
    """
    def __init__(self):
        db_conn.DBConn.__init__(self)

    def user_history_order(self):
        """用户查询历史订单

        """
        pass

    def user_cancel_order(self):
        """用户取消订单
        """
        pass


class ExpiredOrderCanceler():
    """利用OrderManager的功能,实现自动取消过期订单"""