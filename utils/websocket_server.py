#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2021/2/2 14:33
# @Author  : qqc
# @File    : websocket.py
# @Software: PyCharm
import socket
import base64
import hashlib
from threading import Thread


ws_data="GET / HTTP/1.1\r\n" \
        "Host: 127.0.0.1:8080\r\n" \
        "Connection: Upgrade\r\n" \
        "Pragma: no-cache\r\n" \
        "Cache-Control: no-cache\r\n" \
        "User-Agent: Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.104 Safari/537.36\r\n" \
        "Upgrade: websocket\r\n" \
        "Origin: http://localhost:63342\r\n" \
        "Sec-WebSocket-Version: 13\r\n" \
        "Accept-Encoding: gzip, deflate, br\r\n" \
        "Accept-Language: zh-CN,zh;q=0.9\r\n" \
        "Sec-WebSocket-Key: kvwY6ROhDOdBl/LkyAfaQw==\r\n" \
        "Sec-WebSocket-Extensions: permessage-deflate; client_max_window_bits\r\n" \
        "\r\n"


def get_ws_header_data(data):
    """ 解析请求头信息 """
    header_dict = {}
    data = str(data, encoding="utf-8")
    header, body = data.split("\r\n\r\n", 1)
    header_list = header.split("\r\n")

    for i in range(0,len(header_list)):
        if i == 0:
            if len(header_list[0].split(" ")) == 3:
                header_dict['method'], header_dict['url'], header_dict['protocol'] = header_list[0].split(" ")
        else:
            k, v = header_list[i].split(":", 1)
            header_dict[k] = v.strip()
    return header_dict



def get_data(info):
    """ 解析客户端信息 """
    payload_len = info[1] & 127
    if payload_len == 126:
        extend_payload_len = info[2:4]
        mask = info[4:8]
        decoded = info[8:]
    elif payload_len == 127:
        extend_payload_len = info[2:10]
        mask = info[10:14]
        decoded = info[14:]
    else:
        extend_payload_len = None
        mask = info[2:6]
        decoded = info[6:]

    bytes_list = bytearray()    #这里我们使用字节将数据全部收集，再去字符串编码，这样不会导致中文乱码
    for i in range(len(decoded)):
        chunk = decoded[i] ^ mask[i % 4]    #解码方式
        bytes_list.append(chunk)
    body = str(bytes_list, encoding='utf-8')
    return body


def sha_sec_websocket_key(headers):
    """ 加密 sec-websocket-key
    请求和响应的【握手】信息需要遵循规则：
    从请求【握手】信息中提取 Sec-WebSocket-Key
    利用magic_string 和 Sec-WebSocket-Key 进行hmac1加密，再进行base64加密
    将加密结果响应给客户端
    注：magic string为：258EAFA5-E914-47DA-95CA-C5AB0DC85B11
    """
    magic_string = '258EAFA5-E914-47DA-95CA-C5AB0DC85B11'

    value = headers['Sec-WebSocket-Key'] + magic_string
    ac = base64.b64encode(hashlib.sha1(value.encode('utf-8')).digest())

    response_tpl = "HTTP/1.1 101 Switching Protocols\r\n" \
                   "Upgrade:websocket\r\n" \
                   "Connection: Upgrade\r\n" \
                   "Sec-WebSocket-Accept: %s\r\n" \
                   "WebSocket-Location: ws://%s%s\r\n\r\n"

    response_str = response_tpl % (ac.decode('utf-8'), headers['Host'], headers['url'])
    return response_str


def send_msg(conn, msg_bytes):
    import struct

    token = b"\x81"  # 接收的第一字节，一般都是x81不变
    length = len(msg_bytes)
    if length < 126:
        token += struct.pack("B", length)
    elif length <= 0xFFFF:
        token += struct.pack("!BH", 126, length)
    else:
        token += struct.pack("!BQ", 127, length)

    msg = token + msg_bytes
    conn.send(msg)
    return True


