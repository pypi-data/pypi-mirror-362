from typing import Annotated, Optional, List, Dict
from pydantic import Field
from .client import _call_api
from . import mcp

@mcp.tool(description="查询竞价实例上架机型详细信息，包括价格、库存（含OC实例）及用量数据。返回字段：oc_enable(是否启用OC), oc_quota(OC库存), price_cur(竞价价格), quota(可用量), capacity_allot(用量)等")
def list_spot_goods(
    instance_type: Annotated[Optional[str], Field(description="实例类型")] = None,
    instance_family: Annotated[Optional[str], Field(description="实例族")] = None,
    region: Annotated[Optional[str], Field(description="地域")] = None,
    region_alias: Annotated[Optional[str], Field(description="地域别名")] = None,
    zone: Annotated[Optional[str], Field(description="可用区")] = None,
    zones: Annotated[Optional[List[str]], Field(description="可用区列表")] = None,
    sort: Annotated[Optional[List[Dict]], Field(description="排序")] = None,
    page_number: Annotated[Optional[int], Field(description="页码")] = None,
    page_size: Annotated[Optional[int], Field(description="每页数量")] = None
) -> str:
    """查询竞价实例上架机型，包含价格及库存

    Args:
        instance_type: 实例类型
        instance_family: 实例族
        region: 地域
        region_alias: 地域别名
        zone: 可用区
        zones: 可用区列表
        sort: 排序
        page_number: 页码
        page_size: 每页数量

    Returns:
        str: 竞价实例上架机型列表的JSON字符串，包含如下字段：
            - oc_enable (bool): 是否启用OC实例(离线实例)
            - oc_quota (int): OC实例(离线实例)库存
            - oc_capacity_allot (float): OC实例(离线实例)用量
            - price_pri (float): 按量价格
            - price_cur (float): 竞价价格
            - price_pri_i18n (float): 国际站按量价格
            - price_cur_i18n (float): 国际站竞价价格
            - quota (int): 可用量
            - rc_quota (int): rc_quota字段 (值为0)
            - capacity_allot (float): 用量
            # ... 其他可能的字段
    """
    params = {}
    if instance_type is not None:
        params["instanceType"] = instance_type
    if instance_family is not None:
        params["instanceFamily"] = instance_family
    if region is not None:
        params["region"] = region
    if region_alias is not None:
        params["regionAlias"] = region_alias
    if zone is not None:
        params["zone"] = zone
    if zones is not None:
        params["zones"] = zones
    if sort is not None:
        params["sort"] = sort
    if page_number is not None:
        params["pageNumber"] = page_number
    if page_size is not None:
        params["pageSize"] = page_size
    return _call_api("/spot/goods/list", params)

@mcp.tool(description="查询用户的特殊价格")
def query_user_special_price(
    instance_type: Annotated[Optional[str], Field(description="实例类型")] = None,
    instance_family: Annotated[Optional[str], Field(description="实例族")] = None,
    owner: Annotated[Optional[str], Field(description="拥有者")] = None,
    region: Annotated[Optional[str], Field(description="地域")] = None,
    region_alias: Annotated[Optional[str], Field(description="地域别名")] = None,
    zone: Annotated[Optional[str], Field(description="可用区")] = None,
    zones: Annotated[Optional[List[str]], Field(description="可用区列表")] = None,
    sort: Annotated[Optional[List[Dict]], Field(description="排序")] = None,
    page_number: Annotated[Optional[int], Field(description="页码")] = None,
    page_size: Annotated[Optional[int], Field(description="每页数量")] = None
) -> str:
    """查询用户的特殊价格

    Args:
        instance_type: 实例类型
        instance_family: 实例族
        owner: 拥有者
        region: 地域
        region_alias: 地域别名
        zone: 可用区
        zones: 可用区列表
        sort: 排序
        page_number: 页码
        page_size: 每页数量

    Returns:
        str: 特殊价格列表的JSON字符串
    """
    params = {}
    if instance_type is not None:
        params["instanceType"] = instance_type
    if instance_family is not None:
        params["instanceFamily"] = instance_family
    if owner is not None:
        params["owner"] = owner
    if region is not None:
        params["region"] = region
    if region_alias is not None:
        params["regionAlias"] = region_alias
    if zone is not None:
        params["zone"] = zone
    if zones is not None:
        params["zones"] = zones
    if sort is not None:
        params["sort"] = sort
    if page_number is not None:
        params["pageNumber"] = page_number
    if page_size is not None:
        params["pageSize"] = page_size
    return _call_api("/spot/special-price", params)

@mcp.tool(description="查询针对客户配置的竞价实例保留时长")
def query_user_reserve_time(
    owner: Annotated[Optional[str], Field(description="Owner")] = None,
    region: Annotated[Optional[str], Field(description="地域")] = None,
    region_alias: Annotated[Optional[str], Field(description="地域别名")] = None,
    zone: Annotated[Optional[str], Field(description="可用区")] = None,
    zones: Annotated[Optional[List[str]], Field(description="可用区列表")] = None,
    sort: Annotated[Optional[List[Dict]], Field(description="排序")] = None,
    page_number: Annotated[Optional[int], Field(description="页码")] = None,
    page_size: Annotated[Optional[int], Field(description="每页数量")] = None
) -> str:
    """查询针对客户配置的竞价实例保留时长

    Args:
        owner: Owner
        region: 地域
        region_alias: 地域别名
        zone: 可用区
        zones: 可用区列表
        sort: 排序
        page_number: 页码
        page_size: 每页数量

    Returns:
        str: 竞价实例保留时长的JSON字符串
    """
    params = {}
    if owner is not None:
        params["owner"] = owner
    if region is not None:
        params["region"] = region
    if region_alias is not None:
        params["regionAlias"] = region_alias
    if zone is not None:
        params["zone"] = zone
    if zones is not None:
        params["zones"] = zones
    if sort is not None:
        params["sort"] = sort
    if page_number is not None:
        params["pageNumber"] = page_number
    if page_size is not None:
        params["pageSize"] = page_size
    return _call_api("/spot/user-reserve-time", params) 