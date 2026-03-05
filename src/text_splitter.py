"""
文本切割模块

将长文本切割为适配约12秒视频的"幕"。

切割规则：
1. 按段落优先切割
2. 单幕文本长度：200-400字（适配12秒视频）
3. 保持语义完整性
"""

import re
from dataclasses import dataclass
from typing import List


@dataclass
class Scene:
    """一幕的内容"""
    index: int           # 幕序号
    text: str            # 原始文本
    char_count: int      # 字符数
    estimated_duration: float  # 预估视频时长（秒）


class TextSplitter:
    """文本切割器"""

    # 配置参数
    MIN_CHARS = 150      # 最小字符数
    MAX_CHARS = 400      # 最大字符数
    CHARS_PER_SECOND = 25  # 每秒字符数（用于估算）

    def split(self, text: str) -> List[Scene]:
        """
        将长文本切割为若干幕

        Args:
            text: 输入的长文本

        Returns:
            Scene列表
        """
        # 预处理：移除多余空白
        text = self._preprocess(text)

        # 按段落分割
        paragraphs = self._split_paragraphs(text)

        # 合并为幕
        scenes = self._merge_to_scenes(paragraphs)

        return scenes

    def _preprocess(self, text: str) -> str:
        """预处理文本"""
        # 移除多余空白
        text = re.sub(r'\n{3,}', '\n\n', text)
        text = text.strip()
        return text

    def _split_paragraphs(self, text: str) -> List[str]:
        """按段落分割"""
        # 按双换行分割
        paragraphs = re.split(r'\n\s*\n', text)
        # 过滤空段落
        paragraphs = [p.strip() for p in paragraphs if p.strip()]
        return paragraphs

    def _merge_to_scenes(self, paragraphs: List[str]) -> List[Scene]:
        """将段落合并为幕"""
        scenes = []
        current_text = ""
        index = 0

        for para in paragraphs:
            # 如果当前幕为空，直接添加
            if not current_text:
                current_text = para
            # 如果添加后不超过最大长度，合并
            elif len(current_text) + len(para) + 1 <= self.MAX_CHARS:
                current_text = current_text + "\n" + para
            # 否则，保存当前幕，开始新幕
            else:
                # 保存当前幕
                scenes.append(self._create_scene(index, current_text))
                index += 1
                current_text = para

        # 保存最后一幕
        if current_text:
            scenes.append(self._create_scene(index, current_text))

        return scenes

    def _create_scene(self, index: int, text: str) -> Scene:
        """创建一幕"""
        char_count = len(text)
        estimated_duration = char_count / self.CHARS_PER_SECOND
        return Scene(
            index=index,
            text=text,
            char_count=char_count,
            estimated_duration=estimated_duration
        )


def split_text(text: str) -> List[Scene]:
    """便捷函数：切割文本"""
    splitter = TextSplitter()
    return splitter.split(text)


if __name__ == "__main__":
    # 测试
    sample = """
    雨夜，霓虹灯闪烁在香港的街头。

    一个穿着皮夹克的年轻人匆匆走过，他的脸上写满了焦虑。

    "必须找到她。"他喃喃自语，脚步加快。

    街角的咖啡店里，一个女孩正在等待。她的目光望向窗外，似乎在期待着什么。

    "你来了。"她轻声说道。

    年轻人推开门，浑身湿透，但眼中满是坚定。

    "我们走吧。"
    """

    scenes = split_text(sample)
    for scene in scenes:
        print(f"幕{scene.index + 1}: {scene.char_count}字, 预估{scene.estimated_duration:.1f}秒")
        print(f"  {scene.text[:50]}...")
        print()
