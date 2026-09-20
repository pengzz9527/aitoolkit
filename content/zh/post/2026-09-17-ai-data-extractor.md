---
title: 'AI Data Extractor：一键提取 AI 编程助手聊天历史，打造你的私有训练数据集'
date: 2026-09-17
tags: [AI工具, 数据提取, Claude Code, Cursor, Aider, 开源]
categories: [AI 工具评测]
description: 一款免费的开源工具，支持从 Claude Code、Cursor、Windsurf、Aider、Cline/Roo Code 等 10 种 AI 编程助手的本地聊天记录中提取数据，统一导出为 JSONL 格式。
---

# AI Data Extractor：一键提取 AI 编程助手聊天历史，打造你的私有训练数据集

在 AI 编程助手已经深入日常开发工作的今天，你是否想过——那些与 Claude Code、Cursor、Aider 等工具积累的对话记录，其实是一份宝贵的私有知识库？

今天介绍的 **[ai-data-extractor](https://github.com/kruzovic7/ai-data-extractor)**（⭐ 827+）正是为了解决这个问题而生的开源工具。它可以从 10 种主流 AI 编程助手的本地存储中自动提取聊天记录，统一导出为标准 JSONL 格式，方便你用于微调、数据分析或归档备份。

## 核心功能

### 1. 多工具支持
目前支持提取 **10 种 AI 编程助手**的聊天历史：

| 工具 | 存储格式 | 路径示例 |
|------|---------|---------|
| **Claude Code** | JSONL | `~/.claude/projects/**/*.jsonl` |
| **Codex CLI** | JSONL | `~/.codex/sessions/**/rollout-*.jsonl` |
| **Cursor** | SQLite | `~/.../Cursor/User/{global,workspace}Storage` |
| **Windsurf** | SQLite | `~/.../Windsurf/User/{global,workspace}Storage` |
| **Trae** | SQLite + JSONL | `~/.../Trae` |
| **Continue** | JSON | `~/.continue/sessions/*.json` |
| **Gemini CLI** | JSON | `~/.gemini/tmp/<hash>/chats/*.json` |
| **OpenCode** | JSON | `~/.local/share/opencode/storage/` |
| **Cline / Roo Code** | JSON | 编辑器全局存储目录 |
| **Aider** | Markdown | `<项目>/.aider.chat.history.md` |

### 2. 跨平台自动检测
工具会自动搜索 macOS、Linux 和 Windows 三种操作系统下的常见路径（`~/Library/Application Support`、`~/.config`、`~/.local/share`、`%APPDATA%` 等），无需手动指定路径。

### 3. 丰富的提取内容
每个对话记录不仅包含用户消息和助手回复，还自动提取：
- **代码上下文**：文件路径、选中代码片段
- **代码 Diff**：建议的编辑变更
- **工具调用**：执行的命令及其输出结果
- **元数据**：时间戳、会话 ID、项目路径、模型名称

### 4. 灵活的使用方式
```bash
# 交互式菜单选择要提取的工具
python extract.py

# 一键提取所有支持的工具
python extract.py --all

# 指定特定工具
python extract.py --sources cursor,claude_code,aider

# 预览有哪些数据可提取（不实际提取）
python extract.py --list

# 提取并合并到一个文件
python extract.py --all --merge
```

### 5. 零依赖
纯 Python 标准库实现，仅需 Python 3.9+，无需安装任何第三方包。

## 适用人群

- **AI 编程爱好者**：想要备份和整理与 AI 助手的大量对话记录
- **个人知识管理者**：将分散在多工具的 AI 对话整合到统一的数据集
- **LLM 开发者**：收集自己的高质量对话数据用于微调私有模型
- **数据分析师**：研究 AI 编程助手的交互模式和代码生成质量
- **隐私关注者**：在本地完成数据提取，无需上传到云端

## 与同类工具对比

| 特性 | AI Data Extractor | 手动备份 | 商业工具 |
|------|------------------|---------|---------|
| 支持工具数量 | 10 种 | 逐个手动导出 | 通常 1-2 种 |
| 输出格式 | 标准化 JSONL | 各工具原生格式 | 各异 |
| 跨平台 | ✅ macOS/Linux/Windows | ✅ | ❌ |
| 零依赖 | ✅ 纯标准库 | ✅ | ❌ |
| 自动发现路径 | ✅ | ❌ | 部分支持 |
| 成本 | 免费开源 | 免费 | 付费 |

与其他类似工具（如 [ChatGPT Chat Export](https://github.com/logan-markewich/chatgpt-exporter) 等）相比，AI Data Extractor 的独特优势在于**专门针对 AI 编程助手**，并且支持的工具数量最多、覆盖平台最全。

## 如何使用

### 安装
```bash
# 克隆仓库
git clone https://github.com/kruzovic7/ai-data-extractor.git
cd ai-data-extractor

# 检查 Python 版本（需要 3.9+）
python --version
```

### 基本使用
```bash
# 方式一：交互式选择
python extract.py
# 系统会列出所有检测到的工具和数据，让你选择要提取哪些

# 方式二：一键提取全部
python extract.py --all

# 方式三：只提取特定工具
python extract.py --sources cursor,claude_code,aider --merge
```

### 查看提取结果
```bash
ls extracted_data/
# 输出示例：
# ├── claude_code_conversations_20260917_143022.jsonl
# ├── cursor_conversations_20260917_143022.jsonl
# ├── aider_conversations_20260917_143022.jsonl
# ├── all_conversations.jsonl      # 合并后的完整数据集
# └── ...
```

### 进阶用法
```bash
# 自定义输出目录
python extract.py --all --output-dir ~/my_ai_data

# 添加额外搜索路径（如 Aider 的项目目录）
python extract.py --sources aider --search-path ~/projects/my-project

# 只预览，不实际提取
python extract.py --list
```

### 独立运行单个提取器
```bash
# 单独运行某个工具的提取脚本
python -m extractors.cursor
python extractors/aider.py
```

## 注意事项

1. **数据权限**：确保你只提取自己的对话数据，尊重隐私和版权
2. **应用更新**：AI 编程助手可能会更改本地存储格式，如遇到解析问题请检查最新 README 或提交 Issue
3. **Aider 特殊处理**：由于 Aider 没有固定存储目录，需要通过 `--search-path` 指定项目路径
4. **大数据量**：如果对话历史非常庞大，`--merge` 可能会产生较大的 JSONL 文件，建议分批处理

## 总结

**AI Data Extractor** 是一款设计精良、实用价值高的开源工具。它解决了 AI 编程时代的一个痛点——我们每天与 AI 助手的大量对话数据散落在各个应用的本地存储中，缺乏统一的备份和管理方案。

### 推荐指数：⭐⭐⭐⭐⭐（5/5）

**优点：**
- 支持 10 种主流 AI 编程助手，覆盖面最广
- 纯标准库实现，零依赖，开箱即用
- 跨平台自动检测，用户体验优秀
- MIT 开源协议，可自由使用和修改
- 活跃开发中，持续更新支持新工具

**缺点：**
- 目前仅支持英文界面
- 对于某些工具的存储格式理解可能因版本更新而需要调整

如果你是 AI 编程助手的重度用户，或者正在考虑用自己的对话数据微调模型，这个工具绝对是值得收藏的利器。它不仅帮你备份了珍贵的对话记忆，更为后续的数据挖掘和模型优化打开了大门。

---

*项目地址：https://github.com/kruzovic7/ai-data-extractor*
*文档：https://github.com/kruzovic7/ai-data-extractor#readme*

---

喜欢这篇评测？浏览 [198007.xyz 工具集](/tools/) 发现更多 AI 编程辅助工具。
