"""
测试脚本

测试完整流程管道。
"""

import os
import sys

# 添加src路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from pipeline import StoryToVideoPipeline


def create_test_story():
    """创建测试故事文件"""
    test_story = """
雨夜，霓虹灯闪烁在香港的街头。

一个穿着皮夹克的年轻人匆匆走过，他的脸上写满了焦虑。

"必须找到她。"他喃喃自语，脚步加快。

街角的咖啡店里，一个女孩正在等待。她的目光望向窗外，似乎在期待着什么。

咖啡的热气氤氲，窗外的霓虹倒映在她的眼中。

"你来了。"她轻声说道。

年轻人推开门，浑身湿透，但眼中满是坚定。

"我们走吧。"

两人消失在雨夜的街头，只留下霓虹灯的余晖。
"""
    return test_story


def test_pipeline():
    """测试完整流程"""
    print("=" * 50)
    print("AI Story to Video - 测试")
    print("=" * 50)

    # 创建测试文件
    test_dir = os.path.join(os.path.dirname(__file__), 'test_data')
    os.makedirs(test_dir, exist_ok=True)

    test_file = os.path.join(test_dir, 'test_story.txt')
    with open(test_file, 'w', encoding='utf-8') as f:
        f.write(create_test_story())

    print(f"\n测试文件: {test_file}")

    # 创建输出目录
    output_dir = os.path.join(test_dir, 'output')

    # 执行管道
    pipeline = StoryToVideoPipeline(output_dir=output_dir)
    result = pipeline.process(test_file, generate_audio_flag=False)

    # 检查结果
    print("\n" + "=" * 50)
    print("测试结果")
    print("=" * 50)
    print(f"成功: {result.success}")
    print(f"总幕数: {result.total_scenes}")
    print(f"生成视频: {len(result.videos)} 个")

    if result.error_message:
        print(f"错误: {result.error_message}")

    return result.success


if __name__ == "__main__":
    success = test_pipeline()
    sys.exit(0 if success else 1)
