# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy import Field


class AlibbItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


class SupItem(scrapy.Item):
    #关键字
    word = Field()
    #店铺地址
    website = Field()
    #姓名
    name = Field()
    #公司名
    company = Field()
    #手机
    mobile = Field()
    #电话
    tel = Field()
    #星级
    level = Field()
    #诚信通
    honest = Field()
    #成立时间
    buildDate = Field()
    #注册资本
    money = Field()
    #经营范围
    area = Field()
    #经营地址
    address = Field()
    #累计成交数
    successCount = Field()
    lastOneWeek = Field()
    lastOneMonth = Field()
    lastSixMonth = Field()
    beforeHalfYear = Field()
    total = Field()

