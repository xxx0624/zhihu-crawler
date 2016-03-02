from setting import *

import requests
import sys
import time
from bs4 import BeautifulSoup


class ZhihuCommon(object):
	my_header = HEADER
	_xsrf = None
	_session = None
	_last_get_page_fail = False

	@staticmethod
	def set_xsrf(xsrf):
		ZhihuCommon._xsrf = xsrf

	@staticmethod
	def get_xsrf():
		return ZhihuCommon._xsrf

	@staticmethod
	def session_init():
		ZhihuCommon._session = requests.Session()

	@staticmethod
	def get_session():
		return ZhihuCommon._session

	@staticmethod
	def get(url):
		try_time = 0
		
		while try_time < 5:
			if ZhihuCommon._last_get_page_fail:
				time.sleep(10)
				
			try:
				try_time += 1
				response = ZhihuCommon.get_session().get(url, headers = ZhihuCommon.my_header, timeout = 30)
				soup = BeautifulSoup(response.text)
				ZhihuCommon._last_get_page_fail = False
				return response, soup
			except Exception as e:
				print("fail to get " + url + " error info: " + str(e) + " try_time " + str(try_time))
				ZhihuCommon._last_get_page_fail = True
		else:
			raise

	@staticmethod
	def post(url, post_dict):
		try_time = 0
		
		while try_time < 5:
			if ZhihuCommon._last_get_page_fail:
				time.sleep(10)
				
			try:
				try_time += 1
				response = ZhihuCommon.get_session().post(url, headers = ZhihuCommon.my_header, data = post_dict, timeout = 30)
				ZhihuCommon._last_get_page_fail = False
				return response
			except Exception as e:
				print("fail to post " + url + " error info: " + str(e) + " try_time " + str(try_time))
				ZhihuCommon._last_get_page_fail = True
		else:
			raise
