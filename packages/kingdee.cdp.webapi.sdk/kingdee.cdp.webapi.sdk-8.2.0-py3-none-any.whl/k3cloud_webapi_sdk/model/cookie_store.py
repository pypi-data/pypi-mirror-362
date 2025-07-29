#!/usr/bin/python
# -*- coding:UTF-8 -*-


class CookieStore:
    def __init__(self, sid='', cookies=None):
        if cookies is None:
            cookies = {}
        self.SID = sid
        self.cookies = cookies

    def set_sid(self, sid):
        if sid != '' and sid is not None:
            self.SID = sid
