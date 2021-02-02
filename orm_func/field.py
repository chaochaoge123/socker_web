#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2021/1/30 16:40
# @Author  : qqc
# @File    : file.py
# @Software: PyCharm
from orm_func.connect_mysql import *


class Field(object):
    """
    定义字段属性
    """

    def __init__(self, name, column_type, default, primary_key):
        self.name = name
        self.column_type = column_type
        self.default = default
        self.primary_key = primary_key

    def __str__(self):
        return "<%s:%s>" % (self.__class__.__name__, self.name)


class IntegerField(Field):
    def __init__(self, name, column_type='int(11)', default=0, primary_key=False):
        super(IntegerField, self).__init__(name, column_type, default, primary_key)


class StringField(Field):
    def __init__(self, name, column_type='varchar(100)', default='', primary_key=False):
        super(StringField, self).__init__(name, column_type, default, primary_key)


class PrimaryField(Field):
    def __init__(self, name, column_type='int(11)', default=0, primary_key=True):
        super(PrimaryField, self).__init__(name, column_type, default, primary_key)


class DatetimeField(Field):
    def __init__(self, name, column_type='DATE', default='1970-01-01', primary_key=False):
        super(DatetimeField, self).__init__(name, column_type, default, primary_key)


class ModelMetaclass(type):

    def __new__(cls, name, bases, attrs):
        if name == 'Model':
            return type.__new__(cls, name, bases, attrs)

        # 控制模型类的创建(必须指定主键和表名)
        if not attrs.get("__table__"):
            raise Exception("表名不存在")

        print('Found model: %s' % name)
        mappings = dict()
        is_primary_key = False
        primary_name = ''
        for k, v in attrs.items():
            if isinstance(v, Field):
                print('Found mapping: %s ==> %s' % (k, v))
                mappings[k] = v
                if v.primary_key:
                    is_primary_key = True
                    primary_name = v.name

        if not is_primary_key or not primary_name:
            raise Exception('未指定主键')
        for k in mappings.keys():
            attrs.pop(k)

        print(mappings, "##############")
        attrs['__mappings__'] = mappings  # 保存属性和列的映射关系
        attrs['table_name'] = attrs.get("__table__")  # 保存表名
        attrs['primary_name'] = primary_name  # 主键的字段名
        print(attrs)

        # 创建表
        cls.create_table(attrs)

        return type.__new__(cls, name, bases, attrs)

    @staticmethod
    def create_table(kwargs):
        """
        通过模型类的映射关系创建表
        (每次调用模型类时,没有对应的表就创建)
        :return:
        """
        column_str = ''

        for k, v in kwargs['__mappings__'].items():
            default_data = 0
            if 'int' in v.column_type:
                default_data = 'default %s' % v.default
            if 'varchar' in v.column_type:
                default_data = "default '' "
            if v.column_type == "DATE":
                default_data = "default '1970-01-01' "

            column_str += "`{0}` {1} {2},".format(v.name, v.column_type,
                                                  'AUTO_INCREMENT' if v.primary_key else default_data)

        create_sql = """
        CREATE TABLE IF NOT EXISTS `{0}`(
        {1}
        PRIMARY KEY (`{2}`)
        )ENGINE=InnoDB DEFAULT CHARSET=utf8;
        """.format(kwargs['table_name'], column_str, kwargs['primary_name'])

        print(create_sql, "create_sql_&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&")
        cursor_sql(create_sql)


class Model(dict, metaclass=ModelMetaclass):
    def __init__(self, **kwargs):
        super(Model, self).__init__(**kwargs)

    def __getattr__(self, key):
        try:
            return self[key]
        except KeyError:
            raise AttributeError(r"'Model' object has no attribute '%s'" % key)

    def __setattr__(self, key, value):
        self[key] = value

    def insert(self):
        fields = []
        args = []

        for k, v in self.__mappings__.items():
            default_data = ''
            if v.primary_key:
                if v.default:
                    default_data = v.default
                else:
                    # 自增id
                    res = cursor_sql("select id from {0} order by id desc limit 1 ".format(self.table_name))
                    default_data = res[0].get('id', 0) + 1 if res else 1
            else:
                default_data = v.default
            fields.append(v.name)
            args.append(getattr(self, k, default_data))
        sql = ' insert into %s (%s) values %s' % (self.__table__, ','.join(fields), tuple(args))
        cursor_sql(sql)
        print('SQL: %s' % sql)
        print('ARGS: %s' % str(args))

    def select(self, **kwargs):
        str_0 = ''
        if not kwargs:
            result = cursor_sql("select * from %s" % self.table_name)
            return result
        else:
            str_0 = self.get_where_str(kwargs)

        select_sql = " select * from %s where %s" % (self.table_name, str_0)
        print(select_sql, "*&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&")
        result = cursor_sql(select_sql)
        return result

    def update(self, filter_dict=None, update_dict=None):
        if not filter_dict and not update_dict:
            raise Exception('参数缺失')
        where_str = ''
        set_str = ''
        if filter_dict:
            where_str = self.get_where_str(filter_dict)
        if update_dict:
            set_str = self.get_where_str(update_dict, type=1)
        update_sql = " update %s set %s where %s" % (self.table_name, set_str, where_str)
        print(update_sql, "*********************************")
        cursor_sql(update_sql)

    def get_where_str(self, where_dict, type=0):
        str_w = ''
        where_str_list = []
        if not where_dict:
            return str_w

        for k in where_dict:
            where_str1 = " %s='%s'" % (k, where_dict[k])
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

    def delete(self):
        pass
