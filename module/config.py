# ------------------------------------------------------------------------------
# Project:     fake-rss
# Name:        config
# Purpose:
#
# Author:      Atomic
#
# Created:     2019/3/4
# ------------------------------------------------------------------------------
from ruamel import yaml
from transmissionrpc.constants import DEFAULT_PORT

from module.api import Client
from module.item import Task


class Connect(object):
    """requests、transmission服务配置"""
    def __init__(self, conn):
        self.headers = conn.get('headers', None)
        self.transmission = conn.get('transmission', {})

    def trans_client(self):
        return Client(address=self.transmission.get('host', 'localhost'),
                      port=self.transmission.get('port', DEFAULT_PORT),
                      user=self.transmission.get('username', None),
                      password=self.transmission.get('password', None), )


class Schedule(object):
    """计划任务"""
    def __init__(self, sc):
        self.active = sc['active']
        self.interval = sc['interval']
        self.default_path = sc['path']


def config_load(logger):
    with open('config.yaml', 'r', encoding='utf-8') as file:
        content = yaml.safe_load(file.read())
    connect = Connect(content['connect'])
    schedule = Schedule(content['schedule'])
    tasks = []
    for key, task_dict in content['tasks'].items():
        if key in schedule.active:
            task = Task(schedule, key, task_dict)
            tasks.append(task)
            logger.info("Task: {}".format(task.title))
    logger.info("Load {} active task(s) from config.yaml".format(len(tasks)))
    return connect, schedule, tasks


if __name__ == '__main__':
    pass
    # _settings, _tasks = config_load()
    # for _ in _tasks:
    #     _.cache()
    #     print(_.hash)
