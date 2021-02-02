#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2021/1/30 13:29
# @Author  : qqc
# @File    : __init__.py.py
# @Software: PyCharm

import os

PROJECT_PATH = os.path.dirname(os.path.abspath(os.path.dirname(__file__)))
print("PROJECT_PATH:", PROJECT_PATH)


def get_env_config():
    env_mode = os.environ.get("ENV_MODE")
    print("ENV_MODE: %s" % env_mode)
    if env_mode == "develop":
        from config.develop import DevelopConfig
        return DevelopConfig
    elif env_mode == "product":
        from config.product import ProductConfig
        return ProductConfig
    else:
        from config.develop import DevelopConfig
        return DevelopConfig


config_params = get_env_config()
