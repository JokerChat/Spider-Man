# -*- coding: utf-8 -*-
# @Author       :junjie
# @Time         :2019/7/16 15:24
# @FileName     :meizi.py
#IDE            :PyCharm
from lxml import html
import requests
import os


def run(page):
    url = "https://www.mzitu.com/page/{}/".format(page)
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome"
                      "/71.0.3578.98 Safari/537.36",
        "Referer": "https://www.mzitu.com/"
    }

    response = requests.get(url=url, headers=headers).content.decode()
    li_list = html.etree.HTML(response).xpath('//ul[@id="pins"]/li')
    for li in li_list:
        image_url = li.xpath("./a/img/@data-original")[0]
        content = requests.get(url=image_url, headers=headers).content
        image_name = image_url.split("/")[-1]
        down_load(content, image_name)


def down_load(content, image_name):
    with open("./images/{}".format(image_name), "wb") as f:
        f.write(content)
    print("成功下载:{}".format(image_name))


if __name__ == "__main__":
    if not os.path.isdir("./images/"):
        os.mkdir("./images/")
    page = 1
    while True:
        run(page)
        page += 1
