#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
OHLCV 数据管道 - 双源融合 (OKX + CoinGecko)
============================================
为量化交易系统构建稳定的 OHLCV 数据基础。

数据源:
  1. OKX (CCXT库) — 高频实时OHLCV，1m/5m/1h/4h/1d，3976个交易对
  2. CoinGecko API — 长周期历史OHLCV，17405个币种，聚合多交易所

融合策略:
  - CoinGecko 提供长历史 (>90天日K)
  - OKX 提供近期高精度数据
  - 双源交叉验证数据一致性

阶段: 9.1 — 量化数据基础设施
"""
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
from datetime import datetime, timedelta
import os, sys, time, json, sqlite3

# ===== 配置 =====
FONT_PATH = '/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc'
BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE, 'output', 'data', 'crypto')
PLOTS_DIR = os.path.join(BASE, 'output', 'plots', 'crypto')
os.makedirs(DATA_DIR, exist_ok=True)
os.makedirs(PLOTS_DIR, exist_ok=True)

TS = datetime.now().strftime("%Y%m%d_%H%M%S")
COINS = ['BTC/USDT', 'ETH/USDT', 'SOL/USDT', 'XRP/USDT', 'DOGE/USDT']

# 中文字体
try:
    cf = fm.FontProperties(fname=FONT_PATH, size=12)
    plt.rcParams['font.family'] = 'Noto Sans CJK JP'
except:
    cf = None

# ============================================================
# 数据源1: OKX (CCXT)
# ============================================================
class OKXSource:
    """OKX交易所数据源"""
    def __init__(self):
        import ccxt
        self.ex = ccxt.okx({"enableRateLimit": True, "timeout": 15000})
        self.name = "OKX"
    
    def fetch_ohlcv(self, symbol, timeframe='1d', limit=100):
        """获取OHLCV数据"""
        ohlcv = self.ex.fetch_ohlcv(symbol, timeframe, limit=limit)
        df = pd.DataFrame(ohlcv, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
        df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
        df.set_index('timestamp', inplace=True)
        df['source'] = 'OKX'
        return df

    def fetch_multi_timeframe(self, symbol):
        """同时获取多个时间周期的K线"""
        result = {}
        for tf in ['1h', '4h', '1d']:
            limits = {'1h': 120, '4h': 120, '1d': 365}
            try:
                df = self.fetch_ohlcv(symbol, tf, limit=limits[tf])
                result[tf] = df
                print(f"    OKX {symbol} {tf}: {len(df)} 条")
            except Exception as e:
                print(f"    OKX {symbol} {tf}: ❌ {str(e)[:50]}")
            time.sleep(1)
        return result

# ============================================================
# 数据源2: CoinGecko
# ============================================================
class CoinGeckoSource:
    """CoinGecko数据源"""
    def __init__(self, sleep=2.5):
        import requests
        self.r = requests
        self.sleep = sleep
        self.name = "CoinGecko"
    
    def fetch_ohlcv(self, coin_id='bitcoin', vs_currency='usd', days=90):
        """获取OHLCV数据"""
        url = f"https://api.coingecko.com/api/v3/coins/{coin_id}/ohlc"
        params = {"vs_currency": vs_currency, "days": days}
        resp = self.r.get(url, params=params, timeout=15)
        resp.raise_for_status()
        data = resp.json()
        df = pd.DataFrame(data, columns=['timestamp', 'open', 'high', 'low', 'close'])
        df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
        df.set_index('timestamp', inplace=True)
        df['source'] = 'CoinGecko'
        time.sleep(self.sleep)  # 限频
        return df

    def fetch_market_chart(self, coin_id='bitcoin', vs_currency='usd', days=90):
        """获取市场图表数据（价格+市值+量）"""
        url = f"https://api.coingecko.com/api/v3/coins/{coin_id}/market_chart"
        params = {"vs_currency": vs_currency, "days": days}
        resp = self.r.get(url, params=params, timeout=15)
        resp.raise_for_status()
        data = resp.json()
        
        prices = pd.DataFrame(data['prices'], columns=['timestamp', 'price'])
        prices['timestamp'] = pd.to_datetime(prices['timestamp'], unit='ms')
        prices.set_index('timestamp', inplace=True)
        
        volumes = pd.DataFrame(data['total_volumes'], columns=['timestamp', 'volume'])
        volumes['timestamp'] = pd.to_datetime(volumes['timestamp'], unit='ms')
        volumes.set_index('timestamp', inplace=True)
        
        time.sleep(self.sleep)
        return prices, volumes

    def coin_id_map(self):
        """币种ID映射表（BTC/USDT → bitcoin）"""
        return {
            'BTC/USDT': 'bitcoin',
            'ETH/USDT': 'ethereum',
            'SOL/USDT': 'solana',
            'XRP/USDT': 'ripple',
            'DOGE/USDT': 'dogecoin',
            'BNB/USDT': 'binancecoin',
            'ADA/USDT': 'cardano',
            'AVAX/USDT': 'avalanche-2',
            'DOT/USDT': 'polkadot',
            'LINK/USDT': 'chainlink',
        }

# ============================================================
# 管道核心: 数据融合
# ============================================================
def align_and_merge(df_okx, df_cg):
    """对齐并合并两个数据源的OHLCV数据"""
    if df_okx.empty or df_cg.empty:
        return None
    
    # 标准化列名
    okx = df_okx[['open', 'high', 'low', 'close', 'volume']].copy()
    cg = df_cg[['open', 'high', 'low', 'close']].copy()
    
    # 对齐到日期（去除时间部分）
    okx.index = okx.index.normalize()
    cg.index = cg.index.normalize()
    
    # 合并: OKX为主, CoinGecko补充
    merged = pd.concat([
        okx.add_suffix('_okx'),
        cg.add_suffix('_cg')
    ], axis=1)
    
    # 去重（相同日期的取OKX）
    merged = merged[~merged.index.duplicated(keep='first')]
    merged = merged.sort_index()
    
    # 差异分析
    overlap = merged.dropna()
    if len(overlap) > 0:
        merged['close_diff_pct'] = abs(overlap['close_okx'] - overlap['close_cg']) / overlap['close_cg'] * 100
    
    return merged

def build_unified_dataset(symbol, okx, cg, coin_id, days=90):
    """构建统一OHLCV数据集"""
    print(f"\n  {'='*50}")
    print(f"  {symbol} 数据融合")
    print(f"  {'='*50}")
    
    # OKX日K
    df_okx = okx.fetch_ohlcv(symbol, '1d', limit=min(days, 365))
    print(f"  OKX: {len(df_okx)} 条 ({df_okx.index[0].strftime('%Y-%m-%d')} ~ {df_okx.index[-1].strftime('%Y-%m-%d')})")
    
    # CoinGecko OHLCV
    df_cg = cg.fetch_ohlcv(coin_id, 'usd', days)
    print(f"  CG:  {len(df_cg)} 条 ({df_cg.index[0].strftime('%Y-%m-%d')} ~ {df_cg.index[-1].strftime('%Y-%m-%d')})")
    
    # 对齐合并
    merged = align_and_merge(df_okx, df_cg)
    
    if merged is not None:
        overlap_count = merged['close_okx'].notna().sum()
        cg_only = merged['close_cg'].notna().sum() - merged['close_okx'].notna().sum() if merged['close_cg'].notna().sum() > merged['close_okx'].notna().sum() else 0
        print(f"  {'='*50}")
        print(f"  融合结果:")
        print(f"    OKX数据天数: {merged['close_okx'].notna().sum()}")
        print(f"    CoinGecko仅天数: {cg_only}")
        print(f"    重叠天数: {merged['close_okx'].notna().sum()}")
        
        if 'close_diff_pct' in merged.columns and merged['close_diff_pct'].notna().sum() > 0:
            avg_diff = merged['close_diff_pct'].mean()
            print(f"    收盘价平均差异: {avg_diff:.2f}%")
    
    return merged, df_okx, df_cg

# ============================================================
# 技术分析 (多时间周期)
# ============================================================
def compute_indicators(df, prefix=''):
    """计算技术指标"""
    if df is None or len(df) < 20:
        return df
    
    close = df['close'] if 'close' in df.columns else df['close_okx']
    prefix = prefix + '_' if prefix else ''
    
    # 均线
    df[f'{prefix}MA10'] = close.rolling(10).mean()
    df[f'{prefix}MA30'] = close.rolling(30).mean()
    df[f'{prefix}MA60'] = close.rolling(60).mean() if len(df) >= 60 else float('nan')
    
    # MACD
    ema12 = close.ewm(span=12).mean()
    ema26 = close.ewm(span=26).mean()
    df[f'{prefix}MACD'] = ema12 - ema26
    df[f'{prefix}MACD_Signal'] = df[f'{prefix}MACD'].ewm(span=9).mean()
    df[f'{prefix}MACD_Hist'] = df[f'{prefix}MACD'] - df[f'{prefix}MACD_Signal']
    
    # RSI
    delta = close.diff()
    gain = delta.where(delta > 0, 0).rolling(14).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(14).mean()
    rs = gain / loss
    df[f'{prefix}RSI14'] = 100 - (100 / (1 + rs))
    
    # 布林带
    mid = close.rolling(20).mean()
    std = close.rolling(20).std()
    df[f'{prefix}BOLL_UP'] = mid + 2 * std
    df[f'{prefix}BOLL_MID'] = mid
    df[f'{prefix}BOLL_DN'] = mid - 2 * std
    
    # 金叉死叉信号
    if f'{prefix}MA10' in df.columns and f'{prefix}MA30' in df.columns:
        ma10 = df[f'{prefix}MA10']
        ma30 = df[f'{prefix}MA30']
        df[f'{prefix}Signal'] = '持有'
        df.loc[(ma10 > ma30) & (ma10.shift(1) <= ma30.shift(1)), f'{prefix}Signal'] = '金叉'
        df.loc[(ma10 < ma30) & (ma10.shift(1) >= ma30.shift(1)), f'{prefix}Signal'] = '死叉'
    
    # ATR (波动率)
    high_low = df['high'] - df['low']
    high_close = (df['high'] - df['close'].shift(1)).abs()
    low_close = (df['low'] - df['close'].shift(1)).abs()
    tr = pd.concat([high_low, high_close, low_close], axis=1).max(axis=1)
    df[f'{prefix}ATR14'] = tr.rolling(14).mean()
    
    return df

# ============================================================
# 可视化
# ============================================================
def visualize_pipeline(symbol, merged, df_okx, df_okx_1h, df_okx_4h, df_cg):
    """生成数据管道可视化"""
    ts = TS
    
    # --- 图1: 双源数据对比 ---
    print("\n  生成图1: 双源OHLCV数据对比...")
    fig, axes = plt.subplots(3, 1, figsize=(14, 10))
    
    if merged is not None and 'close_okx' in merged.columns and 'close_cg' in merged.columns:
        ax = axes[0]
        ax.plot(merged.index, merged['close_okx'], color='#f7931a', linewidth=1.5, label='OKX', alpha=0.8)
        ax.plot(merged.index, merged['close_cg'], color='#2196F3', linewidth=1.5, label='CoinGecko', alpha=0.8, linestyle='--')
        ax.set_title(f'{symbol} 双源收盘价对比', fontproperties=cf)
        ax.legend(prop=cf)
        ax.grid(True, alpha=0.3)
        
        ax = axes[1]
        if 'close_diff_pct' in merged.columns:
            diff_valid = merged['close_diff_pct'].dropna()
            if len(diff_valid) > 0:
                ax.bar(diff_valid.index, diff_valid.values, color='#9C27B0', alpha=0.6, width=0.6)
                ax.axhline(y=diff_valid.mean(), color='red', linestyle='--', alpha=0.5, label=f'均值: {diff_valid.mean():.2f}%')
                ax.set_title('收盘价差异百分比 (OKX vs CoinGecko)', fontproperties=cf)
                ax.legend(prop=cf)
                ax.grid(True, alpha=0.3)
    
    # 多时间周期
    ax = axes[2]
    if df_okx_1h is not None and df_okx_4h is not None:
        # 归一化到100
        close_1h = df_okx_1h['close'].resample('1D').last().ffill() if len(df_okx_1h) > 0 else None
        close_4h = df_okx_4h['close'].resample('1D').last().ffill() if len(df_okx_4h) > 0 else None
        close_1d = df_okx['close'] if 'close' in df_okx.columns else None
        
        if close_1d is not None:
            base = close_1d.iloc[0]
            ax.plot(close_1d.index, close_1d / base * 100, label='1d', linewidth=2, color='#f7931a')
        if close_4h is not None:
            ax.plot(close_4h.index, close_4h / close_4h.iloc[0] * 100, label='4h', linewidth=1.2, alpha=0.7, color='#2196F3')
        if close_1h is not None:
            ax.plot(close_1h.index, close_1h / close_1h.iloc[0] * 100, label='1h', linewidth=0.8, alpha=0.5, color='#4CAF50')
        
        ax.set_title('多时间周期归一化对比 (基准=100)', fontproperties=cf)
        ax.legend(prop=cf)
        ax.grid(True, alpha=0.3)
    
    fig.autofmt_xdate()
    path1 = os.path.join(PLOTS_DIR, f'ohlcv_data_comparison_{ts}.png')
    plt.tight_layout()
    plt.savefig(path1, dpi=120, bbox_inches='tight')
    plt.close()
    print(f"    -> {path1}")
    
    # --- 图2: 技术分析全景 ---
    print("  生成图2: 技术分析全景...")
    if df_okx is not None and len(df_okx) > 20:
        df_ta = compute_indicators(df_okx.copy())
        
        fig = plt.figure(figsize=(14, 12))
        gs = fig.add_gridspec(4, 2, hspace=0.3, wspace=0.2)
        
        # 价格+均线+信号
        ax1 = fig.add_subplot(gs[0, :])
        ax1.plot(df_ta.index, df_ta['close'], color='#f7931a', linewidth=1.5, label='Close')
        ax1.plot(df_ta.index, df_ta['MA10'], color='#2196F3', linewidth=1, alpha=0.7, label='MA10')
        ax1.plot(df_ta.index, df_ta['MA30'], color='#FF9800', linewidth=1, alpha=0.7, label='MA30')
        ax1.fill_between(df_ta.index, df_ta['BOLL_UP'], df_ta['BOLL_DN'], alpha=0.08, color='gray')
        
        golden = df_ta[df_ta['Signal'] == '金叉']
        death = df_ta[df_ta['Signal'] == '死叉']
        if len(golden) > 0:
            ax1.scatter(golden.index, golden['close'], color='red', marker='^', s=100, zorder=5, edgecolors='black', linewidths=0.5)
        if len(death) > 0:
            ax1.scatter(death.index, death['close'], color='lime', marker='v', s=100, zorder=5, edgecolors='black', linewidths=0.5)
        
        ax1.set_title(f'{symbol} 价格+均线+布林带', fontproperties=cf)
        ax1.legend(prop=cf, loc='upper left')
        ax1.grid(True, alpha=0.3)
        
        # MACD
        ax2 = fig.add_subplot(gs[1, 0])
        colors = ['#4CAF50' if v >= 0 else '#f44336' for v in df_ta['MACD_Hist']]
        ax2.bar(df_ta.index, df_ta['MACD_Hist'], color=colors, width=0.6, alpha=0.6)
        ax2.plot(df_ta.index, df_ta['MACD'], color='#2196F3', linewidth=1, label='MACD')
        ax2.plot(df_ta.index, df_ta['MACD_Signal'], color='#FF9800', linewidth=1, label='Signal')
        ax2.axhline(y=0, color='gray', linestyle='--', linewidth=0.5)
        ax2.set_title('MACD (12,26,9)', fontproperties=cf)
        ax2.legend(prop=cf, fontsize=8)
        ax2.grid(True, alpha=0.3)
        
        # RSI
        ax3 = fig.add_subplot(gs[1, 1])
        ax3.plot(df_ta.index, df_ta['RSI14'], color='#9C27B0', linewidth=1.5)
        ax3.axhline(y=70, color='red', linestyle='--', alpha=0.4)
        ax3.axhline(y=30, color='green', linestyle='--', alpha=0.4)
        ax3.fill_between(df_ta.index, 30, 70, alpha=0.05, color='gray')
        ax3.set_title(f'RSI(14) 当前: {df_ta["RSI14"].iloc[-1]:.1f}', fontproperties=cf)
        ax3.set_ylim(0, 100)
        ax3.grid(True, alpha=0.3)
        
        # 布林带带宽
        ax4 = fig.add_subplot(gs[2, 0])
        bandwidth = (df_ta['BOLL_UP'] - df_ta['BOLL_DN']) / df_ta['BOLL_MID'] * 100
        ax4.fill_between(df_ta.index, bandwidth, alpha=0.3, color='purple')
        ax4.plot(df_ta.index, bandwidth, color='purple', linewidth=1)
        ax4.set_title('布林带带宽 (%)', fontproperties=cf)
        ax4.grid(True, alpha=0.3)
        
        # 成交量
        ax5 = fig.add_subplot(gs[2, 1])
        vol_colors = ['#4CAF50' if df_ta['close'].iloc[i] >= df_ta['close'].iloc[i-1] else '#f44336' for i in range(1, len(df_ta))]
        vol_colors.insert(0, '#4CAF50')
        ax5.bar(df_ta.index, df_ta['volume'], color=vol_colors, alpha=0.5, width=0.6)
        ax5.set_title('成交量', fontproperties=cf)
        ax5.grid(True, alpha=0.3)
        
        # 波动率 (ATR)
        ax6 = fig.add_subplot(gs[3, 0])
        ax6.plot(df_ta.index, df_ta['ATR14'], color='#FF5722', linewidth=1.5)
        ax6.set_title('ATR(14) 波动率', fontproperties=cf)
        ax6.grid(True, alpha=0.3)
        
        # 信号汇总
        ax7 = fig.add_subplot(gs[3, 1])
        last = df_ta.iloc[-1]
        summary_text = (
            f"当前状态 ({df_ta.index[-1].strftime('%m-%d %H:%M')})\n"
            f"{'='*20}\n"
            f"价格: ${last['close']:,.2f}\n"
            f"MA10: ${last['MA10']:,.2f}\n"
            f"MA30: ${last['MA30']:,.2f}\n"
            f"MACD: {last['MACD']:+.0f}\n"
            f"RSI:  {last['RSI14']:.1f}\n"
            f"ATR:  ${last['ATR14']:,.0f}\n"
            f"信号: {last['Signal']}\n"
        )
        ax7.text(0.1, 0.5, summary_text, transform=ax7.transAxes, fontsize=11,
                 fontproperties=cf, verticalalignment='center',
                 bbox=dict(boxstyle='round', facecolor='#f5f5f5'))
        ax7.axis('off')
        
        fig.autofmt_xdate()
        path2 = os.path.join(PLOTS_DIR, f'ohlcv_technical_analysis_{ts}.png')
        plt.tight_layout()
        plt.savefig(path2, dpi=120, bbox_inches='tight')
        plt.close()
        print(f"    -> {path2}")
    
    # --- 图3: 数据源质量对比 ---
    print("  生成图3: 数据源质量对比...")
    if df_cg is not None and df_okx is not None:
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(14, 8))
        
        # CG日K（长历史）
        ax1.plot(df_cg.index, df_cg['close'], color='#2196F3', linewidth=1, alpha=0.7, label=f'CoinGecko (days={days_param})')
        ax1.set_title(f'CoinGecko 长周期历史', fontproperties=cf)
        ax1.legend(prop=cf)
        ax1.grid(True, alpha=0.3)
        
        # OKX日K（近期高精度）
        ax2.plot(df_okx.index, df_okx['close'], color='#f7931a', linewidth=2, label=f'OKX ({len(df_okx)}条)')
        ax2.set_title(f'OKX 近期数据', fontproperties=cf)
        ax2.set_xlabel('日期', fontproperties=cf)
        ax2.legend(prop=cf)
        ax2.grid(True, alpha=0.3)
        
        fig.autofmt_xdate()
        path3 = os.path.join(PLOTS_DIR, f'ohlcv_source_comparison_{ts}.png')
        plt.tight_layout()
        plt.savefig(path3, dpi=120, bbox_inches='tight')
        plt.close()
        print(f"    -> {path3}")

# ============================================================
# 存储
# ============================================================
def save_to_csv(symbol, merged, df_okx, df_cg, df_1h, df_4h):
    """保存数据到CSV"""
    safe_sym = symbol.replace('/', '_')
    
    if merged is not None:
        path = os.path.join(DATA_DIR, f'ohlcv_merged_{safe_sym}_{TS}.csv')
        merged.to_csv(path, encoding='utf-8-sig')
        print(f"  OK 合并数据: {os.path.basename(path)}")
    
    if df_okx is not None:
        path = os.path.join(DATA_DIR, f'ohlcv_okx_{safe_sym}_1d_{TS}.csv')
        df_okx.to_csv(path, encoding='utf-8-sig')
        print(f"  OK OKX日K: {os.path.basename(path)}")
    
    if df_1h is not None and len(df_1h) > 0:
        path = os.path.join(DATA_DIR, f'ohlcv_okx_{safe_sym}_1h_{TS}.csv')
        df_1h.to_csv(path, encoding='utf-8-sig')
        print(f"  OK OKX1hK: {os.path.basename(path)}")
    
    if df_4h is not None and len(df_4h) > 0:
        path = os.path.join(DATA_DIR, f'ohlcv_okx_{safe_sym}_4h_{TS}.csv')
        df_4h.to_csv(path, encoding='utf-8-sig')
        print(f"  OK OKX4hK: {os.path.basename(path)}")
    
    if df_cg is not None:
        path = os.path.join(DATA_DIR, f'ohlcv_coingecko_{safe_sym}_{TS}.csv')
        df_cg.to_csv(path, encoding='utf-8-sig')
        print(f"  OK CoinGecko: {os.path.basename(path)}")

# ============================================================
# 主流程
# ============================================================
if __name__ == '__main__':
    global days_param  # for visualization
    days_param = 90
    
    print(f"""
