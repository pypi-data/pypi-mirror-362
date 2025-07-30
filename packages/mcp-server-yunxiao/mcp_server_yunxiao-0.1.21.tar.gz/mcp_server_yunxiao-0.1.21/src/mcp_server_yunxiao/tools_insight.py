from typing import Annotated, Optional, List, Dict
from pydantic import Field
from .client import _call_api
from . import mcp

@mcp.tool(description="查询VStation购买失败记录")
def describe_purchase_failed_alarms(
    limit: Annotated[int, Field(description="分页大小，最大100")] = 100,
    distinct: Annotated[bool, Field(description="去重")] = True,
    pool: Annotated[Optional[List[str]], Field(description="资源池列表")] = ['qcloud'],
    instance_family: Annotated[Optional[List[str]], Field(description="实例族列表")] = None,
    sort: Annotated[Optional[List[Dict]], Field(description="排序规则")] = None,
    start_timestamp: Annotated[Optional[int], Field(description="起始时间戳")] = None,
    end_timestamp: Annotated[Optional[int], Field(description="结束时间戳")] = None,
    app_id: Annotated[Optional[str], Field(description="客户APPID")] = None,
    owner_uin: Annotated[Optional[str], Field(description="UIN")] = None,
    app_ids: Annotated[Optional[List[str]], Field(description="客户APPID列表")] = None,
    uin: Annotated[Optional[List[str]], Field(description="UIN列表")] = None,
    region: Annotated[Optional[List[str]], Field(description="地域列表")] = None,
    zone: Annotated[Optional[List[str]], Field(description="可用区列表")] = None,
    eks_flag: Annotated[Optional[bool], Field(description="EKS标记")] = False,
    error_code: Annotated[Optional[str], Field(description="错误码")] = None,
    error_message: Annotated[Optional[str], Field(description="错误信息")] = None,
    count: Annotated[Optional[int], Field(description="错误次数")] = None,
    only_privilege: Annotated[Optional[bool], Field(description="是否仅查询大客户购买失败事件")] = None,
    next_token: Annotated[Optional[str], Field(description="分页token")] = None
) -> str:
    """查询VStation购买失败记录
    
    Args:
        distinct: 去重
        instance_family: 实例族列表
        limit: 分页大小，最大100
        sort: 排序规则
        start_timestamp: 起始时间戳
        end_timestamp: 结束时间戳
        app_id: 客户APPID
        owner_uin: UIN
        pool: 资源池列表
        app_ids: 客户APPID列表
        uin: UIN列表
        region: 地域列表
        zone: 可用区列表
        eks_flag: EKS标记
        error_code: 错误码
        error_message: 错误信息
        count: 错误次数
        only_privilege: 是否仅查询大客户购买失败事件
        next_token: 分页token
        
    Returns:
        str: 购买失败记录的JSON字符串
    """
    params = {
        "limit": limit,
        "distinct": distinct,
        "taskName": 'instance_launch',
        "pool": pool
    }
    if instance_family is not None:
        params["instanceFamily"] = instance_family
    if sort is not None:
        params["sort"] = sort
    if start_timestamp is not None:
        params["startTimestamp"] = start_timestamp
    if end_timestamp is not None:
        params["endTimestamp"] = end_timestamp
    if app_id is not None:
        params["appId"] = app_id
    if owner_uin is not None:
        params["ownerUin"] = owner_uin
    if app_ids is not None:
        params["appIds"] = app_ids
    if uin is not None:
        params["uin"] = uin
    if region is not None:
        params["region"] = region
    if zone is not None:
        params["zone"] = zone
    if eks_flag is not None:
        params["eksFlag"] = eks_flag
    if error_code is not None:
        params["errorCode"] = error_code
    if error_message is not None:
        params["errorMessage"] = error_message
    if count is not None:
        params["count"] = count
    if only_privilege is not None:
        params["onlyPrivilege"] = only_privilege
    if next_token is not None:
        params["nextToken"] = next_token
    return _call_api("/insight/purchase-failed-alarm/records", params)

