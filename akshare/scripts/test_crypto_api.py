#!/usr/bin/env python3
"""测试免费数字货币数据源"""
import requests, sys
from datetime import datetime

def test_coingecko():
    print("=" * 60)
    print("1. CoinGecko API (免费, 无需Key)")
    print("=" * 60)
    try:
        r = requests.get("https://api.coingecko.com/api/v3/ping", timeout=10)
        print(f"  连接: {'OK' if r.ok else 'FAIL'}")
        
        r = requests.get("https://api.coingecko.com/api/v3/simple/price?ids=bitcoin,ethereum&vs_currencies=usd&include_24hr_change=true", timeout=10)
        if r.ok:
            data = r.json()
            for coin, info in data.items():
                print(f"  {coin:12s} ${info['usd']:>10,.2f}  24h: {info.get('usd_24h_change',0):+.2f}%")
        
        # 历史OHLCV
        r = requests.get("https://api.coingecko.com/api/v3/coins/bitcoin/ohlc?vs_currency=usd&days=7", timeout=10)
        if r.ok:
            ohlcv = r.json()
            print(f"  BTC日K线(最近7天): {len(ohlcv)}条")
            for c in ohlcv[-3:]:
                t = datetime.fromtimestamp(c[0]/1000)
                print(f"    {t.strftime('%Y-%m-%d')}  O:{c[1]:,.0f} H:{c[2]:,.0f} L:{c[3]:,.0f} C:{c[4]:,.0f}")
        return True
    except Exception as e:
        print(f"  错误: {e}")
        return False

def test_coinpaprika():
    print("\n" + "=" * 60)
    print("2. CoinPaprika API (免费, 无需Key)")
    print("=" * 60)
    try:
        r = requests.get("https://api.coinpaprika.com/v1/global", timeout=10)
        if r.ok:
            d = r.json()
            print(f"  总市值: ${d['market_cap_usd']:,.0f}")
            print(f"  24h量:  ${d['volume_24h_usd']:,.0f}")
            print(f"  BTC占比: {d['bitcoin_dominance_percentage']:.1f}%")
        
        # 历史OHLCV
        r = requests.get("https://api.coinpaprika.com/v1/coins/btc-bitcoin/ohlcv/historical?start=2026-05-06&end=2026-05-13", timeout=10)
        if r.ok:
            data = r.json()
            print(f"  BTC日K线: {len(data)}条")
            for d in data[-3:]:
                print(f"    {d['time_open'][:10]}  O:{d['open']:,.0f} H:{d['high']:,.0f} L:{d['low']:,.0f} C:{d['close']:,.0f}")
        return True
    except Exception as e:
        print(f"  错误: {e}")
        return False

def test_okx_ccxt():
    print("\n" + "=" * 60)
    print("3. OKX 交易所 (CCXT库, 公开数据)")
    print("=" * 60)
    try:
        import ccxt
        ex = ccxt.okx({"enableRateLimit": True})
        ticker = ex.fetch_ticker("BTC/USDT")
        print(f"  BTC/USDT: ${ticker['last']:,.2f}")
        print(f"  24h涨跌:  {ticker['percentage']:.2f}%")
        
        ohlcv = ex.fetch_ohlcv("BTC/USDT", "1d", limit=3)
        print(f"  最近3根日K线:")
        for c in ohlcv:
            t = datetime.fromtimestamp(c[0]/1000)
            print(f"    {t.strftime('%Y-%m-%d')}  O:{c[1]:,.2f} H:{c[2]:,.2f} L:{c[3]:,.2f} C:{c[4]:,.2f} V:{c[5]:,.2f}")
        return True
    except Exception as e:
        print(f"  错误: {e}")
        return False

if __name__ == "__main__":
    results = []
    results.append(test_coingecko())
    results.append(test_coinpaprika())
    results.append(test_okx_ccxt())
    
    print("\n" + "=" * 60)
    print("测试总结:")
    sources = ["CoinGecko", "CoinPaprika", "OKX(CCXT)"]
    for name, ok in zip(sources, results):
        print(f"  {name:15s}: {'可用' if ok else '不可用'}")
