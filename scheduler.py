#!/usr/bin/env python3
"""
定时任务管理器

每30分钟执行一次优化任务。
"""

import os
import sys
import time
import subprocess
import signal
from datetime import datetime, timedelta
from pathlib import Path

PROJECT_DIR = Path(__file__).parent
PID_FILE = PROJECT_DIR / ".optimizer.pid"
LOG_FILE = PROJECT_DIR / "logs" / "scheduler.log"

INTERVAL_MINUTES = 15


def log(message: str):
    """输出日志"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_msg = f"[{timestamp}] {message}"
    print(log_msg)

    # 写入日志文件
    with open(LOG_FILE, 'a', encoding='utf-8') as f:
        f.write(log_msg + "\n")


def run_optimization():
    """执行优化"""
    log("🚀 开始优化任务...")

    try:
        result = subprocess.run(
            [sys.executable, str(PROJECT_DIR / "optimize.py")],
            cwd=PROJECT_DIR,
            capture_output=True,
            text=True,
            timeout=300  # 5分钟超时
        )

        if result.returncode == 0:
            log("✅ 优化完成")
        else:
            log(f"❌ 优化失败: {result.stderr[:200]}")

        return result.returncode == 0

    except Exception as e:
        log(f"❌ 优化异常: {e}")
        return False


def signal_handler(signum, frame):
    """信号处理器"""
    log("收到停止信号，退出...")
    if PID_FILE.exists():
        PID_FILE.unlink()
    sys.exit(0)


def main():
    """主函数"""
    # 注册信号处理器
    signal.signal(signal.SIGTERM, signal_handler)
    signal.signal(signal.SIGINT, signal_handler)

    # 写入PID
    with open(PID_FILE, 'w') as f:
        f.write(str(os.getpid()))

    log("=" * 50)
    log("定时优化任务启动")
    log(f"执行间隔: {INTERVAL_MINUTES} 分钟")
    log("=" * 50)

    next_run = datetime.now()

    while True:
        now = datetime.now()

        # 检查是否到执行时间
        if now >= next_run:
            run_optimization()

            # 计算下次执行时间
            next_run = now + timedelta(minutes=INTERVAL_MINUTES)
            log(f"下次执行: {next_run.strftime('%H:%M:%S')}")

        # 等待60秒再检查
        time.sleep(60)


if __name__ == "__main__":
    main()
