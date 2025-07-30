from typing import Annotated, Optional, List, Dict
from pydantic import Field
from .client import _call_api
from . import mcp
from datetime import datetime
import json

@mcp.tool(description="查询库存(不支持多地域查询)")
def describe_inventory(
    region: Annotated[str, Field(description="地域")],
    zone: Annotated[Optional[str], Field(description="可用区")] = None,
    instance_family: Annotated[Optional[str], Field(description="实例族")] = None,
    instance_type: Annotated[Optional[str], Field(description="实例类型")] = None,
    offset: Annotated[int, Field(description="偏移量")] = 0,
    limit: Annotated[int, Field(description="每页数量")] = 100
) -> str:
    """查询库存数据(不支持多地域查询)
    
    Args:
        region: 地域
        zone: 可用区
        instance_family: 实例族
        instance_type: 实例类型
        offset: 偏移量
        limit: 每页数量
        
    Returns:
        str: 查询结果的JSON字符串，包含如下字段：
            - 可用区 (str): 可用区名称
            - 实例族 (str): 实例族名称
            - 实例类型 (str): 实例类型
            - 实例CPU数 (str): CPU核数（带单位"核"）
            - 实例内存 (str): 内存大小
            - 实例GPU数 (str): GPU数量
            - 库存 (str): 库存数量（带单位"核"）
            - 数据更新时间 (str): 数据更新时间，格式：YYYY-MM-DD HH:MM:SS
            - totalCount (int): 总记录数
    """
    request_body = {
        "chargeType": [2],
        "pool": ["public"],
        "offset": offset,
        "limit": limit,
        "region": region
    }
    if zone:
        request_body["zone"] = [zone]
    if instance_family:
        request_body["instanceFamily"] = instance_family
    if instance_type:
        request_body["instanceType"] = [instance_type]
    response = _call_api("/beacon/ceres/instance-sales-config/list", request_body)
    # 处理响应数据
    result = {}
    response = json.loads(response)
    if "data" in response:
        data = response["data"]
        result["data"] = [{
            "可用区": item["zone"],
            "实例族": item["instanceFamily"],
            "实例类型": item["instanceType"],
            "实例CPU数": f"{item['cpu']}核",
            "实例内存": item["mem"],
            "实例GPU数": item["gpu"],
            "库存": f"{item['inventory']}核",
            "数据更新时间": datetime.fromtimestamp(item["updateTime"] / 1000).strftime("%Y-%m-%d %H:%M:%S")
        } for item in data["data"]]
        result["totalCount"] = data["totalCount"]
    return json.dumps(result, ensure_ascii=False)

