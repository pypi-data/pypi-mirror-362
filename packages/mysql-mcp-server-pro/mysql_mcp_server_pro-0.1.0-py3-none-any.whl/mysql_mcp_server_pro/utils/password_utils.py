import hashlib
import time
from typing import Optional, Tuple

class PasswordUtils:
    """密码加密和验证工具类"""
    
    @staticmethod
    def hash_password(password: str, salt: str, timestamp: str) -> str:
        """
        使用双重哈希加密密码
        
        Args:
            password: 原始密码
            salt: 盐值
            timestamp: 时间戳
            
        Returns:
            str: 加密后的密码
        """
        # 第一次哈希：密码 + 盐
        first_hash = hashlib.sha256((password + salt).encode()).hexdigest()
        # 第二次哈希：第一次哈希结果 + 时间戳
        final_hash = hashlib.sha256((first_hash + timestamp).encode()).hexdigest()
        return final_hash
    
    @staticmethod
    def verify_timestamp(timestamp: str, max_age: int = 300) -> bool:
        """
        验证时间戳是否在有效期内
        
        Args:
            timestamp: 时间戳（毫秒）
            max_age: 最大有效期（秒），默认5分钟
            
        Returns:
            bool: 是否有效
        """
        try:
            ts = int(timestamp) / 1000  # 转换为秒
            current_time = time.time()
            return current_time - ts <= max_age
        except (ValueError, TypeError):
            return False
    
    @staticmethod
    def verify_password(
        stored_password: str,
        input_password: str,
        salt: str,
        timestamp: str
    ) -> bool:
        """
        验证密码是否正确
        
        Args:
            stored_password: 存储的密码哈希
            input_password: 输入的加密后的密码
            salt: 盐值
            timestamp: 时间戳
            
        Returns:
            bool: 密码是否正确
        """
        # 验证输入的加密密码是否与存储的密码匹配
        return input_password == stored_password 