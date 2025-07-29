import dash
from dash import html, dcc, Input, Output
import datetime
import random
from dash_kline_charts import DashKLineChart

# 创建应用
app = dash.Dash(__name__)

# 生成示例数据
def create_sample_data(count=100):
    """生成示例K线数据"""
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

# 初始数据
sample_data = create_sample_data(50)

app.layout = html.Div([
    html.H1("Dash KLineChart 完整示例", style={'textAlign': 'center', 'marginBottom': '30px'}),
    
    # 控制面板
    html.Div([
        html.Div([
            html.Label("主题选择:", style={'fontWeight': 'bold', 'marginBottom': '10px'}),
            dcc.Dropdown(
                id='theme-dropdown',
                options=[
                    {'label': '明亮主题', 'value': 'light'},
                    {'label': '暗黑主题', 'value': 'dark'}
                ],
                value='light',
                style={'width': '150px'}
            )
        ], style={'display': 'inline-block', 'margin': '0 20px'}),
        
        html.Div([
            html.Label("图表类型:", style={'fontWeight': 'bold', 'marginBottom': '10px'}),
            dcc.Dropdown(
                id='chart-type-dropdown',
                options=[
                    {'label': '实心蜡烛图', 'value': 'candle_solid'},
                    {'label': '空心蜡烛图', 'value': 'candle_stroke'},
                    {'label': 'OHLC 图', 'value': 'ohlc'}
                ],
                value='candle_solid',
                style={'width': '150px'}
            )
        ], style={'display': 'inline-block', 'margin': '0 20px'}),
        
        html.Div([
            html.Label("技术指标:", style={'fontWeight': 'bold', 'marginBottom': '10px'}),
            dcc.Checklist(
                id='indicator-checklist',
                options=[
                    {'label': '移动平均线 (MA)', 'value': 'MA'},
                    {'label': '相对强弱指数 (RSI)', 'value': 'RSI'},
                    {'label': 'MACD', 'value': 'MACD'}
                ],
                value=['MA'],
                style={'fontSize': '14px'}
            )
        ], style={'display': 'inline-block', 'margin': '0 20px', 'verticalAlign': 'top'}),
        
        html.Div([
            html.Label("显示选项:", style={'fontWeight': 'bold', 'marginBottom': '10px'}),
            dcc.Checklist(
                id='display-options',
                options=[
                    {'label': '网格线', 'value': 'grid'},
                    {'label': '十字线', 'value': 'crosshair'},
                    {'label': '响应式', 'value': 'responsive'}
                ],
                value=['grid', 'crosshair', 'responsive'],
                style={'fontSize': '14px'}
            )
        ], style={'display': 'inline-block', 'margin': '0 20px', 'verticalAlign': 'top'})
    ], style={'textAlign': 'center', 'padding': '20px', 'backgroundColor': '#f5f5f5', 'margin': '20px'}),
    
    # 图表容器
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
    
    # 信息面板
    html.Div([
        html.Div([
            html.Button('刷新数据', id='refresh-btn', n_clicks=0, 
                       style={'padding': '10px 20px', 'fontSize': '16px', 'marginRight': '10px'}),
            html.Button('添加数据点', id='add-data-btn', n_clicks=0,
                       style={'padding': '10px 20px', 'fontSize': '16px', 'marginRight': '10px'}),
            html.Button('清空数据', id='clear-data-btn', n_clicks=0,
                       style={'padding': '10px 20px', 'fontSize': '16px'})
        ], style={'textAlign': 'center', 'marginBottom': '20px'}),
        
        html.Div(id='data-info', style={'textAlign': 'center', 'fontSize': '16px', 'fontWeight': 'bold'}),
        
        html.Div([
            html.H3("当前配置:", style={'marginBottom': '10px'}),
            html.Pre(id='config-info', style={'backgroundColor': '#f8f9fa', 'padding': '10px', 'borderRadius': '5px'})
        ], style={'margin': '20px'})
    ], style={'backgroundColor': '#f8f9fa', 'padding': '20px', 'margin': '20px', 'borderRadius': '10px'})
])

# 主题和图表类型更新回调
@app.callback(
    [Output('kline-chart', 'config'),
     Output('config-info', 'children')],
    [Input('theme-dropdown', 'value'),
     Input('chart-type-dropdown', 'value'),
     Input('display-options', 'value')]
)
def update_chart_config(theme, chart_type, display_options):
    config = {
        'theme': theme,
        'grid': {'show': 'grid' in display_options},
        'candle': {'type': chart_type},
        'crosshair': {'show': 'crosshair' in display_options}
    }
    
    config_text = f"""主题: {theme}
图表类型: {chart_type}
网格线: {'显示' if 'grid' in display_options else '隐藏'}
十字线: {'显示' if 'crosshair' in display_options else '隐藏'}
响应式: {'启用' if 'responsive' in display_options else '禁用'}"""
    
    return config, config_text

# 技术指标更新回调
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

# 响应式设置更新回调
@app.callback(
    Output('kline-chart', 'responsive'),
    Input('display-options', 'value')
)
def update_responsive(display_options):
    return 'responsive' in display_options

# 数据操作回调
@app.callback(
    [Output('kline-chart', 'data'),
     Output('data-info', 'children')],
    [Input('refresh-btn', 'n_clicks'),
     Input('add-data-btn', 'n_clicks'),
     Input('clear-data-btn', 'n_clicks')],
    prevent_initial_call=True
)
def update_data(refresh_clicks, add_clicks, clear_clicks):
    ctx = dash.callback_context
    if not ctx.triggered:
        return sample_data, f'数据点数量: {len(sample_data)}'
    
    trigger_id = ctx.triggered[0]['prop_id'].split('.')[0]
    
    if trigger_id == 'refresh-btn':
        new_data = create_sample_data(50)
        return new_data, f'数据已刷新，共 {len(new_data)} 个数据点'
    elif trigger_id == 'add-data-btn':
        # 添加新数据点到现有数据
        current_data = sample_data.copy()
        if current_data:
            last_timestamp = current_data[-1]['timestamp']
            last_price = current_data[-1]['close']
        else:
            last_timestamp = int(datetime.datetime.now().timestamp() * 1000)
            last_price = 100.0
        
        new_timestamp = last_timestamp + 86400 * 1000
        change = random.uniform(-1, 1)
        new_price = last_price + change
        
        new_point = {
            'timestamp': new_timestamp,
            'open': round(new_price, 2),
            'high': round(new_price + random.uniform(0, 0.5), 2),
            'low': round(new_price - random.uniform(0, 0.5), 2),
            'close': round(new_price + random.uniform(-0.25, 0.25), 2),
            'volume': random.randint(1000, 10000)
        }
        
        current_data.append(new_point)
        return current_data, f'已添加数据点，共 {len(current_data)} 个数据点'
    elif trigger_id == 'clear-data-btn':
        return [], '数据已清空'
    
    return sample_data, f'数据点数量: {len(sample_data)}'

if __name__ == '__main__':
    print("启动完整示例应用...")
    print("浏览器访问: http://127.0.0.1:8054")
    app.run_server(debug=True, port=8054)