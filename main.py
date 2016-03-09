from setting import *

from zhihu_user_crawler import ZhihuUserCrawler

import logging, time
import thread, threading
from Queue import Queue

import zhihu_user_queue


#thread_local = threading.local()
#thread_local.user_id_queue = Queue()
mylock_queue = thread.allocate_lock()


class MyThread(threading.Thread):

	def __init__(self, target, thread_id):
		#father class
		super(MyThread, self).__init__()
		self.target = target
		self.thread_id = thread_id

	def run(self):
		self.target(self.thread_id)


def spider_thread(thread_id):
	if zhihu_user_queue.q_size() > 0:
		start_user_id = zhihu_user_queue.get_user()
		print 'thread_id:'+str(thread_id)+' queue size = ', zhihu_user_queue.q_size()
		zhc = ZhihuUserCrawler()
		print '['+zhc._now_time()+']'+'thread_id:'+str(thread_id)+' start...'
		#login_flag = zhc.login()
		#if login_flag:
		zhc.start_parse("https://www.zhihu.com/people/"+start_user_id+"/about", thread_id)
		print '['+zhc._now_time()+']'+'thread_id:'+str(thread_id)+' over...\n'
		
def setting_test():
	if EMAIL == '' or PASSWORD == '':
		print 'ERROR:email or pwd in setting.py is null...'
		return False
	if ACCESS_KEY == '' or SECRET_KEY == '' or BUCKET_NAME == '':
		print "ERROR:access_key or secret_key or bucket_name in setting.py is null..."
		print "if you dont want to upload pics to QiniuCloud, you should set upload_flag = False"
		return False
	return True


if __name__ == '__main__':

	if setting_test() == False:
		exit()
	
	zhihu_user_queue.put_user('xxx0624')
	zhihu_user_queue.put_user('zihaolucky')
	zhihu_user_queue.put_user('gao-tian-50')
	zhihu_user_queue.put_user('YLongJimmy')

	cur_cnt_thread = 0
	thread_list = []

	print 'start zhihu user crawl ....'

	zhc = ZhihuUserCrawler()
	login_flag = zhc.login()
	if login_flag == True:

		for i in range(THREADS_NUM):
			my_thread = MyThread(spider_thread, cur_cnt_thread)			
			cur_cnt_thread += 1
			thread_list.append(my_thread)

		
		for item in thread_list:
			item.start()
			time.sleep(10)
			
		for item in thread_list:
			item.join()

	print 'all work finished............'
