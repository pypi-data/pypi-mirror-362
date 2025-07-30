"""
云霄服务 tools_data360 工具单元测试
"""
import os
import json
import unittest
from src.mcp_server_yunxiao.tools_data360 import (
    query_quota,
    query_instance_families,
    get_instance_count,
    query_instances,
    get_instance_details,
    get_user_owned_grid,
    get_user_owned_instances,
    get_customer_account_info
)

class TestToolsData360(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        os.environ["YUNXIAO_API_URL"] = "http://api.yunxiao.vstation.woa.com"
        os.environ["YUNXIAO_SECRET_ID"] = "ak.xiaoliu"
        os.environ["YUNXIAO_SECRET_KEY"] = "sk.63fc6b1a23e3ab55c3ced2d4"

    def test_query_quota(self):
        result = query_quota(region="ap-guangzhou")
        data = json.loads(result)
        self.assertIsInstance(data, dict)

    def test_query_instance_families(self):
        result = query_instance_families()
        data = json.loads(result)
        self.assertIsInstance(data, dict)

    def test_get_instance_count(self):
        result = get_instance_count(region="ap-guangzhou")
        data = json.loads(result)
        self.assertIsInstance(data, dict)

    def test_query_instances(self):
        result = query_instances(region="ap-guangzhou")
        data = json.loads(result)
        self.assertIsInstance(data, dict)

    def test_get_instance_details(self):
        result = get_instance_details(region="ap-guangzhou", instance_id=["ins-123456"])
        data = json.loads(result)
        self.assertIsInstance(data, dict)

    def test_get_user_owned_grid(self):
        result = get_user_owned_grid(app_id=251000022)
        data = json.loads(result)
        self.assertIsInstance(data, dict)

    def test_get_user_owned_instances(self):
        result = get_user_owned_instances(app_id=251000022)
        data = json.loads(result)
        self.assertIsInstance(data, dict)

    def test_get_customer_account_info(self):
        result = get_customer_account_info(customer_ids=["251000022"])
        data = json.loads(result)
        self.assertIsInstance(data, dict)

if __name__ == "__main__":
    unittest.main() 