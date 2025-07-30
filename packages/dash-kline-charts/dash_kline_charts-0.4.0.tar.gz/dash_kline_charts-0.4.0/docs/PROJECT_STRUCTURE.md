# 项目结构说明

```
dash-kline-charts/
├── 📁 dash_kline_charts/           # Python 包主目录
│   ├── __init__.py                 # 包初始化文件
│   ├── _imports_.py                # 导入定义
│   ├── _version.py                 # 版本信息
│   ├── DashKLineChart.py           # 主组件类（自动生成）
│   ├── dash_kline_charts.min.js    # 编译后的 JS 文件
│   ├── dash_kline_charts.min.js.LICENSE.txt
│   ├── dash_kline_charts.min.js.map
│   ├── metadata.json               # 组件元数据
│   └── package-info.json           # 包信息
├── 📁 docs/                        # 文档目录
│   ├── API.md                      # API 文档
│   ├── CONTRIBUTING.md             # 贡献指南
│   └── PROJECT_STRUCTURE.md        # 项目结构说明
├── 📁 examples/                    # 示例应用
│   ├── README.md                   # 示例说明
│   ├── complete_example.py         # 完整功能示例
│   ├── realtime_test.py           # 实时更新测试
│   └── test_dash_app.py           # 基础测试应用
├── 📁 scripts/                     # 脚本文件
│   └── release.sh                  # 发布脚本
├── 📁 src/                         # 源代码目录
│   ├── components/                 # React 组件
│   │   ├── DashKLineChart.tsx      # 主组件 TypeScript 源码
│   │   └── DashKLineChart.test.tsx # 组件测试
│   ├── hooks/                      # React Hooks
│   │   └── index.ts                # Hooks 定义
│   ├── lib/                        # 库输出目录
│   │   ├── components/             # 编译后的组件
│   │   │   └── DashKLineChart.react.js
│   │   └── index.js                # 入口文件
│   ├── types/                      # TypeScript 类型定义
│   │   ├── index.ts                # 主类型定义
│   │   └── klinecharts.d.ts        # KLineChart 类型定义
│   ├── utils/                      # 工具函数
│   │   ├── index.ts                # 工具函数实现
│   │   └── index.test.ts           # 工具函数测试
│   ├── index.ts                    # TypeScript 入口文件
│   └── setupTests.ts               # 测试设置
├── 📁 tests/                       # Python 测试
│   ├── __init__.py                 # 测试包初始化
│   └── test_dash_kline_chart.py    # 主要测试文件
├── 📄 .babelrc                     # Babel 配置
├── 📄 .eslintrc.js                 # ESLint 配置
├── 📄 .gitignore                   # Git 忽略文件
├── 📄 CHANGELOG.md                 # 变更日志
├── 📄 CLAUDE.md                    # Claude 工作指南
├── 📄 jest.config.js               # Jest 测试配置
├── 📄 LICENSE                      # 许可证文件
├── 📄 MANIFEST.in                  # Python 包清单
├── 📄 package.json                 # Node.js 包配置
├── 📄 package-lock.json            # Node.js 依赖锁定
├── 📄 pyproject.toml               # Python 项目配置
├── 📄 README.md                    # 项目说明
├── 📄 setup.py                     # Python 安装脚本
├── 📄 tsconfig.json                # TypeScript 配置
└── 📄 webpack.config.js            # Webpack 配置
```

## 目录说明

### 📁 核心目录

- **`dash_kline_charts/`**: Python 包的主目录，包含所有运行时需要的文件
- **`src/`**: 源代码目录，包含 TypeScript/React 组件和相关工具
- **`examples/`**: 示例应用，展示组件的各种用法
- **`docs/`**: 文档目录，包含 API 文档和使用指南

### 📁 构建相关

- **`scripts/`**: 构建和发布脚本
- **`tests/`**: Python 测试文件

### 📄 配置文件

- **`.babelrc`**: Babel 转译配置
- **`.eslintrc.js`**: ESLint 代码检查配置
- **`jest.config.js`**: Jest 测试框架配置
- **`package.json`**: Node.js 项目配置和依赖
- **`pyproject.toml`**: Python 项目配置
- **`setup.py`**: Python 包安装脚本
- **`tsconfig.json`**: TypeScript 编译配置
- **`webpack.config.js`**: Webpack 打包配置

## 构建流程

1. **TypeScript 编译**: `src/` 中的 TypeScript 代码编译为 JavaScript
2. **Webpack 打包**: 将 React 组件打包为 `dash_kline_charts.min.js`
3. **Python 包生成**: 使用 `dash-generate-components` 生成 Python 包装器

## 开发工作流

1. **修改源码**: 在 `src/components/DashKLineChart.tsx` 中修改组件
2. **运行构建**: `npm run build` 编译 JavaScript 和生成 Python 包
3. **测试**: 运行 `examples/` 中的示例应用进行测试
4. **文档更新**: 更新 `docs/` 中的相关文档

## 发布流程

1. **版本更新**: 更新 `package.json` 和 `_version.py` 中的版本号
2. **构建**: 运行完整构建流程
3. **测试**: 运行所有测试确保功能正常
4. **发布**: 使用 `scripts/release.sh` 发布到 PyPI

## 注意事项

- `dash_kline_charts/DashKLineChart.py` 是自动生成的，不要手动修改
- 修改组件功能需要在 `src/components/DashKLineChart.tsx` 中进行
- 添加新功能后需要重新运行构建流程
- KLineChart 库通过 npm 包管理，不再需要静态文件