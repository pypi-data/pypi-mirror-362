"""
性能测试应用 - 测试优化后的 DashKLineChart 组件
"""

import dash
from dash import html, dcc, callback, Input, Output, State
import json
import time
import random
from datetime import datetime, timedelta
from dash_kline_charts import DashKLineChart

# 生成大量测试数据
def generate_large_dataset(count=5000):
    """生成大量K线数据用于性能测试"""
    data = []
    base_timestamp = int(datetime(2020, 1, 1).timestamp() * 1000)
    base_price = 100
    
    for i in range(count):
        timestamp = base_timestamp + (i * 60 * 1000)  # 每分钟一条数据
        
        # 随机价格变动
        change = random.uniform(-2, 2)
        base_price = max(10, base_price + change)
        
        open_price = base_price
        high_price = open_price + random.uniform(0, 3)
        low_price = open_price - random.uniform(0, 3)
        close_price = low_price + random.uniform(0, high_price - low_price)
        volume = random.randint(1000, 10000)
        
        data.append({
            'timestamp': timestamp,
            'open': round(open_price, 2),
            'high': round(high_price, 2),
            'low': round(low_price, 2),
            'close': round(close_price, 2),
            'volume': volume
        })
        
        base_price = close_price
    
    return data

# 生成实时数据
def generate_realtime_data(base_data, count=10):
    """生成实时数据用于测试快速更新"""
    if not base_data:
        return []
    
    last_item = base_data[-1]
    new_data = []
    
    for i in range(count):
        timestamp = last_item['timestamp'] + ((i + 1) * 60 * 1000)
        
        # 基于最后价格生成新数据
        base_price = last_item['close']
        change = random.uniform(-1, 1)
        base_price = max(10, base_price + change)
        
        open_price = base_price
        high_price = open_price + random.uniform(0, 2)
        low_price = open_price - random.uniform(0, 2)
        close_price = low_price + random.uniform(0, high_price - low_price)
        volume = random.randint(1000, 5000)
        
        new_data.append({
            'timestamp': timestamp,
            'open': round(open_price, 2),
            'high': round(high_price, 2),
            'low': round(low_price, 2),
            'close': round(close_price, 2),
            'volume': volume
        })
    
    return new_data

# 初始化应用
app = dash.Dash(__name__)

# 初始大数据集
large_dataset = generate_large_dataset(5000)

app.layout = html.Div([
    html.H1("DashKLineChart 性能测试", style={'textAlign': 'center'}),
    
    html.Div([
        html.H2("测试控制"),
        html.Div([
            html.Button("加载大数据集 (5000条)", id="load-large-btn", n_clicks=0, 
                       style={'margin': '5px', 'padding': '10px'}),
            html.Button("清空数据", id="clear-btn", n_clicks=0,
                       style={'margin': '5px', 'padding': '10px'}),
            html.Button("开始实时更新", id="start-realtime-btn", n_clicks=0,
                       style={'margin': '5px', 'padding': '10px', 'backgroundColor': '#4CAF50', 'color': 'white'}),
            html.Button("停止实时更新", id="stop-realtime-btn", n_clicks=0,
                       style={'margin': '5px', 'padding': '10px', 'backgroundColor': '#f44336', 'color': 'white'}),
        ], style={'margin': '20px 0'}),
        
        html.Div([
            html.Label("主题:"),
            dcc.Dropdown(
                id="theme-dropdown",
                options=[
                    {'label': '浅色主题', 'value': 'light'},
                    {'label': '深色主题', 'value': 'dark'}
                ],
                value='light',
                style={'width': '150px', 'display': 'inline-block', 'margin': '0 10px'}
            ),
            
            html.Label("技术指标:"),
            dcc.Dropdown(
                id="indicators-dropdown",
                options=[
                    {'label': '无指标', 'value': 'none'},
                    {'label': 'MA (5,10,20)', 'value': 'ma'},
                    {'label': 'RSI (14)', 'value': 'rsi'},
                    {'label': 'MACD (12,26,9)', 'value': 'macd'},
                    {'label': '全部指标', 'value': 'all'}
                ],
                value='none',
                style={'width': '150px', 'display': 'inline-block', 'margin': '0 10px'}
            ),
        ], style={'margin': '20px 0'}),
        
        html.Div([
            html.Label("数据量: "),
            html.Span(id="data-count", children="0"),
            html.Label(" | 最后更新: "),
            html.Span(id="last-update", children="未更新"),
            html.Label(" | 更新次数: "),
            html.Span(id="update-count", children="0"),
        ], style={'margin': '20px 0', 'fontWeight': 'bold'}),
    ], style={'padding': '20px', 'backgroundColor': '#f0f0f0', 'borderRadius': '5px', 'margin': '20px'}),
    
    # 性能指标展示
    html.Div([
        html.H3("性能指标"),
        html.Div(id="performance-metrics", style={'fontFamily': 'monospace'})
    ], style={'padding': '20px', 'backgroundColor': '#e8f4f8', 'borderRadius': '5px', 'margin': '20px'}),
    
    # 图表容器
    html.Div([
        DashKLineChart(
            id="performance-chart",
            data=[],
            config={'theme': 'light'},
            indicators=[],
            symbol="PERF-TEST",
            style={'height': '600px', 'width': '100%'},
            responsive=True
        )
    ], style={'margin': '20px'}),
    
    # 实时更新间隔
    dcc.Interval(
        id="realtime-interval",
        interval=500,  # 500ms间隔
        disabled=True,
        n_intervals=0
    ),
    
    # 存储组件
    dcc.Store(id="chart-data-store", data=large_dataset),
    dcc.Store(id="update-counter", data=0),
    dcc.Store(id="performance-data", data={}),
], style={'fontFamily': 'Arial, sans-serif'})

