#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2021/2/18 17:12
# @Author  : qqc
# @File    : socket_server.py
# @Software: PyCharm

from socket import *
from threading import Thread


def talk(conn, addr):
    print("子进程开始.")
    while 1:
        try:
            client_from_msg = conn.recv(1024)
            print("来自客户端%s端口%s的消息: " % (addr[0], addr[1]), client_from_msg)
            if not client_from_msg: break
            conn.send(client_from_msg.upper())
        except Exception:
            break


if __name__ == '__main__':
    print("主进程开始.")
    server = socket()
    ip_port = ("127.0.0.1", 8080)
    server.bind(ip_port)
    server.listen(5)
    while 1:
        conn, client_addr = server.accept()
        print(conn, client_addr)
        p = Thread(target=talk, args=(conn, client_addr))
        p.start()