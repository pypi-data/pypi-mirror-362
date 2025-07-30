# 云霄服务 SDK

云霄（YunXiao）是腾讯云 CVM 的内部运维运营平台，提供了一系列强大的管理和运营功能。本 SDK 封装了云霄平台的 API 接口，方便开发者进行集成和使用。

## 功能特性

- 售卖策略查询：获取实例的售卖推荐数据
- 库存管理：查询各区域、机型的库存情况
- 用户管理：查询用户归属和账号信息
- 配额管理：查询和管理资源配额
- 实例管理：查询实例列表、详情和统计信息
- 实例族管理：查询可用的实例族信息

## 环境要求

- Python 3.6+
- 需要配置以下环境变量：
  - `YUNXIAO_API_URL`: 云霄 API 服务地址
  - `YUNXIAO_SECRET_ID`: 访问密钥 ID
  - `YUNXIAO_SECRET_KEY`: 访问密钥 Key

## 安装

```bash
pip install mcp-server-yunxiao
```

## API 说明

### 售卖策略相关
- `describe_sale_policies(**kwargs)`: 查询售卖推荐数据
  - 参数：
    - customhouse: List[str] - 境内外列表
    - region_alias: List[str] - 地域别名列表
    - region: List[str] - 地域列表
    - zone_id: List[int] - 可用区ID列表
    - zone: List[str] - 可用区列表
    - instance_family: List[str] - 实例族列表
    - instance_category: List[str] - 实例分组列表，可选值：CVM/GPU/FPGA/BARE_METAL
    - instance_family_state: List[str] - 实例族状态列表
    - instance_family_supply_state: List[str] - 实例族供货状态列表，可选值：LTS/EOL
    - zone_state: List[str] - 可用区状态列表
    - stock_state: List[str] - 库存状态列表
    - sales_policy: List[int] - 售卖建议列表
    - page_number: int - 页码（必填，默认1）
    - page_size: int - 每页数量（必填，默认20，最大100）
  - 返回：包含售卖策略和库存信息的JSON字符串

### 库存相关
- `describe_inventory(region: str)`: 查询指定地域的库存数据
  - 参数：
    - region: 地域名称，如 ap-guangzhou
  - 返回：包含可用区、实例族、实例类型、库存等信息

### 用户相关
- `get_user_owned_grid(app_id: int)`: 获取用户归属预扣统计
  - 参数：
    - app_id: 用户 AppID
    
- `get_customer_account_info(customer_ids: List[str])`: 获取客户账号信息
  - 参数：
    - customer_ids: 客户 ID 列表

### 配额相关
- `query_quota(region: str)`: 查询配额信息
  - 参数：
    - region: 地域名称

### 实例相关
- `query_instances(region: str)`: 查询实例列表
  - 参数：
    - region: 地域名称

- `get_instance_details(region: str)`: 获取实例详细信息
  - 参数：
    - region: 地域名称

- `get_instance_count(region: str)`: 获取实例数量统计
  - 参数：
    - region: 地域名称

### 实例族相关
- `query_instance_families()`: 查询实例族信息

## 使用示例

```python
from mcp_server_yunxiao.tool_yunxiao import describe_inventory, query_instances

# 查询广州地域的库存情况
inventory = describe_inventory(region="ap-guangzhou")
print(json.loads(inventory))

# 查询实例列表
instances = query_instances(region="ap-guangzhou")
print(json.loads(instances))
```

## 测试

运行单元测试：

```bash
cd yunxiao
python -m pytest tests/test_tool_yunxiao.py -v
```

## 注意事项

1. 请确保在使用前正确配置环境变量
2. API 返回的数据均为 JSON 格式字符串，需要使用 `json.loads()` 解析
3. 在生产环境中使用时，请注意访问频率限制
4. 部分 API 可能需要特定的访问权限，请确保有相应的权限配置

### Usage in Claude Desktop
Add the following configuration to claude_desktop_config.json:

```json
{
  "mcpServers": {
    "tencent-cvm": {
      "command": "uv",
      "args": [
        "run",
        "mcp-server-yunxiao"
      ],
      "env": {
        "YUNXIAO_SECRET_ID": "YOUR_SECRET_ID_HERE",
        "YUNXIAO_SECRET_KEY": "YOUR_SECRET_KEY_HERE"
      }
    }
  }
}
```