# ------------------------------------------------------------------------------
# Project:     fake-rss
# Name:        operate
# Purpose:
#
# Author:      Atomic
#
# Created:     2019/3/7
# ------------------------------------------------------------------------------
from multiprocessing import Process
import time

from module.config import config_load
from module.task import start_task
from module.log import Log


class Operation(object):

    def __init__(self, logger):
        self.logger = logger
        self.process = Process()

    def start(self):
        self.logger.info("Program start")
        self.process = Process(target=self.mission)
        self.process.start()

    def reload(self):
        self.logger.info("Config reload and restart the program")
        self.process.terminate()
        self.process = Process(target=self.mission)
        self.process.start()

    def quit(self):
        if self.process.is_alive():
            self.logger.info("Program exit")
            self.process.terminate()
        else:
            self.logger.info("Task not started")

    @staticmethod
    def mission():
        logger = Log("Tasks").logger
        logger.info("------------------------------------------------------------")
        connect, schedule, tasks = config_load(logger)
        t_client = connect.trans_client()
        d_service = connect.download_service()
        time.sleep(5)
        while True:
            for i, task in enumerate(tasks):
                logger.info("Start the task.py {}: {}".format(i+1, task.title))
                start_task(t_client, d_service, task, logger)
            logger.info("Task completed, start timing")
            logger.info("------------------------------")
            time.sleep(schedule.interval)