@mcp.tool(description="查询因资源问题造成用户购买失败的事件")
def query_purchase_failed_resource_cause(
    limit: Annotated[int, Field(description="分页大小")] = 100,
    task_name: Annotated[List[str], Field(description="任务类型列表")] = ['instance_launch'],
    pool: Annotated[List[str], Field(description="资源池列表")] = ['qcloud'],
    app_id: Annotated[Optional[List[str]], Field(description="客户APPID列表")] = None,
    uin: Annotated[Optional[List[str]], Field(description="UIN列表")] = None,
    region: Annotated[Optional[List[str]], Field(description="地域列表")] = None,
    zone: Annotated[Optional[List[str]], Field(description="可用区列表")] = None,
    zone_id: Annotated[Optional[List[int]], Field(description="可用区ID列表")] = None,
    cvm_pay_mode: Annotated[Optional[List[str]], Field(description="支付类型列表")] = None,
    instance_id: Annotated[Optional[List[str]], Field(description="实例ID列表")] = None,
    instance_type: Annotated[Optional[List[str]], Field(description="实例类型列表")] = None,
    instance_family: Annotated[Optional[List[str]], Field(description="实例族列表")] = None,
    not_instance_family: Annotated[Optional[List[str]], Field(description="排除的实例族列表")] = None,
    start_time: Annotated[Optional[str], Field(description="起始时间，格式：YYYY-MM-DD HH:mm:ss")] = None,
    end_time: Annotated[Optional[str], Field(description="结束时间，格式：YYYY-MM-DD HH:mm:ss")] = None,
    success: Annotated[Optional[bool], Field(description="是否成功")] = None,
    eks_flag: Annotated[Optional[bool], Field(description="EKS标记")] = None,
    error_code: Annotated[Optional[str], Field(description="错误码")] = None,
    error_message: Annotated[Optional[str], Field(description="错误信息")] = None,
    main_zone: Annotated[Optional[bool], Field(description="是否主力园区")] = None,
    inner_user: Annotated[Optional[bool], Field(description="是否内部客户")] = None,
    customhouse: Annotated[Optional[List[str]], Field(description="境内外列表，可选值：境内/境外")] = None,
    next_token: Annotated[Optional[str], Field(description="分页Token")] = None,
    offset: Annotated[Optional[int], Field(description="偏移量")] = None
) -> str:
    """查询因资源问题造成用户购买失败的事件
    
    Args:
        task_name: 任务名称, instance_terminate: 实例销毁，instance_launch: 实例启动
        pool: 资源池列表
        app_id: 客户APPID列表
        uin: UIN列表
        region: 地域列表
        zone: 可用区列表
        zone_id: 可用区ID列表
        cvm_pay_mode: 支付类型列表
        instance_id: 实例ID列表
        instance_type: 实例类型列表
        instance_family: 实例族列表
        not_instance_family: 排除的实例族列表
        limit: 分页大小
        start_time: 起始时间，格式：YYYY-MM-DD HH:mm:ss
        end_time: 结束时间，格式：YYYY-MM-DD HH:mm:ss
        success: 是否成功
        eks_flag: EKS标记
        error_code: 错误码
        error_message: 错误信息
        main_zone: 是否主力园区
        inner_user: 是否内部客户
        customhouse: 境内外列表，可选值：境内/境外
        next_token: 分页Token
        offset: 偏移量
    Returns:
        str: VStation任务事件的JSON字符串
    """
    params = {}
    if pool is not None:
        params["pool"] = pool
    if limit is not None:
        params["limit"] = limit
    if task_name is not None:
        params["taskName"] = task_name
    if app_id is not None:
        params["appId"] = app_id
    if uin is not None:
        params["uin"] = uin
    if region is not None:
        params["region"] = region
    if zone is not None:
        params["zone"] = zone
    if zone_id is not None:
        params["zoneId"] = zone_id
    if cvm_pay_mode is not None:
        params["cvmPayMode"] = cvm_pay_mode
    if instance_id is not None:
        params["instanceId"] = instance_id
    if instance_type is not None:
        params["instanceType"] = instance_type
    if instance_family is not None:
        params["instanceFamily"] = instance_family
    if not_instance_family is not None:
        params["notInstanceFamily"] = not_instance_family
    if start_time is not None:
        params["startTime"] = start_time
    if end_time is not None:
        params["endTime"] = end_time
    if success is not None:
        params["success"] = success
    if eks_flag is not None:
        params["eksFlag"] = eks_flag
    if error_code is not None:
        params["errorCode"] = error_code
    if error_message is not None:
        params["errorMessage"] = error_message
    if main_zone is not None:
        params["mainZone"] = main_zone
    if inner_user is not None:
        params["innerUser"] = inner_user
    if customhouse is not None:
        params["customhouse"] = customhouse
    if next_token is not None:
        params["nextToken"] = next_token
    if offset is not None:
        params["offset"] = offset
    return _call_api("/insight/query-purchase-failed-resource-cause", params)