╔═══════════════════════════════════════════════════════════════╗
║         OHLCV 数据管道 — 双源融合 (OKX + CoinGecko)          ║
║         阶段9.1 — 量化交易数据基础设施                        ║
╚═══════════════════════════════════════════════════════════════╝
时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
币种: {', '.join(COINS)}
历史深度: {days_param}天
""")
    
    start = time.time()
    
    # ===== 初始化数据源 =====
    print(f"\n{'='*55}")
    print("初始化数据源")
    print(f"{'='*55}")
    okx = OKXSource()
    cg = CoinGeckoSource(sleep=2.5)
    print("  OKX: 3,976交易对")
    print(f"  CoinGecko: {len(cg.coin_id_map())} 个币种映射")
    
    # ===== 多币种数据获取 + 融合 =====
    print(f"\n{'='*55}")
    print("多币种 OHLCV 数据获取")
    print(f"{'='*55}")
    
    all_merged = {}
    for symbol in COINS:
        coin_id = cg.coin_id_map().get(symbol)
        if not coin_id:
            print(f"\n  XX {symbol}: 无CoinGecko映射, 跳过")
            continue
        
        try:
            # 获取OKX多时间周期
            multi_tf = okx.fetch_multi_timeframe(symbol)
            df_okx_1d = multi_tf.get('1d')
            df_okx_1h = multi_tf.get('1h')
            df_okx_4h = multi_tf.get('4h')
            
            # 获取CoinGecko
            df_cg = cg.fetch_ohlcv(coin_id, 'usd', days_param)
            
            # 融合
            merged, _, _ = build_unified_dataset(symbol, okx, cg, coin_id, days_param)
            
            all_merged[symbol] = {
                'merged': merged,
                'okx_1d': df_okx_1d,
                'okx_1h': df_okx_1h,
                'okx_4h': df_okx_4h,
                'cg': df_cg,
            }
        except Exception as e:
            print(f"  XX {symbol}: {str(e)[:80]}")
    
    # ===== 技术分析 =====
    print(f"\n{'='*55}")
    print("技术分析")
    print(f"{'='*55}")
    
    primary = 'BTC/USDT'
    if primary in all_merged:
        d = all_merged[primary]
        df_ta = compute_indicators(d['okx_1d'].copy() if d['okx_1d'] is not None else None)
        
        if df_ta is not None and len(df_ta) > 20:
            last = df_ta.iloc[-1]
            print(f"\n  BTC/USD 当前技术状态 ({df_ta.index[-1].strftime('%Y-%m-%d')})")
            print(f"  {'='*40}")
            print(f"    价格: ${last['close']:>8,.2f}")
            print(f"    MA10: ${last['MA10']:>8,.2f}  MA30: ${last['MA30']:>8,.2f}")
            print(f"    MACD: {last['MACD']:>+8,.0f}  Signal: {last['MACD_Signal']:>+8,.0f}")
            print(f"    RSI(14): {last['RSI14']:>5.1f}  {'超买' if last['RSI14'] > 70 else '超卖' if last['RSI14'] < 30 else '正常'}")
            print(f"    BOLL带宽: {((last['BOLL_UP']-last['BOLL_DN'])/last['BOLL_MID']*100):>5.2f}%")
            print(f"    ATR(14): ${last['ATR14']:>8,.0f}")
            print(f"    信号: {last['Signal']}")
            
            # 信号统计
            signals = df_ta[df_ta['Signal'] != '持有']
            golden_count = len(signals[signals['Signal'] == '金叉'])
            death_count = len(signals[signals['Signal'] == '死叉'])
            print(f"    金叉/死叉: {golden_count}/{death_count} (最近30天)")
    
    # ===== 可视化 =====
    print(f"\n{'='*55}")
    print("可视化")
    print(f"{'='*55}")
    
    if primary in all_merged:
        d = all_merged[primary]
        visualize_pipeline(primary, d['merged'], d['okx_1d'], d['okx_1h'], d['okx_4h'], d['cg'])
    
    # ===== 存储 =====
    print(f"\n{'='*55}")
    print("数据导出")
    print(f"{'='*55}")
    
    if primary in all_merged:
        d = all_merged[primary]
        save_to_csv(primary, d['merged'], d['okx_1d'], d['cg'], d['okx_1h'], d['okx_4h'])
    
    elapsed = time.time() - start
    
    # ===== 总结 =====
    print(f"""
