---
title: 'Palmier Pro 评测：Y Combinator 支持的 AI 原生视频编辑器，让 Agent 也能剪视频'
date: 2026-07-26T08:00:00+08:00
description: 'Palmier Pro 是一款专为 AI 时代打造的 macOS 原生视频编辑器，支持内置生成式 AI、MCP 服务器集成 Claude Code/Codex/Cursor 等编程 Agent，基于 Swift 从零构建。'
tags:
  - AI工具
  - 视频编辑
  - macOS
  - MCP
  - 开源项目
  - GitHub Trending
  - 工具评测
categories:
  - 工具评测
---

## 一句话介绍

**Palmier Pro** 是一款由 Y Combinator S24 孵化的开源 AI 原生视频编辑器，让你在时间线上与 AI Agent（Claude Code、Codex、Cursor）协作生成和编辑视频，底层集成 Seedance、Kling 等前沿生成模型。

## 它是什么？

Palmier Pro 是由 Palmier, Inc.（Y Combinator S24 毕业项目）开发的 macOS 原生视频编辑器。与传统视频编辑软件不同，它从设计之初就将 AI 深度融入工作流——不仅可以在应用内直接调用 Seedance、Kling、Nano Banana Pro 等 SOTA 生成式 AI 模型来创建视频和图片素材，还通过内置的 MCP 服务器让 Claude Code、Codex CLI、Cursor 等编程 Agent 直接操控你的时间线项目。

该项目于 2026 年 4 月 7 日首次发布，短短三个月内已获得 **12,293+ Stars**、897+ Forks，采用 GPLv3 开源许可证。它要求 macOS Tahoe（macOS 26）以上版本，仅支持 Apple Silicon 芯片。

Palmier Pro 的核心设计理念是"人和 Agent 在同一时间线上协作"——你可以手动剪辑，也可以让 AI Agent 根据你的自然语言指令完成复杂的编辑任务，比如"把第三段换成 AI 生成的太空场景"或"为整个视频添加字幕和转场"。

## 核心功能

### 1. Swift 原生视频编辑引擎

Palmier Pro 完全使用 Swift 从零编写，目标对标 Adobe Premiere Pro。它提供了专业的多轨道时间线、精细的剪辑工具、色彩调整和音频处理功能，性能经过深度优化，能够流畅处理高分辨率视频。

### 2. 内置生成式 AI 能力

这是 Palmier Pro 最大的亮点。应用内集成了多个 SOTA 生成模型：

- **Seedance**：Google 的视频生成模型，可创建高质量动态视频片段
- **Kling**：快手推出的视频生成模型，擅长复杂动作和物理模拟
- **Nano Banana Pro**：AI 图片生成模型，可用于创建视频素材和封面

这些模型直接在时间线编辑器中可用，无需切换到其他应用，生成内容可直接拖入时间线使用。

### 3. MCP 服务器 — Agent 直接操控时间线

Palmier Pro 启动后自动暴露一个 MCP（Model Context Protocol）HTTP 服务器（默认端口 19789），允许外部 AI Agent 直接读取和操作你的视频项目：

```bash
# Claude Code 接入
claude mcp add --transport http palmier-pro http://127.0.0.1:19789/mcp

# Codex CLI 接入
codex mcp add palmier-pro --url http://127.0.0.1:19789/mcp
```

接入后，你可以用自然语言命令 Agent 完成剪辑任务，比如添加转场、调整时长、替换素材、导出项目等。

### 4. 应用内 Agent 聊天

除了连接外部 Agent，Palmier Pro 还内置了 Agent 聊天界面，可以直接在应用内与 AI 对话，让 AI 帮你完成编辑操作，无需离开编辑器。

### 5. 一键安装集成

应用内置了 `mcpb`（MCP Builder）工具，提供一键安装功能：

- 在应用菜单中选择 `Help` → `MCP Instructions` → `Install in Cursor` 即可将 Palmier Pro 的配置写入 Cursor
- 同样支持一键安装到 Claude Desktop 扩展

## 适用人群

- **视频创作者**：希望利用 AI 加速视频制作流程的内容创作者、YouTuber、短视频制作者
- **开发者/技术爱好者**：对 MCP 协议和 AI Agent 感兴趣的开发者，想探索 Agent 操控创意工具的边界
- **macOS 用户**：寻找专业级 macOS 原生视频编辑器的用户，尤其是不需要跨平台支持的 Mac 用户
- **AI 实验者**：希望体验"人与 Agent 协作创作"新范式的用户

