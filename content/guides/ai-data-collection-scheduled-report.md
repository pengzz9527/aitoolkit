---
title: "用AI做定时数据采集与报表：零基础设置自动抓取网站数据并生成周报（2026实战教程）"
date: 2026-07-24
draft: false
description: "零基础用AI自动采集网页数据并生成周报的完整教程：从设置定时任务、抓取竞品价格到自动生成CSV报表，全程零代码操作。"
tags: ["AI", "ChatGPT", "数据采集", "自动化", "定时任务", "周报", "教程", "零代码"]
image: /images/guides/ai-data-collection-report.png
---

你每天都在关心竞争对手的价格变化吗？你的产品需要在固定时间收集行业数据并生成报告吗？手动复制粘贴不仅浪费时间，还容易出错——漏掉一行数据、填错一个单元格都是常有的事。

**2026年，这些重复性工作完全可以交给AI自动完成。**

本文将手把手教你用ChatGPT编写自动化脚本，配合定时调度工具，实现从数据采集、清洗到报表生成的全流程自动化。不需要写一行代码，不需要搭建服务器，只需要一台电脑和免费的在线工具。

---

## 一、场景说明：我们要做什么

假设你是一个电商运营人员，每天需要收集三个竞品的商品价格和库存状态，每周五下午生成一份周报发给团队。传统做法是：打开浏览器 → 逐个访问竞品网站 → 复制数据到Excel → 整理格式 → 发送邮件。整个过程至少耗时30分钟。

通过AI自动化，这套流程可以压缩到**零人工干预**。我们分三步来实现：

1. 用AI编写数据采集脚本
2. 用定时任务调度器自动执行
3. 用数据分析工具生成可视化报表

---

## 二、第一步：让AI帮你写数据采集脚本

### 2.1 明确采集需求

在找ChatGPT之前，先想清楚你要采集什么。以竞品价格监控为例，你需要告诉AI：

- **目标网站**：比如 `https://example-shop.com/product/123`
- **采集字段**：商品名称、价格、库存状态、更新时间
- **输出格式**：CSV文件（推荐，方便后续分析）

### 2.2 用ChatGPT生成Python脚本

打开ChatGPT或Claude，输入以下提示词（直接复制使用）：

```
请帮我写一个Python脚本，实现以下功能：
1. 使用requests库访问指定URL获取网页HTML
2. 使用BeautifulSoup解析页面，提取商品名称、价格和库存信息
3. 将结果保存为CSV文件，文件名格式为 price_YYYYMMDD.csv
4. 如果访问失败，记录错误日志到 error.log
5. 添加详细的中文注释

目标URL示例：https://example-shop.com/product/123
价格CSS选择器示例：.product-price
库存CSS选择器示例：.stock-status

请确保代码兼容Python 3.8+，并在开头列出所需依赖包。
```

AI会返回一个完整的Python脚本。关键部分包括：

- `requests.get()` 发起HTTP请求
- `BeautifulSoup(html, 'html.parser')` 解析HTML
- `csv.writer()` 写入CSV文件
- `try/except` 异常处理

### 2.3 安装依赖并测试

脚本生成后，在终端运行以下命令安装依赖：

```bash
pip install requests beautifulsoup4
```

然后运行脚本测试：

```bash
python collect_prices.py
```

检查生成的CSV文件内容是否正确。如果数据格式不对，回到ChatGPT调整CSS选择器，让它重新生成代码。

> **小技巧**：如果目标网站有反爬机制（如返回403），可以在提示词中加上"添加headers模拟浏览器访问"，AI会自动加入User-Agent等请求头。

---

## 三、第二步：设置定时任务自动执行

采集脚本写好了，但每次手动运行还是很麻烦。接下来我们用定时任务让它在固定时间自动执行。

### 3.1 方案A：使用Cron（Linux/Mac）

如果你用的是Mac或Linux系统，Cron是最简单的选择。

**步骤1：让AI帮你生成Cron表达式**

打开我们的 [Cron 表达式生成器](/tools/cron-builder/)，选择"每周五下午5点"，它会生成对应的表达式：

```
0 17 * * 5
```

或者直接用 [Cron 表达式解析器](/tools/cron-expression-parser/) 验证一下这个表达式的含义——它表示"每周星期五 17:00 执行"。

**步骤2：添加到系统Cron**

```bash
crontab -e
```

在末尾添加一行：

```
0 17 * * 5 cd ~/price-monitor && python collect_prices.py >> cron.log 2>&1
```

这样每周五下午5点，脚本就会自动运行并生成当天的数据文件。

### 3.2 方案B：使用GitHub Actions（免费，跨平台）

如果你不想配置本地定时任务，GitHub Actions 是一个更好的选择——完全免费，不需要开电脑。

让ChatGPT帮你生成workflow文件：

```
请帮我写一个GitHub Actions workflow YAML文件，
功能是每周五下午5点（UTC时间）运行一次Python脚本。
脚本路径是 scripts/collect_prices.py。
运行环境是 ubuntu-latest，Python 3.11。
请在workflow中将生成的CSV文件上传为artifact。
```

生成的 `.github/workflows/price-collect.yml` 大致如下：

```yaml
name: Price Collection
on:
  schedule:
    - cron: '0 17 * * 5'
  workflow_dispatch:

jobs:
  collect:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: '3.11'
      - run: pip install requests beautifulsoup4
      - run: python scripts/collect_prices.py
      - uses: actions/upload-artifact@v4
        with:
          name: price-data
          path: "*.csv"
```

把文件提交到GitHub仓库后，Actions会在每到设定时间自动触发。

