#!/usr/bin/env python3
"""
监控脚本 - 检查定时任务状态并发送汇报
由心跳检查时调用
"""

import os
import sys
from pathlib import Path
from datetime import datetime

PROJECT_DIR = Path(__file__).parent
REPORT_FILE = PROJECT_DIR / ".last_report.txt"
PID_FILE = PROJECT_DIR / ".optimizer.pid"
SCHEDULER_LOG = PROJECT_DIR / "logs" / "scheduler.log"


def check_scheduler_running():
    """检查定时任务是否运行"""
    if not PID_FILE.exists():
        return False, "PID文件不存在"

    try:
        with open(PID_FILE, 'r') as f:
            pid = f.read().strip()

        # 检查进程是否存在
        import subprocess
        result = subprocess.run(
            ['ps', '-p', pid],
            capture_output=True,
            text=True
        )

        if result.returncode == 0:
            return True, f"运行中 (PID: {pid})"
        else:
            return False, f"进程已停止 (PID: {pid})"

    except Exception as e:
        return False, f"检查失败: {e}"


def get_last_execution():
    """获取上次执行时间"""
    try:
        with open(SCHEDULER_LOG, 'r') as f:
            lines = f.readlines()

        # 查找最后一次"优化完成"
        for line in reversed(lines):
            if "✅ 优化完成" in line:
                # 提取时间
                time_str = line.split(']')[0].replace('[', '')
                return time_str

        return "未知"

    except Exception as e:
        return f"读取失败: {e}"


def get_pending_report():
    """获取待发送的汇报"""
    if not REPORT_FILE.exists():
        return None

    try:
        with open(REPORT_FILE, 'r', encoding='utf-8') as f:
            content = f.read().strip()

        # 检查是否是最近的汇报（5分钟内）
        import time
        file_mtime = REPORT_FILE.stat().st_mtime
        age_seconds = time.time() - file_mtime

        if age_seconds < 300:  # 5分钟内
            return content
        else:
            return None

    except Exception as e:
        return None


def main():
    """主函数"""
    # 检查定时任务状态
    running, status = check_scheduler_running()

    # 获取上次执行时间
    last_exec = get_last_execution()

    # 获取待发送汇报
    report = get_pending_report()

    # 输出状态
    print(f"定时任务状态: {status}")
    print(f"上次执行: {last_exec}")
    print(f"待发送汇报: {'有' if report else '无'}")

    # 如果有待发送的汇报，输出到标准输出
    if report:
        print("\n---REPORT_START---")
        print(report)
        print("---REPORT_END---")


if __name__ == "__main__":
    main()
