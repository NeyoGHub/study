#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
配置管理模块
提供统一的配置加载、保存和管理功能
"""

import yaml
import json
from pathlib import Path
from typing import Dict, Any, Optional, List
import copy

from .logger import get_logger

logger = get_logger(__name__)


class ConfigManager:
    """配置管理器"""

    def __init__(self, config_file: Optional[str] = None):
        """
        初始化配置管理器

        Args:
            config_file: 配置文件路径
        """
        self.config = {}
        self.config_file = Path(config_file) if config_file else None

        if self.config_file and self.config_file.exists():
            self.load()

    def load(self, config_file: Optional[str] = None) -> Dict[str, Any]:
        """
        加载配置文件

        Args:
            config_file: 配置文件路径（如果为None则使用初始化时指定的文件）

        Returns:
            配置字典
        """
        if config_file:
            self.config_file = Path(config_file)

        if not self.config_file or not self.config_file.exists():
            raise FileNotFoundError(f"配置文件不存在: {self.config_file}")

        logger.info(f"加载配置文件: {self.config_file}")

        if self.config_file.suffix in ['.yaml', '.yml']:
            with open(self.config_file, 'r', encoding='utf-8') as f:
                self.config = yaml.safe_load(f) or {}
        elif self.config_file.suffix == '.json':
            with open(self.config_file, 'r', encoding='utf-8') as f:
                self.config = json.load(f)
        else:
            raise ValueError(f"不支持的配置文件格式: {self.config_file.suffix}")

        logger.debug(f"配置加载完成: {len(self.config)} 项")
        return self.config

    def save(self, config_file: Optional[str] = None) -> None:
        """
        保存配置文件

        Args:
            config_file: 配置文件路径（如果为None则使用初始化时指定的文件）
        """
        if config_file:
            self.config_file = Path(config_file)

        if not self.config_file:
            raise ValueError("未指定配置文件路径")

        self.config_file.parent.mkdir(parents=True, exist_ok=True)

        logger.info(f"保存配置文件: {self.config_file}")

        if self.config_file.suffix in ['.yaml', '.yml']:
            with open(self.config_file, 'w', encoding='utf-8') as f:
                yaml.dump(self.config, f, default_flow_style=False,
                         allow_unicode=True, sort_keys=False)
        elif self.config_file.suffix == '.json':
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(self.config, f, indent=2, ensure_ascii=False)
        else:
            raise ValueError(f"不支持的配置文件格式: {self.config_file.suffix}")

        logger.info("配置保存完成")

    def get(self, key: str, default: Any = None) -> Any:
        """
        获取配置项

        Args:
            key: 配置键（支持点分隔的嵌套键，如 'database.host'）
            default: 默认值

        Returns:
            配置值
        """
        keys = key.split('.')
        value = self.config

        try:
            for k in keys:
                value = value[k]
            return value
        except (KeyError, TypeError):
            return default

    def set(self, key: str, value: Any) -> None:
        """
        设置配置项

        Args:
            key: 配置键（支持点分隔的嵌套键）
            value: 配置值
        """
        keys = key.split('.')
        config = self.config

        for k in keys[:-1]:
            if k not in config:
                config[k] = {}
            config = config[k]

        config[keys[-1]] = value
        logger.debug(f"设置配置项: {key} = {value}")

    def update(self, updates: Dict[str, Any]) -> None:
        """
        批量更新配置

        Args:
            updates: 更新字典
        """
        for key, value in updates.items():
            self.set(key, value)

    def has(self, key: str) -> bool:
        """
        检查配置项是否存在

        Args:
            key: 配置键

        Returns:
            是否存在
        """
        return self.get(key) is not None

    def delete(self, key: str) -> None:
        """
        删除配置项

        Args:
            key: 配置键
        """
        keys = key.split('.')
        config = self.config

        try:
            for k in keys[:-1]:
                config = config[k]
            del config[keys[-1]]
            logger.debug(f"删除配置项: {key}")
        except (KeyError, TypeError):
            logger.warning(f"配置项不存在: {key}")

    def clear(self) -> None:
        """清空所有配置"""
        self.config = {}
        logger.info("清空所有配置")

    def copy(self) -> 'ConfigManager':
        """
        创建配置管理器的副本

        Returns:
            新的配置管理器实例
        """
        new_manager = ConfigManager()
        new_manager.config = copy.deepcopy(self.config)
        new_manager.config_file = self.config_file
        return new_manager

    def to_dict(self) -> Dict[str, Any]:
        """
        转换为字典

        Returns:
            配置字典
        """
        return copy.deepcopy(self.config)

    @staticmethod
    def load_config_file(config_file: str) -> Dict[str, Any]:
        """
        静态方法：加载配置文件

        Args:
            config_file: 配置文件路径

        Returns:
            配置字典
        """
        manager = ConfigManager(config_file)
        return manager.config

    @staticmethod
    def save_config_file(config: Dict[str, Any], config_file: str) -> None:
        """
        静态方法：保存配置文件

        Args:
            config: 配置字典
            config_file: 配置文件路径
        """
        manager = ConfigManager()
        manager.config = config
        manager.save(config_file)


class ConfigDict:
    """配置字典类，提供类似字典的访问方式"""

    def __init__(self, data: Dict[str, Any] = None):
        """
        初始化配置字典

        Args:
            data: 初始数据
        """
        self._data = data or {}

    def __getitem__(self, key: str) -> Any:
        return self._data.get(key)

    def __setitem__(self, key: str, value: Any) -> None:
        self._data[key] = value

    def __contains__(self, key: str) -> bool:
        return key in self._data

    def __len__(self) -> int:
        return len(self._data)

    def __iter__(self):
        return iter(self._data)

    def get(self, key: str, default: Any = None) -> Any:
        """获取配置项"""
        return self._data.get(key, default)

    def set(self, key: str, value: Any) -> None:
        """设置配置项"""
        self._data[key] = value

    def update(self, updates: Dict[str, Any]) -> None:
        """批量更新"""
        self._data.update(updates)

    def to_dict(self) -> Dict[str, Any]:
        """转换为普通字典"""
        return self._data.copy()


def merge_configs(*configs: Dict[str, Any]) -> Dict[str, Any]:
    """
    合并多个配置字典（后面的覆盖前面的）

    Args:
        *configs: 配置字典

    Returns:
        合并后的配置字典
    """
    result = {}
    for config in configs:
        result.update(config)
    return result


if __name__ == "__main__":
    # 测试配置管理
    print("=== 测试配置管理模块 ===")

    # 创建配置管理器
    manager = ConfigManager()

    # 设置配置
    manager.set('database.host', 'localhost')
    manager.set('database.port', 5432)
    manager.set('app.name', 'test_app')
    manager.set('app.debug', True)

    # 获取配置
    print(f"数据库地址: {manager.get('database.host')}")
    print(f"应用名称: {manager.get('app.name')}")

    # 检查配置
    print(f"包含 database.host: {manager.has('database.host')}")
    print(f"包含 database.user: {manager.has('database.user')}")

    # 批量更新
    manager.update({
        'database.user': 'test_user',
        'database.password': 'test_pass'
    })

    # 保存配置
    manager.save('test_config.yaml')

    # 加载配置
    manager2 = ConfigManager('test_config.yaml')
    print(f"加载后的配置: {manager2.to_dict()}")

    # 清理测试文件
    Path('test_config.yaml').unlink()

    print("=== 配置管理模块测试完成 ===")