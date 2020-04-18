# -*- coding: utf-8 -*-
# @Author       :junjie    
# @Time         :2020/4/14 16:27
# @FileName     :manhua.py
# @Motto        :AS the tree,so the fruit
#IDE            :PyCharm

import requests
import re
from lxml import html
import os
from urllib import parse
import random
import time
headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': "zh-CN,zh;q=0.9",
        'Cache-Control': 'no-cache',
        'Connection': 'keep-alive',
        'Host': 'comic2.kukudm.com',
        'Pragma': 'no-cache',
        'Cookie': '__cfduid=d494a7f633a8cdd0a71a5eafb9787940e1586837414; Hm_lvt_75aea7db257a7d18f20c6c4204622a78=1586832717,1586878298; Hm_lpvt_75aea7db257a7d18f20c6c4204622a78=1586946687',
        'Upgrade-Insecure-Requests': "1",
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36'
    }

#获取漫画目录
def catalog():
    num = 0
    url = "http://comic2.kukudm.com/comiclist/2126/index.htm"
    data = requests.get(url=url, headers=headers)
    data.encoding = 'gbk'
    li_list = html.etree.HTML(data.text).xpath('//*[@id="comiclistn"]')
    data = li_list[0]
    k = []
    v = []
    for i in data.xpath('//*[@id="comiclistn"]/dd'):
        num += 1
        d = i.xpath(f'//*[@id="comiclistn"]/dd[{num}]/a[3]')[0]
        e=i.xpath(f'//*[@id="comiclistn"]/dd[{num}]/a[1]')[0]
        result = html.etree.tostring(d, encoding='utf-8')
        a = re.findall('<a href="(.+?)"', result.decode('utf-8'))
        result1 = html.etree.tostring(e, encoding="utf-8", pretty_print=True, method="html")
        title = re.findall('>(.+?)</a> ', result1.decode())
        k.append(title[0])
        v.append(a[0][0:-5])
    d = dict(zip(k, v))
    return d


#获取对应话的图片地址
def index_url(url):
    list1=[]
    num = 1
    while True:
        new_url=url+str(num)+'.htm'
        # 防止请求频繁
        time.sleep(random.random() * 5)
        data = requests.get(url=new_url, headers=headers)
        data.encoding = 'gbk'
        num+=1
        image_url = re.findall("newkuku(.+?)'>", data.text)[0]
        index = re.findall("共(.+?)页", data.text)[0]
        list1.append(image_url)
        if num > int(index):
            break
    return list1


#下载图片
def down_load(content, file_name,image_name):
    with open("./鬼灭之刃/{}/{}.jpg".format(file_name,image_name), "wb") as f:
        f.write(content)
    print("成功下载:{},{}".format(file_name,image_name))


#主程序
def main():
    new_data = catalog()
    for file_name in os.listdir('./鬼灭之刃'):
        if os.path.isdir(f"./鬼灭之刃/{file_name}"):
            #避免不可描述原因，要从第一话重新下载。
            del new_data[file_name]
    for k,v in new_data.items():
        index = 1
        if not os.path.isdir(f"./鬼灭之刃/{k}/"):
            os.mkdir(f"./鬼灭之刃/{k}/")
        for a in index_url(v):
            string1=parse.quote(a)
            url2 = 'http://v2.kukudm.com/newkuku' + string1
            # 防止请求频繁
            time.sleep(random.random() * 5)
            data = requests.get(url=url2, stream=True)
            down_load(data.content, k, index)
            index += 1
if __name__ == '__main__':
    main()

