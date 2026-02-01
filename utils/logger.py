# -*- coding: utf-8 -*-
"""
日志记录模块
=====================================
【模块说明】
记录系统运行日志。

【功能】
1. 记录错误信息
2. 记录操作日志
3. 支持不同日志级别

【版本信息】
- 版本：v1.0
- 最后更新：2026-01-24
"""

import logging
import sys
from typing import Optional


def setup_logger(name: str,
                 level: int = logging.INFO,
                 log_file: Optional[str] = None) -> logging.Logger:
    """设置日志记录器"""

    logger = logging.getLogger(name)
    logger.setLevel(level)

    # 避免重复添加handler
    if logger.handlers:
        return logger

    # 格式器
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )

    # 控制台handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    # 文件handler（如果指定了日志文件）
    if log_file:
        file_handler = logging.FileHandler(log_file, encoding='utf-8')
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

    return logger