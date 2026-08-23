---
title: 'MoneyPrinterTurbo 评测：一句话生成 AI 短视频'
date: 2026-08-22
tags: ['AI工具', '视频生成', 'MoneyPrinterTurbo', 'AI Agent', '短视频', '开源', 'Python']
categories: ['AI工具评测']
description: 'MoneyPrinterTurbo 是一个一站式 AI 短视频生成工具，只需提供主题或关键词，即可自动生成视频脚本、匹配素材、生成字幕和背景音乐，并合成高清短视频。GitHub Star 数已突破 15 万，支持 Kimi、Claude、GPT-4o、DeepSeek 等主流模型。'
---

## 一句话介绍

**MoneyPrinterTurbo** 是一个一站式 AI 短视频生成工具，只需输入视频主题或关键词，即可自动生成脚本、匹配素材、生成字幕和配音，最终合成高清短视频。GitHub Star 数已突破 15 万，支持 Kimi、Claude、GPT-4o、DeepSeek 等主流大模型。

---

## 工具简介

短视频创作门槛很高：需要写脚本、找素材、配音、剪辑、加字幕，每一步都耗时耗力。MoneyPrinterTurbo 的出现让这一切变得简单——你只需告诉它「主题是什么」，剩下的全交给 AI。

这个项目由开发者 harry0703 发起，采用 Python 3.11+ 开发，支持 Windows、macOS 和 Linux。它提供 AI Agent、WebUI、API 和 CLI 四种使用方式，代码按控制器、服务和模型等职责分层，结构清晰。

更特别的是，MoneyPrinterTurbo 支持接入 WaveSpeed AI 的文生视频模型（默认 Seedance），可以按脚本关键词直接生成全新画面，不再局限于免费素材库的库存视频。

---

## 核心功能

### 1. AI 自动生成视频脚本

输入主题或关键词，AI 会自动生成视频脚本，支持多语言（中文、英文等）。你也可以完全自定义脚本，自己撰写文案后交由工具处理后续环节。

### 2. 智能素材匹配与 AI 生成画面

工具可以从 Pexels、Pixabay 和 Coverr 等平台获取免费高清素材，也可以接入 WaveSpeed AI 的文生视频模型（Seedance），根据脚本关键词直接生成全新的视频片段，突破素材库的限制。

### 3. 多模型语音合成

支持 Edge TTS、Azure Speech、SiliconFlow、Google Gemini、小米 MiMo、ElevenLabs 和 Chatterbox 等多种语音合成方案，可实时试听并选择合适的音色。

### 4. 丰富的字幕与背景音乐支持

字幕可调整字体、位置、颜色、大小、描边和背景样式。背景音乐支持随机选择或指定音乐文件，并可独立调节音量。

### 5. 高清视频输出与批量生成

支持竖屏 9:16（1080x1920）和横屏 16:9（1920x1080）两种高清视频尺寸。支持批量视频生成，一次可生成多个版本，从中选择最满意的一个。

### 6. 跨平台一键发布

生成完成后，可自动上传至 TikTok、Instagram 和 YouTube Shorts，实现从创作到发布的全流程自动化。

### 7. 主流 AI 模型全面兼容

支持 Kimi / Moonshot AI、OpenAI、Anthropic Claude、Google Gemini、DeepSeek、阿里云通义千问、Microsoft Azure OpenAI、火山引擎方舟、xAI Grok、MiniMax、小米 MiMo 等主流模型，并兼容 Cloudflare AI Gateway、魔搭 ModelScope、Ollama、LiteLLM、Groq 等网关和本地运行环境。

---

## 适用人群

- **短视频创作者**：想快速产出高质量短视频，但不想花大量时间剪辑
- **内容营销团队**：需要批量生成产品宣传、科普类短视频
- **自媒体博主**：用 AI 辅助脚本撰写和素材匹配，提升内容生产力
- **AI 爱好者**：喜欢尝试新技术，想体验一键生成视频的快感
- **企业用户**：需要制作培训视频、产品介绍等商业内容

---

## 与同类工具对比

