#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2021/2/2 17:05
# @Author  : qqc
# @File    : client.py
# @Software: PyCharm


import asyncio
import websockets

async def hello():
    async with websockets.connect('ws://127.0.0.1:8765') as websocket:
        name = input("What's your name? ")

        await websocket.send(name)
        print(f"> {name}")

        greeting = await websocket.recv()
        print(f"< {greeting}")

asyncio.get_event_loop().run_until_complete(hello())

