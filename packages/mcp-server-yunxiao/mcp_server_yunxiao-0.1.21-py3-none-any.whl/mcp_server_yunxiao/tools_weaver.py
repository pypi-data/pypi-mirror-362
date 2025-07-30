from typing import Annotated, Optional, List
from pydantic import Field
from concurrent.futures import ThreadPoolExecutor, as_completed
from .client import _call_api, _call_api_raw
from . import mcp
import re
import json
from datetime import datetime, timedelta


REGION_ALIAS_MAP = {
    "sheec": "ap-shenyang-ec",
    "sh": "ap-shanghai",
    "sao": "sa-saopaulo",
    "bjjr": "ap-beijing-fsi",
    "hzec": "ap-hangzhou-ec",
    "cgoec": "ap-zhengzhou-ec",
    "use": "na-ashburn",
    "xiyec": "ap-xian-ec",
    "cd": "ap-chengdu",
    "cq": "ap-chongqing",
    "shjr": "ap-shanghai-fsi",
    "szjr": "ap-shenzhen-fsi",
    "usw": "na-siliconvalley",
    "jkt": "ap-jakarta",
    "in": "ap-mumbai",
    "jnec": "ap-jinan-ec",
    "gz": "ap-guangzhou",
    "szsycft": "ap-shenzhen-sycft",
    "qyxa": "ap-qingyuan-xinan",
    "hk": "ap-hongkong",
    "sjwec": "ap-shijiazhuang-ec",
    "tpe": "ap-taipei",
    "gzopen": "ap-guangzhou-open",
    "jp": "ap-tokyo",
    "hfeec": "ap-hefei-ec",
    "qy": "ap-qingyuan",
    "bj": "ap-beijing",
    "whec": "ap-wuhan-ec",
    "csec": "ap-changsha-ec",
    "tsn": "ap-tianjin",
    "nj": "ap-nanjing",
    "de": "eu-frankfurt",
    "th": "ap-bangkok",
    "sg": "ap-singapore",
    "kr": "ap-seoul",
    "fzec": "ap-fuzhou-ec",
    "szx": "ap-shenzhen",
    "xbec": "ap-xibei-ec",
    "shadc": "ap-shanghai-adc",
    "shwxzf": "ap-shanghai-wxzf",
    "gzwxzf": "ap-guangzhou-wxzf",
    "szjxcft": "ap-shenzhen-jxcft",
    "shhqcft": "ap-shanghai-hq-cft",
    "shhqcftfzhj": "ap-shanghai-hq-uat-cft",
    "shwxzfjpyzc": "ap-shanghai-wxp-ops",
    "njxfcft": "ap-nanjing-xf-cft",
}

def _get_region_alias(region: str, region_alias: Optional[str] = None) -> str:
    """
    通用 region 到 regionAlias 的映射
    """
    if region_alias:
        return region_alias
    for k, v in REGION_ALIAS_MAP.items():
        if v == region:
            return k
    return ""

