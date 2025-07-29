# AUTO GENERATED FILE - DO NOT EDIT

from dash.development.base_component import Component, _explicitize_args


class DashKLineChart(Component):
    """A DashKLineChart component.
DashKLineChart is a Dash component for displaying financial charts using KLineChart v10.
It takes data in OHLC format and renders a beautiful, interactive candlestick chart.

Performance optimizations:
- useMemo and useCallback for performance optimization
- Separated initialization, data updates, config updates, and indicator updates
- ResizeObserver for responsive design
- Improved error handling and lifecycle management
- Better memory management and resource cleanup

Keyword arguments:

- id (string; optional):
    The ID used to identify this component in Dash callbacks.

- className (string; default ''):
    CSS class name.

- config (dict; optional):
    Chart configuration options including: - theme (string): Chart
    theme ('light' or 'dark') - grid (object): Grid configuration -
    candle (object): Candle configuration - crosshair (object):
    Crosshair configuration - yAxis (object): Y-axis configuration -
    xAxis (object): X-axis configuration.

- data (list of dicts; optional):
    The K-line data in OHLC format. Each item should be an object
    with: - timestamp (number): Timestamp in milliseconds - open
    (number): Opening price - high (number): Highest price - low
    (number): Lowest price - close (number): Closing price - volume
    (number, optional): Trading volume.

    `data` is a list of dicts with keys:

    - timestamp (number; required)

    - open (number; required)

    - high (number; required)

    - low (number; required)

    - close (number; required)

    - volume (number; optional)

- indicators (list of dicts; optional):
    Technical indicators configuration. Each item should be an object
    with: - name (string): Indicator name (e.g., 'MA', 'RSI', 'MACD')
    - params (array): Indicator parameters - visible (boolean,
    optional): Whether the indicator is visible.

    `indicators` is a list of dicts with keys:

    - name (string; required)

    - params (list; optional)

    - visible (boolean; optional)

- responsive (boolean; default True):
    Whether to enable responsive design.

- style (dict; optional):
    CSS style properties.

- symbol (string; optional):
    Symbol information for the chart."""
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
