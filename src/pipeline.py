"""
完整流程管道

整合所有模块，实现从长文本到视频的自动化流程。
"""

import os
import sys
import time
from dataclasses import dataclass
from typing import List, Optional
from pathlib import Path

# 导入各模块
from text_splitter import TextSplitter, Scene
from script_generator import generate_script, Script
from video_generator import generate_scene_video, GeneratedVideo
from tts_module import generate_audio, GeneratedAudio


@dataclass
class ProcessResult:
    """处理结果"""
    input_file: str
    total_scenes: int
    videos: List[GeneratedVideo]
    audios: List[GeneratedAudio]
    output_dir: str
    success: bool
    error_message: Optional[str] = None


class StoryToVideoPipeline:
    """故事转视频管道"""

    def __init__(self, output_dir: str = "./output"):
        """
        初始化管道

        Args:
            output_dir: 输出目录
        """
        self.output_dir = output_dir
        self.splitter = TextSplitter()

    def process(self, input_file: str, generate_audio_flag: bool = True) -> ProcessResult:
        """
        执行完整流程

        Args:
            input_file: 输入文件路径（TXT/MD）
            generate_audio_flag: 是否生成配音

        Returns:
            ProcessResult对象
        """
        start_time = time.time()

        try:
            # 1. 读取文本
            print(f"📖 读取文件: {input_file}")
            text = self._read_file(input_file)

            # 2. 切割文本
            print("✂️ 切割文本...")
            scenes = self.splitter.split(text)
            print(f"   共切割为 {len(scenes)} 幕")

            # 3. 生成剧本和分镜
            print("📝 生成剧本和分镜...")
            scripts = []
            for i, scene in enumerate(scenes):
                print(f"   处理第 {i + 1}/{len(scenes)} 幕...")
                script = generate_script(scene.text, scene_index=i)
                scripts.append(script)

            # 4. 生成视频
            print("🎬 生成视频...")
            videos = []
            for i, script in enumerate(scripts):
                print(f"   生成第 {i + 1}/{len(scripts)} 个视频...")
                video = generate_scene_video(script, self.output_dir, scene_index=i)
                videos.append(video)

            # 5. 生成配音（可选）
            audios = []
            if generate_audio_flag:
                print("🔊 生成配音...")
                for i, script in enumerate(scripts):
                    print(f"   生成第 {i + 1}/{len(scripts)} 个配音...")
                    audio_path = os.path.join(self.output_dir, f"audio_{i + 1:03d}.wav")
                    audio = generate_audio(script.narration, audio_path)
                    audio.scene_index = i
                    audios.append(audio)

            # 6. 完成
            elapsed = time.time() - start_time
            print(f"\n✅ 处理完成！")
            print(f"   总耗时: {elapsed:.1f}秒")
            print(f"   生成视频: {len(videos)} 个")
            print(f"   生成配音: {len(audios)} 个")
            print(f"   输出目录: {self.output_dir}")

            return ProcessResult(
                input_file=input_file,
                total_scenes=len(scenes),
                videos=videos,
                audios=audios,
                output_dir=self.output_dir,
                success=True
            )

        except Exception as e:
            elapsed = time.time() - start_time
            print(f"\n❌ 处理失败: {e}")
            print(f"   耗时: {elapsed:.1f}秒")

            return ProcessResult(
                input_file=input_file,
                total_scenes=0,
                videos=[],
                audios=[],
                output_dir=self.output_dir,
                success=False,
                error_message=str(e)
            )

    def _read_file(self, file_path: str) -> str:
        """读取文件内容"""
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()


def main():
    """主函数"""
    import argparse

    parser = argparse.ArgumentParser(description='AI故事转视频')
    parser.add_argument('input', help='输入文件路径（TXT/MD）')
    parser.add_argument('-o', '--output', default='./output', help='输出目录')
    parser.add_argument('--no-audio', action='store_true', help='不生成配音')

    args = parser.parse_args()

    # 创建管道
    pipeline = StoryToVideoPipeline(output_dir=args.output)

    # 执行处理
    result = pipeline.process(args.input, generate_audio_flag=not args.no_audio)

    # 退出码
    sys.exit(0 if result.success else 1)


if __name__ == "__main__":
    main()