@mcp.tool(description="查询VStation任务事件")
def describe_vstation_events(
    limit: Annotated[int, Field(description="分页大小")] = 100,
    task_name: Annotated[List[str], Field(description="任务类型列表")] = ['instance_launch'],
    pool: Annotated[List[str], Field(description="资源池列表")] = ['qcloud'],
    app_id: Annotated[Optional[List[str]], Field(description="客户APPID列表")] = None,
    uin: Annotated[Optional[List[str]], Field(description="UIN列表")] = None,
    region: Annotated[Optional[List[str]], Field(description="地域列表")] = None,
    zone: Annotated[Optional[List[str]], Field(description="可用区列表")] = None,
    zone_id: Annotated[Optional[List[int]], Field(description="可用区ID列表")] = None,
    cvm_pay_mode: Annotated[Optional[List[str]], Field(description="支付类型列表")] = None,
    instance_id: Annotated[Optional[List[str]], Field(description="实例ID列表")] = None,
    instance_type: Annotated[Optional[List[str]], Field(description="实例类型列表")] = None,
    instance_family: Annotated[Optional[List[str]], Field(description="实例族列表")] = None,
    not_instance_family: Annotated[Optional[List[str]], Field(description="排除的实例族列表")] = None,
    start_time: Annotated[Optional[str], Field(description="起始时间，格式：YYYY-MM-DD HH:mm:ss")] = None,
    end_time: Annotated[Optional[str], Field(description="结束时间，格式：YYYY-MM-DD HH:mm:ss")] = None,
    success: Annotated[Optional[bool], Field(description="是否成功")] = None,
    eks_flag: Annotated[Optional[bool], Field(description="EKS标记")] = None,
    error_code: Annotated[Optional[str], Field(description="错误码")] = None,
    error_message: Annotated[Optional[str], Field(description="错误信息")] = None,
    main_zone: Annotated[Optional[bool], Field(description="是否主力园区")] = None,
    inner_user: Annotated[Optional[bool], Field(description="是否内部客户")] = None,
    customhouse: Annotated[Optional[List[str]], Field(description="境内外列表，可选值：境内/境外")] = None,
    next_token: Annotated[Optional[str], Field(description="分页Token")] = None,
    offset: Annotated[Optional[int], Field(description="偏移量")] = None
) -> str:
    """查询VStation任务事件
    Args:
        task_name: 任务名称, instance_terminate: 实例销毁，instance_launch: 实例启动
        pool: 资源池列表
        app_id: 客户APPID列表
        uin: UIN列表
        region: 地域列表
        zone: 可用区列表
        zone_id: 可用区ID列表
        cvm_pay_mode: 支付类型列表
        instance_id: 实例ID列表
        instance_type: 实例类型列表
        instance_family: 实例族列表
        not_instance_family: 排除的实例族列表
        limit: 分页大小
        start_time: 起始时间，格式：YYYY-MM-DD HH:mm:ss
        end_time: 结束时间，格式：YYYY-MM-DD HH:mm:ss
        success: 是否成功
        eks_flag: EKS标记
        error_code: 错误码
        error_message: 错误信息
        main_zone: 是否主力园区
        inner_user: 是否内部客户
        customhouse: 境内外列表，可选值：境内/境外
        next_token: 分页Token
        offset: 偏移量
    Returns:
        str: VStation任务事件的JSON字符串
    """
    params = {}
    if pool is not None:
        params["pool"] = pool
    if limit is not None:
        params["limit"] = limit
    if task_name is not None:
        params["taskName"] = task_name
    if app_id is not None:
        params["appId"] = app_id
    if uin is not None:
        params["uin"] = uin
    if region is not None:
        params["region"] = region
    if zone is not None:
        params["zone"] = zone
    if zone_id is not None:
        params["zoneId"] = zone_id
    if cvm_pay_mode is not None:
        params["cvmPayMode"] = cvm_pay_mode
    if instance_id is not None:
        params["instanceId"] = instance_id
    if instance_type is not None:
        params["instanceType"] = instance_type
    if instance_family is not None:
        params["instanceFamily"] = instance_family
    if not_instance_family is not None:
        params["notInstanceFamily"] = not_instance_family
    if start_time is not None:
        params["startTime"] = start_time
    if end_time is not None:
        params["endTime"] = end_time
    if success is not None:
        params["success"] = success
    if eks_flag is not None:
        params["eksFlag"] = eks_flag
    if error_code is not None:
        params["errorCode"] = error_code
    if error_message is not None:
        params["errorMessage"] = error_message
    if main_zone is not None:
        params["mainZone"] = main_zone
    if inner_user is not None:
        params["innerUser"] = inner_user
    if customhouse is not None:
        params["customhouse"] = customhouse
    if next_token is not None:
        params["nextToken"] = next_token
    if offset is not None:
        params["offset"] = offset
    return _call_api("/insight/vstation-event", params)

