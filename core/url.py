#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2021/1/30 13:27
# @Author  : qqc
# @File    : url.py
# @Software: PyCharm

from .view import *

url_dict = {
    '/api/v1/test': test_api_v1,
    '/api/v2/test': test_api_v2,
    '/api/v1/test/templates/login': test_templates_login,
}
