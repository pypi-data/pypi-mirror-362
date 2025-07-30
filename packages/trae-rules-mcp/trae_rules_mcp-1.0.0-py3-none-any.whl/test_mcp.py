#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试 MCP 服务器功能
"""

import asyncio
import json
from mcp.client.session import ClientSession
from mcp.client.stdio import stdio_client

async def test_mcp_server():
    """测试 MCP 服务器的基本功能"""
    try:
        # 连接到 MCP 服务器
        async with stdio_client() as (read, write):
            async with ClientSession(read, write) as session:
                # 初始化会话
                await session.initialize()
                
                # 获取可用工具列表
                tools = await session.list_tools()
                print("可用工具:")
                for tool in tools.tools:
                    print(f"  - {tool.name}: {tool.description}")
                
                # 测试生成项目规则
                print("\n测试生成项目规则...")
                result = await session.call_tool(
                    "generate_project_rules",
                    {
                        "project_type": "web",
                        "features": ["authentication", "database", "api"],
                        "language": "中文"
                    }
                )
                print("生成的规则内容:")
                print(result.content[0].text[:500] + "...")
                
                print("\n✅ MCP 服务器测试成功!")
                
    except Exception as e:
        print(f"❌ 测试失败: {e}")

if __name__ == "__main__":
    asyncio.run(test_mcp_server())