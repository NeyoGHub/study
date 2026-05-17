#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
数字货币数据源研究 - CoinGecko API 完全测试
=========================================
背景: AkShare自带的crypto接口只有3个且数据有限
方案: 使用CoinGecko免费API (无需Key, 10-30次/分钟)
测试全部公开端点并输出技术分析

CoinGecko API文档: https://docs.coingecko.com/v3.0.1/reference/endpoint-overview
"""
import pandas as pd
import numpy as np
import requests
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
from datetime import datetime, timedelta
import os
import time
import json

# ===== 配置 =====
FONT_PATH = '/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc'
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUTPUT_DIR = os.path.join(BASE_DIR, 'output')
DATA_DIR = os.path.join(OUTPUT_DIR, 'data', 'crypto')
PLOTS_DIR = os.path.join(OUTPUT_DIR, 'plots', 'crypto')
os.makedirs(DATA_DIR, exist_ok=True)
os.makedirs(PLOTS_DIR, exist_ok=True)

API_BASE = "https://api.coingecko.com/api/v3"
TS_NOW = datetime.now().strftime("%Y%m%d_%H%M%S")

# 中文字体
try:
    cf = fm.FontProperties(fname=FONT_PATH, size=12)
    plt.rcParams['font.family'] = 'Noto Sans CJK JP'
    CHINESE_OK = True
except:
    cf = None
    CHINESE_OK = False
    print("⚠ 中文字体加载失败")

# API限速: 每次请求后休眠
RATE_LIMIT_SLEEP = 3  # 秒

def cg_get(endpoint, params=None, retries=2):
    """调用CoinGecko API的通用函数"""
    url = f"{API_BASE}{endpoint}"
    for attempt in range(retries):
        try:
            r = requests.get(url, params=params, timeout=15)
            if r.status_code == 429:
                print(f"    ⚠ 限速, 等待5秒...")
                time.sleep(5)
                continue
            if r.status_code == 404:
                return None, 404
            if r.status_code == 401:
                return None, 401
            r.raise_for_status()
            return r.json(), r.status_code
        except requests.exceptions.HTTPError as e:
            print(f"    ❌ HTTP {r.status_code}: {str(e)[:100]}")
            return None, r.status_code
        except Exception as e:
            if attempt < retries - 1:
                print(f"    ⚠ 重试 {attempt+1}/{retries}: {str(e)[:80]}")
                time.sleep(2)
                continue
            print(f"    ❌ 错误: {str(e)[:100]}")
            return None, 0
    return None, 0

def section(title):
    print(f"\n{'=' * 65}")
    print(f"📌 {title}")
    print(f"{'=' * 65}")

def subsection(title):
    print(f"\n  [{title}]")

# ============================================================
# 一、系统状态
# ============================================================
def test_ping():
    section("一、系统状态 - /ping")
    data, code = cg_get("/ping")
    if data:
        print(f"  ✅ 服务器状态: {data.get('gecko_says', 'OK')}")
    return {"ping": data is not None}

# ============================================================
# 二、简单价格 API
# ============================================================
def test_simple_price():
    section("二、简单价格 API (/simple/*)")
    
    results = {}
    
    # 2.1 实时价格
    subsection("2.1 /simple/price - 多币种实时价格")
    coin_ids = "bitcoin,ethereum,solana,ripple,cardano,dogecoin,polkadot,avalanche-2,chainlink,tron"
    data, code = cg_get("/simple/price", {
        "ids": coin_ids,
        "vs_currencies": "usd",
        "include_24hr_change": "true",
        "include_24hr_vol": "true",
        "include_market_cap": "true",
        "include_last_updated_at": "true"
    })
    if data:
        rows = []
        for cid, info in data.items():
            rows.append({
                "CoinGeckoID": cid,
                "价格(USD)": info.get("usd", 0),
                "24h变化(%)": info.get("usd_24h_change", 0),
                "24h量(USD)": info.get("usd_24h_vol", 0),
                "市值(USD)": info.get("usd_market_cap", 0),
            })
        df = pd.DataFrame(rows)
        results['实时价格'] = df
        print(df.round(2).to_string(index=False))
        save_csv(df, "coingecko_simple_price")
    
    time.sleep(RATE_LIMIT_SLEEP)
    
    # 2.2 支持的计价货币
    subsection("2.2 /simple/supported_vs_currencies - 支持的计价货币")
    data, code = cg_get("/simple/supported_vs_currencies")
    if data:
        df_cur = pd.DataFrame({"计价货币": data})
        # 列出主要货币
        majors = [c for c in data if c in ['usd', 'cny', 'eur', 'gbp', 'jpy', 'krw', 'hkd', 'aud', 'cad', 'chf']]
        print(f"  ✅ 共 {len(data)} 种计价货币")
        print(f"  主流: {', '.join(majors)}")
        results['计价货币'] = df_cur
    
    time.sleep(RATE_LIMIT_SLEEP)
    
    return results

# ============================================================
# 三、Coins 数据 API
# ============================================================
def test_coins_data():
    section("三、Coins 数据 API (/coins/*)")
    results = {}
    
    # 3.1 币种列表
    subsection("3.1 /coins/list - 全部币种列表")
    data, code = cg_get("/coins/list")
    if data:
        df_list = pd.DataFrame(data)
        active = len(data)
        print(f"  ✅ CoinGecko 收录币种总数: {active:,}")
        results['币种总数'] = active
        # 保存完整列表到CSV (截取部分用于展示)
        df_list.to_csv(os.path.join(DATA_DIR, f"coingecko_coins_list_{TS_NOW}.csv"), index=False, encoding='utf-8-sig')
        print(f"  示例: {df_list.head(5).to_string(index=False)}")
    
    time.sleep(RATE_LIMIT_SLEEP)
    
    # 3.2 币种行情列表
    subsection("3.2 /coins/markets - 币种行情列表")
    data, code = cg_get("/coins/markets", {
        "vs_currency": "usd",
        "order": "market_cap_desc",
        "per_page": 20,
        "page": 1,
        "sparkline": "false",
        "price_change_percentage": "1h,24h,7d"
    })
    if data:
        rows = []
        for c in data:
            rows.append({
                "排名": c.get("market_cap_rank", 0),
                "币种": c.get("name", ""),
                "符号": c.get("symbol", "").upper(),
                "价格(USD)": c.get("current_price", 0),
                "24h变化(%)": c.get("price_change_percentage_24h", 0),
                "7d变化(%)": c.get("price_change_percentage_7d_in_currency", 0),
                "市值(USD)": c.get("market_cap", 0),
                "24h量(USD)": c.get("total_volume", 0),
                "流通量": c.get("circulating_supply", 0),
                "总供应量": c.get("total_supply", 0) or 0,
                "历史最高": c.get("ath", 0),
                "ATH日期": c.get("ath_date", ""),
                "涨跌幅从ATH": c.get("ath_change_percentage", 0),
            })
        df_market = pd.DataFrame(rows)
        results['行情列表'] = df_market
        print(df_market.round(2).to_string(index=False))
        save_csv(df_market, "coingecko_markets")
    
    time.sleep(RATE_LIMIT_SLEEP)
    
    # 3.3 单个币种详情
    subsection("3.3 /coins/{id} - 币种详细信息")
    for coin_id in ["bitcoin", "ethereum"]:
        data, code = cg_get(f"/coins/{coin_id}", {
            "localization": "false",
            "tickers": "false",
            "community_data": "true",
            "developer_data": "true",
            "sparkline": "false"
        })
        if data:
            desc = data.get("description", {}).get("en", "")[:120]
            links = data.get("links", {})
            social = {
                "twitter": links.get("twitter_screen_name", ""),
                "reddit": links.get("subreddit_url", ""),
                "github": links.get("repos_url", {}).get("github", [None])[0] if links.get("repos_url") else "",
            }
            market = data.get("market_data", {})
            print(f"  {data['name']} ({data['symbol'].upper()})")
            print(f"    描述: {desc}...")
            print(f"    当前价格: ${market.get('current_price', {}).get('usd', 'N/A'):,}")
            print(f"    市值排名: #{data.get('market_cap_rank', 'N/A')}")
            print(f"    24h变化: {market.get('price_change_percentage_24h', 0):+.2f}%")
            print(f"    30d变化: {market.get('price_change_percentage_30d', 0):+.2f}%")
            print(f"    Twitter: @{social['twitter']}")
            print(f"    GitHub: {social['github'] or 'N/A'}")
            print(f"    社区评分: {data.get('community_score', 'N/A')}")
            print(f"    开发者评分: {data.get('developer_score', 'N/A')}")
            results[f'{coin_id}_详情'] = data
    
    time.sleep(RATE_LIMIT_SLEEP)
    
    # 3.4 币种Tickers
    subsection("3.4 /coins/{id}/tickers - 币种交易所Ticker")
    for coin_id in ["bitcoin", "ethereum"]:
        data, code = cg_get(f"/coins/{coin_id}/tickers", {"exchange_ids": "binance,okx,bybit", "order": "volume_desc"})
        if data and data.get("tickers"):
            tickers = data["tickers"][:5]
            print(f"  {coin_id} Top 5 Tickers:")
            for t in tickers:
                base = t.get("base", "")
                target = t.get("target", "")
                vol = t.get("volume", 0)
                last = t.get("last", 0)
                market = t.get("market", {}).get("name", "")
                print(f"    {market:10s} {base}/{target:6s}  ${last:>8,.2f}  量: {float(vol):>12,.0f}")
            results[f'{coin_id}_tickers'] = tickers
    
    time.sleep(RATE_LIMIT_SLEEP)
    
    # 3.5 历史数据 (指定日期)
    subsection("3.5 /coins/{id}/history - 历史数据")
    data, code = cg_get("/coins/bitcoin/history", {"date": "13-05-2026", "localization": "false"})
    if data:
        market = data.get("market_data", {})
        print(f"  BTC 2026-05-13 历史数据:")
        print(f"    价格: ${market.get('current_price', {}).get('usd', 'N/A'):,}")
        print(f"    市值: ${market.get('market_cap', {}).get('usd', 'N/A'):,}")
        print(f"    24h量: ${market.get('total_volume', {}).get('usd', 'N/A'):,}")
        results['btc_history_date'] = data
    
    time.sleep(RATE_LIMIT_SLEEP)
    
    # 3.6 OHLC数据
    subsection("3.6 /coins/{id}/ohlc - OHLC数据")
    data, code = cg_get("/coins/bitcoin/ohlc", {"vs_currency": "usd", "days": "30"})
    if data:
        df_ohlc = pd.DataFrame(data, columns=["timestamp", "open", "high", "low", "close"])
        df_ohlc["timestamp"] = pd.to_datetime(df_ohlc["timestamp"], unit="ms")
        df_ohlc.set_index("timestamp", inplace=True)
        results['btc_ohlc'] = df_ohlc
        print(f"  BTC 30天OHLC: {len(df_ohlc)} 条K线 ({df_ohlc.index[0].date()} ~ {df_ohlc.index[-1].date()})")
        print(df_ohlc.tail(5).round(0).to_string())
        
        # 也获取ETH的OHLC用于对比
        time.sleep(RATE_LIMIT_SLEEP)
        eth_ohlc, _ = cg_get("/coins/ethereum/ohlc", {"vs_currency": "usd", "days": "30"})
        if eth_ohlc:
            df_eth = pd.DataFrame(eth_ohlc, columns=["timestamp", "open", "high", "low", "close"])
            df_eth["timestamp"] = pd.to_datetime(df_eth["timestamp"], unit="ms")
            df_eth.set_index("timestamp", inplace=True)
            results['eth_ohlc'] = df_eth
        
        save_csv(df_ohlc, "coingecko_btc_ohlc_30d")
    
    time.sleep(RATE_LIMIT_SLEEP)
    
    # 3.7 市场图表 (价格+市值+量)
    subsection("3.7 /coins/{id}/market_chart - 市场图表数据")
    data, code = cg_get("/coins/bitcoin/market_chart", {"vs_currency": "usd", "days": "14"})
    if data:
        prices = pd.DataFrame(data.get("prices", []), columns=["timestamp", "price"])
        prices["timestamp"] = pd.to_datetime(prices["timestamp"], unit="ms")
        prices.set_index("timestamp", inplace=True)
        
        caps = pd.DataFrame(data.get("market_caps", []), columns=["timestamp", "market_cap"])
        caps["timestamp"] = pd.to_datetime(caps["timestamp"], unit="ms")
        caps.set_index("timestamp", inplace=True)
        
        volumes = pd.DataFrame(data.get("total_volumes", []), columns=["timestamp", "volume"])
        volumes["timestamp"] = pd.to_datetime(volumes["timestamp"], unit="ms")
        volumes.set_index("timestamp", inplace=True)
        
        print(f"  价格数据: {len(prices)} 条")
        print(f"  市值数据: {len(caps)} 条")
        print(f"  量数据:   {len(volumes)} 条")
        print(f"  当前价格: ${prices['price'].iloc[-1]:,.2f}")
        print(f"  14天前:  ${prices['price'].iloc[0]:,.2f}")
        print(f"  涨跌幅:   {((prices['price'].iloc[-1] / prices['price'].iloc[0]) - 1) * 100:+.2f}%")
        
        results['btc_market_chart'] = {"prices": prices, "market_caps": caps, "volumes": volumes}
        
        # 保存
        df_chart = pd.DataFrame({
            "price": prices["price"],
            "market_cap": caps["market_cap"],
            "volume": volumes["volume"]
        })
        save_csv(df_chart, "coingecko_btc_market_chart_14d")
    
    time.sleep(RATE_LIMIT_SLEEP)
    
    # 3.8 市场图表 (时间范围)
    subsection("3.8 /coins/{id}/market_chart/range - 时间范围市场数据")
    start_ts = int((datetime.now() - timedelta(days=7)).timestamp())
    end_ts = int(datetime.now().timestamp())
    data, code = cg_get("/coins/bitcoin/market_chart/range", {
        "vs_currency": "usd",
        "from": start_ts,
        "to": end_ts
    })
    if data:
        print(f"  7天范围价格点: {len(data.get('prices', []))}")
        prices_range = data.get("prices", [])
        if prices_range:
            print(f"  起始: ${prices_range[0][1]:,.2f} -> 结束: ${prices_range[-1][1]:,.2f}")
        results['btc_market_chart_range'] = data
    
    time.sleep(RATE_LIMIT_SLEEP)
    
    # 3.9 币种分类
    subsection("3.9 /coins/categories - 分类市场数据")
    data, code = cg_get("/coins/categories")
    if data:
        rows = []
        for c in data[:15]:
            rows.append({
                "分类": c.get("name", ""),
                "市值(USD)": c.get("market_cap", 0),
                "24h变化(%)": c.get("market_cap_change_percentage_24h", 0),
                "币种数": c.get("top_3_coins", [None, None, None])[0] if c.get("top_3_coins") else "",
            })
        df_cat = pd.DataFrame(rows)
        print(df_cat.round(2).to_string(index=False))
        results['categories'] = data[:15]
        save_csv(df_cat, "coingecko_categories")
    
    time.sleep(RATE_LIMIT_SLEEP)
    
    return results

# ============================================================
# 四、交易所 & 衍生品 API
# ============================================================
def test_exchanges():
    section("四、交易所 & 衍生品 API")
    results = {}
    
    # 4.1 交易所列表
    subsection("4.1 /exchanges - 交易所列表")
    data, code = cg_get("/exchanges", {"per_page": 10, "page": 1})
    if data:
        rows = []
        for ex in data:
            rows.append({
                "交易所": ex.get("name", ""),
                "排名": ex.get("trust_score_rank", 0),
                "国家": ex.get("country", ""),
                "24h量(BTC)": ex.get("trade_volume_24h_btc", 0),
                "信任分": ex.get("trust_score", 0),
                "建立年份": ex.get("year_established", ""),
                "网址": ex.get("url", ""),
            })
        df_ex = pd.DataFrame(rows)
        print(df_ex.to_string(index=False))
        results['exchanges'] = df_ex
        save_csv(df_ex, "coingecko_exchanges")
    
    time.sleep(RATE_LIMIT_SLEEP)
    
    # 4.2 交易所ID列表
    subsection("4.2 /exchanges/list - 交易所ID映射")
    data, code = cg_get("/exchanges/list")
    if data:
        print(f"  ✅ 支持 {len(data)} 个交易所")
        # 找主流交易所
        majors = [e for e in data if e['id'] in ['binance', 'okx', 'bybit', 'coinbase', 'kraken', 'bitfinex', 'kucoin', 'huobi']]
        print(f"  主流交易所: {', '.join([e['id'] for e in majors])}")
        results['exchange_list'] = data
    
    time.sleep(RATE_LIMIT_SLEEP)
    
    # 4.3 单个交易所详情
    subsection("4.3 /exchanges/{id} - 交易所详情")
    for ex_id in ["binance", "okx", "coinbase"]:
        data, code = cg_get(f"/exchanges/{ex_id}")
        if data:
            print(f"  {data.get('name', ex_id)}:")
            print(f"    排名: #{data.get('trust_score_rank', 'N/A')}")
            print(f"    国家: {data.get('country', 'N/A')}")
            print(f"    建立: {data.get('year_established', 'N/A')}")
            print(f"    24h量: {data.get('trade_volume_24h_btc', 0):,.0f} BTC")
            results[f'{ex_id}_detail'] = data
        time.sleep(RATE_LIMIT_SLEEP)
    
    # 4.4 衍生品交易所
    subsection("4.4 /derivatives/exchanges - 衍生品交易所")
    data, code = cg_get("/derivatives/exchanges", {"order": "open_interest_btc_desc", "per_page": 10})
    if data:
        rows = []
        for ex in data:
            rows.append({
                "交易所": ex.get("name", ""),
                "未平仓量(BTC)": ex.get("open_interest_btc", 0),
                "24h量(BTC)": ex.get("trade_volume_24h_btc", 0),
                "币种数": ex.get("number_of_perpetual_pairs", 0),
                "网址": ex.get("url", ""),
            })
        df_der = pd.DataFrame(rows)
        print(df_der.to_string(index=False))
        results['derivatives_exchanges'] = df_der
        save_csv(df_der, "coingecko_derivatives_exchanges")
    
    time.sleep(RATE_LIMIT_SLEEP)
    
    # 4.5 衍生品Tickers
    subsection("4.5 /derivatives - 衍生品Tickers")
    data, code = cg_get("/derivatives", {"include_tickers": "all", "order": "open_interest_btc_desc", "per_page": 10})
    if data:
        rows = []
        for d in data[:10]:
            rows.append({
                "交易所": d.get("market", ""),
                "交易对": d.get("symbol", ""),
                "价格": d.get("last", 0),
                "24h变化(%)": d.get("price_change_percentage_24h", 0),
                "未平仓量": d.get("open_interest", 0),
                "资金费率": d.get("funding_rate", 0),
            })
        if rows:
            df_dert = pd.DataFrame(rows)
            print(df_dert.to_string(index=False))
            results['derivatives_tickers'] = df_dert
    
    time.sleep(RATE_LIMIT_SLEEP)
    
    return results

# ============================================================
# 五、全局数据 API
# ============================================================
def test_global():
    section("五、全局数据 API")
    results = {}
    
    # 5.1 全球加密市场数据
    subsection("5.1 /global - 全球加密市场概览")
    data, code = cg_get("/global")
    if data:
        gd = data.get("data", data)
        
        # 提取关键指标
        info = {
            "活跃币种": gd.get("active_cryptocurrencies", "N/A"),
            "总市值(USD)": gd.get("total_market_cap", {}).get("usd", 0),
            "24h交易量(USD)": gd.get("total_volume", {}).get("usd", 0),
            "BTC占比(%)": gd.get("market_cap_percentage", {}).get("btc", 0),
            "ETH占比(%)": gd.get("market_cap_percentage", {}).get("eth", 0),
            "BTC/ETH市值比": gd.get("market_cap_percentage", {}).get("btc", 0) / max(gd.get("market_cap_percentage", {}).get("eth", 1), 1),
            "交易所数量": gd.get("active_exchanges", "N/A"),
            "BTC24h量占比(%)": gd.get("volume_percentage", {}).get("btc", 0),
            "ETH24h量占比(%)": gd.get("volume_percentage", {}).get("eth", 0),
        }
        
        for k, v in info.items():
            if isinstance(v, (int, float)) and v > 1e6:
                print(f"  ✅ {k}: ${v:,.0f}")
            else:
                print(f"  ✅ {k}: {v}")
        
        results['global'] = info
        
        # 导出
        df_global = pd.DataFrame([info])
        save_csv(df_global, "coingecko_global_data")
    
    time.sleep(RATE_LIMIT_SLEEP)
    
    # 5.2 DeFi数据
    subsection("5.2 /global/decentralized_finance_defi - DeFi市场")
    data, code = cg_get("/global/decentralized_finance_defi")
    if data:
        dd = data.get("data", data)
        defi_info = {
            "DeFi市值(USD)": dd.get("defi_market_cap", ""),
            "ETH占比(%)": dd.get("eth_market_cap_percentage", ""),
            "DeFi占比(%)": dd.get("defi_percentage_of_global_market_cap", ""),
            "DeFi24h量(USD)": dd.get("defi_24h_volume", ""),
            "DeFi币数": dd.get("defi_coin_count", ""),
        }
        for k, v in defi_info.items():
            try:
                fv = float(v)
                print(f"  ✅ {k}: {'${:,.0f}'.format(fv) if fv > 1000 else fv}")
            except:
                print(f"  ✅ {k}: {v}")
        results['defi'] = defi_info
    
    time.sleep(RATE_LIMIT_SLEEP)
    
    return results

# ============================================================
# 六、资产平台 & 汇率 & 搜索
# ============================================================
def test_general():
    section("六、通用数据 API")
    results = {}
    
    # 6.1 资产平台 (区块链网络)
    subsection("6.1 /asset_platforms - 区块链网络列表")
    data, code = cg_get("/asset_platforms")
    if data:
        rows = []
        for p in data[:20]:
            rows.append({
                "网络": p.get("name", ""),
                "简称": p.get("shortname", ""),
                "链ID": p.get("chain_identifier", ""),
            })
        print(f"  ✅ 共 {len(data)} 个区块链网络")
        print(f"  Top 20:")
        for r in rows:
            print(f"    {r['网络']:20s} {r['简称']:10s} {str(r['链ID']):5s}")
        results['asset_platforms'] = data
    
    time.sleep(RATE_LIMIT_SLEEP)
    
    # 6.2 汇率
    subsection("6.2 /exchange_rates - BTC汇率")
    data, code = cg_get("/exchange_rates")
    if data:
        rates = data.get("rates", {})
        majors = ["btc", "eth", "usd", "cny", "eur", "gbp", "jpy", "krw"]
        print("  BTC 兑主要货币汇率:")
        for curr in majors:
            if curr in rates:
                r = rates[curr]
                print(f"    1 BTC = {r['value']:>12,.4f} {r['name']:20s}")
        results['exchange_rates'] = rates
    
    time.sleep(RATE_LIMIT_SLEEP)
    
    # 6.3 搜索
    subsection("6.3 /search - 搜索功能")
    for query in ["bitcoin", "solana", "defi"]:
        data, code = cg_get("/search", {"query": query})
        if data:
            coins = data.get("coins", [])[:3]
            print(f"  搜索 '{query}': 找到 {len(data.get('coins', []))} 个币种, "
                  f"{len(data.get('exchanges', []))} 个交易所, "
                  f"{len(data.get('categories', []))} 个分类")
            for c in coins:
                print(f"    ▶ {c.get('name', '')} ({c.get('symbol', '')}) - #{c.get('market_cap_rank', '?')}")
        time.sleep(RATE_LIMIT_SLEEP)
    
    # 6.4 热门搜索
    subsection("6.4 /search/trending - 热门趋势")
    data, code = cg_get("/search/trending")
    if data:
        coins = data.get("coins", [])[:10]
        nfts = data.get("nfts", [])[:3]
        categories = data.get("categories", [])[:3]
        print(f"  🔥 热门币种 Top 10:")
        for i, c in enumerate(coins, 1):
            item = c.get("item", c)
            name = item.get("name", "")
            sym = item.get("symbol", "")
            rank = item.get("market_cap_rank", "")
            score = item.get("score", 0)
            print(f"    {i:2d}. {name:20s} ({sym:8s}) #{rank}  热度分: {item.get('web_slug_24h_rank_total', score)}")
        results['trending'] = data
    
    time.sleep(RATE_LIMIT_SLEEP)
    
    return results

# ============================================================
# 七、NFT API
# ============================================================
def test_nfts():
    section("七、NFT API")
    results = {}
    
    # 7.1 NFT列表
    subsection("7.1 /nfts/list - NFT集合列表")
    data, code = cg_get("/nfts/list", {"per_page": 10, "page": 1})
    if data:
        rows = []
        for n in data[:10]:
            rows.append({
                "名称": n.get("name", ""),
                "符号": n.get("symbol", ""),
                "平台": n.get("asset_platform_id", ""),
                "合约地址": str(n.get("contract_address", ""))[:20],
            })
        print(f"  ✅ 首批10个NFT集合:")
        for r in rows:
            print(f"    {r['名称']:25s} {r['符号']:10s} {r['平台']:15s}")
        results['nft_list'] = data[:10]
        if rows:
            save_csv(pd.DataFrame(rows), "coingecko_nft_list")
    
    time.sleep(RATE_LIMIT_SLEEP)
    
    # 7.2 指定NFT详情
    subsection("7.2 /nfts/{id} - NFT集合详情")
    for nft_id in ["bored-ape-yacht-club", "cryptopunks"]:
        data, code = cg_get(f"/nfts/{nft_id}")
        if data:
            print(f"  {data.get('name', nft_id)}:")
            print(f"    地板价: {data.get('floor_price', {}).get('usd', 'N/A')} USD")
            print(f"    24h量:  {data.get('volume_24h', {}).get('usd', 'N/A')} USD")
            print(f"    总供应: {data.get('total_supply', 'N/A')}")
            print(f"    收藏家: {data.get('number_of_unique_addresses', 'N/A')}")
            results[f'nft_{nft_id}'] = data
        time.sleep(RATE_LIMIT_SLEEP)
    
    return results

# ============================================================
# 八、公开持仓 API
# ============================================================
def test_treasuries():
    section("八、公开持仓 API")
    results = {}
    
    # 8.1 实体列表
    subsection("8.1 /entities/list - 实体列表")
    data, code = cg_get("/entities/list")
    if data:
        print(f"  ✅ 共 {len(data)} 个实体")
        examples = [e for e in data[:5]]
        for e in examples:
            print(f"    {e.get('id', ''):20s} {e.get('name', ''):25s} {e.get('country', ''):15s}")
    
    time.sleep(RATE_LIMIT_SLEEP)
    
    # 8.2 上市公司BTC持仓
    subsection("8.2 上市公司及政府BTC持仓")
    for coin_id in ["bitcoin", "ethereum"]:
        data, code = cg_get(f"/companies/public_treasury/{coin_id}")
        if data:
            companies = data.get("companies", [])
            total = data.get("total_holdings", 0)
            total_value = data.get("total_value_usd", 0)
            print(f"  {coin_id.upper()} 公开持仓:")
            print(f"    公司数: {len(companies)}")
            print(f"    总持仓: {total:,.2f} {coin_id[:3].upper()}")
            print(f"    总价值: ${total_value:,.0f}")
            for c in companies[:5]:
                print(f"    - {c.get('name', ''):25s} {c.get('total_holding', 0):>8,.0f} {coin_id[:3].upper()}")
            results[f'{coin_id}_treasury'] = data
        time.sleep(RATE_LIMIT_SLEEP)
    
    return results

# ============================================================
# CSV导出
# ============================================================
def save_csv(df, name):
    """保存DataFrame到CSV"""
    path = os.path.join(DATA_DIR, f"{name}_{TS_NOW}.csv")
    df.to_csv(path, index=False, encoding='utf-8-sig')
    print(f"    💾 已保存: {os.path.basename(path)}")

# ============================================================
# 九、技术分析 + 可视化
# ============================================================
def technical_analysis(results_coins):
    section("九、技术分析与可视化")
    
    btc_ohlc = results_coins.get("btc_ohlc")
    eth_ohlc = results_coins.get("eth_ohlc")
    if btc_ohlc is None:
        print("  ❌ 缺少OHLC数据, 跳过可视化")
        return
    
    df = btc_ohlc.copy()
    
    # 计算技术指标
    df['MA10'] = df['close'].rolling(10).mean()
    df['MA30'] = df['close'].rolling(30).mean()
    df['MA60'] = df['close'].rolling(60).mean() if len(df) >= 60 else None
    
    # MACD
    ema12 = df['close'].ewm(span=12).mean()
    ema26 = df['close'].ewm(span=26).mean()
    df['MACD'] = ema12 - ema26
    df['MACD_Signal'] = df['MACD'].ewm(span=9).mean()
    df['MACD_Hist'] = df['MACD'] - df['MACD_Signal']
    
    # RSI (14)
    delta = df['close'].diff()
    gain = delta.where(delta > 0, 0).rolling(14).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(14).mean()
    rs = gain / loss
    df['RSI14'] = 100 - (100 / (1 + rs))
    
    # 布林带 (20,2)
    df['BOLL_MID'] = df['close'].rolling(20).mean()
    std20 = df['close'].rolling(20).std()
    df['BOLL_UP'] = df['BOLL_MID'] + 2 * std20
    df['BOLL_DN'] = df['BOLL_MID'] - 2 * std20
    
    # 金叉死叉信号
    df['Signal'] = '持有'
    df.loc[(df['MA10'] > df['MA30']) & (df['MA10'].shift(1) <= df['MA30'].shift(1)), 'Signal'] = '🟢 金叉'
    df.loc[(df['MA10'] < df['MA30']) & (df['MA10'].shift(1) >= df['MA30'].shift(1)), 'Signal'] = '🔴 死叉'
    
    # 当前状态
    current = df.iloc[-1]
    print(f"\n  📊 BTC/USD 当前技术状态 ({df.index[-1].strftime('%Y-%m-%d %H:%M')})")
    print(f"     价格: ${current['close']:,.2f}")
    print(f"     MA10: ${current['MA10']:,.2f}  MA30: ${current['MA30']:,.2f}")
    print(f"     MACD: {current['MACD']:+.0f}  Signal: {current['MACD_Signal']:+.0f}")
    print(f"     RSI:  {current['RSI14']:.1f}")
    print(f"     信号: {current['Signal']}")
    
    # 信号统计
    signals = df[df['Signal'] != '持有']
    print(f"\n  信号统计:")
    print(f"    金叉次数: {len(signals[signals['Signal'] == '🟢 金叉'])}")
    print(f"    死叉次数: {len(signals[signals['Signal'] == '🔴 死叉'])}")
    
    # 导出技术分析数据
    save_csv(df, "coingecko_btc_technical_analysis")
    
    # ===== 生成图表 =====
    
    # 图1: BTC价格 + 均线 + 金叉死叉
    print("\n  生成图1: BTC价格走势+均线信号...")
    fig, ax = plt.subplots(figsize=(14, 7))
    
    ax.plot(df.index, df['close'], label='BTC/USD', color='#f7931a', linewidth=1.8)
    ax.plot(df.index, df['MA10'], label='MA10', color='#2196F3', linewidth=1, alpha=0.8)
    ax.plot(df.index, df['MA30'], label='MA30', color='#FF9800', linewidth=1, alpha=0.8)
    
    if df['MA60'] is not None:
        ax.plot(df.index, df['MA60'], label='MA60', color='#9C27B0', linewidth=1, alpha=0.7)
    
    # 布林带
    ax.fill_between(df.index, df['BOLL_UP'], df['BOLL_DN'], alpha=0.1, color='gray', label='布林带(20,2)')
    
    # 金叉(红三角) 死叉(绿倒三角)
    golden = df[df['Signal'] == '🟢 金叉']
    death = df[df['Signal'] == '🔴 死叉']
    ax.scatter(golden.index, golden['close'], color='red', marker='^', s=130, zorder=5,
               label='金叉', edgecolors='black', linewidths=0.5)
    ax.scatter(death.index, death['close'], color='lime', marker='v', s=130, zorder=5,
               label='死叉', edgecolors='black', linewidths=0.5)
    
    ax.set_title('BTC/USD CoinGecko OHLC价格走势 + 技术指标', fontproperties=cf, fontsize=14)
    ax.set_xlabel('日期', fontproperties=cf)
    ax.set_ylabel('价格 (USD)', fontproperties=cf)
    ax.legend(prop=cf, loc='upper left')
    ax.grid(True, alpha=0.3)
    fig.autofmt_xdate()
    
    path1 = os.path.join(PLOTS_DIR, f'btc_price_signals_{TS_NOW}.png')
    plt.tight_layout()
    plt.savefig(path1, dpi=120, bbox_inches='tight')
    plt.close()
    print(f"    💾 -> {path1}")
    
    # 图2: MACD
    print("  生成图2: BTC MACD...")
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(14, 8), gridspec_kw={'height_ratios': [2.5, 1]})
    
    ax1.plot(df.index, df['close'], color='#f7931a', linewidth=1.5)
    ax1.set_title(f'BTC/USD 价格', fontproperties=cf)
    ax1.set_ylabel('价格 (USD)', fontproperties=cf)
    ax1.grid(True, alpha=0.3)
    
    colors = ['#4CAF50' if v >= 0 else '#f44336' for v in df['MACD_Hist']]
    ax2.bar(df.index, df['MACD_Hist'], color=colors, width=0.6, alpha=0.7, label='柱状图')
    ax2.plot(df.index, df['MACD'], color='#2196F3', linewidth=1.2, label='MACD')
    ax2.plot(df.index, df['MACD_Signal'], color='#FF9800', linewidth=1.2, label='Signal')
    ax2.axhline(y=0, color='gray', linestyle='--', linewidth=0.5)
    ax2.set_title(f'MACD (12, 26, 9)', fontproperties=cf)
    ax2.set_ylabel('MACD', fontproperties=cf)
    ax2.legend(prop=cf)
    ax2.grid(True, alpha=0.3)
    
    fig.autofmt_xdate()
    path2 = os.path.join(PLOTS_DIR, f'btc_macd_{TS_NOW}.png')
    plt.tight_layout()
    plt.savefig(path2, dpi=120, bbox_inches='tight')
    plt.close()
    print(f"    💾 -> {path2}")
    
    # 图3: RSI + 布林带
    print("  生成图3: BTC RSI+布林带...")
    fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(14, 10), gridspec_kw={'height_ratios': [2.5, 1, 1]})
    
    ax1.plot(df.index, df['close'], color='#f7931a', linewidth=1.5)
    ax1.plot(df.index, df['BOLL_UP'], color='gray', linewidth=0.8, linestyle='--', alpha=0.6)
    ax1.plot(df.index, df['BOLL_MID'], color='purple', linewidth=0.8, linestyle='--', alpha=0.4)
    ax1.plot(df.index, df['BOLL_DN'], color='gray', linewidth=0.8, linestyle='--', alpha=0.6)
    ax1.fill_between(df.index, df['BOLL_UP'], df['BOLL_DN'], alpha=0.08, color='gray')
    ax1.set_title(f'BTC/USD 布林带(20,2)', fontproperties=cf)
    ax1.set_ylabel('价格 (USD)', fontproperties=cf)
    ax1.grid(True, alpha=0.3)
    
    ax2.plot(df.index, df['RSI14'], color='#9C27B0', linewidth=1.5)
    ax2.axhline(y=70, color='red', linestyle='--', alpha=0.5, label='超买(70)')
    ax2.axhline(y=30, color='green', linestyle='--', alpha=0.5, label='超卖(30)')
    ax2.axhline(y=50, color='gray', linestyle='--', alpha=0.3)
    ax2.fill_between(df.index, 30, 70, alpha=0.08, color='gray')
    ax2.set_title(f'RSI(14)', fontproperties=cf)
    ax2.set_ylabel('RSI', fontproperties=cf)
    ax2.set_ylim(0, 100)
    ax2.legend(prop=cf, loc='upper left')
    ax2.grid(True, alpha=0.3)
    
    # 成交量
    ax3.bar(df.index, df['close'] * 0.1, color='#607D8B', alpha=0.5, label='相对成交量')
    ax3.set_title(f'成交量 (相对)', fontproperties=cf)
    ax3.set_ylabel('量', fontproperties=cf)
    ax3.set_xlabel('日期', fontproperties=cf)
    ax3.grid(True, alpha=0.3)
    
    fig.autofmt_xdate()
    path3 = os.path.join(PLOTS_DIR, f'btc_rsi_bollinger_{TS_NOW}.png')
    plt.tight_layout()
    plt.savefig(path3, dpi=120, bbox_inches='tight')
    plt.close()
    print(f"    💾 -> {path3}")
    
    # 图4: BTC vs ETH 走势对比 (如果ETH数据存在)
    print("  生成图4: BTC vs ETH 走势对比...")
    if eth_ohlc is not None:
        df_btc_norm = df[['close']].copy()
        df_eth_norm = eth_ohlc[['close']].copy()
        df_eth_norm.columns = ['ETH']
        df_btc_norm.columns = ['BTC']
        
        # 合并并对齐索引
        df_compare = pd.concat([df_btc_norm, df_eth_norm], axis=1).dropna()
        df_norm = df_compare.div(df_compare.iloc[0]) * 100
        
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(14, 8), gridspec_kw={'height_ratios': [1.5, 1]})
        
        ax1.plot(df_compare.index, df_compare['BTC'], color='#f7931a', linewidth=1.5, label='BTC')
        ax1.plot(df_compare.index, df_compare['ETH'], color='#627eea', linewidth=1.5, label='ETH')
        ax1.set_title('BTC vs ETH 价格走势', fontproperties=cf, fontsize=13)
        ax1.set_ylabel('价格 (USD)', fontproperties=cf)
        ax1.legend(prop=cf)
        ax1.grid(True, alpha=0.3)
        
        # ETH/BTC比率
        ax2.plot(df_compare.index, df_compare['ETH'] / df_compare['BTC'], color='#4CAF50', linewidth=1.5)
        ax2.set_title('ETH/BTC 汇率', fontproperties=cf, fontsize=13)
        ax2.set_ylabel('ETH/BTC', fontproperties=cf)
        ax2.set_xlabel('日期', fontproperties=cf)
        ax2.grid(True, alpha=0.3)
        
        fig.autofmt_xdate()
        path4 = os.path.join(PLOTS_DIR, f'btc_eth_compare_{TS_NOW}.png')
        plt.tight_layout()
        plt.savefig(path4, dpi=120, bbox_inches='tight')
        plt.close()
        print(f"    💾 -> {path4}")
    
    print(f"\n  ✅ 所有图表已保存到: {PLOTS_DIR}/")

# ============================================================
# 主流程
# ============================================================
if __name__ == '__main__':
    print(f"""
