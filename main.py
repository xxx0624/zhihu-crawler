from zhihu_user_crawler import ZhihuUserCrawler

import logging


zhc = ZhihuUserCrawler()

login_flag = zhc.login()

if login_flag:
	logging.info("login success")
	zhc.start_parse("")
else:
	logging.info("login fail...")
logging.info('over......................................')