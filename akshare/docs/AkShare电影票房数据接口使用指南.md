# AkShare 电影票房数据接口使用指南 (阶段7.2)

## 概述

AkShare 提供了 `movie_boxoffice_*` 系列接口用于获取中国电影票房数据，但**当前所有接口均不可用**（数据源艺恩 endata.com.cn 已停止API服务）。本文档提供替代数据源方案。

## 接口状态

| 接口名 | 说明 | 状态 | 错误原因 |
|--------|------|------|---------|
| `movie_boxoffice_realtime()` | 实时票房 | ❌ | API返回405 (已关闭) |
| `movie_boxoffice_daily(date)` | 日票房 | ❌ | 同上 |
| `movie_boxoffice_weekly(date)` | 周票房 | ❌ | 同上 |
| `movie_boxoffice_monthly(date)` | 月票房 | ❌ | 同上 |
| `movie_boxoffice_yearly(date)` | 年票房 | ❌ | 同上 |
| `movie_boxoffice_cinema_daily(date)` | 影院日票房 | ❌ | 同上 |

**技术原因**: 原接口调用 `https://www.endata.com.cn/API/GetData.ashx` 使用POST方式 + `py_mini_racer` JS解密。该API已返回405 Not Allowed，新域名 `ys.endata.cn` 仅返回HTML页面。

## 替代方案

### 方案1: 小尘API (推荐, 免费, 无需认证)

获取每日票房Top10排行，返回JSON格式数据。

**接口地址**: `https://api.xcvts.cn/api/hotlist/piaofang?type=json`

**返回格式**:
```json
{
  "time": "2026-05-13",
  "data": [
    {"index": 1, "title": "电影名称", "releaseInfo": "上映14天", "sumBoxDesc": "1.76亿"},
    ...
  ]
}
```

**Python示例**:
```python
import requests
r = requests.get('https://api.xcvts.cn/api/hotlist/piaofang?type=json', timeout=15)
data = r.json()
for item in data['data']:
    print(f"#{item['index']} {item['title']} {item['sumBoxDesc']}")
```

**注意**: 该接口有时第一次请求会超时，重试即可。建议设置 `timeout=15`。

### 方案2: 猫眼专业版 (需浏览器渲染)

访问 `https://piaofang.maoyan.com/dashboard` 可查看完整实时票房排行（含排片场次、票房占比等详细数据）。

数据通过客户端渲染和自定义字体加密，纯HTTP请求无法获取结构化数据。需要通过浏览器自动化工具（如Selenium、Playwright）渲染页面后提取。

### 方案3: 猫眼年度排行 (历史数据)

访问 `https://piaofang.maoyan.com/rankings/year` 获取历史票房总榜。页面为静态HTML，可通过文本提取获取排行信息（含100条历史记录）。

## 测试脚本

- `scripts/s7.2_test_movie_boxoffice.py`: 接口可用性测试
- `scripts/s7.2_demo_movie_boxoffice.py`: 综合演示 + 可视化

## 运行示例

```bash
cd /home/neyo/workspace/code/study/akshare
./venv/bin/python scripts/s7.2_test_movie_boxoffice.py
./venv/bin/python scripts/s7.2_demo_movie_boxoffice.py
```

## 注意事项

1. 小尘API偶尔首次请求超时，重试即可恢复正常
2. 猫眼使用自定义字体渲染票房数字，直接取DOM的textContent会得到乱码
3. 若需要更详细的数据（按影院、按地区等），建议使用猫眼专业版配合浏览器自动化
4. 等待AkShare未来版本可能更新为新的数据源
