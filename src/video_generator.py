"""
视频生成模块

调用视频生成API，基于剧本生成分段视频。
"""

import os
import sys
import time
from dataclasses import dataclass
from typing import List, Optional

# 添加 chux_skills 核心模块路径
sys.path.insert(0, os.path.expanduser('~/Desktop/openclaw/skills/chux-skills/core'))

from video_generation import generate_video as _generate_video
from common import temp_path


@dataclass
class GeneratedVideo:
    """生成的视频"""
    scene_index: int       # 幕序号
    video_path: str        # 视频文件路径
    duration: float        # 时长（秒）
    prompt: str            # 生成提示词


def generate_scene_video(
    script,  # Script对象
    output_dir: str = "./output",
    scene_index: int = 0
) -> GeneratedVideo:
    """
    为一幕生成视频

    Args:
        script: Script对象（剧本）
        output_dir: 输出目录
        scene_index: 幕序号

    Returns:
        GeneratedVideo对象
    """
    # 确保输出目录存在
    os.makedirs(output_dir, exist_ok=True)

    # 构建视频生成提示词
    prompt = _build_video_prompt(script)

    # 生成视频文件路径
    video_path = os.path.join(output_dir, f"scene_{scene_index + 1:03d}.mp4")

    try:
        # 调用视频生成API
        _generate_video(prompt, out_path=video_path)

        # 检查文件是否生成成功
        if os.path.exists(video_path) and os.path.getsize(video_path) > 1000:
            return GeneratedVideo(
                scene_index=scene_index,
                video_path=video_path,
                duration=script.total_duration,
                prompt=prompt
            )
        else:
            # 生成失败，返回占位
            return GeneratedVideo(
                scene_index=scene_index,
                video_path=video_path,
                duration=0.0,
                prompt=prompt
            )

    except Exception as e:
        print(f"视频生成失败: {e}")
        return GeneratedVideo(
            scene_index=scene_index,
            video_path=video_path,
            duration=0.0,
            prompt=prompt
        )


def _build_video_prompt(script) -> str:
    """
    构建视频生成提示词

    将剧本和分镜转换为视频生成API能理解的提示词
    """
    parts = []

    # 添加风格
    parts.append(script.style)

    # 添加分镜描述
    for sb in script.storyboards:
        parts.append(sb.description)
        if sb.camera_movement != "固定镜头":
            parts.append(sb.camera_movement)

    # 添加氛围关键词
    prompt = "，".join(parts)

    # 限制长度（视频生成API通常有提示词长度限制）
    if len(prompt) > 300:
        prompt = prompt[:300]

    return prompt


def generate_videos_batch(scripts: List, output_dir: str = "./output") -> List[GeneratedVideo]:
    """
    批量生成视频

    Args:
        scripts: Script列表
        output_dir: 输出目录

    Returns:
        GeneratedVideo列表
    """
    videos = []
    total = len(scripts)

    for i, script in enumerate(scripts):
        print(f"生成视频 {i + 1}/{total}...")
        video = generate_scene_video(script, output_dir, scene_index=i)
        videos.append(video)

        # 避免API调用过快
        if i < total - 1:
            time.sleep(2)

    return videos


if __name__ == "__main__":
    # 测试需要先导入Script
    from script_generator import Script, Storyboard

    # 创建测试剧本
    test_script = Script(
        scene_index=0,
        narration="雨夜，霓虹灯闪烁",
        storyboards=[
            Storyboard(1, "香港街头雨夜，霓虹灯闪烁", "推镜头", 4.0),
            Storyboard(2, "穿着皮夹克的年轻人走过", "跟拍", 4.0),
            Storyboard(3, "年轻人脸上焦虑的表情", "特写", 4.0)
        ],
        total_duration=12.0,
        style="复古港风，电影质感"
    )

    video = generate_scene_video(test_script, output_dir="./test_output")
    print(f"视频路径: {video.video_path}")
    print(f"提示词: {video.prompt}")
