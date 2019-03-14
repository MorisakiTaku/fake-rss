# ------------------------------------------------------------------------------
# Project:     fake-rss
# Name:        logs
# Purpose:
#
# Author:      Atomic
#
# Created:     2019/3/8
# ------------------------------------------------------------------------------
import logging
import time


class Log(object):

    def __init__(self, type_):
        self.logger = logging.getLogger()
        self.logger.setLevel(logging.INFO)  # log等级总开关
        self.formatter = logging.Formatter("%(asctime)s - %(levelname)s: %(message)s")
        self.logfile = self.gen_filename(type_)
        self.create_logger()

    @staticmethod
    def gen_filename(type_):
        # 创建一个handler，用于写入日志文件
        time_now = time.strftime('%Y%m%d', time.localtime(time.time()))
        filename = time_now + '.log'
        logfile = "logs/[" + str(type_) + "]" + filename
        return logfile

    def create_logger(self):
        # 创建file handler
        fh = logging.FileHandler(self.logfile, mode='w', encoding='utf-8')
        fh.setLevel(logging.INFO)  # 输出到file的log等级的开关
        fh.setFormatter(self.formatter)
        # 将logger添加到handler里面
        self.logger.addHandler(fh)
