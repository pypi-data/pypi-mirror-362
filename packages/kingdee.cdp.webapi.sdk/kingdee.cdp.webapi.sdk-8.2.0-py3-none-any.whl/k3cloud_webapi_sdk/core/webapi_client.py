#!/usr/bin/python
# -*- coding:UTF-8 -*-
import json
from urllib.parse import quote
from urllib.parse import urlparse
import requests
import time
import urllib3

from k3cloud_webapi_sdk.const.const_define import InvokeMethod, QueryMode, QueryState
from k3cloud_webapi_sdk.const.header_param import HeaderParam
from k3cloud_webapi_sdk.model import cookie
from k3cloud_webapi_sdk.model.cookie_store import CookieStore
from k3cloud_webapi_sdk.model.identity import Identify
from k3cloud_webapi_sdk.model.query_param import QueryTaskParam
from k3cloud_webapi_sdk.util import encode_util, hmac_util, base64_util
from urllib3.exceptions import InsecureRequestWarning

urllib3.disable_warnings(InsecureRequestWarning)


def ValidResult(response_content):
    if response_content.startswith('response_error:'):
        res_error = response_content.rstrip('response_error:').strip()
        if res_error != '':
            raise RuntimeError(res_error)
        else:
            raise RuntimeError('Empty exception message')
    else:
        return response_content


