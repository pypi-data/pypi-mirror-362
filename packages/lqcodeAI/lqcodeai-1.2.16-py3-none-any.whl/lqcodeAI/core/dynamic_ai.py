"""
动态AI类 - 自动加载和管理所有AI插件
"""
from typing import Any, Dict, Optional
from .config import Config
from .plugin_registry import registry

class DynamicLqcodeAI:
    """动态AI功能接口类 - 自动发现和加载所有插件"""
    
    def __init__(self, config: Optional[Config] = None):
        self.config = config or Config()
        # 自动发现插件
        registry.auto_discover_plugins()
        
    @property
    def registry(self):
        """获取插件注册表"""
        return registry
        
    def __getattr__(self, name: str) -> Any:
        """动态方法调用 - 自动路由到对应的插件"""
        if name.startswith('ai_'):
            plugin_name = name[3:]  # 去掉 'ai_' 前缀
            if registry.get_plugin(plugin_name):
                def plugin_method(password: str, *args, **kwargs):
                    return registry.call_plugin(plugin_name, password, *args, **kwargs)
                return plugin_method
        
        raise AttributeError(f"'{self.__class__.__name__}' 对象没有属性 '{name}'")
    
    def get_available_functions(self) -> Dict[str, str]:
        """获取所有可用的AI功能"""
        plugins = registry.get_all_plugins()
        return {f"ai_{name}": info['description'] for name, info in plugins.items()}
    
    def help(self, function_name: Optional[str] = None) -> str:
        """获取帮助信息"""
        if function_name is None:
            # 显示所有功能
            functions = self.get_available_functions()
            help_text = "可用的AI功能：\n"
            for func_name, description in functions.items():
                help_text += f"  - {func_name}: {description}\n"
            return help_text
        
        # 显示特定功能的帮助
        if function_name.startswith('ai_'):
            plugin_name = function_name[3:]
            plugin_info = registry.get_plugin(plugin_name)
            if plugin_info:
                return f"{function_name}: {plugin_info['description']}"
        
        return f"未找到功能: {function_name}"
    
    def call_function(self, function_name: str, password: str, *args, **kwargs) -> Any:
        """通用函数调用接口"""
        if function_name.startswith('ai_'):
            plugin_name = function_name[3:]
            return registry.call_plugin(plugin_name, password, *args, **kwargs)
        
        raise ValueError(f"未知功能: {function_name}")

# 创建单例实例
lq = DynamicLqcodeAI()

# 为了向后兼容，也导出类
LqcodeAI = DynamicLqcodeAI 