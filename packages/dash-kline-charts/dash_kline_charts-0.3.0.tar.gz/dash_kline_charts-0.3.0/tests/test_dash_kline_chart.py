"""
Tests for dash_kline_charts Python component
"""

import unittest
import pytest
from dash_kline_charts import DashKLineChart


class TestDashKLineChart(unittest.TestCase):
    """Test cases for DashKLineChart component"""

    def setUp(self):
        """Set up test fixtures"""
        self.valid_data = [
            {
                'timestamp': 1609459200000,
                'open': 100.0,
                'high': 110.0,
                'low': 95.0,
                'close': 105.0,
                'volume': 1000
            },
            {
                'timestamp': 1609545600000,
                'open': 105.0,
                'high': 115.0,
                'low': 100.0,
                'close': 110.0,
                'volume': 1200
            }
        ]

    def test_component_creation_with_default_values(self):
        """Test component creation with default values"""
        component = DashKLineChart()
        
        self.assertIsNotNone(component)
        # Without explicit values, properties should not exist as attributes
        self.assertFalse(hasattr(component, 'responsive'))
        self.assertFalse(hasattr(component, 'className'))
        self.assertFalse(hasattr(component, 'style'))
        self.assertFalse(hasattr(component, 'config'))
        self.assertFalse(hasattr(component, 'data'))
        self.assertFalse(hasattr(component, 'indicators'))

    def test_component_creation_with_valid_data(self):
        """Test component creation with valid data"""
        component = DashKLineChart(data=self.valid_data)
        
        self.assertIsNotNone(component)
        self.assertEqual(component.data, self.valid_data)
        # Only data property should exist since we only set that
        self.assertTrue(hasattr(component, 'data'))
        self.assertFalse(hasattr(component, 'responsive'))

    def test_component_creation_with_all_params(self):
        """Test component creation with all parameters"""
        config = {
            'theme': 'dark',
            'grid': {'show': True},
            'candle': {'type': 'candle_solid'}
        }
        
        indicators = [
            {'name': 'MA', 'params': [5, 10, 20]},
            {'name': 'RSI', 'params': [14]}
        ]
        
        style = {'height': '600px', 'width': '100%'}
        
        component = DashKLineChart(
            id='test-chart',
            data=self.valid_data,
            config=config,
            indicators=indicators,
            style=style,
            className='custom-class',
            responsive=False,
            symbol='AAPL'
        )
        
        self.assertEqual(component.id, 'test-chart')
        self.assertEqual(component.data, self.valid_data)
        self.assertEqual(component.config, config)
        self.assertEqual(component.indicators, indicators)
        self.assertEqual(component.style, style)
        self.assertEqual(component.className, 'custom-class')
        self.assertEqual(component.responsive, False)
        self.assertEqual(component.symbol, 'AAPL')

    def test_component_properties_in_prop_names(self):
        """Test that all expected properties are in _prop_names"""
        component = DashKLineChart()
        
        expected_props = ['id', 'className', 'config', 'data', 'indicators', 'responsive', 'style', 'symbol']
        
        for prop in expected_props:
            self.assertIn(prop, component._prop_names)

    def test_component_available_properties(self):
        """Test that all expected properties are in available_properties"""
        component = DashKLineChart()
        
        expected_props = ['id', 'className', 'config', 'data', 'indicators', 'responsive', 'style', 'symbol']
        
        for prop in expected_props:
            self.assertIn(prop, component.available_properties)

    def test_component_namespace_and_type(self):
        """Test component namespace and type"""
        component = DashKLineChart()
        
        self.assertEqual(component._namespace, 'dash_kline_charts')
        self.assertEqual(component._type, 'DashKLineChart')

    def test_component_with_empty_data(self):
        """Test component with empty data"""
        component = DashKLineChart(data=[])
        
        self.assertEqual(component.data, [])
        self.assertIsNotNone(component)

    def test_component_with_minimal_data(self):
        """Test component with minimal data (no volume)"""
        minimal_data = [
            {
                'timestamp': 1609459200000,
                'open': 100.0,
                'high': 110.0,
                'low': 95.0,
                'close': 105.0
            }
        ]
        
        component = DashKLineChart(data=minimal_data)
        self.assertEqual(component.data, minimal_data)

    def test_component_with_indicators(self):
        """Test component with various indicators"""
        indicators = [
            {'name': 'MA', 'params': [5, 10, 20], 'visible': True},
            {'name': 'RSI', 'params': [14], 'visible': False},
            {'name': 'MACD', 'params': [12, 26, 9]}
        ]
        
        component = DashKLineChart(indicators=indicators)
        self.assertEqual(component.indicators, indicators)

    def test_component_with_theme_config(self):
        """Test component with theme configuration"""
        light_config = {'theme': 'light'}
        dark_config = {'theme': 'dark'}
        
        light_component = DashKLineChart(config=light_config)
        dark_component = DashKLineChart(config=dark_config)
        
        self.assertEqual(light_component.config, light_config)
        self.assertEqual(dark_component.config, dark_config)

    def test_component_with_complex_config(self):
        """Test component with complex configuration"""
        complex_config = {
            'theme': 'dark',
            'grid': {
                'show': True,
                'horizontal': {'show': True, 'size': 1, 'color': '#393939'},
                'vertical': {'show': True, 'size': 1, 'color': '#393939'}
            },
            'candle': {
                'type': 'candle_solid',
                'priceMark': {'show': True, 'high': {'show': True}, 'low': {'show': True}}
            },
            'crosshair': {
                'show': True,
                'horizontal': {'show': True, 'line': {'show': True}},
                'vertical': {'show': True, 'line': {'show': True}}
            }
        }
        
        component = DashKLineChart(config=complex_config)
        self.assertEqual(component.config, complex_config)

    def test_component_styling(self):
        """Test component styling options"""
        style = {
            'height': '500px',
            'width': '100%',
            'backgroundColor': '#1a1a1a',
            'border': '1px solid #333'
        }
        
        component = DashKLineChart(style=style, className='my-chart')
        self.assertEqual(component.style, style)
        self.assertEqual(component.className, 'my-chart')

    def test_component_responsive_flag(self):
        """Test responsive flag behavior"""
        responsive_component = DashKLineChart(responsive=True)
        non_responsive_component = DashKLineChart(responsive=False)
        
        self.assertTrue(responsive_component.responsive)
        self.assertFalse(non_responsive_component.responsive)

    def test_component_symbol_property(self):
        """Test symbol property"""
        symbols = ['AAPL', 'GOOGL', 'MSFT', 'TSLA']
        
        for symbol in symbols:
            component = DashKLineChart(symbol=symbol)
            self.assertEqual(component.symbol, symbol)

    def test_component_with_large_dataset(self):
        """Test component with large dataset"""
        large_data = []
        base_timestamp = 1609459200000
        
        for i in range(1000):
            timestamp = base_timestamp + (i * 86400000)  # Add 1 day
            large_data.append({
                'timestamp': timestamp,
                'open': 100 + (i * 0.1),
                'high': 110 + (i * 0.1),
                'low': 90 + (i * 0.1),
                'close': 105 + (i * 0.1),
                'volume': 1000 + (i * 10)
            })
        
        component = DashKLineChart(data=large_data)
        self.assertEqual(len(component.data), 1000)
        self.assertEqual(component.data[0]['timestamp'], base_timestamp)

    def test_component_inheritance(self):
        """Test that DashKLineChart inherits from Dash Component"""
        from dash.development.base_component import Component
        
        component = DashKLineChart()
        self.assertIsInstance(component, Component)

    def test_component_undefined_values(self):
        """Test component with undefined values"""
        from dash.development.base_component import Component
        
        component = DashKLineChart(
            data=Component.UNDEFINED,
            config=Component.UNDEFINED
        )
        
        self.assertEqual(component.data, Component.UNDEFINED)
        self.assertEqual(component.config, Component.UNDEFINED)
        # These properties should exist since we explicitly set them
        self.assertTrue(hasattr(component, 'data'))
        self.assertTrue(hasattr(component, 'config'))
        # id should not exist since we didn't set it
        self.assertFalse(hasattr(component, 'id'))


if __name__ == '__main__':
    unittest.main()