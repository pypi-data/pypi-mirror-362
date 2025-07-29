from typing import Any, Dict, TypedDict
from ..core.base import BaseAI
from ..core.plugin_registry import ai_plugin

class WeaponResult(TypedDict):
    """武器生成器结果类型"""
    name: str
    description: str
    attributes: str
    special_effects: str

@ai_plugin(
    name="weapons",
    description="AI武器生成器 - 根据主题和风格生成创意武器",
    cli_args=[
        {"name": "theme", "help": "武器主题", "default": "奇幻"},
        {"name": "style", "help": "武器风格", "default": "近战"}
    ],
    result_type=WeaponResult
)
class WeaponAI(BaseAI):
    """武器生成器AI功能"""
    
    def ai_weapons(self, password: str, theme: str = "奇幻", style: str = "近战") -> WeaponResult:
        """根据主题和风格生成武器
        
        Args:
            password: 访问密码
            theme: 武器主题，如"奇幻"、"科幻"、"武侠"等，默认为"奇幻"
            style: 武器风格，如"近战"、"远程"、"魔法"等，默认为"近战"
            
        Returns:
            WeaponResult: 包含武器名称、描述、属性和特殊效果的字典
            
        Raises:
            ValueError: 当输入参数无效时
        """
        if not password or not isinstance(password, str):
            raise ValueError("password必须是有效的字符串")
        if not theme or not isinstance(theme, str):
            raise ValueError("theme必须是有效的字符串")
        if not style or not isinstance(style, str):
            raise ValueError("style必须是有效的字符串")
            
        parameters = {
            "theme": theme,
            "style": style,
            "choose": "AI_WEAPONS",
        }
        result = self._execute_workflow(password, parameters, max_retries=5)
        if "error" in result:
            return {"name": result["error"], "description": "", "attributes": "", "special_effects": ""}
        return result

    def _parse_output(self, output: Any) -> WeaponResult:
        """解析武器生成器输出
        
        Args:
            output: 工作流返回的输出
            
        Returns:
            WeaponResult: 解析后的结果
        """
        if isinstance(output, dict):
            return {
                "name": output.get('name', ""),
                "description": output.get('description', ""),
                "attributes": output.get('attributes', ""),
                "special_effects": output.get('special_effects', "")
            }
        return {"name": str(output), "description": "", "attributes": "", "special_effects": ""}