@mcp.tool(description="查询用户退还TOP（资源净增为负）")
def describe_user_activity_top_decrease(
    device_class: Annotated[Optional[List[str]], Field(description="设备类型列表")] = None,
    instance_family: Annotated[Optional[List[str]], Field(description="实例族")] = None,
    instance_type: Annotated[Optional[List[str]], Field(description="实例类型")] = None,
    pool: Annotated[Optional[List[str]], Field(description="资源池")] = None,
    region: Annotated[Optional[List[str]], Field(description="地域")] = None,
    zone: Annotated[Optional[List[str]], Field(description="可用区")] = None,
    start_time: Annotated[Optional[str], Field(description="起始时间，时间格式:YYYY-MM-DD HH:MM:SS")] = None,
    end_time: Annotated[Optional[str], Field(description="结束时间，时间格式:YYYY-MM-DD HH:MM:SS")] = None,
    main_zone: Annotated[Optional[bool], Field(description="是否主力园区")] = None,
    main_instance_family: Annotated[Optional[bool], Field(description="是否主力机型")] = None,
    customhouse: Annotated[Optional[List[str]], Field(description="境内外列表，可选值：境内/境外")] = None,
    instance_category: Annotated[Optional[str], Field(description="实例分类")] = None,
    next_token: Annotated[Optional[str], Field(description="分页标记")] = None,
    offset: Annotated[Optional[int], Field(description="偏移量")] = None,
    limit: Annotated[Optional[int], Field(description="分页大小")] = None,
    app_id: Annotated[Optional[List[str]], Field(description="客户APPID列表")] = None,
    uin: Annotated[Optional[List[str]], Field(description="UIN列表")] = None,
) -> str:
    """
    查询资源退还TOP

    Args:
        device_class: 设备类型列表
        instance_family: 实例族
        instance_type: 实例类型
        limit: 分页大小
        pool: 资源池
        region: 地域
        zone: 可用区
        start_time: 起始时间
        end_time: 结束时间
        main_zone: 是否主力园区
        main_instance_family: 是否主力机型
        customhouse: 境内外列表，可选值：境内/境外
        instance_category: 实例分类
        next_token: 分页标记
        offset: 偏移量
        app_id: 客户APPID列表
        uin: UIN列表
    Returns:
        str: 资源退还TOP的JSON字符串
    """
    params = {}
    if device_class is not None:
        params["deviceClass"] = device_class
    if instance_family is not None:
        params["instanceFamily"] = instance_family
    if instance_type is not None:
        params["instanceType"] = instance_type
    if limit is not None:
        params["limit"] = limit
    if pool is not None:
        params["pool"] = pool
    if region is not None:
        params["region"] = region
    if zone is not None:
        params["zone"] = zone
    if start_time is not None:
        params["startTime"] = start_time
    if end_time is not None:
        params["endTime"] = end_time
    if main_zone is not None:
        params["mainZone"] = main_zone
    if main_instance_family is not None:
        params["mainInstanceFamily"] = main_instance_family
    if customhouse is not None:
        params["customhouse"] = customhouse
    if instance_category is not None:
        params["instanceCategory"] = instance_category
    if next_token is not None:
        params["nextToken"] = next_token
    if offset is not None:
        params["offset"] = offset
    if app_id is not None:
        params["appId"] = app_id
    if uin is not None:
        params["uin"] = uin
    return _call_api("/insight/user-activity/top-decrease", params)

