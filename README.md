#crawl zhihu user info

爬取知乎(zhihu)用户的代码，数据存储于mongodb

#install(仅依赖scrapy.item&Field)

0. python version = 2.7.10

1. 安装scrapy

2. 安装mongodb在本机

3. mongodb: ip默认localhost，port默认27017 (配置在setting.py)

4. mongodb: collection如下：

   - `zh_user`: 知乎用户

5. mongodb: db.zhihu.zh_user 用户表结构
    ```
    _id int, # 用户id
    url string,
    username string, # 用户名，如 zhouyuan
    nickname string, # 昵称，如 周源
    location string, # 居住地
    industry string, # 行业，如 互联网
    sex int, # 性别，1：男， 2：女， 0：未知
    jobs [], # 工作列表
    educations [], # 学校教育列表
    description string, # 自我简介
    sinaweibo string, # 新浪微博账号
    tencentweibo string, # 腾讯微博账号
    ask_num int, # 提问数， 如 590
    answer_num int, # 回答数，如 340
    post_num int, # 专栏文章数， 如 3
    collection_num int, # 收藏数，如 9
    log_num int, # 编辑数，如14980
    agree_num int, # 收到的赞同，如 15316
    thank_num int, # 收到的感谢，如 3500
    fav_num int, # 被收藏次数，如 9424
    share_num int, # 被分享次数，如 922
    followee_num int, # 关注数，如 1515
    follower_num int, # 被关注数（粉丝），如 319529
    update_time datetime # 信息更新时间，如 2014-05-17 11:15:00
    ```

#开始爬取知乎zhihu信息

1. 先在setting中设置知乎账号和密码以及开始的url
2. python zhihu_user_crawler.py
   
#查看运行结果

```
> use zhihu
switched to db zhihu
> db.gh_user.count()
10000
```

#Reference

[SmileXie / zhihu_crawler](https://github.com/SmileXie/zhihu_crawler)

[javachen / scrapy-zhihu-github](https://github.com/javachen/scrapy-zhihu-github)