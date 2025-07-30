"""
同步记录模块 - 提供记录同步功能
"""
from typing import Optional, Dict, Any
from .auth import get_api_key,get_target_url
from .exceptions import SyncError
import requests

# Define coordinate object


class RecordSynchronizer:
    """记录同步器类"""
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        self.config = config or {}

    def sync(self, record_data: Dict[str, Any], target: Optional[str] = None, 
             api_key: Optional[str] = None, **kwargs) -> Dict[str, Any]:
        # 获取API密钥
        key = get_api_key(api_key)
        # 检查目标URL
        target_url = get_target_url(kwargs.get("target_url"))
        try:
            # 直接发送原始数据，不再使用Pydantic模型校验和转换
            headers = {
                "Authorization": f"Bearer {key}",
                "Content-Type": "application/json"
            }
            response = requests.post(
                target_url + "/p1.syncData/data",
                json=record_data,
                headers=headers
            )
            response.raise_for_status()
            result = response.json()
            return result
        except Exception as e:
            raise SyncError(f"记录同步失败: {str(e)}")

def sync_record(record_data: Dict[str, Any], target: Optional[str] = None, 
                api_key: Optional[str] = None, **kwargs) -> Dict[str, Any]:
    synchronizer = RecordSynchronizer()
    return synchronizer.sync(record_data, target, api_key, **kwargs)