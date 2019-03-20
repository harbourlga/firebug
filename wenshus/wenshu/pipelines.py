# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymysql

class WenshuPipeline(object):
    def __init__(self):
        self.conn = pymysql.connect(host='127.0.0.1',
                           port=3307,
                           user='root',
                           password='zxc123456',
                           database='wenshu',
                           charset="utf8")
        self.cursor = self.conn.cursor()

    def process_item(self, item, spider):
        insert_sql = """insert into wenshu_test(caseId, caseNum, caseName, judical, caseType, countName, decideTime, content)
                                values (%s, %s, %s, %s, %s, %s, %s, %s)"""
        self.cursor.execute(insert_sql, (item["case_Id"], item["case_Num"], item["case_name"], item["judicial_process"],item["case_type"], item["count_name"], item["decide_time"], item["content"]))
        self.conn.commit()

    def close_spider(self, spider):
        self.cursor.close()
        self.conn.close()
