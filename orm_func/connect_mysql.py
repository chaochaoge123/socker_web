#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/12/10 11:17
# @Author  : qqc
# @File    : connect_mysql.py
# @Software: PyCharm


import pymysql
from config import config_params



def connect():
    db = pymysql.connect(host=config_params.DB_HOST, user=config_params.DB_USER, password=config_params.DB_PASSWORD,
                         database=config_params.DB_NAME, port=config_params.DB_PORT)
    cur = db.cursor(cursor=pymysql.cursors.DictCursor)
    return db, cur


def cursor_sql(sql_str):

    # sql_str="select * from logs"
    results = []
    db, cur = connect()
    try:
        cur.execute(sql_str)
        db.commit()
        results = cur.fetchall()
        db.close()
        cur.close()
    except Exception as e:
        print(e, "#################")
        db.rollback()
        return []

    return results
