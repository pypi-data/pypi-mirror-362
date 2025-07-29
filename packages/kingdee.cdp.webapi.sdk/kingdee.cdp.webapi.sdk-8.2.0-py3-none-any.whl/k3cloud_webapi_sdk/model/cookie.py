#!/usr/bin/python
# -*- coding:UTF-8 -*-


class Cookie:
    def __init__(self, cookie=''):
        self.name = ''
        self.value = ''
        self.path = ''
        self.domain = ''
        self.secure = False
        if cookie != '':
            arr = cookie.split(';')
            for i in range(0, len(arr)):
                item = arr[i].rstrip().split('=', 1)
                if len(item) == 2:
                    if item[0].lower() == 'expires':
                        continue
                    elif item[0].lower() == 'path':
                        self.path = item[1]
                    elif item[0].lower() == 'domain':
                        self.domain = item[1]
                    elif i == 0:
                        self.name = item[0]
                        self.value = item[1]
                elif arr[i].rstrip() == 'SECURE':
                    self.secure = True

    def ToString(self):
        return self.name + '=' + self.value


def parse(ck):
    c = Cookie(ck)
    if c.name == '':
        return None
    else:
        return c
