# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class WenshuItem(scrapy.Item):
    # define the fields for your item here like:
    content = scrapy.Field()  #裁判要旨段原文
    case_type = scrapy.Field()   #案件类型
    decide_time = scrapy.Field()    #裁判日期
    case_name = scrapy.Field()   #案件名称
    case_Id = scrapy.Field()   #文书ID
    judicial_process = scrapy.Field()   #审判程序
    case_Num = scrapy.Field()   #案号
    count_name = scrapy.Field()    #法院名称
    pass
