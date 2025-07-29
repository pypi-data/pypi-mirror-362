#!/usr/bin/python
# -*- coding:UTF-8 -*-
import string

base64_charset = string.ascii_uppercase + string.ascii_lowercase + string.digits + '+/'


def encode(origin_bytes):
    base64_bytes = ['{:0>8}'.format(str(bin(b)).replace('0b', '')) for b in origin_bytes]

    resp = ''
    nums = len(base64_bytes) // 3
    remain = len(base64_bytes) % 3

    integral_part = base64_bytes[0:3 * nums]
    while integral_part:
        tmp_unit = ''.join(integral_part[0:3])
        tmp_unit = [int(tmp_unit[x: x + 6], 2) for x in [0, 6, 12, 18]]
        resp += ''.join([base64_charset[i] for i in tmp_unit])
        integral_part = integral_part[3:]

    if remain:
        remain_part = ''.join(base64_bytes[3 * nums:]) + (3 - remain) * '0' * 8
        tmp_unit = [int(remain_part[x: x + 6], 2) for x in [0, 6, 12, 18]][:remain + 1]
        resp += ''.join([base64_charset[i] for i in tmp_unit]) + (3 - remain) * '='
    return resp


def decode(base64_str):
    if not valid_base64_str(base64_str):
        return bytearray()

    base64_bytes = ['{:0>6}'.format(str(bin(base64_charset.index(s))).replace('0b', '')) for s in base64_str if
                    s != '=']
    resp = bytearray()
    nums = len(base64_bytes) // 4
    remain = len(base64_bytes) % 4
    integral_part = base64_bytes[0:4 * nums]

    while integral_part:
        tmp_unit = ''.join(integral_part[0:4])
        tmp_unit = [int(tmp_unit[x: x + 8], 2) for x in [0, 8, 16]]
        for i in tmp_unit:
            resp.append(i)
        integral_part = integral_part[4:]

    if remain:
        remain_part = ''.join(base64_bytes[nums * 4:])
        tmp_unit = [int(remain_part[i * 8:(i + 1) * 8], 2) for i in range(remain - 1)]
        for i in tmp_unit:
            resp.append(i)

    return resp


def valid_base64_str(b_str):
    if len(b_str) % 4:
        return False

    for m in b_str:
        if m not in base64_charset:
            return False
    return True
