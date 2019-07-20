# -*- coding: utf-8 -*-
# @Author       :junjie    
# @Time         :2019/7/16 20:16
# @FileName     :wechat_spider.py
#IDE            :PyCharm
import requests
import json
import time
import random
# import pdfkit
from public.get_database import getDatabase
import pymysql
from config.config import *
test = getDatabase(local_config)
def get_wx_data(biz,uin,key,next_offset):
    params = {
        '__biz': biz,
        'uin': uin,
        'key': key,
        'offset':next_offset,
        'count':10,
        'action': 'getmsg',
        'f': 'json'
    }
    headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.116 Safari/537.36 QBCore/3.53.1159.400 QQBrowser/9.0.2524.400 Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36 MicroMessenger/6.5.2.501 NetType/WIFI WindowsWechat'
        }
    url='http://mp.weixin.qq.com/mp/profile_ext'
    re=requests.get(url,params=params,headers=headers)
    data=re.json()
    if data.get('errmsg')=='ok':
        data = re.json()
        can_msg_continue = data['can_msg_continue']
        general_msg_list = json.loads(data['general_msg_list'])
        list = general_msg_list.get('list')
        offset=data['next_offset']
        test.updata('wx_config','id',1,next_offset=offset)
        for i in list:
            if 'app_msg_ext_info' in i.keys():
                app_msg_ext_info=i['app_msg_ext_info']
                title=app_msg_ext_info['title']    #文章标题
                url=app_msg_ext_info['content_url'] #文章链接
                is_multi=app_msg_ext_info['is_multi'] #是否一次推送多条信息
                # cover=app_msg_ext_info['cover'] #封面url
                datetime = i['comm_msg_info']['datetime'] #发布时间
                datetime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(datetime))
                test.insert('wx_article', wx_title=title, wx_url=url,time=datetime,wx_id=biz)
                if is_multi==1:
                    for ll in app_msg_ext_info['multi_app_msg_item_list']:
                        print(ll['title'])
                        print(ll['content_url'])
                        test.insert('wx_article', wx_title=ll['title'], wx_url=ll['content_url'],time=datetime,wx_id=biz)
            else:
                data=i['comm_msg_info']
                print(data)
        if can_msg_continue==1:
            return True
        return False
    else:
        print('获取文章异常')
# name='aifou1.pdf'
# url='https://mp.weixin.qq.com/s?__biz=MjM5NzE1NTMyNg==&amp;mid=2650929551&amp;idx=1&amp;sn=30de26b5ab026c1bf314de41a89d99aa&amp;chksm=bd2b011e8a5c880814eb02d677dd7e0456b11abb31d8d84a1972e81f9756ed394f580d464814&amp;scene=27#wechat_redirect'
# config=pdfkit.configuration(wkhtmltopdf=r"C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe")
# pdfkit.from_url(url, name,configuration=config)
if __name__ == '__main__':
    test = getDatabase(local_config)
    data=test.select('wx_config',id=1)[0]
    uin='OTIzODk5MjYw'
    biz=data['wx_biz']
    key='c8b1cdfc5f2a0a52ec96de1937c3edb517aafe5e23725a8c342dd4f906ec2ca8b0a9590366905919baf324244fce6f70c40a46356a5de1880bec74bc5a6ef50aadbc4d8f4966c2ea22fab256d5603c6d'
    index=0
    while 1:
        print(f'********开始抓取公众号第{index + 1}页文章********')
        data = test.select('wx_config', id=1)[0]
        next_offset = data['next_offset']
        is_continue=get_wx_data(biz=biz,uin=uin,key=key,next_offset=next_offset)
        # 防止和谐，暂停8秒
        time.sleep(8)
        index += 1
        if not is_continue:
            print('公众号文章已全部抓取完毕，退出程序.')
            break
        print(f'********准备抓取公众号第{index+1}页文章********')

