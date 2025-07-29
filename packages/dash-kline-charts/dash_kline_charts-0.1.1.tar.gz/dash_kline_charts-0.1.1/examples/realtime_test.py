#!/usr/bin/env python3
"""
实时数据更新测试 - 修复版本
确保所有生成的数据都符合价格关系要求
"""

import dash
from dash import html, dcc, Input, Output, State, callback_context
import datetime
import random
import time
from dash_kline_charts import DashKLineChart

# 创建应用
app = dash.Dash(__name__)

# 数据生成函数
def generate_valid_kline_data(base_price, timestamp):
    """生成符合价格关系的K线数据"""
    # 基础价格变化
    change = random.uniform(-1, 1)
    new_price = base_price + change

    # 生成开盘价
    open_price = new_price + random.uniform(-0.5, 0.5)

    # 生成收盘价
    close_price = new_price + random.uniform(-0.5, 0.5)

    # 生成高低价（确保覆盖开盘和收盘价）
    high_price = max(open_price, close_price) + random.uniform(0, 0.5)
    low_price = min(open_price, close_price) - random.uniform(0, 0.5)

    # 生成成交量
    volume = random.randint(1000, 10000)

    return {
        "timestamp": timestamp,
        "open": round(open_price, 2),
        "high": round(high_price, 2),
        "low": round(low_price, 2),
        "close": round(close_price, 2),
        "volume": volume,
    }, close_price

# 初始数据
initial_data = []
start_time = int((datetime.datetime.now() - datetime.timedelta(days=50)).timestamp() * 1000)
price = 100.0

print("生成初始数据...")
for i in range(50):
    timestamp = start_time + i * 86400 * 1000
    data_point, price = generate_valid_kline_data(price, timestamp)
    initial_data.append(data_point)

print(f"初始数据生成完成，共 {len(initial_data)} 条数据")

# 验证初始数据
def validate_data(data):
    """验证数据格式"""
    for i, item in enumerate(data):
        if not (item['high'] >= item['low'] and
                item['open'] >= item['low'] and item['open'] <= item['high'] and
                item['close'] >= item['low'] and item['close'] <= item['high']):
            print(f"数据验证失败，第 {i+1} 条数据: {item}")
            return False
    return True

if validate_data(initial_data):
    print("✅ 初始数据验证通过")
else:
    print("❌ 初始数据验证失败")

app.layout = html.Div([
    html.H1("实时数据更新测试 - 修复版本", style={"textAlign": "center", "marginBottom": "20px"}),

    html.Div([
        html.P("此版本修复了数据验证问题，确保所有生成的数据都符合价格关系要求。",
               style={"textAlign": "center", "color": "#666", "marginBottom": "20px"})
    ]),

    html.Div([
        html.Button("开始实时更新", id="start-btn", n_clicks=0,
                   style={"marginRight": "10px", "padding": "10px 20px", "backgroundColor": "#28a745", "color": "white", "border": "none", "borderRadius": "4px"}),
        html.Button("停止更新", id="stop-btn", n_clicks=0,
                   style={"marginRight": "10px", "padding": "10px 20px", "backgroundColor": "#dc3545", "color": "white", "border": "none", "borderRadius": "4px"}),
        html.Button("添加一条数据", id="add-data-btn", n_clicks=0,
                   style={"padding": "10px 20px", "backgroundColor": "#007bff", "color": "white", "border": "none", "borderRadius": "4px"}),
    ], style={"margin": "20px", "textAlign": "center"}),

    html.Div([
        html.Div(id="status-info", style={"margin": "10px", "textAlign": "center", "fontSize": "16px", "fontWeight": "bold"}),
    ]),

    html.Div([
        DashKLineChart(
            id="realtime-chart",
            data=initial_data,
            config={
                "theme": "light",
                "grid": {"show": True},
                "crosshair": {"show": True},
            },
            indicators=[
                {"name": "MA", "params": [5, 10], "visible": True},
            ],
            style={"width": "100%", "height": "500px", "border": "1px solid #ddd", "borderRadius": "4px"},
        ),
    ], style={"margin": "20px"}),

    # 隐藏的存储组件
    dcc.Store(id="chart-data", data=initial_data),
    dcc.Store(id="is-running", data=False),
    dcc.Store(id="last-price", data=price),

    # 间隔组件用于自动更新
    dcc.Interval(
        id="interval-component",
        interval=2000,  # 2秒更新一次
        n_intervals=0,
        disabled=True
    ),
])

@app.callback(
    [Output("chart-data", "data"),
     Output("last-price", "data"),
     Output("status-info", "children")],
    [Input("add-data-btn", "n_clicks"),
     Input("interval-component", "n_intervals")],
    [State("chart-data", "data"),
     State("last-price", "data"),
     State("is-running", "data")]
)
def update_data(add_clicks, n_intervals, current_data, last_price, is_running):
    ctx = callback_context

    if not ctx.triggered:
        return current_data, last_price, f"数据点: {len(current_data)}"

    trigger_id = ctx.triggered[0]["prop_id"].split(".")[0]

    if trigger_id == "add-data-btn" or (trigger_id == "interval-component" and is_running):
        # 生成新数据点
        new_data = current_data.copy()

        # 生成新的时间戳
        last_timestamp = new_data[-1]["timestamp"] if new_data else int(time.time() * 1000)
        new_timestamp = last_timestamp + 86400 * 1000  # 增加1天

        # 使用验证过的数据生成函数
        new_point, new_price = generate_valid_kline_data(last_price, new_timestamp)

        new_data.append(new_point)

        # 保持最多100个数据点
        if len(new_data) > 100:
            new_data = new_data[-100:]

        status = f"数据点: {len(new_data)}, 最新价格: {new_point['close']:.2f}"
        if is_running:
            status += " (自动更新中)"

        return new_data, new_price, status

    return current_data, last_price, f"数据点: {len(current_data)}"

@app.callback(
    Output("realtime-chart", "data"),
    Input("chart-data", "data")
)
def update_chart(data):
    return data

@app.callback(
    [Output("interval-component", "disabled"),
     Output("is-running", "data")],
    [Input("start-btn", "n_clicks"),
     Input("stop-btn", "n_clicks")],
    [State("is-running", "data")]
)
def control_updates(start_clicks, stop_clicks, is_running):
    ctx = callback_context

    if not ctx.triggered:
        return True, False

    trigger_id = ctx.triggered[0]["prop_id"].split(".")[0]

    if trigger_id == "start-btn":
        return False, True  # 启用interval，设置运行状态
    elif trigger_id == "stop-btn":
        return True, False  # 禁用interval，设置停止状态

    return not is_running, not is_running

if __name__ == "__main__":
    print("🚀 启动实时数据更新测试（修复版本）...")
    print("📍 浏览器访问: http://127.0.0.1:8056")
    print("💡 修复内容:")
    print("   - 确保所有生成的数据都符合价格关系要求")
    print("   - high >= low")
    print("   - open 和 close 都在 [low, high] 范围内")
    print("   - 添加了数据验证函数")
    print("\n按 Ctrl+C 停止服务器")
    app.run_server(debug=True, port=8056)