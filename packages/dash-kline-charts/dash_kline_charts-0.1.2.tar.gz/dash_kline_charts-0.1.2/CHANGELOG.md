# 更新日志

所有重要的项目更改都将记录在此文件中。

格式基于 [Keep a Changelog](https://keepachangelog.com/zh-CN/1.0.0/)，
并且本项目遵循 [语义化版本](https://semver.org/lang/zh-CN/) 规范。



## [0.1.0] - 2025-07-14

### 新增
- 🎉 首次发布 dash-kline-charts 组件
- 📈 集成 KLineChart 10.0.0-alpha8 库
- 🐍 完整的 Python Dash 接口
- ⚛️ React 组件基础架构
- 📊 支持多种图表类型：
  - 蜡烛图 (candle_solid)
  - 空心蜡烛图 (candle_stroke)
  - OHLC 图 (ohlc)
  - 面积图 (area)
- 📐 技术指标支持：
  - MA (移动平均线)
  - EMA (指数移动平均线)
  - RSI (相对强弱指数)
  - MACD (移动平均收敛散度)
  - BOLL (布林带)
- 🎨 主题支持：
  - 明亮主题 (light)
  - 暗黑主题 (dark)
  - 自定义主题配置
- 📱 响应式设计支持
- 🔧 完整的配置选项：
  - 网格配置
  - 十字线配置
  - 坐标轴配置
  - 样式配置
- 📝 数据验证和错误处理
- 🧪 完整的单元测试覆盖
- 📚 详细的文档和示例

### 功能特性
- **数据格式**: 支持标准 OHLC 数据格式
- **实时更新**: 支持动态数据更新
- **性能优化**: 基于 Canvas 的高性能渲染
- **类型安全**: 完整的 TypeScript 类型定义
- **易用性**: 简单的 Python API 接口

### 示例应用
- 基础示例 (basic_example.py)
- 高级示例 (advanced_example.py)
- 实时数据示例 (realtime_example.py)

### 技术栈
- **前端**: React 18+ + TypeScript
- **图表**: KLineChart 10.0.0-alpha8
- **后端**: Python 3.7+ + Dash 2.0+
- **构建**: Webpack 5 + Babel
- **测试**: Jest + React Testing Library + pytest

### 依赖
- React >= 16.14.0
- Dash >= 2.0.0
- KLineChart ^10.0.0-alpha8

## 开发信息

### 贡献者
- Dash KLineChart Team

### 许可证
- MIT License

### 支持
- GitHub Issues: 问题报告和功能请求
- GitHub Discussions: 社区讨论
- 文档: 完整的 API 文档和使用指南