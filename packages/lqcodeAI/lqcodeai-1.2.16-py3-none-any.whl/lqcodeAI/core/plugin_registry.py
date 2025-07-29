"""
插件注册系统 - 让添加新AI功能变得简单
"""
import inspect
from typing import Dict, Any, Optional, Callable, Type
from functools import wraps
from .base import BaseAI

class PluginRegistry:
    """插件注册表，管理所有AI功能插件"""
    
    def __init__(self):
        self._plugins: Dict[str, Dict[str, Any]] = {}
        self._instances: Dict[str, BaseAI] = {}
    
    def register(self, 
                name: str, 
                description: str = "",
                cli_args: Optional[list] = None,
                result_type: Optional[Type] = None):
        """
        装饰器：注册AI功能插件
        
        Args:
            name: 功能名称 (如 'poetry', 'weather')
            description: 功能描述
            cli_args: CLI命令参数配置
            result_type: 返回结果类型
        """
        def decorator(cls: Type[BaseAI]):
            # 检查类是否继承自BaseAI
            if not issubclass(cls, BaseAI):
                raise TypeError(f"{cls.__name__} 必须继承自 BaseAI")
            
            # 自动检测主要方法
            main_method = self._find_main_method(cls, name)
            
            # 注册插件信息
            self._plugins[name] = {
                'class': cls,
                'description': description or f"{name} AI功能",
                'cli_args': cli_args or [],
                'result_type': result_type,
                'main_method': main_method,
                'module': cls.__module__
            }
            
            return cls
        return decorator
    
    def _find_main_method(self, cls: Type[BaseAI], name: str) -> str:
        """自动找到主要的AI方法"""
        # 优先查找 ai_{name} 方法
        method_name = f"ai_{name}"
        if hasattr(cls, method_name):
            return method_name
        
        # 查找其他可能的方法名
        methods = [m for m in dir(cls) if m.startswith('ai_') and not m.startswith('_')]
        if methods:
            return methods[0]
        
        raise ValueError(f"在 {cls.__name__} 中未找到以 'ai_' 开头的方法")
    
    def get_plugin(self, name: str) -> Optional[Dict[str, Any]]:
        """获取插件信息"""
        return self._plugins.get(name)
    
    def get_all_plugins(self) -> Dict[str, Dict[str, Any]]:
        """获取所有插件"""
        return self._plugins.copy()
    
    def create_instance(self, name: str, config=None) -> Optional[BaseAI]:
        """创建插件实例"""
        if name not in self._instances:
            plugin_info = self._plugins.get(name)
            if not plugin_info:
                return None
            
            plugin_class = plugin_info['class']
            self._instances[name] = plugin_class(config)
        
        return self._instances[name]
    
    def call_plugin(self, name: str, password: str, *args, **kwargs) -> Any:
        """调用插件方法"""
        instance = self.create_instance(name)
        if not instance:
            raise ValueError(f"未找到插件: {name}")
        
        plugin_info = self._plugins[name]
        method_name = plugin_info['main_method']
        method = getattr(instance, method_name)
        
        return method(password, *args, **kwargs)
    
    def auto_discover_plugins(self, package_name: str = "lqcodeAI"):
        """自动发现并加载插件 - 完全自动化，无需手动导入"""
        import pkgutil
        import importlib
        import os
        import glob
        
        try:
            # 方法1：使用相对导入（推荐）
            try:
                # 从当前模块的位置推断plugins包的路径
                current_module = __import__(__name__)
                current_package = current_module.__package__
                
                # 构造plugins包的路径
                if current_package and current_package.endswith('.core'):
                    plugins_package = current_package.replace('.core', '.plugins')
                    
                    # 尝试导入plugins包
                    plugins_module = importlib.import_module(plugins_package)
                    
                    # 扫描plugins包中的所有模块
                    for finder, name, ispkg in pkgutil.iter_modules(plugins_module.__path__, plugins_package + "."):
                        if name.startswith(f"{plugins_package}.ai_"):
                            try:
                                importlib.import_module(name)
                                module_short_name = name.split('.')[-1]
                                print(f"✅ 自动加载插件: {module_short_name}")
                            except Exception as e:
                                print(f"⚠️ 加载插件失败 {name}: {e}")
                                continue
                    return
            except Exception as e:
                print(f"⚠️ 相对导入方式失败: {e}")
            
            # 方法2：直接扫描文件系统（备用方案）
            try:
                # 获取当前包的路径
                current_dir = os.path.dirname(os.path.dirname(__file__))  # 从core目录回到lqcodeAI目录
                plugins_dir = os.path.join(current_dir, "plugins")
                
                if os.path.exists(plugins_dir):
                    # 查找所有ai_*.py文件
                    pattern = os.path.join(plugins_dir, "ai_*.py")
                    plugin_files = glob.glob(pattern)
                    
                    for plugin_file in plugin_files:
                        # 获取文件名（不含扩展名）
                        filename = os.path.basename(plugin_file)
                        module_name = filename[:-3]  # 去掉.py扩展名
                        
                        # 尝试多种可能的模块路径
                        possible_paths = [
                            f"{package_name}.lqcodeAI.plugins.{module_name}",
                            f"lqcodeAI.lqcodeAI.plugins.{module_name}",
                            f"lqcodeAI.plugins.{module_name}"
                        ]
                        
                        imported = False
                        for full_module_name in possible_paths:
                            try:
                                importlib.import_module(full_module_name)
                                print(f"✅ 自动加载插件: {module_name}")
                                imported = True
                                break
                            except ImportError:
                                continue
                        
                        if not imported:
                            print(f"⚠️ 加载插件失败 {module_name}: 无法找到模块")
                            
            except Exception as e:
                print(f"⚠️ 文件系统扫描失败: {e}")
                
        except Exception as e:
            print(f"⚠️ 插件自动发现失败: {e}")
            pass

# 全局插件注册表
registry = PluginRegistry()

# 导出装饰器供使用
ai_plugin = registry.register 