# ------------------------------------------------------------------------------
# Project:     fake-rss
# Name:        config
# Purpose:     Load configuration from config.yaml.
#
# Author:      Atomic
#
# Created:     2019/3/4
# ------------------------------------------------------------------------------
import requests
from ruamel import yaml
from transmissionrpc.constants import DEFAULT_PORT

from module.trans_api import Client
from module.item import TaskInfo


class Connect(object):
    """下载requests headers、transmission服务配置"""
    def __init__(self, conn):
        self.headers = conn.get('request_headers', None)
        self.transmission = conn.get('transmission', {})

    def trans_client(self):
        return Client(address=self.transmission.get('host', 'localhost'),
                      port=self.transmission.get('port', DEFAULT_PORT),
                      user=self.transmission.get('username', None),
                      password=self.transmission.get('password', None))

    def download_service(self):
        return Downloader(self.headers)


class Schedule(object):
    """计划任务"""
    def __init__(self, sc):
        self.active = sc['active']
        self.interval = sc['interval']
        self.default_path = sc['path']


class Downloader(object):
    """torrent文件下载管理器"""

    def __init__(self, headers: dict):
        self.headers = headers

    def download(self, target_url):
        content = self._ftp_download(target_url)
        return content

    def _ftp_download(self, target_url):
        """FTP下载种子"""
        res = requests.get(target_url, headers=self.headers)
        return res.content

    def _magnet_link_download(self, magnet_link):
        """磁力链接下载种子, 待实现"""
        # http://magnet2torrent.com/ 可以实现转换, 但是需要绕过Cloudflare的探测, 比较麻烦
        pass


def config_load(logger):
    with open('config.yaml', 'r', encoding='utf-8') as file:
        content = yaml.safe_load(file.read())
    connect = Connect(content['connect'])
    schedule = Schedule(content['schedule'])
    tasks = []
    for key, task_dict in content['tasks'].items():
        if key in schedule.active:
            task = TaskInfo(key, task_dict, schedule.default_path)
            tasks.append(task)
    logger.info("Load {} active task.py(s) from config.yaml".format(len(tasks)))
    title_list = [_.title for _ in tasks]
    logger.info("Task: {}".format(", ".join(title_list)))
    logger.info("------------------------------")
    return connect, schedule, tasks
