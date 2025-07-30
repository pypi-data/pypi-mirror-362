# 发布指南

本文档描述了如何发布 Dash KLineChart 组件到 PyPI。

## 前提条件

1. **工具安装**
   ```bash
   pip install build twine
   npm install
   ```

2. **PyPI 账户设置**
   - 注册 [PyPI](https://pypi.org/account/register/) 账户
   - 配置 [API Token](https://pypi.org/manage/account/token/)
   - 设置环境变量或使用 `.pypirc` 文件

## 发布流程

### 1. 版本管理

使用版本管理脚本更新版本号：

```bash
# 更新到新版本
./scripts/bump_version.sh 0.1.1

# 或者手动更新以下文件中的版本号：
# - dash_kline_charts/_version.py
# - package.json
# - pyproject.toml
```

### 2. 运行测试

确保所有测试通过：

```bash
# 运行完整测试套件
./scripts/test.sh

# 或者分别运行
npm test
python -m pytest tests/ -v
```

### 3. 构建包

```bash
# 清理旧的构建文件
rm -rf dist/ build/ *.egg-info/

# 构建 JavaScript 组件
npm run build

# 构建 Python 包
python -m build
```

### 4. 验证构建

```bash
# 检查包的完整性
twine check dist/*

# 本地安装测试
pip install dist/*.whl
python -c "import dash_kline_charts; print('✅ 导入成功')"
```

### 5. 发布到 PyPI

#### 发布到测试 PyPI（推荐先测试）

```bash
twine upload --repository testpypi dist/*
```

#### 发布到正式 PyPI

```bash
twine upload dist/*
```

### 6. 创建 Git 标签

```bash
git tag v0.1.1
git push origin v0.1.1
```

## 自动化发布

### 使用发布脚本

```bash
# 运行完整发布流程
./scripts/release.sh
```

### GitHub Actions 自动发布

当推送 `v*` 标签时，GitHub Actions 会自动：
1. 运行测试
2. 构建包
3. 发布到 PyPI
4. 创建 GitHub Release

```bash
# 触发自动发布
git tag v0.1.1
git push origin v0.1.1
```

## 发布清单

- [ ] 更新版本号
- [ ] 更新 CHANGELOG.md
- [ ] 运行所有测试
- [ ] 构建并验证包
- [ ] 发布到测试 PyPI
- [ ] 测试安装和功能
- [ ] 发布到正式 PyPI
- [ ] 创建 Git 标签
- [ ] 创建 GitHub Release
- [ ] 更新文档

## 故障排除

### 常见问题

1. **构建失败**
   - 检查 JavaScript 构建：`npm run build`
   - 检查依赖是否完整：`npm install`

2. **上传失败**
   - 检查 PyPI 认证配置
   - 确保版本号是唯一的
   - 检查包的完整性：`twine check dist/*`

3. **导入错误**
   - 确保 JavaScript 文件已正确包含在包中
   - 检查 `MANIFEST.in` 配置

### 日志文件

- 构建日志：检查控制台输出
- 上传日志：`~/.pypirc` 配置检查
- 测试日志：`pytest` 输出

## 版本策略

采用语义化版本控制 (SemVer)：

- **主版本号** (MAJOR)：不兼容的 API 修改
- **次版本号** (MINOR)：向下兼容的功能性新增
- **修订号** (PATCH)：向下兼容的问题修正

示例：
- `0.1.0` → `0.1.1`：Bug 修复
- `0.1.1` → `0.2.0`：新功能
- `0.2.0` → `1.0.0`：重大变更