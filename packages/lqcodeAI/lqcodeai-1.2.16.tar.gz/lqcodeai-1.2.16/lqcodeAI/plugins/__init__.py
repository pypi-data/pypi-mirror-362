"""
AI功能插件模块

自动发现和导入所有AI插件 - 无需手动维护导入列表！
"""

import os
import glob
import importlib
from typing import List, Any

def _auto_import_plugins():
    """自动发现并导入所有AI插件"""
    # 获取当前目录
    current_dir = os.path.dirname(__file__)
    
    # 查找所有ai_*.py文件
    pattern = os.path.join(current_dir, "ai_*.py")
    plugin_files = glob.glob(pattern)
    
    imported_classes = []
    all_exports = []
    
    for plugin_file in plugin_files:
        # 获取模块名
        filename = os.path.basename(plugin_file)
        module_name = filename[:-3]  # 去掉.py扩展名
        
        try:
            # 动态导入模块
            module = importlib.import_module(f".{module_name}", package=__name__)
            
            # 查找模块中的AI类（以AI结尾的类）
            for attr_name in dir(module):
                attr = getattr(module, attr_name)
                if (isinstance(attr, type) and 
                    attr_name.endswith('AI') and 
                    attr.__module__ == module.__name__):
                    
                    # 将类添加到当前模块的全局命名空间
                    globals()[attr_name] = attr
                    imported_classes.append(attr)
                    all_exports.append(attr_name)
                    
        except Exception as e:
            pass  # 静默忽略导入失败的插件
    
    return imported_classes, all_exports

# 执行自动导入
_, _all_exports = _auto_import_plugins()

# 动态设置__all__
__all__ = _all_exports 