@mcp.tool(description="查询多维度库存指标数据，包括不同核心数库存、售卖比率、资源消耗、预留、规模、故障状态等详细信息")
def describe_stock_metrics(
    customhouse: Annotated[Optional[list[str]], Field(description="境内外")] = None,
    region_alias: Annotated[Optional[list[str]], Field(description="地域别名")] = None,
    region: Annotated[Optional[list[str]], Field(description="地域")] = None,
    zone_id: Annotated[Optional[list[int]], Field(description="可用区ID")] = None,
    zone: Annotated[Optional[list[str]], Field(description="可用区")] = None,
    instance_family: Annotated[Optional[list[str]], Field(description="实例族")] = None,
    device_class: Annotated[Optional[list[str]], Field(description="设备类型")] = None,
    zone_sales_strategy: Annotated[Optional[str], Field(description="可用区状态")] = None,
    instance_family_state: Annotated[Optional[list[str]], Field(description="实例族状态")] = None,
    instance_category: Annotated[Optional[str], Field(description="实例分组")] = None,
    instance_family_supply_state: Annotated[Optional[str], Field(description="实例售卖状态")] = None,
    sort: Annotated[Optional[list], Field(description="排序，可排序字段：cpuStock(库存), cpuStock16c(16C库存), cpuStock32c(32C库存), cpuStock64c(64C库存), cpuStock128c(128C库存), successfulRate(购买成功率), sellThroughRate(售罄比例), sellRate(非空售卖率), sellRateUpperLimit(理论非空售卖率), sellOutInstanceTypeCount(售罄实例类型数), cpuConsumption(消耗), cpuConsumption16c(16C消耗), cpuAccumulatedConsumption(当天累积消耗), cpuAccumulatedConsumption16c(16C当天累积消耗), cpuReservedIdle(空闲预扣块), cpuReservedLongTimeIdle(空闲预扣块(长期预扣)), cpuFaultReserve(故障预留), cpuInBuffer(缓冲区(8号)), cpuInReserveAppMask(逻辑区(非1号)), cpuEmpty(空母机), cpuPowerOff(关机), cpuTagged(有标签), cpuOrigin(物理核规模), cpuTotal(总规模), cpuOffline(线下资源), cpuMax(峰值), currentCpuInc(规模增量)。示例：[{\"property\": \"cpuStock\", \"direction\": \"DESC\"}]")] = None,
    page_number: Annotated[int, Field(description="分页")] = 1,
    page_size: Annotated[int, Field(description="分页大小")] = 20
) -> str:
    """预测库存指标查询
    Args:
        customhouse: 境内外
        main_instance_family: 主力机型
        main_zone: 主力园区
        region_alias: 地域别名
        region: 地域
        zone_id: 可用区ID
        zone: 可用区
        instance_family: 实例族
        device_class: 设备类型
        zone_sales_strategy: 可用区状态
        instance_family_state: 实例族状态
        instance_category: 实例分组
        instance_family_supply_state: 实例售卖状态
        sort: 排序，可排序字段：cpuStock(库存), cpuStock16c(16C库存), cpuStock32c(32C库存), cpuStock64c(64C库存), cpuStock128c(128C库存), successfulRate(购买成功率), sellThroughRate(售罄比例), sellRate(非空售卖率), sellRateUpperLimit(理论非空售卖率), sellOutInstanceTypeCount(售罄实例类型数), cpuConsumption(消耗), cpuConsumption16c(16C消耗), cpuAccumulatedConsumption(当天累积消耗), cpuAccumulatedConsumption16c(16C当天累积消耗), cpuReservedIdle(空闲预扣块), cpuReservedLongTimeIdle(空闲预扣块(长期预扣)), cpuFaultReserve(故障预留), cpuInBuffer(缓冲区(8号)), cpuInReserveAppMask(逻辑区(非1号)), cpuEmpty(空母机), cpuPowerOff(关机), cpuTagged(有标签), cpuOrigin(物理核规模), cpuTotal(总规模), cpuOffline(线下资源), cpuMax(峰值), currentCpuInc(规模增量)。示例：[{"property": "cpuStock", "direction": "DESC"}]
        page_number: 分页
        page_size: 分页大小
    Returns:
        str: 预测库存指标的JSON字符串，包含如下字段：
            - cpuStock (int): 库存
            - cpuStock16c (int): 16C库存
            - cpuStock32c (int): 32C库存
            - cpuStock64c (int): 64C库存
            - cpuStock128c (int): 128C库存
            - successfulRate (float): 购买成功率
            - sellThroughRate (float): 售罄比例
            - sellRate (float): 非空售卖率
            - sellRateUpperLimit (float): 理论非空售卖率
            - sellOutInstanceTypeCount (int): 售罄实例类型数
            - cpuConsumption (int): 消耗
            - cpuConsumption16c (int): 16C消耗
            - cpuAccumulatedConsumption (int): 当天累积消耗
            - cpuAccumulatedConsumption16c (int): 16C当天累积消耗
            - cpuReservedIdle (int): 空闲预扣块
            - cpuReservedLongTimeIdle (int): 空闲预扣块(长期预扣)
            - cpuFaultReserve (int): 故障预留
            - cpuInBuffer (int): 缓冲区(8号)
            - cpuInReserveAppMask (int): 逻辑区(非1号)
            - cpuEmpty (int): 空母机
            - cpuPowerOff (int): 关机
            - cpuTagged (int): 有标签
            - cpuOrigin (int): 物理核规模
            - cpuTotal (int): 总规模
            - cpuOffline (int): 线下资源
            - cpuMax (int): 峰值
            - currentCpuInc (int): 规模增量
            - totalCount (int): 总记录数
    """
    params = {}
    if customhouse is not None:
        params["customhouse"] = customhouse
    if region_alias is not None:
        params["regionAlias"] = region_alias
    if region is not None:
        params["region"] = region
    if zone_id is not None:
        params["zoneId"] = zone_id
    if zone is not None:
        params["zone"] = zone
    if instance_family is not None:
        params["instanceFamily"] = instance_family
    if device_class is not None:
        params["deviceClass"] = device_class
    if zone_sales_strategy is not None:
        params["zoneSalesStrategy"] = zone_sales_strategy
    if instance_family_state is not None:
        params["instanceFamilyState"] = instance_family_state
    if instance_category is not None:
        params["instanceCategory"] = instance_category
    if instance_family_supply_state is not None:
        params["instanceFamilySupplyState"] = instance_family_supply_state
    if sort is not None:
        params["sort"] = sort
    if page_number is not None:
        params["pageNumber"] = page_number
    if page_size is not None:
        params["pageSize"] = page_size
    response = _call_api("/beacon/stock-metrics/list", params)
    return response