# 加载大数据集
@callback(
    [Output("chart-data-store", "data"),
     Output("performance-data", "data", allow_duplicate=True)],
    Input("load-large-btn", "n_clicks"),
    prevent_initial_call=True
)
def load_large_dataset(n_clicks):
    if n_clicks > 0:
        start_time = time.time()
        data = generate_large_dataset(5000)
        load_time = time.time() - start_time
        
        perf_data = {
            'data_generation_time': f"{load_time:.3f}s",
            'data_size': len(data),
            'memory_usage': f"{len(json.dumps(data)) / 1024 / 1024:.2f}MB"
        }
        
        return data, perf_data
    return dash.no_update, dash.no_update

# 清空数据
@callback(
    Output("chart-data-store", "data", allow_duplicate=True),
    Input("clear-btn", "n_clicks"),
    prevent_initial_call=True
)
def clear_data(n_clicks):
    if n_clicks > 0:
        return []
    return dash.no_update

# 控制实时更新
@callback(
    Output("realtime-interval", "disabled"),
    [Input("start-realtime-btn", "n_clicks"),
     Input("stop-realtime-btn", "n_clicks")]
)
def control_realtime(start_clicks, stop_clicks):
    ctx = dash.callback_context
    if not ctx.triggered:
        return True
    
    button_id = ctx.triggered[0]['prop_id'].split('.')[0]
    
    if button_id == "start-realtime-btn" and start_clicks > 0:
        return False
    elif button_id == "stop-realtime-btn" and stop_clicks > 0:
        return True
    
    return True

# 实时数据更新
@callback(
    [Output("chart-data-store", "data", allow_duplicate=True),
     Output("update-counter", "data")],
    Input("realtime-interval", "n_intervals"),
    [State("chart-data-store", "data"),
     State("update-counter", "data")],
    prevent_initial_call=True
)
def update_realtime_data(n_intervals, current_data, update_count):
    if n_intervals > 0 and current_data:
        # 生成新的实时数据
        new_data = generate_realtime_data(current_data, 5)
        
        # 限制总数据量，避免无限增长
        max_data_points = 10000
        updated_data = current_data + new_data
        if len(updated_data) > max_data_points:
            updated_data = updated_data[-max_data_points:]
        
        return updated_data, update_count + 1
    
    return dash.no_update, dash.no_update

# 更新图表配置和数据
@callback(
    [Output("performance-chart", "data"),
     Output("performance-chart", "config"),
     Output("performance-chart", "indicators"),
     Output("data-count", "children"),
     Output("last-update", "children"),
     Output("update-count", "children"),
     Output("performance-metrics", "children"),
     Output("performance-data", "data", allow_duplicate=True)],
    [Input("chart-data-store", "data"),
     Input("theme-dropdown", "value"),
     Input("indicators-dropdown", "value"),
     Input("update-counter", "data")],
    [State("performance-data", "data")],
    prevent_initial_call=True
)
def update_chart(data, theme, indicators_type, update_count, perf_data):
    start_time = time.time()
    
    # 配置主题
    config = {'theme': theme}
    
    # 配置技术指标
    indicators = []
    if indicators_type == 'ma':
        indicators = [{'name': 'MA', 'params': [5, 10, 20]}]
    elif indicators_type == 'rsi':
        indicators = [{'name': 'RSI', 'params': [14]}]
    elif indicators_type == 'macd':
        indicators = [{'name': 'MACD', 'params': [12, 26, 9]}]
    elif indicators_type == 'all':
        indicators = [
            {'name': 'MA', 'params': [5, 10, 20]},
            {'name': 'RSI', 'params': [14]},
            {'name': 'MACD', 'params': [12, 26, 9]}
        ]
    
    # 计算渲染时间
    render_time = time.time() - start_time
    
    # 更新性能数据
    if not perf_data:
        perf_data = {}
    
    perf_data.update({
        'render_time': f"{render_time:.3f}s",
        'current_data_points': len(data) if data else 0,
        'indicators_count': len(indicators),
        'theme': theme
    })
    
    # 生成性能指标显示
    metrics_display = html.Div([
        html.P(f"数据生成时间: {perf_data.get('data_generation_time', 'N/A')}"),
        html.P(f"渲染时间: {perf_data.get('render_time', 'N/A')}"),
        html.P(f"数据大小: {perf_data.get('data_size', 'N/A')} 条"),
        html.P(f"内存使用: {perf_data.get('memory_usage', 'N/A')}"),
        html.P(f"当前数据点: {perf_data.get('current_data_points', 0)} 条"),
        html.P(f"技术指标数量: {perf_data.get('indicators_count', 0)}"),
        html.P(f"当前主题: {perf_data.get('theme', 'light')}")
    ])
    
    # 当前时间
    current_time = datetime.now().strftime("%H:%M:%S")
    
    return (data, config, indicators, 
            len(data) if data else 0, 
            current_time, 
            update_count or 0,
            metrics_display,
            perf_data)

if __name__ == '__main__':
    app.run_server(debug=True, port=8051)