@mcp.tool(description="查询用户购买TOP（资源净增为正）")
def describe_user_activity_top_increase(
    device_class: Annotated[Optional[List[str]], Field(description="设备类型列表")] = None,
    instance_family: Annotated[Optional[List[str]], Field(description="实例族")] = None,
    instance_type: Annotated[Optional[List[str]], Field(description="实例类型")] = None,
    pool: Annotated[Optional[List[str]], Field(description="资源池")] = None,
    region: Annotated[Optional[List[str]], Field(description="地域，如：ap-guanghzou")] = None,
    zone: Annotated[Optional[List[str]], Field(description="可用区，如：ap-guangzhou-1")] = None,
    start_time: Annotated[Optional[str], Field(description="起始时间，时间格式:YYYY-MM-DD HH:MM:SS")] = None,
    end_time: Annotated[Optional[str], Field(description="结束时间，时间格式:YYYY-MM-DD HH:MM:SS")] = None,
    main_zone: Annotated[Optional[bool], Field(description="是否主力园区")] = None,
    main_instance_family: Annotated[Optional[bool], Field(description="是否主力机型")] = None,
    customhouse: Annotated[Optional[List[str]], Field(description="境内外列表，可选值：境内/境外")] = None,
    instance_category: Annotated[Optional[str], Field(description="实例分类")] = None,
    next_token: Annotated[Optional[str], Field(description="分页标记")] = None,
    offset: Annotated[Optional[int], Field(description="偏移量")] = None,
    limit: Annotated[Optional[int], Field(description="分页大小")] = None,
    app_id: Annotated[Optional[List[str]], Field(description="客户APPID列表")] = None,
    uin: Annotated[Optional[List[str]], Field(description="UIN列表")] = None,
) -> str:
    """
    查询资源增长TOP

    Args:
        device_class: 设备类型列表
        instance_family: 实例族
        instance_type: 实例类型
        limit: 分页大小
        pool: 资源池
        region: 地域
        zone: 可用区
        start_time: 起始时间
        end_time: 结束时间
        main_zone: 是否主力园区
        main_instance_family: 是否主力机型
        customhouse: 境内外列表，可选值：境内/境外
        instance_category: 实例分类
        next_token: 分页标记
        offset: 偏移量
        app_id: 客户APPID列表
        uin: UIN列表
    Returns:
        str: 资源增长TOP的JSON字符串
    """
    params = {}
    if device_class is not None:
        params["deviceClass"] = device_class
    if instance_family is not None:
        params["instanceFamily"] = instance_family
    if instance_type is not None:
        params["instanceType"] = instance_type
    if limit is not None:
        params["limit"] = limit
    if pool is not None:
        params["pool"] = pool
    if region is not None:
        params["region"] = region
    if zone is not None:
        params["zone"] = zone
    if start_time is not None:
        params["startTime"] = start_time
    if end_time is not None:
        params["endTime"] = end_time
    if main_zone is not None:
        params["mainZone"] = main_zone
    if main_instance_family is not None:
        params["mainInstanceFamily"] = main_instance_family
    if customhouse is not None:
        params["customhouse"] = customhouse
    if instance_category is not None:
        params["instanceCategory"] = instance_category
    if next_token is not None:
        params["nextToken"] = next_token
    if offset is not None:
        params["offset"] = offset
    if app_id is not None:
        params["appId"] = app_id
    if uin is not None:
        params["uin"] = uin
    return _call_api("/insight/user-activity/top-increase", params)