@mcp.tool(description="查询VStation任务列表（简称VS任务)必传参数region，可选参数task_id/instance_id/uuid/request_id/host_ip/owner/start_time/end_time/limit/region_alias")
def query_vstation_task_message(
    region: Annotated[str, Field(description="地域，如 ap-guangzhou")],
    task_id: Annotated[Optional[List[str]], Field(description="VStation任务ID")] = [],
    instance_id: Annotated[Optional[List[str]], Field(description="实例ID，格式为ins-xxxxxxxx")] = [],
    uuid: Annotated[Optional[List[str]], Field(description="UUID，格式为8a23be54-f4cf-4a4b-95b7-8d3eda6fd803")] = [],
    request_id: Annotated[Optional[List[str]], Field(description="请求ID")] = [],
    host_ip: Annotated[Optional[List[str]], Field(description="母机/宿主机的IP")] = [],
    owner: Annotated[Optional[List[str]], Field(description="客户Owner")] = [],
    start_time: Annotated[Optional[str], Field(description="起始时间，格式：YYYY-MM-DD HH:mm:ss")] = None,
    end_time: Annotated[Optional[str], Field(description="结束时间，格式：YYYY-MM-DD HH:mm:ss")] = None,
    limit: Annotated[int, Field(description="分页长度")] = 100,
    region_alias: Annotated[Optional[str], Field(description="地域别名")] = None
) -> str:
    """
    查询 VStation 任务列表
    Args:
        region: 地域，如 ap-guangzhou
        task_id: VStation任务ID
        instance_id: 实例ID
        uuid: 任务UUID
        request_id: 请求ID
        host_ip: 母机/宿主机 IP
        start_time: 起始时间，格式：YYYY-MM-DD HH:mm:ss（可选，默认当天 00:00:00）
        end_time: 结束时间，格式：YYYY-MM-DD HH:mm:ss（可选，默认当天 23:59:59）
        region_alias: 地域别名（可选，若未传则自动匹配）
    Returns:
        str: 查询结果的JSON字符串
    """
    # 自动补全时间
    if not start_time or not end_time:
        today = datetime.now().strftime("%Y-%m-%d")
        if not start_time:
            start_time = f"{today} 00:00:00"
        if not end_time:
            end_time = f"{today} 23:59:59"
    alias = _get_region_alias(region, region_alias)
    filters = []
    if task_id:
        filters.append({
            "Name": "task_id",
            "Values": task_id
        })
    if request_id:
        filters.append({
            "Name": "requestId",
            "Values": request_id
        })
    if uuid:
        filters.append({
            "Name": "uuid",
            "Values": uuid
        })
    if instance_id:
        filters.append({
            "Name": "uInstanceId",
            "Values": instance_id
        })
    if host_ip:
        filters.append({
            "Name": "hostIp",
            "Values": host_ip
        })
    if owner:
        filters.append({
            "Name": "owner",
            "Values": owner
        })
    params = {
        "Region": region,
        "Filters": filters,
        "StartTime": start_time,
        "EndTime": end_time,
        "Offset": 0,
        "Limit": limit,
        "Action": "QueryTaskMessage",
        "AppId": "251006228",
        "RequestSource": "YunXiao",
        "SubAccountUin": "493083759",
        "Uin": "493083759",
        "regionAlias": alias,
        "Fields": [
            "taskStatus",
            "code",
            "cursor",
            "errorMsg",
            "hostIp",
            "hypervisor",
            "mode",
            "owner",
            "parentTaskId",
            "region",
            "requestId",
            "startTime",
            "taskId",
            "taskName",
            "taskProgress",
            "taskState",
            "traceRequestId",
            "uInstanceId",
            "uuid",
            "finishTime",
            "updateTime",
            "delayExecSteps",
            "hasDelaySteps",
            "migrateHostIp",
            "stepsLength",
            "productCategory",
            "chcId",
            "dedicatedClusterId",
            "p2pFlow",
            "desTaskId",
            "dataDiskSerial",
            "rootDiskSerial",
            "vifSerial",
            "uImageId",
            "vpcId",
            "instanceType",
            "zoneId",
            "gridId"
        ]
    }
    return _call_api("/weaver/upstream/terra/QueryTaskMessage", params)

