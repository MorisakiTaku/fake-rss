# ------------------------------------------------------------------------------
# Project:     fake-rss
# Name:        opera
# Purpose:
#
# Author:      Atomic
#
# Created:     2019/3/7
# ------------------------------------------------------------------------------
from multiprocessing import Process
import time

from module.config import config_load
from module.main_task import start_task
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
        connect, schedule, tasks = config_load(logger)
        t_client = connect.trans_client()
        time.sleep(5)
        while True:
            for i, task in enumerate(tasks):
                logger.info("Start the task {}".format(i+1))
                start_task(t_client, task, logger)
            logger.info("Task completed, start timing")
            time.sleep(schedule.interval)
