import dash
from dash import html, dcc, Input, Output
import datetime
import random
from dash_kline_charts import DashKLineChart


# 创建测试数据


# 创建面积图数据（只需要 timestamp 和 close）
def create_area_data(count=50):
    """创建面积图数据"""
    data = []
    timestamp = int(
        (datetime.datetime.now() - datetime.timedelta(days=count)).timestamp() * 1000
    )
    price = 100.0

    for i in range(count):
        # 模拟价格变化
        change = random.uniform(-2, 2)
        price += change

        data.append(
            {
                "timestamp": timestamp,
                "close": round(price, 2),
            }
        )

        timestamp += 86400 * 1000  # 增加1天

    return data


# 创建应用
app = dash.Dash(__name__)

# 生成示例数据

area_data = create_area_data(30)

app.layout = html.Div(
    [
        html.H1("Dash KLineChart 测试", style={"textAlign": "center"}),
        html.Div(
            [
                html.H3("area测试"),
                DashKLineChart(
                    id="kline-chart-area",
                    data=area_data,
                    config={
                        "theme": "light",
                        "grid": {"show": True},
                        "candle": {
                            "type": "area",
                            "tooltip": {
                                "title": {
                                    "show": False,
                                },
                                "legend": {
                                    "template": [
                                        {"title": "日期", "value": "{time}"},
                                        {"title": "收盘价", "value": "{close}"},
                                    ],
                                },
                            },
                        },
                    },
                    indicators=[
                        {
                            "name": "MA",
                            "isStack": False,
                            "paneOptions": {
                                "id": "candle_pane",
                            },
                            "calcParams": [60, 250],
                        },
                        {
                            "name": "EMA",
                            "isStack": True,
                            "paneOptions": {
                                "id": "candle_pane",
                            },
                        },
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
    return f"蜡烛图数据点数量: {len(area_data)}, 面积图数据点数量: {len(area_data)}, 刷新次数: {n_clicks}"


if __name__ == "__main__":
    print("启动Dash应用...")
    print("浏览器访问: http://127.0.0.1:8060")
    app.run_server(debug=True, port=8060)
