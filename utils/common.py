#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2021/1/30 13:30
# @Author  : qqc
# @File    : common.py
# @Software: PyCharm

import socket
import json
from core import *
import threading
from utils.threading_tool import *


# 解析请求数据
def get_request_params_url_method(da):
    """ 获取参数,路由,请求方式,其他头部信息
    """
    method = ''
    params = ''
    url = ''

    data = str(da, encoding='utf-8')
    headers, body = data.split('\r\n\r\n')
    temp_list = headers.split('\r\n')
    headers_dict = {}
    for h in temp_list:
        if ":" in h:
            h_list = h.split(':')
            headers_dict.update({h_list[0]: h_list[1]})
    mod, url_da, http = temp_list[0].split(' ')
    print(mod, url_da, http, "############################")

    if mod == "GET":
        method = "GET"
        u_p_data = url_da.split('?')
        url = u_p_data[0]

        if len(u_p_data) > 1:
            params_str = u_p_data[1]
            if params_str:
                dd = params_str.split('&')

                pas = {}
                for i in dd:
                    p_list = i.split('=')
                    pas.update({p_list[0]: p_list[1]})
                params = pas
    elif mod == "POST":
        method = "POST"
        url = url_da
        params = json.loads(body)

    else:
        return None

    return {"method": method, "params": params, "url": url, "headers": headers_dict}


def matching_url(url_str, params):
    """ 匹配用户输入的url"""

    if url_str in url_dict:
        res = threading_pool_tool(url_dict[url_str], params)
        return res
    else:
        return {"code": 0, "msg": "url not found"}


def run_server(ip='127.0.0.1', port=8000):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as phone:
    # phone = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # 网络通信种类，tcp 协议 流式协议
        phone.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  # 重新用端口
        phone.bind((ip, port))
        phone.listen(5)

        # 等待消息
        print('start............')
        while True:
            conn, addr = phone.accept()
            data = conn.recv(1024)

            analysis_data = get_request_params_url_method(data)
            if not analysis_data:
                conn.send(bytes("请求方法错误", encoding='utf-8'))

            # 匹配路由
            result = matching_url(analysis_data['url'], analysis_data['params'])

            # 响应头信息
            conn.send(b"HTTP/1.1 200 OK\r\n Content-Type: application/json\r\n\r\n")

            if "tem" in analysis_data['url']:  # tem 关键字为模板请求
                conn.send(result)
            else:
                conn.send(json.dumps(result).encode())

            conn.close()
