#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
日志工具模块
提供统一的日志配置和管理
"""

import logging
import sys
from pathlib import Path
from typing import Optional

# 默认日志格式
DEFAULT_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
DEFAULT_DATE_FORMAT = '%Y-%m-%d %H:%M:%S'

# 日志级别映射
LOG_LEVELS = {
    'DEBUG': logging.DEBUG,
    'INFO': logging.INFO,
    'WARNING': logging.WARNING,
    'ERROR': logging.ERROR,
    'CRITICAL': logging.CRITICAL
}


class ColorFormatter(logging.Formatter):
    """带颜色的日志格式化器"""

    # ANSI颜色代码
    COLORS = {
        'DEBUG': '\033[36m',      # 青色
        'INFO': '\033[32m',       # 绿色
        'WARNING': '\033[33m',    # 黄色
        'ERROR': '\033[31m',      # 红色
        'CRITICAL': '\033[35m',   # 紫色
    }
    RESET = '\033[0m'

    def format(self, record):
        # 添加颜色
        if record.levelname in self.COLORS:
            record.levelname = f"{self.COLORS[record.levelname]}{record.levelname}{self.RESET}"
        return super().format(record)


def get_logger(name: str,
               level: str = 'INFO',
               log_file: Optional[str] = None,
               use_color: bool = True) -> logging.Logger:
    """
    获取配置好的日志记录器

    Args:
        name: 日志记录器名称
        level: 日志级别（DEBUG/INFO/WARNING/ERROR/CRITICAL）
        log_file: 日志文件路径（可选）
        use_color: 是否使用彩色输出

    Returns:
        配置好的日志记录器
    """
    logger = logging.getLogger(name)

    # 设置日志级别
    log_level = LOG_LEVELS.get(level.upper(), logging.INFO)
    logger.setLevel(log_level)

    # 避免重复添加处理器
    if logger.handlers:
        return logger

    # 创建格式化器
    if use_color:
        formatter = ColorFormatter(DEFAULT_FORMAT, DEFAULT_DATE_FORMAT)
    else:
        formatter = logging.Formatter(DEFAULT_FORMAT, DEFAULT_DATE_FORMAT)

    # 控制台处理器
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(log_level)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    # 文件处理器（如果指定）
    if log_file:
        file_path = Path(log_file)
        file_path.parent.mkdir(parents=True, exist_ok=True)

        # 文件格式化器（不带颜色）
        file_formatter = logging.Formatter(DEFAULT_FORMAT, DEFAULT_DATE_FORMAT)

        file_handler = logging.FileHandler(file_path, encoding='utf-8')
        file_handler.setLevel(log_level)
        file_handler.setFormatter(file_formatter)
        logger.addHandler(file_handler)

    return logger


def set_level(logger: logging.Logger, level: str) -> None:
    """
    设置日志级别

    Args:
        logger: 日志记录器
        level: 日志级别
    """
    log_level = LOG_LEVELS.get(level.upper(), logging.INFO)
    logger.setLevel(log_level)
    for handler in logger.handlers:
        handler.setLevel(log_level)


def add_file_handler(logger: logging.Logger, log_file: str) -> None:
    """
    添加文件处理器到日志记录器

    Args:
        logger: 日志记录器
        log_file: 日志文件路径
    """
    file_path = Path(log_file)
    file_path.parent.mkdir(parents=True, exist_ok=True)

    file_formatter = logging.Formatter(DEFAULT_FORMAT, DEFAULT_DATE_FORMAT)
    file_handler = logging.FileHandler(file_path, encoding='utf-8')
    file_handler.setFormatter(file_formatter)
    logger.addHandler(file_handler)


def remove_file_handlers(logger: logging.Logger) -> None:
    """
    移除所有文件处理器

    Args:
        logger: 日志记录器
    """
    handlers_to_remove = [h for h in logger.handlers
                         if isinstance(h, logging.FileHandler)]
    for handler in handlers_to_remove:
        handler.close()
        logger.removeHandler(handler)


def log_function_call(logger: logging.Logger, func_name: str,
                     args: tuple = None, kwargs: dict = None) -> None:
    """
    记录函数调用

    Args:
        logger: 日志记录器
        func_name: 函数名称
        args: 位置参数
        kwargs: 关键字参数
    """
    logger.debug(f"调用函数: {func_name}")
    if args:
        logger.debug(f"  参数: {args}")
    if kwargs:
        logger.debug(f"  关键字参数: {kwargs}")


def log_execution_time(logger: logging.Logger, func_name: str,
                      execution_time: float) -> None:
    """
    记录函数执行时间

    Args:
        logger: 日志记录器
        func_name: 函数名称
        execution_time: 执行时间（秒）
    """
    logger.info(f"{func_name} 执行完成，耗时: {execution_time:.2f}秒")


class LoggerContext:
    """日志上下文管理器"""

    def __init__(self, logger: logging.Logger, context_name: str):
        self.logger = logger
        self.context_name = context_name
        self.start_time = None

    def __enter__(self):
        self.start_time = __import__('time').time()
        self.logger.debug(f"开始: {self.context_name}")
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        execution_time = __import__('time').time() - self.start_time

        if exc_type is None:
            self.logger.info(f"完成: {self.context_name} (耗时: {execution_time:.2f}秒)")
        else:
            self.logger.error(f"失败: {self.context_name} (错误: {exc_val}, 耗时: {execution_time:.2f}秒)")
        return False  # 不抑制异常


if __name__ == "__main__":
    # 测试日志模块
    print("=== 测试日志模块 ===")

    # 基本用法
    logger1 = get_logger("test1", level="INFO")
    logger1.info("这是一条信息")
    logger1.warning("这是一条警告")

    # 带日志文件
    logger2 = get_logger("test2", level="DEBUG", log_file="test.log")
    logger2.debug("调试信息")
    logger2.info("信息")
    logger2.error("错误信息")

    # 使用上下文管理器
    with LoggerContext(logger1, "测试操作"):
        __import__('time').sleep(0.1)
        logger1.debug("在上下文中")

    print("=== 日志模块测试完成 ===")