"""
视频生成模块

调用视频生成 API 为每一幕生成视频。
"""

import os
from dataclasses import dataclass
from typing import Optional
from api_client import call_video_api
from script_generator import Script


@dataclass
class GeneratedVideo:
    """生成的视频"""
    scene_index: int       # 幕序号
    video_path: str        # 视频文件路径
    duration: float        # 视频时长
    success: bool          # 是否成功


def generate_scene_video(
    script: Script,
    output_dir: str,
    scene_index: int = 0
) -> GeneratedVideo:
    """
    为一幕剧本生成视频

    Args:
        script: 剧本对象
        output_dir: 输出目录
        scene_index: 场景序号

    Returns:
        GeneratedVideo 对象
    """
    os.makedirs(output_dir, exist_ok=True)
    video_path = os.path.join(output_dir, f"scene_{scene_index + 1:03d}.mp4")
    
    # 构建视频生成 prompt
    prompt = f"""{script.visual_description}

镜头风格：电影质感，真实光影
氛围：{script.mood}
"""
    
    # 添加分镜描述
    if script.storyboards:
        prompt += "\n镜头设计：\n"
        for sb in script.storyboards:
            prompt += f"- {sb.description}（{sb.camera_movement}，{sb.duration}秒）\n"
    
    try:
        call_video_api(prompt, video_path)
        
        # 检查文件是否有效（非最小降级文件）
        with open(video_path, "rb") as f:
            content = f.read()
        success = len(content) > 100  # 大于最小降级文件
        
        return GeneratedVideo(
            scene_index=scene_index,
            video_path=video_path,
            duration=script.estimated_duration,
            success=success
        )
        
    except Exception as e:
        # 降级：创建占位视频
        call_video_api("placeholder", video_path)
        
        return GeneratedVideo(
            scene_index=scene_index,
            video_path=video_path,
            duration=script.estimated_duration,
            success=False
        )


if __name__ == "__main__":
    # 测试
    from script_generator import generate_script
    
    test_text = "雨夜，霓虹灯闪烁在香港的街头。"
    script = generate_script(test_text)
    
    video = generate_scene_video(script, "./test_output")
    print(f"视频路径: {video.video_path}")
    print(f"成功: {video.success}")
