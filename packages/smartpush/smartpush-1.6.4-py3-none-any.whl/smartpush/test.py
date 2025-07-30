# -*- codeing = utf-8 -*-
# @Time :2025/2/20 00:27
# @Author :luzebin
import json
import re
import time

import pandas as pd

from smartpush.export.basic import ExcelExportChecker
from smartpush.export.basic.ReadExcel import read_excel_from_oss
from smartpush.export.basic.ReadExcel import read_excel_and_write_to_dict
from smartpush.export.basic.GetOssUrl import get_oss_address_with_retry
from smartpush.utils.DataTypeUtils import DataTypeUtils
from smartpush.flow import MockFlow
from smartpush.utils import EmailUtlis, ListDictUtils
from smartpush.flow import history_flow

if __name__ == '__main__':
    # with open("/Users/SL/project/python/smartpush_autotest/smartpush/test.json", "r", encoding="utf-8") as file:
    #     jsondata = json.load(file)
    host_domain = "https://test.smartpushedm.com/bff/api-em-ec2"
    cookies = "_ga=GA1.1.88071637.1717860341; _ga_NE61JB8ZM6=GS1.1.1718954972.32.1.1718954972.0.0.0; _ga_Z8N3C69PPP=GS1.1.1723104149.2.0.1723104149.0.0.0; osudb_lang=; _ga_D2KXR23WN3=GS2.1.s1750155311$o4$g1$t1750155365$j6$l0$h0; osudb_appid=SMARTPUSH; osudb_subappid=1; osudb_uid=4213785247; osudb_oar=#01#SID0000132BHI1r3cd4Ql7G3PdLEyquxTGSH1bRwwZ9Ukl032ycMYDwyV2wt22xT9xAD/hg0R3pX9KK4omO5F16VO3fibHwCqGJRHfqlrm2NxilkURarsZ1BT2DcvWZGJxbzSccW6G3zrUvzWVNVMk7J1XqGsX; a_lang=zh-hant-tw; ecom_http_token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3NTUzMjk3NTMsImp0aSI6IjI2YzIwN2IwLTQ2YjAtNGNmZi04ZTNkLWY3MWQxZDg2ZmFjZCIsInVzZXJJbmZvIjp7ImlkIjowLCJ1c2VySWQiOiI0MjEzNzg1MjQ3IiwidXNlcm5hbWUiOiIiLCJlbWFpbCI6ImZlbGl4LnNoYW9Ac2hvcGxpbmVhcHAuY29tIiwidXNlclJvbGUiOiJvd25lciIsInBsYXRmb3JtVHlwZSI6Nywic3ViUGxhdGZvcm0iOjEsInBob25lIjoiIiwibGFuZ3VhZ2UiOiJ6aC1oYW50LXR3IiwiYXV0aFR5cGUiOiIiLCJhdHRyaWJ1dGVzIjp7ImNvdW50cnlDb2RlIjoiQ04iLCJjdXJyZW5jeSI6IkpQWSIsImN1cnJlbmN5U3ltYm9sIjoiSlDCpSIsImRvbWFpbiI6InNtYXJ0cHVzaDQubXlzaG9wbGluZXN0Zy5jb20iLCJsYW5ndWFnZSI6ImVuIiwibWVyY2hhbnRFbWFpbCI6ImZlbGl4LnNoYW9Ac2hvcGxpbmUuY29tIiwibWVyY2hhbnROYW1lIjoiU21hcnRQdXNoNF9lYzJf6Ieq5Yqo5YyW5bqX6ZO6IiwicGhvbmUiOiIiLCJzY29wZUNoYW5nZWQiOmZhbHNlLCJzdGFmZkxhbmd1YWdlIjoiemgtaGFucy1jbiIsInN0YXR1cyI6MCwidGltZXpvbmUiOiJBc2lhL01hY2FvIn0sInN0b3JlSWQiOiIxNjQ0Mzk1OTIwNDQ0IiwiaGFuZGxlIjoic21hcnRwdXNoNCIsImVudiI6IkNOIiwic3RlIjoiIiwidmVyaWZ5IjoiIn0sImxvZ2luVGltZSI6MTc1MjczNzc1MzY4Mywic2NvcGUiOlsiZW1haWwtbWFya2V0IiwiY29va2llIiwic2wtZWNvbS1lbWFpbC1tYXJrZXQtbmV3LXRlc3QiLCJlbWFpbC1tYXJrZXQtbmV3LWRldi1mcyIsImFwaS11Yy1lYzIiLCJhcGktc3UtZWMyIiwiYXBpLWVtLWVjMiIsImZsb3ctcGx1Z2luIiwiYXBpLXNwLW1hcmtldC1lYzIiXSwiY2xpZW50X2lkIjoiZW1haWwtbWFya2V0In0.26kjiBatHX0pyuWRgvsUxqmbKK9q8YFjQQY541-EwkE; JSESSIONID=910B0EAC71357A61D5571CA2E07A79E9"
    flow_id = "FLOW6441875700060831242"
    init_flow_params = {'id': '${fe_flow_id}', 'version': '${historyVersion}', 'triggerId': 'c1001', 'templateId': '',
                        'showData': False, 'flowChange': True, 'nodes': [{'type': 'trigger', 'data': {
            'trigger': {'trigger': 'c1001', 'group': '', 'suggestionGroupId': '', 'triggerStock': False,
                        'completedCount': 0, 'skippedCount': 0}, 'completedCount': 0, 'skippedCount': 0},
                                                                          'id': '8978d673-3485-47dd-849c-e08a6e181d7c'},
                                                                         {'type': 'sendSms', 'data': {
                                                                             'sendSms': {'id': 304196,
                                                                                         'activityTemplateId': 304196,
                                                                                         'activityName': 'flowActivity_FkY0zS',
                                                                                         'merchantId': '1644395920444',
                                                                                         'merchantName': 'SmartPush4_ec2_自动化店铺',
                                                                                         'brandName': 'SmartPush4_ec2_自动化店铺 AutoTestName',
                                                                                         'currency': 'JP¥',
                                                                                         'activityType': 'NORMAL',
                                                                                         'activityStatus': 'DRAFT',
                                                                                         'createTime': 1723545075926,
                                                                                         'updateTime': 1723545191007,
                                                                                         'createDate': '2024-08-13 18:31:15',
                                                                                         'updateDate': '2024-08-13 18:33:11',
                                                                                         'pickContactPacks': [],
                                                                                         'excludeContactPacks': [],
                                                                                         'customerGroupIds': [],
                                                                                         'excludeCustomerGroupIds': [],
                                                                                         'pickContactInfos': [],
                                                                                         'excludeContactInfos': [],
                                                                                         'customerGroupInfos': [],
                                                                                         'excludeCustomerGroupInfos': [],
                                                                                         'sender': 'SmartPush4_ec2_自动化店铺 AutoTestName',
                                                                                         'originTemplate': 33,
                                                                                         'currentJsonSchema': '{"extend":{"version":"1.0.0"},"children":[{"children":[{"children":[],"id":"98d909a48","type":"Column","props":{}}],"id":"84ba788da","type":"Header","props":{"borderLeft":"1px none #ffffff","backgroundColor":"#ffffff","paddingBottom":"0px","borderRight":"1px none #ffffff","paddingRight":"0px","paddingTop":"0px","borderTop":"1px none #ffffff","borderBottom":"1px none #ffffff","paddingLeft":"0px","cols":[12]}},{"children":[{"children":[],"id":"8cab9aa48","type":"Column","props":{}}],"id":"84ba7bbda","type":"Section","props":{"borderLeft":"1px none #ffffff","backgroundColor":"#ffffff","paddingBottom":"0px","borderRight":"1px none #ffffff","paddingRight":"0px","paddingTop":"0px","borderTop":"1px none #ffffff","borderBottom":"1px none #ffffff","paddingLeft":"0px","cols":[12]}},{"children":[{"children":[{"children":[],"id":"b39b6a94a","type":"Subscribe","props":{"content":"<p style=\\"text-align:center;\\"><span style=\\"font-size:12px\\"><span style=\\"font-family:Arial, Helvetica, sans-serif\\">Please enter the contact address here, so that your customers can trust this email more</span></span></p>"}}],"id":"b3bcabad7","type":"Column","props":{}}],"id":"b8bbabad9","type":"Footer","props":{"borderLeft":"1px none #ffffff","backgroundColor":"#ffffff","paddingBottom":"0px","borderRight":"1px none #ffffff","paddingRight":"0px","paddingTop":"0px","borderTop":"1px none #ffffff","borderBottom":"1px none #ffffff","paddingLeft":"0px","cols":[12]}}],"id":"a4a9fba2a","type":"Stage","props":{"backgroundColor":"#EAEDF1","fullWidth":"normal-width","width":"600px"}}',
                                                                                         'currentHtml': '自动化短信',
                                                                                         'generatedHtml': False,
                                                                                         'templateUrl': 'https://kmalgo.oss-ap-southeast-1.aliyuncs.com/material/2021-11-29/d4f96fc873e942a397be708c932bbbe4-自定义排版.png',
                                                                                         'sendStrategy': 'NOW',
                                                                                         'totalReceiver': 0,
                                                                                         'receiverAreaInfos': [],
                                                                                         'utmConfigEnable': False,
                                                                                         'language': 'en',
                                                                                         'languageName': '英语',
                                                                                         'timezone': 'Asia/Macao',
                                                                                         'timezoneGmt': 'GMT+08:00',
                                                                                         'type': 'FLOW',
                                                                                         'relId': 'FLOW6441875700060831242',
                                                                                         'parentId': '0',
                                                                                         'nodeId': 'd96e632c-11b6-4836-a8a0-e5af2810ddb7',
                                                                                         'version': '14',
                                                                                         'nodeOrder': 0,
                                                                                         'sendType': 'SMS',
                                                                                         'createSource': 'BUILD_ACTIVITY',
                                                                                         'contentChange': True,
                                                                                         'activityChange': False,
                                                                                         'warmupPack': 0,
                                                                                         'boosterEnabled': False,
                                                                                         'smartSending': False,
                                                                                         'boosterCreated': False,
                                                                                         'gmailPromotion': False,
                                                                                         'sendTimeType': 'FIXED',
                                                                                         'sendTimezone': 'B_TIMEZONE',
                                                                                         'sendTimeDelay': False,
                                                                                         'sendOption': 1,
                                                                                         'minSendTime': '2024-08-13 18:31:15',
                                                                                         'completedCount': 0,
                                                                                         'skippedCount': 0},
                                                                             'completedCount': 0, 'skippedCount': 0},
                                                                          'id': 'd96e632c-11b6-4836-a8a0-e5af2810ddb7'}],
                        'showDataStartTime': None, 'showDataEndTime': None}
    change_flow_params = {'id': '${fe_flow_id}', 'version': '28', 'triggerId': 'c1001', 'templateId': '',
                          'showData': False, 'flowChange': True, 'nodes': [{'type': 'trigger', 'data': {
            'trigger': {'trigger': 'c1001', 'condition': {'relation': '$AND', 'groups': [{'relation': '$AND', 'rules': [
                {'type': 'checkoutSubscribed', 'contentTxt': '', 'operator': 'eq', 'value': 'true'}]}]}}},
                                                                            'id': '8978d673-3485-47dd-849c-e08a6e181d7c'},
                                                                           {'type': 'sendSms', 'data': {
                                                                               'sendSms': {'id': 303869,
                                                                                           'activityTemplateId': 303869,
                                                                                           'activityName': 'flowActivity_FkY0zS',
                                                                                           'merchantId': '1644395920444',
                                                                                           'merchantName': 'SmartPush4_ec2_自动化店铺',
                                                                                           'brandName': 'SmartPush4_ec2_自动化店铺 AutoTestName',
                                                                                           'currency': 'JP¥',
                                                                                           'activityType': 'NORMAL',
                                                                                           'activityStatus': 'ACTIVE',
                                                                                           'createTime': 1723602996795,
                                                                                           'updateTime': 1723603000762,
                                                                                           'createDate': '2024-08-14 10:36:36',
                                                                                           'updateDate': '2024-08-14 10:36:40',
                                                                                           'pickContactPacks': [],
                                                                                           'excludeContactPacks': [],
                                                                                           'customerGroupIds': [],
                                                                                           'excludeCustomerGroupIds': [],
                                                                                           'pickContactInfos': [],
                                                                                           'excludeContactInfos': [],
                                                                                           'customerGroupInfos': [],
                                                                                           'excludeCustomerGroupInfos': [],
                                                                                           'sender': 'SmartPush4_ec2_自动化店铺 AutoTestName',
                                                                                           'originTemplate': 33,
                                                                                           'currentJsonSchema': '{"extend":{"version":"1.0.0"},"children":[{"children":[{"children":[],"id":"98d909a48","type":"Column","props":{}}],"id":"84ba788da","type":"Header","props":{"borderLeft":"1px none #ffffff","backgroundColor":"#ffffff","paddingBottom":"0px","borderRight":"1px none #ffffff","paddingRight":"0px","paddingTop":"0px","borderTop":"1px none #ffffff","borderBottom":"1px none #ffffff","paddingLeft":"0px","cols":[12]}},{"children":[{"children":[],"id":"8cab9aa48","type":"Column","props":{}}],"id":"84ba7bbda","type":"Section","props":{"borderLeft":"1px none #ffffff","backgroundColor":"#ffffff","paddingBottom":"0px","borderRight":"1px none #ffffff","paddingRight":"0px","paddingTop":"0px","borderTop":"1px none #ffffff","borderBottom":"1px none #ffffff","paddingLeft":"0px","cols":[12]}},{"children":[{"children":[{"children":[],"id":"b39b6a94a","type":"Subscribe","props":{"content":"<p style=\\"text-align:center;\\"><span style=\\"font-size:12px\\"><span style=\\"font-family:Arial, Helvetica, sans-serif\\">Please enter the contact address here, so that your customers can trust this email more</span></span></p>"}}],"id":"b3bcabad7","type":"Column","props":{}}],"id":"b8bbabad9","type":"Footer","props":{"borderLeft":"1px none #ffffff","backgroundColor":"#ffffff","paddingBottom":"0px","borderRight":"1px none #ffffff","paddingRight":"0px","paddingTop":"0px","borderTop":"1px none #ffffff","borderBottom":"1px none #ffffff","paddingLeft":"0px","cols":[12]}}],"id":"a4a9fba2a","type":"Stage","props":{"backgroundColor":"#EAEDF1","fullWidth":"normal-width","width":"600px"}}',
                                                                                           'currentHtml': '自动化短信',
                                                                                           'generatedHtml': False,
                                                                                           'templateUrl': 'https://kmalgo.oss-ap-southeast-1.aliyuncs.com/material/2021-11-29/d4f96fc873e942a397be708c932bbbe4-自定义排版.png',
                                                                                           'sendStrategy': 'NOW',
                                                                                           'totalReceiver': 0,
                                                                                           'receiverAreaInfos': [],
                                                                                           'utmConfigEnable': False,
                                                                                           'language': 'en',
                                                                                           'languageName': '英语',
                                                                                           'timezone': 'Asia/Macao',
                                                                                           'timezoneGmt': 'GMT+08:00',
                                                                                           'type': 'FLOW',
                                                                                           'relId': 'FLOW6441875700060831242',
                                                                                           'parentId': '0',
                                                                                           'nodeId': 'd96e632c-11b6-4836-a8a0-e5af2810ddb7',
                                                                                           'version': '28',
                                                                                           'nodeOrder': 0,
                                                                                           'sendType': 'SMS',
                                                                                           'createSource': 'BUILD_ACTIVITY',
                                                                                           'contentChange': True,
                                                                                           'activityChange': False,
                                                                                           'warmupPack': 0,
                                                                                           'boosterEnabled': False,
                                                                                           'smartSending': False,
                                                                                           'boosterCreated': False,
                                                                                           'gmailPromotion': False,
                                                                                           'sendTimeType': 'FIXED',
                                                                                           'sendTimezone': 'B_TIMEZONE',
                                                                                           'sendTimeDelay': False,
                                                                                           'sendOption': 1,
                                                                                           'minSendTime': '2024-08-14 10:36:36',
                                                                                           'completedCount': 0,
                                                                                           'skippedCount': 0},
                                                                               'completedCount': 0, 'skippedCount': 0},
                                                                            'id': 'd96e632c-11b6-4836-a8a0-e5af2810ddb7'}],
                          'showDataStartTime': None, 'showDataEndTime': None}

    expected_history = {
        "triggerType": "filter",
        "opt": "c",
        "moduleNext": "checkoutSubscribed",
        "before": "",
        "after": "等于 是"
    }

    t1 = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    result = history_flow.check_history(host_domain=host_domain, cookies=cookies, flow_id=flow_id,
                                        init_flow_params=init_flow_params, change_flow_params=change_flow_params,
                                        expected_history=expected_history)
    t2 = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    print(result)
    print(t1)
    print(t2)

