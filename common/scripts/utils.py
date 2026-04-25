#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
通用工具函数模块
提供跨项目的公共工具函数
"""

import sys
import os
import json
import yaml
import logging
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, List, Optional

# 添加项目路径
PROJECT_ROOT = Path(__file__).parent.parent.parent
sys.path.append(str(PROJECT_ROOT))


def setup_logger(name: str, log_file: Optional[str] = None,
                level: int = logging.INFO) -> logging.Logger:
    """
    设置日志记录器

    Args:
        name: 日志记录器名称
        log_file: 日志文件路径（可选）
        level: 日志级别

    Returns:
        配置好的日志记录器
    """
    logger = logging.getLogger(name)
    logger.setLevel(level)

    # 避免重复添加处理器
    if not logger.handlers:
        # 控制台处理器
        console_handler = logging.StreamHandler()
        console_handler.setLevel(level)
        console_format = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        console_handler.setFormatter(console_format)
        logger.addHandler(console_handler)

        # 文件处理器（如果指定了文件）
        if log_file:
            log_path = Path(log_file)
            log_path.parent.mkdir(parents=True, exist_ok=True)
            file_handler = logging.FileHandler(log_file)
            file_handler.setLevel(level)
            file_format = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            )
            file_handler.setFormatter(file_format)
            logger.addHandler(file_handler)

    return logger


def parse_config(config_path: str) -> Dict[str, Any]:
    """
    解析配置文件

    Args:
        config_path: 配置文件路径（支持yaml和json）

    Returns:
        配置字典
    """
    config_file = Path(config_path)
    if not config_file.exists():
        raise FileNotFoundError(f"配置文件不存在: {config_path}")

    if config_file.suffix in ['.yaml', '.yml']:
        with open(config_file, 'r', encoding='utf-8') as f:
            return yaml.safe_load(f)
    elif config_file.suffix == '.json':
        with open(config_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    else:
        raise ValueError(f"不支持的配置文件格式: {config_file.suffix}")


def save_config(config: Dict[str, Any], config_path: str) -> None:
    """
    保存配置文件

    Args:
        config: 配置字典
        config_path: 配置文件路径
    """
    config_file = Path(config_path)
    config_file.parent.mkdir(parents=True, exist_ok=True)

    if config_file.suffix in ['.yaml', '.yml']:
        with open(config_file, 'w', encoding='utf-8') as f:
            yaml.dump(config, f, default_flow_style=False, allow_unicode=True)
    elif config_file.suffix == '.json':
        with open(config_file, 'w', encoding='utf-8') as f:
            json.dump(config, f, indent=2, ensure_ascii=False)
    else:
        raise ValueError(f"不支持的配置文件格式: {config_file.suffix}")


def ensure_dir(path: str) -> Path:
    """
    确保目录存在，如果不存在则创建

    Args:
        path: 目录路径

    Returns:
        Path对象
    """
    dir_path = Path(path)
    dir_path.mkdir(parents=True, exist_ok=True)
    return dir_path


def get_project_root() -> Path:
    """
    获取项目根目录

    Returns:
        项目根目录Path对象
    """
    return PROJECT_ROOT


def get_current_timestamp() -> str:
    """
    获取当前时间戳字符串

    Returns:
        格式化的时间戳字符串
    """
    return datetime.now().strftime("%Y%m%d_%H%M%S")


def create_symlink(source: str, target: str) -> None:
    """
    创建符号链接

    Args:
        source: 源文件路径
        target: 目标文件路径
    """
    source_path = Path(source)
    target_path = Path(target)

    if not source_path.exists():
        raise FileNotFoundError(f"源文件不存在: {source_path}")

    target_path.parent.mkdir(parents=True, exist_ok=True)

    if target_path.exists():
        target_path.unlink()

    target_path.symlink_to(source_path)


def list_files(directory: str, pattern: str = "*",
                recursive: bool = False) -> List[Path]:
    """
    列出目录中的文件

    Args:
        directory: 目录路径
        pattern: 文件匹配模式
        recursive: 是否递归搜索

    Returns:
        文件路径列表
    """
    dir_path = Path(directory)
    if not dir_path.exists():
        raise FileNotFoundError(f"目录不存在: {dir_path}")

    if recursive:
        return list(dir_path.rglob(pattern))
    else:
        return list(dir_path.glob(pattern))


def merge_dicts(dict1: Dict, dict2: Dict) -> Dict:
    """
    合并两个字典

    Args:
        dict1: 第一个字典
        dict2: 第二个字典（覆盖dict1中的相同键）

    Returns:
        合并后的字典
    """
    result = dict1.copy()
    result.update(dict2)
    return result


def chunk_list(lst: List, chunk_size: int) -> List[List]:
    """
    将列表分块

    Args:
        lst: 原始列表
        chunk_size: 块大小

    Returns:
        分块后的列表
    """
    return [lst[i:i + chunk_size] for i in range(0, len(lst), chunk_size)]


def retry_func(func, max_retries: int = 3, delay: float = 1.0,
               exceptions: tuple = (Exception,), *args, **kwargs):
    """
    重试执行函数

    Args:
        func: 要执行的函数
        max_retries: 最大重试次数
        delay: 重试间隔（秒）
        exceptions: 需要捕获的异常类型
        *args: 函数位置参数
        **kwargs: 函数关键字参数

    Returns:
        函数执行结果

    Raises:
        最后一次的异常
    """
    import time

    last_exception = None
    for attempt in range(max_retries):
        try:
            return func(*args, **kwargs)
        except exceptions as e:
            last_exception = e
            if attempt < max_retries - 1:
                time.sleep(delay)
            else:
                raise last_exception


if __name__ == "__main__":
    # 测试工具函数
    print("=== 测试工具函数 ===")

    # 测试日志设置
    logger = setup_logger("test", level=logging.DEBUG)
    logger.debug("调试消息")
    logger.info("信息消息")
    logger.warning("警告消息")

    # 测试项目根目录
    print(f"项目根目录: {get_project_root()}")

    # 测试时间戳
    print(f"当前时间戳: {get_current_timestamp()}")

    # 测试分块
    test_list = list(range(10))
    print(f"分块结果: {chunk_list(test_list, 3)}")

    print("=== 工具函数测试完成 ===")