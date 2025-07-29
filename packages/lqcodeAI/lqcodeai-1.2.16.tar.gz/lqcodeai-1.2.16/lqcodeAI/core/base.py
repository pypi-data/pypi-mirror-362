from typing import Dict, Any, Optional
import requests
import time
import functools
from datetime import datetime, timedelta
import json

from .config import Config
from cozepy import Coze, COZE_CN_BASE_URL, TokenAuth, Stream, WorkflowEvent, WorkflowEventType

class BaseAI:
    """AI功能的基础类，提供通用的功能和方法"""
    
    def __init__(self, config: Optional[Config] = None):
        self.config = self._validate_config(config)
        self._token_cache = {}
        self._token_expiry = {}
    
    def _validate_config(self, config: Optional[Config]) -> Config:
        """验证配置的有效性"""
        if config is None:
            return Config()
        if not isinstance(config, Config):
            raise TypeError("config必须是Config类型")
        return config
    
    @functools.lru_cache(maxsize=100)  # 使用默认值100，实际值会在运行时通过self.config.cache_size获取
    def _get_ai_token(self, password: str) -> TokenAuth:
        """获取AI访问令牌（带缓存）"""
        cache_key = f"{password}"
        if cache_key in self._token_cache:
            if datetime.now() < self._token_expiry.get(cache_key, datetime.now()):
                return self._token_cache[cache_key]
        
        res = requests.get(self.config.base_url, params={'password': password}, timeout=10)
        res.raise_for_status()
        data = res.json()
        token = TokenAuth(data['data'])
        self._token_cache[cache_key] = token
        self._token_expiry[cache_key] = datetime.now() + timedelta(hours=self.config.token_expiry_hours)
        return token

    def _execute_workflow(self, password: str, parameters: Dict[str, Any], 
                         max_retries: Optional[int] = None, base_delay: Optional[int] = None) -> Dict[str, Any]:
        """执行工作流的通用方法"""
        max_retries = max_retries or self.config.max_retries
        base_delay = base_delay or self.config.base_delay
        retry_count = 0
        
        while retry_count < max_retries:
            try:
                token_auth = self._get_ai_token(password)
                coze = Coze(auth=token_auth, base_url=COZE_CN_BASE_URL)
                
                workflow_stream = coze.workflows.runs.stream(
                    workflow_id=self.config.workflow_id,
                    parameters=parameters
                )
                
                return self._process_workflow_stream(workflow_stream, coze)
                
            except Exception:
                retry_count += 1
                if retry_count == max_retries:
                    return {"error": "执行失败，请稍后再试"}
                delay = min(base_delay * (2 ** (retry_count - 1)), 30)
                time.sleep(delay)
        
        return {"error": "执行失败，请稍后再试"}

    def _process_workflow_stream(self, workflow_stream: Stream, coze: Coze) -> Dict[str, Any]:
        """处理工作流事件的通用方法"""
        for event in workflow_stream:
            if event.event == WorkflowEventType.MESSAGE:
                if hasattr(event.message, 'content'):
                    return self._parse_content(event.message.content)
            elif event.event == WorkflowEventType.ERROR:
                return {"error": f"工作流错误: {str(event.error)}"}
            elif event.event == WorkflowEventType.INTERRUPT:
                interrupt_result = self._handle_workflow_interrupt(coze, event)
                if interrupt_result:
                    return interrupt_result
        
        return {"error": "未能获取结果，请稍后再试"}

    def _handle_workflow_interrupt(self, coze: Coze, event: WorkflowEvent) -> Optional[Dict[str, Any]]:
        """处理工作流中断事件"""
        try:
            resume_stream = coze.workflows.runs.resume(
                workflow_id=self.config.workflow_id,
                event_id=event.interrupt.interrupt_data.event_id,
                resume_data="继续",
                interrupt_type=event.interrupt.interrupt_data.type,
            )
            
            for resume_event in resume_stream:
                if resume_event.event == WorkflowEventType.MESSAGE:
                    if hasattr(resume_event.message, 'content'):
                        return self._parse_content(resume_event.message.content)
                elif resume_event.event == WorkflowEventType.INTERRUPT:
                    nested_result = self._handle_workflow_interrupt(coze, resume_event)
                    if nested_result:
                        return nested_result
            
            return None
        except Exception:
            return None

    def _parse_content(self, content: Any) -> Dict[str, Any]:
        """解析工作流返回的内容"""
        if isinstance(content, str):
            try:
                content_json = json.loads(content)
                if 'output' in content_json:
                    return self._parse_output(content_json['output'])
                return {"result": str(content_json)}
            except json.JSONDecodeError:
                return {"result": content}
        elif hasattr(content, 'text'):
            return {"result": content.text}
        return {"result": str(content)}

    def _parse_output(self, output: Any) -> Dict[str, Any]:
        """解析output1字段的内容，由子类实现"""
        raise NotImplementedError 