---
title: "用AI做PDF批量处理：自动合并、拆分、提取文字与加水印（2026实战教程）"
date: 2026-08-30
description: "零基础学会用AI批量处理PDF：合并多个PDF、按页拆分、提取文字和图片、添加水印。ChatGPT+免费工具，办公室效率翻倍。"
tags: ["AI", "PDF处理", "批量处理", "办公自动化", "ChatGPT", "教程", "零代码"]
categories: ["guides"]
image: /images/guides/ai-pdf-batch-processing.png
draft: false
---

你是不是也有过这样的烦恼：手里有一堆PDF文件，需要合并成一份交给领导；或者要拆开一本PDF报告，每章单独发；又或者是从几十份PDF合同里提取特定条款……以前这些活儿要么手动操作半天，要么装一堆专用软件，又贵又难用。

**2026年的AI工具彻底改变了这个局面。** 你不需要安装任何专业软件，也不用学编程，用ChatGPT或Claude配合几个免费在线工具，就能批量搞定所有PDF处理需求。

本篇教程手把手教你用AI做PDF批量处理——合并、拆分、提取文字、添加水印，一篇全懂。

---

## 一、用AI合并多个PDF文件

### 场景：把分散的月度报告合并成一份年度汇总

这是最常见的需求。假设你有12个月的PDF报告，需要合并成一份全年汇总文件。

### 方法一：用ChatGPT Plus/Pro直接合并（最简单）

如果你用的是ChatGPT Plus或Pro版，可以直接在对话中上传多个PDF文件：

