"""
AI藏头诗功能测试案例
"""
from lqcodeAI import lq

def test_ai_poetry():
    """测试AI藏头诗功能"""
    try:
        # 测试基本功能
        result = lq.ai_poetry(password='lqcode', message='李梅')
        
        # 验证结果格式
        assert isinstance(result, dict)
        assert 'poem' in result
        assert 'explanation' in result
        assert isinstance(result['poem'], str)
        assert isinstance(result['explanation'], str)
        
        print("✅ AI藏头诗功能测试通过")
        print(f"诗词: {result['poem']}")
        print(f"解释: {result['explanation']}")
        
    except Exception as e:
        print(f"❌ AI藏头诗功能测试失败: {e}")
        raise

if __name__ == "__main__":
    test_ai_poetry() 