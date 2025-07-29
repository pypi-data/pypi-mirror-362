#!/usr/bin/python
# -*- coding:UTF-8 -*-


class ApiConfig:
    Xor_Code = ''

    def __init__(self):
			# 取消默认旧网关，要求必须输入url by Ann 2025-01-15
        # self.server_url = 'https://api.kingdee.com/galaxyapi/'
        self.server_url = ''
        self.dcid = ''
        self.user_name = ''
        self.app_id = ''
        self.app_secret = ''
        self.lcid = 2052
        self.org_num = 0
        self.connect_timeout = 120
        self.request_timeout = 120
        self.proxy = ''
