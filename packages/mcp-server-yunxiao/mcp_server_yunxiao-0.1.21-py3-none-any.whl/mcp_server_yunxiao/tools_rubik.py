from typing import Annotated, Optional, List
from pydantic import Field
from .client import _call_api
from . import mcp

@mcp.tool(description="查询资源预扣单")
def describe_reservation_forms(
    page_number: Annotated[int, Field(description="页码，默认1")] = 1,
    page_size: Annotated[int, Field(description="每页数量，默认20，最大100")] = 20,
    instance_family: Annotated[Optional[List[str]], Field(description="机型族列表，可选")] = [],
    instance_type: Annotated[Optional[List[str]], Field(description="机型列表，可选")] = [],
    order_id: Annotated[Optional[str], Field(description="关联预约单ID")] = None,
    order_created: Annotated[Optional[bool], Field(description="是否预约单创建")] = None,
    creator: Annotated[Optional[str], Field(description="创建者")] = None,
    app_id: Annotated[Optional[str], Field(description="客户AppID")] = None,
    app_name: Annotated[Optional[str], Field(description="客户名称")] = None,
    uin: Annotated[Optional[str], Field(description="UIN")] = None,
    region: Annotated[Optional[str], Field(description="地域")] = None,
    zone: Annotated[Optional[List[str]], Field(description="可用区列表")] = None,
    status: Annotated[Optional[List[str]], Field(description="状态列表")] = None,
    instance_category: Annotated[Optional[List[str]], Field(description="实例分组列表")] = None,
    customhouse: Annotated[Optional[List[str]], Field(description="境内外列表，可选值：境内/境外")] = None
) -> str:
    """查询资源预扣单
    
    Args:
        page_number: 页码，默认1
        page_size: 每页数量，默认20，最大100
        instance_family: 机型族列表，可选
        instance_type: 机型列表，可选
        order_id: 关联预约单ID
        order_created: 是否预约单创建
        creator: 创建者
        app_id: 客户AppID
        app_name: 客户名称
        uin: UIN
        region: 地域
        zone: 可用区列表
        status: 状态列表
        instance_category: 实例分组列表
        customhouse: 境内外列表，可选值：境内/境外
        
    Returns:
        str: 预扣单列表的JSON字符串
    """
    params = {
        "pageNumber": page_number,
        "pageSize": page_size
    }
    if instance_family:
        params["instanceFamily"] = instance_family
    if instance_type:
        params["instanceType"] = instance_type
    if order_id:
        params["orderId"] = order_id
    if order_created is not None:
        params["orderCreated"] = order_created
    if creator:
        params["creator"] = creator
    if app_id:
        params["appId"] = app_id
    if app_name:
        params["appName"] = app_name
    if uin:
        params["uin"] = uin
    if region:
        params["region"] = region
    if zone:
        params["zone"] = zone
    if status:
        params["status"] = status
    if instance_category:
        params["instanceCategory"] = instance_category
    if customhouse:
        params["customhouse"] = customhouse
    return _call_api("/rubik/reservation-form/list", params)