## 与同类工具对比

| 特性 | Palmier Pro | Adobe Premiere Pro | CapCut (剪映) | DaVinci Resolve |
|------|-------------|-------------------|---------------|-----------------|
| AI 原生设计 | ✅ 从底层集成 | ⚠️ 后期添加 | ✅ 内置 AI | ⚠️ 部分集成 |
| 生成式 AI | ✅ 多模型集成 | ❌ 需插件 | ✅ 内置 | ❌ 有限 |
| Agent 集成 | ✅ MCP 服务器 | ❌ | ❌ | ❌ |
| 开源 | ✅ GPLv3 | ❌ 商业 | ❌ 商业 | ✅ 免费版开源 |
| 平台 | macOS only | 全平台 | 全平台 | 全平台 |
| 价格 | 编辑器免费 | $22.99/月 | 免费+订阅 | 免费+Studio $295 |
| 学习曲线 | 中等 | 高 | 低 | 高 |

Palmier Pro 的独特之处在于它是**第一个将 MCP 协议引入视频编辑领域的工具**。这意味着 AI Agent 不再只是"帮你生成素材"，而是可以真正理解你的项目结构、操作时间线元素、完成复杂的编辑任务。这种"Agent 作为编辑助手"的模式代表了视频编辑的未来方向。

与 CapCut 相比，Palmier Pro 更偏向专业用户和开发者；与 Premiere Pro 相比，它更轻量且 AI 集成度更高，但生态插件和第三方资源还不够丰富。

## 如何使用

### 第一步：下载安装

访问 [GitHub Releases](https://github.com/palmier-io/palmier-pro/releases/latest/download/PalmierPro.dmg) 下载 DMG 安装包，无需登录即可使用基础功能。

**系统要求**：macOS Tahoe（26）+ Apple Silicon 芯片

### 第二步：开始基础编辑

打开应用后即可使用专业视频编辑功能：导入素材、多轨道剪辑、色彩调整、音频处理等。界面直观，类似传统非线性编辑软件。

### 第三步：使用内置 AI 生成

在时间线面板中点击 AI 生成按钮，选择所需模型（Seedance/Kling/Nano Banana Pro），输入描述即可生成视频或图片素材，直接拖入时间线使用。

> 注意：生成式 AI 功能需要登录账户并订阅付费计划。

### 第四步：连接 AI Agent（可选）

如果你想让 AI Agent 协助编辑：

1. 打开 Claude Code，执行：
   ```bash
   claude mcp add --transport http palmier-pro http://127.0.0.1:19789/mcp
   ```

2. 或者在 Cursor 中，通过 `Help` → `MCP Instructions` → `Install in Cursor` 一键配置

3. 连接成功后，你就可以用自然语言告诉 Agent："帮我删除第一段中不需要的部分"、"给这个视频加上英文字幕"等指令

### 第五步：导出项目

完成编辑后，支持多种格式导出，包括 MP4、MOV 等主流格式，可自定义分辨率、码率和帧率。

## 总结推荐指数

Palmier Pro 是目前市场上**最具创新性的 AI 视频编辑工具之一**。它将专业视频编辑能力、生成式 AI 和 Agent 协作三大趋势融合到一个应用中，代表了创意工具的未来发展方向。

**优点**：
- 编辑器本身免费且功能完整，无需付费即可使用专业剪辑功能
- MCP 服务器设计让 AI Agent 真正参与到创作过程中
- 内置多个 SOTA 生成模型，一站式完成素材生成和编辑
- Swift 原生开发，macOS 上性能优秀
- Y Combinator 背书，社区活跃，更新频繁

**不足**：
- 仅支持 macOS Apple Silicon，跨平台用户无法使用
- 要求 macOS Tahoe（最新系统），对系统版本要求较高
- 生成式 AI 功能需要付费订阅
- 目前生态尚不成熟，插件和社区资源较少
- GPLv3 许可证对商业使用有一定限制

**综合评分：8.5/10**

如果你是 macOS 用户、视频创作者或 AI 技术爱好者，Palmier Pro 绝对值得尝试。特别是对于想要探索"AI Agent + 创意工具"新范式的开发者来说，这是一个不可错过的实验平台。即使不连接 Agent，它作为一个免费的 AI 增强型视频编辑器，也已经具备了与 CapCut 等专业工具竞争的实力。

---

*本文基于 2026 年 7 月 26 日的公开信息撰写，工具功能和定价可能随时更新，请以官方最新信息为准。*
