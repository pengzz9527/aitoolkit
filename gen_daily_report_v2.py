#!/usr/bin/env python3
"""Generate a rich daily AI report matching the established style."""
import json
import os
import re
from datetime import datetime, timezone, timedelta

BJ = timezone(timedelta(hours=8))

AI_KEYWORDS = [
    "ai","llm","gpt","openai","claude","deepseek","anthropic","gemini",
    "machine learning","neural","transformer","model","agent","robot",
    "inference","quantization","benchmark","chatbot","generative",
    "diffusion","llama","mistral","grok","xai","perplexity","cursor",
    "copilot","sora","prompt","rag","embedding","multimodal",
    "vision","reasoning","mcp","crewai","langchain","openclaw",
    "watermark","provenance","safety","alignment","rlhf","fine-tune",
    "gemma","qwen","o1","o3","agentic","automated reasoning",
    "foundation model","coding agent","reasoning model",
]

def is_ai(title, url=""):
    text = f"{title} {url}".lower()
    return any(k in text for k in AI_KEYWORDS)

def clean_title(t):
    t = re.sub(r'\s*\([^)]*HN\s*\d+\s*点赞\)\s*$', '', t)
    t = re.sub(r'\s*–.*$', '', t)
    t = re.sub(r'\s*\([^)]*\)\s*$', '', t)
    return t.strip()

