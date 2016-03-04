# -*- coding:utf-8 -*-

from scrapy.item import Item, Field

class ZhihuUserItem(Item):
	_id = Field()
	url = Field()
	img = Field()
	img_rule = [
		'//div[@class="zm-profile-header-avatar-container "]/img[@class="Avatar Avatar--l"]/@src',
		'//div[@class="top-nav-profile"]/img[@class="Avatar"]/@src'
	]
	username = Field()
	nickname = Field()
	nickname_rule = "//div[@class='title-section ellipsis']/a[@class='name']/text()"
	location = Field()
	location_rule = "//span[@class='location item']/@title"
	industry = Field()
	industry_rule = "//span[@class='business item']/@title"
	sex = Field()
	sex_rule = '//div[@class="item editable-group"]/span/span[@class="item gender"]/i/@class'
	jobs = Field()
	jobs_rule = '//div[@class="zm-profile-module zg-clear"][1]/div/ul[@class="zm-profile-details-items"]/li'
	educations = Field()
	educations_rule = '//div[@class="zm-profile-module zg-clear"][3]/div/ul[@class="zm-profile-details-items"]/li'
	description = Field()
	description_rule = "//span[@class='description unfold-item']/span/text()"
	sinaweibo = Field()
	tencentweibo = Field()

	followee_num = Field()
	follower_num = Field()
	statistics_follow_rule = "//a[@class='item']/strong/text()"

	ask_num = Field()
	answer_num = Field()
	post_num = Field()
	collection_num = Field()
	log_num = Field()
	
	agree_num = Field()
	thank_num = Field()
	fav_num = Field()
	share_num = Field()
	statistics_other_rule = "//div[@class='zm-profile-module-desc']/span/strong/text()"

	view_num = Field()
	view_num_rule = "//span[@class='zg-gray-normal']/strong/text()"
	update_time = Field()

class ZhihuAskItem(Item):
	_id = Field()
	username = Field()
	url= Field()
	view_num = Field()
	title = Field()
	answer_num = Field()
	follower_num = Field()

class ZhihuAnswerItem(Item):
	_id = Field()
	username = Field()
	url = Field()
	ask_title = Field()
	ask_url = Field()
	agree_num = Field()
	summary = Field()
	content = Field()
	comment_num = Field()

class ZhihuFolloweesItem(Item):
	_id = Field()
	username = Field()
	followees = Field()

class ZhihuFollowersItem(Item):
	_id = Field()
	username = Field()
	followers = Field()