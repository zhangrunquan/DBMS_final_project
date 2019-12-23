import sqlite3 as sqlite
import uuid
import json
import logging

from flask import jsonify

from be.model import db_conn
from be.model import error
import psycopg2
from be.model.constants import Constants as C
from be.model.order_manager import OrderManager


class Buyer(db_conn.DBConn):
    def __init__(self):
        db_conn.DBConn.__init__(self)

    def new_order(self, user_id: str, store_id: str, id_and_count: [(str, int)]) -> (int, str, str):
        order_id = ""

        if not self.user_id_exist(user_id):
            return error.error_non_exist_user_id(user_id) + (order_id, )
        if not self.store_id_exist(store_id):
            return error.error_non_exist_store_id(store_id) + (order_id, )
        uid = "{}_{}_{}".format(user_id, store_id, str(uuid.uuid1()))

        total_price=0

        cursor = self.conn.cursor()

        for book_id, count in id_and_count:

            # 获取店铺中书籍信息
            sql='select book_id,stock_level,book_info from store ' \
                'where store_id=\'{0}\' and book_id=\'{1}\';'.format(store_id,book_id)
            cursor.execute(sql)
            rows=cursor.fetchall()

            if rows ==[]:
                return error.error_non_exist_book_id(book_id) + (order_id, )

            try:
                stock_level = rows[0][1]
                book_info = rows[0][2]
            except ValueError as e:
                print(e)
            book_info_json = json.loads(book_info)
            price = book_info_json.get("price")
            total_price+=price*count


            if stock_level < count:
                return error.error_stock_level_low(book_id) + (order_id,)

            # 库存足够,减少被购买的量
            sql='update store set stock_level=stock_level-{0} ' \
                'where store_id =\'{1}\' and book_id=\'{2}\' and stock_level>={3};' \
                .format(count, store_id, book_id, count)
            cursor.execute(sql)
            if cursor.rowcount == 0:
                return error.error_stock_level_low(book_id) + (order_id, )

        # 获取卖家id
        sql='select user_id from user_store where store_id=\'{0}\';'.format(store_id)
        cursor.execute(sql)
        rows=cursor.fetchall()
        seller_id=rows[0][0]

        # 添加新订单
        create_ts='now()'
        order_info=jsonify(id_and_count)

        sql='insert into pending_order (buyer_id, seller_id, store_id, price, order_info, status, create_ts,order_id) ' \
            'values (\'{0}\',\'{1}\',\'{2}\',{3},\'{4}\',{5},\'{6}\',\'{7}\'); ' \
            .format(user_id,seller_id,store_id,total_price,order_info,C.PO_WAIT_PAYMENT,create_ts,uid)
        cursor.execute(sql)

        self.conn.commit()
        order_id = uid

        return 200, "ok", order_id

    def payment(self, user_id: str, password: str, order_id: str) -> (int, str):
        conn = self.conn

        # 获取订单信息
        sql='SELECT  buyer_id, seller_id, price,status ' \
            'FROM pending_order WHERE order_id = \'{}\';'.format(order_id)

        cursor=conn.cursor()
        cursor.execute(sql)
        rows = cursor.fetchall()

        if rows ==[]:
            return error.error_invalid_order_id(order_id)

        # 检查订单状态为待支付
        status=rows[0][3]
        if(status!=C.PO_WAIT_PAYMENT):
            return error.error_invalid_order_id(order_id)

        buyer_id=rows[0][0]
        seller_id = rows[0][1]
        price = rows[0][2]


        if buyer_id != user_id:
            return error.error_authorization_fail()

        # 检查用户钱够
        sql ='SELECT balance, password FROM usr WHERE user_id = \'{0}\';'.format(user_id)
        rows = cursor.execute(sql)
        rows = cursor.fetchall()

        if rows is None:
            return error.error_non_exist_user_id(buyer_id)
        balance = rows[0][0]

        if password != rows[0][1]:
            return error.error_authorization_fail()

        # 确认卖家存在
        if not self.user_id_exist(seller_id):
            return error.error_non_exist_user_id(seller_id)

        # 确认用户钱够
        if balance < price:
            return error.error_not_sufficient_funds(order_id)

        # 减少用户余额
        sql='UPDATE usr set balance = balance - {0} ' \
            'WHERE user_id = \'{1}\' AND balance >= {2};' \
            .format(price,user_id,price)
        cursor.execute(sql)

        if cursor.rowcount == 0:
            return error.error_not_sufficient_funds(order_id)

        # 增加卖家余额
        sql='UPDATE usr set balance = balance + {0} ' \
            'WHERE user_id = \'{1}\';'.format(price,buyer_id)
        cursor.execute(sql)

        if cursor.rowcount == 0:
            return error.error_non_exist_user_id(buyer_id)

        # 修改订单状态为待发货
        om=OrderManager(conn)
        om.update_order_status(order_id,C.PO_WATI_SHIPMENT)

        conn.commit()

        return 200, "ok"

    def add_funds(self, user_id, password, add_value) -> (int, str):

        sql='SELECT password  from usr where user_id=\'{0}\''.format(user_id)

        cursor=self.conn.cursor()
        cursor.execute(sql)
        rows=cursor.fetchall()

        if rows is None:
            return error.error_authorization_fail()

        if rows[0][0] != password:
            return error.error_authorization_fail()

        sql='UPDATE usr SET balance = balance + {0} WHERE user_id = \'{1}\''.format(add_value,user_id)
        cursor.execute(sql)

        if cursor.rowcount == 0:
            return error.error_non_exist_user_id(user_id)

        self.conn.commit()

        return 200, "ok"