@mcp.tool(description="查询活跃资源TOP（退还和购买累加）")
def describe_user_activity_top_active(
    device_class: Annotated[Optional[List[str]], Field(description="设备类型列表")] = None,
    instance_family: Annotated[Optional[List[str]], Field(description="实例族")] = None,
    instance_type: Annotated[Optional[List[str]], Field(description="实例类型")] = None,
    pool: Annotated[Optional[List[str]], Field(description="资源池")] = None,
    region: Annotated[Optional[List[str]], Field(description="地域")] = None,
    zone: Annotated[Optional[List[str]], Field(description="可用区")] = None,
    start_time: Annotated[Optional[str], Field(description="起始时间，时间格式:YYYY-MM-DD HH:MM:SS")] = None,
    end_time: Annotated[Optional[str], Field(description="结束时间，时间格式:YYYY-MM-DD HH:MM:SS")] = None,
    main_zone: Annotated[Optional[bool], Field(description="是否主力园区")] = None,
    main_instance_family: Annotated[Optional[bool], Field(description="是否主力机型")] = None,
    customhouse: Annotated[Optional[List[str]], Field(description="境内外列表，可选值：境内/境外")] = None,
    instance_category: Annotated[Optional[str], Field(description="实例分类")] = None,
    next_token: Annotated[Optional[str], Field(description="分页标记")] = None,
    offset: Annotated[Optional[int], Field(description="偏移量")] = None,
    limit: Annotated[Optional[int], Field(description="分页大小")] = None,
    app_id: Annotated[Optional[List[str]], Field(description="客户APPID列表")] = None,
    uin: Annotated[Optional[List[str]], Field(description="UIN列表")] = None,
) -> str:
    """
    查询活跃资源TOP

    Args:
        device_class: 设备类型列表
        instance_family: 实例族
        instance_type: 实例类型
        limit: 分页大小
        pool: 资源池
        region: 地域
        zone: 可用区
        start_time: 起始时间
        end_time: 结束时间
        main_zone: 是否主力园区
        main_instance_family: 是否主力机型
        customhouse: 境内外列表，可选值：境内/境外
        instance_category: 实例分类
        next_token: 分页标记
        offset: 偏移量
        app_id: 客户APPID列表
        uin: UIN列表

    Returns:
        str: 活跃资源TOP的JSON字符串
    """
    params = {}
    if device_class is not None:
        params["deviceClass"] = device_class
    if instance_family is not None:
        params["instanceFamily"] = instance_family
    if instance_type is not None:
        params["instanceType"] = instance_type
    if limit is not None:
        params["limit"] = limit
    if pool is not None:
        params["pool"] = pool
    if region is not None:
        params["region"] = region
    if zone is not None:
        params["zone"] = zone
    if start_time is not None:
        params["startTime"] = start_time
    if end_time is not None:
        params["endTime"] = end_time
    if main_zone is not None:
        params["mainZone"] = main_zone
    if main_instance_family is not None:
        params["mainInstanceFamily"] = main_instance_family
    if customhouse is not None:
        params["customhouse"] = customhouse
    if instance_category is not None:
        params["instanceCategory"] = instance_category
    if next_token is not None:
        params["nextToken"] = next_token
    if offset is not None:
        params["offset"] = offset
    if app_id is not None:
        params["appId"] = app_id
    if uin is not None:
        params["uin"] = uin
    return _call_api("/insight/user-activity/top-active", params)

