# -*- coding: utf-8 -*-
# @Author       :junjie    
# @Time         :2019/7/25 14:15
# @FileName     :pdf_demo.py
#IDE            :PyCharm
import pdfkit
from public.get_database import getDatabase
import pymysql
from config.config import *
test=getDatabase(local_config)
pdf_config=pdfkit.configuration(wkhtmltopdf=r"C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe")
data=test.select_all('wx_article',wx_id='MzI2NTU4OTI1NQ==')
for i in data:
    pdfkit.from_url(i['wx_url'], i['wx_title']+'.pdf', configuration=pdf_config)