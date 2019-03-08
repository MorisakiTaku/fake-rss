# ------------------------------------------------------------------------------
# Project:     fake-rss
# Name:        util
# Purpose:
#
# Author:      Atomic
#
# Created:     2019/3/5
# ------------------------------------------------------------------------------
from ruamel import yaml


def transfer(line):
    # 排除非法文件名字符
    line = line.replace('\\', '').replace('/', '').replace(':', '').replace('*', '')\
        .replace('?', '').replace('"', '').replace('<', '').replace('>', '')\
        .replace('|', '').replace('  ', ' ')
    # 替换HTML转义字符
    line = line.replace('&lt;', '<').replace('&gt;', '>').replace('&amp;', '&')\
        .replace('&apos;', '\'').replace('&quot;', '\"')
    return line


def set_timestamp(title, end_time):
    with open('config.yaml', 'r', encoding='utf-8') as file:
        content = yaml.safe_load(file.read())
    with open('config.yaml', 'w', encoding='utf-8') as file:
        content['tasks'][title]['timestamp'] = end_time
        yaml.dump(content, file, Dumper=yaml.RoundTripDumper, allow_unicode=True)
