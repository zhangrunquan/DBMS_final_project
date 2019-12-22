"""store constants"""

class Constants:

    # 数据库连接设置
    DB_NAME="bookstore"
    DB_USER="postgres"
    DB_PASSWORD="lcz123456"
    DB_HOST="127.0.0.1"
    DB_PORT="5432"



    # 数据库中表示状态的数字
    # pending order表 status
    PO_WAIT_PAYMENT=0
    PO_WATI_SHIPMENT=1
    PO_WATI_RECEIPT=2



    # 自动清除过期订单
    AUTO_CANCELER_DEFAULT_INTERVAL=15 # 默认时间间隔


    # 测试用
    TEST_DEFAULT_USER_PASSWORD='123456'
    TEST_DEFAULT_TERMINAL='terminal1'
    TEST_DEFAULT_SELLER='test_seller'
    TEST_DEFAULT_BUYER='test_buyer'
