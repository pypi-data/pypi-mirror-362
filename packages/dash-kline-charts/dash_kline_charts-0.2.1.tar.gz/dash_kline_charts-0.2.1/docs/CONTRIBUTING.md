# 贡献指南

感谢您对 dash-kline-charts 项目的兴趣！我们欢迎各种形式的贡献。

## 开发环境设置

### 环境要求

- Python 3.7+
- Node.js 16+
- npm 或 yarn

### 安装开发依赖

```bash
# 克隆项目
git clone https://github.com/your-username/dash-kline-charts.git
cd dash-kline-charts

# 安装 Python 依赖
pip install -r requirements.txt
pip install -e .

# 安装 JavaScript 依赖
npm install
```

### 项目结构

```
dash-kline-charts/
├── src/                    # React 组件源码
│   ├── components/         # 组件
│   ├── types/             # TypeScript 类型定义
│   ├── utils/             # 工具函数
│   └── hooks/             # 自定义 Hooks
├── dash_kline_charts/     # Python 包
├── examples/              # 示例应用
├── tests/                 # 测试文件
├── docs/                  # 文档
└── lib/                   # 构建输出
```

## 开发流程

### 1. 创建分支

```bash
git checkout -b feature/your-feature-name
```

### 2. 开发

#### React 组件开发

```bash
# 启动开发服务器
npm run dev

# 类型检查
npm run type-check

# 代码检查
npm run lint
npm run lint:fix
```

#### Python 开发

```bash
# 运行示例
python examples/basic_example.py

# 运行测试
python -m pytest tests/
```

### 3. 测试

```bash
# JavaScript 测试
npm test
npm run test:watch

# Python 测试
python -m pytest tests/ -v
```

### 4. 构建

```bash
# 构建 JavaScript 组件
npm run build

# 构建 Python 包
python setup.py sdist bdist_wheel
```

## 编码规范

### TypeScript/JavaScript

- 使用 TypeScript 进行类型安全
- 遵循 ESLint 配置
- 使用 Prettier 格式化代码
- 组件使用函数式组件和 Hooks
- 导出类型定义

### Python

- 遵循 PEP 8 代码风格
- 使用类型注解
- 编写详细的文档字符串
- 使用 Black 格式化代码

### 提交信息

遵循 [约定式提交](https://www.conventionalcommits.org/zh-hans/v1.0.0/) 规范：

```
<类型>[可选 范围]: <描述>

[可选 正文]

[可选 脚注]
```

类型：
- `feat`: 新功能
- `fix`: 修复
- `docs`: 文档
- `style`: 样式
- `refactor`: 重构
- `test`: 测试
- `chore`: 构建过程或辅助工具的变动

示例：
```
feat: 添加实时数据更新功能

- 实现 WebSocket 连接
- 添加数据缓存机制
- 更新示例应用

Closes #123
```

## 测试要求

### 新功能要求

1. **单元测试**: 每个新功能都必须有相应的单元测试
2. **集成测试**: 复杂功能需要集成测试
3. **示例代码**: 提供使用示例

### 测试覆盖率

- JavaScript: 最低 80%
- Python: 最低 85%

### 测试运行

```bash
# JavaScript 测试和覆盖率
npm test -- --coverage

# Python 测试和覆盖率
python -m pytest tests/ --cov=dash_kline_charts --cov-report=html
```

## 文档

### 更新文档

当添加新功能时，请同时更新：

1. `README.md` - 如果是主要功能
2. `docs/API.md` - API 文档
3. 示例文件 - 在 `examples/` 目录中
4. 类型定义 - 在 `src/types/` 中

### 文档格式

- 使用 Markdown 格式
- 包含代码示例
- 提供清晰的说明
- 支持中英文双语

## 发布流程

### 版本号

遵循 [语义化版本](https://semver.org/lang/zh-CN/) 规范：

- `主版本号`: 不兼容的 API 修改
- `次版本号`: 向下兼容的功能性新增
- `修订版本号`: 向下兼容的问题修正

### 发布检查清单

- [ ] 所有测试通过
- [ ] 文档已更新
- [ ] 版本号已更新
- [ ] CHANGELOG 已更新
- [ ] 示例应用可正常运行

### 发布命令

```bash
# 更新版本
npm version patch  # 或 minor/major

# 构建
npm run build

# 发布到 npm
npm publish

# 发布到 PyPI
python setup.py sdist bdist_wheel
twine upload dist/*
```

## 问题报告

### Bug 报告

使用 GitHub Issues 报告问题，请包含：

1. **环境信息**:
   - 操作系统
   - Python 版本
   - Node.js 版本
   - 浏览器版本

2. **复现步骤**:
   - 详细的操作步骤
   - 预期结果
   - 实际结果

3. **代码示例**:
   - 最小化的复现代码
   - 相关的配置文件

4. **错误信息**:
   - 完整的错误堆栈
   - 浏览器控制台信息

### 功能请求

1. **需求描述**: 详细描述所需功能
2. **使用场景**: 说明使用场景和价值
3. **实现建议**: 如果有实现想法，请分享

## 社区规范

### 行为准则

我们采用 [贡献者约定](https://www.contributor-covenant.org/zh-cn/version/2/0/code_of_conduct/) 作为行为准则。

### 沟通方式

1. **GitHub Issues**: 用于 bug 报告和功能请求
2. **GitHub Discussions**: 用于一般讨论和问题
3. **Pull Requests**: 用于代码审查和讨论

### 获得帮助

- 查看 [FAQ](docs/FAQ.md)
- 阅读 [API 文档](docs/API.md)
- 参考 [示例代码](examples/)
- 在 GitHub Discussions 中提问

## 许可证

通过贡献代码，您同意您的贡献将在 MIT 许可证下授权。

## 感谢

感谢所有为此项目做出贡献的开发者！您的贡献让这个项目变得更好。

---

如果您有任何问题或建议，请随时联系我们。我们期待您的贡献！