# -*- coding: utf-8 -*-
# @Author       :junjie
# @Time         :2020/5/14 16:30
# @FileName     :meinv.py
# @Motto        :AS the tree,so the fruit
#IDE            :PyCharm

import os
import requests
from lxml import etree


class Work(object):
    headers = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36"
    }

    def run(self):
        page = 1
        while page <= 10:
            url = f"https://mm.enterdesk.com/dalumeinv/{page}.html"
            response = requests.get(url=url, headers=self.headers).content.decode()
            div_list = etree.HTML(response).xpath('//div[@class="egeli_pic_li"]')
            for div in div_list:
                html_url = div.xpath('./dl/dd/a/@href')[0]
                title = div.xpath('./dl/dd/a/img/@title')[0]
                self.download_image(html_url, title)
            page += 1

    def download_image(self, html_url, title):
        # 创建相应的文件夹
        if not os.path.isdir(f"./files/{title}"):
            os.mkdir(f"./files/{title}")
        response = requests.get(url=html_url, headers=self.headers).content.decode()
        img_list = etree.HTML(response).xpath('//div[@class="swiper-wrapper"]/div/a/@src')
        for img_url in img_list:
            img_content = requests.get(url=img_url, headers=self.headers).content
            img_name = img_url.split("/")[-1]
            print(f"正在下载：{title}， {img_name}")
            with open(f"./files/{title}/{img_name}", "wb") as f:
                f.write(img_content)


if __name__ == '__main__':
    if not os.path.isdir(f"./files/"):
        os.mkdir(f"./files/")
    work = Work()
    work.run()
