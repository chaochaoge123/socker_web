#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2021/2/18 14:44
# @Author  : qqc
# @File    : web_client.py
# @Software: PyCharm


import websocket

header=["user_id:33"]
ws = websocket.create_connection("ws://127.0.0.1:5000/ws/v1/user/one/chet/qqc1", header=header)

# print("发送中...")

while True:
    msgs=input("shuru")
    ws.send(msgs)

    result = ws.recv()
    print("返回结果：%s" % result)


