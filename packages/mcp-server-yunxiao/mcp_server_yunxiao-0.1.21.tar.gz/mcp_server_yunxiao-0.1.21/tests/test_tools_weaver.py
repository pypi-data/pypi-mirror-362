"""
云霄服务 tools_weaver 工具单元测试
"""
import os
import json
import unittest
from datetime import datetime, timedelta
from src.mcp_server_yunxiao.tools_weaver import (
    query_vstation_task_message,
    query_vstation_error_codes,
    query_host_task_list,
    query_host_task_detail,
    get_host_stat,
    get_vm_xml,
    query_vm_pico,
    health_check
)


class TestToolsWeaver(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # 设置测试环境变量
        os.environ["YUNXIAO_API_URL"] = "http://api.yunxiao.vstation.woa.com"
        os.environ["YUNXIAO_SECRET_ID"] = "ak.xiaoliu"
        os.environ["YUNXIAO_SECRET_KEY"] = "sk.63fc6b1a23e3ab55c3ced2d4"

        # 测试用的宿主机IP
        cls.test_ip = "11.26.140.21"
        # 测试用的虚拟机UUID
        cls.test_uuid = "12345678-1234-5678-1234-567812345678"
        # 测试用的任务ID
        cls.test_task_id = "1234567890"
        # 测试用的日期字符串
        cls.test_date = datetime.now().strftime("%Y%m%d")
        # 测试用的时间字符串
        cls.test_time = "12:00:00"

    def test_query_vstation_task_message(self):
        """测试查询任务列表接口"""
        result = query_vstation_task_message(
            region="ap-guangzhou",
            task_id=[self.test_task_id]
        )
        self._assert_valid_json(result)

    def test_query_vstation_error_codes(self):
        """测试查询错误码接口"""
        result = query_vstation_error_codes(region="ap-guangzhou")
        self._assert_valid_json(result)

    def test_query_host_task_list(self):
        """测试查询宿主机任务接口"""
        result = query_host_task_list(
            region="ap-guangzhou",
            host=self.test_ip,
            vs_task_id=123456
        )
        self._assert_valid_json(result)

    def test_query_host_task_detail(self):
        """测试查询宿主机任务日志接口"""
        result = query_host_task_detail(
            region="ap-guangzhou",
            host_ip=self.test_ip,
            host_task_id=self.test_task_id
        )
        self._assert_valid_json(result)

    def test_get_host_stat(self):
        """测试获取宿主机状态接口"""
        result = get_host_stat(ip=self.test_ip)
        self._assert_valid_json(result)

    def test_get_vm_xml(self):
        """测试获取虚拟机XML配置接口"""
        result = get_vm_xml(
            ip=self.test_ip,
            uuid=self.test_uuid
        )
        self.assertIsInstance(result, str)
        self.assertTrue(result.startswith("<") or result.startswith("{"))

    def test_query_vm_pico(self):
        """测试查询虚拟机Pico信息接口"""
        result = query_vm_pico(
            ip=self.test_ip,
            uuid=self.test_uuid,
            date_str=self.test_date,
            time_str=self.test_time
        )
        self._assert_valid_json(result)

    def test_health_check(self):
        """测试健康检查接口"""
        result = health_check(ip=self.test_ip)
        self._assert_valid_json(result)

    def _assert_valid_json(self, result):
        """辅助方法，验证返回结果是否为有效JSON"""
        self.assertIsInstance(result, str)
        try:
            data = json.loads(result)
            self.assertIsInstance(data, (dict, list))
        except Exception:
            self.assertTrue(result.startswith("{") or result.startswith("["))


if __name__ == "__main__":
    unittest.main()
