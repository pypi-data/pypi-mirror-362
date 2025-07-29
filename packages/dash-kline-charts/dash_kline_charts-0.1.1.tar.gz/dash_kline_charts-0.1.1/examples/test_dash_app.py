import dash
from dash import html, dcc, Input, Output
import datetime
import random
from dash_kline_charts import DashKLineChart


# 创建测试数据
def create_sample_data(count=100):
    """创建示例K线数据"""
    data = []
    timestamp = int(
        (datetime.datetime.now() - datetime.timedelta(days=count)).timestamp() * 1000
    )
    price = 100.0

    for i in range(count):
        # 模拟价格变化
        change = random.uniform(-2, 2)
        price += change

        # 生成 OHLC 数据 (确保正确的价格关系)
        open_price = price
        close_price = price + random.uniform(-1, 1)

        # 确保 high 是 open 和 close 中的较大值，再加上一些随机增量
        high_price = max(open_price, close_price) + random.uniform(0, 1)

        # 确保 low 是 open 和 close 中的较小值，再减去一些随机增量
        low_price = min(open_price, close_price) - random.uniform(0, 1)

        volume = random.randint(1000, 10000)

        data.append(
            {
                "timestamp": timestamp,
                # "open": round(close_price, 2),
                # "high": round(close_price, 2),
                # "low": round(close_price, 2),
                "close": round(close_price, 2),
                # "volume": volume,
            }
        )

        timestamp += 86400 * 1000  # 增加1天
        price = close_price

    return data


# 创建应用
app = dash.Dash(__name__)

# 生成示例数据
sample_data = create_sample_data(50)

app.layout = html.Div(
    [
        html.H1("Dash KLineChart 测试", style={"textAlign": "center"}),
        html.Div(
            [
                html.H3("基础K线图"),
                DashKLineChart(
                    id="kline-chart-basic",
                    data=sample_data,
                    config={
                        "theme": "light",
                        "grid": {"show": True},
                        "candle": {"type": "area"},
                        "crosshair": {"show": True},
                    },
                    style={"width": "100%", "height": "400px"},
                ),
            ],
            style={"margin": "20px"},
        ),
        html.Div(
            [
                html.H3("深色主题K线图"),
                DashKLineChart(
                    id="kline-chart-dark",
                    data=sample_data,
                    config={
                        "theme": "dark",
                        "grid": {"show": True},
                        "crosshair": {"show": True},
                    },
                    style={"width": "100%", "height": "400px"},
                ),
            ],
            style={"margin": "20px"},
        ),
        html.Div(
            [
                html.H3("带技术指标的K线图"),
                DashKLineChart(
                    id="kline-chart-indicators",
                    data=sample_data,
                    config={
                        "theme": "light",
                        "grid": {"show": True},
                        "crosshair": {"show": True},
                    },
                    indicators=[
                        {"name": "MA", "params": [5, 10, 20], "visible": True},
                        {"name": "RSI", "params": [14], "visible": True},
                    ],
                    style={"width": "100%", "height": "400px"},
                ),
            ],
            style={"margin": "20px"},
        ),
        html.Div(
            [
                html.Button("刷新数据", id="refresh-btn", n_clicks=0),
                html.Div(id="data-info"),
            ],
            style={"margin": "20px"},
        ),
    ]
)


@app.callback(Output("data-info", "children"), Input("refresh-btn", "n_clicks"))
def update_data_info(n_clicks):
    return f"数据点数量: {len(sample_data)}, 刷新次数: {n_clicks}"


if __name__ == "__main__":
    print("启动Dash应用...")
    print("浏览器访问: http://127.0.0.1:8060")
    app.run_server(debug=True, port=8060)
