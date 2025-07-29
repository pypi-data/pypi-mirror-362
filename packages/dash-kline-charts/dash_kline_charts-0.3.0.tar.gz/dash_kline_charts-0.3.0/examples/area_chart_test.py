#!/usr/bin/env python3
"""
面积图测试
测试当 candle.type 为 'area' 时，tooltip.legend 只显示 close 值
"""

import dash
from dash import html, dcc, callback, Input, Output
import dash_kline_charts as dkc
import json

# 创建测试数据 - 简化数据，只包含 timestamp 和 close
area_data = [
    {"timestamp": 1609459200000, "close": 100},
    {"timestamp": 1609545600000, "close": 102},
    {"timestamp": 1609632000000, "close": 98},
    {"timestamp": 1609718400000, "close": 105},
    {"timestamp": 1609804800000, "close": 110},
    {"timestamp": 1609891200000, "close": 108},
    {"timestamp": 1609977600000, "close": 112},
    {"timestamp": 1610064000000, "close": 115},
    {"timestamp": 1610150400000, "close": 113},
    {"timestamp": 1610236800000, "close": 118},
]

# 创建完整的 OHLC 数据用于对比
candle_data = [
    {"timestamp": 1609459200000, "open": 100, "high": 105, "low": 95, "close": 100, "volume": 1000},
    {"timestamp": 1609545600000, "open": 100, "high": 107, "low": 98, "close": 102, "volume": 1200},
    {"timestamp": 1609632000000, "open": 102, "high": 104, "low": 92, "close": 98, "volume": 1500},
    {"timestamp": 1609718400000, "open": 98, "high": 110, "low": 96, "close": 105, "volume": 800},
    {"timestamp": 1609804800000, "open": 105, "high": 115, "low": 103, "close": 110, "volume": 900},
    {"timestamp": 1609891200000, "open": 110, "high": 112, "low": 105, "close": 108, "volume": 1100},
    {"timestamp": 1609977600000, "open": 108, "high": 118, "low": 106, "close": 112, "volume": 1300},
    {"timestamp": 1610064000000, "open": 112, "high": 120, "low": 110, "close": 115, "volume": 700},
    {"timestamp": 1610150400000, "open": 115, "high": 117, "low": 108, "close": 113, "volume": 1000},
    {"timestamp": 1610236800000, "open": 113, "high": 122, "low": 112, "close": 118, "volume": 1400},
]

app = dash.Dash(__name__)

app.layout = html.Div([
    html.H1("面积图 vs 蜡烛图 Tooltip 测试", style={'textAlign': 'center'}),
    
    html.Div([
        html.H3("面积图 (只显示 Close)", style={'textAlign': 'center'}),
        html.P("配置: candle.type = 'area', tooltip.legend.ohlc.show = false", 
               style={'textAlign': 'center', 'color': 'gray'}),
        dkc.DashKLineChart(
            id='area-chart',
            data=area_data,
            config={
                'theme': 'light',
                'candle': {'type': 'area'},
                'grid': {'show': True},
                'crosshair': {'show': True}
            },
            style={'height': '400px', 'border': '1px solid #ddd', 'margin': '10px'}
        )
    ], style={'width': '48%', 'display': 'inline-block', 'verticalAlign': 'top'}),
    
    html.Div([
        html.H3("蜡烛图 (显示完整 OHLC)", style={'textAlign': 'center'}),
        html.P("配置: candle.type = 'candle_solid' (默认)", 
               style={'textAlign': 'center', 'color': 'gray'}),
        dkc.DashKLineChart(
            id='candle-chart',
            data=candle_data,
            config={
                'theme': 'light',
                'candle': {'type': 'candle_solid'},
                'grid': {'show': True},
                'crosshair': {'show': True}
            },
            style={'height': '400px', 'border': '1px solid #ddd', 'margin': '10px'}
        )
    ], style={'width': '48%', 'display': 'inline-block', 'verticalAlign': 'top'}),
    
    html.Div([
        html.H3("测试说明", style={'margin': '20px 0'}),
        html.Ul([
            html.Li("左侧面积图应该只在 tooltip 中显示 Close 价格"),
            html.Li("右侧蜡烛图应该在 tooltip 中显示完整的 OHLC 数据"),
            html.Li("将鼠标悬停在图表上查看 tooltip 效果"),
            html.Li("验证面积图的 tooltip 不显示 Open、High、Low 数据")
        ])
    ], style={'margin': '20px', 'padding': '20px', 'backgroundColor': '#f9f9f9'})
])

if __name__ == '__main__':
    app.run_server(debug=True, port=8051)