@mcp.tool(description="聚合统计VStation事件（可用于统计用户购买退还情况）")
def vstation_event_aggregate(
    group_by: Annotated[Optional[List[str]], Field(description="分组字段")] = None,
    sort: Annotated[Optional[List[Dict]], Field(description="排序")] = None,
    start_time: Annotated[Optional[str], Field(description="起始时间，格式：YYYY-MM-DD HH:mm:ss")] = None,
    end_time: Annotated[Optional[str], Field(description="结束时间，格式：YYYY-MM-DD HH:mm:ss")] = None,
    task_name: Annotated[Optional[List[str]], Field(description="任务类型列表，可选值：实例创建(instance_launch)、实例销毁(instance_terminate)、实例关机(instance_power_off)、实例开机(instance_power_on)")] = None,
    pool: Annotated[Optional[List[str]], Field(description="资源池列表")] = None,
    app_id: Annotated[Optional[List[str]], Field(description="客户APPID列表")] = None,
    uin: Annotated[Optional[List[str]], Field(description="UIN列表")] = None,
    success: Annotated[Optional[bool], Field(description="是否成功")] = None,
    region: Annotated[Optional[List[str]], Field(description="地域列表")] = None,
    zone: Annotated[Optional[List[str]], Field(description="可用区列表")] = None,
    zone_id: Annotated[Optional[List[int]], Field(description="可用区ID列表")] = None,
    cvm_pay_mode: Annotated[Optional[List[str]], Field(description="支付类型列表")] = None,
    eks_flag: Annotated[Optional[bool], Field(description="EKS标记")] = None,
    error_code: Annotated[Optional[str], Field(description="错误码")] = None,
    error_message: Annotated[Optional[str], Field(description="错误信息")] = None,
    instance_id: Annotated[Optional[List[str]], Field(description="实例ID列表")] = None,
    instance_type: Annotated[Optional[List[str]], Field(description="实例类型列表")] = None,
    instance_family: Annotated[Optional[List[str]], Field(description="实例族列表")] = None,
    not_instance_family: Annotated[Optional[List[str]], Field(description="排除的实例族列表")] = None,
    main_zone: Annotated[Optional[bool], Field(description="是否主力园区")] = None,
    inner_user: Annotated[Optional[bool], Field(description="是否内部客户")] = None,
    customhouse: Annotated[Optional[List[str]], Field(description="境内外列表，可选值：境内/境外")] = None,
    next_token: Annotated[Optional[str], Field(description="分页Token")] = None,
    offset: Annotated[Optional[int], Field(description="偏移量")] = None,
    limit: Annotated[Optional[int], Field(description="分页大小")] = None
) -> str:
    """
    聚合统计VStation事件（可用于统计用户购买退还情况）
    Args:
        group_by: 分组字段
        sort: 排序
        start_time: 起始时间，格式：YYYY-MM-DD HH:mm:ss
        end_time: 结束时间，格式：YYYY-MM-DD HH:mm:ss
        task_name: 任务类型列表，可选值：
            实例创建：instance_launch
            实例销毁：instance_terminate
            实例关机：instance_power_off
            实例开机：instance_power_on
        pool: 资源池列表
        app_id: 客户APPID列表
        uin: UIN列表
        success: 是否成功
        region: 地域列表
        zone: 可用区列表
        zone_id: 可用区ID列表
        cvm_pay_mode: 支付类型列表
        eks_flag: EKS标记
        error_code: 错误码
        error_message: 错误信息
        instance_id: 实例ID列表
        instance_type: 实例类型列表
        instance_family: 实例族列表
        not_instance_family: 排除的实例族列表
        main_zone: 是否主力园区
        inner_user: 是否内部客户
        customhouse: 境内外列表，可选值：境内/境外
        next_token: 分页Token
        offset: 偏移量
        limit: 分页大小
    Returns:
        str: 聚合统计结果的JSON字符串
    """
    params = {
        "groupBy": [
            "appId", 
            "name", 
            "zoneName", 
            "region", 
            "regionName", 
            "taskName", 
            "zone", 
            "vmInstanceTypeFamily", 
            "vmInstanceType"
        ],
        "sort": [{
            "property": "relativeCount", 
            "direction": "DESC"
            }]
    }
    if group_by is not None:
        params["groupBy"] = group_by
    if sort is not None:
        params["sort"] = sort
    if start_time is not None:
        params["startTime"] = start_time
    if end_time is not None:
        params["endTime"] = end_time
    if task_name is not None:
        params["taskName"] = task_name
    if pool is not None:
        params["pool"] = pool
    if app_id is not None:
        params["appId"] = app_id
    if uin is not None:
        params["uin"] = uin
    if success is not None:
        params["success"] = success
    if region is not None:
        params["region"] = region
    if zone is not None:
        params["zone"] = zone
    if zone_id is not None:
        params["zoneId"] = zone_id
    if cvm_pay_mode is not None:
        params["cvmPayMode"] = cvm_pay_mode
    if eks_flag is not None:
        params["eksFlag"] = eks_flag
    if error_code is not None:
        params["errorCode"] = error_code
    if error_message is not None:
        params["errorMessage"] = error_message
    if instance_id is not None:
        params["instanceId"] = instance_id
    if instance_type is not None:
        params["instanceType"] = instance_type
    if instance_family is not None:
        params["instanceFamily"] = instance_family
    if not_instance_family is not None:
        params["notInstanceFamily"] = not_instance_family
    if main_zone is not None:
        params["mainZone"] = main_zone
    if inner_user is not None:
        params["innerUser"] = inner_user
    if customhouse is not None:
        params["customhouse"] = customhouse
    if next_token is not None:
        params["nextToken"] = next_token
    if offset is not None:
        params["offset"] = offset
    if limit is not None:
        params["limit"] = limit
    return _call_api("/insight/vstation-event/aggregate", params)

@mcp.tool(description="聚合统计VStation事件可聚合字段")
def vstation_event_aggregate_metrics() -> str:
    """
    查询VStation事件可聚合字段
    Returns:
        str: 可聚合字段的JSON字符串
    """
    return _call_api("/insight/vstation-event/aggregate/metrics", {}) 