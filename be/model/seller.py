import sqlite3 as sqlite
from be.model import error
from be.model import db_conn
import psycopg2
from be.model.constants import Constants as C

class Seller(db_conn.DBConn):

    def __init__(self):
        db_conn.DBConn.__init__(self)

    def add_book(self, user_id: str, store_id: str, book_id: str, book_json_str: str, stock_level: int):

        if not self.user_id_exist(user_id):
            return error.error_non_exist_user_id(user_id)
        if not self.store_id_exist(store_id):
            return error.error_non_exist_store_id(store_id)
        if self.book_id_exist(store_id, book_id):
            return error.error_exist_book_id(book_id)

        sql='INSERT into store(store_id, book_id, book_info, stock_level) values (\'{0}\',\'{1}\',\'{2}\',{3})' \
            .format(store_id, book_id, book_json_str, stock_level)
        cursor=self.conn.cursor()
        try:
            cursor.execute(sql)
        except Exception as e:
            l=len(book_json_str)
            print(e)
        self.conn.commit()

        return 200, "ok"

    def add_stock_level(self, user_id: str, store_id: str, book_id: str, add_stock_level: int):
        if not self.user_id_exist(user_id):
            return error.error_non_exist_user_id(user_id)
        if not self.store_id_exist(store_id):
            return error.error_non_exist_store_id(store_id)
        if not self.book_id_exist(store_id, book_id):
            return error.error_non_exist_book_id(book_id)

        # sql="UPDATE store SET stock_level = stock_level + {0}  " \
        #     "WHERE store_id = {1} AND book_id = {2}".format(add_stock_level, store_id, book_id))
        sql='update store set stock_level=stock_level+{0} ' \
            'WHERE store_id = \'{1}\' AND book_id = \'{2}\''.format(add_stock_level,store_id,book_id)
        cursor=self.conn.cursor()
        cursor.execute(sql)
        self.conn.commit()
        return 200, "ok"

    def create_store(self, user_id: str, store_id: str) -> (int, str):
        if not self.user_id_exist(user_id):
            return error.error_non_exist_user_id(user_id)
        if self.store_id_exist(store_id):
            return error.error_exist_store_id(store_id)
        sql='insert into user_store(user_id, store_id) values (\'{0}\',\'{1}\')'.format(user_id,store_id)
        cursor=self.conn.cursor()
        cursor.execute(sql)
        self.conn.commit()
        return 200, "ok"


