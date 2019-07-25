# -*- coding: utf-8 -*-
# @Author       :junjie    
# @Time         :2019/7/23 14:05
# @FileName     :boss_zhipin.py
#IDE            :PyCharm
import requests
from public.get_database import getDatabase
import json
import time
from config.config import *
test = getDatabase(local_config)
def boss_spider(mpt,query,page,degree=0,experience=0,salary=0,stage=0,scale=0,industry=0,position=0):
    url='https://www.zhipin.com/wapi/zpgeek/miniapp/search/joblist.json'
    headers={
        'Content-Type':'application/x-www-form-urlencoded',
        'mpt':mpt, #小程序授权码,一段时间会失效
        'platform':'zhipin',
        'wt':'JPfsiaBw4hMcZ02s',
        'referer':'https://servicewechat.com/wxa8da525af05281f3/70/page-frame.html',
        'User-Agent':'Mozilla/5.0 (iPhone; CPU iPhone OS 12_3_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 MicroMessenger/7.0.4(0x17000428) NetType/WIFI Language/zh_CN',
        'v':'2',
        'apappid':'10002'
    }
    params={'query':query, #查询职业
            'city':101280100, #城市id
            'appId':10002, #小程序id
            'stage':stage, #融资规模
            'scale':scale, #团队规模
            'industry':industry, #行业
            'degree':degree, #最低学历，初中以下：209 中专：208，高中：206，大专：202，本科：203,硕士：204，博士：205
            'salary':salary, #薪资 3K：402，3-5K：403,5-10K：404,10-20K：404,20-50K：405,50K：406
            'experience':experience,#工作经验，在校生：108，应届生：102，1年以内：103,1-3年：104,3-5年：105,5-10年：106,10年以上：107
            'position':position,
            'page':page
    }
    re=requests.get(url,headers=headers,params=params)
    data=re.json()
    if data['message']=='Success':
        data = re.json()
        is_more = data['zpData']['hasMore']
        for i in data['zpData']['list']:
            jobName=i['jobName'] #职业名称
            jobExperience=i['jobExperience'] #工作年限
            jobDegree=i['jobDegree']#学历
            salaryDesc=i['salaryDesc']#薪资范围
            try:
                if salaryDesc.find('K')!=-1:
                    if len(split_salary(salaryDesc))==2:
                        low_salary=split_salary(salaryDesc)['low_salary']
                        high_salary=split_salary(salaryDesc)['high_salary']
                        other_salary='0'
                    else:
                        low_salary = split_salary(salaryDesc)['low_salary']
                        high_salary = split_salary(salaryDesc)['high_salary']
                        other_salary= split_salary(salaryDesc)['other_salary']
                else:
                    low_salary='0'
                    high_salary='0'
                    other_salary='0'
            except:
                print('切割字符串错误：{0}'.format(salaryDesc))
            jobLabels=json.dumps(i['jobLabels'],ensure_ascii=False)#工作标签
            jobLabels = jobLabels.replace('"', '\\"')
            area=i['jobLabels'][0]#工作地点
            brandName=i['brandName']#公司名字
            encryptJobId=i['encryptJobId']#职业详细id
            test.insert('boss_zhipin',job_id=encryptJobId,job_name=jobName,brand_name=brandName,
                        job_degree=jobDegree,job_experience=jobExperience,area=area,low_salary=low_salary,
                        high_salary=high_salary,other_salary=other_salary,salary=salaryDesc,query_name=query,
                        job_labels=jobLabels
                        )
        if is_more==True:
            return True
        return False
    else:
        print('获取数据失败')
#切割字符串
def split_salary(salary):
    if salary.find('薪') != -1:
        low_salary=salary[0:salary.index('-')]
        high_salary=salary[salary.index('-') + 1: salary.index('K')]
        other_salary=salary[salary.index('·') + 1:salary.index('薪')]
        return {'low_salary':low_salary,'high_salary':high_salary,'other_salary':other_salary}
    else:
        low_salary = salary[0:salary.index('-')]
        high_salary = salary[salary.index('-') + 1: salary.index('K')]
        return {'low_salary': low_salary, 'high_salary': high_salary}
if __name__ == '__main__':
    index=1
    mpt='fb66b7cbdfcd9f0f9b03decf8470ab9e'
    while 1:
        print(f'*************开始抓取boss招聘第{index}页数据***************')
        is_more=boss_spider(mpt,'测试',index)
        print(f'*************boss招聘数据第{index}页已抓取完毕*************')
        time.sleep(3)
        if not is_more:
            print('*************数据已抓取完毕，退出程序*****************')
            break
        index += 1