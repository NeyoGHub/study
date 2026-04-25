#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
项目名称: AkShare
脚本名称: 基础使用示例（演示版，无需akshare库）
作者: Adams (CTO)
创建时间: 2026-04-24
修改时间: 2026-04-24
描述: AkShare基础使用示例演示，展示如何使用AkShare进行金融数据分析
"""

import sys
from pathlib import Path
import pandas as pd

# 添加公共脚本路径
COMMON_SCRIPTS = Path(__file__).parent.parent.parent / 'common' / 'scripts'
sys.path.append(str(COMMON_SCRIPTS))

from utils import setup_logger, get_project_root, get_current_timestamp
from logger import get_logger, LoggerContext


def create_demo_stock_data():
    """创建模拟的股票数据（演示用）"""
    logger = get_logger("stock_data", level="INFO")

    with LoggerContext(logger, "创建演示股票数据"):
        try:
            # 创建模拟的股票数据
            data = {
                '代码': ['000001.SZ', '000002.SZ', '600000.SH', '600036.SH', '601318.SH'],
                '名称': ['平安银行', '万科A', '浦发银行', '招商银行', '中国平安'],
                '最新价': [12.34, 23.45, 8.90, 35.67, 45.78],
                '涨跌幅': [1.23, -0.89, 2.34, 0.56, -1.12],
                '成交量': [1234567, 2345678, 3456789, 4567890, 5678901],
                '成交额': [15234.56, 54987.65, 30762.23, 162987.32, 259876.54]
            }

            df = pd.DataFrame(data)

            logger.info(f"✓ 创建了 {len(df)} 条模拟股票数据")
            logger.info(f"数据列: {list(df.columns)}")
            logger.info("\n数据预览:")
            print(df.to_string(index=False))

            return df

        except Exception as e:
            logger.error(f"✗ 创建股票数据失败: {e}")
            raise


def create_demo_fund_data():
    """创建模拟的基金数据（演示用）"""
    logger = get_logger("fund_data", level="INFO")

    with LoggerContext(logger, "创建演示基金数据"):
        try:
            # 创建模拟的基金数据
            data = {
                '代码': ['510300', '510500', '159919', '159915', '511220'],
                '名称': ['沪深300ETF', '中证500ETF', '消费ETF', '创业板ETF', '国债ETF'],
                '单位净值': [4.5678, 7.8901, 2.3456, 3.4567, 1.0234],
                '累计净值': [4.8901, 8.1234, 2.6789, 3.7890, 1.0567],
                '涨跌幅': [0.12, 0.34, -0.23, 0.45, 0.01],
                '规模': [567.89, 890.12, 345.67, 456.78, 123.45]
            }

            df = pd.DataFrame(data)

            logger.info(f"✓ 创建了 {len(df)} 条模拟基金数据")
            logger.info(f"数据列: {list(df.columns)}")
            logger.info("\n数据预览:")
            print(df.to_string(index=False))

            return df

        except Exception as e:
            logger.error(f"✗ 创建基金数据失败: {e}")
            raise


def create_demo_economic_data():
    """创建模拟的经济数据（演示用）"""
    logger = get_logger("economic_data", level="INFO")

    with LoggerContext(logger, "创建演示经济数据"):
        try:
            # 创建模拟的经济数据
            data = {
                '年份': [2019, 2020, 2021, 2022, 2023],
                'GDP总量(万亿)': [98.65, 101.36, 114.92, 121.02, 126.06],
                'GDP增速(%)': [6.0, 2.2, 8.4, 3.0, 5.2],
                '人均GDP(元)': [70343, 72447, 81268, 85698, 89358]
            }

            df = pd.DataFrame(data)

            logger.info(f"✓ 创建了 {len(df)} 条模拟经济数据")
            logger.info(f"数据列: {list(df.columns)}")
            logger.info("\n数据预览:")
            print(df.to_string(index=False))

            return df

        except Exception as e:
            logger.error(f"✗ 创建经济数据失败: {e}")
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


def show_akshare_guide():
    """显示AkShare使用指导"""
    logger = get_logger("guide", level="INFO")

    guide = """
    ╔════════════════════════════════════════════════════════════════╗
    ║                    AkShare使用指导                              ║
    ╠════════════════════════════════════════════════════════════════╣
    ║                                                                ║
    ║  本脚本演示了如何使用AkShare进行金融数据分析                ║
    ║  由于当前环境未安装akshare库，使用模拟数据演示                 ║
    ║                                                                ║
    ║  安装AkShare:                                                  ║
    ║    pip install akshare pandas                                  ║
    ║                                                                ║
    ║  常用API示例:                                                  ║
    ║    import akshare as ak                                        ║
    ║                                                                ║
    ║    # 获取股票数据                                              ║
    ║    stock_data = ak.stock_zh_a_spot_em()                       ║
    ║                                                                ║
    ║    # 获取基金数据                                              ║
    ║    fund_data = ak.fund_em_open_fund_daily()                   ║
    ║                                                                ║
    ║    # 获取经济数据                                              ║
    ║    gdp_data = ak.macro_china_gdp()                            ║
    ║                                                                ║
    ║    # 获取指数数据                                              ║
    ║    index_data = ak.index_zh_a_spot_em()                        ║
    ║                                                                ║
    ║  官方文档:                                                      ║
    ║    https://akshare.akfamily.xyz/                               ║
    ║                                                                ║
    ║  学习路径:                                                      ║
    ║    1. 学习基础API使用                                          ║
    ║    2. 数据清洗和处理                                          ║
    ║    3. 数据分析和可视化                                        ║
    ║    4. 量化策略开发                                            ║
    ║                                                                ║
    ╚════════════════════════════════════════════════════════════════╝
    """

    logger.info(guide)


def main():
    """主函数"""
    logger = get_logger("main", level="INFO")

    logger.info("=" * 60)
    logger.info("AkShare基础使用示例（演示版）")
    logger.info("=" * 60)

    # 显示使用指导
    show_akshare_guide()

    try:
        # 测试股票数据
        print("\n" + "=" * 60)
        print("1. 股票数据演示")
        print("=" * 60)
        stock_df = create_demo_stock_data()

        if stock_df is not None:
            stock_file = save_to_csv(stock_df, "stock_demo_data", "stock")
            logger.info(f"✓ 股票数据已保存: {stock_file}")

        # 测试基金数据
        print("\n" + "=" * 60)
        print("2. 基金数据演示")
        print("=" * 60)
        fund_df = create_demo_fund_data()

        if fund_df is not None:
            fund_file = save_to_csv(fund_df, "fund_demo_data", "fund")
            logger.info(f"✓ 基金数据已保存: {fund_file}")

        # 测试经济数据
        print("\n" + "=" * 60)
        print("3. 经济数据演示")
        print("=" * 60)
        gdp_df = create_demo_economic_data()

        if gdp_df is not None:
            gdp_file = save_to_csv(gdp_df, "gdp_demo_data", "economic")
            logger.info(f"✓ 经济数据已保存: {gdp_file}")

        print("\n" + "=" * 60)
        logger.info("✓ 所有演示完成！")
        logger.info("=" * 60)

        # 输出统计信息
        logger.info("\n数据统计:")
        logger.info(f"  股票数据: {len(stock_df)} 条")
        logger.info(f"  基金数据: {len(fund_df)} 条")
        logger.info(f"  经济数据: {len(gdp_df)} 条")

        # 提示下一步
        logger.info("\n下一步建议:")
        logger.info("  1. 安装AkShare: pip install akshare pandas")
        logger.info("  2. 查看官方文档: https://akshare.akfamily.xyz/")
        logger.info("  3. 开始学习计划中的源码分析")
        logger.info("  4. 尝试实践项目开发")

    except Exception as e:
        logger.error(f"✗ 程序执行失败: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()