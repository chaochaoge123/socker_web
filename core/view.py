#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2021/1/30 13:27
# @Author  : qqc
# @File    : view.py
# @Software: PyCharm

def test_api_v1():
    return {"msg": "successful"}


def test_api_v2(params):
    return {"mag": "successful,用户id:%s,用户名：%s" % (params['user_id'], params['user_name'])}


def test_templates_login():
    with open(r'C:\Users\admin\Desktop\MiPush_Server_Python_20170704\xmpush-python-1.0.4\socket_tool\templates\one.html', 'rb') as f:
        data=f.read()
        return data