def create_socket_server(bind_info):
    phone = socket.socket()
    phone.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  # 重新用端口
    # phone.setblocking(0)
    # phone.settimeout(10)
    phone.bind(bind_info)
    phone.listen(5)
    print('server start 127.0.0.1:8080 ............')
    return phone



def accept_client():
    global client_loop
    server_obj=create_socket_server(('127.0.0.1', 8080))
    while True:
        client_conn, address=server_obj.accept()
        data = client_conn.recv(1024)
        # 解析请求头信息
        headers = get_ws_header_data(data)
        # 加密
        response_str = sha_sec_websocket_key(headers)
        print(response_str, "$$$$$$$$$$$$$$$$$$$$$$")

        # 发送响应信息
        client_conn.send(bytes(response_str, encoding='utf-8'))

        send_msg(client_conn, "连接服务器成功!".encode(encoding='utf8'))

        # 加入客户端连接池
        client_loop.append(client_conn)

        thread = Thread(target=massage_interactive, args=(client_conn,))
        # 设置成守护线程
        thread.setDaemon(True)
        thread.start()
        return client_conn


def massage_interactive(client_conn):
    global client_loop
    while True:
        client_data = client_conn.recv(8096)

        client_data = get_data(client_data)
        print("获取客户端的消息：---%s" % client_data)

        # 回复客户端信息
        send_msg(client_conn, bytes(client_data + "hello", encoding="utf-8"))



if __name__ == '__main__':
    client_loop = []
    while True:
        server_obj = create_socket_server(('127.0.0.1', 8080))

        client_conn, address = server_obj.accept()
        data = client_conn.recv(1024)
        # 解析请求头信息
        headers = get_ws_header_data(data)
        print("请求头信息%s"% headers)
        # 加密
        response_str = sha_sec_websocket_key(headers)
        print(response_str, "$$$$$$$$$$$$$$$$$$$$$$")

        # 发送响应信息
        client_conn.send(bytes(response_str, encoding='utf-8'))

        send_msg(client_conn, "连接服务器成功!".encode(encoding='utf8'))

        # 加入客户端连接池
        if client_conn not in client_loop:
            client_loop.append({"client":client_conn})

        thread = Thread(target=massage_interactive, args=(client_conn,))
        # 设置成守护线程
        thread.setDaemon(True)
        thread.start()
        cmd = input("""--------------------------
        输入1:查看当前在线人数
        输入2:给指定客户端发送消息
        输入3:关闭服务端
        """)
        if cmd == '1':
            print("--------------------------")
            print("当前在线人数：", len(client_loop), client_loop)
        elif cmd == '2':
            print("--------------------------")
            index, msg = input("请输入“索引,消息”的形式：").split(",")
            client_loop[int(index)].sendall(msg.encode(encoding='utf8'))
        elif cmd == '3':
            exit()

# with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as phone:
#     # phone = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # 网络通信种类，tcp 协议 流式协议
#     phone.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  # 重新用端口
#     phone.bind(('127.0.0.1', 8080))
#     phone.listen(5)
#
#     # 等待消息
#     print('server start 127.0.0.1:8080 ............')
#     while True:
#         conn, addr = phone.accept()
#         data = conn.recv(1024)
#         print(data)
#         headers=get_ws_header_data(data)
#
#         #加密
#         response_str = sha_sec_websocket_key(headers)
#         print(response_str, "$$$$$$$$$$$$$$$$$$$$$$")
#
#         # 发送响应信息
#         conn.send(bytes(response_str, encoding='utf-8'))
#
#         while True:
#             client_data = conn.recv(8096)
#             client_data = get_data(client_data)
#             print("获取客户端的消息：---%s" % client_data)
#
#             # 回复客户端信息
#             send_msg(conn, bytes(client_data+"hello", encoding="utf-8"))

# https://www.cnblogs.com/ssyfj/p/9245150.html

