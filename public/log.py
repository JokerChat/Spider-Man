# -*- coding: utf-8 -*-
# @Author       :junjie    
# @Time         :2019/7/5 17:07
# @FileName     :log.py
#IDE            :PyCharm
import logging
import os
import time
class logger(object):
    def __init__(self, logger):
        """
        指定保存日志的文件路径，日志级别，以及调用文件
            将日志存入到指定的文件中
        :param logger:传入当前模块名字，便于分析日志
        """
        # 创建一个logger,初始化日志级别
        self.logger = logging.getLogger(logger)
        self.logger.setLevel(logging.INFO)
        #判断log目录是否存在，不存在则创建目录
        if not os.path.isdir("./log/"):
            os.mkdir("./log/")
        # 创建一个handler，用于写入日志文件
        now_time = time.strftime('%Y-%m-%d-%H-%M', time.localtime(time.time()))
        log_path = './log/'
        log_name = log_path + now_time + '.log'
        file_log = logging.FileHandler(log_name,encoding='utf-8')
        #设置输出到目录默认日志级别
        file_log.setLevel(logging.INFO)

        # 再创建一个handler，用于输出到控制台
        console = logging.StreamHandler()
        console.setLevel(logging.INFO)

        # 定义handler的输出格式
        formatter = logging.Formatter('%(asctime)s-%(levelname)s-%(filename)s-%(name)s日志信息：%(message)s')
        file_log.setFormatter(formatter)
        console.setFormatter(formatter)

        # 给logger添加handler
        self.logger.addHandler(console)
        self.logger.addHandler(file_log)

    def get_logger(self):
        return self.logger
if __name__=='__main__':
    mylog = logger('excel').get_logger()
    mylog.info("#############初始化数据")