@mcp.tool(description="查询预扣信息根据可用区和实例类型聚合统计分析")
def describe_grid_by_zone_instance_type(
    region: Annotated[str, Field(description="地域")],
    has_total_count: Annotated[Optional[bool], Field(description="是否返回总数")] = None,
    limit: Annotated[Optional[int], Field(description="分页大小")] = None,
    next_token: Annotated[Optional[str], Field(description="分页标记")] = None,
    region_alias: Annotated[Optional[str], Field(description="地域别名")] = None,
    reserve_package: Annotated[Optional[bool], Field(description="是否预扣资源包")] = None,
    reserve_mode: Annotated[Optional[List[str]], Field(description="预扣类型列表")] = None,
    status: Annotated[Optional[List[str]], Field(description="状态列表")] = None,
    greater_than_days: Annotated[Optional[int], Field(description="大于天数")] = None,
    less_than_days: Annotated[Optional[int], Field(description="小于天数")] = None,
    healthy: Annotated[Optional[bool], Field(description="是否健康")] = None,
    has_pico: Annotated[Optional[bool], Field(description="是否有Pico标记")] = None,
    has_match_rule: Annotated[Optional[bool], Field(description="是否有MatchRule")] = None,
    grid_owner: Annotated[Optional[List[str]], Field(description="块Owner列表")] = None,
    grid_id: Annotated[Optional[List[int]], Field(description="块Id列表")] = None,
    zone: Annotated[Optional[List[str]], Field(description="可用区列表")] = None,
    instance_family: Annotated[Optional[List[str]], Field(description="实例族列表")] = None,
    disaster_recover_tag: Annotated[Optional[List[str]], Field(description="置放群组列表")] = None,
    instance_type: Annotated[Optional[List[str]], Field(description="实例类型列表")] = None,
    hypervisor: Annotated[Optional[List[str]], Field(description="hypervisor列表")] = None,
    host_ip: Annotated[Optional[List[str]], Field(description="IP地址列表")] = None,
    host_type: Annotated[Optional[List[str]], Field(description="母机机型列表")] = None,
    zone_id: Annotated[Optional[List[int]], Field(description="可用区ID列表")] = None,
    rack_id: Annotated[Optional[List[int]], Field(description="机架号列表")] = None,
    pool: Annotated[Optional[List[str]], Field(description="资源池列表")] = None,
    offset: Annotated[Optional[int], Field(description="偏移量")] = None
) -> str:
    """查询预扣信息根据可用区和实例类型聚合统计分析
    Args:
        has_total_count: 是否返回总数
        limit: 分页大小
        next_token: 分页标记
        region: 地域
        region_alias: 地域别名
        reserve_package: 是否预扣资源包
        reserve_mode: 预扣类型列表
        status: 状态列表
        greater_than_days: 大于天数
        less_than_days: 小于天数
        healthy: 是否健康
        has_pico: 是否有Pico标记
        has_match_rule: 是否有MatchRule
        grid_owner: 块Owner列表
        grid_id: 块Id列表
        zone: 可用区列表
        instance_family: 实例族列表
        disaster_recover_tag: 置放群组列表
        instance_type: 实例类型列表
        hypervisor: hypervisor列表
        host_ip: IP地址列表
        host_type: 母机机型列表
        zone_id: 可用区ID列表
        rack_id: 机架号列表
        pool: 资源池列表
        sort: 排序规则
        offset: 偏移量
    Returns:
        预扣信息聚合统计结果的JSON字符串
    """
    params = {
        "region": region,
        "limit": 200,
        "pool": ["qcloud"],
        "status": ["idle"],
        "hasTotalCount": False,
        "offset": 0,
        "sort": [{"property": "totalCpuCount", "direction": "DESC"}]
    }
    if limit is not None:
        params["limit"] = limit
    if next_token is not None:
        params["nextToken"] = next_token
    if has_total_count is not None:
        params["hasTotalCount"] = has_total_count
    if region is not None:
        params["region"] = region
    if region_alias is not None:
        params["regionAlias"] = region_alias
    if reserve_package is not None:
        params["reservePackage"] = reserve_package
    if reserve_mode is not None:
        params["reserveMode"] = reserve_mode
    if status is not None:
        params["status"] = status
    if greater_than_days is not None:
        params["greaterThanDays"] = greater_than_days
    if less_than_days is not None:
        params["lessThanDays"] = less_than_days
    if healthy is not None:
        params["healthy"] = healthy
    if has_pico is not None:
        params["hasPico"] = has_pico
    if has_match_rule is not None:
        params["hasMatchRule"] = has_match_rule
    if grid_owner is not None:
        params["gridOwner"] = grid_owner
    if grid_id is not None:
        params["gridId"] = grid_id
    if zone is not None:
        params["zone"] = zone
    if instance_family is not None:
        params["instanceFamily"] = instance_family
    if disaster_recover_tag is not None:
        params["disasterRecoverTag"] = disaster_recover_tag
    if instance_type is not None:
        params["instanceType"] = instance_type
    if hypervisor is not None:
        params["hypervisor"] = hypervisor
    if host_ip is not None:
        params["hostIp"] = host_ip
    if host_type is not None:
        params["hostType"] = host_type
    if zone_id is not None:
        params["zoneId"] = zone_id
    if rack_id is not None:
        params["rackId"] = rack_id
    if pool is not None:
        params["pool"] = pool
    if offset is not None:
        params["offset"] = offset
    return _call_api("/rubik/grid/group-by-zone-instance-type", params) 