### 3.3 方案C：使用Hermes Agent Cron（推荐）

如果你已经在使用 [Hermes Agent](https://github.com/NousResearch/hermes-agent)，它的内置cron调度器是最省心的方案。通过 `hermes cron create` 命令即可创建定时任务，支持自然语言描述（如"every Friday at 5pm"），无需记忆复杂的Cron语法。

---

## 四、第三步：用AI分析采集的数据并生成报表

数据已经自动采集了，接下来要做的是分析和展示。

### 4.1 批量查看CSV数据

如果采集了多个文件，可以用 [CSV 查看器](/tools/csv-viewer/) 直接在浏览器中打开CSV文件，快速预览数据结构。支持拖拽上传，无需安装任何软件。

### 4.2 用SQL查询分析数据

当数据量变大后，用Excel筛选就太慢了。这时候用SQL查询会高效得多。

打开 [CSV/SQL 在线分析器](/tools/csv-sql-analyzer/)，上传你的CSV文件，然后用SQL语句进行各种分析：

```sql
-- 查看每个商品的平均价格
SELECT product_name, AVG(price) as avg_price
FROM data
GROUP BY product_name
ORDER BY avg_price DESC;

-- 查看价格波动超过10%的商品
SELECT product_name, 
       MAX(price) - MIN(price) as price_range,
       ROUND((MAX(price) - MIN(price)) / MIN(price) * 100, 2) as change_pct
FROM data
GROUP BY product_name
HAVING change_pct > 10;
```

所有计算都在浏览器内完成，数据不会上传到任何服务器，安全又快速。

### 4.3 让AI帮你写分析报告

数据准备好了，最后一步是生成文字报告。把CSV中的关键数据粘贴给ChatGPT，用这样的提示词：

```
我是一名电商运营人员。以下是本周采集的竞品价格数据：

[粘贴CSV数据或关键统计结果]

请帮我写一份简洁的周报，包含以下内容：
1. 本周整体价格趋势（上涨/下降/持平）
2. 重点竞品的价格变动分析
3. 发现的价格异常波动
4. 下周建议关注的商品

字数控制在500字以内，语气专业但不生硬。
```

ChatGPT会生成一份可以直接发送给团队的周报。

---

## 五、进阶：搭建完整的数据采集流水线

当你掌握了基础流程后，可以尝试搭建更完善的自动化系统。

### 5.1 多源数据聚合

让AI帮你扩展脚本，同时采集多个来源的数据：

```python
# 让ChatGPT生成的多源采集代码框架
sources = [
    {"url": "https://shop-a.com/product/1", "name": "Shop A"},
    {"url": "https://shop-b.com/product/1", "name": "Shop B"},
    {"url": "https://shop-c.com/product/1", "name": "Shop C"},
]

for source in sources:
    html = requests.get(source["url"]).text
    # ... 解析逻辑 ...
    # 所有数据追加到同一个CSV文件
```

### 5.2 数据质量检查

在采集脚本中加入数据验证：

```python
# 让ChatGPT添加数据校验
if price <= 0:
    logger.warning(f"价格异常: {product_name} = {price}")
    continue  # 跳过这条数据
```

### 5.3 告警通知

当价格变动超过阈值时，让AI帮你添加通知功能：

```
请在Python脚本中添加邮件通知功能：
当检测到商品价格下降超过15%时，
自动发送一封邮件到我的邮箱，
包含商品名称、原价、现价和降幅。
使用smtplib库实现。
```

---

## 六、常见问题排查

### Q1：采集脚本运行时没有数据

**原因**：网页结构可能已更新，CSS选择器失效。

**解决**：
1. 先用浏览器开发者工具检查目标页面的实际HTML结构
2. 把新的HTML片段发给ChatGPT，让它更新选择器
3. 运行脚本并查看输出确认

### Q2：定时任务没有执行

**原因**：Cron路径问题或权限不足。

**解决**：
1. 在脚本开头添加 `#!/usr/bin/env python3` shebang
2. 使用绝对路径：`/usr/bin/python3 collect_prices.py`
3. 用 `crontab -l` 确认任务已添加
4. 查看 cron.log 了解执行日志

### Q3：目标网站拒绝访问

**原因**：IP被封或需要登录。

**解决**：
1. 让ChatGPT在请求头中添加更多模拟字段（Referer、Accept-Language等）
2. 添加随机延迟：`time.sleep(random.uniform(1, 3))`
3. 考虑使用代理IP服务

---

## 七、总结：从零到一的自动化工作流

回顾一下我们今天做的事情：

| 步骤 | 工具 | 耗时 |
|------|------|------|
| 编写采集脚本 | ChatGPT + Python | 10分钟 |
| 设置定时任务 | Cron / GitHub Actions | 5分钟 |
| 数据分析 | [CSV/SQL 在线分析器](/tools/csv-sql-analyzer/) | 5分钟 |
| 生成周报 | ChatGPT | 3分钟 |

整个流程建立完成后，你只需要每周五花3分钟审核一下AI生成的周报，其余时间完全不用管。

**核心思路**：AI不是替代你思考，而是替你完成那些枯燥、重复、容易出错的工作。把精力留给真正需要判断力的事情——比如根据数据做出商业决策。

如果你想深入学习数据处理技能，推荐阅读 [duckdblab.org/zh/](https://duckdblab.org/zh/) 上的DuckDB实战教程，掌握更高效的数据分析方法。

---

*本文是「AI 应用指南」系列文章之一。查看更多 AI 实战教程，请访问 [AI 应用指南](/guides/) 栏目。*
