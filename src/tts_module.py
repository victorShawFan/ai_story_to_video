"""
配音模块（TTS）

调用TTS API为视频生成配音。
"""

import os
import sys
from dataclasses import dataclass
from typing import List, Optional

# 添加 chux_skills 核心模块路径
sys.path.insert(0, os.path.expanduser('~/Desktop/openclaw/skills/chux-skills/core'))

from tts import synthesize_tts


@dataclass
class GeneratedAudio:
    """生成的音频"""
    scene_index: int       # 幕序号
    audio_path: str        # 音频文件路径
    text: str              # 配音文本
    duration: float        # 预估时长（秒）


# 推荐音色
VOICE_PRESETS = {
    "narrator": "zh_female_xiaohe_uranus_bigtts",     # 旁白（女声）
    "male": "zh_male_m191_uranus_bigtts",             # 男声
    "female": "zh_female_vv_uranus_bigtts",           # 女声
}


def generate_audio(
    text: str,
    output_path: str,
    voice: str = "narrator"
) -> GeneratedAudio:
    """
    生成配音

    Args:
        text: 配音文本
        output_path: 输出路径
        voice: 音色类型（narrator/male/female）

    Returns:
        GeneratedAudio对象
    """
    # 确保输出目录存在
    os.makedirs(os.path.dirname(output_path) or ".", exist_ok=True)

    # 获取音色标识
    speaker = VOICE_PRESETS.get(voice, VOICE_PRESETS["narrator"])

    try:
        # 调用TTS API
        synthesize_tts(text, out_path=output_path, speaker=speaker)

        # 预估时长（约每秒25字）
        estimated_duration = len(text) / 25.0

        return GeneratedAudio(
            scene_index=0,  # 需要外部设置
            audio_path=output_path,
            text=text,
            duration=estimated_duration
        )

    except Exception as e:
        print(f"TTS生成失败: {e}")
        return GeneratedAudio(
            scene_index=0,
            audio_path=output_path,
            text=text,
            duration=0.0
        )


def generate_audio_batch(
    texts: List[str],
    output_dir: str = "./output",
    voice: str = "narrator"
) -> List[GeneratedAudio]:
    """
    批量生成配音

    Args:
        texts: 文本列表
        output_dir: 输出目录
        voice: 音色类型

    Returns:
        GeneratedAudio列表
    """
    audios = []
    os.makedirs(output_dir, exist_ok=True)

    for i, text in enumerate(texts):
        output_path = os.path.join(output_dir, f"audio_{i + 1:03d}.wav")
        audio = generate_audio(text, output_path, voice)
        audio.scene_index = i
        audios.append(audio)

    return audios


if __name__ == "__main__":
    # 测试
    test_text = "雨夜，霓虹灯闪烁在香港的街头。"

    audio = generate_audio(test_text, "./test_output/audio_test.wav")
    print(f"音频路径: {audio.audio_path}")
    print(f"文本: {audio.text}")
    print(f"预估时长: {audio.duration}秒")
