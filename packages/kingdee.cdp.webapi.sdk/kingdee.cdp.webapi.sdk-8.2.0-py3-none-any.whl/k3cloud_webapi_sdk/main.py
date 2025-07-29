#!/usr/bin/python
# -*- coding:UTF-8 -*-
from k3cloud_webapi_sdk.core.webapi_client import WebApiClient
from k3cloud_webapi_sdk.const.const_define import InvokeMethod
from k3cloud_webapi_sdk.util import config_util


class K3CloudApiSdk(WebApiClient):
    def __init__(self, server_url, timeout=120):
        super(K3CloudApiSdk, self).__init__()
        self.ServerUrl = server_url
        self.TimeOut = timeout

    def InitConfig(self, acct_id, user_name, app_id, app_secret, server_url, lcid=2052, org_num=0,
                   connect_timeout=120,
                   request_timeout=120, proxy=''):
        self.config = config_util.InitConfigByParams(acct_id, user_name, app_id, app_secret, server_url, lcid, org_num,
                                                     connect_timeout, request_timeout, proxy)
        super(K3CloudApiSdk, self).Init(self.ServerUrl, self.TimeOut, self.IsValid())

    def Init(self, config_path='conf.ini', config_node='config'):
        self.config = config_util.InitConfig(config_path, config_node)
        super(K3CloudApiSdk, self).Init(self.ServerUrl, self.TimeOut, self.IsValid())

    def IsValid(self):
        msg = ''
        if self.config.dcid == '':
            msg += ',账套ID'
        if self.config.user_name == '':
            msg += ',用户'
        if self.config.app_id == '':
            msg += ',应用ID'
        if self.config.app_secret == '':
            msg += ',应用密钥'
        if msg != '':
            print('SDK初始化失败，缺少必填授权项：' + msg[1:])
            return False
        else:
            return True

    def GetDataCenters(self):
        return self.Execute('Kingdee.BOS.ServiceFacade.ServicesStub.Account.AccountService.GetDataCenterList')

    def ExcuteOperation(self, formid, opNumber, data):
        """操作接口"""
        return self.Execute('Kingdee.BOS.WebApi.ServicesStub.DynamicFormService.ExcuteOperation',
                            {'formid': formid, 'opNumber': opNumber, 'data': data})

    def Save(self, formid, data):
        """保存"""
        return self.Execute('Kingdee.BOS.WebApi.ServicesStub.DynamicFormService.Save',
                            {'formid': formid, 'data': data})

    def BatchSave(self, formid, data):
        """批量保存"""
        return self.Execute('Kingdee.BOS.WebApi.ServicesStub.DynamicFormService.BatchSave',
                            {'formid': formid, 'data': data})

    def BatchSaveQuery(self, formid, data):
        """批量保存（轮询）"""
        return self.Execute('Kingdee.BOS.WebApi.ServicesStub.DynamicFormService.BatchSave',
                            {'formid': formid, 'data': data},
                            invoke_type=InvokeMethod.QUERY)

    def Audit(self, formid, data):
        """审核"""
        return self.Execute('Kingdee.BOS.WebApi.ServicesStub.DynamicFormService.Audit',
                            {'formid': formid, 'data': data})

    def Delete(self, formid, data):
        """删除"""
        return self.Execute('Kingdee.BOS.WebApi.ServicesStub.DynamicFormService.Delete',
                            {'formid': formid, 'data': data})

    def UnAudit(self, formid, data):
        """反审核"""
        return self.Execute('Kingdee.BOS.WebApi.ServicesStub.DynamicFormService.UnAudit',
                            {'formid': formid, 'data': data})

    def Submit(self, formid, data):
        """提交"""
        return self.Execute('Kingdee.BOS.WebApi.ServicesStub.DynamicFormService.Submit',
                            {'formid': formid, 'data': data})

    def View(self, formid, data):
        """查看"""
        return self.Execute('Kingdee.BOS.WebApi.ServicesStub.DynamicFormService.View',
                            {'formid': formid, 'data': data})

    def ExecuteBillQuery(self, data):
        """
        单据查询
        :param data:
        :return:List<List<object>>的json串
        """
        return self.Execute('Kingdee.BOS.WebApi.ServicesStub.DynamicFormService.ExecuteBillQuery',
                            {'data': data})

    def BillQuery(self, data):
        """
        单据查询（json） 2023-9-14新加
        :param data:
        :return:string
        """
        return self.Execute('Kingdee.BOS.WebApi.ServicesStub.DynamicFormService.BillQuery',
                            {'data': data})

    def Draft(self, formid, data):
        """暂存"""
        return self.Execute('Kingdee.BOS.WebApi.ServicesStub.DynamicFormService.Draft',
                            {'formid': formid, 'data': data})

    def Allocate(self, formid, data):
        """分配"""
        return self.Execute('Kingdee.BOS.WebApi.ServicesStub.DynamicFormService.Allocate',
                            {'formid': formid, 'data': data})

    def FlexSave(self, formid, data):
        """弹性域保存"""
        return self.Execute('Kingdee.BOS.WebApi.ServicesStub.DynamicFormService.FlexSave',
                            {'formid': formid, 'data': data})

    def SendMsg(self, data):
        """发送消息"""
        return self.Execute('Kingdee.BOS.WebApi.ServicesStub.DynamicFormService.SendMsg',
                            {'data': data})

    def Push(self, formid, data):
        """下推"""
        return self.Execute('Kingdee.BOS.WebApi.ServicesStub.DynamicFormService.Push',
                            {'formid': formid, 'data': data})

    def GroupSave(self, formid, data):
        """分组保存"""
        return self.Execute('Kingdee.BOS.WebApi.ServicesStub.DynamicFormService.GroupSave',
                            {'formid': formid, 'data': data})

    def Disassembly(self, formid, data):
        """拆单"""
        return self.Execute('Kingdee.BOS.WebApi.ServicesStub.DynamicFormService.Disassembly',
                            {'formid': formid, 'data': data})

    def QueryBusinessInfo(self, data):
        """查询单据接口"""
        return self.Execute('Kingdee.BOS.WebApi.ServicesStub.DynamicFormService.QueryBusinessInfo',
                            {'data': data})

    def QueryGroupInfo(self, data):
        """查询分组信息接口"""
        return self.Execute('Kingdee.BOS.WebApi.ServicesStub.DynamicFormService.QueryGroupInfo',
                            {'data': data})

    def WorkflowAudit(self, data):
        """工作流审批"""
        return self.Execute('Kingdee.BOS.WebApi.ServicesStub.DynamicFormService.WorkflowAudit',
                            {'data': data})

    def GroupDelete(self, data):
        """分组删除接口"""
        return self.Execute('Kingdee.BOS.WebApi.ServicesStub.DynamicFormService.GroupDelete',
                            {'data': data})

    def SwitchOrg(self, data):
        """切换组织"""
        return self.Execute('Kingdee.BOS.WebApi.ServicesStub.DynamicFormService.SwitchOrg',
                            {'data': data})

    def cancelAllocate(self, formid, data):
        """取消分配"""
        return self.Execute('Kingdee.BOS.WebApi.ServicesStub.DynamicFormService.CancelAllocate',
                            {'formid': formid, 'data': data})

    def cancelAssign(self, formid, data):
        """撤销服务接口"""
        return self.Execute('Kingdee.BOS.WebApi.ServicesStub.DynamicFormService.CancelAssign',
                            {'formid': formid, 'data': data})

    def getSysReportData(self, formid, data):
        """获取报表数据"""
        return self.Execute('Kingdee.BOS.WebApi.ServicesStub.DynamicFormService.GetSysReportData',
                            {'formid': formid, 'data': data})

    def attachmentUpload(self, data):
        """上传附件"""
        return self.Execute('Kingdee.BOS.WebApi.ServicesStub.DynamicFormService.AttachmentUpload',
                            {'data': data})

    def attachmentDownLoad(self, data):
        """下载附件"""
        return self.Execute('Kingdee.BOS.WebApi.ServicesStub.DynamicFormService.AttachmentDownLoad',
                            {'data': data})

    def CancelAllocate(self, formid, data):
        """取消分配"""
        return self.Execute('Kingdee.BOS.WebApi.ServicesStub.DynamicFormService.CancelAllocate',
                            {'formid': formid, 'data': data})

    def CancelAssign(self, formid, data):
        """撤销服务接口"""
        return self.Execute('Kingdee.BOS.WebApi.ServicesStub.DynamicFormService.CancelAssign',
                            {'formid': formid, 'data': data})

    def GetSysReportData(self, formid, data):
        """获取报表数据"""
        return self.Execute('Kingdee.BOS.WebApi.ServicesStub.DynamicFormService.GetSysReportData',
                            {'formid': formid, 'data': data})

    def AttachmentUpload(self, data):
        """上传附件"""
        return self.Execute('Kingdee.BOS.WebApi.ServicesStub.DynamicFormService.AttachmentUpload',
                            {'data': data})

    def AttachmentDownLoad(self, data):
        """下载附件"""
        return self.Execute('Kingdee.BOS.WebApi.ServicesStub.DynamicFormService.AttachmentDownLoad',
                            {'data': data})