class WebApiClient:

    def __init__(self):
        self.initialize = False
        self.config = None
        self.identify = None
        self.cookiesStore = CookieStore()
        self.connectTimeout = 120
        self.requestTimeout = 120
        self.proxy = ''

    def Init(self, server_url, timeout, sdk_initialize):
        self.initialize = sdk_initialize
        if self.config is None:
            raise RuntimeError('Configuration file unload, you need initial config firstly!')
        if server_url == '':
            # 取消默认旧网关，要求必须输入url by Ann 2025-01-15
            # server_url = self.config.server_url
            raise RuntimeError('ServerUrl is required')
        self.identify = Identify(server_url, self.config.dcid, self.config.user_name, self.config.app_id,
                                 self.config.app_secret, self.config.org_num, self.config.lcid, '')
        if self.config.connect_timeout > 0:
            self.connectTimeout = self.config.connect_timeout
        if self.config.request_timeout > 0:
            self.requestTimeout = self.config.request_timeout
        if timeout > 0:
            self.requestTimeout = timeout
        if self.config.proxy != '':
            self.proxy = self.config.proxy
        return self

    def BuildHeader(self, service_url):
        path_url = service_url
        if service_url.startswith('http'):
            p_index = service_url.index('/', 10)
            if p_index > -1:
                path_url = service_url[p_index:]
        path_url = quote(path_url, encoding='utf-8').replace('/', '%2F')
        time_stamp = str(int(time.time()))
        nonce = str(int(time.time()))
        client_id = ''
        client_sec = ''
        arr = self.identify.AppId.split('_')
        if len(arr) == 2:
            client_id = arr[0]
            client_sec = encode_util.DecodeAppSecret(arr[1])

        api_sign = 'POST\n' + path_url + '\n\nx-api-nonce:' + nonce + '\nx-api-timestamp:' + time_stamp + '\n'
        app_data = self.identify.DCID + ',' + self.identify.UserName + ',' + str(self.identify.LCID) + ',' + str(
            self.identify.OrgNum)

        dic_header = {HeaderParam.X_Api_ClientID: client_id, HeaderParam.X_Api_Auth_Version: '2.0',
                      HeaderParam.X_Api_Timestamp: time_stamp,
                      HeaderParam.X_Api_Nonce: nonce,
                      HeaderParam.X_Api_SignHeaders: 'x-api-timestamp,x-api-nonce',
                      HeaderParam.X_Api_Signature: hmac_util.HmacSHA256(api_sign, client_sec),
                      HeaderParam.X_KD_AppKey: self.identify.AppId,
                      HeaderParam.X_KD_AppData: base64_util.encode(bytes(app_data, 'utf-8')),
                      HeaderParam.X_KD_Signature: hmac_util.HmacSHA256(self.identify.AppId + app_data,
                                                                       self.identify.AppSecret)}

        if self.cookiesStore.SID != '':
            dic_header[HeaderParam.KDService_SessionId] = self.cookiesStore.SID
        if len(self.cookiesStore.cookies) > 0:
            cookie_str = 'Theme=standard'
            for k, v in self.cookiesStore.cookies.items():
                cookie_str += ';' + v.ToString()
            dic_header['Cookie'] = cookie_str

        dic_header['Accept-Charset'] = 'utf-8'
        dic_header['User-Agent'] = 'Kingdee/Python WebApi SDK 7.3 (compatible; MSIE 6.0; Windows NT 5.1;SV1)'
        dic_header['Content-Type'] = 'application/json'

        return dic_header

    def PostJson(self, service_name, json_data=None, invoke_type=InvokeMethod.SYNC):
        if json_data is None:
            json_data = {}
        if self.identify.ServerUrl.endswith('/'):
            req_url = self.identify.ServerUrl + service_name + '.common.kdsvc'
        else:
            req_url = self.identify.ServerUrl + '/' + service_name + '.common.kdsvc'

        proxies = None
        if self.proxy != '':
            proxy_url = urlparse(self.proxy)
            proxy_scheme = proxy_url.scheme
            proxies = {proxy_scheme: self.proxy}

        if invoke_type == InvokeMethod.QUERY:
            json_data[QueryMode.BeginMethod_Header.value] = QueryMode.BeginMethod_Method.value
            json_data[QueryMode.QueryMethod_Header.value] = QueryMode.QueryMethod_Method.value

        res = requests.post(url=req_url, headers=self.BuildHeader(req_url), data=json.dumps(json_data),
                            proxies=proxies, timeout=(self.connectTimeout, self.requestTimeout), verify=False)

        if res.status_code == requests.codes.ok or res.status_code == requests.codes.partial:
            self.FillCookieAndHeader(res.cookies, res.headers)
            return ValidResult(res.text)
        else:
            raise RuntimeError(res.text)

    def FillCookieAndHeader(self, cookies, headers):
        self.cookiesStore.set_sid(cookies.get(HeaderParam.KDService_SessionId))
        if HeaderParam.Cookie_Set in headers:
            self.cookiesStore.cookies.clear()
            for item in headers[HeaderParam.Cookie_Set].split(','):
                ck = cookie.parse(item)
                if ck is not None:
                    self.cookiesStore.cookies[ck.name] = ck

    def Execute(self, service_name, json_data=None, invoke_type=InvokeMethod.SYNC):
        if not self.initialize:
            return RuntimeError('拒绝请求，请先正确初始化!')
        if self.config is None:
            raise RuntimeError('请先初始化SDK配置信息!')
        if invoke_type == InvokeMethod.SYNC:
            return self.PostJson(service_name, json_data, InvokeMethod.SYNC)
        elif invoke_type == InvokeMethod.QUERY:
            return self.ExecuteByQuery(service_name, json_data)
        else:
            raise RuntimeError('Not support for InvokeMode:' + str(invoke_type))

    def ExecuteByQuery(self, service_name, json_data=None):
        response_content = self.PostJson(service_name, json_data, InvokeMethod.QUERY)
        json_result = json.loads(response_content)
        if json_result['Status'] == QueryState.Complete.value:
            return json.dumps(json_result['Result'])
        else:
            return self.QueryTaskResult(service_name, {'TaskId': json_result['TaskId'], 'Cancelled': False}, 5)

    def QueryTaskResult(self, service_name, param, retry_count):
        try:
            time.sleep(1)
            query_service = service_name[0:service_name.rindex('.')] + '.' + QueryMode.QueryMethod_Method.value
            response_content = self.PostJson(query_service, {'queryInfo': json.dumps(param)}, InvokeMethod.SYNC)
            json_result = json.loads(response_content)
            if json_result['Status'] == QueryState.Complete.value:
                return json.dumps(json_result['Result'])
            else:
                return self.QueryTaskResult(service_name, param, 5)
        except RuntimeError as err:
            if retry_count > 0:
                return self.QueryTaskResult(service_name, param, retry_count - 1)
            else:
                raise err
