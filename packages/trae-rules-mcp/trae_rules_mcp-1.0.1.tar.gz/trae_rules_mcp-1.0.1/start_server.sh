#!/bin/bash
# Trae AI 规则生成器 MCP 服务器启动脚本

set -e

# 获取脚本所在目录
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "🚀 启动 Trae AI 规则生成器 MCP 服务器..."
echo "📁 工作目录: $SCRIPT_DIR"

# 检查是否存在虚拟环境
if [ ! -d ".venv" ]; then
    echo "⚠️  未找到虚拟环境，正在创建..."
    uv sync
fi

# 检查依赖是否已安装
if ! uv run python -c "import mcp" 2>/dev/null; then
    echo "📦 安装依赖..."
    uv sync
fi

echo "✅ 环境检查完成"
echo "🌐 启动 MCP 服务器..."
echo "💡 使用 Ctrl+C 停止服务器"
echo ""

# 启动服务器
uv run python main.py