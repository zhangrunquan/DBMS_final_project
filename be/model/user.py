import jwt
import time
import logging
import sqlite3 as sqlite

from flask import jsonify

from be.model import error
from be.model import db_conn
from be.model.constants import Constants as C

# encode a json string like:
#   {
#       "user_id": [user name],
#       "terminal": [terminal code],
#       "timestamp": [ts]} to a JWT
#   }
from be.model.order_manager import OrderManager


def jwt_encode(user_id: str, terminal: str) -> str:
    encoded = jwt.encode(
        {"user_id": user_id, "terminal": terminal, "timestamp": time.time()},
        key=user_id,
        algorithm="HS256",
    )
    return encoded.decode("utf-8")


# decode a JWT to a json string like:
#   {
#       "user_id": [user name],
#       "terminal": [terminal code],
#       "timestamp": [ts]} to a JWT
#   }
def jwt_decode(encoded_token, user_id: str) -> str:
    decoded = jwt.decode(encoded_token, key=user_id, algorithms="HS256")
    return decoded


class User(db_conn.DBConn):
    token_lifetime: int = 3600  # 3600 second

    def __init__(self):
        db_conn.DBConn.__init__(self)

    def __check_token(self, user_id, db_token, token) -> bool:
        try:
            if db_token != token:
                return False
            jwt_text = jwt_decode(encoded_token=token, user_id=user_id)
            ts = jwt_text["timestamp"]
            if ts is not None:
                now = time.time()
                if self.token_lifetime > now - ts >= 0:
                    return True
        except jwt.exceptions.InvalidSignatureError as e:
            logging.error(str(e))
            return False

    def register(self, user_id: str, password: str):
        try:
            terminal = "terminal_{}".format(str(time.time()))
            token = jwt_encode(user_id, terminal)
            self.conn.execute(
                "INSERT into user(user_id, password, balance, token, terminal) "
                "VALUES (?, ?, ?, ?, ?);",
                (user_id, password, 0, token, terminal), )
            self.conn.commit()
        except sqlite.Error:
            return error.error_exist_user_id(user_id)
        return 200, "ok"

    def check_token(self, user_id: str, token: str) -> (int, str):
        cursor = self.conn.execute("SELECT token from user where user_id=?", (user_id,))
        row = cursor.fetchone()
        if row is None:
            return error.error_authorization_fail()
        db_token = row[0]
        if not self.__check_token(user_id, db_token, token):
            return error.error_authorization_fail()
        return 200, "ok"

    def check_password(self, user_id: str, password: str) -> (int, str):
        cursor = self.conn.execute("SELECT password from user where user_id=?", (user_id,))
        row = cursor.fetchone()
        if row is None:
            return error.error_authorization_fail()

        if password != row[0]:
            return error.error_authorization_fail()

        return 200, "ok"

    def login(self, user_id: str, password: str, terminal: str) -> (int, str, str):
        token = ""
        try:
            code, message = self.check_password(user_id, password)
            if code != 200:
                return code, message, ""

            token = jwt_encode(user_id, terminal)
            cursor = self.conn.execute(
                "UPDATE user set token= ? , terminal = ? where user_id = ?",
                (token, terminal, user_id), )
            if cursor.rowcount == 0:
                return error.error_authorization_fail() + ("", )
            self.conn.commit()
        except sqlite.Error as e:
            return 528, "{}".format(str(e)), ""
        except BaseException as e:
            return 530, "{}".format(str(e)), ""
        return 200, "ok", token

    def logout(self, user_id: str, token: str) -> bool:
        try:
            code, message = self.check_token(user_id, token)
            if code != 200:
                return code, message

            terminal = "terminal_{}".format(str(time.time()))
            dummy_token = jwt_encode(user_id, terminal)

            cursor = self.conn.execute(
                "UPDATE user SET token = ?, terminal = ? WHERE user_id=?",
                (dummy_token, terminal, user_id), )
            if cursor.rowcount == 0:
                return error.error_authorization_fail()

            self.conn.commit()
        except sqlite.Error as e:
            return 528, "{}".format(str(e))
        except BaseException as e:
            return 530, "{}".format(str(e))
        return 200, "ok"

    def unregister(self, user_id: str, password: str) -> (int, str):
        try:
            code, message = self.check_password(user_id, password)
            if code != 200:
                return code, message

            cursor = self.conn.execute("DELETE from user where user_id=?", (user_id,))
            if cursor.rowcount == 1:
                self.conn.commit()
            else:
                return error.error_authorization_fail()
        except sqlite.Error as e:
            return 528, "{}".format(str(e))
        except BaseException as e:
            return 530, "{}".format(str(e))
        return 200, "ok"

    def change_password(self, user_id: str, old_password: str, new_password: str) -> bool:
        try:
            code, message = self.check_password(user_id, old_password)
            if code != 200:
                return code, message

            terminal = "terminal_{}".format(str(time.time()))
            token = jwt_encode(user_id, terminal)
            cursor = self.conn.execute(
                "UPDATE user set password = ?, token= ? , terminal = ? where user_id = ?",
                (new_password, token, terminal, user_id), )
            if cursor.rowcount == 0:
                return error.error_authorization_fail()

            self.conn.commit()
        except sqlite.Error as e:
            return 528, "{}".format(str(e))
        except BaseException as e:
            return 530, "{}".format(str(e))
        return 200, "ok"

    def cancel_order(self,user_id,password,order_id):
        """取消订单"""
        # sql="select user_id,password from usr where user_id={0}".format(user_id)
        # cursor=self.conn.cursor()
        # cursor.execute(sql)
        # if(cursor.rowcount==0):
        #     return error.error_non_exist_user_id(user_id)
        # row = cursor.fetchone()
        # if(row[1]!=password):
        #     return error.error_authorization_fail()
        code,msg=self.check_password(user_id,password)
        if(code!=200):
            return code,msg
        # 用户认证通过
        om=OrderManager(conn=self.conn)
        canceled_num=om.cancel_order(order_id)
        if(canceled_num==0):
            return error.error_invalid_order_id(order_id)
        else:
            return 200,"ok"

    def history_order(self,user_id,token):
        """用户查询已完成订单

        Returns:
            code,json_response_body
        """
        code,msg=self.check_token(user_id,token)
        if(code!=200):
            return code,msg
        # 用户认证通过
        om=OrderManager(conn=self.conn)
        rows=om.user_history_order(user_id)
        l=list(rows)
        return 200,jsonify(l)

    def consign(self, seller_id, password, order_id):
        """商家发货"""
        code, msg = self.check_password(seller_id, password)
        if (code != 200):
            return code, msg
        # 用户认证通过
        om = OrderManager(conn=self.conn)
        updated_num=om.update_order_status(order_id,C.PO_WATI_RECEIPT)
        if(updated_num!=1):
            return error.error_invalid_order_id(order_id)
        else:
            return 200,"ok"

    def receive(self, user_id, password, order_id):
        """用户收货"""
        code, msg = self.check_password(user_id, password)
        if (code != 200):
            return code, msg
        # 用户认证通过
        om = OrderManager(conn=self.conn)
        succ_flag = om.move_to_finished(order_id)
        if(succ_flag):
            return 200,'ok'
        else:
            return error.error_invalid_order_id(order_id)