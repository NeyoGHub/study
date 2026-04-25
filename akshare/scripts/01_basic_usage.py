#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
项目名称: AkShare
脚本名称: 基础使用示例
作者: Adams (CTO)
创建时间: 2026-04-24
描述: AkShare基础使用示例，学习如何获取股票、基金等金融数据
"""

import sys
from pathlib import Path

# 添加公共脚本路径
COMMON_SCRIPTS = Path(__file__).parent.parent.parent / 'common' / 'scripts'
sys.path.append(str(COMMON_SCRIPTS))

from utils import setup_logger, get_project_root, get_current_timestamp
from logger import get_logger, LoggerContext

# 导入项目库
try:
    import akshare as ak
    import pandas as pd
except ImportError as e:
    print(f"错误：缺少必要的库: {e}")
    print("请运行: pip install akshare pandas")
    sys.exit(1)


def test_stock_data():
    """测试股票数据获取"""
    logger = get_logger("stock_data", level="INFO")

    with LoggerContext(logger, "获取股票数据"):
        try:
            # 获取A股历史数据
            logger.info("获取A股历史数据...")
            stock_df = ak.stock_zh_a_hist(
                symbol="000001",  # 平安银行
                period="daily",   # 日线数据
                adjust="qfq"     # 前复权
            )

            logger.info(f"✓ 获取到 {len(stock_df)} 条数据")
            logger.info(f"数据列: {list(stock_df.columns)}")
            logger.info("\n数据预览:")
            print(stock_df.head().to_string())

            return stock_df

        except Exception as e:
            logger.error(f"✗ 获取股票数据失败: {e}")
            raise


def test_fund_data():
    """测试基金数据获取"""
    logger = get_logger("fund_data", level="INFO")

    with LoggerContext(logger, "获取基金数据"):
        try:
            # 获取开放式基金数据
            logger.info("获取开放式基金数据...")
            fund_df = ak.fund_em_open_fund_daily()

            logger.info(f"✓ 获取到 {len(fund_df)} 只基金")
            logger.info(f"数据列: {list(fund_df.columns)}")
            logger.info("\n数据预览:")
            print(fund_df.head().to_string())

            return fund_df

        except Exception as e:
            logger.error(f"✗ 获取基金数据失败: {e}")
            raise


def test_economic_data():
    """测试经济数据获取"""
    logger = get_logger("economic_data", level="INFO")

    with LoggerContext(logger, "获取经济数据"):
        try:
            # 获取宏观经济数据
            logger.info("获取宏观经济数据...")
            gdp_df = ak.macro_china_gdp()

            logger.info(f"✓ 获取到 {len(gdp_df)} 条GDP数据")
            logger.info(f"数据列: {list(gdp_df.columns)}")
            logger.info("\n数据预览:")
            print(gdp_df.head().to_string())

            return gdp_df

        except Exception as e:
            logger.error(f"✗ 获取经济数据失败: {e}")
            raise


def test_index_data():
    """测试指数数据获取"""
    logger = get_logger("index_data", level="INFO")

    with LoggerContext(logger, "获取指数数据"):
        try:
            # 获取上证指数历史数据
            logger.info("获取上证指数数据...")
            index_df = ak.index_zh_a_hist(symbol="sh000001")

            logger.info(f"✓ 获取到 {len(index_df)} 条指数数据")
            logger.info(f"数据列: {list(index_df.columns)}")
            logger.info("\n数据预览:")
            print(index_df.head().to_string())

            return index_df

        except Exception as e:
            logger.error(f"✗ 获取指数数据失败: {e}")
            raise


def save_to_csv(df, filename: str, subdir: str = "stock"):
    """
    保存数据到CSV文件

    Args:
        df: DataFrame数据
        filename: 文件名
        subdir: 子目录名称
    """
    output_dir = Path(__file__).parent.parent / 'outputs' / 'data' / subdir
    output_dir.mkdir(parents=True, exist_ok=True)

    filepath = output_dir / f"{filename}_{get_current_timestamp()}.csv"
    df.to_csv(filepath, index=False, encoding='utf-8-sig')

    return filepath


def main():
    """主函数"""
    logger = get_logger("main", level="INFO")

    logger.info("=" * 60)
    logger.info("AkShare基础使用示例")
    logger.info("=" * 60)

    try:
        # 测试股票数据
        print("\n" + "=" * 60)
        print("1. 股票数据测试")
        print("=" * 60)
        stock_df = test_stock_data()

        if stock_df is not None:
            stock_file = save_to_csv(stock_df, "000001_stock_data", "stock")
            logger.info(f"✓ 股票数据已保存: {stock_file}")

        # 测试基金数据
        print("\n" + "=" * 60)
        print("2. 基金数据测试")
        print("=" * 60)
        fund_df = test_fund_data()

        if fund_df is not None:
            fund_file = save_to_csv(fund_df, "fund_data", "fund")
            logger.info(f"✓ 基金数据已保存: {fund_file}")

        # 测试经济数据
        print("\n" + "=" * 60)
        print("3. 经济数据测试")
        print("=" * 60)
        gdp_df = test_economic_data()

        if gdp_df is not None:
            gdp_file = save_to_csv(gdp_df, "china_gdp_data", "economic")
            logger.info(f"✓ 经济数据已保存: {gdp_file}")

        # 测试指数数据
        print("\n" + "=" * 60)
        print("4. 指数数据测试")
        print("=" * 60)
        index_df = test_index_data()

        if index_df is not None:
            index_file = save_to_csv(index_df, "sh000001_index_data", "stock")
            logger.info(f"✓ 指数数据已保存: {index_file}")

        print("\n" + "=" * 60)
        logger.info("✓ 所有测试完成！")
        logger.info("=" * 60)

        # 输出统计信息
        logger.info("\n数据统计:")
        logger.info(f"  股票数据: {len(stock_df)} 条")
        logger.info(f"  基金数据: {len(fund_df)} 条")
        logger.info(f"  经济数据: {len(gdp_df)} 条")
        logger.info(f"  指数数据: {len(index_df)} 条")

    except Exception as e:
        logger.error(f"✗ 程序执行失败: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()