@mcp.tool(description="查询VStation任务列表（简称VS任务)必传参数region，可选参数task_id/instance_id/uuid/request_id/host_ip/owner/start_time/end_time/limit/region_alias")
def query_failed_vstation_task_message(
    region: Annotated[str, Field(description="地域，如 ap-guangzhou")],
    task_id: Annotated[Optional[List[str]], Field(description="VStation任务ID")] = [],
    instance_id: Annotated[Optional[List[str]], Field(description="实例ID，格式为ins-xxxxxxxx")] = [],
    uuid: Annotated[Optional[List[str]], Field(description="UUID，格式为8a23be54-f4cf-4a4b-95b7-8d3eda6fd803")] = [],
    request_id: Annotated[Optional[List[str]], Field(description="请求ID")] = [],
    host_ip: Annotated[Optional[List[str]], Field(description="母机/宿主机的IP")] = [],
    owner: Annotated[Optional[List[str]], Field(description="客户Owner")] = [],
    start_time: Annotated[Optional[str], Field(description="起始时间，格式：YYYY-MM-DD HH:mm:ss")] = None,
    end_time: Annotated[Optional[str], Field(description="结束时间，格式：YYYY-MM-DD HH:mm:ss")] = None,
    limit: Annotated[int, Field(description="分页长度")] = 100,
    region_alias: Annotated[Optional[str], Field(description="地域别名")] = None
) -> str:
    """
    查询 VStation 任务列表
    Args:
        region: 地域，如 ap-guangzhou
        task_id: VStation任务ID
        instance_id: 实例ID
        uuid: 任务UUID
        request_id: 请求ID
        host_ip: 母机/宿主机 IP
        start_time: 起始时间，格式：YYYY-MM-DD HH:mm:ss（可选，默认当天 00:00:00）
        end_time: 结束时间，格式：YYYY-MM-DD HH:mm:ss（可选，默认当天 23:59:59）
        region_alias: 地域别名（可选，若未传则自动匹配）
    Returns:
        str: 查询结果的JSON字符串
    """
    # 自动补全时间
    if not start_time or not end_time:
        today = datetime.now().strftime("%Y-%m-%d")
        if not start_time:
            start_time = f"{today} 00:00:00"
        if not end_time:
            end_time = f"{today} 23:59:59"
    alias = _get_region_alias(region, region_alias)
    filters = []
    error_codes = [
        102101, 102102, 102103, 102104, 102105, 102200,
        102201, 102202, 102203, 102204, 102205, 102206, 102207, 102208, 102209, 102210,
        102211, 102212, 102213, 102214, 102215, 102216, 102217, 102218, 102219, 102220,
        102221, 102222, 102223, 102224, 102225, 102226, 102227, 102228, 102229, 102230,
        102231, 102232, 102233, 102234, 102235, 102236, 102237, 102238, 102239, 102240,
        102241, 102242, 102243, 102244, 102245, 102246, 102247, 102248, 102249, 102250,
        102251, 102252, 102253, 102254, 102255, 102256, 102257, 102258, 102259, 102260,
        102261, 102262, 102264, 102265, 102266, 102267, 102268, 102269, 102270, 102271,
        102272, 102273, 102274, 102275, 102276, 102277, 102278, 102279, 102280, 102281,
        102282, 102283, 102284, 102285, 102286, 102287, 102289, 102290, 102291, 102292
    ]
    filters.append({
        "Name": "code",
        "Values": list(map(str, error_codes))
    })

    if task_id:
        filters.append({
            "Name": "task_id",
            "Values": task_id
        })
    if request_id:
        filters.append({
            "Name": "requestId",
            "Values": request_id
        })
    if uuid:
        filters.append({
            "Name": "uuid",
            "Values": uuid
        })
    if instance_id:
        filters.append({
            "Name": "uInstanceId",
            "Values": instance_id
        })
    if host_ip:
        filters.append({
            "Name": "hostIp",
            "Values": host_ip
        })
    if owner:
        filters.append({
            "Name": "owner",
            "Values": owner
        })


    params = {
        "Region": region,
        "Filters": filters,
        "StartTime": start_time,
        "EndTime": end_time,
        "Offset": 0,
        "Limit": limit,
        "Action": "QueryTaskMessage",
        "AppId": "251006228",
        "RequestSource": "YunXiao",
        "SubAccountUin": "493083759",
        "Uin": "493083759",
        "regionAlias": alias,
        "Fields": [
            "taskStatus",
            "code",
            "errorMsg",
            "hostIp",
            "region",
            "requestId",
            "startTime",
            "taskId",
            "taskName",
            "taskProgress",
            "taskState",
            "traceRequestId",
            "uInstanceId",
            "uuid",
            "finishTime",
            "updateTime",
        ]
    }
    return _call_api("/weaver/upstream/terra/QueryTaskMessage", params)


@mcp.tool(description="查询VStation错误码（VStation简称VS）")
def query_vstation_error_codes(
    region: Annotated[str, Field(description="地域，如 ap-guangzhou")],
    region_alias: Annotated[Optional[str], Field(description="地域别名")] = None
) -> str:
    """
    查询 VStation 错误码
    Args:
        region: 地域，如 ap-guangzhou
        region_alias: 地域别名（可选，若未传则自动匹配）
    Returns:
        str: 查询结果的JSON字符串
    """
    alias = _get_region_alias(region, region_alias)
    params = {
        "Region": region,
        "AppId": "251006228",
        "Action": "DescribeErrorCodes",
        "Uin": "493083759",
        "SubAccountUin": "493083759",
        "RequestSource": "YunXiao",
        "regionAlias": alias
    }
    return _call_api("/weaver/upstream/terra/QueryTaskMessage", params)


