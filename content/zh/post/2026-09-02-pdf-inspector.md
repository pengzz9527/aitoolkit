---
title: 'pdf-inspector 评测：Firecrawl 出品，Rust 写的 PDF 解析神器，18K+ 星'
date: 2026-09-02
tags: ['AI工具', 'PDF处理', 'Rust', '开源', '数据提取', 'Firecrawl']
categories: ['AI工具评测']
description: 'pdf-inspector 是 Firecrawl 团队出品的 Rust PDF 解析库，智能区分扫描件与文本PDF，直接输出 Markdown，性能远超 PyMuPDF4LLM 等传统方案，18K+ GitHub 星标。'
---

# pdf-inspector：PDF 解析的新一代 Rust 利器

**一句话简介**：pdf-inspector 是由 Firecrawl 团队开发的快速 Rust 库，用于 PDF 分类和文本提取，智能识别扫描版与文本版 PDF，自动输出干净的结构化 Markdown，无需 OCR 即可处理大多数日常文档。

---

## 工具概览

| 属性 | 信息 |
|------|------|
| 仓库地址 | [firecrawl/pdf-inspector](https://github.com/firecrawl/pdf-inspector) |
| 开发者 | Firecrawl (firecrawl.dev) |
| GitHub 星标 | ⭐ 18,090 |
| 语言 | Rust |
| 更新时间 | 2026-09-01 |
| 许可证 | MIT |
| 支持语言 | Python / Node.js / Rust / WebAssembly |
| 官网 | [firecrawl.dev](https://firecrawl.dev) |

---

## 核心功能

### 1. 智能 PDF 分类（TextBased / Scanned / ImageBased / Mixed）

pdf-inspector 最核心的卖点是在约 10-50ms 内判断 PDF 类型，返回置信度分数（0.0-1.0）以及每页是否需要 OCR 的路由建议。这意味着：

- 纯文本 PDF（约占 54%）完全跳过 OCR，直接在本地解析
- 扫描件只处理需要 OCR 的页面，大幅节省计算资源
- 混合文档可分章节路由，精准控制

### 2. 位置感知的文本提取

提取过程保留字体信息、X/Y 坐标，并自动处理多栏排版和从左到右/从右到左的阅读顺序。这对于学术论文、报纸排版等复杂布局的 PDF 尤其重要。

### 3. 直接输出结构化 Markdown

pdf-inspector 能将 PDF 直接转为干净的 Markdown，支持：
- H1-H4 标题（通过字号比例自动判断层级）
- 有序/无序/字母列表
- 代码块（等宽字体自动识别）
- 表格（矩形绘制检测 + 启发式对齐检测双模式）
- 粗体/斜体、URL 链接、分页符

### 4. 表格检测双模式

- **矩形绘制检测**：从 PDF 绘图操作中提取表格边框
- **启发式对齐检测**：根据文本对齐方式推断表格结构

支持财务报表、带注脚表格和跨页续表等复杂场景。

### 5. 选择性 OCR 集成

对于需要 OCR 的页面，pdf-inspector 提供 PP-OCRv6 Small 模型的本地集成。关键优势是：
- 默认不开 OCR 运行时，只有真正需要时才加载
- 原生 Python、Node.js 包包含 OCR 集成
- WebAssembly 版可在浏览器中运行，无需服务器往返

---

## 性能基准

在 [opendataloader-bench](https://github.com/opendataloader-project/opendataloader-bench) 基准测试（200 份 PDF，OCR 禁用）中：

| 引擎 | 综合评分 | 阅读顺序 | 表格 (TEDS) | 速度 (200份) |
|------|---------|---------|------------|-------------|
| **pdf-inspector** | **0.875** | **0.915** | **0.814** | **0.470s** |
| liteparse | 0.873 | 0.913 | 0.693 | 0.750s |
| opendataloader | 0.831 | 0.902 | 0.489 | 2.569s |
| pymupdf4llm | 0.735 | 0.886 | 0.401 | 17.117s |
| markitdown | 0.589 | 0.844 | 0.273 | 16.165s |

pdf-inspector 在综合评分、阅读顺序和表格质量三项上均领先，且速度是最快的——处理 200 份文档仅需 0.47 秒，比 PyMuPDF4LLM 快 36 倍。

---

## 适用人群

- **AI 工程师**：构建 RAG 系统时需要将 PDF 文档快速转为 Markdown 喂给 LLM
- **数据科学家**：需要从大量 PDF 中提取表格和结构化数据进行分析
- **内容创作者**：需要将学术论文、报告、技术文档转为易读格式
- **开发者工具链建设者**：需要在 Python/Node.js/Rust 项目中集成 PDF 解析能力
- **对 OCR 成本敏感的用户**：智能路由避免了对文本 PDF 不必要地调用 OCR API

---

## 与同类工具对比

| 特性 | pdf-inspector | PyMuPDF4LLM | MarkItDown | LiteParse |
|------|-------------|-------------|------------|-----------|
| 语言 | Rust | Python | Python | Python |
| 本地运行 | ✅ | ✅ | ✅ | ✅ |
| 智能分类 | ✅ 4类 | ❌ | ❌ | ⚠️ 基础 |
| 多栏支持 | ✅ 自动检测 | ⚠️ 需手动 | ❌ | ⚠️ 有限 |
| 表格质量 | ✅ 0.814 TEDS | ❌ 0.401 | ❌ 0.273 | ⚠️ 0.693 |
| 速度 | ✅ 0.47s/200 | ❌ 17.1s | ❌ 16.2s | ⚠️ 0.75s |
| 多语言绑定 | ✅ Python/Node/Rust/WASM | ✅ | ✅ | ✅ |
| CLI 工具 | ✅ | ⚠️ 需包装 | ✅ | ✅ |
| 可选 OCR | ✅ 选择性 | ❌ | ❌ | ⚠️ |

pdf-inspector 的核心差异化在于：它是目前唯一同时兼顾**高分表格质量**、**极速处理**和**智能 OCR 路由**的开源方案。PyMuPDF4LLM 虽然流行但速度较慢且表格效果一般；MarkItDown 表格评分接近零；LiteParse 速度尚可但表格质量和多栏支持不如 pdf-inspector。

---

## 如何使用

### Python 安装与使用

```bash
pip install pdf-inspector
```

```python
import pdf_inspector

# 基础解析（不触发 OCR）
result = pdf_inspector.process_pdf("document.pdf")
print(result.pdf_type)    # "text_based" / "scanned" / "image_based" / "mixed"
print(result.markdown)    # 干净的结构化 Markdown

# 选择性 OCR（仅处理需要 OCR 的页面）
ocr = pdf_inspector.process_pdf_with_ocr("document.pdf")
print(ocr.pages_routed_to_ocr)  # 需要 OCR 的页数
```

### Node.js 安装与使用

```bash
npm install @firecrawl/pdf-inspector
```

```javascript
import { readFileSync } from 'fs';
import { processPdf, processPdfWithOcr } from '@firecrawl/pdf-inspector';

const pdf = readFileSync('document.pdf');
const result = processPdf(pdf);
console.log(result.pdfType);   // "TextBased", "Scanned", ...
console.log(result.markdown);  // Markdown 字符串
```

### CLI 命令行

```bash
cargo install pdf-inspector

# 转为 Markdown
pdf2md document.pdf

# 输出 JSON（便于管道处理）
pdf2md document.pdf --json

# 带位置信息的文本项
pdf2md document.pdf --items-json
```

### 浏览器 WebAssembly

```bash
npm install @firecrawl/pdf-inspector-wasm
```

```javascript
import init, { processPdf } from '@firecrawl/pdf-inspector-wasm';

await init();
const response = await fetch('/document.pdf');
const pdf = new Uint8Array(await response.arrayBuffer());
const result = processPdf(pdf);
console.log(result.pdfType);
console.log(result.markdown);
```

---

## 总结

pdf-inspector 是 Firecrawl 团队继 Crawl4AI 之后推出的又一力作。它精准地解决了一个长期痛点：**如何快速、低成本地将 PDF 转为 AI 可用的 Markdown 格式**。

它的核心优势归纳为三点：
1. **快**：200 份 PDF 仅需 0.47 秒，比主流方案快数十倍
2. **准**：综合评分 0.875，表格和阅读顺序质量最高
3. **省**：智能路由只对需要 OCR 的页面调用 OCR，节省大量计算和 API 成本

无论你是构建 RAG 系统、处理批量文档，还是需要一个可靠的 PDF 解析后端，pdf-inspector 都值得一试。

**推荐指数：⭐⭐⭐⭐⭐（5/5）**

- 完全免费开源，MIT 许可
- 多语言绑定，Python / Node.js / Rust / WASM 全覆盖
- 性能卓越，适合生产环境大规模使用
- Firecrawl 团队持续维护，社区活跃

如果你正在寻找一款能够替代商业 PDF-to-Markdown API 的开源方案，pdf-inspector 是当前最佳选择之一。
