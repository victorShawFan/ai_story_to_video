# AI Story to Video

将 TXT/MD 格式的长文本（小说、散文、剧本等）全自动转化为分段 AI 视频。

## 核心流程

```
长文本输入 → 文本切割 → 剧本&分镜生成 → 视频生成 → 视频输出
```

## 功能模块

### 1. 长文本切割模块
- 基于规则的切割方式
- 每幕文本适配约12秒视频
- 保证文本完整性

### 2. 剧本 & 分镜生成模块
- 调用 AI 大模型生成剧本
- 生成分镜描述（画面、镜头、时长）
- 适配视频生成模型输入

### 3. AI 视频生成模块
- 调用视频生成模型
- 每段视频约12秒
- 支持配音（TTS）

## 技术栈

- **文本切割**：基于规则的分段算法
- **剧本生成**：火山引擎 ARK API (ai_chat_integration)
- **视频生成**：火山引擎视频生成 API
- **配音**：火山引擎 TTS API
- **网络搜索**：火山引擎搜索 API

## 项目结构

```
ai_story_to_video/
├── src/
│   ├── text_splitter.py      # 文本切割模块
│   ├── script_generator.py   # 剧本&分镜生成
│   ├── video_generator.py    # 视频生成模块
│   ├── tts_module.py         # 配音模块
│   └── pipeline.py           # 完整流程管道
├── logs/
│   └── optimization_log.md   # 优化日志
├── tests/
│   └── test_pipeline.py      # 测试脚本
├── examples/
│   └── sample_story.txt      # 示例文本
├── README.md
└── requirements.txt
```

## 使用方法

```python
from src.pipeline import StoryToVideoPipeline

# 初始化管道
pipeline = StoryToVideoPipeline()

# 执行转换
pipeline.process("examples/sample_story.txt", output_dir="output/")
```

## 开发状态

- [x] 项目初始化
- [ ] 文本切割模块
- [ ] 剧本生成模块
- [ ] 视频生成模块
- [ ] 配音模块
- [ ] 完整流程测试
- [ ] 定时优化任务

## 优化日志

查看 [logs/optimization_log.md](logs/optimization_log.md) 了解项目演进历史。

## License

MIT
