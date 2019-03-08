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


def filename():
    # 创建一个handler，用于写入日志文件
    time_now = time.strftime('%Y%m%d_%H%M', time.localtime(time.time()))
    file_name = time_now + '.log'
    return file_name


def create_logger(logfile):
    # 创建一个logger
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)  # log等级总开关
    formatter = logging.Formatter("%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s")
    # 创建file handler
    fh = logging.FileHandler(logfile, mode='w', encoding='utf-8')
    fh.setLevel(logging.INFO)  # 输出到file的log等级的开关
    fh.setFormatter(formatter)
    # 将logger添加到handler里面
    logger.addHandler(fh)
    return logger


def log(type_):
    logfile = "logs/[" + str(type_) + "]" + str(filename())
    logger = create_logger(logfile)
    return logger
