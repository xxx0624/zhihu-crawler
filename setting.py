# -*- coding:utf-8 -*-

#the time to sleep between two urls
SLEEP_TIME = 0

#user name
EMAIL = '273589630@qq.com'

#user pwd
PASSWORD = 'qqqqxxx0624'

#start url
START_URL = "https://www.zhihu.com/people/xxx0624/about"

#the max depth to follow url
MAX_DEPTH = 20

#mongodb ip
MONGODB_IP = "localhost"
#mongodb port
MONGODB_PORT = 27017

#the place for user img to save
IMG_FOLDER = 'UserImg'

HEADER={
    "Host": "www.zhihu.com",
    "Connection": "keep-alive",
    "Cache-Control": "max-age=0",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/34.0.1847.131 Safari/537.36",
    "Referer": "http://www.zhihu.com/people/xxx0624",
    "Accept-Encoding": "gzip,deflate,sdch",
    "Accept-Language": "zh-CN,zh;q=0.8,en-US;q=0.6,en;q=0.4,zh-TW;q=0.2",
}