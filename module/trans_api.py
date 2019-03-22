# ------------------------------------------------------------------------------
# Project:     fake-rss
# Name:        trans_api
# Purpose:
#
# Author:      Atomic
#
# Created:     2019/3/12
# ------------------------------------------------------------------------------
from transmissionrpc.utils import make_rpc_name, argument_value_convert
import urllib.parse
import transmissionrpc
import base64
import time

from module.item import Downloader


class Client(transmissionrpc.Client):

    def add_torrent(self, torrent, downloader=None, timeout=None, **kwargs):
        if torrent is None:
            raise ValueError('add_torrent requires data or a URI.')
        torrent_data = None
        parsed_uri = urllib.parse.urlparse(torrent)
        if parsed_uri.scheme in ['ftp', 'ftps', 'http', 'https']:
            # there has been some problem with T's built in torrent fetcher,
            # use a python one instead
            torrent_data = downloader.start_download(torrent)
            torrent_data = base64.b64encode(torrent_data).decode('utf-8')
            time.sleep(3)
        if parsed_uri.scheme in ['file']:
            filepath = torrent
            # uri decoded different on linux / windows ?
            if len(parsed_uri.path) > 0:
                filepath = parsed_uri.path
            elif len(parsed_uri.netloc) > 0:
                filepath = parsed_uri.netloc
            torrent_file = open(filepath, 'rb')
            torrent_data = torrent_file.read()
            torrent_data = base64.b64encode(torrent_data).decode('utf-8')
        if not torrent_data:
            if torrent.endswith('.torrent') or torrent.startswith('magnet:'):
                torrent_data = None
            else:
                might_be_base64 = False
                # noinspection PyBroadException
                try:
                    # check if this is base64 data
                    base64.b64decode(torrent.encode('utf-8'))
                    might_be_base64 = True
                except Exception:
                    pass
                if might_be_base64:
                    torrent_data = torrent
        if torrent_data:
            args = {'metainfo': torrent_data}
        else:
            args = {'filename': torrent}
        for key, value in kwargs.items():
            argument = make_rpc_name(key)
            (arg, val) = argument_value_convert('torrent-add', argument, value, self.rpc_version)
            args[arg] = val
        return list(self._request('torrent-add', args, timeout=timeout).values())[0]
