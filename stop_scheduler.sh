#!/bin/bash
# 停止定时优化任务

cd /Users/bytedance/Desktop/openclaw/ai_story_to_video

if [ -f .optimizer.pid ]; then
    PID=$(cat .optimizer.pid)
    kill $PID 2>/dev/null
    rm .optimizer.pid
    echo "定时任务已停止 (PID: $PID)"
else
    echo "未找到运行中的定时任务"
fi
