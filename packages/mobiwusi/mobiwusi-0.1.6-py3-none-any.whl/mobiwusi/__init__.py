"""
MobiWuSi - 移动文件上传与同步工具包
"""

__version__ = "0.1.0"

from .uploader import upload_file, FileUploader
from .synchronizer import sync_record
from .auth import APIKeyManager

# 导出便捷函数
set_api_key = APIKeyManager.set_api_key
clear_api_key = APIKeyManager.clear_api_key
set_target_url = APIKeyManager.set_target_url
clear_target_url = APIKeyManager.clear_target_url

__all__ = [
    "upload_file",
    "sync_record", 
    "set_api_key", 
    "clear_api_key",
    "set_target_url",
    "clear_target_url",
    "FileUploader"
]