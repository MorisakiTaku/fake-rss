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

from module.util import transfer


class Item(object):

    def __init__(self, entry):
        self.title = transfer(entry.title)
        self.link = entry.link
        self.links = entry.links
        self.published_parsed = entry.published_parsed
        self.published_timestamp = time.mktime(self.published_parsed)

    def parse_torrent(self):
        for s_link in self.links:
            if s_link['type'] == 'application/x-bittorrent':
                tor_url = s_link['href']
                tor_name = self.title + ".torrent"
                return tor_url, tor_name
        return None, None