@mcp.tool(description="查询宿主机/母机Compute任务列表，支持批量查询和并发控制")
def query_host_task_list(
        region: Annotated[str, Field(description="地域，如 ap-guangzhou")],
        host: Annotated[str, Field(description="宿主机IP/hostIp")],
        vs_task_id: Annotated[str, Field(description="taskId/VStation任务ID（支持逗号分隔的多个ID）")],
        region_alias: Annotated[Optional[str], Field(description="地域别名")] = None,
        max_workers: Annotated[int, Field(description="最大并发查询数")] = 5
) -> str:
    """
    查询 Compute 任务列表，支持批量查询和并发控制

    Args:
        region: 地域，如 ap-guangzhou
        host: 宿主机IP
        vs_task_id: VStation任务ID（支持逗号分隔的多个ID）
        region_alias: 地域别名（可选）
        max_workers: 最大并发查询数（默认5）

    Returns:
        str: 合并后的查询结果JSON字符串
    """
    # 处理多个任务ID的情况
    task_ids = [tid.strip() for tid in str(vs_task_id).split(",") if tid.strip()]
    if not task_ids:
        return json.dumps({"error": "No valid task IDs provided"})

    alias = _get_region_alias(region, region_alias)
    results = {}

    def _query_single_task(task_id: str) -> tuple:
        """单个任务的查询函数"""
        try:
            params = {
                "TaskId": int(task_id),  # 转换为整数保持兼容性
                "Host": host,
                "Region": region,
                "Action": "DescribeHostTask",
                "AppId": "251006228",
                "RequestSource": "QCLOUD_OP",
                "SubAccountUin": "493083759",
                "Uin": "493083759",
                "regionAlias": alias
            }
            result = _call_api("/weaver/upstream/terra/DescribeHostTask", params)
            return (task_id, {"status": "success", "data": json.loads(result)})
        except Exception as e:
            return (task_id, {"status": "error", "error": str(e)})

    # 使用线程池控制并发数
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = {
            executor.submit(_query_single_task, task_id): task_id
            for task_id in task_ids
        }

        for future in as_completed(futures):
            task_id, result = future.result()
            results[task_id] = result

    return json.dumps(results, indent=2)


@mcp.tool(description="查询母机Compute任务的执行日志详细信息，支持批量查询和并发控制")
def query_host_task_detail(
        region: Annotated[str, Field(description="地域，如 ap-guangzhou")],
        host_ip: Annotated[str, Field(description="宿主机IP")],
        host_task_id: Annotated[str, Field(
            description="母机/宿主机/Compute组件的任务ID，为query_host_task返回的taskid字段。注意这里不要和VS任务ID混淆。")],
        region_alias: Annotated[Optional[str], Field(description="地域别名")] = None,
        max_workers: Annotated[int, Field(description="最大并发查询数")] = 5
) -> str:
    """
    查询 Compute 任务的执行日志，支持批量查询和并发控制

    Args:
        region: 地域，如 ap-guangzhou
        host_ip: 宿主机IP
        host_task_id: 母机/宿主机任务ID（支持逗号分隔的多个ID）
        region_alias: 地域别名（可选）
        max_workers: 最大并发查询数（默认5）

    Returns:
        str: 合并后的查询结果JSON字符串
    """
    # 处理多个任务ID的情况
    task_ids = [tid.strip() for tid in host_task_id.split(",") if tid.strip()]
    if not task_ids:
        return json.dumps({"error": "No valid task IDs provided"})

    alias = _get_region_alias(region, region_alias)
    results = {}

    def _query_single_task(task_id: str) -> tuple:
        """单个任务的查询函数"""
        params = {
            "TaskId": task_id,
            "HostIp": host_ip,
            "Region": region,
            "Action": "QueryTaskLog",
            "AppId": "1251783334",
            "RequestSource": "YunXiao",
            "SubAccountUin": "3205597606",
            "Uin": "3205597606",
            "regionAlias": alias
        }
        try:
            result = _call_api("/weaver/upstream/terra/QueryTaskLog", params)
            return (task_id, {"status": "success", "data": json.loads(result)})
        except Exception as e:
            return (task_id, {"status": "error", "error": str(e)})

    # 使用线程池控制并发数
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = {
            executor.submit(_query_single_task, task_id): task_id
            for task_id in task_ids
        }

        for future in as_completed(futures):
            task_id, result = future.result()
            results[task_id] = result

    return json.dumps(results, indent=2)


def _call_compute(ip: str, method: str, data: dict, check: bool = True) -> str:
    """
    发送请求到Compute服务
    Args:
        ip: 宿主机IP地址
        method: 请求方法名
        data: 请求数据
        check: 是否检查返回数据

    Returns:
        str: 返回的JSON字符串
    """
    req_params = {
        "username": "vstation",
        "password": "vstation",
        "data": data,
        "command": method,
        "ip": ip
    }
    return _call_api("/weaver/upstream/compute/CommonTools", req_params)


def _call_compute_log(ip: str, logname: str = 'procedure', timestr: Optional[str] = None) -> Optional[str]:
    """
    请求日志文件
    Args:
        ip: 宿主机IP地址
        logname: 日志名称
        timestr: 时间字符串

    Returns:
        Optional[str]: 日志内容或None
    """
    req_params = {
        "username": "vstation",
        "password": "vstation",
        "data": {'hostIp': ip},
        "ip": ip,
        "logname": logname,
        "timestr": timestr
    }
    return _call_api_raw("/weaver/upstream/compute/ComputeLog", req_params)


