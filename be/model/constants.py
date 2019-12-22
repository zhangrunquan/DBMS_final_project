"""store constants"""

class Constants:

    # 数据库连接设置
    DB_NAME="bookstore"
    DB_USER="postgres"
    DB_PASSWORD="lcz123456"
    DB_HOST="127.0.0.1"
    DB_PORT="5432"

    # 自动清除过期订单
    AUTO_CANCELER_DEFAULT_INTERVAL=15 # 默认时间间隔

    # 测试用
    TEST_DEFAULT_USER_PASSWORD='123456'
    TEST_DEFAULT_TERMINAL='terminal1'