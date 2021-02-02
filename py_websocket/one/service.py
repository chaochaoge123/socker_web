#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2021/2/2 16:59
# @Author  : qqc
# @File    : py_websocket.py
# @Software: PyCharm

import websockets

import asyncio
import websockets

# https://websockets.readthedocs.io/en/stable/intro.html
# https://www.yiibai.com/websocket/python-websockets-library.html
async def hello(websocket, path):
    name = await websocket.recv()
    print(name)

    greeting = "Hello {name}!".format(name=name)

    await websocket.send(greeting)
    print(greeting)

start_server = websockets.serve(hello, '127.0.0.1', 8765)
print('start....................')

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()

