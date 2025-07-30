# AUTO GENERATED FILE - DO NOT EDIT

from dash.development.base_component import Component, _explicitize_args


class DashKLineChart(Component):
    """A DashKLineChart component.
DashKLineChart 是一个使用 KLineChart v10 显示金融图表的 Dash 组件。
它接受 OHLC 格式的数据，并渲染出美观的交互式蜡烛图。

功能特性：
- 多种图表类型：蜡烛图、面积图、线图
- 技术指标：MA、RSI、MACD 等
- 交互式十字线和缩放功能
- 明暗主题
- 响应式设计，自动调整大小
- 实时数据更新

@example
```python
import dash_kline_charts as dkc

dkc.DashKLineChart(
    id='my-chart',
    data=[
        {'timestamp': 1609459200000, 'open': 100, 'high': 110, 'low': 90, 'close': 105, 'volume': 1000},
        # ... more data
    ],
    config={'theme': 'dark', 'grid': {'show': True}},
    indicators=[{'name': 'MA', 'params': [5, 10, 20]}]
)
```

Keyword arguments:

- id (string; optional):
    用于在 Dash 回调中识别此组件的 ID。.

- className (string; default ''):
    CSS 类名.

- config (dict; optional):
    图表配置选项。此对象允许您自定义图表外观和行为。<br/><br/> 可用选项：<br/> - theme (string):
    图表主题（'light' 或 'dark'）。默认：'light'<br/> - grid (object): 网格配置<br/>
    - show (boolean): 是否显示网格线<br/>   - horizontal (object):
    水平网格线设置<br/>   - vertical (object): 垂直网格线设置<br/> - candle
    (object): 蜡烛图/图表类型配置<br/>   - type (string): 图表类型（'candle_solid',
    'area', 'line'）<br/>   - tooltip (object): 图例提示<br/>     - title
    (object): 标题配置<br/>       - show (boolean): 是否显示标题<br/>     -
    legend (object): 图例设置<br/>       - template (array):
    图例模板，包含多个对象，每个对象有 title 和 value 字段<br/> - crosshair (object):
    十字线配置<br/>   - show (boolean): 是否显示十字线<br/>   -
    horizontal/vertical (object): 十字线设置<br/> - yAxis (object): Y
    轴配置<br/>   - show (boolean): 是否显示 Y 轴<br/>   - position (string):
    Y 轴位置（'left' 或 'right'）<br/> - xAxis (object): X 轴配置<br/>   - show
    (boolean): 是否显示 X 轴<br/>   - position (string): X 轴位置（'top' 或
    'bottom'）<br/><br/> @example config={   'theme': 'dark',   'grid':
    {'show': True, 'horizontal': {'show': True}},   'candle': {'type':
    'area'},   'crosshair': {'show': True} }.

- data (list of dicts; optional):
    OHLC 格式的 K 线数据。每个数据项应该是一个包含以下字段的对象：<br/> - timestamp (number):
    时间戳（毫秒）<br/> - open (number): 开盘价, 面积图时可忽略<br/> - high (number):
    最高价, 面积图时可忽略<br/> - low (number): 最低价, 面积图时可忽略<br/> - close
    (number): 收盘价<br/> - volume (number, 可选): 交易量.

    `data` is a list of dicts with keys:

    - timestamp (number; required)

    - open (number; optional)

    - high (number; optional)

    - low (number; optional)

    - close (number; required)

    - volume (number; optional)

- indicators (list of dicts; optional):
    技术指标配置。每个指标项应该是一个包含以下字段的对象：<br/> - name (string): 指标名称（例如：'MA',
    'RSI', 'MACD'）<br/> - calcParams (array): 指标参数<br/> - isStack
    (boolean, 可选): 是否堆叠<br/> - paneOptions (object, 可选): 指标面板选项<br/>
    - id (string, 可选): 指标面板 ID<br/> - styles (object, 可选): 指标样式<br/>
    - lines (array, 可选): 指标线样式<br/>          - color (string, 可选):
    指标线颜色<br/>          - style (string, 可选): 指标线样式（'solid' 或
    'dashed'）<br/> - visible (boolean, 可选): 指标是否可见.

    `indicators` is a list of dicts with keys:

    - name (string; required)

    - isStack (boolean; optional)

    - paneOptions (dict; optional)

    - calcParams (list; optional)

    - styles (dict; optional)

    - visible (boolean; optional)

- responsive (boolean; default True):
    是否启用响应式设计。启用后，当窗口或容器大小发生变化时， 图表将自动调整大小以适应其容器。  @default True.

- style (dict; optional):
    CSS 样式属性.

- symbol (string; optional):
    图表的交易品种信息."""
    _children_props = []
    _base_nodes = ['children']
    _namespace = 'dash_kline_charts'
    _type = 'DashKLineChart'
    @_explicitize_args
    def __init__(self, id=Component.UNDEFINED, data=Component.UNDEFINED, config=Component.UNDEFINED, indicators=Component.UNDEFINED, symbol=Component.UNDEFINED, style=Component.UNDEFINED, className=Component.UNDEFINED, responsive=Component.UNDEFINED, **kwargs):
        self._prop_names = ['id', 'className', 'config', 'data', 'indicators', 'responsive', 'style', 'symbol']
        self._valid_wildcard_attributes =            []
        self.available_properties = ['id', 'className', 'config', 'data', 'indicators', 'responsive', 'style', 'symbol']
        self.available_wildcard_properties =            []
        _explicit_args = kwargs.pop('_explicit_args')
        _locals = locals()
        _locals.update(kwargs)  # For wildcard attrs and excess named props
        args = {k: _locals[k] for k in _explicit_args}

        super(DashKLineChart, self).__init__(**args)
