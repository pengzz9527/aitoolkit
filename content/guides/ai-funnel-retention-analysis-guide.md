---
title: "用AI做用户漏斗分析与留存分析：从原始行为数据到可落地改进方向（2026实战教程）"
date: 2026-11-26
draft: false
description: "想知道用户在哪一步流失、为什么不再回来？这篇教程给你一条能落地的路径：先用CSV-SQL分析器从原始数据生成漏斗SQL，再让AI写留存和同期群查询，最后输出改进报告。不用会写代码，一份CSV就能跑通。"
tags: ["AI", "漏斗分析", "留存分析", "数据分析", "用户增长", "教程"]
image: /images/guides/ai-guide-cover.png
---

产品一上线，最常被问的两个问题：用户在哪一步流失了？用完还会回来吗？很多团队手里要么只有"总访问、总成交"两个数，要么有一堆行为日志却没人会看。这篇教程的核心，是把原始行为数据交给 AI，拿到三样东西：**漏斗**（在哪掉的）、**留存**（还剩多少）、**同期群**（是产品变差还是这批用户不行）。全程不用自己写代码。

## 一、先用一句话分清三件套

- **漏斗**：把一条从入口到完成的路径切成 3-7 步，看每步之间掉了多少人。回答"哪一步最该修"。
- **留存**：圈一批用户，看他们第一次动作后的第 N 天还有多少回来。回答"是否真的在用"。
- **同期群**：把多批用户的留存曲线叠在一起看。同一列普遍下滑=产品在变差，单独一行异常=那批用户不行。回答"别怪错人"。

三件事互补：漏斗找流失点，留存测粘性，同期群排时间干扰。

## 二、第一步：把原始数据备齐

你需要一份行为事件导出，至少三列：`user_id`、`event`（事件名）、`ts`（时间戳）。导出成 CSV。

动手前先用 [CSV 查看器](https://198007.xyz/tools/csv-viewer/) 扫一眼两件事：事件名口径是否一致（`view` 和 `view_product` 是不是一回事）、有没有测试号脏数据。这两类没清掉，后面所有数字都会偏。

## 三、第二步：让 AI 写漏斗查询

会 SQL 的直接写，不会就用 [CSV-SQL 分析器](https://198007.xyz/tools/csv-sql-analyzer/)：把表头贴进去，描述成"算商品浏览→加购→开始结算→支付成功每一步的转化率"，它会给出可跑的查询。

电商结算漏斗的核心思路，是"每个用户一行、取每个事件最早时间戳"，再聚合：

```sql
WITH steps AS (
  SELECT user_id,
         MIN(CASE WHEN event='view_product' THEN ts END) AS t1,
         MIN(CASE WHEN event='add_cart'     THEN ts END) AS t2,
         MIN(CASE WHEN event='checkout'     THEN ts END) AS t3,
         MIN(CASE WHEN event='pay_success'  THEN ts END) AS t4
  FROM events GROUP BY user_id
)
SELECT COUNT(t1) AS view,
       COUNT(t2) AS add_cart,
       COUNT(t3) AS checkout,
       COUNT(t4) AS paid,
       ROUND(COUNT(t2)*100.0/COUNT(t1),1) AS cvr_view_cart,
       ROUND(COUNT(t3)*100.0/COUNT(t2),1) AS cvr_cart_check,
       ROUND(COUNT(t4)*100.0/COUNT(t3),1) AS cvr_check_pay
FROM steps;
```

记住三点：`MIN(ts)` 取最早一次动作；`COUNT(列)` 会自动跳过 NULL，所以只统计"到达这一步"的人；转化率用"当前步 ÷ 上一步"。

AI 生成的 SQL 常带格式问题或漏括号，丢进 [SQL 格式化器](https://198007.xyz/tools/sql-formatter/) 清理一遍再跑，避免把语法错误当成数据问题。

选步骤有两条原则：一是 3 到 7 步，再多没人看得完；二是每步都得是用户明确的一个动作，别用"浏览中""意向高"这种含糊状态。想同时看新用户转化和整体转化，就给查询加一个"是否首次访问"维度拆开算，这两种口径差距能大到一倍。

## 四、第三步：让 AI 写留存和同期群

留存需要一张 `user_days` 表（`user_id` + 活跃日期，活跃一天一行）。算每周新用户次周 D7 留存：

```sql
WITH cohort AS (
  SELECT user_id, MIN(d) AS signup_day
  FROM user_days GROUP BY user_id
)
SELECT c.signup_day,
       COUNT(DISTINCT c.user_id) AS new_users,
       COUNT(DISTINCT CASE
         WHEN u.d = c.signup_day + 7 THEN u.user_id END) AS retained_d7
FROM cohort c
LEFT JOIN user_days u ON c.user_id = u.user_id
GROUP BY c.signup_day ORDER BY c.signup_day;
```

让 AI 直接写并解释：`signup_day + 7` 就是 D7 口径，`LEFT JOIN` 保证没回来的用户也进分母。想看"整体留存没变"里藏着什么，再按新老或按周拆开看——这就是同期群视角的实际用法。

读留存数别看绝对值，看斜率。次日留存曲线掉得急但随后走平稳住，说明核心价值是成立的，缺的是召回机制；一直往下掉不企稳，说明价值本身没讲清楚。参考线大致是：游戏类次日 40%、七日 20%，工具类次日 20% 上下，电商更该盯 30 天复购而不是次日。别拿不同行业的数字互相对比，这是最常见的第一个坑。

还有一个容易翻车的点：同期群表必须以"用户自己的注册日"为锚，不能用自然周。锚点选错，就排不掉时间干扰，分不清到底是"产品变差了"还是"这批用户不行"。

## 五、第四步：输出改进报告

拿到数字后，最后一步是把数字变成动作。把三样东西喂给 AI：漏斗结果、留存曲线、业务背景。让它输出三段：①流失最大的一步和可能原因；②留存对照行业参考线（比如游戏类次日 40%、七日 20%）是否达标；③下一步该做哪一个实验来验证。

想把这套做成能自动更新的看板，就用 DuckDB 接上 [DuckDB Lab](https://duckdblab.org/zh/)，在浏览器里直接跑查询看趋势。等到要真正验证某个改进，再上 A/B 测试：流量分两组、只改一个变量、收够数据做显著性，那一步我们留到下一篇。
