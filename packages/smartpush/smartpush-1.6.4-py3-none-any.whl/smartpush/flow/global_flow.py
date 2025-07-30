import json
import requests


def get_flow_version(host_domain, cookies, flow_id, **kwargs):
    """获取flow版本号"""
    get_flow_url = host_domain + "/flow/getFlowDetail"
    get_flow_headers = {
        "cookie": cookies
    }
    get_flow_params = {
        "flowId": flow_id,
        "active": True,
        "includeActivityDetail": True
    }
    result = json.loads(
        requests.request(method="get", url=get_flow_url, headers=get_flow_headers, params=get_flow_params).text)

    return result["resultData"]["version"]


def update_flow(host_domain, cookies, **kwargs):
    """
    # 更新flow
    update_flow_params: 必填，saveFlow接口所有参数，dict格式
    version: 非必填，flow版本号
    """
    _url = host_domain + "/flow/saveFlow"
    headers = {
        "cookie": cookies,
        "Content-Type": "application/json"
    }
    kwargs["update_flow_params"]["version"] = kwargs.get("version", kwargs["update_flow_params"]["version"])
    kwargs["update_flow_params"]["id"] = kwargs.get("flow_id", kwargs["update_flow_params"]["id"])
    params = kwargs["update_flow_params"]
    result = requests.request(method="post", url=_url, headers=headers, json=params).text


def start_flow(host_domain, cookies, flow_id, version):
    """启动flow"""
    _url = host_domain + "/flow/publishFlow"
    headers = {
        "cookie": cookies,
        "Content-Type": "application/json"
    }
    params = {
        "flowId": flow_id,
        "version": str(version)
    }
    result = requests.request(method="post", url=_url, headers=headers, json=params).text


def disable_flow(host_domain, cookies, flow_ids, version):
    """关闭flow"""
    _url = host_domain + "flow/disableFlow"
    headers = {
        "cookie": cookies,
        "Content-Type": "application/json"
    }
    for flow_id in flow_ids:
        params = {
            "flowId": flow_id,
            "version": str(version),
            "continueRun": False
        }
        result = requests.request(method="post", url=_url, headers=headers, json=params).text
