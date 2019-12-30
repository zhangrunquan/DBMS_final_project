"""实现搜索"""
import sqlite3 as sqlite
from be.model import error
from be.model import db_conn
import psycopg2
from be.model.constants import Constants as C
import json
from be.model.store import Store


class Searcher(db_conn.DBConn):
    """实现搜索"""

    def __init__(self):
        db_conn.DBConn.__init__(self)
    
    def database_ini(self):
        #initiate databse
        Store.init_tables()
        conn = Store.get_db_conn()
        cursor = conn.cursor()
        sql="INSERT into store(store_id, book_id, book_info, stock_level,search_content1, search_content2) values (\'{0}\',\'{1}\',\'{2}\',{3},to_tsvector(\'{4}\'),to_tsvector(\'{5}\'))"\
            .format("1", "1", "book_info", "1","人物","美丽心灵")
        cursor.execute(sql)
        conn.commit()
        cursor.close()
        conn.close()

    def search(self,content_scope:str,book_scope:str,max_id:int,keyword:str):
        """查找内容与关键字匹配的书籍

        Args:
            content_scope: 书籍的哪些部分用来搜索
            book_scope: 搜索书籍的范围,可能为全站或店铺
            max_id: 上次返回结果的最大id,用于分页
            keyword: 搜索关键字

        Returns:
            code,bookinfo json str

        """

        if content_scope=="tags":
            search_feild="search_content1"
        elif content_scope=="titles":
            search_feild="search_content2"
        else:
            return 521,"No such feild"
        
        if book_scope=="all":
            search_scope = 1
        else:
            if not self.store_id_exist(book_scope):
                return error.error_non_exist_store_id(book_scope)
            search_scope=0
        
        if search_scope==1:
            sql= "select * from store where %s@@to_tsquery('%s') limit 20 offset %d"%(search_feild,keyword,max_id)
        else:
            sql= "select * from store where store_id='%s' and %s@@to_tsquery('%s') limit 20 offset %d"%(book_scope,search_feild, keyword, max_id)
        cursor=self.conn.cursor()
        cursor.execute(sql)
        self.conn.commit()
        result = cursor.fetchall()
        if(len(result)==0):
            return 522, "No result returned!" 
    
        return 200,json.dumps(result)