"""
独立的API调用模块

避免相对导入问题。
"""

import os
import json
import requests


# API配置
ARK_API_KEY = "fc6cebfc-2f06-42e5-8b00-afee06eb50f1"
ARK_BASE_URL = "https://ark-cn-beijing.bytedance.net/api/v3"


def chat(prompt: str, temperature: float = 0.7) -> str:
    """调用AI对话API"""
    url = f"{ARK_BASE_URL}/chat/completions"
    headers = {
        "Authorization": f"Bearer {ARK_API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": "doubao-seed-1-6-251015",
        "messages": [{"role": "user", "content": prompt}],
        "temperature": temperature
    }

    try:
        resp = requests.post(url, headers=headers, json=payload, timeout=60)
        resp.raise_for_status()
        data = resp.json()
        return data["choices"][0]["message"]["content"]
    except Exception as e:
        return f"API调用失败: {e}"


def web_search(query: str, limit: int = 3) -> list:
    """模拟网络搜索（返回示例结果）"""
    # 由于实际搜索需要API，这里返回示例
    return [
        {"title": f"AI视频生成技术{query}", "url": "https://example.com/1", "snippet": "文本转视频的最新进展"},
        {"title": f"故事转视频{query}", "url": "https://example.com/2", "snippet": "自动化视频生成方案"},
        {"title": f"视频生成API{query}", "url": "https://example.com/3", "snippet": "主流视频生成服务对比"},
    ][:limit]


if __name__ == "__main__":
    # 测试
    result = chat("你好")
    print(result)
