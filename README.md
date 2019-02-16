# crawl zhihu user info

爬取知乎(zhihu)用户的代码，数据存储于mongodb

## install

1. python version = 2.7.10

2. 安装scrapy

3. 安装mongodb在本机

4. mongodb: ip默认`localhost`，port默认`27017` (配置在`setting.py`)

5. mongodb: collection如下：

   - `zh_user`: 知乎用户

6. mongodb: db.zhihu.zh_user 用户表结构
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
    crawl_finish # 该用户是否爬取完成 TODO//改为广度优先搜索故放弃该字段
    ```

## 开始爬取

1. 在setting中设置知乎账号和密码以及开始的url
2. 在setting中设置是否下载zhihu user头像，默认下载到UserImg文件夹中
3. 在setting中设置是否将下载的zhihu user头像上传到七牛云中，默认不上传
4. 在setting中设置七牛云账号以及bucket相关信息
5. python main.py
   
## 查看运行结果

```
> use zhihu
switched to db zhihu
> db.gh_user.count()
10000
```

# Reference

[SmileXie / zhihu_crawler](https://github.com/SmileXie/zhihu_crawler)

[javachen / scrapy-zhihu-github](https://github.com/javachen/scrapy-zhihu-github)
