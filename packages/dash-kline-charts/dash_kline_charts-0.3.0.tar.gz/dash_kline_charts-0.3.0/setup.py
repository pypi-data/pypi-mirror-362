from setuptools import setup, find_packages
import os

# 读取 README 文件
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

# 读取版本信息
def get_version():
    version_file = os.path.join("dash_kline_charts", "_version.py")
    with open(version_file, "r", encoding="utf-8") as f:
        content = f.read()
        for line in content.split('\n'):
            if line.startswith('__version__'):
                return line.split('=')[1].strip().strip('"').strip("'")
    return "0.1.0"

setup(
    name="dash-kline-charts",
    version=get_version(),
    author="Yefei Fan",
    author_email="fyfcnc@hotmail.com",
    description="A Dash component for displaying financial charts using KLineCharts",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/kingzeus/dash-kline-charts",
    packages=find_packages(),
    include_package_data=True,
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Framework :: Dash",
        "Intended Audience :: Developers",
        "Intended Audience :: Financial and Insurance Industry",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Scientific/Engineering :: Visualization",
        "Topic :: Office/Business :: Financial",
    ],
    python_requires=">=3.7",
    install_requires=[
        "dash>=2.0.0",
        "plotly>=5.0.0",
    ],
    extras_require={
        "dev": [
            "pytest>=6.0.0",
            "pytest-cov>=2.0.0",
            "black>=21.0.0",
            "flake8>=3.8.0",
            "mypy>=0.910",
            "twine>=6.0.0",
        ],
    },
    package_data={
        "dash_kline_charts": [
            "*.json",
            "*.js",
            "*.css",
            "*.map",
        ],
    },
)
