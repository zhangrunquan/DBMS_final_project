## 用户查询所有历史订单(已完成订单)

#### URL：
POST http://$address$/buyer/finished_order

#### Request

Body:
```
{
    "user_id":"$user name$",
    "token":"token"
}
```

变量名 | 类型 | 描述 | 是否可为空
---|---|---|---
user_id | string | 用户名 | N
token | token | token | N


#### Response

Status Code:

码 | 描述
--- | ---
200 | 正常
401 | 认证失败


##### Body:
```json
{
  "order_num": "$order num$",
  "orders":[
    {
      "order_id": "uuid",
      "seller_id": "uuid",
      "store_id": "uuid",
      "order_info": [{}],
      "price": "$price$"
    }
  ]
  
}
```

##### 属性说明：

变量名 | 类型 | 描述 | 是否可为空
---|---|---|---
order_id | string | 订单号，只有返回200时才有效 | N
order_info | array | 书籍信息json的数组 | N


## 用户取消订单

#### URL：
POST http://$address$/buyer/cancel_order

#### Request

Body:
```
{
    "user_id":"$user name$",
    "password":"$user password$"
    "order_id":"$order id$"
}
```

变量名 | 类型 | 描述 | 是否可为空
---|---|---|---
user_id | string | 用户名 | N
password | string | 登陆密码 | N


#### Response

Status Code:

码 | 描述
--- | ---
200 | 正常
5XX | 买家用户ID不存在
401 | 密码错误
518 | 该用户无此order_id的order



