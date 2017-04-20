工作交接
===
### 交接内容
#### **大众点评用户信息**
|城市\类别|餐厅|酒店|景点|
|:-:|-|-|-|
|北京|√|√|√|
|上海|√|√|√
|广州|√|√|√
**字段：**
>{'用户ID': user_id, '店铺ID': merchant_id, '用户名': username, '地址': address, '性别': gender, '恋爱状况': relationship, '星座': sign, '生日': birthday}

*PS:*
* 大众点评目前对用户信息页面无反爬虫措施
*  爬虫先从文件读取用户信息页面的链接和店铺ID，然后根据用户链接抓取内容
* *pps:* 将用户评论信息的json文件清洗为本爬虫能解析的json文件格式的代码在老胡那里
* 本爬虫能解析的json文件内容的格式，例：
`{"shop_url": "http://www.dianping.com/shop/10342086/review_more?pageno=3", "user_url": "http://www.dianping.com/member/17219648"}`

---
[爬虫源码]（）
