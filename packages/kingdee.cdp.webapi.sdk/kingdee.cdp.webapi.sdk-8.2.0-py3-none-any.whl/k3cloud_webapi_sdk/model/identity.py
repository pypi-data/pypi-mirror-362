#!/usr/bin/python
# -*- coding:UTF-8 -*-


class Identify:
    def __init__(self, server_url, dcid, user_name, app_id, app_secret, org_num, lcid=2052, pwd=''):
        self.ServerUrl = server_url
        self.DCID = dcid
        self.LCID = lcid
        self.UserName = user_name
        self.Pwd = pwd
        self.AppId = app_id
        self.AppSecret = app_secret
        self.OrgNum = org_num
