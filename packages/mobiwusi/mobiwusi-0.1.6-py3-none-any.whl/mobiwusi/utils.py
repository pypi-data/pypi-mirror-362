"""
工具函数模块
"""
import json
import time
import base64
import hmac
import hashlib
import secrets
from typing import List, Optional, Dict, Any
def generate_api_key(client_id: str, permissions: List[str], 
                     expiry_days: int = 365, secret_key: Optional[str] = None) -> str:
    """
    生成 API 密钥
    
    Args:
        client_id (str): 客户端 ID
        permissions (List[str]): 权限列表
        expiry_days (int, optional): 过期天数，默认 365 天
        secret_key (str, optional): 用于签名的密钥，如果不提供则生成随机密钥
        
    Returns:
        str: 生成的 API 密钥
    """
    # 计算过期时间
    expiry = int(time.time()) + (expiry_days * 24 * 60 * 60)
    
    # 创建密钥数据
    key_data = {
        'client_id': client_id,
        'permissions': permissions,
        'expiry': expiry
    }
    
    # 将数据转换为 JSON 并编码为 base64
    json_data = json.dumps(key_data)
    encoded_data = base64.b64encode(json_data.encode('utf-8')).decode('utf-8').rstrip('=')
    
    # 使用密钥签名数据
    signing_key = secret_key or secrets.token_hex(32)
    signature = hmac.new(
        signing_key.encode('utf-8'),
        encoded_data.encode('utf-8'),
        hashlib.sha256
    ).hexdigest()
    
    # 组合数据和签名
    api_key = f"{encoded_data}.{signature}"
    
    return api_key