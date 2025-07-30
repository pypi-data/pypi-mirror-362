"""
文件上传模块 - 提供文件上传功能
"""
from typing import Optional, Dict, Any
from .auth import get_api_key, get_target_url
from .exceptions import UploadError
import requests


class FileUploader:
    """文件上传器类"""
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """
        初始化上传器
        
        Args:
            config (Dict[str, Any], optional): 上传配置参数
        """
        self.config = config or {}
    
    def upload(self, file_path: str, destination: Optional[str] = None, 
               api_key: Optional[str] = None, **kwargs) -> Dict[str, Any]:
        """
        上传文件
        
        Args:
            file_path (str): 要上传的文件路径
            destination (str, optional): 目标位置
            api_key (str, optional): API密钥
            **kwargs: 其他上传参数
            
        Returns:
            Dict[str, Any]: 上传结果信息
            
        Raises:
            UploadError: 上传失败时
        """
        # 获取API密钥
        key = get_api_key(api_key)
        # 检查目标URL
        target_url = get_target_url(kwargs.get("target_url"))
        
        try:
            with open(file_path, "rb") as f:
                files = {"file": f}
                headers = {"Authorization": f"Bearer {key}"}
                data = {}
                if destination:
                    data["destination"] = destination
                # 发送POST请求，form-data参数名为file
                response = requests.post(target_url+'/p1.syncData/upload', files=files, data=data, headers=headers)
                response.raise_for_status()
                result = response.json()
                return result
        except Exception as e:
            raise UploadError(f"文件上传失败: {str(e)}")


def upload_file(file_path: str, destination: Optional[str] = None, 
                api_key: Optional[str] = None, **kwargs) -> Dict[str, Any]:
    """
    上传文件的便捷函数
    
    Args:
        file_path (str): 要上传的文件路径
        destination (str, optional): 目标位置
        api_key (str, optional): API密钥
        **kwargs: 其他上传参数
        
    Returns:
        Dict[str, Any]: 上传结果信息
    """
    uploader = FileUploader()
    return uploader.upload(file_path, destination, api_key, **kwargs)