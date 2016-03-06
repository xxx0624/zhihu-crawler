from items import *
from setting import *

import json

from pymongo import MongoClient
from datetime import datetime


class MongoDBPipeline(object):
	def __init__(self):
		self.client = MongoClient(MONGODB_IP, MONGODB_PORT)
		self.db = self.client["zhihu_multhread"]
		self.zh_user_col = self.db["zh_user"]
		self._now_time = str(datetime.strptime(str(datetime.today()), "%Y-%m-%d %H:%M:%S.%f"))

		'''
		self.zh_ask_col = self.db["zh_ask"]
		self.zh_answer_col = self.db["zh_answer"]
		self.zh_followee_col = self.db["zh_followee"]
		self.zh_follower_col = self.db["zh_follower"]

		self.gh_user_col = self.db["gh_user"]
		self.om_user_col = self.db["om_user"]
		self.gh_repo_col = self.db["gh_repo"]
		'''

	def saveOrUpdate(self, collection, item):
		_id= dict(item).get("_id")
		if _id is not None:
			try:
				tmp = collection.find_one({"_id":_id})
			except Exception as e:
				self.client.close()
				self.client = MongoClient(MONGODB_IP, MONGODB_PORT)
				self.db = self.client["zhihu"]
				self.zh_user_col = self.db["zh_user"]
				print '['+self._now_time+']'+' id find error...'
			#id not exitst
			if tmp is None:
				try:
					collection.insert(dict(item))
				except Exception as e:
					self.client.close()
					self.client = MongoClient(MONGODB_IP, MONGODB_PORT)
					self.db = self.client["zhihu"]
					self.zh_user_col = self.db["zh_user"]
					try:
						collection.insert(dict(item))
					except Exception as e:
						print '['+self._now_time+']'+' ignore the user ' + item['_id']
			else:
				try:
					collection.update({"_id":_id}, dict(item))
				except Exception as e:
					self.client.close()
					self.client = MongoClient(MONGODB_IP, MONGODB_PORT)
					self.db = self.client["zhihu"]
					self.zh_user_col = self.db["zh_user"]
					try:
						collection.update({"_id":_id}, dict(item))
					except Exception as e:
						print '['+self._now_time+']'+' ignore the user ' + item['_id']
		else:
			pass

	def find_item(self, user_id):
		if user_id is None:
			#print 'the user '+user_id+' is None...'
			return -1
		try:
			tmp = self.zh_user_col.find_one({"_id":user_id})
			if tmp is None:
				#user not exist
				#print 'the user '+user_id+' is None, cannot find it in mongodb...'
				return -1
			else:
				#0 not in queue(follow url is ok)
				#1 crawl finish
				#2 in queue // TO DO
				return self.zh_user_col.find({"_id":user_id})[0]['crawl_finish']
		except Exception as e:
			self.client.close()
			self.client = MongoClient(MONGODB_IP, MONGODB_PORT)
			self.db = self.client["zhihu"]
			self.zh_user_col = self.db["zh_user"]
			print '['+self._now_time+']'+' user_id find error...'
			#special case
			return -2

	def process_item(self, item):
		if isinstance(item, ZhihuUserItem):
			self.saveOrUpdate(self.zh_user_col, item)

		elif isinstance(item, ZhihuAskItem):
			self.saveOrUpdate(self.zh_ask_col, item)

		elif isinstance(item, ZhihuFollowersItem):
			self.saveOrUpdate(self.zh_follower_col, item)

		elif isinstance(item, ZhihuFolloweesItem):
			self.saveOrUpdate(self.zh_followee_col, item)

		elif isinstance(item, ZhihuAnswerItem):
			self.saveOrUpdate(self.zh_answer_col, item)

		elif isinstance(item, GithubUserItem):
			self.saveOrUpdate(self.gh_user_col, item)

		elif isinstance(item, OutofmemoryUserItem):
			self.saveOrUpdate(self.om_user_col, item)

		elif isinstance(item, GithubRepoItem):
			self.saveOrUpdate(self.gh_repo_col, item)

		return item