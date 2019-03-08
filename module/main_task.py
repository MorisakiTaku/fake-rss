# ------------------------------------------------------------------------------
# Project:     fake-rss
# Name:        main
# Purpose:
#
# Author:      Atomic
#
# Created:     2019/3/4
# ------------------------------------------------------------------------------
import feedparser
import requests
import time

from module.item import Item


def parse_rss(rss_url):
    """使用feedparser模块解析rss，将条目以Item类保存"""
    content = feedparser.parse(rss_url)
    entries = [Item(entry) for entry in content.entries]
    return entries


def download_torrent(settings, entry, logger):
    """根据条目名和种子链接下载保存"""
    tor_url, tor_name = entry.parse_torrent()
    logger.info("Download [{}] with url: {}".format(tor_name, tor_url))
    if tor_url:
        try:
            response = requests.get(tor_url, headers=settings.headers)
            with open(settings.path + tor_name, 'wb') as tr:
                tr.write(response.content)
        except ConnectionError as e:
            logger.info('Download failed: {}'.format(e))


def start_task(settings, task, logger):
    """任务主模块"""
    url = task.rss_url()
    entries = parse_rss(url)
    i, end_time = 0, 0
    for i, entry in enumerate(entries):
        if entry.published_timestamp > task.time:
            end_time = max(end_time, entry.published_timestamp)
            download_torrent(settings, entry, logger)
        else:
            i -= 1
            break
        time.sleep(10)
    if end_time:
        logger.info('Finished {} entry(s)'.format(i+1))
        task.update_time(end_time)
