# 🎯 一个文件搞定：AI功能插件开发指南

## 🎉 终极简化：真正的"一个文件搞定"

经过最新架构优化，现在添加新的AI功能**真的只需要创建一个文件**！每个插件完全独立，包含自己的类型定义、业务逻辑和注册信息。

## ✨ 完全自动化的功能

- ✅ **自动发现插件** - 无需手动导入
- ✅ **自动注册功能** - 无需修改注册表  
- ✅ **自动生成CLI** - 无需配置命令行
- ✅ **插件内部类型定义** - 完全独立，无外部依赖
- ✅ **动态导出** - 自动添加到包的导出列表
- ✅ **完整的类型检查** - 支持TypedDict和IDE智能提示

## 🆕 最新架构优势

### 插件完全独立
- 🔒 **零外部依赖** - 每个插件都是自包含的
- 📦 **类型定义内置** - 不再依赖全局types.py
- 🔧 **一文件完整** - 类型、逻辑、配置全在一个文件
- 🚀 **即插即用** - 创建文件立即可用

### 开发体验优化
- 💡 **IDE友好** - 完整的类型提示和自动补全
- 🐛 **调试简单** - 所有相关代码都在同一文件
- 📝 **维护容易** - 修改功能只需要编辑一个文件
- 🔄 **版本独立** - 每个插件可以独立更新

## 🚀 超简单步骤

### 步骤1：创建插件文件（唯一步骤！）

在 `lqcodeAI/plugins/` 目录下创建 `ai_你的功能名.py` 文件：

```python
"""
你的功能描述
"""
from typing import Any, Dict, TypedDict
from ..core.base import BaseAI
from ..core.plugin_registry import ai_plugin

# 插件内部定义返回类型（推荐做法）
class YourFeatureResult(TypedDict):
    """你的功能结果类型"""
    content: str
    explanation: str

@ai_plugin(
    name="yourfeature",                    # 功能名称
    description="你的功能描述",             # 功能描述
    cli_args=[                            # CLI参数（可选）
        {"name": "input_text", "help": "输入文本", "default": "默认值"},
        {"name": "style", "help": "处理风格", "default": "标准"}
    ],
    result_type=YourFeatureResult          # 返回类型（可选但推荐）
)
class YourFeatureAI(BaseAI):
    """你的功能AI类"""
    
    def ai_yourfeature(self, password: str, input_text: str = "默认值", style: str = "标准") -> YourFeatureResult:
        """你的功能实现
        
        Args:
            password: 访问密码（必需）
            input_text: 输入文本
            style: 处理风格
            
        Returns:
            YourFeatureResult: 返回结果
        """
        # 参数验证
        if not password or not isinstance(password, str):
            raise ValueError("password必须是有效的字符串")
            
        # 准备工作流参数
        parameters = {
            "input": f"用户输入: {input_text}，风格: {style}",
            "choose": "AI_YOUR_TYPE",  # 根据实际工作流类型修改
        }
        
        # 调用工作流
        result = self._execute_workflow(password, parameters)
        
        # 错误处理
        if "error" in result:
            return {"content": result["error"], "explanation": ""}
        
        return result

    def _parse_output(self, output: Any) -> YourFeatureResult:
        """解析输出结果"""
        if isinstance(output, dict):
            return {
                "content": output.get('content', str(output)),
                "explanation": output.get('explanation', "")
            }
        return {"content": str(output), "explanation": ""}
```

### 步骤2：完成！

没有步骤2！创建文件后，系统会自动：

- 🔍 **发现新插件**
- 📋 **注册到系统**  
- 🐍 **提供Python接口**: `lq.ai_yourfeature()`
- 🖥️ **生成CLI命令**: `lqcodeAI yourfeature`
- 📖 **生成帮助**: `lqcodeAI yourfeature --help`

## 📝 真实示例：藏头诗生成器

以下是一个完整的真实插件示例：

### 文件：`ai_poetry.py`

```python
from typing import Any, Dict, TypedDict
from ..core.base import BaseAI
from ..core.plugin_registry import ai_plugin

class PoetryResult(TypedDict):
    """藏头诗结果类型"""
    poem: str
    explanation: str

@ai_plugin(
    name="poetry",
    description="生成藏头诗功能",
    cli_args=[
        {"name": "message", "help": "藏头诗内容", "default": "李梅"}
    ],
    result_type=PoetryResult
)
class PoetryAI(BaseAI):
    """藏头诗AI功能"""
    
    def ai_poetry(self, password: str, message: str = "李梅") -> PoetryResult:
        """生成藏头诗"""
        if not password or not isinstance(password, str):
            raise ValueError("password必须是有效的字符串")
        if not message or not isinstance(message, str):
            raise ValueError("message必须是有效的字符串")
            
        parameters = {
            "input": message,
            "choose": "AI_POETY",
        }
        result = self._execute_workflow(password, parameters, max_retries=5)
        if "error" in result:
            return {"poem": result["error"], "explanation": ""}
        return result

    def _parse_output(self, output: Any) -> PoetryResult:
        """解析藏头诗输出"""
        if isinstance(output, dict):
            return {
                "poem": output.get('poety', ""),
                "explanation": output.get('explain', "")
            }
        return {"poem": str(output), "explanation": ""}
```

### 自动获得的功能：

**Python接口:**
```python
from lqcodeAI import lq

# 生成藏头诗
result = lq.ai_poetry('lqcode', message='绿旗编程')
print(result['poem'])
print(result['explanation'])
```

**CLI命令:**
```bash
# 使用默认参数
lqcodeAI poetry

# 指定参数
lqcodeAI poetry --message 绿旗编程

# 查看帮助
lqcodeAI poetry --help
```

