#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2021/1/31 10:52
# @Author  : qqc
# @File    : userinfo.py
# @Software: PyCharm

from orm_func.field import *
import datetime


class Logs(Model):
    __table__ = 'logs'
    id = PrimaryField(name='id')
    user_id = IntegerField(name='user_id', default=666)
    context = StringField(name='context', default='')
    create_time = DatetimeField(name='create_time')


# 创建
# ffg=Logs(user_id=325,context="记个c日志")
# print(ffg.insert())


ffs = Logs()
# 查找
res = ffs.select(id=1)
print(res, "##################")

# 更新(过滤条件的字段，更新的字段)
# ffs.update(filter_dict={"id":1}, update_dict={"context":"今天天气好"})
