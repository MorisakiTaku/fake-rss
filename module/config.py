# ------------------------------------------------------------------------------
# Project:     fake-rss
# Name:        config
# Purpose:
#
# Author:      Atomic
#
# Created:     2019/3/4
# ------------------------------------------------------------------------------
import urllib.parse
from ruamel import yaml

from module.util import set_timestamp


class Settings(object):
    """配置"""
    def __init__(self, gl):
        self.interval = gl['interval']
        self.active = gl['active']
        self.headers = gl['headers']
        self.path = gl['target_path']


class Task(object):
    """任务"""
    def __init__(self, key, allocation):
        self.title = key
        self.site = allocation['site']
        self.rss = allocation['rss']
        self.type = allocation['rss_type']
        self.time = allocation['timestamp']
        self.params = allocation['params']

    def rss_url(self):
        if self.type == 1:
            url = urllib.parse.urlencode(self.params)
            url = self.rss + "?" + url
        elif self.type == 2:
            url = urllib.parse.quote("+".join(self.params['keyword'].split(" ")))
            url = self.rss[:-4] + "-" + url + self.rss[-4:]
        else:
            url = self.rss
        return url

    def update_time(self, end_time):
        self.time = end_time
        set_timestamp(self.title, self.time)


def config_load(logger):
    with open('config.yaml', 'r', encoding='utf-8') as file:
        content = yaml.safe_load(file.read())
    settings = Settings(content['global'])
    tasks = []
    for key, allocation in content['tasks'].items():
        if key in settings.active:
            task = Task(key, allocation)
            tasks.append(task)
            logger.info("Task: {} in {} with params {}".format(task.title, task.site, task.params))
    logger.info("Load {} active task(s) from config.yaml".format(len(tasks)))
    return settings, tasks
