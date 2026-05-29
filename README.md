# 永鼎股份 600105 日K中长线观察看板

当前版本 `v9`，这是一个针对永鼎股份 `600105.SH` 的单股静态看板。页面保留分时实时曲线，同时把核心量化策略切换到日K维度，更适合中长线观察。

## 功能

- 分时监控：浏览器打开后先回填当天 9:30 到当前的分钟走势，再自动轮询实时行情。
- 日K更新：页面自动读取东方财富日K数据，计算中长线指标。
- 自动化数据：GitHub Actions 会在交易日自动生成 `data/yd_600105_daily.json`，页面优先读取这个文件。
- 日K图表：展示最近 90 个交易日K线，并叠加 MA20、MA60。
- 中长线评分：从趋势、动量、量价、位置、风险五个维度计算综合评分。
- 周期观察：输出次日、一周、一个月三个观察维度。
- 关键价位：自动给出关键支撑、关键压力、观察买点和关键卖点。
- 本地缓存：日K数据读取失败时，会优先使用浏览器本地缓存。

## 策略思路

新版参考了已下载的金融/量化工具思路：

- `microsoft/qlib`：借鉴因子化研究框架，把信号拆成趋势、动量、量能、位置、风险。
- `TauricResearch/TradingAgents`：借鉴多角色分析结构，把技术面、风险面、交易观察分开输出。
- `OpenBB`：借鉴技术指标和可解释分析方式，强调历史价格、均线、指标和图表联动。

页面内置的主要指标包括：

- 趋势：MA5、MA10、MA20、MA60、MA120、EMA20、EMA60、均线斜率。
- 动量：MACD、RSI14、KDJ。
- 量价：成交量/20日均量、20日均成交额、涨跌与量能配合。
- 位置：20/60/120日高低点、BOLL位置、60日回撤。
- 风险：ATR14、距MA20偏离、RSI过热、跌破MA60风险。

## 部署

这是纯静态页面，适合部署到 GitHub Pages。

1. 上传 `index.html`、`README.md`、`.nojekyll`、`scripts/update_yongding_daily.py` 和 `.github/workflows/update-yongding-daily.yml` 到仓库根目录对应位置。
2. 在 GitHub 仓库 `Settings -> Pages` 中选择 `Deploy from a branch`。
3. 分支选择 `main`，目录选择 `/root`。

## GitHub Actions 自动更新

工作流文件位于 `.github/workflows/update-yongding-daily.yml`。

- 交易日北京时间约 16:20 和 20:10 自动运行一次。
- 也可以在 GitHub 仓库 `Actions -> Update Yongding Daily Data -> Run workflow` 手动运行。
- 运行后会更新 `data/yd_600105_daily.json` 并自动提交。
- 看板打开时会优先读取该静态 JSON；如果文件不存在或读取失败，再回退到浏览器端在线行情源。

如果使用本地脚本发布，设置 `GITHUB_TOKEN` 后运行：

```powershell
$env:GITHUB_TOKEN="你的新 GitHub token"
python publish_to_github.py
```

## 风险提示

本看板只用于行情观察和策略辅助，不构成投资建议，也不保证收益。A股行情源可能因网络、跨域或数据源策略变化而短暂不可用。
