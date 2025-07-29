#!/usr/bin/python
# -*- coding: utf-8 -*-
import time

from k3cloud_webapi_sdk.main import K3CloudApiSdk

def Demo_For_Save(sdk):
    list_seq = gen_seq(1)
    # 构造保存接口的部分字段数据，使用时请参考WebAPI具体接口的实际参数列表
    save_data = {"Model": {
        "FCreateOrgId": {"FNumber":100},
        "FUserOrgId": {"FNumber":100},
        "FNumber": "wg" + list_seq[0],
        "FName": "wg-物料名称-" + list_seq[0]
    }}

    # 调用SDK中的同步模式的批量保存接口
    return sdk.Save("BD_Material", save_data)

def Demo_For_BillQuery(sdk):
    # 构造保存接口的部分字段数据，使用时请参考WebAPI具体接口的实际参数列表
    query_data = {
    "FormId": "BD_MATERIAL",
    "FieldKeys": "FNumber"
    }
    # 调用SDK中的同步模式的批量保存接口
    return sdk.ExecuteBillQuery(query_data)

def Demo_For_SwitchOrg(sdk):
    #list_seq = gen_seq(1)
    # 构造保存接口的部分字段数据，使用时请参考WebAPI具体接口的实际参数列表
    # save_data = {"Model": {
    #     "FCreateOrgId": {"FNumber": 100},
    #     "FUserOrgId": {"FNumber": 100},
    #     "FNumber": "Webb" + list_seq[0],
    #     "FName": "物料名称-" + list_seq[0]
    # }}
    data={"Model":{
    "FSALEORGID": {"FNumber": 102}
    }}
    # 调用SDK中的同步模式的批量保存接口
    return sdk.SwitchOrg(data)

# def Demo_For_BatchSave(sdk, count, query=False):
#     list_seq = gen_seq(count)
#     # 构造批量保存接口的部分字段数据，使用时请参考WebAPI具体接口的实际参数列表
#     list_data = []
#     for i in range(0, count):
#         list_data.append({
#             "FCreateOrgId": {"FNumber": 100},
#             "FUserOrgId": {"FNumber": 100},
#             "FNumber": "Webb" + list_seq[i],
#             "FName": "物料名称-" + list_seq[i]
#         })
#     save_data = {"Model": list_data}
#     if query:
#         # 调用SDK中的轮询模式的批量保存接口
#         return sdk.BatchSaveQuery("BD_Material", save_data)
#     else:
#         # 调用SDK中的同步模式的批量保存接口
#         return sdk.BatchSave("BD_Material", save_data)
#

def gen_seq(loop_count):
    # 此方法仅为生成物料编码的演示数据而写，使用时以实际数据为准
    prefix = time.strftime('%Y%m%d%H%M%S', time.localtime())
    list_num = []
    for index in range(0, loop_count):
        list_num.append(prefix + str(10000 + index + 1))
    return list_num


if __name__ == '__main__':
    # 首先构造一个SDK实例
    api_sdk = K3CloudApiSdk()
    # api_sdk = K3CloudApiSdk('http://net64pool04091/k3cloud')
    # 然后初始化SDK，需指定相关参数，否则会导致SDK初始化失败而无法使用：
    # 初始化方案一：Init初始化方法，使用conf.ini配置文件
    # config_path:配置文件的相对或绝对路径，建议使用绝对路径
    # config_node:配置文件中的节点名称
    api_sdk.Init(config_path='../conf.ini', config_node='config')
    #print('Demo_For_Save : ', Demo_For_Save(api_sdk))
    #print("Demo_For_SwitchOrg:",Demo_For_SwitchOrg(api_sdk))
    # print('Demo_For_BillQuery : ',Demo_For_BillQuery(api_sdk))


    # 初始化方案二（新增）：InitConfig初始化方法，直接传参，不使用配置文件
    # acct_id:第三方系统登录授权的账套ID,user_name:第三方系统登录授权的用户,app_id:第三方系统登录授权的应用ID,app_sec:第三方系统登录授权的应用密钥
    # server_url:k3cloud环境url,lcid:账套语系(默认2052),org_num:组织编码(启用多组织时配置对应的组织编码才有效)
    api_sdk.InitConfig('5db25ac8d2b819', 'webapi', '204399_72epSbtEQMC92Vwt2d3LRa9LRqSc1tqJ', 'fb7d46647ac346dbb5fcd45b65512a45','')
    #api_sdk.InitConfig('610ba563e982e1', 'Administrator', '218358_1ccC0/HFQmH/XUVET36Bzz8M1rWb0APu', 'be319058d85246e4a2a7be73c684bdce', 'http://ahxl.com.cn:81/k3cloud')
    # print(api_sdk.View("BD_MATERIAL", {"Number": "Webb2020031909092410001"}))
    # 使用Save示例
    #print('Demo_For_Save : ', Demo_For_Save(api_sdk))
    # 使用BatchSave示例
    # print('Demo_For_BatchSave : ', Demo_For_BatchSave(api_sdk, count=50, query=True))
