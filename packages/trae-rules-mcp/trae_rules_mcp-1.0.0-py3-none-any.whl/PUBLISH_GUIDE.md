# 📦 Trae Rules MCP 发布指南

本指南详细说明了如何将 `trae-rules-mcp` 项目发布到各个平台的完整流程。

## 🚀 发布前准备

### 1. **代码质量检查**
```bash
# 运行代码格式检查
ruff check .
ruff format .

# 运行类型检查（如果使用 mypy）
mypy main.py

# 运行测试
python -m pytest tests/
```

### 2. **版本管理**
更新 `pyproject.toml` 中的版本号：
```toml
[project]
version = "1.0.0"  # 遵循语义化版本控制
```

### 3. **更新文档**
- 更新 `README.md` 中的版本信息
- 更新 `CHANGELOG.md`（如果有）
- 确保所有示例代码可以正常运行

## 📋 发布检查清单

- [ ] 所有测试通过
- [ ] 代码格式化完成
- [ ] 文档更新完成
- [ ] 版本号已更新
- [ ] Git 标签已创建
- [ ] 依赖项版本已锁定

## 🏷️ Git 标签和发布

### 1. **创建 Git 标签**
```bash
# 提交所有更改
git add .
git commit -m "chore: prepare for v1.0.0 release"

# 创建标签
git tag -a v1.0.0 -m "Release version 1.0.0"

# 推送标签到远程仓库
git push origin v1.0.0
git push origin main
```

### 2. **GitHub Release**
1. 访问 GitHub 仓库页面
2. 点击 "Releases" → "Create a new release"
3. 选择刚创建的标签 `v1.0.0`
4. 填写发布说明：

```markdown
## 🎉 Trae Rules MCP v1.0.0

### ✨ 新功能
- 支持读取现有规则文件
- 智能生成项目规则
- 保存和更新规则文件
- 支持多种项目类型

### 🔧 改进
- 优化规则生成算法
- 改进错误处理
- 增强文档说明

### 📦 安装方式
```bash
pip install trae-rules-mcp
```

### 🚀 快速开始
参见 [README.md](README.md) 获取详细使用说明。
```

## 📦 PyPI 发布

### 1. **安装发布工具**
```bash
# 安装 build 和 twine
pip install build twine
```

### 2. **构建分发包**
```bash
# 清理之前的构建
rm -rf dist/ build/ *.egg-info/

# 构建源码包和轮子包
python -m build
```

### 3. **检查构建结果**
```bash
# 检查分发包
twine check dist/*

# 查看构建的文件
ls -la dist/
```

### 4. **上传到 PyPI**

#### **测试环境（推荐先测试）**
```bash
# 上传到 TestPyPI
twine upload --repository testpypi dist/*

# 从 TestPyPI 安装测试
pip install --index-url https://test.pypi.org/simple/ trae-rules-mcp
```

#### **生产环境**
```bash
# 上传到正式 PyPI
twine upload dist/*
```

### 5. **配置 PyPI 凭据**

#### **方法一：使用 API Token（推荐）**
1. 登录 [PyPI](https://pypi.org/)
2. 进入 Account Settings → API tokens
3. 创建新的 API token
4. 配置 `~/.pypirc`：

```ini
[distutils]
index-servers = pypi testpypi

[pypi]
username = __token__
password = pypi-your-api-token-here

[testpypi]
repository = https://test.pypi.org/legacy/
username = __token__
password = pypi-your-test-api-token-here
```

#### **方法二：环境变量**
```bash
export TWINE_USERNAME=__token__
export TWINE_PASSWORD=pypi-your-api-token-here
```

## 🔄 自动化发布（GitHub Actions）

创建 `.github/workflows/publish.yml`：

```yaml
name: Publish to PyPI

on:
  release:
    types: [published]

jobs:
  publish:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v4
    
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.11'
    
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install build twine
    
    - name: Build package
      run: python -m build
    
    - name: Publish to PyPI
      env:
        TWINE_USERNAME: __token__
        TWINE_PASSWORD: ${{ secrets.PYPI_API_TOKEN }}
      run: twine upload dist/*
```

## 📱 MCP 服务器注册

### 1. **MCP 官方注册**
如果 MCP 有官方服务器注册表，按照其指南提交：
- 项目描述
- 安装说明
- 使用示例
- 工具列表

### 2. **社区分享**
- 在 MCP 相关论坛或社区分享
- 创建使用教程和博客文章
- 在 GitHub 上添加相关标签

## 🔍 发布后验证

### 1. **安装测试**
```bash
# 在新环境中测试安装
pip install trae-rules-mcp

# 验证安装
python -c "import main; print('安装成功')"
```

### 2. **功能测试**
```bash
# 运行 MCP 服务器
python main.py

# 在另一个终端测试连接
python test_mcp.py
```

### 3. **文档验证**
- 确保 PyPI 页面显示正确
- 检查 README 在 PyPI 上的渲染
- 验证所有链接可访问

## 📊 发布监控

### 1. **下载统计**
- 监控 PyPI 下载量
- 使用 [pypistats](https://pypistats.org/) 查看统计

### 2. **用户反馈**
- 监控 GitHub Issues
- 关注用户评论和建议
- 及时回复问题

## 🚨 发布问题排查

### 常见问题

1. **构建失败**
   ```bash
   # 检查 pyproject.toml 配置
   # 确保所有依赖都已安装
   ```

2. **上传失败**
   ```bash
   # 检查网络连接
   # 验证 API token
   # 确保版本号未重复
   ```

3. **安装失败**
   ```bash
   # 检查依赖兼容性
   # 验证 Python 版本要求
   ```

## 📝 发布记录

维护发布记录表：

| 版本 | 发布日期 | PyPI | GitHub | 说明 |
|------|----------|------|--------|------|
| v1.0.0 | 2025-01-17 | ✅ | ✅ | 初始发布 |

## 🎯 下一步计划

- [ ] 设置自动化测试
- [ ] 配置代码覆盖率报告
- [ ] 创建用户文档网站
- [ ] 添加更多项目类型支持
- [ ] 性能优化和监控

---

💡 **提示**: 首次发布建议先在 TestPyPI 上测试，确认无误后再发布到正式 PyPI。

🔗 **相关链接**:
- [PyPI 官方文档](https://packaging.python.org/)
- [Twine 使用指南](https://twine.readthedocs.io/)
- [语义化版本控制](https://semver.org/lang/zh-CN/)