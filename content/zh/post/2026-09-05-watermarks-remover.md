---
title: 'watermarks-remover：一键清除 AI 内容水印，守护你的数字隐私'
date: 2026-09-05
tags: [AI工具, 水印检测, 隐私保护, Claude, Gemini, OpenAI]
categories: [AI工具评测]
description: watermarks-remover 是一款开源 AI 水印清除工具，支持去除文本、图片、文档中的多厂商 AI 来源标记，适用于关注内容隐私的创作者和开发者。
---

# watermarks-remover：一键清除 AI 内容水印，守护你的数字隐私

在 AI 生成内容（AIGC）蓬勃发展的今天，各大平台纷纷为自己的模型添加了数字水印——从 Claude 的隐形标记到 Gemini 的 SynthID 文本水印，再到 OpenAI 的内容来源标识。这些水印本意是透明化 AI 产出，但对于创作者而言，也可能带来隐私泄露和内容归属争议。

今天评测的 **watermarks-remover**（[GitHub](https://github.com/guillaumemeyer/watermarks-remover)）就是一款面向隐私保护的开源工具，能够检测和清除多种 AI 来源标记。

---

## 工具简介

**watermarks-remover** 是一个基于 Python 的 Agent Skill + 命令行工具，旨在帮助用户清除自己拥有内容中的 AI 水印和来源标记。当前已获得 **20,000+** 星标，支持 Claude、Gemini/SynthID、OpenAI 及多个开源 LLM 的水印格式。

**一句话总结：** 一个隐私优先的 AI 水印清除器，让你完全掌控自己内容的数字痕迹。

---

## 核心功能

### 1. 多类型水印检测与清除

工具覆盖了目前主流的 AI 水印形式：

| 层级 | 目标 | 清除方式 |
|------|------|----------|
| A 层 | 不可见 Unicode 字符、双向文字、标签字符 | 确定性 Python 脚本 |
| B 层 | 统计采样文本水印（token-level） | Agent 重写 + 可选 hook 清理 |
| 文件层 | C2PA / EXIF / XMP 等元数据 | 批量清理文档和媒体文件 |

### 2. 全文件格式支持

支持清除水印的文件格式包括：

- **图片：** PNG、JPEG、WebP、AVIF、HEIC、BMP、GIF、TIFF、SVG
- **文档：** PDF、DOCX、XLSX、PPTX、EPUB、ODT、HTML、Markdown
- **音视频：** MP4、MOV、M4A、M4V、WAV、MP3、FLAC

### 3. 多 AI 厂商兼容

支持清除以下厂商的 AI 来源标记：

- **Anthropic Claude**（隐形字符标记）
- **Google Gemini / SynthID-Text**
- **OpenAI 内容来源标识**
- **开源 LLM**（Kirchenbauer 绿色列表、Gumbel-EXP 等 keyed watermark）

### 4. Agent 集成支持

作为 Agent Skill 运行，与 Claude Code、Cursor、Cowork 等 AI 编程助手无缝集成：

- 支持 Claude Code 插件市场一键安装
- 提供 `PostToolUse` Hook 自动化清洗
- 支持 check 模式（仅报告不修改）和 clean 模式（直接清除）

### 5. 无依赖轻量设计

纯 Python 标准库实现（需 Python 3.10+），无需安装额外依赖，可快速部署在任何环境中。

---

## 适用人群

- **AI 创作者：** 使用 Claude、Gemini、ChatGPT 等生成内容后，希望保护自己的原创性和隐私
- **内容审核者：** 需要验证和处理带有 AI 水印的文件
- **隐私倡导者：** 关心数字内容中隐形标记带来的隐私风险
- **开发者：** 需要集成水印清除功能的团队或个人

---

## 同类工具对比

| 特性 | watermarks-remover | SynthID 官方检测 | WatermarkBuster |
|------|-------------------|-----------------|-----------------|
| 清除能力 | ✅ 主动清除 | ❌ 仅检测 | ✅ 部分清除 |
| 多厂商支持 | ✅ Claude/Gemini/OpenAI/开源 | ❌ 仅 Google | ⚠️ 有限支持 |
| 文件类型 | ✅ 图片/文档/音视频 | ❌ 仅文本 | ❌ 仅文本 |
| Agent 集成 | ✅ Claude Code/Cursor | ❌ | ❌ |
| 部署难度 | 低（pip install） | 低 | 中 |
| 开源程度 | MIT 开源 | 闭源 | MIT 开源 |

**结论：** watermarks-remover 在功能全面性和易用性上明显领先同类工具，尤其是跨平台和多厂商支持方面具有独特优势。

---

## 如何使用

### 方式一：命令行安装（推荐）

```bash
# 克隆仓库
git clone https://github.com/guillaumemeyer/watermarks-remover.git
cd watermarks-remover

# 安装 skill（以 claude-code 为例）
python3 install_skill.py --skill remove-ai-marks --target claude-code

# 或使用 pip 安装服务
pip install .
```

### 方式二：Claude Code 插件市场

在 Claude Code 中直接运行：

```
/plugin marketplace add guillaumemeyer/watermarks-remover
/plugin install watermarks-remover@watermarks-remover
```

安装后使用 `/remove-ai-marks` 命令即可调用。

### 方式三：自动化 Hook（高级）

在 `~/.claude/settings.json` 中配置 PostToolUse Hook，实现每次写入文件时自动检测水印：

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Write|Edit|MultiEdit|NotebookEdit",
        "hooks": [
          {
            "type": "command",
            "command": "python3",
            "args": ["/path/to/hook_written_file.py", "--mode", "check"],
            "timeout": 30
          }
        ]
      }
    ]
  }
}
```

---

## 总结

watermarks-remover 是目前最全面的 AI 水印清除工具之一，其跨厂商、跨文件格式的支持在实际应用中非常实用。对于经常使用多个 AI 平台创作内容、关注数字隐私的用户来说，这是一个值得收藏的工具。

**优点：**
- 支持多种 AI 厂商的水印格式
- 兼容图片、文档、音视频等多种文件类型
- 与主流 AI 编程助手深度集成
- 纯 Python 实现，无额外依赖

**缺点：**
- 统计类水印的清除可能影响文本质量（需要人工复核）
- 部分文件格式的元数据清理效果依赖于具体实现

**推荐指数：⭐⭐⭐⭐☆（4/5）**

> 适用于：AI 创作者、隐私保护意识较强的用户、需要批量处理 AI 生成内容的团队。

---

*工具信息更新至 2026-09-05，数据来源：[GitHub](https://github.com/guillaumemeyer/watermarks-remover)*