def main():
    date_str = datetime.now(BJ).strftime("%Y-%m-%d")
    data_file = f"/root/aitoolkit/daily_data_{date_str}.json"
    
    if not os.path.exists(data_file):
        import glob
        files = sorted(glob.glob("/root/aitoolkit/daily_data_*.json"))
        if files:
            data_file = files[-1]
        else:
            print(f"ERROR: No data file found", flush=True)
            return
    
    with open(data_file) as f:
        data = json.load(f)
    
    full_date = data.get("full_date", date_str)
    hn_ai = data.get("hn_ai", [])
    hn_all = data.get("hn_all", [])
    gh_repos = data.get("github_trending", [])
    arxiv = data.get("arxiv", [])
    extra_hn = data.get("extra_hn", [])
    
    # ── Select: New Tools (HN AI with URLs, high points) ──
    tools = []
    for s in hn_ai:
        if s["url"] and "news.ycombinator.com" not in s["url"]:
            tools.append(s)
        if len(tools) >= 3:
            break
    # supplement from extra
    if len(tools) < 2:
        for s in extra_hn:
            if s["url"] and "news.ycombinator.com" not in s["url"]:
                tools.append(s)
            if len(tools) >= 3:
                break
    
    # ── Select: Open Source Projects (GitHub + arXiv) ──
    oss = []
    seen_repos = set()
    for r in gh_repos:
        repo = r["repo"]
        if repo in seen_repos:
            continue
        seen_repos.add(repo)
        oss.append({"type": "github", "repo": repo, "desc": r.get("description", ""), "stars": r.get("stars", "")})
        if len(oss) >= 3:
            break
    
    # If not enough GitHub repos, add arXiv papers
    if len(oss) < 2 and arxiv:
        for p in arxiv:
            title = clean_title(p["title"])
            if len(title) > 10:
                oss.append({
                    "type": "arxiv",
                    "title": title,
                    "link": p["link"],
                    "desc": p.get("description", "")[:100]
                })
            if len(oss) >= 3:
                break
    
    # ── Select: Industry Trends (high-point HN stories) ──
    trends = []
    for s in hn_all:
        if s["points"] >= 80 and s["url"] and "news.ycombinator.com" not in s["url"]:
            trends.append(s)
        if len(trends) >= 2:
            break
    
    # ── Select: Funding ──
    funding = []
    funding_kw = ["fund","seed","series","venture","startup","acquisition","ipo",
                  "raise","valuation","investment","funding","billion","million dollar"]
    for s in hn_all + extra_hn:
        text = f"{s['title']} {s.get('url','')}".lower()
        if any(k in text for k in funding_kw) and s["points"] >= 40:
            funding.append(s)
        if len(funding) >= 2:
            break
    
    # ── Build Markdown ──
    lines = []
    lines.append('---')
    lines.append(f'title: "AI 日报 | {full_date}"')
    lines.append(f'date: {date_str}T07:00:00+08:00')
    
    # Description: 8-item preview
    desc_items = []
    for s in tools[:2]:
        desc_items.append(clean_title(s["title"])[:50])
    for o in oss[:2]:
        if o["type"] == "github":
            desc_items.append(o["repo"].split("/")[1] + " 开源")
        else:
            desc_items.append(o["title"][:40])
    for s in trends[:2]:
        desc_items.append(clean_title(s["title"])[:50])
    for s in funding[:1]:
        desc_items.append(clean_title(s["title"])[:50])
    desc = "今日 AI 圈：" + "、".join(desc_items[:8])
    lines.append(f'description: "{desc}"')
    lines.append(f'type: "daily"')
    lines.append('---')
    lines.append('')
    
    # 🛠️ 新工具
    lines.append('## 🛠️ 新工具')
    lines.append('')
    for s in tools[:3]:
        title = clean_title(s["title"])
        url = s.get("url", "")
        points = s["points"]
        short = title.split(" – ")[0].split(" | ")[0].strip()
        if len(short) > 45:
            short = short[:45] + "..."
        lines.append(f'### {short}')
        lines.append('')
        if url and url != "#":
            lines.append(f'> [{title}]({url})  ·  🔥 {points} 点赞')
        else:
            lines.append(f'> {title}  ·  🔥 {points} 点赞')
        lines.append('')
    lines.append('')
    
    # 🔬 开源项目
    lines.append('## 🔬 开源项目')
    lines.append('')
    for o in oss[:3]:
        if o["type"] == "github":
            repo = o["repo"]
            repo_name = repo.split("/")[1] if "/" in repo else repo
            lines.append(f'### {repo_name}')
            lines.append('')
            lines.append(f'**[{repo}](https://github.com/{repo})*')
            if o["desc"]:
                lines.append(f'{o["desc"]}')
            if o["stars"]:
                lines.append(f'  ·  ⭐ {o["stars"]}')
        else:
            lines.append(f'### {o["title"]}')
            lines.append('')
            lines.append(f'**[arXiv:cs.AI]({o["link"]})**')
            if o["desc"]:
                lines.append(f'{o["desc"]}')
        lines.append('')
    lines.append('')
    
    # 💰 融资动态
    lines.append('## 💰 融资动态')
    lines.append('')
    if funding:
        for s in funding[:2]:
            title = clean_title(s["title"])
            url = s.get("url", "")
            points = s["points"]
            lines.append(f'### {title}')
            lines.append('')
            if url and url != "#":
                lines.append(f'> [{title}]({url})  ·  🔥 {points} 点赞')
            else:
                lines.append(f'> {title}  ·  🔥 {points} 点赞')
            lines.append('')
    else:
        lines.append('今日 AI 领域暂无重大融资消息。')
        lines.append('')
    
    # 📄 行业趋势
    lines.append('## 📄 行业趋势')
    lines.append('')
    for s in trends[:2]:
        title = clean_title(s["title"])
        url = s.get("url", "")
        points = s["points"]
        short = title.split(" – ")[0].split(" | ")[0].strip()
        if len(short) > 40:
            short = short[:40] + "..."
        lines.append(f'### {short}')
        lines.append('')
        if url and url != "#":
            lines.append(f'> [{title}]({url})  ·  🔥 {points} 点赞')
        else:
            lines.append(f'> {title}  ·  🔥 {points} 点赞')
        lines.append('')
    
    # Footer
    lines.append('---')
    lines.append('')
    lines.append('*本日报由 AI 从 Hacker News、GitHub Trending、arXiv 等信息源自动聚合筛选，仅供参考，不构成任何投资建议。*')
    lines.append('')
    
    markdown = "\n".join(lines)
    
    output_path = f"/root/aitoolkit/content/daily/{date_str}.md"
    with open(output_path, "w") as f:
        f.write(markdown)
    
    print(f"✅ Report generated: {output_path}", flush=True)
    print(f"   Tools: {len(tools[:3])}, OSS: {len(oss[:3])}, Funding: {len(funding)}, Trends: {len(trends[:2])}", flush=True)

if __name__ == "__main__":
    main()
