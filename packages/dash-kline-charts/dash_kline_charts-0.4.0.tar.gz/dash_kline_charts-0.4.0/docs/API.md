# API 文档

## DashKLineChart 组件

### 属性 (Props)

#### 必需属性

- **data** (`List[Dict]`): K线数据数组
  - 每个数据项必须包含以下字段：
    - `timestamp` (number): 时间戳（毫秒）
    - `open` (number): 开盘价
    - `high` (number): 最高价
    - `low` (number): 最低价
    - `close` (number): 收盘价
    - `volume` (number, 可选): 成交量

#### 可选属性

- **id** (`str`): 组件的唯一标识符
- **config** (`Dict`): 图表配置选项
- **indicators** (`List[Dict]`): 技术指标配置
- **style** (`Dict`): CSS 样式属性
- **className** (`str`): CSS 类名
- **responsive** (`bool`): 是否启用响应式设计，默认 `True`
- **symbol** (`str`): 交易标的符号，默认 `'DASH-KLINE'`

### 配置选项 (Config)

```python
config = {
    'theme': 'light',  # 'light' 或 'dark'
    'grid': {
        'show': True,
        'horizontal': {'show': True},
        'vertical': {'show': True}
    },
    'candle': {
        'type': 'candle_solid',  # 'candle_solid', 'candle_stroke', 'ohlc', 'area'
        'bar': {
            'upColor': '#26A69A',
            'downColor': '#EF5350',
            'noChangeColor': '#888888'
        }
    },
    'crosshair': {
        'show': True,
        'horizontal': {'show': True},
        'vertical': {'show': True}
    },
    'yAxis': {
        'show': True,
        'position': 'right'  # 'left' 或 'right'
    },
    'xAxis': {
        'show': True,
        'position': 'bottom'  # 'top' 或 'bottom'
    }
}
```

### 技术指标 (Indicators)

```python
indicators = [
    {
        'name': 'MA',           # 指标名称
        'params': [5, 10, 20],  # 参数
        'visible': True,        # 是否可见
        'color': '#FF0000'      # 颜色（可选）
    },
    {
        'name': 'RSI',
        'params': [14]
    },
    {
        'name': 'MACD',
        'params': [12, 26, 9]
    }
]
```

### 支持的技术指标

| 指标名称 | 参数 | 描述 |
|---------|------|------|
| MA | [period1, period2, ...] | 移动平均线 |
| EMA | [period1, period2, ...] | 指数移动平均线 |
| RSI | [period] | 相对强弱指数 |
| MACD | [fast, slow, signal] | 移动平均收敛散度 |
| BOLL | [period, deviation] | 布林带 |
| KDJ | [k, d, j] | 随机指标 |
| VOL | [] | 成交量 |

### 样式配置 (Style)

```python
style = {
    'height': '600px',
    'width': '100%',
    'backgroundColor': '#ffffff',
    'border': '1px solid #ddd',
    'borderRadius': '4px'
}
```

### 主题配置

#### 明亮主题
```python
config = {
    'theme': 'light'
}
```

#### 暗黑主题
```python
config = {
    'theme': 'dark'
}
```

#### 自定义主题
通过 `candle.bar` 配置自定义颜色：
```python
config = {
    'candle': {
        'bar': {
            'upColor': '#00FF00',      # 上涨颜色
            'downColor': '#FF0000',    # 下跌颜色
            'noChangeColor': '#888888' # 不变颜色
        }
    }
}
```

### 响应式设计

```python
# 启用响应式设计（默认）
DashKLineChart(
    data=data,
    responsive=True
)

# 禁用响应式设计
DashKLineChart(
    data=data,
    responsive=False
)
```

### 回调函数示例

```python
from dash import Input, Output, callback

@callback(
    Output('kline-chart', 'data'),
    Input('interval-component', 'n_intervals')
)
def update_chart_data(n):
    # 获取新数据
    new_data = get_latest_data()
    return new_data

@callback(
    Output('kline-chart', 'config'),
    Input('theme-dropdown', 'value')
)
def update_theme(theme):
    return {'theme': theme}

@callback(
    Output('kline-chart', 'indicators'),
    Input('indicator-checklist', 'value')
)
def update_indicators(selected_indicators):
    indicators = []
    for indicator in selected_indicators:
        if indicator == 'MA':
            indicators.append({'name': 'MA', 'params': [5, 10, 20]})
        elif indicator == 'RSI':
            indicators.append({'name': 'RSI', 'params': [14]})
    return indicators
```

### 完整示例

