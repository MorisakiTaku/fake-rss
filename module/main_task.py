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
import time

from module.item import Item


def parse_rss(rss_url):
    """使用feedparser模块解析rss，将条目以Item类保存"""
    content = feedparser.parse(rss_url)
    entries = [Item(entry) for entry in content.entries]
    return entries


def start_task(t_client, task, logger):
    """任务主模块"""
    url = task.rss_url()
    print(url)
    entries = parse_rss(url)
    num = 0  # 满足条件的条目数
    for i, entry in enumerate(entries):
        # 判断条目是否满足条件。若满足，则使用transmission api添加任务
        if task.filtrate(entry):
            t_client.add_torrent(entry.torrent(), download_dir=task.path)
            logger.info("Download \"{}\"".format(entry.title))
            num += 1
            time.sleep(10)
    if num:
        logger.info('Finished {} entry(s)'.format(num))
        task.set_time(entries[0].published_timestamp)
    else:
        logger.info("Entry not updated")


if __name__ == '__main__':
    _entries = parse_rss("http://www.kisssub.org/rss-%E6%BE%84%E7%A9%BA+Kaguya.xml")
    for _ in _entries:
        print(_.title)
        print(_.link)
