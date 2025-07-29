#!/usr/bin/python
# -*- coding:UTF-8 -*-


class QueryTaskParam:
    def __init__(self, task_id='', is_cancelled=False):
        self.TaskId = task_id
        self.Cancelled = is_cancelled
