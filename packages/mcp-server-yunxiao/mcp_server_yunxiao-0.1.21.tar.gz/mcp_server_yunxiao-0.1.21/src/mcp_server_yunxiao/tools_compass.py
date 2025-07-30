from typing import Annotated, Optional, List
from pydantic import Field
from .client import _call_api
from . import mcp
import json

@mcp.tool(description="查询售卖推荐数据")
def describe_sale_policies(
    page_number: Annotated[int, Field(description="页码，默认1")] = 1,
    page_size: Annotated[int, Field(description="每页数量，默认20，最大100")] = 200,
    customhouse: Annotated[list[str], Field(description="境内外列表，可选值：境内/境外")] = None,
    region_alias: Annotated[list[str], Field(description="地域别名列表")] = None,
    region: Annotated[list[str], Field(description="地域列表")] = None,
    zone_id: Annotated[list[int], Field(description="可用区ID列表")] = None,
    zone: Annotated[list[str], Field(description="可用区列表")] = None,
    instance_family: Annotated[list[str], Field(description="实例族列表")] = None,
    instance_category: Annotated[list[str], Field(description="实例分组列表，可选值：CVM/GPU/FPGA/BARE_METAL")] = None,
    instance_family_state: Annotated[list[str], Field(description="实例族状态列表")] = None,
    instance_family_supply_state: Annotated[list[str], Field(description="实例族供货状态列表，可选值：LTS/EOL")] = None,
    zone_state: Annotated[list[str], Field(description="可用区状态列表")] = None,
    stock_state: Annotated[list[str], Field(description="库存状态列表")] = None,
    sales_policy: Annotated[list[int], Field(description="售卖建议列表")] = None
) -> str:
    """查询售卖推荐数据
    
    Args:
        page_number (int): 页码，默认1
        page_size (int): 每页数量，默认20，最大100
        customhouse (list[str]): 境内外列表，可选值：境内/境外
        region_alias (list[str]): 地域别名列表
        region (list[str]): 地域列表
        zone_id (list[int]): 可用区ID列表
        zone (list[str]): 可用区列表
        instance_family (list[str]): 实例族列表
        instance_category (list[str]): 实例分组列表，可选值：CVM/GPU/FPGA/BARE_METAL
        instance_family_state (list[str]): 实例族状态列表
        instance_family_supply_state (list[str]): 实例族供货状态列表，可选值：LTS/EOL
        zone_state (list[str]): 可用区状态列表
        stock_state (list[str]): 库存状态列表
        sales_policy (list[int]): 售卖建议列表
        
    Returns:
        str: 售卖策略和库存信息的JSON字符串
    """
    params = {
        "pageNumber": page_number,
        "pageSize": page_size,
        "sort": [
            {
                "property": "stock",
                "direction": "DESC"
            } 
        ]
    }
    if customhouse:
        params["customhouse"] = customhouse
    if region_alias:
        params["regionAlias"] = region_alias
    if region:
        params["region"] = region
    if zone_id:
        params["zoneId"] = zone_id
    if zone:
        params["zone"] = zone
    if instance_family:
        params["instanceFamily"] = instance_family
    if instance_category:
        params["instanceCategory"] = instance_category
    else:
        params["instanceCategory"] = ['CVM', 'GPU', 'FPGA', 'BARE_METAL']
    if instance_family_state:
        params["instanceFamilyState"] = instance_family_state
    if instance_family_supply_state:
        params["instanceFamilySupplyState"] = instance_family_supply_state
    if zone_state:
        params["zoneState"] = zone_state
    if stock_state:
        params["stockState"] = stock_state
    if sales_policy:
        params["salesPolicy"] = sales_policy
    response = _call_api("/compass/sales-policy/list", params)
    # 处理响应数据
    result = {}
    response = json.loads(response)
    if "data" in response:
        data = response["data"]
        result["data"] = [{
            "customhouse": item["customhouse"],
            "zoneName": item["zoneName"],
            "instanceFamily": item["instanceFamily"],
            "实例族售卖状态": {
                "PRINCIPAL": "主力",
                "SECONDARY": "非主力"
            }.get(item["instanceFamilyState"], item["instanceFamilyState"]),
            "实例族供货策略": {
                "LTS": "持续供应",
                "EOL": "停止供应"
            }.get(item["instanceFamilySupplyState"], item["instanceFamilySupplyState"]),
            "可用区售卖策略": {
                "PRINCIPAL": "主力",
                "SECONDARY": "非主力"
            }.get(item["zoneState"], item["zoneState"]),
            "实例分类": item["instanceCategory"],
            "库存情况": {
                "WithStock": "库存充足",
                "ClosedWithStock": "库存紧张",
                "WithoutStock": "售罄"
            }.get(item["stockState"], item["stockState"]),
            "售卖策略": {
                0: "未知",
                1: "推荐购买",
                2: "正常购买",
                3: "即将售罄",
                4: "联系购买",
                5: "无法购买",
                6: "请预约"
            }.get(item["salesPolicy"], "未知"),
            "库存/核": f"{item.get('stock', 0)}核",
            "十六核以上库存核": f"{item.get('stock16c', 0)}核",
            "数据更新时间": item["updateTime"]
        } for item in data["data"]]
        result["totalCount"] = data["totalCount"]
    return json.dumps(result, ensure_ascii=False)

