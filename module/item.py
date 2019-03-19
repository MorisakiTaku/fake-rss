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
import requests
import feedparser
import dateutil.parser
from ruamel import yaml
from urllib import parse

from module.util import transfer


class Entry(object):
    """条目"""
    def __init__(self, entry):
        self.title = transfer(entry.title)
        self.link = entry.link
        self.links = entry.links
        self.published_timestamp = time.mktime(entry.published_parsed)

    def get_download_url(self):
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
        self.filter_ = task_dict.get('filter', {})
        self.timestamp = 0
        self.hash = hashlib.md5(str(task_dict).encode('utf-8')).hexdigest()

    def parse_rss(self):
        """使用feedparser模块解析rss，将条目以Item类保存"""
        content = feedparser.parse(self.rss_url())
        entries = [Entry(entry) for entry in content.entries]
        return entries

    def rss_url(self):
        if self.params:
            return self.rss + "?" + parse.urlencode(self.params)
        else:
            return self.rss

    def filtrate(self, entry):
        # 时间戳条件
        default_timestamp = time.mktime(dateutil.parser.parse(self.filter_.get('after_time', '1970.1.2')).timetuple())
        after_time = max(default_timestamp, self._get_time())
        # 关键词条件
        filter_word = self.filter_.get('keyword', "")
        # 过滤
        if (entry.published_timestamp > after_time) & (filter_word in entry.title):
            return True
        else:
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


class Downloader(object):
    """torrent文件下载器"""
    def __init__(self, headers):
        self.headers = headers

    def start_download(self, target_url):
        content = self._direct_download(target_url)
        return content

    def _direct_download(self, target_url):
        res = requests.get(target_url, headers=self.headers)
        return res.content
