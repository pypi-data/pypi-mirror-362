"""
名称:绿旗编程AI课程SDK

说明:这个模块提供了与绿旗编程AI服务交互的接口。
现在支持插件化架构，添加新功能更简单！

新的目录结构：
- core/: 核心功能（基础类、配置、插件系统等）
- plugins/: AI功能插件（所有ai_xxx.py文件）
- cli/: 命令行接口
"""

# 导入核心功能
from .core import (
    BaseAI, Config, registry, ai_plugin, 
    DynamicLqcodeAI, LqcodeAI, lq
)

# 自动导入所有插件（这会触发插件注册）
from . import plugins  # 这会自动导入所有插件

# 插件类通过插件系统自动管理，不需要手动导出

# 导入CLI功能
from .cli import DynamicCLI, cli, main as cli_main

# 向后兼容类已移除，使用新的动态AI系统

# 导出类和实例
__all__ = [
    # 核心功能
    'BaseAI',
    'Config',
    'ai_plugin',
    'registry',
    'lq',
    'LqcodeAI',
    'DynamicLqcodeAI',
    
    # CLI功能
    'DynamicCLI',
    'cli',
    'cli_main',
] 