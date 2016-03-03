# -*- coding:utf-8 -*-

from items import *
from setting import *

from bs4 import BeautifulSoup
from scrapy.selector import Selector
from zhihu_common import ZhihuCommon
from lxml import etree
from datetime import datetime
from zhihu_pipeline import MongoDBPipeline

import sys, time
import logging, requests
import codecs, json



reload(sys)
sys.setdefaultencoding('utf-8')


class ZhihuUserCrawler(object):

	_base_url = 'https://www.zhihu.com'
	_email = EMAIL
	_password = PASSWORD
	_xsrf = ''
	mgd = None
	_now_time = str(datetime.strptime(str(datetime.today()), "%Y-%m-%d %H:%M:%S.%f"))

	def __init__(self):
		self.mgd = MongoDBPipeline()

	def init_xsrf(self):
		try:
			_, soup = ZhihuCommon.get(self._base_url)
			input_tag = soup.find("input", {"name": "_xsrf"})
			xsrf = input_tag["value"]
			#ZhihuCommon.set_xsrf(xsrf)
			self._xsrf = xsrf
			print '['+self._now_time+']'+'set the xsrf is :' + xsrf
		except Exception as e:
			logging.error("fail to init xsrf. " + str(e))

	def login(self):
		ZhihuCommon.session_init()
		self.init_xsrf()
		login_url = self._base_url + "/login/email"
		post_data = {
			'rememberme:': 'y',
			'password': self._password,
			'email': self._email,
			'_xsrf': self._xsrf
		}
		reponse_login = ZhihuCommon.post(login_url, post_data)
		
		if reponse_login.json()['r'] == 0:
			time.sleep(SLEEP_TIME)
			print '['+self._now_time+']'+' '+'login successfully...'
			return True
		else:
			print '['+self._now_time+']'+' '+'login...fail...sad...story...'
			return False

	def start_parse(self, START_URL):
		if START_URL == "":
			START_URL = "https://www.zhihu.com/people/xxx0624/about"
		print '['+self._now_time+']'+' '+'start parse url:' + START_URL + '...'
		response, soup = ZhihuCommon.get(START_URL)
		self.parse_zhihu_user(response, soup, 0)
		print '['+self._now_time+']'+' '+'finish the zhihu-user-crawler...23333333333333333...'
		return 

	def parse_zhihu_user(self, response, soup, depth):
		zhihu_user = ZhihuUserItem()
		selector = etree.HTML(str(soup))
		time.sleep(SLEEP_TIME)
		#get zhihu_user info
		zhihu_user['_id']=zhihu_user['username']= response.url.split('/')[-2]
		zhihu_user['url']= response.url

		select_list = selector.xpath(zhihu_user.nickname_rule)
		if len(select_list) == 0:
			select_list = ['']
		zhihu_user['nickname'] = ''.join(select_list[0])

		select_list = selector.xpath(zhihu_user.location_rule)
		if len(select_list) == 0:
			select_list = ['']
		zhihu_user['location'] = ''.join(select_list[0])

		select_list = selector.xpath(zhihu_user.industry_rule)
		if len(select_list) == 0:
			select_list = ['']
		zhihu_user['industry'] = ''.join(select_list[0])

		select_list = selector.xpath(zhihu_user.sex_rule)
		if len(select_list) == 0:
			select_list = ['']
		zhihu_user['sex'] = ''.join(select_list[0]).replace("icon icon-profile-","")
		
		select_list = selector.xpath(zhihu_user.description_rule)
		if len(select_list) == 0:
			select_list = ['']
		zhihu_user['description'] = ''.join(select_list[0]).strip().replace("\n",'')
		
		select_list = selector.xpath(zhihu_user.view_num_rule)
		if len(select_list) == 0:
			select_list = ['']
		zhihu_user['view_num'] = ''.join(select_list[0])
		
		zhihu_user['update_time'] = str(datetime.now())
		
		zhihu_user['jobs'] = []
		jobs_list = selector.xpath(zhihu_user.jobs_rule)
		for job in jobs_list:
			company = ''.join(job.xpath('@data-title')[0])
			title = ''.join(job.xpath('@data-sub-title')[0])
			zhihu_user['jobs'].append({'company': company, 'title':title})

		zhihu_user['educations'] = []
		edu_list = selector.xpath(zhihu_user.educations_rule)
		for edu in edu_list:
			school = ''.join(edu.xpath('@data-title')[0])
			major = ''.join(edu.xpath('@data-sub-title')[0])
			zhihu_user['educations'].append({'school':school, 'major':major})

		zhihu_user['sinaweibo'] = ''
		zhihu_user['tencentweibo'] = ''
		for node in selector.xpath("//a[@class='zm-profile-header-user-weibo']/@href"):
			if node.startswith('http://weibo.com'):
				zhihu_user['sinaweibo'] = node
			elif node.startswith('http://t.qq.com'):
				zhihu_user['tencentweibo'] = node
		
		statistics = selector.xpath(zhihu_user.statistics_follow_rule)
		if len(statistics) < 2:
			statistics = ["0", "0"]
		followee_num = zhihu_user['followee_num'] = statistics[0]
		follower_num = zhihu_user['follower_num'] = statistics[1]

		statistics = selector.xpath(zhihu_user.statistics_other_rule)
		if len(statistics) < 4:
			statistics = ["0", "0", "0", "0"]
		zhihu_user['agree_num'] = statistics[0]
		zhihu_user['thank_num'] = statistics[1]
		zhihu_user['fav_num'] = statistics[2]
		zhihu_user['share_num'] = statistics[3]

		statistics = selector.xpath("//div[@class='profile-navbar clearfix']/a/span/text()")
		if len(statistics) < 6:
			statistics = ["0", "0", "0", "0", "0", "0"]
		zhihu_user['ask_num'] = statistics[1]
		zhihu_user['answer_num'] = statistics[2]
		zhihu_user['post_num'] = statistics[3]
		zhihu_user['collection_num'] = statistics[4]
		zhihu_user['log_num'] = statistics[5]

		select_list = selector.xpath(zhihu_user.img_rule)
		if len(select_list) == 0:
			select_list = [""]
		zhihu_user['img'] = self._get_xl_img(''.join(select_list[0]))
		#save the img
		self._download_img(zhihu_user['img'], zhihu_user['_id'], IMG_FOLDER)

		print '['+self._now_time+']'+' '+"[depth = "+str(depth)+"]"+' '+'get user:' + zhihu_user['_id'] + ' info!'

		'''
		#just test
		a = zhihu_user['nickname']
		b = zhihu_user['nickname'].encode('utf-8')
		c = zhihu_user['nickname'].decode('unicode-escape')
		print type(a), type(b), type(c)
		return
		'''

		if self._dead_zhihu_user(zhihu_user):
			print '['+self._now_time+']'+' '+"[depth = "+str(depth)+"]"+' '+'bi~bi~bi~~~user:' + zhihu_user['_id'] + ' maybe dead user...'
			return 
		
		#one user is ok
		save_user = self.save_zhihu_user(zhihu_user)
		if save_user:
			print '['+self._now_time+']'+' '+"[depth = "+str(depth)+"]"+' '+'save user:' + zhihu_user['_id'] + ' to mongod! It\'s done! '
		else:
			print '['+self._now_time+']'+' '+"[depth = "+str(depth)+"]"+' '+'canot save user:' + zhihu_user['_id'] + ' to mongod successfully...'
		
		if depth > MAX_DEPTH:
			return 
			
		'''
		num = int(followee_num) if followee_num else 0
		page_num = num / 20
		page_num += 1 if num % 20 else 0
		for i in xrange(page_num):
			response, soup = ZhihuCommon.get('https://www.zhihu.com/people/'+zhihu_user['_id']+'/followees')
			self.parse_follow_url(response, soup)

		num = int(follower_num) if follower_num else 0
		page_num = num / 20
		page_num += 1 if num % 20 else 0
		for i in xrange(page_num):
			response, soup = ZhihuCommon.get('https://www.zhihu.com/people/'+zhihu_user['_id']+'/followers')
			self.parse_follow_url(response, soup)
		'''
		response, soup = ZhihuCommon.get('https://www.zhihu.com/people/'+zhihu_user['_id']+'/followers')
		self.parse_follow_url(response, soup, depth)
		print '['+self._now_time+']'+' '+"[depth = "+str(depth)+"]"+' '+'user:'+zhihu_user['_id']+' \'s all follow had been parsed!'
		return

	def parse_follow_url(self, response, soup, depth):
		selector = etree.HTML(str(soup))
		for link in selector.xpath('//div[@class="zm-list-content-medium"]/h2/a/@href'):
			#link  ===> http://www.zhihu.com/people/...
			username_tmp = link.split('/')[-1]
			if self.mgd.find_item(username_tmp) == 0:
				print '\n['+self._now_time+']'+' '+"[depth = "+str(depth)+"]"+' '+"start parse user:" + username_tmp + '...'
				response, soup = ZhihuCommon.get("https://www.zhihu.com/people/"+username_tmp+"/about")
				self.parse_zhihu_user(response, soup, depth+1)

	def save_zhihu_user(self, zhihu_user):
		print '['+self._now_time+']'+' '+'start record the user ', zhihu_user['_id']
		if isinstance(zhihu_user, ZhihuUserItem):
			if isinstance(self.mgd, MongoDBPipeline):
				self.mgd.process_item(zhihu_user)
				return True
			else:
				print '['+self._now_time+']'+' '+"mgd is err............."
		else:
			print '['+self._now_time+']'+' '+'zhihu_user item err.............'
		return False

	def _dead_zhihu_user(self, zhihu_user):
		if zhihu_user['_id']:
			if int(zhihu_user['followee_num']) == 0 or int(zhihu_user['follower_num']) == 0:
				return True
			if int(zhihu_user['agree_num']) == 0:
				return True
			return False
		else:
			return False

	def _get_xl_img(self, img_url):
		#https://pic4.zhimg.com/db444fc1609c86ec6b650b7f61dfa2ef_s.jpg
		#https://pic4.zhimg.com/db444fc1609c86ec6b650b7f61dfa2ef_l.jpg
		#to
		#https://pic4.zhimg.com/db444fc1609c86ec6b650b7f61dfa2ef_xl.jpg
		_pos = img_url.find('_')
		if _pos < 0:
			print 'the img:'+img_url+' dont exist xlarge img...'
			return img_url
		return img_url[:_pos+1] + 'xl.jpg'

	def _download_img(self, url, save_img_name, save_img_place):
		print '['+self._now_time+']'+' '+' the imgurl is ' + url
		img =  requests.get(url, stream=True)
		with open(save_img_place+'/'+save_img_name+'.jpg', 'wb') as fw:
			for chunk in img.iter_content():
				fw.write(chunk)

	def _encode_zhihu_user_info(self, zhihu_user):
		zhihu_user['username'] = zhihu_user['username'].encode('ISO 8859-1')
		zhihu_user['nickname'] = zhihu_user['nickname'].encode('ISO 8859-1')
		zhihu_user['location'] = zhihu_user['location'].encode('ISO 8859-1')
		zhihu_user['industry'] = zhihu_user['industry'].encode('ISO 8859-1')
		zhihu_user['description'] = zhihu_user['description'].encode('ISO 8859-1')
		temp_list = []
		for item in zhihu_user['jobs']:
			item['company'] = item['company'].encode('ISO 8859-1')
			item['title'] = item['title'].encode('ISO 8859-1')
			temp_list.append(item)
		zhihu_user['jobs'] = temp_list
		temp_list = []
		for item in zhihu_user['educations']:
			item['school'] = item['school'].encode('ISO 8859-1')
			item['major'] = item['major'].encode('ISO 8859-1')
			temp_list.append(item)
		zhihu_user['educations'] = temp_list
		return zhihu_user
			
if __name__ == '__main__':
	zhc = ZhihuUserCrawler()

	login_flag = zhc.login()

	if login_flag:
		time.sleep(SLEEP_TIME)
		zhc.start_parse("")
	print '['+zhc._now_time+']'+' '+'over......................................'