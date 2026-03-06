"""
剧本 & 分镜生成模块

调用 AI 大模型为每一幕生成剧本和分镜描述。
"""

import json
from dataclasses import dataclass
from typing import List, Optional
from api_client import call_text_api


@dataclass
class Storyboard:
    """分镜"""
    shot_number: int        # 镜头序号
    description: str        # 画面描述
    camera_movement: str    # 镜头运动
    duration: float         # 时长（秒）


@dataclass
class Script:
    """剧本"""
    scene_index: int            # 幕序号
    original_text: str          # 原始文本
    narration: str              # 旁白文本
    visual_description: str     # 视觉描述
    storyboards: List[Storyboard]  # 分镜列表
    mood: str                   # 氛围/情绪
    estimated_duration: float   # 预估总时长


def generate_script(scene_text: str, scene_index: int = 0) -> Script:
    """
    为一幕文本生成剧本和分镜

    Args:
        scene_text: 场景文本
        scene_index: 场景序号

    Returns:
        Script 对象
    """
    prompt = f"""你是一个专业的影视剧本编剧。请为以下场景文本生成剧本和分镜描述。

场景文本：
{scene_text}

请按以下 JSON 格式输出（不要包含 ```json 标记）：
{{
    "narration": "旁白文本（适合朗读）",
    "visual_description": "整体视觉描述",
    "mood": "氛围（如：紧张、温馨、神秘）",
    "storyboards": [
        {{
            "shot_number": 1,
            "description": "画面描述",
            "camera_movement": "镜头运动（如：推镜头、拉镜头、固定）",
            "duration": 3.0
        }}
    ]
}}

要求：
1. 旁白要简洁生动，适合配音
2. 视觉描述要具体，包含场景、人物、动作
3. 分镜建议 2-4 个，总时长控制在 10-15 秒
4. 只输出 JSON，不要其他内容"""

    try:
        response = call_text_api(prompt)
        
        # 清理响应
        response = response.strip()
        if response.startswith("```"):
            response = response.split("\n", 1)[1]
        if response.endswith("```"):
            response = response.rsplit("\n", 1)[0]
        response = response.strip()
        
        data = json.loads(response)
        
        storyboards = [
            Storyboard(
                shot_number=sb.get("shot_number", i + 1),
                description=sb.get("description", ""),
                camera_movement=sb.get("camera_movement", "固定"),
                duration=sb.get("duration", 3.0)
            )
            for i, sb in enumerate(data.get("storyboards", []))
        ]
        
        total_duration = sum(sb.duration for sb in storyboards)
        
        return Script(
            scene_index=scene_index,
            original_text=scene_text,
            narration=data.get("narration", scene_text),
            visual_description=data.get("visual_description", ""),
            storyboards=storyboards,
            mood=data.get("mood", "中性"),
            estimated_duration=total_duration
        )
        
    except Exception as e:
        # 降级：返回简单剧本
        return Script(
            scene_index=scene_index,
            original_text=scene_text,
            narration=scene_text,
            visual_description=scene_text,
            storyboards=[Storyboard(1, scene_text, "固定", 12.0)],
            mood="中性",
            estimated_duration=12.0
        )


if __name__ == "__main__":
    # 测试
    test_text = "雨夜，霓虹灯闪烁在香港的街头。一个穿着皮夹克的年轻人匆匆走过。"
    script = generate_script(test_text)
    print(f"旁白: {script.narration}")
    print(f"分镜数: {len(script.storyboards)}")
    print(f"预估时长: {script.estimated_duration}秒")
