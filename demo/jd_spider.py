# -*- coding: utf-8 -*-
# @Author       :junjie    
# @Time         :2019/7/13 15:02
# @FileName     :jd_spider.py
#IDE            :PyCharm
import requests
import json
from public.get_database import getDatabase
import random
import time
from config.config import *
test = getDatabase(local_config)
def jd_spider(page=0):
    url='https://sclub.jd.com/comment/productPageComments.action?callback='\
        'fetchJSON_comment98vv4993&productId=1263013576&score=0&sortType=5&page=%s&pageSize=10&isShadowSku=0&fold=1'% page
    header={'user-agent': 'Mozilla/5.0', 'Referer': 'https://item.jd.com/1263013576.html'}
    re=requests.get(url,headers=header)
    json_str=re.text[26:-2]
    json_obj = json.loads(json_str)
    for i in json_obj['comments']:
        test.insert('jd_comment', comment=i['content'], comment_id=str(i['id']))
if __name__ == '__main__':
    for i in range(5):
        jd_spider(i)
        time.sleep(random.random() * 5)
        print(random.random())
    print('爬取成功')

