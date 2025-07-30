import json
import os
import time
import random
import hashlib
import logging
import requests
from typing import Any, Dict, Optional

logger = logging.getLogger(__name__)

class YunxiaoClient:
    """云霄服务客户端类"""
    def __init__(self):
        """初始化客户端"""
        self.base_url = os.getenv("YUNXIAO_API_URL", "http://api.yunxiao.vstation.woa.com")
        self.secret_id = os.getenv("YUNXIAO_SECRET_ID")
        self.secret_key = os.getenv("YUNXIAO_SECRET_KEY")
        if not self.secret_id or not self.secret_key:
            raise ValueError("YUNXIAO_SECRET_ID and YUNXIAO_SECRET_KEY must be set in environment variables")
        self.session = requests.Session()
        self.session.headers.update({'Content-Type': 'application/json'})

    def _generate_headers(self) -> Dict[str, str]:
        rand = random.randint(1, 999999)
        ts = int(time.time())
        sig = hashlib.sha1(f"{ts}{rand}{self.secret_key}".encode()).hexdigest()
        return {
            'random': str(rand),
            'appkey': self.secret_id,
            'timestamp': str(ts),
            'signature': sig
        }

    def post(self, path: str, data: Any) -> Dict[str, Any]:
        url = f"{self.base_url}{path}"
        headers = self._generate_headers()
        logger.debug(f"POST {url} with headers: {headers} and data: {data}")
        try:
            response = self.session.post(url, json=data, headers=headers)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"Request failed: {e}")
            raise

_client: Optional[YunxiaoClient] = None

def get_yunxiao_client() -> YunxiaoClient:
    """获取云霄服务客户端实例"""
    global _client
    if _client is None:
        _client = YunxiaoClient()
    return _client

def _call_api(path: str, params: dict) -> str:
    """调用云霄API并返回JSON格式的响应"""
    print(f"调用API: {path}, 参数: {params}")
    response = get_yunxiao_client().post(path, params)
    return json.dumps(response, ensure_ascii=False)


def _call_api_raw(path: str, params: dict) -> dict:
    """调用云霄API并返回JSON格式的响应"""
    print(f"调用API: {path}, 参数: {params}")
    return get_yunxiao_client().post(path, params)