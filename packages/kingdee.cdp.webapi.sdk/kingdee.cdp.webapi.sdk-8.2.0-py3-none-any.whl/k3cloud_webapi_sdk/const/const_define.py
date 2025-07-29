#!/usr/bin/python
# -*- coding:UTF-8 -*-
from enum import Enum


class InvokeMethod(Enum):
    SYNC = 1
    ASYNC = 2
    QUERY = 3


class QueryState(Enum):
    Pending = 0
    Running = 1
    Complete = 2


class QueryMode(Enum):
    BeginMethod_Header = 'beginmethod'
    BeginMethod_Method = 'BeginQueryImpl'
    QueryMethod_Header = 'querymethod'
    QueryMethod_Method = 'QueryAsyncResult'
