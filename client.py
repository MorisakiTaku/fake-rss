# ------------------------------------------------------------------------------
# Project:     fake-rss
# Name:        piptest
# Purpose:
#
# Author:      Atomic
#
# Created:     2019/3/7
# ------------------------------------------------------------------------------
import socket
import sys


def send(text):
    try:
        # 建立连接:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect(('localhost', 9999))
        # 发送指令并退出
        s.send(text.encode())
        data = s.recv(1024)
        print(data.decode())
        s.close()
    except Exception as e:
        print("服务未启动")
        print('Error:', e)


def main():
    opt = sys.argv[1:]
    if (not opt) or (opt[0] == 'start'):
        send('start')
    elif opt[0] in ['reload', 'quit']:
        send(opt[0])
    elif opt[0] == 'help':
        print("可用命令: (start), reload, quit, help")
    else:
        print('无效命令。使用help参数获取有效命令')


if __name__ == '__main__':
    main()
