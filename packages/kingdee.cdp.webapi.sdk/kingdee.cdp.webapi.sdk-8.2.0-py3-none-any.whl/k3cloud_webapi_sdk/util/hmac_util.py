#!/usr/bin/python
# -*- coding:UTF-8 -*-
import hmac
import hashlib

from k3cloud_webapi_sdk.util import base64_util


def HmacSHA256(content, sign_key, encode_format='utf-8'):
    signature = hmac.new(bytes(sign_key, encode_format), bytes(content, encode_format), hashlib.sha256).digest()
    sign_hex = signature.hex()
    sign_hex = base64_util.encode(bytes(sign_hex, encode_format))
    return sign_hex
