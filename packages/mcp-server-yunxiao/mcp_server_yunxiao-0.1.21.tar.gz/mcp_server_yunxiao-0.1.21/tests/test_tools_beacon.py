"""
云霄服务 tools_beacon 工具单元测试
"""
import os
import json
import unittest
from src.mcp_server_yunxiao.tools_beacon import (
    describe_inventory,
    describe_stock_metrics,
    describe_cvm_type_config
)

class TestToolsBeacon(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        os.environ["YUNXIAO_API_URL"] = "http://api.yunxiao.vstation.woa.com"
        os.environ["YUNXIAO_SECRET_ID"] = "ak.xiaoliu"
        os.environ["YUNXIAO_SECRET_KEY"] = "sk.63fc6b1a23e3ab55c3ced2d4"

    def test_describe_inventory(self):
        result = describe_inventory(region="ap-guangzhou")
        data = json.loads(result)
        self.assertIsInstance(data, dict)
        self.assertIn("data", data)
        self.assertIn("totalCount", data)

    def test_describe_stock_metrics(self):
        result = describe_stock_metrics(region=["ap-guangzhou"])
        self.assertIsInstance(result, str)
        try:
            data = json.loads(result)
            self.assertIsInstance(data, dict)
        except Exception:
            self.assertTrue(result.startswith("{"))

    def test_describe_cvm_type_config(self):
        result = describe_cvm_type_config(region=["ap-guangzhou"])
        self.assertIsInstance(result, str)
        try:
            data = json.loads(result)
            self.assertIsInstance(data, dict)
        except Exception:
            self.assertTrue(result.startswith("{"))

if __name__ == "__main__":
    unittest.main() 