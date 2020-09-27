# ------------------------------------------------------------------------------
# Project:     fake-rss
# Name:        operate
# Purpose:
#
# Author:      Atomic
#
# Created:     2019/3/7
# ------------------------------------------------------------------------------
import threading
import time

from module.config import config_load
from module.log import Log


class Operation(object):
    """管理主任务进程"""
    flag = True

    def __init__(self, logger):
        self.logger = logger
        self.thread = None
        self.lock = threading.Lock()

    def start(self):
        self.logger.info("Start task thread")
        Operation.flag = True
        self.thread = threading.Thread(target=Task.start, args=[self.lock])
        self.thread.start()

    def reload(self):
        self.logger.info("Config reload and restart the program")
        Operation.flag = False
        time.sleep(5)
        self.thread = threading.Thread(target=Task.start, args=[self.lock])
        self.thread.start()

    def quit(self):
        if self.thread.is_alive():
            self.logger.info("Program exit")
            Operation.flag = False
        else:
            self.logger.info("Task not started")


class Task(object):

    @staticmethod
    def start(lock):
        """循环串联运行所有任务, 每完成一个回合等待若干秒"""
        logger = Log("Tasks").logger
        logger.info("Acquiring lock ...")
        lock.acquire()
        logger.info("Successfully acquired the lock")
        logger.info("------------------------------")
        connect, schedule, tasks = config_load(logger)
        transmission = connect.trans_client()
        downloader = connect.download_service()

        time_start = time.time()
        while Operation.flag:
            if time.time() - time_start > schedule.interval:  # 使用当前时间来计算间隔判断启动任务与否
                time_start += schedule.interval
                for i, task in enumerate(tasks):
                    logger.info("Start subject {}: {}".format(i + 1, task.title))
                    Task.subject(transmission, downloader, task, logger)
                logger.info("----------")
                logger.info("Task completed, start timing")
                logger.info("------------------------------")
            time.sleep(5)  # 循环间隔时间缩短
        lock.release()
        logger.info("Released the lock")
        logger.info("Task thread is over")

    @staticmethod
    def subject(transmission, downloader, task, logger):
        """下载一个项目下的所有条目"""
        entries = task.parse_rss()
        num = 0  # 满足条件的条目数
        for i, entry in enumerate(entries):
            # 判断条目是否满足条件。若满足，则使用transmission api添加任务
            if task.filtrate(entry):
                transmission.add_torrent(entry.get_download_url(), downloader=downloader, download_dir=task.path)
                logger.info("Download \"{}\"".format(entry.title))
                num += 1
        if num:
            logger.info('Finished {} entry(s)'.format(num))
            task.save_update_time(entries[0].published_timestamp)
        else:
            logger.info("Subject not update")
