import os
import logging
from datetime import datetime

def setup_logger(log_dir: str) -> logging.Logger:
    """配置 root 日志器，确保所有日志（包括第三方库）都写入文件"""
    # 1. 获取 root 日志器（Python 所有日志的根节点）
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.INFO)  # 捕获 INFO 及以上级别日志

    # 2. 清除已有 Handler（避免重复输出）
    if root_logger.hasHandlers():
        root_logger.handlers.clear()

    # 3. 创建日志目录
    os.makedirs(log_dir, exist_ok=True)
    date_str = datetime.now().strftime('%Y%m%d')
    daily_log_dir = os.path.join(log_dir, date_str)
    os.makedirs(daily_log_dir, exist_ok=True)

    # 4. 日志文件路径
    timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
    log_path = os.path.join(daily_log_dir, f"monitor_{timestamp}.log")

    # 5. 添加文件 Handler（写入日志文件）
    file_handler = logging.FileHandler(log_path, encoding='utf-8')
    file_formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',  # 包含日志器名称（如 root、yagmail）
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    file_handler.setFormatter(file_formatter)
    root_logger.addHandler(file_handler)

    # 6. 添加控制台 Handler（同时输出到控制台）
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(file_formatter)
    root_logger.addHandler(console_handler)

    root_logger.info(f"root 日志器初始化完成，日志文件路径: {log_path}")
    return root_logger
