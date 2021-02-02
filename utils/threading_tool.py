#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2021/1/30 14:35
# @Author  : qqc
# @File    : threading_tool.py
# @Software: PyCharm


from concurrent.futures import ThreadPoolExecutor, as_completed

def threading_pool_tool(worker, params):
    with ThreadPoolExecutor(4) as executor:
        da = ''
        if params:
            da = [executor.submit(worker, params)
                  ]
        else:
            da = [executor.submit(worker)
                  ]
        for future in as_completed(da):
            data = future.result()
            print(data, "******************************************")
            return data
