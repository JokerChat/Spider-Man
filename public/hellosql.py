# -*- coding: utf-8 -*-
import time
import datetime
from public.log import logger
import pymysql
mylog=logger('操作数据库').get_logger()
class HelloSql(object):

    def __init__(self, **kwargs):
        mylog.info("mysql_config:{}".format(str(kwargs)))
        self.mysql_config = kwargs

    def connect(self):
        try:
            conn = pymysql.connect(charset='utf8', **self.mysql_config)
            return conn
        except Exception as e:
            mylog.info("数据库连接失败，开始重连:{}".format(e))
            time.sleep(5)
            conn = pymysql.connect(charset='utf8', **self.mysql_config)
            return conn

    def find_all(self, conn, sql, value=None):
        count, cursor = self.execute(conn, sql=sql, value=value)
        if count > 0:
            rows = cursor.fetchall()
            dict_rows = []
            for row in rows:
                dict_item = self.sql_row_to_dict(cursor=cursor, row=row)
                dict_item = self.dict_datetime_obj_to_str(dict_item)
                dict_rows.append(dict_item)
            return dict_rows
        else:
            return False

    def find_one(self, conn, sql, value=None):
        count, cursor = self.execute(conn, sql=sql, value=value)
        if count > 0:
            row = cursor.fetchone()
            dict_item = self.sql_row_to_dict(cursor=cursor, row=row)
            dict_item = self.dict_datetime_obj_to_str(dict_item)
            return dict_item
        else:
            return False

    def insert_one(self, conn, sql, value=None):
        try:
            _, cursor = self.execute(conn, sql=sql, value=value)
            last_id = int(cursor.lastrowid)
            conn.commit()
            return last_id
        except Exception as e:
            mylog.info("insert_one出错:{}".format(e))
            return False

    def update(self, conn, sql, value=None):
        try:
            num = self.query(conn, sql, value=value)
            conn.commit()
            return num
        except Exception as e:
            mylog.info("update出错:{}".format(e))
            return False

    def update_db(self, conn, data_table, data, find_dict):
        if not isinstance(data, dict):
            return False
        find_keys = list(find_dict.keys())
        keys = list(data.keys())
        update_sql = "update `" + data_table + "` set " + ", ".join(["`" + i + "`" + "= %s" for i in keys]) \
                     + " where " + " and ".join(["`" + i + "`" + "= %s" for i in find_keys])
        num = self.update(conn, update_sql, value=list(data.values()) + list(find_dict.values()))
        conn.commit()
        return num

    def delete(self, conn, sql, value=None):
        try:
            num = self.query(conn, sql, value)
            conn.commit()
            return num
        except Exception as e:
            mylog.info("delete出错:{}".format(e))
            return False

    @staticmethod
    def execute(conn, sql, value=None):
        try:
            cursor = conn.cursor()
            if value:
                r = cursor.execute(sql, value)
            else:
                r = cursor.execute(sql)
            return r, cursor
        except Exception as e:
            mylog.info('execute出错:{}'.format(e))

    def query(self, conn, sql, value=None):
        try:
            count, cursor = self.execute(conn, sql=sql, value=value)
            return count
        except Exception as e:
            mylog.info('query出错:{}'.format(e))

    @staticmethod
    def sql_row_to_dict(cursor=None, row=None):
        """这里是将数据行转换成字段的形式输出"""
        try:
            result = dict()
            columns = [desc[0] for desc in cursor.description]
            for k, v in zip(columns, row):
                result[k] = v
            return result
        except Exception as e:
            mylog.error('sql_row_to_dict出错:{}'.format(e))

    @staticmethod
    def dict_datetime_obj_to_str(result_dict):
        """这里是将字典里面的对象信息转换成字符串"""
        try:
            if result_dict:
                result_replace = {k: v.__str__() for k, v in result_dict.items() if isinstance(v, datetime.datetime)}
                result_dict.update(result_replace)
            return result_dict
        except Exception as e:
            mylog.info("dict_datetime_obj_to_str出错:{}".format(e))
