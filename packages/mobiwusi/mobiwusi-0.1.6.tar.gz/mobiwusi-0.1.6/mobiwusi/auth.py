"""
认证模块 - 提供简单的API密钥管理功能
"""
import os
from typing import Optional
from .exceptions import AuthError


class APIKeyManager:
    """API密钥管理器"""
    
    _instance = None
    _api_key = None
    _target_url = None
    
    def __new__(cls):
        """单例模式实现"""
        if cls._instance is None:
            cls._instance = super(APIKeyManager, cls).__new__(cls)
        return cls._instance
    
    @classmethod
    def set_api_key(cls, api_key: str) -> None:
        """
        设置API密钥
        
        Args:
            api_key (str): API密钥
        """
        cls._api_key = api_key
    
    @classmethod
    def get_api_key(cls) -> Optional[str]:
        """
        获取API密钥，优先使用已设置的密钥，其次尝试从环境变量获取
        
        Returns:
            Optional[str]: API密钥，如果未设置则返回None
        """
        if cls._api_key:
            return cls._api_key
        
        # 尝试从环境变量获取
        return os.environ.get("MOBIWUSI_API_KEY")
    
    @classmethod
    def clear_api_key(cls) -> None:
        """清除已设置的API密钥"""
        cls._api_key = None

    @classmethod
    def set_target_url(cls, url: str) -> None:
        """
        设置目标URL
        """
        cls._target_url = url

    @classmethod
    def get_target_url(cls) -> Optional[str]:
        """
        获取目标URL，优先使用已设置的URL，其次尝试从环境变量获取
        """
        if cls._target_url:
            return cls._target_url
        return os.environ.get("MOBIWUSI_TARGET_URL")

    @classmethod
    def clear_target_url(cls) -> None:
        """
        清除已设置的目标URL
        """
        cls._target_url = None

def get_api_key(api_key: Optional[str] = None) -> str:
    """
    获取API密钥的便捷函数
    
    Args:
        api_key (str, optional): 直接传入的API密钥
        
    Returns:
        str: API密钥
        
    Raises:
        AuthError: 当无法获取API密钥时
    """
    # 优先使用传入的密钥
    if api_key:
        return api_key
    
    # 其次使用已设置的密钥或环境变量
    key = APIKeyManager.get_api_key()
    if not key:
        raise AuthError("未提供API密钥，请通过参数传入、使用set_api_key()方法设置或设置MOBIWUSI_API_KEY环境变量")
    
    return key

def get_target_url(url: Optional[str] = None) -> str:
    """
    获取目标URL的便捷函数
    """
    if url:
        return url
    target_url = APIKeyManager.get_target_url()
    if not target_url:
        raise AuthError("未提供目标URL，请通过参数传入、使用set_target_url()方法设置或设置MOBIWUSI_TARGET_URL环境变量")
    return target_url