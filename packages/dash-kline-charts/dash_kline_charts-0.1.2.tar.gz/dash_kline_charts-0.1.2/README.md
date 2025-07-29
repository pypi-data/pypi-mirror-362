# Dash KLineChart Component

[![npm version](https://badge.fury.io/js/dash-kline-charts.svg)](https://badge.fury.io/js/dash-kline-charts)
[![PyPI version](https://badge.fury.io/py/dash-kline-charts.svg)](https://badge.fury.io/py/dash-kline-charts)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

一个基于 KLineChart 的自定义 Dash 组件，用于在 Python Dash 应用中展示专业的金融图表。

## 🚀 项目特性

- **📈 专业金融图表**：基于 KLineChart 10.0.0-alpha8，支持 K线图、蜡烛图等金融图表
- **🎯 完整技术指标**：内置 MA、EMA、RSI、MACD、BOLL 等常用技术指标
- **📱 响应式设计**：支持桌面端和移动端，自适应不同屏幕尺寸
- **🎨 主题定制**：支持明暗主题切换和自定义样式
- **⚡ 高性能渲染**：基于 HTML5 Canvas，支持大数据集流畅渲染
- **🔄 实时更新**：支持实时数据更新和动态交互
- **🐍 Python 友好**：完全兼容 Dash 生态系统，支持 Pandas DataFrame

## 📦 安装

```bash
pip install dash-kline-charts
```

> **📌 注意**: KLineChart JavaScript 库会自动包含在组件中，无需额外安装或配置。组件会自动加载所需的 `klinecharts.min.js` 文件。

## 🔧 快速开始

### 基础用法

```python
import dash
from dash import html, dcc, Input, Output
import dash_kline_charts as dkc
import pandas as pd

# 创建示例数据
data = [
    {'timestamp': 1609459200000, 'open': 100, 'high': 110, 'low': 95, 'close': 105, 'volume': 1000},
    {'timestamp': 1609545600000, 'open': 105, 'high': 115, 'low': 100, 'close': 110, 'volume': 1200},
    # ... 更多数据
]

app = dash.Dash(__name__)

app.layout = html.Div([
    dkc.DashKLineChart(
        id='kline-chart',
        data=data,
        style={'height': '600px'},
        config={
            'grid': {'show': True},
            'candle': {'type': 'candle_solid'},
            'theme': 'dark'
        }
    )
])

if __name__ == '__main__':
    app.run_server(debug=True)
```

### 添加技术指标

```python
dkc.DashKLineChart(
    id='kline-chart',
    data=data,
    indicators=[
        {'name': 'MA', 'params': [5, 10, 20]},
        {'name': 'RSI', 'params': [14]},
        {'name': 'MACD', 'params': [12, 26, 9]}
    ],
    style={'height': '600px'}
)
```

### 实时数据更新

```python
@app.callback(
    Output('kline-chart', 'data'),
    Input('interval-component', 'n_intervals')
)
def update_data(n):
    # 获取最新数据
    new_data = get_latest_market_data()
    return new_data
```

## 📋 API 文档

### DashKLineChart 属性

| 属性 | 类型 | 默认值 | 描述 |
|------|------|--------|------|
| `id` | str | - | 组件唯一标识符 |
| `data` | list | [] | 图表数据，OHLC 格式 |
| `config` | dict | {} | 图表配置选项 |
| `style` | dict | {} | 组件样式设置 |
| `indicators` | list | [] | 技术指标配置 |
| `theme` | str | 'light' | 主题设置 ('light' 或 'dark') |
| `responsive` | bool | True | 是否启用响应式设计 |

### 数据格式

```python
data = [
    {
        'timestamp': 1609459200000,  # 时间戳（毫秒）
        'open': 100.0,              # 开盘价
        'high': 110.0,              # 最高价
        'low': 95.0,                # 最低价
        'close': 105.0,             # 收盘价
        'volume': 1000              # 成交量
    },
    # ... 更多数据点
]
```

### 配置选项

```python
config = {
    'grid': {
        'show': True,
        'horizontal': {'show': True},
        'vertical': {'show': True}
    },
    'candle': {
        'type': 'candle_solid',      # 蜡烛图类型
        'bar': {'upColor': '#26A69A', 'downColor': '#EF5350'}
    },
    'crosshair': {
        'show': True,
        'horizontal': {'show': True},
        'vertical': {'show': True}
    },
    'yAxis': {
        'show': True,
        'position': 'right'
    },
    'xAxis': {
        'show': True,
        'position': 'bottom'
    }
}
```

## 🧪 支持的技术指标

- **移动平均线**: MA, EMA, SMA
- **趋势指标**: MACD, RSI, KDJ
- **成交量指标**: VOL, OBV
- **波动率指标**: BOLL, ATR
- **自定义指标**: 支持自定义技术指标

## 🎨 主题定制

### 预设主题

```python
# 明亮主题
theme = 'light'

# 暗黑主题
theme = 'dark'
```

### 自定义主题

```python
custom_theme = {
    'background': '#1e1e1e',
    'grid': '#333333',
    'candle': {
        'up': '#26A69A',
        'down': '#EF5350'
    },
    'text': '#ffffff'
}
```

## 📱 响应式设计

组件自动适配不同屏幕尺寸：

```python
dkc.DashKLineChart(
    id='kline-chart',
    data=data,
    responsive=True,
    style={
        'height': '400px',
        'width': '100%'
    }
)
```

## 🔧 开发环境设置

### 开发依赖

```bash
# 安装开发依赖
npm install

# 启动开发服务器
npm start

# 构建生产版本
npm run build

# 运行测试
npm test
```

### Python 开发环境

```bash
# 创建虚拟环境
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

# 安装依赖
pip install -r requirements.txt

# 运行示例
python examples/basic_example.py
```

## 🤝 贡献指南

1. Fork 本项目
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 创建 Pull Request

### 开发规范

- 遵循 PEP 8 代码风格
- 编写单元测试
- 更新文档
- 提交前运行测试套件

## 📄 许可证

本项目基于 MIT 许可证开源 - 详见 [LICENSE](LICENSE) 文件。

## 📚 相关资源

- [KLineChart 官方文档](https://klinecharts.com/)
- [Dash 文档](https://dash.plotly.com/)
- [React 组件开发指南](https://reactjs.org/docs/components-and-props.html)

## 🐛 问题反馈

如果您发现任何问题或有功能建议，请在 [GitHub Issues](https://github.com/your-username/dash-kline-charts/issues) 中提出。

## 📧 联系我们

- 项目主页: [https://github.com/your-username/dash-kline-charts](https://github.com/your-username/dash-kline-charts)
- 邮箱: your-email@example.com

## 📊 支持的图表类型

- **蜡烛图** (candle_solid): 实心蜡烛图
- **空心蜡烛图** (candle_stroke): 空心蜡烛图
- **OHLC 图** (ohlc): 开高低收图
- **面积图** (area): 面积填充图

## 📐 技术指标

| 指标 | 名称 | 参数示例 |
|------|------|----------|
| MA | 移动平均线 | [5, 10, 20] |
| EMA | 指数移动平均线 | [12, 26] |
| RSI | 相对强弱指数 | [14] |
| MACD | 移动平均收敛散度 | [12, 26, 9] |
| BOLL | 布林带 | [20, 2] |
| KDJ | 随机指标 | [9, 3, 3] |
| VOL | 成交量 | [] |

## 🎨 主题支持

- **明亮主题**: 适合白天使用的明亮界面
- **暗黑主题**: 适合夜间使用的暗色界面
- **自定义主题**: 支持完全自定义颜色方案

## 🔧 系统要求

### Python 环境
- Python 3.7+
- Dash 2.0+
- Plotly 5.0+

### 浏览器支持
- Chrome 80+
- Firefox 75+
- Safari 13+
- Edge 80+

## 🏗️ 项目架构

```
dash-kline-charts/
├── src/                    # React 组件源码
├── dash_kline_charts/     # Python 包
├── examples/              # 示例应用
├── tests/                 # 测试文件
├── docs/                  # 文档
└── lib/                   # 构建输出
```

## 🧪 测试

### JavaScript 测试
```bash
npm test
npm run test:watch
npm run test:coverage
```

### Python 测试
```bash
python -m pytest tests/
python -m pytest tests/ --cov=dash_kline_charts
```

## 📚 文档

- [📋 API 文档](docs/API.md) - 详细的 API 参考
- [🤝 贡献指南](docs/CONTRIBUTING.md) - 如何参与项目开发
- [🏗️ 项目结构](docs/PROJECT_STRUCTURE.md) - 项目目录结构说明
- [📝 更新日志](CHANGELOG.md) - 版本更新记录

## 🔗 相关链接

- [KLineChart 官方文档](https://klinecharts.com/)
- [Dash 官方文档](https://dash.plotly.com/)
- [React 官方文档](https://reactjs.org/)

## 🏷️ 版本历史

查看 [CHANGELOG.md](CHANGELOG.md) 了解详细的版本更新历史。

## 📄 许可证

本项目基于 [MIT 许可证](LICENSE) 开源。

## 🙏 致谢

- [KLineChart](https://github.com/klinecharts/KLineChart) - 提供优秀的金融图表库
- [Dash](https://github.com/plotly/dash) - 提供强大的 Python web 应用框架
- 所有为此项目做出贡献的开发者

## 📞 支持

- 🐛 [报告问题](https://github.com/your-username/dash-kline-charts/issues)
- 💡 [功能请求](https://github.com/your-username/dash-kline-charts/issues)
- 💬 [社区讨论](https://github.com/your-username/dash-kline-charts/discussions)
- 📧 邮箱: your-email@example.com

---

**⭐ 如果这个项目对您有帮助，请给我们一个 Star！**