# 📚 dash-kline-charts 文档指南

本指南解释了如何维护和更新由 `dash-generate-components` 自动生成的 `DashKLineChart` 组件文档。

## 🔍 文档生成机制

`dash-generate-components` 工具会自动从 React 组件源代码中提取文档，并生成相应的 Python 文档。文档来源包括：

1. **组件描述**：组件函数上方的 JSDoc 注释
2. **属性文档**：每个 PropType 定义上方的 JSDoc 注释
3. **类型信息**：从 PropTypes 定义中自动推断
4. **默认值**：从 defaultProps 中提取

## ✏️ 如何更新文档

### 1. 组件主要描述

编辑 `src/lib/components/DashKLineChart.react.js` 中组件函数上方的 JSDoc 注释：

````javascript
/**
 * DashKLineChart 是一个使用 KLineChart v10 显示金融图表的 Dash 组件。
 * 它接受 OHLC 格式的数据，并渲染出美观的交互式蜡烛图。
 *
 * 功能特性：
 * - 多种图表类型：蜡烛图、面积图、线图
 * - 技术指标：MA、RSI、MACD 等
 * - 交互式十字线和缩放功能
 *
 * @example
 * ```python
 * import dash_kline_charts as dkc
 *
 * dkc.DashKLineChart(
 *     id='my-chart',
 *     data=[...],
 *     config={'theme': 'dark'}
 * )
 * ```
 */
const DashKLineChart = ({ ... }) => {
````

### 2. 属性文档

更新每个 PropType 定义上方的 JSDoc 注释：

```javascript
DashKLineChart.propTypes = {
  /**
   * 用于在 Dash 回调中识别此组件的 ID。
   */
  id: PropTypes.string,

  /**
   * 图表配置选项。此对象允许您自定义图表外观。
   *
   * 可用选项：
   * - theme (string): 图表主题（'light' 或 'dark'）。默认：'light'
   * - grid (object): 网格配置
   *   - show (boolean): 是否显示网格线
   *
   * @example
   * config={
   *   'theme': 'dark',
   *   'grid': {'show': True}
   * }
   */
  config: PropTypes.object,
};
```

### 3. 默认值

更新 defaultProps 以确保正确的默认值被记录：

```javascript
DashKLineChart.defaultProps = {
  data: [],
  config: {},
  indicators: [],
  style: {},
  className: "",
  responsive: true,
};
```

## 🔄 重新生成流程

在对 React 组件中的文档进行更改后：

1. **保存更改** 到 `src/lib/components/DashKLineChart.react.js`
2. **重新生成 Python 组件**：
   ```bash
   npm run build:backends
   ```
3. **验证更改** 在 `dash_kline_charts/DashKLineChart.py` 中

## 📝 文档最佳实践

### 1. 使用清晰的描述

- 从属性的作用开始说明
- 解释预期的格式/类型
- 提供使用场景的上下文

### 2. 包含示例

- 使用 `@example` 标签添加代码示例
- 展示实际的使用模式
- 包括简单和复杂的示例

### 3. 记录对象属性

- 对于对象属性，记录嵌套结构
- 使用缩进显示层次结构
- 指定必需与可选的嵌套属性

### 4. 指定默认值

- 在有帮助的地方使用 `@default` 标签
- 确保 defaultProps 与文档匹配

## 🚫 不要编辑的内容

**永远不要直接编辑这些文件** - 它们是自动生成的：

- `dash_kline_charts/DashKLineChart.py`
- `dash_kline_charts/_imports_.py`
- `dash_kline_charts/metadata.json`
- `dash_kline_charts/package-info.json`

## 📖 生成的 Python 文档结构

生成的 Python 文档遵循以下结构：

```python
class DashKLineChart(Component):
    """一个 DashKLineChart 组件。
    [来自 JSDoc 的组件主要描述]

    [来自 JSDoc 的功能和示例]

    关键字参数：

    - property_name (type; default value):
        [来自 PropType JSDoc 的属性描述]

        [附加详细信息和示例]
    """
```

## 🔍 故障排除

### 文档未更新

1. 检查您的 JSDoc 语法是否正确
2. 确保您正在编辑 React 组件，而不是生成的 Python 文件
3. 运行 `npm run build:backends` 重新生成
4. 检查控制台中是否有构建错误

### 格式问题

- 使用正确的 JSDoc 语法（`/**` 开始，`*/` 结束）
- 在每行开头使用 `*`
- 适当使用 `@example`、`@default` 标签

### 类型信息不正确

- 检查您的 PropTypes 定义
- 确保 defaultProps 与您的文档匹配
- 验证必需属性是否正确标记

## 📚 其他资源

- [JSDoc 文档](https://jsdoc.app/)
- [React PropTypes](https://reactjs.org/docs/typechecking-with-proptypes.html)
- [Dash 组件开发](https://dash.plotly.com/plugins)