| 特性 | MoneyPrinterTurbo | OpusClip | Pictory | Runway |
|------|-------------------|----------|---------|--------|
| 开源 | ✅ 完全开源 | ❌ 付费 SaaS | ❌ 付费 SaaS | ❌ 付费 SaaS |
| 本地运行 | ✅ | ❌ | ❌ | ❌ |
| 自动生成脚本 | ✅ | ✅ | ✅ | ❌ |
| 免费素材库 | ✅ Pexels/Pixabay/Coverr | ✅ | ✅ | ❌ |
| AI 生成素材 | ✅ WaveSpeed/Seedance | ❌ | ❌ | ✅ |
| 多语言脚本 | ✅ | ✅ | ✅ | ❌ |
| 跨平台发布 | ✅ TikTok/Instagram/YouTube | ✅ | ❌ | ❌ |
| AI 模型兼容性 | ✅ 10+ 主流模型 | ❌ | ❌ | ❌ |
| 批量生成 | ✅ | ✅ | ✅ | ❌ |
| 定价 | 免费（仅需 API Key） | $19/月起 | $19/月起 | $15/月起 |

**总结**：MoneyPrinterTurbo 是目前最免费的 AI 短视频生成工具，开源可本地部署，模型兼容性极强，且在 AI 生成素材和跨平台发布方面有明显优势。

---

## 如何使用

### 方式一：AI Agent 一键生成（最简单）

如果你的 AI Agent（如 Claude Code、Cursor Agent 等）支持读取 Skill 文档并操作本地终端，直接发送以下指令：

```
使用这个 Skill：https://raw.githubusercontent.com/harry0703/MoneyPrinterTurbo/main/docs/skill/SKILL.md
帮我生成一个主题为"人工智能如何改变普通人的日常生活"的视频。
```

Agent 会自动完成安装、配置和视频生成，仅需在缺少 API Key 时向你询问。

### 方式二：本地部署（推荐）

**前提条件**：Python 3.11 或更高版本。

```bash
# 克隆项目
git clone https://github.com/harry0703/MoneyPrinterTurbo.git
cd MoneyPrinterTurbo

# 使用 uv 管理依赖（推荐）
uv python install 3.11
uv sync --frozen
```

然后复制配置文件：

```bash
cp config.example.toml config.toml
```

编辑 `config.toml`，配置你的 API Key（支持 Kimi、OpenAI、DeepSeek、Ollama 等）。

启动 WebUI：

```bash
uv run streamlit run app.py
```

启动后自动打开浏览器访问 http://127.0.0.1:8501。

### 方式三：Docker 部署

```bash
cd MoneyPrinterTurbo
cp config.example.toml config.toml
docker compose -f docker-compose.release.yml up
```

访问 http://127.0.0.1:8501 使用 WebUI，或访问 http://127.0.0.1:8080/docs 查看 API 文档。

### 方式四：Google Colab 在线体验

无需本地安装，点击[此链接](https://colab.research.google.com/github/harry0703/MoneyPrinterTurbo/blob/main/docs/MoneyPrinterTurbo.ipynb)直接在 Google Colab 中运行。

### 方式五：Windows 一键启动包

下载[最新 Release](https://github.com/harry0703/MoneyPrinterTurbo/releases/latest)中的 Windows 一键启动包，解压后：

1. 双击执行 `update.bat` 更新到最新代码
2. 双击 `start.bat` 启动

> 注意：路径不要包含中文、特殊字符或空格。

---

## 配置要求

| 项目 | 最低配置 | 推荐配置 | 理想配置 |
|------|----------|----------|----------|
| CPU | 4 核 | 6-8 核 | 8 核及以上 |
| RAM | 4 GB | 8 GB | 16 GB 及以上 |
| GPU | 非必须 | 4 GB 显存 | 8 GB 显存及以上 |

> 如果你主要依赖云端 LLM 和云端 TTS，CPU 与内存比 GPU 更重要。启用 `faster-whisper` 或批量生成时，GPU 会明显提升速度。

---

## 总结

MoneyPrinterTurbo 是目前开源社区中最成熟的 AI 短视频生成工具之一。它的核心优势在于：

- **真正的一站式**：从脚本到成片，全程自动化
- **极高的模型兼容性**：支持 10+ 主流 AI 模型，你已有 API Key 的都能用
- **开源免费**：本地部署零成本，数据完全自控
- **持续迭代**：GitHub Star 数已突破 15 万，社区活跃，更新频繁
- **AI 生成素材**：接入 Seedance 等文生视频模型，不再受限于库存素材

无论你是想快速产出科普短视频、产品宣传，还是纯粹想体验 AI 创作的乐趣，MoneyPrinterTurbo 都值得尝试。

**推荐指数：★★★★★**

🔗 项目地址：https://github.com/harry0703/MoneyPrinterTurbo

生成视频后可用本站的 [文本去重工具](/tools/text-deduplicator/) 清理重复文案，或用 [Base64 编码解码工具](/tools/base64-encode-decode/) 处理素材编码。
