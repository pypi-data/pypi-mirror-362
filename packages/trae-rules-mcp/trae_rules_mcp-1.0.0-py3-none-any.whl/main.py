#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Trae AI 规则文件生成器 MCP 服务器
自动生成和管理项目规则文件的 MCP 服务
"""

import os
import json
from datetime import datetime
from typing import List, Dict, Any, Optional
from pathlib import Path

from mcp.server.fastmcp import FastMCP

# 初始化 MCP 服务器
mcp = FastMCP("Trae Rules Generator")


@mcp.tool()
def read_existing_rules(rules_path: str = ".trae/rules") -> dict:
    """
    读取现有的规则文件内容

    Args:
        rules_path: 规则文件目录路径，默认为 .trae/rules

    Returns:
        现有规则文件的内容和结构信息
    """
    try:
        rules_dir = Path(rules_path)
        if not rules_dir.exists():
            return {
                "status": "error", 
                "message": f"规则目录 {rules_path} 不存在"
            }

        rules_info = {
            "directory": str(rules_dir.absolute()),
            "files": [],
            "total_files": 0
        }

        # 遍历规则文件
        for file_path in rules_dir.rglob("*.md"):
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()

                rules_info["files"].append({
                    "name": file_path.name,
                    "path": str(file_path.relative_to(rules_dir)),
                    "size": len(content),
                    "content_preview": content[:200] + "..." if len(content) > 200 else content
                })
            except Exception as e:
                rules_info["files"].append({
                    "name": file_path.name,
                    "path": str(file_path.relative_to(rules_dir)),
                    "error": str(e)
                })

        rules_info["total_files"] = len(rules_info["files"])
        return {"status": "success", "data": rules_info}

    except Exception as e:
        return {
            "status": "error", 
            "message": f"读取规则文件时出错: {str(e)}"
        }


@mcp.tool()
def generate_project_rules(
    project_type: str, 
    features: List[str], 
    language: str = "中文"
) -> str:
    """
    根据项目类型和功能特性生成新的项目规则文件
    
    Args:
        project_type: 项目类型 (如: web, mobile, ai, backend, frontend 等)
        features: 项目功能特性列表 (如: ["authentication", "database", "api"])
        language: 规则文件语言，默认为中文
    
    Returns:
        生成的规则文件内容
    """
    try:
        # 生成规则文件头部
        header = "---\n"
        header += f"description: {project_type} 项目规则\n"
        header += "globs: \n"
        header += "alwaysApply: true\n"
        header += "---\n\n"
        
        # 生成规则内容
        content = f"### 📋 {project_type.upper()} 项目开发规则\n\n"
        
        # 通用规则
        content += "#### 🔧 通用开发规则\n\n"
        content += "1. **代码质量**\n"
        content += "   * 保持代码简洁、可读性强\n"
        content += "   * 添加必要的注释和文档\n"
        content += "   * 遵循项目的编码规范\n\n"
        
        content += "2. **版本控制**\n"
        content += "   * 提交信息要清晰明确\n"
        content += "   * 定期推送代码到远程仓库\n"
        content += "   * 使用分支管理功能开发\n\n"
        
        # 根据项目类型生成特定规则
        if project_type.lower() in ["web", "frontend"]:
            content += "#### 🌐 前端开发规则\n\n"
            content += "1. **UI/UX 设计**\n"
            content += "   * 保持界面简洁美观\n"
            content += "   * 确保响应式设计\n"
            content += "   * 优化用户体验\n\n"
            
        elif project_type.lower() in ["backend", "api"]:
            content += "#### ⚙️ 后端开发规则\n\n"
            content += "1. **API 设计**\n"
            content += "   * 遵循 RESTful 设计原则\n"
            content += "   * 提供完整的 API 文档\n"
            content += "   * 实现适当的错误处理\n\n"
            
        elif project_type.lower() == "ai":
            content += "#### 🤖 AI 项目规则\n\n"
            content += "1. **模型管理**\n"
            content += "   * 记录模型版本和性能指标\n"
            content += "   * 保存训练数据和参数\n"
            content += "   * 实现模型验证和测试\n\n"
        
        # 根据功能特性添加规则
        if features:
            content += "#### 🎯 功能特性规则\n\n"
            for i, feature in enumerate(features, 1):
                content += f"{i}. **{feature.title()}**\n"
                
                if feature.lower() == "authentication":
                    content += "   * 实现安全的用户认证\n"
                    content += "   * 使用强密码策略\n"
                    content += "   * 实现会话管理\n\n"
                    
                elif feature.lower() == "database":
                    content += "   * 设计合理的数据库结构\n"
                    content += "   * 实现数据备份策略\n"
                    content += "   * 优化查询性能\n\n"
                    
                elif feature.lower() == "api":
                    content += "   * 设计清晰的 API 接口\n"
                    content += "   * 实现接口版本管理\n"
                    content += "   * 添加接口文档\n\n"
                    
                else:
                    content += f"   * 确保 {feature} 功能的稳定性\n"
                    content += f"   * 优化 {feature} 的性能\n"
                    content += f"   * 测试 {feature} 的各种场景\n\n"
        
        # 添加时间戳
        content += f"\n---\n*规则生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*\n"
        
        return header + content
        
    except Exception as e:
        return f"生成规则文件时出错: {str(e)}"


@mcp.tool()
def save_rules_file(
    content: str, 
    filename: str = "project_rules.md", 
    rules_path: str = ".trae/rules"
) -> str:
    """
    保存规则文件到指定目录
    
    Args:
        content: 规则文件内容
        filename: 文件名，默认为 project_rules.md
        rules_path: 规则文件目录路径，默认为 .trae/rules
    
    Returns:
        保存操作的结果信息
    """
    try:
        rules_dir = Path(rules_path)
        rules_dir.mkdir(parents=True, exist_ok=True)
        
        file_path = rules_dir / filename
        
        # 如果文件已存在，创建备份
        if file_path.exists():
            backup_name = f"{filename.rsplit('.', 1)[0]}_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
            backup_path = rules_dir / backup_name
            file_path.rename(backup_path)
        
        # 保存新文件
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        return f"✅ 规则文件已成功保存到: {file_path.absolute()}"
        
    except Exception as e:
        return f"❌ 保存规则文件时出错: {str(e)}"


@mcp.tool()
def update_existing_rules(file_path: str, updates: Dict[str, Any]) -> str:
    """
    更新现有的规则文件内容
    
    Args:
        file_path: 要更新的规则文件路径
        updates: 更新内容的字典，支持以下键:
                - append_content: 要追加的内容
                - replace_section: 要替换的章节 {"section_name": "new_content"}
                - insert_after: 在指定内容后插入 {"after": "content", "insert": "new_content"}
    
    Returns:
        更新操作的结果信息
    """
    try:
        file_path_obj = Path(file_path)
        if not file_path_obj.exists():
            return f"❌ 文件 {file_path} 不存在"
        
        # 读取现有内容
        with open(file_path_obj, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 创建备份
        backup_name = f"{file_path_obj.stem}_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}{file_path_obj.suffix}"
        backup_path = file_path_obj.parent / backup_name
        with open(backup_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        # 应用更新
        if "append_content" in updates:
            content += "\n" + updates["append_content"]
        
        if "replace_section" in updates:
            for section, new_content in updates["replace_section"].items():
                # 简单的章节替换逻辑
                section_start = content.find(f"#### {section}")
                if section_start != -1:
                    next_section = content.find("####", section_start + 1)
                    if next_section != -1:
                        content = content[:section_start] + new_content + content[next_section:]
                    else:
                        content = content[:section_start] + new_content
        
        if "insert_after" in updates:
            after_text = updates["insert_after"]["after"]
            insert_text = updates["insert_after"]["insert"]
            insert_pos = content.find(after_text)
            if insert_pos != -1:
                insert_pos += len(after_text)
                content = content[:insert_pos] + "\n" + insert_text + content[insert_pos:]
        
        # 保存更新后的内容
        with open(file_path_obj, 'w', encoding='utf-8') as f:
            f.write(content)
        
        return f"✅ 规则文件已成功更新: {file_path_obj.absolute()}\n📁 备份文件: {backup_path.absolute()}"
        
    except Exception as e:
        return f"❌ 更新规则文件时出错: {str(e)}"


if __name__ == "__main__":
    # 启动 MCP 服务器
    mcp.run()