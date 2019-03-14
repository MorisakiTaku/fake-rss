# ------------------------------------------------------------------------------
# Project:     fake-rss
# Name:        api
# Purpose:
#
# Author:      Atomic
#
# Created:     2019/3/12
# ------------------------------------------------------------------------------
from transmissionrpc.utils import make_rpc_name, argument_value_convert
from six import PY3, iteritems
import base64

import transmissionrpc
import urllib.parse
import urllib.request


headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                         "(KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36",
           "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8"}


class Client(transmissionrpc.Client):

    def add_torrent(self, torrent, timeout=None, **kwargs):
        if torrent is None:
            raise ValueError('add_torrent requires data or a URI.')
        torrent_data = None
        parsed_uri = urllib.parse.urlparse(torrent)
        if parsed_uri.scheme in ['ftp', 'ftps', 'http', 'https']:
            # there has been some problem with T's built in torrent fetcher,
            # use a python one instead
            req = urllib.request.Request(torrent, b"", headers)
            torrent_file = urllib.request.urlopen(req)
            torrent_data = torrent_file.read()
            torrent_data = base64.b64encode(torrent_data).decode('utf-8')
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
                try:
                    # check if this is base64 data
                    if PY3:
                        base64.b64decode(torrent.encode('utf-8'))
                    else:
                        base64.b64decode(torrent)
                    might_be_base64 = True
                except Exception:
                    pass
                if might_be_base64:
                    torrent_data = torrent
        args = {}
        if torrent_data:
            args = {'metainfo': torrent_data}
        else:
            args = {'filename': torrent}
        for key, value in iteritems(kwargs):
            argument = make_rpc_name(key)
            (arg, val) = argument_value_convert('torrent-add', argument, value, self.rpc_version)
            args[arg] = val
        return list(self._request('torrent-add', args, timeout=timeout).values())[0]


def _add_torrent():
    tc = Client('localhost', port=9091)
    tc.add_torrent('http://v2.uploadbt.com/?r=down&hash=5255bedde4d7b401543f130dc09f6b9a529affb9', download_dir='E:\\Atomic\\Downloads\\Transmission\\Cap')
    torrents = tc.get_torrents()
    for _ in torrents:
        print(_.name)


if __name__ == "__main__":
    add_torrent()
