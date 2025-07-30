"""
完整触发flow历史记录并校验流程
1. 准备好一个flow
2. 获取当前flow版本号
3. 设置flow初始数据后启动 - 避免每次改动过多营销历史记录校验
4. 设置需求修改的flow条件后启动 - 每次改动尽量少，方便校验
5. 校验历史记录
"""
import json
import time
import requests
from smartpush.flow import global_flow
from smartpush.utils import ListDictUtils
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_result

should_stop_retrying = False  # 全局变量控制是否停止


def check_should_retry(result):
    return not should_stop_retrying  # 如果 should_stop_retrying=False，则继续重试


@retry(stop=stop_after_attempt(8),
       retry=retry_if_result(check_should_retry),
       wait=wait_exponential(multiplier=2, min=2, max=10))
def get_flow_history(host_domain, cookies, flow_id, **kwargs):
    global should_stop_retrying
    """获取flow历史记录 - 默认只提取第一条"""
    get_flow_history_url = host_domain + "/flow/queryFlowHistoryRecords"
    get_flow_history_headers = {
        "cookie": cookies,
        "content-type": "application/json"
    }
    get_flow_history_params = {
        "page": 1,
        "pageSize": 10,
        "keyword": "",
        "start": "",
        "flowId": flow_id
    }
    result = json.loads(
        requests.request(method="post", url=get_flow_history_url, headers=get_flow_history_headers,
                         json=get_flow_history_params).text)

    if result["resultData"]["datas"][0]["operateTime"] >= kwargs.get("change_flow_time"):
        should_stop_retrying = True
        return result["resultData"]["datas"][0]["operateList"][0]


def check_history(host_domain, cookies, flow_id, expected_history, **kwargs):
    """校验历史记录
    必填字段：
    host_domain
    cookies
    flow_id
    expected_history
    init_flow_params
    change_flow_params
    """

    # 获取flow版本号
    version = global_flow.get_flow_version(host_domain=host_domain, cookies=cookies, flow_id=flow_id)
    # 准备flow初始数据
    global_flow.update_flow(host_domain=host_domain, cookies=cookies, flow_id=flow_id, version=version,
                            update_flow_params=kwargs.get("init_flow_params"))
    global_flow.start_flow(host_domain=host_domain, cookies=cookies, flow_id=flow_id, version=version)
    # 设置需要修改的值
    new_version = str(int(version) + 1)
    global_flow.update_flow(host_domain=host_domain, cookies=cookies, flow_id=flow_id, version=new_version,
                            update_flow_params=kwargs.get("change_flow_params"))
    change_flow_time = int(time.time() * 1000)
    global_flow.start_flow(host_domain=host_domain, cookies=cookies, flow_id=flow_id, version=new_version)
    # 获取历史记录
    actual_history = get_flow_history(host_domain=host_domain, cookies=cookies, flow_id=flow_id,
                                      change_flow_time=change_flow_time)
    # 校验历史记录
    result = ListDictUtils.contrast_dict(actual_dict=actual_history, expected_dict=expected_history,
                                         only_values_changed=kwargs.get("only_values_changed", True))

    return result
