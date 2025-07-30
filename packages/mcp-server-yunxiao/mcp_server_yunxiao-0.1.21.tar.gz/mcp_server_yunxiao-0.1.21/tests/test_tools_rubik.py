"""
云霄服务 tools_rubik 工具单元测试
"""
import os
import json
import unittest
from src.mcp_server_yunxiao.tools_rubik import (
    describe_reservation_forms,
    describe_grid_by_zone_instance_type
)

class TestToolsRubik(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        os.environ["YUNXIAO_API_URL"] = "http://api.yunxiao.vstation.woa.com"
        os.environ["YUNXIAO_SECRET_ID"] = "ak.xiaoliu"
        os.environ["YUNXIAO_SECRET_KEY"] = "sk.63fc6b1a23e3ab55c3ced2d4"

    def test_describe_reservation_forms(self):
        result = describe_reservation_forms()
        self.assertIsInstance(result, str)
        try:
            data = json.loads(result)
            self.assertIsInstance(data, dict)
        except Exception:
            self.assertTrue(result.startswith("{"))

    def test_describe_grid_by_zone_instance_type(self):
        result = describe_grid_by_zone_instance_type(region="ap-guangzhou")
        self.assertIsInstance(result, str)
        try:
            data = json.loads(result)
            self.assertIsInstance(data, dict)
        except Exception:
            self.assertTrue(result.startswith("{"))

if __name__ == "__main__":
    unittest.main() 