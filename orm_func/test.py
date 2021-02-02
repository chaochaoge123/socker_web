#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2021/1/31 9:39
# @Author  : qqc
# @File    : test.py
# @Software: PyCharm

# class ListMetaclass(type):
#     def __new__(cls, name, bases, attrs):
#         attrs['add'] = lambda self, value: self.append(value)
#         return type.__new__(cls, name, bases, attrs)
#
#
# class Mylist(list, metaclass=ListMetaclass):
#     pass
#
#
# ggh=Mylist()
# print(ggh.addss(2))


# class FirstMetaClass(type):
#     # cls代表动态修改的类
#     # name代表动态修改的类名
#     # bases代表被动态修改的类的所有父类
#     # attr代表被动态修改的类的所有属性、方法组成的字典
#     def __new__(cls, name, bases, attrs):
#         # 动态为该类添加一个name属性
#         print(name,"SSSSSSSSSSSS",bases, attrs)
#         attrs['name'] = "C语言中文网"
#         attrs['say'] = lambda self: print("调用 say() 实例方法")
#         print(attrs,"AZZZZZZZZZZZZZZZZZZZZZ")
#         if attrs['table']<10:
#             raise Exception("table不合法")
#         return super().__new__(cls,name,bases,attrs)
#
# class CLanguage(object,metaclass=FirstMetaClass):
#     table=77
#
#     def test_onr(sele):
#         print("DDDDDDDDDDDDDDDD")
#     pass
# clangs = CLanguage()
# print(clangs.name)
# clangs.say()
# print(getattr(clangs,"say",None),"AAAAAAAAAA",)
# print(dict())


def jj(**kwargs):
    print(kwargs,"AAAAAAAAAAAA")

print(jj(),"DDD")


ffff={'rr': '33'}


def get_where_str(where_dict,type=0):
    str_w = ''
    where_str_list = []
    if not where_dict:
        return str_w

    for k in where_dict:
        where_str1 = " %s=%s" % (k, where_dict[k])
        where_str_list.append(where_str1)
    str_w = where_str_list[0]
    if len(where_str_list) > 1:
        str_w = where_str_list.pop(0)
        for i in where_str_list:
            if type == 0:
                str_w += " and %s" % i
            else:
                str_w += " , %s" % i
    return str_w
print(get_where_str(ffff,type=0),"XXX")