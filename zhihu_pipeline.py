from items import *
from setting import *

import json

from pymongo import MongoClient

class MongoDBPipeline(object):
	def __init__(self):
		client = MongoClient(MONGODB_IP, MONGODB_PORT)
		self.db = client["zhihu"]
		self.zh_user_col = self.db["zh_user"]
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
			tmp = collection.find_one({"_id":_id})
			#id not exitst
			if tmp is None:
				try:
					collection.insert(dict(item))
				except Exception as e:
					self.client = MongoClient(MONGODB_IP, MONGODB_PORT)
					self.db = client["zhihu"]
					self.zh_user_col = self.db["zh_user"]
					collection.insert(dict(item))
			else:
				try:
					collection.update({"_id":_id}, dict(item))
				except Exception as e:
					self.client = MongoClient(MONGODB_IP, MONGODB_PORT)
					self.db = client["zhihu"]
					self.zh_user_col = self.db["zh_user"]
					collection.update({"_id":_id}, dict(item))
		else:
			pass

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