```python
import dash
from dash import html, dcc, Input, Output
import datetime
import random
from dash_kline_charts import DashKLineChart

app = dash.Dash(__name__)

# 生成示例数据
def create_sample_data(count=100):
    data = []
    timestamp = int((datetime.datetime.now() - datetime.timedelta(days=count)).timestamp() * 1000)
    price = 100.0
    
    for i in range(count):
        change = random.uniform(-2, 2)
        price += change
        
        open_price = price
        high_price = price + random.uniform(0, 1)
        low_price = price - random.uniform(0, 1)
        close_price = price + random.uniform(-0.5, 0.5)
        volume = random.randint(1000, 10000)
        
        data.append({
            'timestamp': timestamp,
            'open': round(open_price, 2),
            'high': round(high_price, 2),
            'low': round(low_price, 2),
            'close': round(close_price, 2),
            'volume': volume,
        })
        
        timestamp += 86400 * 1000  # 增加1天
        price = close_price
    
    return data

sample_data = create_sample_data(50)

app.layout = html.Div([
    html.H1("Dash KLineChart 示例", style={'textAlign': 'center'}),
    
    html.Div([
        html.Label("主题选择:"),
        dcc.Dropdown(
            id='theme-dropdown',
            options=[
                {'label': '明亮主题', 'value': 'light'},
                {'label': '暗黑主题', 'value': 'dark'}
            ],
            value='light'
        )
    ], style={'margin': '20px', 'width': '200px'}),
    
    html.Div([
        html.Label("技术指标:"),
        dcc.Checklist(
            id='indicator-checklist',
            options=[
                {'label': '移动平均线 (MA)', 'value': 'MA'},
                {'label': '相对强弱指数 (RSI)', 'value': 'RSI'},
                {'label': 'MACD', 'value': 'MACD'}
            ],
            value=['MA']
        )
    ], style={'margin': '20px'}),
    
    html.Div([
        DashKLineChart(
            id='kline-chart',
            data=sample_data,
            config={
                'theme': 'light',
                'grid': {'show': True},
                'candle': {'type': 'candle_solid'},
                'crosshair': {'show': True}
            },
            indicators=[
                {'name': 'MA', 'params': [5, 10, 20], 'visible': True}
            ],
            style={'height': '600px'},
            responsive=True
        )
    ], style={'margin': '20px'}),
    
    html.Div([
        html.Button('刷新数据', id='refresh-btn', n_clicks=0),
        html.Div(id='data-info')
    ], style={'margin': '20px', 'textAlign': 'center'})
])

@app.callback(
    Output('kline-chart', 'config'),
    Input('theme-dropdown', 'value')
)
def update_theme(theme):
    return {
        'theme': theme,
        'grid': {'show': True},
        'candle': {'type': 'candle_solid'},
        'crosshair': {'show': True}
    }

@app.callback(
    Output('kline-chart', 'indicators'),
    Input('indicator-checklist', 'value')
)
def update_indicators(selected_indicators):
    indicators = []
    for indicator in selected_indicators:
        if indicator == 'MA':
            indicators.append({'name': 'MA', 'params': [5, 10, 20], 'visible': True})
        elif indicator == 'RSI':
            indicators.append({'name': 'RSI', 'params': [14], 'visible': True})
        elif indicator == 'MACD':
            indicators.append({'name': 'MACD', 'params': [12, 26, 9], 'visible': True})
    return indicators

@app.callback(
    [Output('kline-chart', 'data'),
     Output('data-info', 'children')],
    Input('refresh-btn', 'n_clicks')
)
def update_data(n_clicks):
    new_data = create_sample_data(50)
    return new_data, f'数据已更新，共 {len(new_data)} 个数据点'

if __name__ == '__main__':
    app.run_server(debug=True)
```

### 常见问题

#### Q: 图表不显示？
A: 检查以下几点：
1. 确保已正确安装依赖包：`pip install -e .`
2. 验证数据格式是否正确
3. 检查容器是否有足够的高度

#### Q: 技术指标不显示？
A: 确保：
1. 指标名称正确
2. 参数格式正确
3. `visible` 属性设置为 `True`

#### Q: 如何自定义颜色？
A: 通过 `config.candle.bar` 配置：
```python
config = {
    'candle': {
        'bar': {
            'upColor': '#26A69A',
            'downColor': '#EF5350'
        }
    }
}
```

#### Q: 如何处理大数据集？
A: 建议：
1. 数据分页加载
2. 使用虚拟滚动
3. 限制显示的数据点数量（< 1000）

### 数据格式验证

```python
def validate_data(data):
    """验证数据格式"""
    if not isinstance(data, list):
        return False
    
    required_fields = ['timestamp', 'open', 'high', 'low', 'close']
    
    for item in data:
        if not isinstance(item, dict):
            return False
        
        # 检查必需字段
        for field in required_fields:
            if field not in item:
                return False
            if not isinstance(item[field], (int, float)):
                return False
        
        # 检查价格逻辑
        if not (item['low'] <= item['open'] <= item['high'] and
                item['low'] <= item['close'] <= item['high']):
            return False
    
    return True
```

### 性能优化建议

1. **数据量控制**: 建议单次显示的数据点不超过 1000 个
2. **实时更新**: 使用适当的更新间隔，避免过于频繁的更新
3. **响应式设计**: 在移动设备上可以禁用响应式设计以提高性能
4. **技术指标**: 避免同时使用过多的技术指标
5. **内存管理**: 定期清理不需要的历史数据

### 错误处理

组件会自动验证数据格式，如果数据不符合要求，会显示错误信息：

- 数据必须是数组格式
- 每个数据项必须包含 `timestamp`, `open`, `high`, `low`, `close` 字段
- 所有价格字段必须是数字类型
- `volume` 字段可选，如果提供必须是数字类型
- 价格逻辑必须合理（最低价 ≤ 开盘价/收盘价 ≤ 最高价）

### 浏览器兼容性

- Chrome 80+
- Firefox 75+
- Safari 13+
- Edge 80+

### 依赖要求

- Python 3.7+
- Dash 2.0+
- Plotly 5.0+