@mcp.tool(description="获取母机/宿主机/Compute状态信息和当前子机列表")
def get_host_stat(
        ip: Annotated[str, Field(description="宿主机IP地址")],
        raw: Annotated[bool, Field(description="是否返回原始数据")] = False
) -> str:
    """
    获取宿主机状态信息，包括CPU、内存、虚拟机列表等

    Args:
        ip: 宿主机IP地址
        raw: 是否返回原始数据（不进行格式化处理）

    Returns:
        str: JSON格式的宿主机状态信息
    """
    payload = {"debug": True}
    return _call_compute(ip, "get_host_stat", payload)


@mcp.tool(description="获取虚拟机/子机XML信息/配置")
def get_vm_xml(
        ip: Annotated[str, Field(description="宿主机IP地址")],
        uuid: Annotated[str, Field(description="虚拟机UUID，格式为8a23be54-f4cf-4a4b-95b7-8d3eda6fd803")],
        static: Annotated[bool, Field(description="是否获取静态配置")] = False
) -> str:
    """
    获取虚拟机的XML配置信息

    Args:
        ip: 宿主机IP地址
        uuid: 虚拟机UUID
        static: 是否获取静态配置

    Returns:
        str: 虚拟机的XML配置
    """
    payload = {
        "username": "vstation",
        "uuid": [uuid],
        "static": static,
        "password": "vstation",
        "command": "get_vm_xml"
    }
    return _call_compute(ip, "get_vm_xml", payload)


@mcp.tool(description="查询虚拟机cpu/cpuset/Pico信息")
def query_vm_pico(
        ip: Annotated[str, Field(description="宿主机IP地址")],
        uuid: Annotated[
            str, Field(description="虚拟机UUID，格式为8a23be54-f4cf-4a4b-95b7-8d3eda6fd803")],
        date_str: Annotated[str, Field(description="日期字符串，格式: YYYYMMDD")],
        time_str: Annotated[str, Field(description="时间字符串，格式: HH:MM:SS")]
) -> str:
    """
    查询虚拟机的Pico信息

    Args:
        ip: 宿主机IP地址
        uuid: 虚拟机UUID
        date_str: 日期字符串
        time_str: 时间字符串

    Returns:
        str: JSON格式的Pico信息
    """

    def _parse_date(date_str: str) -> datetime:
        try:
            return datetime.strptime(date_str, "%Y%m%d")
        except:
            try:
                return datetime.strptime(date_str, "%Y-%m-%d")
            except:
                try:
                    return datetime.strptime(date_str, "%Y_%m_%d")
                except:
                    raise ValueError("Invalid date format")

    def _parse_time(time_str: str) -> datetime:
        try:
            return datetime.strptime(time_str, "%H:%M:%S")
        except:
            try:
                return datetime.strptime(time_str, "%H%M%S")
            except:
                raise ValueError("Invalid time format")

    counter = 0
    date_obj = _parse_date(date_str)
    while True:
        ret = _call_compute_log(ip, "dump", datetime.strftime(date_obj, "%Y%m%d"))
        if ret is None:
            return json.dumps({"error": "Date not found"})
        the_log = ret.get('log', '')
        the_log = the_log.strip().split("\n")
        for line in the_log[::-1]:
            if not line:
                break
            if (_parse_time(time_str) >= _parse_time(line[1:9]) and
                    uuid in line):
                ghs_data = eval(line[line.find("{"):])
                return json.dumps({
                    "found_at": f"{datetime.strftime(date_obj, '%Y-%m-%d')} {line[1:9]}",
                    "data": ghs_data
                }, indent=4)

        time_str = "23:59:59"
        date_obj = date_obj - timedelta(days=1)
        counter += 1
        if counter >= 10:
            return json.dumps({"error": "Reached max search depth"})


@mcp.tool(description="查询母机/宿主机/Compute健康状态")
def health_check(
        ip: Annotated[str, Field(description="宿主机IP地址")],
        version: Annotated[Optional[int], Field(description="版本号")] = None
) -> str:
    """
    查询宿主机的健康状态

    Args:
        ip: 宿主机IP地址
        version: 版本号

    Returns:
        str: JSON格式的健康状态信息
    """
    payload = {"debug": True}
    return _call_compute(ip, "health_check", payload)
