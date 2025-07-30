"""
云霄服务 tools_insight 工具单元测试
"""
import os
import json
import unittest
from src.mcp_server_yunxiao.tools_insight import (
    describe_purchase_failed_alarms,
    describe_vstation_events,
    describe_user_activity_top_decrease,
    describe_user_activity_top_increase,
    describe_user_activity_top_active
)

class TestToolsInsight(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        os.environ["YUNXIAO_API_URL"] = "http://api.yunxiao.vstation.woa.com"
        os.environ["YUNXIAO_SECRET_ID"] = "ak.xiaoliu"
        os.environ["YUNXIAO_SECRET_KEY"] = "sk.63fc6b1a23e3ab55c3ced2d4"

    def test_describe_purchase_failed_alarms(self):
        result = describe_purchase_failed_alarms()
        self.assertIsInstance(result, str)
        try:
            data = json.loads(result)
            self.assertIsInstance(data, dict)
        except Exception:
            self.assertTrue(result.startswith("{"))

    def test_describe_vstation_events(self):
        result = describe_vstation_events()
        self.assertIsInstance(result, str)
        try:
            data = json.loads(result)
            self.assertIsInstance(data, dict)
        except Exception:
            self.assertTrue(result.startswith("{"))

    def test_describe_user_activity_top_decrease(self):
        result = describe_user_activity_top_decrease()
        self.assertIsInstance(result, str)
        try:
            data = json.loads(result)
            self.assertIsInstance(data, dict)
        except Exception:
            self.assertTrue(result.startswith("{"))

    def test_describe_user_activity_top_increase(self):
        result = describe_user_activity_top_increase()
        self.assertIsInstance(result, str)
        try:
            data = json.loads(result)
            self.assertIsInstance(data, dict)
        except Exception:
            self.assertTrue(result.startswith("{"))

    def test_describe_user_activity_top_active(self):
        result = describe_user_activity_top_active()
        self.assertIsInstance(result, str)
        try:
            data = json.loads(result)
            self.assertIsInstance(data, dict)
        except Exception:
            self.assertTrue(result.startswith("{"))

if __name__ == "__main__":
    unittest.main() 