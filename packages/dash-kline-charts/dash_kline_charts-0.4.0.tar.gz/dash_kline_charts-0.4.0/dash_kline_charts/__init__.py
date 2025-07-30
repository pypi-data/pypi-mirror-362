import os as _os
import sys as _sys
import json

import dash as _dash

# noinspection PyUnresolvedReferences
from ._imports_ import *
from ._imports_ import __all__

if not hasattr(_dash, "__plotly_dash") and not hasattr(_dash, "development"):
    print(
        "Dash was not successfully imported. "
        "Make sure you don't have a file "
        'named \n"dash.py" in your current directory.',
        file=_sys.stderr,
    )
    _sys.exit(1)

_basepath = _os.path.dirname(__file__)
_filepath = _os.path.abspath(_os.path.join(_basepath, "package-info.json"))
with open(_filepath) as f:
    package = json.load(f)

package_name = package["name"].replace(" ", "_").replace("-", "_")
__version__ = package["version"]

_current_path = _os.path.dirname(_os.path.abspath(__file__))

_this_module = _sys.modules[__name__]


async_resources = ["relative_package_path"]

_js_dist = [
    {
        "relative_package_path": "klinecharts.min.js",
        "namespace": "dash_kline_charts",
    },
    {
        "relative_package_path": "dash_kline_charts.min.js",
        "namespace": "dash_kline_charts",
    },
]

_css_dist = []


for _component in __all__:
    setattr(_this_module, _component, getattr(_this_module, _component))
    getattr(_this_module, _component)._js_dist = _js_dist
    getattr(_this_module, _component)._css_dist = _css_dist
