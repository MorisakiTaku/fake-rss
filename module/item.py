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
import urllib.parse
from dateutil.parser import parse
from ruamel import yaml

from module.util import transfer


class Item(object):
    """条目"""
    def __init__(self, entry):
        self.title = transfer(entry.title)
        self.link = entry.link
        self.links = entry.links
        self.published_timestamp = time.mktime(entry.published_parsed)

    def torrent(self):
        for s_link in self.links:
            if s_link['type'] == 'application/x-bittorrent':
                return s_link['href']
        return None


class Task(object):
    """任务"""
    def __init__(self, schedule, key, task_dict):
        self.title = key
        self.rss = task_dict.get('rss', None)
        self.path = task_dict.get('path', schedule.default_path)
        self.interval = task_dict.get('interval', 0)
        self.params = task_dict.get('params', {})
        self.filter = task_dict.get('filter', {})
        self.timestamp = 0
        self.hash = hashlib.md5(str(task_dict).encode('utf-8')).hexdigest()

    def rss_url(self):
        if self.params:
            return self.rss + "?" + urllib.parse.urlencode(self.params)
        else:
            return self.rss

    def filtrate(self, entry):
        # 时间戳条件
        default_timestamp = time.mktime(parse(self.filter.get('after_time', '1970.1.2')).timetuple())
        after_time = max(default_timestamp, self._get_time())
        # 关键词条件
        filter_word = self.filter.get('keyword', "")
        # 过滤
        if (entry.published_timestamp > after_time) & (filter_word in entry.title):
            return True
        else:
            print(entry.published_timestamp)
            print(after_time)
            print(filter_word)
            print(entry.title)
            return False

    def set_time(self, end_time):
        self.timestamp = end_time
        with open('logs/cache.yaml', 'r', encoding='utf-8') as file:
            content = yaml.safe_load(file.read())
            if not content:
                content = {}
        with open('logs/cache.yaml', 'w', encoding='utf-8') as file:
            content[self.hash] = end_time
            yaml.dump(content, file, Dumper=yaml.RoundTripDumper, allow_unicode=True)

    def _get_time(self):
        with open('logs/cache.yaml', 'r', encoding='utf-8') as file:
            content = yaml.safe_load(file.read())
        if content:
            return content.get(self.hash, self.timestamp)
        else:
            return self.timestamp
