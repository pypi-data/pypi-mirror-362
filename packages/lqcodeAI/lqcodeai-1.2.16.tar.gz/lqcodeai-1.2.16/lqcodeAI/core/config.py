"""
SDK配置文件
"""
from dataclasses import dataclass
from typing import Optional

@dataclass
class Config:
    """SDK配置类"""
    # API配置
    base_url: str = 'http://api.lqcode.fun/open/lqedu/coze/getAIToken'
    workflow_id: str = '7478947190259580939'
    
    # 重试配置
    max_retries: int = 3
    base_delay: int = 2
    
    # Token配置
    token_expiry_hours: int = 1
    cache_size: int = 100
    
    # 配置键列表
    CONFIG_KEYS = [
        'base_url',
        'workflow_id',
        'max_retries',
        'base_delay',
        'token_expiry_hours',
        'cache_size'
    ]
    
    @classmethod
    def from_dict(cls, config_dict: dict) -> 'Config':
        """从字典创建配置实例"""
        return cls(**{k: v for k, v in config_dict.items() if k in cls.CONFIG_KEYS})
    
    def to_dict(self) -> dict:
        """将配置转换为字典"""
        return {k: getattr(self, k) for k in self.CONFIG_KEYS}
    
    def validate(self) -> bool:
        """验证配置是否有效"""
        if not self.base_url:
            print("错误: base_url 未设置")
            return False
        if not self.workflow_id:
            print("错误: workflow_id 未设置")
            return False
        return True 