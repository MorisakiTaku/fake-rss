# ------------------------------------------------------------------------------
# Project:     fake-rss
# Name:        server
# Purpose:
#
# Author:      Atomic
#
# Created:     2019/3/7
# ------------------------------------------------------------------------------
import sys
import socket

from module.operate import Operation
from module.log import Log


class Server(object):

    def __init__(self):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.bind(('localhost', 9999))
        self.s.listen(5)
        logger = Log("Server").logger
        self.operation = Operation(logger)
        print("Fake-rss server start. Wait for command. ")

    def monitor(self):
        while True:
            # 接受一个新连接:
            sock, addr = self.s.accept()
            self.tcp_link(sock, addr, self.operation)

    @staticmethod
    def tcp_link(sock, addr, operation):
        operation.logger.info('------------------------------------------------------------')
        operation.logger.info('Accept new connection from %s:%s...' % addr)
        data = sock.recv(1024).decode('utf-8')
        operation.logger.info('Received ' + data + ' command')
        if data == 'start':
            operation.start()
            sock.send("Task start".encode())
        elif data == 'reload':
            operation.reload()
            sock.send("Config reload and restart the task".encode())
        elif data == 'quit':
            operation.quit()
            sock.send("Task quit".encode())
        elif data == 'exit':
            operation.quit()
            sock.send("Task exit".encode())
        sock.close()
        operation.logger.info('Connection from %s:%s closed.' % addr)
        operation.logger.info('------------------------------------------------------------')
        if data == 'exit':
            print('Program exit')
            sys.exit()


if __name__ == "__main__":
    p = Server()
    p.monitor()
