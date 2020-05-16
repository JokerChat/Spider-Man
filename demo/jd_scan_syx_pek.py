# -*- coding:UTF-8 -*-
import requests
import time
import json
import random
import datetime
import smtplib
import sys
from email.mime.text import MIMEText
from email.header import Header
def sendEmail(messages):
    mail_host = "12345"
    mail_user = "1111"
    mail_pass = "123455"
    sender = "123455"
    receivers = "123455"
    title = "123455"
    message = MIMEText(messages, 'plain', 'utf-8')
    message['From'] = "{}".format(sender)
    message['To'] = ",".join(receivers)
    message['Subject'] = title
    try:
        smtpObj = smtplib.SMTP_SSL(mail_host,465)
        smtpObj.login(mail_user, mail_pass)
        smtpObj.sendmail(sender, receivers, message.as_string())
        print("mail has been send successfully.")
    except smtplib.SMTPException as e:
        print(e)
def spider_comment(a,b,i):
    url = 'http://jipiao.jd.com/ajaxTicket/weeklowprice.action?depCity=%s&arrCity=%s&depDate=%s&flag=' % (a,b,i)
    kv = {'user-agent': 'Mozilla/5.0', 'referer': 'http://jipiao.jd.com/ticketquery/flightSearch.action?query.depCity=%E5%8C%97%E4%BA%AC&query.arrCity=%E4%B8%89%E4%BA%9A&query.depCityCode=undefined&query.arrCityCode=undefined&query.depAirportCode=undefined&query.arrAirportCode=undefined&query.lineType=OW&query.depDate=2020-01-30&query.arrDate=2020-01-30&query.goTime=undefined&query.backTime=undefined&query.classNo=%20&query.queryModule=1&query.hasChild=false&query.hasInfant=false&query.oneBox=&query.queryType=jipiaoindexquery&query.source=0'}
    try:
        r = requests.get(url,headers=kv)
        r.raise_for_status()
    except:
        print('爬取失败')
    r_json_str =r.text
    r_json_obj = json.loads(r_json_str)
    r_json_lists = r_json_obj['weekLowPriceInfoList']
    try:
        s = 5000
		for r_json_list in r_json_lists:
            prices = r_json_list['price']
            dates = r_json_list['date']
            if dates == '2021-02-10' and int(prices) < 600:
                messages = a + '-' + b + ',' + '日期：' + dates + '价格：' + prices
                print(a + '-' + b + ',' + '日期：' + dates + '价格：' + prices)
                sendEmail(messages)
                sys.exit()
		    elif s != int(prices):
			    print(a + '-' + b + ',' + '日期：' + dates + '价格：' + prices)
            else:
                pass
		    s = int(prices)
    except Exception as e:
        print(e)
if __name__ == '__main__':
    while True:
        a = '三亚'
        b = '北京'
        i = '2021-02-10'
        try:
           spider_comment(a,b,i)
           time.sleep(random.random() * 50)
        except Exception as e:
            print(e)
