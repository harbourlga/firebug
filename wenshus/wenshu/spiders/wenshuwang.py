# -*- coding: utf-8 -*-
import scrapy
import uuid
from wenshu.items import WenshuItem
import tools

class get_vjkl5(scrapy.Spider):
    name = 'start'

    def start_requests(self):
        urls = 'http://wenshu.court.gov.cn/list/list/?sorttype=1&number=XDKS8C5F&guid=b08dce9b-2c0e-b3a23b8f-1abffd6b0059'
        num = 1
        return [scrapy.Request(url=urls,meta = {'num':num}, callback=self.parse, dont_filter=True)]

    def parse(self, response):
         import requests
         import uuid
         import time
         num = response.meta['num']
         print('num:{}'.format(num))
         Cookies =  response.headers.getlist('Set-Cookie')
         print('cookies:{}'.format(Cookies))
         cookie_str = Cookies[0]
         vjkl5 = str(cookie_str).split('vjkl5=')[1]
         vjkl5 = vjkl5.split(';')[0]
         print('vjkl5:{}'.format(vjkl5))
         try:
             vl5x = tools.create_vl5x(vjkl5)
         except:
             time.sleep(3)
             url_back = 'http://wenshu.court.gov.cn/list/list/?sorttype=1&number=XDKS8C5F&guid=b08dce9b-2c0e-b3a23b8f-1abffd6b0059'
             yield scrapy.Request(url = url_back, meta = {'num':num}, callback=self.parse, dont_filter=True)

         time.sleep(1)
         print('vl5x:{}'.format(vl5x))
         headers = {
              # 'Accept': '*/*',
              # 'Accept-Encoding': 'gzip, deflate',
              # 'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
              # 'Connection': 'keep-alive',
              # 'Host': 'wenshu.court.gov.cn',
              # 'Referer': 'http://wenshu.court.gov.cn/list/list/?sorttype=1&number=&guid=fc1f7422-24e5-7f618641-26b93458a4e6&conditions=searchWord+QWJS+++%E5%85%A8%E6%96%87%E6%A3%80%E7%B4%A2:%E6%B7%B1%E5%9C%B3',
              # 'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:57.0) Gecko/20100101 Firefox/57.0',
              # 'X-Requested-With': 'XMLHttpRequest',
              # 'Content-Length': '222',
              'Content-Type':'application/x-www-form-urlencoded; charset=UTF-8',
              'Cookie': str('_gscu_125736681=23411255r26gs182; Hm_lvt_9e03c161142422698f5b0d82bf699727=1530776352; _gscu_2116842793=234111808ot84931; Hm_lvt_3f1a54c5a86d62407544d433f6418ef5=1530776414; Hm_lvt_d2caefee2de09b8a6ea438d74fd98db2=1532306860,1532337560,1532505883,1533102684; XDEBUG_SESSION=XDEBUG_ECLIPSE; Hm_lpvt_d2caefee2de09b8a6ea438d74fd98db2=1533103127; _gscs_2116842793=33102683dp26z254|pv:4; _gscbrs_2116842793=1; vjkl5=' + vjkl5),
         }
         guid = uuid.uuid4()
         try:
             number = tools.create_number(guid)
             try:
                 test = {'num':str(number)}
             except:
                 guid = uuid.uuid4()
                 number = tools.create_number(guid)

         except:
             url_back = 'http://wenshu.court.gov.cn/list/list/?sorttype=1&number=XDKS8C5F&guid=b08dce9b-2c0e-b3a23b8f-1abffd6b0059'
             yield scrapy.Request(url = url_back, meta = {'num':num}, callback=self.parse, dont_filter=True)

         print('guid:{}'.format(guid))
         post_data = {'Param':'全文检索:深圳',
                 'Index':str(num),
                 'Page':'5',
                 'Order':'法院层级',
                 'Direction':'asc',
                 'vl5x':str(vl5x),
                 'number':str(number),
                 'guid':str(guid),
            }
         print('post_data:{}'.format(post_data))
         print('headers:{}'.format(headers))
         time.sleep(3)
         yield scrapy.FormRequest(url = 'http://wenshu.court.gov.cn/List/ListContent', method = "post", formdata = post_data, headers = headers,
                                  meta = {'num' : num}, callback = self.after_post, dont_filter=True)
         # print(response.meta)

    def after_post(self, response):
         from wenshu.items import WenshuItem
         import json
         import time
         item = WenshuItem()
         response_next=response.body
         response_next = response_next.replace("\\", '')
         response_next = response_next[1:]
         response_next = response_next[:-1]
         print('test:{}'.format(response_next[0:200]))
         try:
             data = json.loads(response_next) #return
         except:
             time.sleep(3)
             url_back = 'http://wenshu.court.gov.cn/list/list/?sorttype=1&number=XDKS8C5F&guid=b08dce9b-2c0e-b3a23b8f-1abffd6b0059'
             yield scrapy.Request(url = url_back, meta = {'num':response.meta['num']}, callback=self.parse, dont_filter=True)
         for var in range(1,len(data)):
              try:
                  item['case_name'] = data[var][u'\u6848\u4ef6\u540d\u79f0']
              except:
                  item['case_name'] = 'Null'
              item['case_type'] = data[var][u'\u6848\u4ef6\u7c7b\u578b']
              item['count_name'] = data[var][u'\u6cd5\u9662\u540d\u79f0']
              try:
                  item['judicial_process'] = data[var][u'\u5ba1\u5224\u7a0b\u5e8f']
              except:
                  item['judicial_process'] = 'Null'
              item['case_Id'] = data[var][u'\u6587\u4e66ID']
              item['case_Num'] = data[var][u'\u6848\u53f7']
              try:
                  item['content'] = data[var][u'\u88c1\u5224\u8981\u65e8\u6bb5\u539f\u6587']
              except:
                  item['content'] = 'Null'
              item['decide_time'] = data[var][u'\u88c1\u5224\u65e5\u671f']
              yield item

         num = response.meta['num']+1 #传回parse,翻到下一页
         if num <100:
            url_back = 'http://wenshu.court.gov.cn/list/list/?sorttype=1&number=XDKS8C5F&guid=b08dce9b-2c0e-b3a23b8f-1abffd6b0059'
            yield scrapy.Request(url = url_back, meta={'num':num}, callback=self.parse, dont_filter=True)