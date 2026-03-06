"""
配音模块

调用 TTS API 为每一幕生成配音。
"""

import os
from dataclasses import dataclass
from typing import Optional
from api_client import call_tts_api


@dataclass
class GeneratedAudio:
    """生成的音频"""
    scene_index: int       # 幕序号
    audio_path: str        # 音频文件路径
    duration: float        # 音频时长（秒）
    success: bool          # 是否成功


def generate_audio(
    text: str,
    output_path: str,
    speaker: str = "zh_female_xiaohe_uranus_bigtts"
) -> GeneratedAudio:
    """
    为文本生成配音

    Args:
        text: 要转换的文本
        output_path: 输出音频路径
        speaker: 音色标识

    Returns:
        GeneratedAudio 对象
    """
    try:
        call_tts_api(text, output_path, speaker)
        
        # 检查文件有效性
        with open(output_path, "rb") as f:
            content = f.read()
        
        # WAV 文件头为 RIFF
        success = content[:4] == b"RIFF" and len(content) > 44
        
        # 简单估算时长（16kHz, 单声道, 16bit）
        duration = (len(content) - 44) / (16000 * 2)
        
        return GeneratedAudio(
            scene_index=0,
            audio_path=output_path,
            duration=duration,
            success=success
        )
        
    except Exception as e:
        # 降级：生成静音
        import wave
        import math
        
        sample_rate = 16000
        seconds = 1.0
        frames = int(sample_rate * seconds)
        
        with wave.open(output_path, "wb") as wf:
            wf.setnchannels(1)
            wf.setsampwidth(2)
            wf.setframerate(sample_rate)
            wf.writeframes(bytes(frames * 2))  # 静音
        
        return GeneratedAudio(
            scene_index=0,
            audio_path=output_path,
            duration=seconds,
            success=False
        )


if __name__ == "__main__":
    # 测试
    audio = generate_audio("你好，这是一个测试。", "./test_audio.wav")
    print(f"音频路径: {audio.audio_path}")
    print(f"时长: {audio.duration:.2f}秒")
    print(f"成功: {audio.success}")
