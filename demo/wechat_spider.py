# -*- coding: utf-8 -*-
# @Author       :junjie
# @Time         :2019/7/16 20:16
# @FileName     :wechat_spider.py
#IDE            :PyCharm
import requests
import json
import time
# import pdfkit
from public.get_database import getDatabase
from config.config import *
test = getDatabase(local_config)
next_offset = 0


def get_wx_data(biz, uin, key):
    global next_offset
    params = {
        '__biz': biz,
        'uin': uin,
        'key': key,
        'offset': next_offset,
        'count': 10,
        'action': 'getmsg',
        'f': 'json'
    }
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.116 Safari/537.36 QBCore/3.53.1159.400 QQBrowser/9.0.2524.400 Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36 MicroMessenger/6.5.2.501 NetType/WIFI WindowsWechat'
    }
    url = 'http://mp.weixin.qq.com/mp/profile_ext'
    re = requests.get(url, params=params, headers=headers)
    data = re.json()
    if data.get('errmsg') == 'ok':
        data = re.json()
        can_msg_continue = data['can_msg_continue']
        general_msg_list = json.loads(data['general_msg_list'])
        list = general_msg_list.get('list')
        offset = data['next_offset']
        next_offset = offset
        for i in list:
            if 'app_msg_ext_info' in i.keys():
                app_msg_ext_info = i['app_msg_ext_info']
                title = app_msg_ext_info['title']  # 文章标题
                url = app_msg_ext_info['content_url']  # 文章链接
                is_multi = app_msg_ext_info['is_multi']  # 是否一次推送多条信息
                # cover=app_msg_ext_info['cover'] #封面url
                datetime = i['comm_msg_info']['datetime']  # 发布时间
                datetime = time.strftime(
                    "%Y-%m-%d %H:%M:%S", time.localtime(datetime))
                test.insert(
                    'wx_article',
                    wx_title=title,
                    wx_url=url,
                    time=datetime,
                    wx_id=biz)
                if is_multi == 1:
                    for ll in app_msg_ext_info['multi_app_msg_item_list']:
                        print(ll['title'])
                        print(ll['content_url'])
                        test.insert(
                            'wx_article',
                            wx_title=ll['title'],
                            wx_url=ll['content_url'],
                            time=datetime,
                            wx_id=biz)
            else:
                data = i['comm_msg_info']
                print(data)
        if can_msg_continue == 1:
            return True
        return False
    else:
        print('获取文章异常')


if __name__ == '__main__':
    test = getDatabase(local_config)
    data = test.select_one('wx_config', id=2)
    uin = 'OTIzODk5MjYw'
    biz = data['wx_biz']
    key = '83859d964d99afb4632d51b1d7e113244e79ff25cd886812b1b09acd6f514f93ce2ed3689b3399772ab054729dac6c9ab0475f3c4c89d11afd93ca972afeed6ba5f9effc991a915c1ab6fc1d6b75a0e5'
    index = 0
    while True:
        print(f'********开始抓取公众号第{index + 1}页文章********')
        is_continue = get_wx_data(biz=biz, uin=uin, key=key)
        # 防止和谐，暂停8秒
        time.sleep(8)
        index += 1
        if not is_continue:
            print('公众号文章已全部抓取完毕，退出程序.')
            break
        print(f'********准备抓取公众号第{index+1}页文章********')
