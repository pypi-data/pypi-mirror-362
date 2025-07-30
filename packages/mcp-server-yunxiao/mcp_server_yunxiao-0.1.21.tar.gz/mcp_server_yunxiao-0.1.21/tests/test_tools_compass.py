"""
云霄服务 tools_compass 工具单元测试
"""
import os
import json
import unittest
from src.mcp_server_yunxiao.tools_compass import (
    describe_sale_policies,
    describe_operation_metrics,
    describe_buy_flow_promise_info,
    describe_stock_metrics_history
)

class TestToolsCompass(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        os.environ["YUNXIAO_API_URL"] = "http://api.yunxiao.vstation.woa.com"
        os.environ["YUNXIAO_SECRET_ID"] = "ak.xiaoliu"
        os.environ["YUNXIAO_SECRET_KEY"] = "sk.63fc6b1a23e3ab55c3ced2d4"

    def test_describe_sale_policies(self):
        result = describe_sale_policies()
        self.assertIsInstance(result, str)
        try:
            data = json.loads(result)
            self.assertIsInstance(data, dict)
        except Exception:
            self.assertTrue(result.startswith("{"))

    def test_describe_operation_metrics(self):
        result = describe_operation_metrics()
        self.assertIsInstance(result, str)
        try:
            data = json.loads(result)
            self.assertIsInstance(data, dict)
        except Exception:
            self.assertTrue(result.startswith("{"))

    def test_describe_buy_flow_promise_info(self):
        result = describe_buy_flow_promise_info()
        self.assertIsInstance(result, str)
        try:
            data = json.loads(result)
            self.assertIsInstance(data, dict)
        except Exception:
            self.assertTrue(result.startswith("{"))

    def test_describe_stock_metrics_history(self):
        result = describe_stock_metrics_history()
        self.assertIsInstance(result, str)
        try:
            data = json.loads(result)
            self.assertIsInstance(data, dict)
        except Exception:
            self.assertTrue(result.startswith("{"))

if __name__ == "__main__":
    unittest.main() 