@mcp.tool(description="查询运营指标数据")
def describe_operation_metrics(
    stat_time: Annotated[Optional[str], Field(description="日期，格式：YYYY-MM-DD")] = None,
    zone: Annotated[Optional[list[str]], Field(description="可用区列表")] = None,
    zone_id: Annotated[Optional[list[int]], Field(description="可用区ID列表")] = None,
    device_class: Annotated[Optional[list[str]], Field(description="设备类型列表")] = None,
    instance_family: Annotated[Optional[list[str]], Field(description="实例族列表")] = None,
    customhouse: Annotated[Optional[list[str]], Field(description="境内外列表")] = None,
    region_alias: Annotated[Optional[list[str]], Field(description="地域别名列表")] = None,
    region: Annotated[Optional[list[str]], Field(description="地域列表")] = None,
    instance_category: Annotated[Optional[list[str]], Field(description="实例分组列表，可选值：CVM/GPU/FPGA/BARE_METAL")] = None,
    instance_family_state: Annotated[Optional[list[str]], Field(description="实例族状态列表")] = None,
    instance_family_supply_state: Annotated[Optional[list[str]], Field(description="实例族供货状态列表，可选值：LTS/EOL")] = None,
    zone_state: Annotated[Optional[list[str]], Field(description="可用区状态列表")] = None
) -> str:
    """查询运营指标数据
    
    Args:
        stat_time: 日期，格式：YYYY-MM-DD
        zone: 可用区列表
        zone_id: 可用区ID列表
        device_class: 设备类型列表
        instance_family: 实例族列表
        customhouse: 境内外列表
        region_alias: 地域别名列表
        region: 地域列表
        instance_category: 实例分组列表，可选值：CVM/GPU/FPGA/BARE_METAL
        instance_family_state: 实例族状态列表
        instance_family_supply_state: 实例族供货状态列表，可选值：LTS/EOL
        zone_state: 可用区状态列表
    Returns:
        str: 运营指标数据的JSON字符串
    """
    params = {}
    if stat_time:
        params["statTime"] = stat_time
    if zone:
        params["zone"] = zone
    if zone_id:
        params["zoneId"] = zone_id
    if device_class:
        params["deviceClass"] = device_class
    if instance_family:
        params["instanceFamily"] = instance_family
    if customhouse:
        params["customhouse"] = customhouse
    if region_alias:
        params["regionAlias"] = region_alias
    if region:
        params["region"] = region
    if instance_category:
        params["instanceCategory"] = instance_category
    if instance_family_state:
        params["instanceFamilyState"] = instance_family_state
    if instance_family_supply_state:
        params["instanceFamilySupplyState"] = instance_family_supply_state
    if zone_state:
        params["zoneState"] = zone_state
    return _call_api("/compass/operation-metrics/list-all", params)

@mcp.tool(description="查询预计交付和采购到货信息")
def describe_buy_flow_promise_info(
    page_number: Annotated[int, Field(description="页码，默认1")] = 1,
    page_size: Annotated[int, Field(description="每页数量，默认20")] = 20,
    region: Annotated[Optional[List[str]], Field(description="地域列表")] = None,
    zone: Annotated[Optional[List[str]], Field(description="可用区列表")] = None,
    instance_family: Annotated[Optional[List[str]], Field(description="实例族列表")] = None,
    start_time: Annotated[Optional[str], Field(description="开始时间，格式：YYYY-MM-DD")] = None,
    end_time: Annotated[Optional[str], Field(description="结束时间，格式：YYYY-MM-DD")] = None
) -> str:
    """查询预计交付和采购到货信息
    
    Args:
        page_number: 页码，默认1
        page_size: 每页数量，默认20
        region: 地域列表
        instance_family: 实例族列表
        start_time: 开始时间，格式：YYYY-MM-DD
        end_time: 结束时间，格式：YYYY-MM-DD
        
    Returns:
        str: 预计交付信息的JSON字符串
    """
    params = {
        "pageNumber": page_number,
        "pageSize": page_size
    }
    if region:
        params["region"] = region
    if zone:
        params["zone"] = zone
    if instance_family:
        params["instanceFamily"] = instance_family
    if start_time:
        params["startTime"] = start_time
    if end_time:
        params["endTime"] = end_time
    return _call_api("/compass/buy-flow-promise-info/query", params)

@mcp.tool(description="查询库存观测指标和库存水位历史数据")
def describe_stock_metrics_history(
    customhouse: Annotated[Optional[List[str]], Field(description="境内外列表")] = None,
    instance_family: Annotated[Optional[List[str]], Field(description="实例族列表")] = None,
    region: Annotated[Optional[List[str]], Field(description="地域列表")] = None,
    zone: Annotated[Optional[List[str]], Field(description="可用区列表")] = None,
    topic_id: Annotated[Optional[str], Field(description="主题ID")] = None,
    limit: Annotated[Optional[int], Field(description="每页数量")] = None,
    next_token: Annotated[Optional[str], Field(description="分页标记")] = None
) -> str:
    """查询库存观测指标和库存水位历史数据
    
    Args:
        customhouse: 境内外列表
        instance_family: 实例族列表
        region: 地域列表
        zone: 可用区列表
        topic_id: 主题ID
        limit: 每页数量
        next_token: 分页标记
        
    Returns:
        str: 库存观测指标和库存水位历史数据的JSON字符串
    """
    params = {}
    if customhouse:
        params["customhouse"] = customhouse
    if instance_family:
        params["instanceFamily"] = instance_family
    if region:
        params["region"] = region
    if zone:
        params["zone"] = zone
    if topic_id:
        params["topicId"] = topic_id
    if limit:
        params["limit"] = limit
    if next_token:
        params["nextToken"] = next_token
    return _call_api("/compass/operation-metrics/history", params) 