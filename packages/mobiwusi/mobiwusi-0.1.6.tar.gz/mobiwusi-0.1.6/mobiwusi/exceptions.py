"""
异常定义模块
"""

class MobiWuSiError(Exception):
    """MobiWuSi 基础异常类"""
    pass


class UploadError(MobiWuSiError):
    """上传过程中的异常"""
    pass


class SyncError(MobiWuSiError):
    """同步过程中的异常"""
    pass


class AuthError(MobiWuSiError):
    """认证过程中的异常"""
    pass