---
title: 'Codex Security 评测：OpenAI 官方安全漏洞扫描工具'
date: 2026-08-06T08:00:00+08:00
description: 'Codex Security 是 OpenAI 官方推出的安全漏洞扫描 CLI 和 TypeScript SDK，支持多模型提供商，能自动发现、验证并修复代码中的安全漏洞。'
tags:
  - AI工具
  - 安全工具
  - 代码扫描
  - OpenAI
  - DevSecOps
  - GitHub趋势
categories:
  - AI工具评测
---

## 一句话介绍

**Codex Security** 是 OpenAI 官方推出的安全漏洞扫描工具，集 CLI 命令行工具和 TypeScript SDK 于一体，能够自动发现、验证并修复代码中的安全漏洞。支持 OpenAI、OpenRouter、Fireworks、Amazon Bedrock 等多种模型提供商。

---

## 它是什么？

在 AI 编码助手普及的当下，代码安全漏洞的引入风险也在增加。开发者使用 AI 生成代码时，可能无意中引入安全缺陷——SQL 注入、XSS、硬编码密钥等问题层出不穷。Codex Security 正是为了解决这一痛点而生。

Codex Security 于 2026 年 7 月 13 日发布，采用 **Apache-2.0 许可证**开源，由 OpenAI 官方维护。项目发布后迅速获得关注，截至 2026 年 8 月 6 日，已在 GitHub 上收获 **8,875+ Stars** 和 **617+ Forks**，成为 DevSecOps 领域的热门工具。

---

## 核心功能

### 1. 自动漏洞扫描

Codex Security 可以扫描整个项目目录，自动识别潜在的安全漏洞，包括：
- SQL 注入和 NoSQL 注入
- 跨站脚本攻击（XSS）
- 硬编码密钥和凭证
- 不安全的依赖项
- 路径遍历漏洞
- 认证和授权缺陷

### 2. 多模型支持

与大多数只支持单一模型的扫描工具不同，Codex Security 支持多种 AI 模型提供商：
- **OpenAI**：原生支持 GPT 系列模型
- **OpenRouter**：支持 Anthropic Claude、Google Gemini 等
- **Fireworks AI**：支持 Qwen3 等大模型
- **Amazon Bedrock**：支持 OpenAI GPT、Claude 等

这让开发者可以根据成本、性能需求灵活选择模型。

### 3. 智能修复建议

Codex Security 不仅能发现问题，还能提供具体的修复建议，并可直接应用到代码中。支持多种扫描模式：
- **标准模式**：快速扫描，适合日常 CI/CD
- **深度模式**（`--mode deep`）：更彻底的扫描，可配置 workers、subagents 等参数
- **自定义参数**：支持 max-discovery-runs、stop-after-no-new 等高级配置

### 4. 扫描历史对比

支持 `scans compare BEFORE_SCAN_ID AFTER_SCAN_ID` 命令，自动匹配两次扫描的漏洞，识别新增、消失、复发或持续存在的问题，帮助团队追踪安全改进进度。

### 5. 容器化批量扫描

提供官方 Docker 镜像和 Docker Compose 配置，支持对 Git 仓库进行不可变版本的批量扫描，适合 CI/CD 流水线集成。

---

## 适用人群

- **全栈开发者**：希望在日常开发中集成安全扫描
- **DevSecOps 工程师**：需要在 CI/CD 流程中自动化安全检测
- **安全研究人员**：快速审计开源项目或企业内部代码
- **技术负责人**：管理团队代码质量，降低安全风险

---

## 与同类工具对比

| 特性 | Codex Security | Snyk | SonarQube | Semgrep |
|------|----------------|------|-----------|---------|
| AI 驱动 | ✅ | ⚠️ 部分 | ❌ | ❌ |
| 多模型支持 | ✅ | ❌ | ❌ | ❌ |
| 自动修复 | ✅ | ⚠️ 有限 | ❌ | ⚠️ 有限 |
| 开源 | ✅ Apache-2.0 | ❌ | ⚠️ 部分 | ✅ |
| 安装复杂度 | 低 | 中 | 高 | 低 |
| 社区活跃度 | 高 | 中 | 高 | 高 |

Codex Security 的核心优势在于**AI 原生设计**——它不是传统静态分析工具的 AI 包装，而是从设计之初就利用大语言模型理解代码语义和上下文，这使得它在识别复杂安全漏洞方面表现更出色。

---

## 如何使用

### 安装

```bash
npm install @openai/codex-security
```

### 快速开始

```bash
# 登录认证
npx @openai/codex-security login

# 标准扫描
npx @openai/codex-security scan .

# 深度扫描（使用特定模型）
npx @openai/codex-security scan . --model gpt-5.6-terra --effort high

# 深度扫描（自定义并发）
npx @openai/codex-security scan . --mode deep --workers 2 --subagents 0 --stop-after-no-new 3 --max-discovery-runs 10
```

### CI/CD 集成

在 CI 环境中使用 API Key 代替登录：

```bash
export OPENAI_API_KEY=your-api-key
npx @openai/codex-security scan . --auth api-key
```

### 使用其他模型提供商

```bash
# OpenRouter
export OPENROUTER_API_KEY="your-key"
npx @openai/codex-security scan . --provider openrouter --model anthropic/claude-sonnet-4.5

# Fireworks AI
export FIREWORKS_API_KEY="your-key"
npx @openai/codex-security scan . --provider fireworks --model accounts/fireworks/models/qwen3-235b-a22b
```

### TypeScript SDK 使用

```typescript
import { CodexSecurity } from "@openai/codex-security";

const security = new CodexSecurity();
const result = await security.run(".");

// 深度扫描配置
await security.run(".", {
  mode: "deep",
  workers: 2,
  subagents: 0,
  stopAfterNoNew: 3,
  maxDiscoveryRuns: 10,
});

console.log(result.reportPath);
await security.close();
```

---

## 总结推荐指数

Codex Security 是 OpenAI 在 AI 安全领域的重要布局，它的出现标志着安全扫描工具正在从传统的规则匹配向语义理解演进。

**优点：**
- OpenAI 官方出品，质量和维护有保障
- 支持多种 AI 模型，灵活选择
- AI 驱动的漏洞发现和修复建议
- 安装使用简单，文档清晰
- 开源且采用 Apache-2.0 许可证

**不足：**
- 部分高级功能需要 Tr austed Access for Cyber 审批
- 深度扫描可能产生较多误报
- 对私有代码库需要谨慎处理 API Key

**推荐指数：⭐⭐⭐⭐☆（4/5）**

如果你在使用 AI 辅助编程，或者关注代码安全问题，Codex Security 是一个值得尝试的工具。它不仅能帮你发现漏洞，还能直接提供修复方案，大幅降低安全开发的学习成本。

使用后可配合本站的 [文本计数器](/tools/text-counter/) 评估输出质量。

---

**相关链接：**
- GitHub: https://github.com/openai/codex-security
- 官方文档: https://learn.chatgpt.com/docs/security/cli
- npm 包: https://www.npmjs.com/package/@openai/codex-security