1. 打开 [chat.openai.com](https://chat.openai.com)，点击输入框旁的「+」号
2. 一次上传所有需要合并的PDF文件（建议不超过20个）
3. 发送提示词：

> 请帮我把这12个PDF文件按月份顺序合并成一个完整的PDF文档，保持原有格式不变。

ChatGPT 会处理文件并返回合并后的PDF下载链接。

**注意**：免费版的ChatGPT对文件数量和大小有限制，大批量文件推荐用下面的方法二。

### 方法二：用Python脚本批量合并（推荐用于大批量）

当你有50个甚至100个PDF需要合并时，让AI帮你写一段Python脚本效率最高。

打开ChatGPT，发送这段提示词：

> 我有一个需求：把某个文件夹下的所有PDF文件按文件名排序后合并成一个PDF。请用Python的PyPDF2库帮我写一个脚本，要求：1）支持中文文件名；2）显示合并进度；3）输出合并后的文件路径。请给出完整可运行的代码。

AI 会给你类似这样的代码：

```python
from PyPDF2 import PdfMerger
import os
import glob

folder = "/path/to/your/pdfs"
output_path = "/path/to/merged_output.pdf"

# 获取所有PDF文件并按名称排序
pdf_files = sorted(glob.glob(os.path.join(folder, "*.pdf")))

merger = PdfMerger()
for i, pdf in enumerate(pdf_files):
    print(f"正在合并第 {i+1}/{len(pdf_files)} 个文件...")
    merger.append(pdf)

merger.write(output_path)
merger.close()
print(f"合并完成！输出文件：{output_path}")
```

把代码保存为 `merge_pdfs.py`，然后运行：

```bash
pip install PyPDF2
python merge_pdfs.py
```

### 方法三：用 DuckDB + AI 做批量合并分析

如果你合并的PDF中包含大量表格数据，还需要在合并后进行分析，可以试试 [DuckDB AI](https://duckdblab.org/zh/)。它能让你在本地快速处理和分析合并后的结构化数据，无需写复杂代码。

---

## 二、用AI按页拆分PDF文件

### 场景：把一本50页的产品说明书拆成每章单独的文件

拆分PDF和合并一样，AI也能帮你自动化。

### 方法一：ChatGPT Plus直接操作

和合并类似，ChatGPT Plus/Pro支持直接拆分PDF：

> 请把这个PDF文件按每5页拆分成独立的PDF文件，命名为 page_1-5.pdf, page_6-10.pdf 这样。

### 方法二：AI生成拆分脚本

对于更复杂的拆分需求（比如按书签拆分、按标题页拆分），让AI写脚本：

> 我需要把一个PDF按章节拆分。已知每个章节的起始页码：第一章在第3页，第二章在第15页，第三章在第28页。请用Python写一个脚本，根据这些页码将PDF拆分成三个独立文件。

```python
from PyPDF2 import PdfReader, PdfWriter

input_pdf = "manual.pdf"
reader = PdfReader(input_pdf)

# 定义章节范围（起始页，结束页，输出文件名）
chapters = [
    (2, 14, "chapter1.pdf"),   # 页码从0开始计数
    (14, 27, "chapter2.pdf"),
    (27, len(reader.pages), "chapter3.pdf"),
]

for start, end, output in chapters:
    writer = PdfWriter()
    for page in reader.pages[start:end]:
        writer.add_page(page)
    with open(output, "wb") as f:
        writer.write(f)
    print(f"已生成：{output}")
```

### 小技巧：用 [文本计数器](https://198007.xyz/tools/text-counter/) 辅助决策

拆分前，你可能想知道每个章节大约有多少字、多少个表格。把PDF内容先提取出来（见下文第三步），然后用本站的文本计数器统计各段字数， helps 你决定拆分的粒度是否合理。

---

## 三、用AI从PDF批量提取文字内容

### 场景：从100份合同中提取所有金额、日期和条款

这是AI最能发挥价值的场景之一。传统方法需要一个个打开PDF复制粘贴，现在只需一条命令。

### 方法一：直接让AI读取PDF

ChatGPT Plus/Pro 支持直接上传PDF并提取文字：

> 请读取这个PDF文件，提取其中所有包含「金额」或「金额」的句子，列出它们所在的页码。

对于单个文件，这是最快的方式。

### 方法二：批量提取——AI生成Python脚本

当需要处理大量PDF时，批量提取脚本是更好的选择：

> 请写一个Python脚本，遍历指定文件夹下所有PDF文件，提取每份文件的文字内容并保存为对应的文本文件。同时提取所有数字（金额）和日期，保存到一个CSV文件中方便后续分析。

```python
import pdfplumber
import os
import csv
import re
from datetime import datetime

def extract_from_pdf(pdf_path):
    with pdfplumber.open(pdf_path) as pdf:
        all_text = ""
        numbers = []
        dates = []
        for page in pdf.pages:
            text = page.extract_text() or ""
            all_text += text + "\n"
            # 提取金额（包含逗号的分隔符数字）
            amounts = re.findall(r'[\d,]+\.?\d*', text)
            numbers.extend(amounts)
            # 提取日期
            date_patterns = re.findall(r'\d{4}[-/年]\d{1,2}[-/月]\d{1,2}[日]?', text)
            dates.extend(date_patterns)
        return all_text, numbers, dates

folder = "/path/to/pdfs"
csv_rows = []

for filename in sorted(os.listdir(folder)):
    if filename.endswith(".pdf"):
        filepath = os.path.join(folder, filename)
        text, numbers, dates = extract_from_pdf(filepath)
        csv_rows.append({
            "filename": filename,
            "word_count": len(text),
            "amounts": ", ".join(numbers[:20]),  # 前20个金额
            "dates": ", ".join(dates[:10]),       # 前10个日期
            "has_contract_clause": "条款" in text or "义务" in text
        })
        print(f"已处理：{filename}")

# 保存为CSV
with open("extracted_results.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=csv_rows[0].keys())
    writer.writeheader()
    writer.writerows(csv_rows)

print("批量提取完成！结果已保存到 extracted_results.csv")
```

运行脚本后，你会得到一个CSV文件，里面包含了所有PDF的提取结果，可以直接用 [CSV 在线查看器](https://198007.xyz/tools/csv-viewer/) 在线浏览和分析。

---

## 四、用AI给PDF批量添加水印

### 场景：给100份内部培训资料加上「内部资料 严禁外传」的水印

水印是保护文档版权的重要手段。AI 同样能帮你自动化这个流程。

### 方法一：ChatGPT生成加水印脚本

> 请写一个Python脚本，给指定文件夹下所有PDF文件添加半透明文字水印「内部资料」，水印需要倾斜45度角，居中显示，不遮挡正文内容。

```python
from PyPDF2 import PdfReader, PdfWriter
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
import os

def create_watermark():
    """生成水印PDF"""
    watermark_path = "watermark.pdf"
    c = canvas.Canvas(watermark_path, pagesize=A4)
    
    # 设置透明度和字体
    c.setFillColorRGBA(0, 0, 0, 0.15)  # 浅灰色，半透明
    c.setFont("Helvetica-Bold", 40)
    
    # 绘制倾斜水印（重复排列）
    width, height = A4
    c.saveState()
    c.translate(width // 2, height // 2)
    c.rotate(45)
    c.drawCentredString(0, 0, "内部资料  严禁外传")
    c.restoreState()
    c.save()
    return watermark_path

def add_watermark_to_pdf(input_pdf, output_pdf, watermark_pdf):
    reader = PdfReader(input_pdf)
    writer = PdfWriter()
    watermark = PdfReader(watermark_pdf)
    
    for page in reader.pages:
        page.merge_page(watermark.pages[0])
        writer.add_page(page)
    
    with open(output_pdf, "wb") as f:
        writer.write(f)

# 批量处理
watermark = create_watermark()
input_folder = "/path/to/source_pdfs"
output_folder = "/path/to/watermarked"

os.makedirs(output_folder, exist_ok=True)

for filename in sorted(os.listdir(input_folder)):
    if filename.endswith(".pdf"):
        input_path = os.path.join(input_folder, filename)
        output_path = os.path.join(output_folder, filename)
        add_watermark_to_pdf(input_path, output_path, watermark)
        print(f"已添加水印：{filename}")

print("全部完成！")
```

### 方法二：使用在线工具（无需编程）

如果你不想写代码，也可以用在线工具：

1. **ILovePDF**（ilovepdf.com）：免费版支持最多5个文件，批量加水印
2. **SmallPDF**（smallpdf.com）：界面友好，支持自定义水印文字和位置
3. **PDF24 Tools**（tools.pdf24.org）：完全免费，无文件数量限制

对于免费方案，推荐配合 [文本替换器](https://198007.xyz/tools/text-replacer/) 先准备好要批量处理的文件列表，然后逐个上传处理。

---

## 五、进阶：AI + DuckDB 做PDF数据分析

### 场景：合并100份月度报表后，用SQL查询分析趋势

如果你处理的PDF本身包含表格数据（如财务报表、销售报表），单纯合并还不够，你可能还需要分析其中的数字。

这时候，先用上面的方法提取PDF中的表格数据，然后用 [DuckDB AI](https://duckdblab.org/zh/) 做分析就非常方便。DuckDB 可以直接读取CSV文件，配合AI帮你写分析SQL，零代码完成数据透视、趋势分析和可视化。

举个例子，把提取出的CSV导入DuckDB后，一句SQL就能得到答案：

```sql
-- 查询所有合同中金额大于10万的记录
SELECT filename, amounts 
FROM extracted_results 
WHERE amounts LIKE '%10%' OR amounts LIKE '%100%';
```

---

## 六、完整工作流：从文件整理到最终交付

下面是一个典型的实际工作场景，把上述技能串联起来：

**场景**：你是一名行政人员，收到来自10个分公司的月度报告（每个分公司3-5份PDF），需要在周五前汇总成一份完整的集团报告，并标注来源。

### 步骤1：整理文件命名

让AI帮你规范文件名：

> 我有一个文件夹，里面的PDF文件名很乱。请写一个Python脚本，把所有PDF文件名统一改成「YYYYMM-分公司名称-报告类型.pdf」的格式，并生成一份文件清单CSV。

### 步骤2：提取关键数据

用前面讲的批量提取脚本，从所有PDF中提取数据，保存为CSV。

### 步骤3：合并同分公司文件

按分公司分组，分别合并各公司的PDF，然后再合并所有公司的汇总文件。

### 步骤4：添加水印

给最终的汇总文件加上「集团内部文件 2026年8月」的水印。

### 步骤5：用DuckDB分析

把提取的数据导入DuckDB，用自然语言提问（如「哪家分公司销售额最高？」），AI自动生成SQL帮你分析。

整个过程，从收到杂乱文件到拿出最终报告，熟练的话30分钟就能完成。

---

## 常见问题

**Q1：我的PDF是扫描版（图片格式），能用AI提取文字吗？**

可以。但普通OCR对中文效果参差不齐。推荐使用专门的OCR工具：
- [MiniMax GPT-4o](https://platform.minimaxi.com/) 支持中文OCR
- 腾讯混元大模型也提供OCR API
- 或者用前面的手写笔记识别教程（[这篇指南](https://198007.xyz/guides/ai-handwriting-ocr-guide/)）

**Q2：ChatGPT免费版本能处理PDF吗？**

ChatGPT免费版目前不支持上传PDF文件。建议：
- 升级Plus版（每月20美元）
- 或者用Claude Haiku（Anthropic免费额度）
- 或者用前面的Python脚本方案，完全免费

**Q3：处理敏感文件会不会泄露数据？**

如果是商业机密或个人隐私数据，不建议上传到任何在线服务。推荐使用本地Python脚本方案，所有操作都在本机完成，数据不会离开你的电脑。

---

## 总结

今天你学会了用AI做PDF批量处理的全套技能：

| 任务 | 推荐方法 |
|------|----------|
| 合并少量PDF（<20个） | ChatGPT Plus/Pro 直接操作 |
| 合并大量PDF | Python脚本（PyPDF2） |
| 按页拆分 | Python脚本 或 ChatGPT |
| 批量提取文字 | pdfplumber + Python |
| 批量加水印 | ReportLab + Python |
| 提取后数据分析 | DuckDB AI |

**核心思路**：AI最擅长的是帮你写代码和处理自然语言描述的任务。对于重复性的PDF操作，让AI生成脚本，以后遇到类似需求直接运行就好，一劳永逸。

下次再收到一堆PDF文件，别再手动一个个打开了。试试用AI自动化处理，你会发现办公室效率真的可以提升好几倍。