@mcp.tool(description="查询库存（支持多地域查询）")
def describe_cvm_type_config(
    region: Annotated[List[str], Field(description="地域")],
    has_total_count: Annotated[bool, Field(description="是否返回总数")] = True,
    limit: Annotated[int, Field(description="分页大小")] = 20,
    next_token: Annotated[Optional[str], Field(description="分页Token")] = None,
    instance_type: Annotated[Optional[List[str]], Field(description="实例类型列表")] = None,
    instance_family: Annotated[Optional[List[str]], Field(description="实例族")] = None,
    zone_id: Annotated[Optional[list], Field(description="可用区ID列表")] = None,
    zone: Annotated[Optional[list], Field(description="可用区列表")] = None,
    cpu: Annotated[Optional[list], Field(description="CPU核数列表")] = None,
    gpu: Annotated[Optional[list], Field(description="GPU数量列表")] = None,
    mem: Annotated[Optional[list], Field(description="内存大小列表")] = None,
    storage_block: Annotated[Optional[list], Field(description="存储块大小列表")] = None,
    sell_out: Annotated[Optional[bool], Field(description="是否售罄")] = None,
    status: Annotated[Optional[list], Field(description="状态列表")] = None,
    sort: Annotated[Optional[list], Field(description="排序规则")] = None,
    offset: Annotated[Optional[int], Field(description="偏移量")] = None
) -> str:
    """查询库存（支持多地域查询）
    Args:
        has_total_count: 是否返回总数
        limit: 分页大小
        next_token: 分页Token
        instance_type: 实例类型列表
        instance_family: 实例族
        zone_id: 可用区ID列表
        zone: 可用区列表
        cpu: CPU核数列表
        gpu: GPU数量列表
        mem: 内存大小列表
        storage_block: 存储块大小列表
        sell_out: 是否售罄
        status: 状态列表
        region: 地域
        sort: 排序规则
        offset: 偏移量
    Returns:
        str: 库存信息的JSON字符串，包含如下字段：
            - Region (str): 地域
            - Zone (str): 可用区
            - InstanceType (str): 实例类型
            - InstanceFamily (str): 实例族
            - CPU (int): CPU核数
            - Memory (int): 内存大小 (GB)
            - GPU (int): GPU数量
            - StorageBlock (str): 存储块大小
            - Status (str): 状态
            - SellOut (bool): 是否售罄
            - TotalCount (int): 总记录数
    """
    params = {
        "sort": [{"field": "cpu", "order": "DESC"}, {"field": "instanceFamily", "order": "DESC"}]
    }
    if has_total_count is not None:
        params["hasTotalCount"] = has_total_count
    if limit is not None:
        params["limit"] = limit
    if next_token is not None:
        params["nextToken"] = next_token
    if instance_type is not None:
        params["instanceType"] = instance_type
    if instance_family is not None:
        params["instanceFamily"] = instance_family
    if zone_id is not None:
        params["zoneId"] = zone_id
    if zone is not None:
        params["zone"] = zone
    if cpu is not None:
        params["cpu"] = cpu
    if gpu is not None:
        params["gpu"] = gpu
    if mem is not None:
        params["mem"] = mem
    if storage_block is not None:
        params["storageBlock"] = storage_block
    if sell_out is not None:
        params["sellOut"] = sell_out
    if status is not None:
        params["status"] = status
    if region is not None:
        params["region"] = region
    if sort is not None:
        params["sort"] = sort
    if offset is not None:
        params["offset"] = offset
    return _call_api("/beacon/cvm-type-config-new/list", params)

@mcp.tool(description="查询库存指标元数据（指标描述信息）")
def beacon_stock_metrics_metrics() -> str:
    """
    查询库存指标元数据
    Returns:
        str: 库存指标元数据的JSON字符串，包含指标的名称、描述等信息。
    """
    return _call_api("/beacon/stock-metrics/metrics", {}) 