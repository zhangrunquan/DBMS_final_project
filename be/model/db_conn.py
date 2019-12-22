from be.model.store import Store


class DBConn:
    def __init__(self):
        self.conn = Store.get_db_conn()

    def user_id_exist(self, user_id):
        cursor=self.conn.cursor()
        sql='select user_id from usr where user_id=\'{0}\''.format(user_id)
        cursor.execute(sql)
        row=cursor.fetchone()
        if row is None:
            return False
        else:
            return True

    def book_id_exist(self, store_id, book_id):
        cursor = self.conn.cursor()
        sql = 'select book_id from store where store_id=\'{0}\' and book_id=\'{1}\''.format(store_id,book_id)
        cursor.execute(sql)
        row = cursor.fetchone()
        if row is None:
            return False
        else:
            return True

    def store_id_exist(self, store_id):
        cursor = self.conn.cursor()
        sql = 'select store_id from user_store where store_id=\'{0}\''.format(store_id)
        cursor.execute(sql)
        row = cursor.fetchone()
        if row is None:
            return False
        else:
            return True
