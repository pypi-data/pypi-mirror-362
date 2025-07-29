#!/usr/bin/python
# -*- coding:UTF-8 -*-
import configparser
import os

from k3cloud_webapi_sdk.model.api_config import ApiConfig


def InitConfig(config_path, config_node):
    if config_path == '':
        raise RuntimeError('Init config failed: Lack of config path!')
    filepath = os.path.abspath(config_path)
    if not os.path.exists(filepath):
        raise RuntimeError('Init config failed: Config file[' + filepath + '] not found!')
    if config_node == '':
        raise RuntimeError('Init config failed: Lack of config node!')
    assign_api_config = ApiConfig()
    conf = configparser.ConfigParser()
    conf.read(filepath, encoding='utf-8')
    if conf.get(config_node, 'x-kdapi-serverurl', fallback='') != '':
        assign_api_config.server_url = conf.get(config_node, 'x-kdapi-serverurl', fallback='')
    assign_api_config.dcid = conf.get(config_node, 'x-kdapi-acctid', fallback='')
    assign_api_config.user_name = conf.get(config_node, 'x-kdapi-username', fallback='')
    assign_api_config.app_id = conf.get(config_node, 'x-kdapi-appid', fallback='')
    assign_api_config.app_secret = conf.get(config_node, 'x-kdapi-appsec', fallback='')
    assign_api_config.lcid = conf.getint(config_node, 'x-kdapi-lcid', fallback=2052)
    assign_api_config.org_num = conf.getint(config_node, 'x-kdapi-orgnum', fallback=0)
    assign_api_config.connect_timeout = conf.getint(config_node, 'x-kdapi-connecttimeout', fallback=120)
    assign_api_config.request_timeout = conf.getint(config_node, 'x-kdapi-requesttimeout', fallback=120)
    assign_api_config.proxy = conf.get(config_node, 'x-kdapi-proxy', fallback='')
    if conf.get(config_node, 'x-kdapi-secpwd', fallback='') != '':
        ApiConfig.Xor_Code = conf.get(config_node, 'x-kdapi-secpwd', fallback='')

    return assign_api_config


def InitConfigByParams(acct_id, user_name, app_id, app_secret, server_url, lcid=2052, org_num=0, connect_timeout=120,
                       request_timeout=120, proxy=''):
    assign_api_config = ApiConfig()
    if server_url != '':
        assign_api_config.server_url = server_url
    else:
    # 取消默认旧网关，要求必须输入url by Ann 2025-01-15
        raise RuntimeError('ServerUrl is required')
    assign_api_config.dcid = acct_id
    assign_api_config.user_name = user_name
    assign_api_config.app_id = app_id
    assign_api_config.app_secret = app_secret
    assign_api_config.lcid = lcid if lcid > 0 else 2052
    assign_api_config.org_num = org_num if org_num > 0 else 0
    assign_api_config.connect_timeout = connect_timeout if connect_timeout > 0 else 120
    assign_api_config.request_timeout = request_timeout if request_timeout > 0 else 120
    assign_api_config.proxy = proxy
    return assign_api_config
