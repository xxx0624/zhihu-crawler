from zhihu_user_crawler import ZhihuUserCrawler

import logging, time


if __name__ == '__main__':
	zhc = ZhihuUserCrawler()
	login_flag = zhc.login()
	if login_flag:
		time.sleep(SLEEP_TIME)
		zhc.start_parse("")
	print '['+zhc._now_time+']'+' '+'over......................................'