╔══════════════════════════════════════════════════════════════╗
║        CoinGecko API 数字货币数据接口完全测试               ║
║        数据源: CoinGecko Demo API (免费, 无需API Key)       ║
╚══════════════════════════════════════════════════════════════╝
运行时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
API基础: {API_BASE}
速率限制: 每请求间隔 {RATE_LIMIT_SLEEP}s
""")
    
    print("\n⚠  由于免费API限频(10-30次/分钟), 全程约需3-4分钟...\n")
    
    test_start = time.time()
    all_results = {}
    
    try:
        all_results['ping'] = test_ping()
        time.sleep(RATE_LIMIT_SLEEP)
    except Exception as e:
        print(f"  ❌ 系统状态测试失败: {e}")
    
    try:
        all_results['simple'] = test_simple_price()
    except Exception as e:
        print(f"  ❌ 简单价格测试失败: {e}")
    
    try:
        all_results['coins'] = test_coins_data()
    except Exception as e:
        print(f"  ❌ Coins数据测试失败: {e}")
    
    try:
        all_results['exchanges'] = test_exchanges()
    except Exception as e:
        print(f"  ❌ 交易所测试失败: {e}")
    
    try:
        all_results['global'] = test_global()
    except Exception as e:
        print(f"  ❌ 全局数据测试失败: {e}")
    
    try:
        all_results['general'] = test_general()
    except Exception as e:
        print(f"  ❌ 通用数据测试失败: {e}")
    
    try:
        all_results['nfts'] = test_nfts()
    except Exception as e:
        print(f"  ❌ NFT测试失败: {e}")
    
    try:
        all_results['treasuries'] = test_treasuries()
    except Exception as e:
        print(f"  ❌ 公开持仓测试失败: {e}")
    
    # 技术分析
    coins_data = all_results.get('coins', {})
    technical_analysis(coins_data)
    
    elapsed = time.time() - test_start
    
    # ===== 总结 =====
    print(f"""
