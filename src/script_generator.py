"""
剧本 & 分镜生成模块

调用 AI 大模型为每一幕生成剧本和分镜描述。
"""

import json
from dataclasses import dataclass
from typing import List, Optional
import sys
import os

# 添加 chux_skills 核心模块路径
sys.path.insert(0, os.path.expanduser('~/Desktop/openclaw/skills/chux-skills/core'))

from ai_chat_integration import chat
from pydantic import BaseModel, Field


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
    scene_index: int                # 幕序号
    narration: str                  # 旁白/台词
    storyboards: List[Storyboard]   # 分镜列表
    total_duration: float           # 总时长
    style: str                      # 风格描述


class ScriptResult(BaseModel):
    """AI返回的结构化结果"""
    narration: str = Field(..., description="旁白或台词")
    storyboards: List[dict] = Field(..., description="分镜列表")
    style: str = Field(default="电影质感", description="画面风格")


# 系统提示词
SYSTEM_PROMPT = """你是一个专业的影视剧本创作专家。你的任务是根据提供的文本片段，生成适合视频展示的剧本和分镜。

要求：
1. 生成简洁的旁白或台词（适合配音）
2. 设计2-3个分镜，每个分镜包含：
   - shot_number: 镜头序号
   - description: 画面描述（具体的视觉内容）
   - camera_movement: 镜头运动（如：推镜头、拉镜头、跟拍、固定镜头）
   - duration: 时长（秒，总和约12秒）
3. 指定画面风格（如：电影质感、复古港风、现代都市等）

输出JSON格式：
{
  "narration": "旁白内容",
  "storyboards": [
    {"shot_number": 1, "description": "画面描述", "camera_movement": "推镜头", "duration": 4.0},
    ...
  ],
  "style": "风格描述"
}
"""


def generate_script(scene_text: str, scene_index: int = 0) -> Script:
    """
    为一幕生成剧本和分镜

    Args:
        scene_text: 一幕的文本
        scene_index: 幕序号

    Returns:
        Script对象
    """
    # 构建提示词
    prompt = f"{SYSTEM_PROMPT}\n\n文本内容：\n{scene_text}"

    try:
        # 调用AI生成
        result = chat(
            prompt=prompt,
            response_format=ScriptResult
        )

        if isinstance(result, str):
            # 如果返回字符串，尝试解析JSON
            try:
                data = json.loads(result)
                result = ScriptResult(**data)
            except:
                # 解析失败，使用默认值
                result = ScriptResult(
                    narration=scene_text[:100],
                    storyboards=[{
                        "shot_number": 1,
                        "description": scene_text[:50],
                        "camera_movement": "固定镜头",
                        "duration": 12.0
                    }],
                    style="电影质感"
                )

        # 转换为Storyboard对象
        storyboards = []
        total_duration = 0.0
        for sb in result.storyboards:
            storyboard = Storyboard(
                shot_number=sb.get("shot_number", 1),
                description=sb.get("description", ""),
                camera_movement=sb.get("camera_movement", "固定镜头"),
                duration=sb.get("duration", 4.0)
            )
            storyboards.append(storyboard)
            total_duration += storyboard.duration

        return Script(
            scene_index=scene_index,
            narration=result.narration,
            storyboards=storyboards,
            total_duration=total_duration,
            style=result.style
        )

    except Exception as e:
        # 错误处理：返回基本剧本
        return Script(
            scene_index=scene_index,
            narration=scene_text[:100],
            storyboards=[Storyboard(
                shot_number=1,
                description=scene_text[:50],
                camera_movement="固定镜头",
                duration=12.0
            )],
            total_duration=12.0,
            style="电影质感"
        )


def generate_scripts_batch(scene_texts: List[str]) -> List[Script]:
    """
    批量生成剧本

    Args:
        scene_texts: 多幕文本列表

    Returns:
        Script列表
    """
    scripts = []
    for i, text in enumerate(scene_texts):
        script = generate_script(text, scene_index=i)
        scripts.append(script)
    return scripts


if __name__ == "__main__":
    # 测试
    sample_text = "雨夜，霓虹灯闪烁在香港的街头。一个穿着皮夹克的年轻人匆匆走过。"

    script = generate_script(sample_text)

    print(f"幕{script.scene_index + 1}")
    print(f"旁白: {script.narration}")
    print(f"风格: {script.style}")
    print(f"总时长: {script.total_duration}秒")
    print("\n分镜:")
    for sb in script.storyboards:
        print(f"  镜头{sb.shot_number}: {sb.description}")
        print(f"    运动: {sb.camera_movement}, 时长: {sb.duration}秒")
