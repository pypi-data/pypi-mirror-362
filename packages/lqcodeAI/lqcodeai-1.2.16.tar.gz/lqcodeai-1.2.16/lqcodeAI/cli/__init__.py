"""
命令行接口模块

包含动态CLI系统，自动为所有插件生成命令行接口
"""

from .dynamic_cli import DynamicCLI, cli, main

__all__ = [
    'DynamicCLI',
    'cli', 
    'main',
] 