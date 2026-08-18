#!/usr/bin/env python3
"""Generate HN AI Morning Report for Telegram channel."""

import json
import urllib.request
import urllib.parse
import os
import sys
import time
from datetime import datetime, timezone, timedelta

def fetch_hn_algolia():
    url = "https://hn.algolia.com/api/v1/search?tags=front_page&hitsPerPage=40"
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=15) as resp:
            data = json.loads(resp.read().decode())
            return data.get("hits", [])
    except Exception as e:
        print(f"Algolia fetch failed: {e}", file=sys.stderr)
        return []

def fetch_hn_firebase():
    try:
        req = urllib.request.Request("https://hacker-news.firebaseio.com/v0/topstories.json", headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=15) as resp:
            ids = json.loads(resp.read().decode())[:50]
    except Exception as e:
        print(f"Firebase IDs fetch failed: {e}", file=sys.stderr)
        return []
    stories = []
    for sid in ids:
        try:
            req = urllib.request.Request(f"https://hacker-news.firebaseio.com/v0/item/{sid}.json", headers={"User-Agent": "Mozilla/5.0"})
            with urllib.request.urlopen(req, timeout=10) as resp:
                data = json.loads(resp.read().decode())
                if data.get("type") == "story":
                    stories.append(data)
        except Exception:
            pass
        time.sleep(0.05)
    return stories

def call_deepseek(prompt, retries=3):
    api_key = os.environ.get("DEEPSEEK_API_KEY", "")
    if not api_key:
        print("ERROR: DEEPSEEK_API_KEY not set", file=sys.stderr)
        return None
    url = "https://api.deepseek.com/chat/completions"
    headers = {"Content-Type": "application/json", "Authorization": f"Bearer {api_key}"}
    payload = {"model": "deepseek-chat", "messages": [{"role": "user", "content": prompt}], "temperature": 0.3, "max_tokens": 4096}
    for attempt in range(1, retries + 1):
        try:
            data = json.dumps(payload).encode()
            req = urllib.request.Request(url, data=data, headers=headers, method="POST")
            with urllib.request.urlopen(req, timeout=60) as resp:
                result = json.loads(resp.read().decode())
                return result["choices"][0]["message"]["content"]
        except urllib.error.HTTPError as e:
            if e.code == 429 and attempt < retries:
                wait = 60 * attempt
                print(f"Rate limited (429), retrying in {wait}s (attempt {attempt}/{retries})", file=sys.stderr)
                time.sleep(wait)
            else:
                print(f"DeepSeek API HTTP error: {e.code} on attempt {attempt}", file=sys.stderr)
                return None
        except Exception as e:
            print(f"DeepSeek API error on attempt {attempt}: {e}", file=sys.stderr)
            if attempt < retries:
                time.sleep(30)
            else:
                return None
    return None

def main():
    now = datetime.now(timezone.utc)
    bj = now + timedelta(hours=8)
    date_str = bj.strftime("%Y%m%d")
    weekday_map = ["周一","周二","周三","周四","周五","周六","周日"]
    full_date_cn = f"{bj.strftime('%Y年%m月%d日')}（{weekday_map[bj.weekday()]}）"

    print(f"Generating report for {full_date_cn}", file=sys.stderr)

    algolia_hits = fetch_hn_algolia()
    print(f"Algolia hits: {len(algolia_hits)}", file=sys.stderr)

    firebase_stories = fetch_hn_firebase()
    print(f"Firebase stories: {len(firebase_stories)}", file=sys.stderr)

    ai_keywords = [
        "ai","llm","gpt","openai","claude","deepseek","anthropic","gemini",
        "machine learning","neural","transformer","model","agent","robot",
        "autonomous","inference","quantization","benchmark","chatbot",
        "generative","diffusion","llama","mistral","grok","xai",
        "perplexity","cursor","copilot","sora","video generation",
        "artificial intelligence","prompt","rag","embedding","multimodal",
        "vision","reasoning","mcp","crewai","langchain","openclaw",
        "watermark","provenance","safety","alignment","rlhf","fine-tune",
    ]

    def is_ai(title, url):
        text = f"{title} {url}".lower()
        return any(k in text for k in ai_keywords)

    items = []
    seen = set()

    for hit in algolia_hits:
        title = hit.get("title", "")
        if not title or title in seen:
            continue
        seen.add(title)
        items.append({
            "title": title,
            "url": hit.get("url", ""),
            "points": hit.get("points", 0),
            "comments": hit.get("num_comments", 0),
        })

    for s in firebase_stories:
        title = s.get("title", "")
        if not title or title in seen:
            continue
        seen.add(title)
        items.append({
            "title": title,
            "url": s.get("url", ""),
            "points": s.get("score", 0),
            "comments": s.get("descendants", 0),
        })

    items.sort(key=lambda x: -x["points"])
    ai_items = [it for it in items if is_ai(it["title"], it.get("url", "")) or it["points"] >= 200]
    print(f"Total: {len(items)}, AI-filtered: {len(ai_items)}", file=sys.stderr)

    top = ai_items[:20]
    top_json = json.dumps(top, ensure_ascii=False, indent=2)

    prompt = f"""你是一位资深科技评论员，正在为「普通人生存指南」Telegram 频道撰写每日 AI 早报。

【今日日期】{full_date_cn}

【HN 今日热门 AI 资讯】（按热度排序）
{top_json}

【写作要求】
1. 挑选 3-5 条最值得关注的 AI 资讯作为头条，每条包括：
   - 标题 + 一句话概括
   - 💡 这意味着：这句话要回答"用户看到这条资讯有什么用？"
2. 补充行业动态板块（可选，有内容才写）
3. 给出「我的判断」板块：提炼今天 2-3 个核心信号
4. 语言风格：简洁有力，不说废话，不堆砌信息，每条资讯都要有洞察
5. 格式：纯文本，用 Emoji 标记板块，适合 Telegram 阅读
6. 总长度控制在 600-1000 字

【输出格式】
🤖 AI 早报 | {full_date_cn}

你的价值不是报道新闻，而是帮你节省时间、做出更好的技术决策。

━━━━━━━━━━━━━━━━━━━━

🔥 头条一：[标题]
[简短描述]
💡 这意味着：[对用户有用的洞察]

━━━━━━━━━━━━━━━━━━━━

📊 行业动态
• ...

━━━━━━━━━━━━━━━━━━━━

🎯 我的判断
今天的 AI 资讯传递了 [N] 个清晰信号：
1️⃣ ...
2️⃣ ...

━━━━━━━━━━━━━━━━━━━━

数据来源：Hacker News
下期见 👋"""

    print("Calling DeepSeek API...", file=sys.stderr)
    report = call_deepseek(prompt)

    if report:
        report_path = f"/root/aitoolkit/telegram_ai_morning_report_{date_str}.txt"
        with open(report_path, "w") as f:
            f.write(report)
        print(f"Report saved to {report_path}", file=sys.stderr)
        print(report)
    else:
        print("ERROR: Failed to generate report via DeepSeek API", file=sys.stderr)
        print(f"\n⚠️ AI 早报生成失败（DeepSeek API 错误）\n\n今日数据：{len(ai_items)} 条 AI 相关资讯\n\n头条候选：\n" + "\n".join(f"• [{i['points']}分] {i['title']} {i.get('url','')}" for i in top[:5]))
        sys.exit(1)

if __name__ == "__main__":
    main()
