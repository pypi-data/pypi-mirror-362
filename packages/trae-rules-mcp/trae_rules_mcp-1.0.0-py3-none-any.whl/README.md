# 📋 Trae Rules Generator MCP

一个用于自动生成和管理 Trae AI 项目规则文件的 MCP (Model Context Protocol) 服务。

## ✨ 功能特性

- 🔍 **读取现有规则**: 扫描和分析现有的规则文件结构
- 🎯 **智能生成规则**: 根据项目类型和功能特性生成定制化规则
- 💾 **规则文件管理**: 保存、更新和备份规则文件
- 🌐 **多语言支持**: 支持中文和英文规则生成
- 🔧 **灵活配置**: 支持自定义规则路径和文件名

## 🚀 快速开始

### 环境要求

- Python 3.8+
- pip 或 uv 包管理器

### 安装依赖

```bash
# 使用 uv (推荐)
uv sync

# 或使用 pip
pip install -e .
```

### 启动服务

```bash
# 方式一：直接运行 Python 脚本
python main.py

# 方式二：使用 uvicorn
uvicorn main:app --host 0.0.0.0 --port 8080 --reload
```

## 🛠️ MCP 工具

### 1. read_existing_rules

读取现有的规则文件内容和结构信息。

**参数:**
- `rules_path` (str, 可选): 规则文件目录路径，默认为 `.trae/rules`

**返回:**
- 规则文件的详细信息，包括文件列表、内容预览等

### 2. generate_project_rules

根据项目类型和功能特性生成新的项目规则文件。

**参数:**
- `project_type` (str): 项目类型 (如: web, mobile, ai, backend, frontend)
- `features` (List[str]): 项目功能特性列表 (如: ["authentication", "database", "api"])
- `language` (str, 可选): 规则文件语言，默认为中文

**返回:**
- 生成的规则文件内容 (Markdown 格式)

### 3. save_rules_file

保存规则文件到指定目录。

**参数:**
- `content` (str): 规则文件内容
- `filename` (str, 可选): 文件名，默认为 `project_rules.md`
- `rules_path` (str, 可选): 规则文件目录路径，默认为 `.trae/rules`

**返回:**
- 保存操作的结果信息

### 4. update_existing_rules

更新现有的规则文件内容。

**参数:**
- `file_path` (str): 要更新的规则文件路径
- `updates` (Dict[str, Any]): 更新内容的字典

**返回:**
- 更新操作的结果信息

## 📁 项目结构

```
trae-rules-mcp/
├── main.py              # MCP 服务主文件
├── pyproject.toml       # 项目配置文件
├── README.md           # 项目说明文档
└── .gitignore          # Git 忽略文件
```

## 🔧 配置说明

### 默认规则路径

服务默认在 `.trae/rules` 目录下查找和保存规则文件。你可以通过工具参数自定义路径。

### 支持的项目类型

- `web` / `frontend`: 前端 Web 项目
- `backend` / `api`: 后端 API 项目
- `ai`: AI/机器学习项目
- `mobile`: 移动应用项目
- 其他自定义类型

### 支持的功能特性

- `authentication`: 用户认证
- `database`: 数据库操作
- `api`: API 接口
- 其他自定义特性

## 🤝 贡献指南

1. Fork 本仓库
2. 创建功能分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 打开 Pull Request

## 📄 许可证

本项目采用 MIT 许可证 - 查看 [LICENSE](LICENSE) 文件了解详情。

## 🆘 支持

如果你遇到任何问题或有功能建议，请在 [Issues](https://github.com/trae-ai/trae-rules-mcp/issues) 中提出。