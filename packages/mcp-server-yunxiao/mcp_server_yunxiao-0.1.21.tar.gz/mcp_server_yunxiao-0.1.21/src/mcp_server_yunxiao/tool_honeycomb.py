from typing import Annotated, List
from pydantic import Field
from .client import _call_api
from . import mcp

@mcp.tool(description="查询宿主机关联实例")
def query_host_instance(
    region: Annotated[str, Field(description="地域，如 ap-shanghai")],
    ip: Annotated[List[str], Field(description="宿主机IP列表")],
) -> str:
    """查询宿主机关联实例
    
    Args:
        region: 地域，如 ap-shanghai
        ip: 宿主机IP列表
    Returns:
        str: 查询结果的JSON字符串
    """
    params = {
        "region": region,
        "ip": ip
    }
    return _call_api("/honeycomb/host/instance", params)

@mcp.tool(description="查询宿主机关联预扣块")
def query_host_grid(
    region: Annotated[str, Field(description="地域，如 ap-shanghai")],
    ip: Annotated[List[str], Field(description="宿主机IP列表")],
) -> str:
    """查询宿主机关联预扣块
    
    Args:
        region: 地域，如 ap-shanghai
        ip: 宿主机IP列表
    Returns:
        str: 查询结果的JSON字符串
    """
    params = {
        "region": region,
        "ip": ip
    }
    return _call_api("/honeycomb/host/grid", params) 