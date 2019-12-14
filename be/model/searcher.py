"""实现搜索"""
from be.model import db_conn


class Searcher(db_conn.DBConn):
    """实现搜索"""

    def __init__(self):
        db_conn.DBConn.__init__(self)

    def search(self,content_scope,book_scope,max_id,keyword,):
        """查找内容与关键字匹配的书籍

        Args:
            content_scope: 书籍的哪些部分用来搜索
            book_scope: 搜索书籍的范围,可能为全站或店铺
            max_id: 上次返回结果的最大id,用于分页
            keyword: 搜索关键字

        Returns:
            code,bookinfo json str

        """