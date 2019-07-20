# -*- coding: utf-8 -*-
# @Author       :junjie    
# @Time         :2019/7/5 17:08
# @FileName     :get_database.py
#IDE            :PyCharm
import pymysql
import datetime
from public.log import logger
from config.config import *
mylog=logger('操作数据库').get_logger()
class getDatabase(object):
    #初始化数据,读取配置文件
    def __init__(self,config):
        try:
            self.conn=pymysql.connect(**config)
            self.cursor=self.conn.cursor()
            mylog.info("############连接数据库成功############")
        except Exception as e:
            mylog.info("############连接失败:{}############".format(e))
    def close(self):
        try:
            self.conn.close()
            self.cursor.close()
        except Exception as e:
            mylog.info("############关闭失败:{}############".format(e))
    def __varchar(self,s):
        # 处理sql语句中的字符串型字典值，在两侧加引号
        if isinstance(s, str):
            return '"' + s + '"'
        else:
            return str(s)
    def __submit(self,sql):
        result=0
        try:
            # mylog.info("############sql:{0}############".format(sql))
            self.cursor.execute(sql)
            self.conn.commit()
            # mylog.info("############提交成功############")
            result=1
            return result
        except Exception as e:
            mylog.info("############提交失败:{}############".format(e))
            return result
    def __changestr(self,items):
        """这里是将字典里面的对象信息转换成字符串"""
        try:
            data=[]
            for ii in items:
                result_replace = {k: v.__str__() for k, v in ii.items() if isinstance(v, datetime.datetime)}
                ii.update(result_replace)
                data.append(ii)
            return data
        except Exception as e:
            mylog.info("转换字符串出错:{}".format(e))
    def select(self,table,**kwargs):
        '''
        查询数据
        :param table: 表名
        :param kwargs: 约束条件
        :return: 返回数据,列表嵌套字典
        '''
        try:
            sql='SELECT * FROM '+table
            if kwargs:
                sql =sql+' WHERE '
                for key,value in kwargs.items():
                    sql=sql +key+'='+self.__varchar(value)+' and '
                sql=sql[:-5]
            self.cursor.execute(sql)
            # mylog.info("############查询成功############")
            return self.__changestr(self.cursor.fetchall())
        except Exception as e:
            mylog.info("############查询失败:{}############".format(e))
    def updata(self,table,conditionKey=None,conditionValue=None,**kwargs):
        '''
        更新数据
        :param table: 表名
        :param conditionKey: 约束的字段
        :param conditionValue: 约束的值
        :param kwargs: 要更新的字段和值
        :return: 1为成功,0为失败
        '''
        try:
            if conditionKey and conditionValue:
                if kwargs:
                    sql ='UPDATE '+table+' SET '
                    for key,value in kwargs.items():
                        sql =sql+key+'='+self.__varchar(value)+' and '
                    sql=sql[:-5]
                    sql =sql + ' WHERE '+conditionKey +'='+self.__varchar(conditionValue)
                    return self.__submit(sql)
                else:
                    print('要更新的字段和值不为空')
            else:
                print('约束字段或者值不能为空')
        except Exception as e:
            mylog.info("############更新失败:{}############".format(e))
    def insert(self,table,**kwargs):
        '''
        插入数据
        :param tabel: 表名
        :param values: 要插入的数据
        :return: 1为成功,0为失败
        '''
        try:
            sql = 'INSERT INTO ' + table + ' ('
            if kwargs:
                for key in kwargs.keys():
                    sql=sql+key+ ','
                sql=sql[:-1]+')'+' VALUES'+' ('
                for value in kwargs.values():
                    sql=sql+self.__varchar(value)+','
                sql=sql[:-1]+')'
                return self.__submit(sql)
        except Exception as e:
            mylog.info("############新增失败:{}############".format(e))
    def delete(self,table,**kwargs):
        '''
        删除数据
        :param table: 表名
        :param kwargs: 约束条件
        :return: 1为成功,0为失败
        '''
        try:
            sql='DELETE FROM '+table
            if kwargs:
                sql=sql+' WHERE '
                for key,value in kwargs.items():
                    sql = sql + key+ '='+self.__varchar(value)+' and '
                sql=sql[:-5]
                return self.__submit(sql)
            else:
                print('约束条件不能为空')
        except Exception as e:
            mylog.info("############删除失败:{}############".format(e))
if __name__=='__main__':
    test = getDatabase(local_config)
    data = test.insert('jd_comment', comment='测试一下是计算机上就',comment_id='456456')
    print('执行成功')






