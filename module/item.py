# ------------------------------------------------------------------------------
# Project:     fake-rss
# Name:        item
# Purpose:
#
# Author:      Atomic
#
# Created:     2019/3/4
# ------------------------------------------------------------------------------
import time
import hashlib
import feedparser
from dateutil.parser import parse as time_parse
from ruamel import yaml
from urllib import parse
from typing import List
from module.util import transfer


class Entry(object):
    """条目"""

    def __init__(self, entry):
        self.title = transfer(entry.title)
        self.link = entry.link
        self.links = entry.links
        self.published_timestamp = time.mktime(entry.published_parsed)

    def get_download_url(self) -> str:
        for s_link in self.links:
            if s_link['type'] == 'application/x-bittorrent':
                return s_link['href']
        return ""


class TaskInfo(object):
    """任务信息"""

    def __init__(self, key: str, task_dict: dict, default_path: str):
        self.title = key
        self.rss = task_dict.get('rss', None)
        self.path = task_dict.get('path', default_path)
        self.params = task_dict.get('params', {})
        self.filter = task_dict.get('filter', {})
        self.timestamp = 0
        self.hash = hashlib.md5(str(task_dict).encode('utf-8')).hexdigest()

    def parse_rss(self) -> List[Entry]:
        """使用feedparser模块解析rss，将条目以Entry类保存"""
        rss_url = self.rss + "?" + parse.urlencode(self.params) if self.params else self.rss
        content = feedparser.parse(rss_url)
        entries = [Entry(entry) for entry in content.entries]
        return entries

    def filtrate(self, entry: Entry) -> bool:
        # 时间戳条件
        default_timestamp = time.mktime(time_parse(self.filter.get('after_time', '1970.1.2')).timetuple())
        after_time = max(default_timestamp, self.__get_update_time())
        if entry.published_timestamp < after_time:
            return False

        # 关键词条件
        include_keyword = self.filter.get('include', "").split(" ")
        exclude_keyword = self.filter.get('include', "").split(" ")
        for word in include_keyword:
            if word not in entry.title:
                return False
        for word in exclude_keyword:
            if word in entry.title:
                return False

        return True

    def save_update_time(self, end_time: int) -> None:
        """使用cache.yaml保存运行过程中变化过的参数, 比如起始时间. key为根据不变参数计算得到的hash值"""
        self.timestamp = end_time
        with open('logs/cache.yaml', 'w+', encoding='utf-8') as file:
            content = yaml.safe_load(file.read())
            content[self.hash] = end_time
            yaml.dump(content, file, Dumper=yaml.RoundTripDumper, allow_unicode=True)

    def __get_update_time(self) -> int:
        with open('logs/cache.yaml', 'r', encoding='utf-8') as file:
            content = yaml.safe_load(file.read())
        return content.get(self.hash, self.timestamp) if content else self.timestamp
