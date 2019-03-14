# ------------------------------------------------------------------------------
# Project:     fake-rss
# Name:        util
# Purpose:
#
# Author:      Atomic
#
# Created:     2019/3/5
# ------------------------------------------------------------------------------


def transfer(line):
    # 排除非法文件名字符
    line = line.replace('\\', '').replace('/', '').replace(':', '').replace('*', '')\
        .replace('?', '').replace('"', '').replace('<', '').replace('>', '')\
        .replace('|', '').replace('  ', ' ')
    # 替换HTML转义字符
    line = line.replace('&lt;', '<').replace('&gt;', '>').replace('&amp;', '&')\
        .replace('&apos;', '\'').replace('&quot;', '\"')
    return line
