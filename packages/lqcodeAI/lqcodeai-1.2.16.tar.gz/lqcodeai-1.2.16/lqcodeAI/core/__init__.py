"""
核心功能模块

包含项目的基础功能组件：
- 基础AI类
- 配置管理
- 插件注册系统
- 动态AI类
"""

from .base import BaseAI
from .config import Config
from .plugin_registry import registry, ai_plugin, PluginRegistry
from .dynamic_ai import DynamicLqcodeAI, lq, LqcodeAI

__all__ = [
    # 基础类
    'BaseAI',
    'Config',
    
    # 插件系统
    'registry',
    'ai_plugin', 
    'PluginRegistry',
    
    # 动态AI
    'DynamicLqcodeAI',
    'LqcodeAI',
    'lq',
] 