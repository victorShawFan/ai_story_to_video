#!/bin/bash
# 启动定时优化任务

cd /Users/bytedance/Desktop/openclaw/ai_story_to_video

# 检查是否已在运行
if [ -f .optimizer.pid ]; then
    PID=$(cat .optimizer.pid)
    if ps -p $PID > /dev/null 2>&1; then
        echo "定时任务已在运行 (PID: $PID)"
        exit 0
    fi
fi

# 后台启动
nohup python3 scheduler.py > logs/scheduler_nohup.log 2>&1 &

echo "定时任务已启动 (PID: $!)"
echo "日志文件: logs/scheduler.log"
