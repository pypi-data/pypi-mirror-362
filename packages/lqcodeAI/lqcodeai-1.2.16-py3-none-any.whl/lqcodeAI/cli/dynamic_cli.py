"""
动态CLI系统 - 自动生成命令行接口
"""
import argparse
from typing import Dict, Any
from ..core.plugin_registry import registry
from ..core.dynamic_ai import lq

class DynamicCLI:
    """动态命令行接口"""
    
    def __init__(self):
        self.password = 'lqcode'  # 默认密码
    
    def create_parser(self) -> argparse.ArgumentParser:
        """动态创建命令行解析器"""
        parser = argparse.ArgumentParser(description='绿旗编程AI功能命令行工具')
        subparsers = parser.add_subparsers(dest='command', help='可用命令')
        
        # 添加帮助命令
        subparsers.add_parser('list', help='列出所有可用功能')
        
        # 自动发现插件并创建子命令
        plugins = registry.get_all_plugins()
        for plugin_name, plugin_info in plugins.items():
            self._add_plugin_parser(subparsers, plugin_name, plugin_info)
        
        return parser
    
    def _add_plugin_parser(self, subparsers, plugin_name: str, plugin_info: Dict[str, Any]):
        """为插件添加子命令"""
        plugin_parser = subparsers.add_parser(
            plugin_name, 
            help=plugin_info['description']
        )
        
        # 添加CLI参数
        cli_args = plugin_info.get('cli_args', [])
        for arg_info in cli_args:
            if isinstance(arg_info, dict):
                arg_name = arg_info['name']
                arg_help = arg_info.get('help', f'{arg_name}参数')
                
                if arg_info.get('required', False):
                    plugin_parser.add_argument(arg_name, help=arg_help)
                else:
                    default_value = arg_info.get('default', '')
                    plugin_parser.add_argument(
                        f'--{arg_name}', 
                        default=default_value,
                        help=f'{arg_help} (默认: {default_value})'
                    )
    
    def run(self, args=None):
        """运行CLI"""
        parser = self.create_parser()
        parsed_args = parser.parse_args(args)
        
        if parsed_args.command == 'list':
            self._list_functions()
            return
        
        if not parsed_args.command:
            parser.print_help()
            return
        
        # 执行插件命令
        self._execute_plugin_command(parsed_args)
    
    def _list_functions(self):
        """列出所有可用功能"""
        print("可用的AI功能：")
        plugins = registry.get_all_plugins()
        for plugin_name, plugin_info in plugins.items():
            print(f"  {plugin_name}: {plugin_info['description']}")
    
    def _execute_plugin_command(self, args):
        """执行插件命令"""
        plugin_name = args.command
        plugin_info = registry.get_plugin(plugin_name)
        
        if not plugin_info:
            print(f"未知命令: {plugin_name}")
            return
        
        try:
            # 准备参数
            kwargs = {}
            cli_args = plugin_info.get('cli_args', [])
            
            for arg_info in cli_args:
                if isinstance(arg_info, dict):
                    arg_name = arg_info['name']
                    if hasattr(args, arg_name):
                        value = getattr(args, arg_name)
                        if value:  # 只传递非空值
                            kwargs[arg_name] = value
            
            # 调用插件
            result = registry.call_plugin(plugin_name, self.password, **kwargs)
            
            # 格式化输出
            self._format_output(plugin_name, result)
            
        except Exception as e:
            print(f"执行 {plugin_name} 时发生错误: {str(e)}")
    
    def _format_output(self, plugin_name: str, result: Any):
        """格式化输出结果"""
        if isinstance(result, dict):
            for key, value in result.items():
                if key == 'error':
                    print(f"错误: {value}")
                else:
                    print(f"{key}: {value}")
                    if key != list(result.keys())[-1]:  # 不是最后一个键
                        print()
        else:
            print(f"结果: {result}")

# 创建CLI实例
cli = DynamicCLI()

def main():
    """CLI入口点"""
    cli.run() 