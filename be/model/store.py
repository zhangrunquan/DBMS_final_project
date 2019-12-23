import logging
import os
import sqlite3 as sqlite
import psycopg2
from be.model.constants import Constants as C

class Store:
    """database abstraction"""

    @staticmethod
    def init_tables():
        """初始化数据库"""

        conn = Store.get_db_conn()
        cursor = conn.cursor()
        # 删除表
        tables = ['usr', 'store', 'user_store', 'pending_order', 'finished_order']
        sql = "".join(['drop table if exists {};'.format(name) for name in tables])

        try:
            cursor.execute(sql)
        except Exception as e:
            print(e)

        conn.commit()

        sql = 'create table usr(' \
              'user_id varchar(200) primary key ,' \
              'password varchar(200),' \
              'balance int,' \
              'token varchar(500),' \
              'terminal varchar(500)' \
              ');'
        sql += 'create table store(' \
               'id serial primary key,' \
               'store_id varchar(100),' \
               'book_id varchar(100),' \
               'book_info varchar(2500000),' \
               'stock_level int,' \
               'price int,' \
               'search_content1 varchar(200),' \
               'search_content2 varchar(200)' \
               ');'
        sql += 'create table user_store(' \
               'user_id varchar(100),' \
               'store_id varchar(100) primary key' \
               ');'
        sql += 'create table pending_order(' \
               'order_id varchar(200) primary key,' \
               'buyer_id varchar(100),' \
               'seller_id varchar(100),' \
               'store_id varchar(100),' \
               'price int,' \
               'order_info varchar(500),' \
               'status smallint,' \
               'create_ts timestamp' \
               ');'
        sql += 'create table finished_order(' \
               'order_id varchar(200) primary key,' \
               'buyer_id varchar(100),' \
               'seller_id varchar(100),' \
               'store_id varchar(100),' \
               'order_info varchar(500),' \
               'price int' \
               ');'
        cursor.execute(sql)
        sql = 'create index store_i1 on store(store_id);'
        sql += 'create index store_i2 on store(book_id);'
        sql += 'create index pending_order_i1 on pending_order(buyer_id);'
        sql += 'create index finished_order_i1 on finished_order(buyer_id);'
        cursor.execute(sql)
        conn.commit()

    @staticmethod
    def get_db_conn():
        """获取到数据库连接"""
        return psycopg2.connect(database=C.DB_NAME, user=C.DB_USER, password=C.DB_PASSWORD, host=C.DB_HOST
                                , port=C.DB_PORT)
