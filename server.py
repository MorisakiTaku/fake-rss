# ------------------------------------------------------------------------------
# Project:     fake-rss
# Name:        server
# Purpose:
#
# Author:      Atomic
#
# Created:     2019/3/7
# ------------------------------------------------------------------------------
from threading import Thread
import socket

from module.operate import Operation
from module.log import Log


def server():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(('localhost', 9999))
    s.listen(5)
    print("Fake-rss server start. Wait for command. ")
    logger = Log("Server").logger
    operation = Operation(logger)
    while True:
        # 接受一个新连接:
        sock, addr = s.accept()
        # 创建新线程来处理TCP连接:
        t = Thread(target=tcp_link, args=(sock, addr, operation))
        t.start()


def tcp_link(sock, addr, operation):
    operation.logger.info('------------------------------------------------------------')
    operation.logger.info('Accept new connection from %s:%s...' % addr)
    data = sock.recv(1024)
    if data.decode('utf-8') == 'start':
        operation.start()
        sock.send("Program start".encode())
        operation.logger.info('Received start command')
    elif data.decode('utf-8') == 'reload':
        operation.reload()
        sock.send("Config reload and restart the program".encode())
        operation.logger.info('Received reload command')
    elif data.decode('utf-8') == 'quit':
        operation.quit()
        sock.send("Program exit".encode())
        operation.logger.info('Received quit command')
    else:
        operation.logger.error('Invalid command')
    sock.close()
    operation.logger.info('Connection from %s:%s closed.' % addr)
    operation.logger.info('------------------------------------------------------------')


if __name__ == "__main__":
    server()
