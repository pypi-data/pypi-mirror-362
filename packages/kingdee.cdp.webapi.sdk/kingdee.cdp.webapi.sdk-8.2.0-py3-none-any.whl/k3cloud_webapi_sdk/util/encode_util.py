#!/usr/bin/python
# -*- coding:UTF-8 -*-
import random

from k3cloud_webapi_sdk.model.api_config import ApiConfig
from k3cloud_webapi_sdk.util import base64_util


def DecodeAppSecret(app_secret):
    if len(app_secret) != 32:
        return ''
    else:
        base64_decode = base64_util.decode(app_secret)
        base64_xor = xor_code(base64_decode)
        return base64_util.encode(base64_xor)


def extend_byte_array(origin, encoding=None, extend_type=0):
    if extend_type == 0:
        return bytearray(rot(origin), encoding=encoding)
    else:
        gene_str = ''
        for i in range(0, 4):
            gene_str += origin[i * 9:(i * 9 + 8)]
        return bytearray(rot(gene_str), encoding=encoding)


def xor_code(byte_array):
    pwd_array = extend_byte_array(generate_code(), encoding='utf-8', extend_type=1)
    out_array = bytearray()
    for i in range(0, len(byte_array)):
        out_array.insert(i, byte_array[i] ^ pwd_array[i])

    return out_array


def encode_char(ch):
    f = lambda x: chr((ord(ch) - x + 13) % 26 + x)
    return f(97) if ch.islower() else (f(65) if ch.isupper() else ch)


def rot(s):
    return ''.join(encode_char(c) for c in s)


def generate_code():
    ret_code = ''
    rand = str(random.randint(1000, 9999))
    if ApiConfig.Xor_Code == '':
        ret_code += '0054s397' + rand[0]
        ret_code += 'p6234378' + rand[1]
        ret_code += 'o09pn7q3' + rand[2]
        ret_code += 'r5qropr7' + rand[3]
    else:

        for i in range(0, 4):
            ret_code += ApiConfig.Xor_Code[i * 8: (i + 1) * 8] + rand[i]
    return ret_code
