---
title: "用AI Agent做个人自动化：从本地部署到智能工作的完整实战教程（2026版）"
date: 2026-09-23
description: "零基础学会搭建属于自己的AI Agent：从本地模型部署、工具配置到日常自动化任务，打造7×24小时在线的个人AI助理。无需编程基础，跟着步骤即可上手。"
tags: ["AI Agent", "本地部署", "Hermes", "自动化", "AI助理", "教程", "零基础", "2026"]
categories: ["guides"]
image: /images/guides/ai-agent-automation-guide.png
---

你是否也有这样的困扰：ChatGPT很强，但它只在你打开网页时才能用；想让AI帮你每天自动整理邮件、定时生成报表、监控服务器状态——这些重复性工作，你每次都得手动找AI做一遍。

**2026年，AI Agent让这一切成为可能。** Agent不是普通的聊天机器人，而是能自主调用工具、执行任务、持续运行的AI助手。你可以把它部署在自己的电脑上，让它7×24小时为你工作。

本篇教程将带你从零搭建一个属于你自己的AI Agent系统，覆盖从本地模型部署、工具配置到日常自动化任务的全流程。全程不需要深厚的编程基础，跟着步骤操作就行。

> 💡 提示：如果你需要处理Agent产生的结构化日志或自动化报表数据，可以使用本站的 [CSV/SQL在线分析器](https://198007.xyz/tools/csv-sql-analyzer/) 直接在浏览器里用SQL查询分析，无需安装任何软件。

---

## 一、AI Agent和普通AI有什么区别？

在开始之前，先搞清楚一个问题：**Agent和ChatGPT有什么区别？**

| | ChatGPT（普通AI） | AI Agent |
|--|--|--|
| 工作方式 | 你问一句，它答一句 | 你可以给它一个任务，它自己一步步完成 |
| 工具使用 | 只能聊天 | 能调用浏览器、终端、文件系统等工具 |
| 运行方式 | 必须你在线对话 | 可以后台运行，定时执行任务 |
| 记忆能力 | 每次对话独立 | 可以跨会话记住你的偏好和习惯 |
| 适合场景 | 问答、写作、翻译 | 自动化工作流、定时任务、复杂项目 |

举个例子：你想"每周生成一份销售数据汇总并发送邮件"。

- 用ChatGPT：你得每周打开网页，描述需求，复制结果，再手动发邮件。
- 用AI Agent：你告诉它一次规则，它自己每周自动执行，结果直接发到你的邮箱。

这就是Agent的价值——**把一次性对话变成可持续的自动化工作流**。

---

## 二、选择你的Agent框架

市面上有很多AI Agent框架，对于个人用户来说，我推荐两个方向：

### 方案A：Hermes Agent（推荐新手）

[Hermes Agent](https://github.com/NousResearch/hermes-agent) 是一个开源的AI Agent框架，支持多种模型（OpenAI、Anthropic、DeepSeek等），内置终端、文件、Web搜索等工具集，还能部署为Telegram/Discord机器人。

**优点：**
- 开箱即用，命令简单
- 支持多平台（Telegram、Discord、Slack等）
- 技能系统可自定义扩展
- 完全开源免费

### 方案B：自建Agent（适合有编程基础的用户）

如果你会Python，可以用LangChain、LlamaIndex等框架自己搭建。但这个过程需要较多开发工作，不适合只想快速上手的用户。

**本文以Hermes Agent为例**，手把手教你完成从安装到日常使用的全流程。如果你已经用过本站的[本地部署大模型教程](https://198007.xyz/guides/ai-local-model-assistant-guide/)，那这部分会更轻松。

---

## 三、第一步：安装Hermes Agent

### 3.1 环境准备

确保你的电脑满足以下条件：
- 操作系统：Linux（推荐Ubuntu 20.04+）、macOS 12+ 或 WSL2
- Python 3.10+
- 内存：至少8GB（运行本地模型建议16GB+）
- 网络：需要访问模型API

### 3.2 一键安装

打开终端，运行以下命令：

```bash
curl -fsSL https://raw.githubusercontent.com/NousResearch/hermes-agent/main/scripts/install.sh | bash
```

安装完成后，验证是否成功：

```bash
hermes --version
```

如果输出版本号，说明安装成功。

### 3.3 初始化配置

运行setup向导，按照提示完成基础配置：

```bash
hermes setup
```

setup会引导你配置：
1. **模型选择** — 选择你想用的模型提供商（OpenRouter、Anthropic、DeepSeek等）
2. **终端环境** — 确认终端类型（local/docker/ssh）
3. **工具集** — 选择需要启用的工具（文件、终端、Web搜索等）
4. **网关平台**（可选）— 如果你想通过Telegram/Discord使用Agent

---

## 四、第二步：配置模型和API密钥

### 4.1 选择模型提供商

Hermes支持18种以上的模型提供商。以下是几种常见选择：

| 提供商 | 特点 | 适合场景 |
|--------|------|----------|
| OpenRouter | 一个key调用多个模型 | 想尝试不同模型的用户 |
| Anthropic | Claude系列，推理能力强 | 复杂任务、长文本处理 |
| DeepSeek | 性价比高，中文理解好 | 日常自动化任务 |
| 本地Ollama | 完全离线，无需联网 | 隐私要求高的场景 |

**推荐新手使用OpenRouter**，注册后获得一个API key，就可以在多个模型之间切换。

### 4.2 添加API密钥

打开 `~/.hermes/.env` 文件，添加你的API密钥：

```bash
# OpenRouter
OPENROUTER_API_KEY=your_key_here

# 或者使用其他提供商
# ANTHROPIC_API_KEY=your_key_here
# DEEPSEEK_API_KEY=your_key_here
```

保存后，运行以下命令测试连接：

```bash
hermes doctor
```

如果看到所有检查项都是绿色✅，说明配置成功。

### 4.3 选择具体模型

运行模型选择命令，交互式的选择你想要的模型：

```bash
hermes model
```

例如选择 `deepseek/deepseek-chat`（性价比高）或 `anthropic/claude-sonnet-4`（推理能力强）。

---

## 五、第三步：配置工具集

工具集是Agent的"手脚"，决定了它能做什么。运行以下命令查看所有可用工具：

```bash
hermes tools list
```

### 5.1 推荐新手启用的工具

| 工具集 | 功能 | 是否必需 |
|--------|------|----------|
| `terminal` | 执行Shell命令 | ✅ 必需 |
| `file` | 读写文件、搜索内容 | ✅ 必需 |
| `web` | 网页搜索、内容抓取 | ✅ 推荐 |
| `memory` | 跨会话记忆 | ✅ 推荐 |
| `cronjob` | 定时任务调度 | ⭐ 推荐 |
| `delegation` | 子任务委派 | 可选 |
| `browser` | 浏览器自动化 | 可选 |

启用或禁用工具：

```bash
# 启用工具集
hermes tools enable terminal file web memory cronjob

# 禁用不需要的工具
hermes tools disable browser image_gen
```

### 5.2 配置记忆功能

记忆功能让Agent能记住你的习惯和偏好，是Agent比普通ChatGPT强大的关键。

在 `~/.hermes/config.yaml` 中配置：

```yaml
memory:
  memory_enabled: true
  user_profile_enabled: true
  provider: built-in  # 内置存储，无需额外配置
```

重启Agent后，记忆功能生效。你可以告诉Agent你的偏好，比如：

> "我是一名电商运营，平时用Python做数据分析，帮我记住这个背景。"

下次对话时，Agent会自动使用这些信息来调整回答风格。

---

## 六、第四步：创建你的第一个自动化任务

### 6.1 场景：每日AI新闻摘要

假设你每天早上想收到一份AI领域的最新新闻摘要。我们来设置一个定时任务。

**第1步：测试手动任务**

先在Chat模式下测试，让Agent帮你生成一份AI新闻摘要：

```bash
hermes chat
```

输入：
> 请搜索今天AI领域的最新新闻，整理成5条摘要，每条不超过100字。

确认结果满意后，退出chat模式。

**第2步：创建定时任务**

使用cron工具创建定时任务：

```bash
hermes cron create '0 8 * * *' \
  --prompt "搜索今天AI领域的最新新闻，整理成5条摘要，每条不超过100字，保存到 ~/daily-ai-news.md" \
  --schedule daily \
  --source agent
```

这表示每天早上8点自动执行。

**第3步：验证任务**

```bash
hermes cron list
```

确认任务已创建，然后可以手动触发一次测试：

```bash
hermes cron run <任务ID>
```

---

### 6.2 场景：定期备份重要文件

**第1步：编写备份脚本**

让Agent帮你写一个备份脚本。在chat中输入：

> 请帮我写一个Shell脚本，功能如下：
> 1. 备份 ~/Documents 目录下最近7天修改过的文件
> 2. 压缩后保存到 ~/backups/daily/
> 3. 文件名格式为 backup-YYYYMMDD.tar.gz
> 4. 保留最近30天的备份，自动清理旧文件

**第2步：测试脚本**

将生成的脚本保存为 `~/scripts/backup-daily.sh`，然后测试：

```bash
chmod +x ~/scripts/backup-daily.sh
~/scripts/backup-daily.sh
```

**第3步：设置定时执行**

```bash
hermes cron create '0 2 * * *' \
  --prompt "运行 ~/scripts/backup-daily.sh 并报告结果" \
  --workdir /root
```

---

### 6.3 场景：监控网站可用性

**第1步：创建监控脚本**

让Agent生成一个网站监控脚本：

> 请写一个Shell脚本，功能如下：
> 1. 检测指定URL是否可访问（HTTP状态码200表示正常）
> 2. 检测响应时间是否超过3秒
> 3. 检测SSL证书是否即将过期（少于30天）
> 4. 将结果写入日志文件，格式为JSON
> 5. 如果发现问题，打印警告信息

**第2步：设置定时监控**

```bash
hermes cron create '*/30 * * * *' \
  --prompt "运行 ~/scripts/monitor-site.sh 并汇总结果" \
  --workdir /root
```

每30分钟检查一次，异常时即时知晓。

---

## 七、进阶：技能系统

技能（Skills）是Hermes的核心特色——你可以把解决问题的流程保存为技能文档，让Agent在遇到类似问题时自动应用。

### 7.1 创建一个自定义技能

假设你经常需要处理CSV数据，可以创建一个数据处理技能：

**第1步：创建技能文件**

```bash
mkdir -p ~/.hermes/skills/csv-data-processing
```

**第2步：编写技能文档**

创建 `~/.hermes/skills/csv-data-processing/skill.md`：

```markdown
---
name: csv-data-processing
description: 处理CSV数据的标准工作流
version: 1.0.0
---

当你需要处理CSV数据时，按照以下步骤：

1. 使用CSV/SQL分析器在线工具查看数据概览：https://198007.xyz/tools/csv-sql-analyzer/
2. 用Python pandas读取CSV，查看数据结构
3. 根据用户需求进行数据清洗、转换或分析
4. 输出结果并解释关键发现
```

**第3步：使用技能**

在chat中加载技能：

```bash
hermes -s csv-data-processing
```

或者让Agent自动识别并使用：

> "帮我分析一下这个CSV文件..."

---

## 八、进阶：多平台部署

如果你希望随时随地访问你的Agent，可以部署到 messaging 平台。

### 8.1 Telegram Bot

**第1步：在Telegram中创建Bot**

1. 打开Telegram，搜索 `@BotFather`
2. 发送 `/newbot`，按提示设置Bot名称
3. 保存获得的API token

**第2步：配置Hermes**

在 `~/.hermes/config.yaml` 中添加：

```yaml
gateway:
  telegram:
    enabled: true
    bot_token: "your_bot_token_here"
```

**第3步：启动网关**

```bash
hermes gateway run
```

现在你可以在Telegram中直接和你的Agent对话了！

### 8.2 Discord Bot

配置方式类似，在config.yaml中添加Discord配置即可。详细步骤请参考官方文档。

---

## 九、日常使用技巧

### 9.1 常用命令速查

```bash
# 开始聊天
hermes chat

# 单次问答
hermes chat -q "帮我写一个Python脚本..."

# 恢复上次会话
hermes chat --continue

# 查看配置
hermes config

# 查看技能列表
hermes skills list

# 查看定时任务
hermes cron list

# 查看诊断信息
hermes doctor
```

### 9.2 会话内快捷指令

在chat模式中，你可以使用斜杠命令：

| 命令 | 功能 |
|------|------|
| `/new` | 新建会话 |
| `/model` | 切换模型 |
| `/tools` | 管理工具 |
| `/skills` | 搜索/安装技能 |
| `/cron` | 管理定时任务 |
| `/verbose` | 切换详细输出 |
| `/yolo` | 跳过危险命令确认 |
| `/exit` | 退出 |

### 9.3 与现有工具的配合

Agent可以和你已有的工具无缝配合：

- **配合DuckDB**：Agent生成的SQL查询可以直接在 [DuckDB在线环境](https://duckdblab.org/) 中执行验证
- **配合CSV分析器**：Agent处理后的数据可以导入 [CSV/SQL分析器](https://198007.xyz/tools/csv-sql-analyzer/) 进行可视化
- **配合本地模型**：如果需要完全离线的场景，可以先按[本地部署教程](https://198007.xyz/guides/ai-local-model-assistant-guide/)安装Ollama，再让Agent调用本地模型

---

## 十、常见问题排查

### 问题1：API调用失败

```bash
# 检查API密钥是否正确
cat ~/.hermes/.env | grep API_KEY

# 测试连接
hermes doctor
```

### 问题2：定时任务不执行

```bash
# 查看任务列表
hermes cron list

# 查看最近日志
tail -50 ~/.hermes/logs/agent.log
```

### 问题3：模型响应慢或错误

尝试切换模型：
```bash
hermes model
```

选择另一个模型（如从Claude切换到DeepSeek）。

### 问题4：工具集不生效

重启Agent或新建会话（`/new`）后再次尝试。工具变更需要新会话才能生效。

---

## 总结

通过本篇教程，你已经学会了：

1. ✅ 理解AI Agent与普通聊天机器人的区别
2. ✅ 安装和配置Hermes Agent
3. ✅ 选择合适的模型提供商和API密钥
4. ✅ 配置工具集和记忆功能
5. ✅ 创建日常自动化任务（新闻摘要、文件备份、网站监控）
6. ✅ 使用技能系统扩展Agent能力
7. ✅ 部署到Telegram/Discord等多平台
8. ✅ 排查常见问题

**下一步建议：**
- 从最简单的定时任务开始（如每日新闻摘要），逐步扩展到更复杂的自动化
- 阅读本站的[自动化运维教程](https://198007.xyz/guides/ai-automation-ops-server-management/)和[定时数据采集教程](https://198007.xyz/guides/ai-data-collection-scheduled-report/)，了解更多实用场景
- 尝试使用技能系统，把你的工作流沉淀为可复用的知识

AI Agent不是为了替代你，而是为了让你把时间花在更有价值的事情上。现在就开始搭建你的第一个Agent吧！
