from typing import Any, Dict, TypedDict
from ..core.base import BaseAI
from ..core.plugin_registry import ai_plugin

class SnackPropsResult(TypedDict):
    """零食推荐结果类型"""
    recommendations: str
    explanation: str

@ai_plugin(
    name="snackprops",
    description="AI零食推荐器 - 根据喜好推荐合适的零食",
    cli_args=[
        {"name": "preferences", "help": "零食偏好", "default": "甜食"}
    ],
    result_type=SnackPropsResult
)
class SnackPropsAI(BaseAI):
    """零食推荐AI功能"""
    
    def ai_snackprops(self, password: str, preferences: str = "甜食") -> SnackPropsResult:
        """根据用户偏好推荐零食
        
        Args:
            password: 访问密码
            preferences: 用户零食偏好，默认为"甜食"
            
        Returns:
            SnackPropsResult: 包含推荐零食和解释的字典
            
        Raises:
            ValueError: 当输入参数无效时
        """
        if not password or not isinstance(password, str):
            raise ValueError("password必须是有效的字符串")
        if not preferences or not isinstance(preferences, str):
            raise ValueError("preferences必须是有效的字符串")
            
        parameters = {
            "input": preferences,
            "choose": "AI_SNACKPROPS",
        }
        result = self._execute_workflow(password, parameters, max_retries=5)
        if "error" in result:
            return {"title": result["error"], "explanation": ""}
        return result

    def _parse_output(self, output: Any) -> SnackPropsResult:
        """解析零食推荐输出
        
        Args:
            output: 工作流返回的输出
            
        Returns:
            SnackPropsResult: 解析后的结果
        """
        if isinstance(output, dict):
            return {
                "title": output.get('title', ""),
                "appearance": output.get('appearance', ""),
                "function": output.get('function', ""),
                "sub_fuction": output.get('sub_fuction', ""),
                "warning": output.get('warning', "")
            }
        return {"title": str(output), "explanation": ""}