╔═══════════════════════════════════════════════════════════════╗
║  完成总结                                                     ║
╚═══════════════════════════════════════════════════════════════╝

  覆盖币种: {len(all_merged)}/{len(COINS)}
  OKX 数据: {sum(1 for v in all_merged.values() if v['okx_1d'] is not None)}/{len(all_merged)}
  CoinGecko: {sum(1 for v in all_merged.values() if v['cg'] is not None)}/{len(all_merged)}

  数据源融合策略:
  ┌─────────────┬─────────────────┬──────────────────┐
  │             │    OKX (CCXT)   │   CoinGecko      │
  ├─────────────┼─────────────────┼──────────────────┤
  │ 定位        │ 主力实时        │ 历史补充         │
  │ 频率        │ 1m/5m/1h/4h/1d │ 4h/日K           │
  │ 历史        │ 500条内         │ 数年             │
  │ 币种        │ 3976交易对      │ 17405个          │
  │ 延迟        │ <1s             │ ~2s              │
  │ 免费限频    │ 无              │ 10-30次/分       │
  └─────────────┴─────────────────┴──────────────────┘

  推荐使用:
  - OKX: 策略执行、实时监控、短线交易
  - CoinGecko: 历史回测、全市场扫描、宏观分析
  - 双源: 交叉验证、数据完整性保障

  输出文件:
  CSV: {DATA_DIR}/
  图表: {PLOTS_DIR}/

  耗时: {elapsed:.0f}秒
  时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
""")