## 🔧 开发模板

为了让开发更简单，这里提供一个通用模板：

```python
"""
[功能名称]插件 - [功能描述]
"""
from typing import Any, Dict, TypedDict
from ..core.base import BaseAI
from ..core.plugin_registry import ai_plugin

# 插件内部定义返回类型（推荐做法）
class [功能名称]Result(TypedDict):
    """[功能名称]结果类型"""
    content: str
    explanation: str

@ai_plugin(
    name="[功能名称小写]",
    description="[功能描述]",
    cli_args=[
        {"name": "input_param", "help": "输入参数说明", "default": "默认值"},
        {"name": "style_param", "help": "风格参数说明", "default": "标准"}
    ],
    result_type=[功能名称]Result
)
class [功能名称]AI(BaseAI):
    """[功能名称]AI功能"""
    
    def ai_[功能名称小写](self, password: str, input_param: str = "默认值", style_param: str = "标准") -> [功能名称]Result:
        """[功能名称]实现"""
        # 参数验证
        if not password or not isinstance(password, str):
            raise ValueError("password必须是有效的字符串")
            
        # 准备工作流参数
        parameters = {
            "input": f"用户输入: {input_param}，风格: {style_param}",
            "choose": "AI_[功能名称大写]",
        }
        
        # 调用工作流
        result = self._execute_workflow(password, parameters)
        
        # 错误处理
        if "error" in result:
            return {"content": result["error"], "explanation": ""}
        
        return result

    def _parse_output(self, output: Any) -> [功能名称]Result:
        """解析输出结果"""
        if isinstance(output, dict):
            return {
                "content": output.get('content', str(output)),
                "explanation": output.get('explanation', "")
            }
        return {"content": str(output), "explanation": ""}
```

## 🎯 命名规范

### 文件命名
- **格式**: `ai_功能名.py`
- **示例**: `ai_poetry.py`, `ai_translate.py`, `ai_summary.py`

### 类命名  
- **格式**: `功能名AI`
- **示例**: `PoetryAI`, `TranslateAI`, `SummaryAI`

### 类型命名
- **格式**: `功能名Result`
- **示例**: `PoetryResult`, `TranslateResult`, `SummaryResult`

### 方法命名
- **格式**: `ai_功能名`
- **示例**: `ai_poetry`, `ai_translate`, `ai_summary`

### 插件名称
- **格式**: 小写，简洁明了
- **示例**: `poetry`, `translate`, `summary`

## 📊 系统会自动处理

| 功能 | 自动化程度 | 说明 |
|------|-----------|------|
| 插件发现 | ✅ 100% | 扫描plugins目录自动发现 |
| 功能注册 | ✅ 100% | @ai_plugin装饰器自动注册 |
| Python接口 | ✅ 100% | 动态生成lq.ai_xxx()方法 |
| CLI命令 | ✅ 100% | 根据cli_args自动生成 |
| 类型检查 | ✅ 100% | 完整的TypedDict支持 |
| 帮助文档 | ✅ 100% | 自动生成--help信息 |
| 错误处理 | ✅ 100% | 统一的错误处理机制 |

## ✅ 最佳实践

### 类型定义
```python
# ✅ 推荐：在插件内部定义类型
class MyFeatureResult(TypedDict):
    """功能结果类型"""
    content: str
    explanation: str

# ❌ 避免：使用过于通用的类型
def ai_feature(self, password: str) -> Dict[str, Any]:
```

### 参数设计
```python
# ✅ 推荐：提供有意义的默认值
cli_args=[
    {"name": "theme", "help": "故事主题", "default": "科幻"},
    {"name": "length", "help": "故事长度", "default": "短篇"}
]

# ❌ 避免：没有默认值或帮助信息
cli_args=[
    {"name": "param1"},
    {"name": "param2"}
]
```

### 错误处理
```python
# ✅ 推荐：完整的参数验证
if not password or not isinstance(password, str):
    raise ValueError("password必须是有效的字符串")

# ✅ 推荐：优雅的错误处理
if "error" in result:
    return {"content": result["error"], "explanation": "处理失败"}
```

## 🎉 当前插件展示

现在已经实现的插件，都是"一个文件搞定"：

- 📝 **ai_poetry.py** - 藏头诗生成（完整类型定义、CLI支持）
- 🛡️ **ai_weapons.py** - AI武器生成器（主题风格定制）
- 🍪 **ai_snackprops.py** - 零食推荐器（个性化推荐）

每个插件都自动拥有：
- 🐍 **Python接口**：`lq.ai_xxx()`
- 🖥️ **CLI命令**：`lqcodeAI xxx`
- 📖 **帮助文档**：`lqcodeAI xxx --help`
- 🔍 **类型检查**：完整的IDE支持

## 🚀 立即开始

想要添加新功能？就是这么简单：                  

1. 在 `lqcodeAI/plugins/` 目录创建 `ai_你的功能.py`
2. 复制上面的模板代码
3. 修改功能名称和实现逻辑
4. 保存文件
5. 完成！🎉

## 🔧 调试和测试

### 快速测试新插件
```bash
# 测试插件是否正确加载
cd lqcodeAI
python -c "from lqcodeAI import lq; print(lq.get_available_functions())"

# 测试CLI命令
lqcodeAI list
lqcodeAI yourfeature --help
```

### 常见问题排查
1. **插件未被发现**：检查文件名是否以`ai_`开头
2. **CLI参数错误**：检查`cli_args`格式是否正确
3. **类型错误**：确保导入了`TypedDict`
4. **方法未找到**：确保方法名以`ai_`开头

现在就去试试吧！你的新AI功能只需要一个文件！✨ 