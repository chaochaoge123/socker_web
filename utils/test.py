#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2021/1/30 11:17
# @Author  : qqc
# @File    : test.py
# @Software: PyCharm


# https://www.cnblogs.com/xiao-apple36/p/8673356.html#_label0
# https://www.cnblogs.com/hyit/articles/6474020.html
import socket
import time

test_da = b'GET /ddf/www?user_id=22&age=44 HTTP/1.1\r\nUser-Agent: PostmanRuntime/7.26.8\r\nAccept: */*\r\n' \
          b'Cache-Control: no-cache\r\nPostman-Token: f5cba65f-08d0-4de7-b798-3d7b2e8c2546\r\nHost: 127.0.0.1:8080\r\n' \
          b'Accept-Encoding: gzip, deflate, br\r\nConnection: keep-alive\r\n\r\n'

post_data=b'POST /ddf/www HTTP/1.1\r\nContent-Type: application/json\r\nUser-Agent: PostmanRuntime/7.26.8\r\n' \
          b'Accept: */*\r\nCache-Control: no-cache\r\nPostman-Token: 4d42e236-ecab-414f-9bfa-815e477153cb\r\n' \
          b'Host: 127.0.0.1:8080\r\nAccept-Encoding: gzip, deflate, br\r\nConnection: keep-alive' \
          b'\r\nContent-Length: 15\r\n\r\n{"user_id":444}'


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

    if mod == "GET":
        method = "GET"
        u_p_data = url_da.split('?')
        url = u_p_data[0]

        if len(u_p_data) > 0 and u_p_data[1]:
            params_str = u_p_data[1]

            dd = params_str.split('&')

            pas = {}
            for i in dd:
                p_list = i.split('=')
                pas.update({p_list[0]: p_list[1]})
            params = pas
    elif mod == "POST":
        method = "POST"
        url = url_da
        params = body

    else:
        return None

    return {"method": method, "params": params, "url": url, "headers": headers_dict}

print(get_request_params_url_method(test_da))



def client():
    import socket
    phone = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print(phone)

    phone.connect(('127.0.0.1', 8080))  # 指定服务端的IP和端口

    msg = input('<<<')
    phone.send(bytes(msg, encoding='utf-8'))  # 传输二进制
    data = phone.recv(1024)  # 收消息
    print(data)

    phone.close()


# class Hello(object):
#     def hello(self, name='word'):
#         print('Hello,%s'%name)
#
# h=Hello()
# print(h.hello(),type(Hello),type(h))

# def fn(self,name='word'):
#     print('hello,%s'%name)
#
# hell=type("Hello",(object,),dict(he=fn))
# h=hell()
# h.he()

class ListMetaclass(type):
    def __new__(cls, name,bases,attrs):
        attrs['add'] = lambda self,value:self.append(value)
        return type.__new__(cls,name,bases,attrs)