╔══════════════════════════════════════════════════════════════╗
║                    测试完成总结                               ║
╚══════════════════════════════════════════════════════════════╝""")
    
    categories_tested = {
        "系统状态": all_results.get('ping', {}).get('ping', False),
        "简单价格": 'simple' in all_results,
        "币种数据+OHLC": 'coins' in all_results,
        "交易所+衍生品": 'exchanges' in all_results,
        "全局+DeFi": 'global' in all_results,
        "平台+汇率+搜索": 'general' in all_results,
        "NFT": 'nfts' in all_results,
        "公开持仓": 'treasuries' in all_results,
        "技术分析+可视化": 'btc_ohlc' in all_results.get('coins', {}),
    }
    
    for k, v in categories_tested.items():
        print(f"  {'✅' if v else '❌'} {k}")
    
    print(f"""
⏱  总耗时: {elapsed:.0f} 秒
📂  CSV数据: {DATA_DIR}/
📊  图表:     {PLOTS_DIR}/
🌐  API文档:  https://docs.coingecko.com/v3.0.1/reference/endpoint-overview

CoinGecko免费API特点:
  1. ✅ 完全免费, 无需要API Key
  2. ✅ 17405+ 币种, 覆盖最广
  3. ✅ 支持OHLCV/市值/交易量/全局数据
  4. ✅ 交易所/衍生品/NFT/公开持仓
  5. ✅ 无需VPN也可用 (国内直接访问)
  6. ⚠  限频 ~10-30次/分钟 (免费层)
  
与AkShare crypto对比:
  AkShare: 仅3个接口 (crypto_js_spot/持仓报告/CME)
  CoinGecko: 30+ 端点, 涵盖全部数据维度
""")
