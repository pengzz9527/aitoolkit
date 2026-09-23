#!/usr/bin/env python3
"""Generate the daily AI report from fetched data."""
import json
import os
import re
from datetime import datetime, timezone, timedelta

BJ = timezone(timedelta(hours=8))

def main():
    date_str = datetime.now(BJ).strftime("%Y-%m-%d")
    data_file = f"/root/aitoolkit/daily_data_{date_str}.json"
    
    if not os.path.exists(data_file):
        import glob
        files = sorted(glob.glob("/root/aitoolkit/daily_data_*.json"))
        if files:
            data_file = files[-1]
        else:
            print(f"ERROR: No data file found for {date_str}", flush=True)
            return
    
    with open(data_file) as f:
        data = json.load(f)
    
    full_date = data.get("full_date", date_str)
    hn_ai = data.get("hn_ai", [])
    hn_all = data.get("hn", [])
    
    # ── Select content for each section ──
    
    # New Tools: top HN AI stories with external URLs
    tools = []
    for s in hn_ai:
        if s["url"] and not s["url"].startswith("https://news.ycombinator.com"):
            tools.append(s)
        if len(tools) >= 4:
            break
    
    # Open source projects: GitHub trending AI-related
    gh_py = data.get("github_python", [])
    gh_all = data.get("github_all", [])
    oss_projects = []
    ai_gh_keywords = ["ai","llm","gpt","model","agent","ml","machine learning",
                      "neural","transformer","inference","quantization","benchmark",
                      "chatbot","generative","diffusion","coding","cursor","rag",
                      "embedding","multimodal","vision","reasoning","mcp","llama",
                      "gemma","claude","deepseek","openai","anthropic","perplexity",
                      "agent","crewai","langchain","foundation","transformer",
                      "reinforcement","rlhf","fine-tune","distill","onnx","ort"]
    
    all_gh = gh_py + gh_all
    for r in all_gh:
        text = f"{r['repo']} {r['description']}".lower()
        if any(k in text for k in ai_gh_keywords):
            oss_projects.append(r)
        if len(oss_projects) >= 4:
            break
    
    if len(oss_projects) < 2 and all_gh:
        seen = {r["repo"] for r in oss_projects}
        for r in all_gh:
            if r["repo"] not in seen:
                oss_projects.append(r)
            if len(oss_projects) >= 4:
                break
    
    # Industry trends: high-point HN stories (including non-AI but tech-relevant)
    trends = []
    for s in hn_all:
        if s["points"] >= 100 and s["url"] and not s["url"].startswith("https://news.ycombinator.com"):
            trends.append(s)
        if len(trends) >= 3:
            break
    
    # Funding: look for funding/startup related
    funding = []
    funding_kw = ["fund","seed","series","venture","startup","acquisition","ipo",
                  "raise","valuation","investment","funding","billion","million dollar"]
    for s in hn_all:
        text = f"{s['title']} {s.get('url','')}".lower()
        if any(k in text for k in funding_kw) and s["points"] >= 50:
            funding.append(s)
        if len(funding) >= 2:
            break
    
    # ── Build markdown ──
    lines = []
    lines.append('---')
    lines.append(f'title: "AI 日报 | {full_date}"')
    lines.append(f'date: {date_str}T07:00:00+08:00')
    
    # Description: quick preview of 8 stories
    desc_items = []
    for s in hn_ai[:4]:
        t = re.sub(r'\s*\([^)]*\)\s*$', '', s["title"]).strip()
        desc_items.append(t[:55])
    for r in oss_projects[:2]:
        desc_items.append(f"{r['repo']} 开源")
    for s in trends[:2]:
        t = re.sub(r'\s*\([^)]*\)\s*$', '', s["title"]).strip()
        desc_items.append(t[:55])
    
    desc = "今日 AI 圈：" + "、".join(desc_items[:8])
    lines.append(f'description: "{desc}"')
    lines.append(f'type: "daily"')
    lines.append('---')
    lines.append('')
    
    # 🛠️ 新工具
    lines.append('## 🛠️ 新工具')
    lines.append('')
    tool_count = 0
    for s in tools[:3]:
        if tool_count >= 3:
            break
        title = s["title"]
        url = s.get("url", "")
        points = s["points"]
        title_clean = re.sub(r'\s*\([^)]*HN\s*\d+\s*点赞\)\s*$', '', title)
        title_clean = re.sub(r'\s*–.*$', '', title_clean)
        short_name = title_clean.split(" – ")[0].split(" | ")[0].strip()
        if len(short_name) > 50:
            short_name = short_name[:50] + "..."
        
        lines.append(f'### {short_name}')
        lines.append('')
        if url and url != "#":
            lines.append(f'> [{title_clean}]({url})  ·  🔥 {points} 点赞')
        else:
            lines.append(f'> {title_clean}  ·  🔥 {points} 点赞')
        lines.append('')
        tool_count += 1
    lines.append('')
    
    # 🔬 开源项目
    lines.append('## 🔬 开源项目')
    lines.append('')
    for r in oss_projects[:3]:
        repo = r["repo"]
        desc_text = r.get("description", "")
        stars = r.get("stars", "")
        repo_name = repo.split("/")[1] if "/" in repo else repo
        lines.append(f'### {repo_name}')
        lines.append('')
        lines.append(f'**[{repo}](https://github.com/{repo})*')
        if desc_text:
            lines.append(f'{desc_text}')
        if stars:
            lines.append(f'  ·  ⭐ {stars}')
        lines.append('')
    lines.append('')
    
    # 💰 融资动态
    lines.append('## 💰 融资动态')
    lines.append('')
    if funding:
        for s in funding[:2]:
            title = s["title"]
            url = s.get("url", "")
            points = s["points"]
            title_clean = re.sub(r'\s*\([^)]*\)\s*$', '', title)
            lines.append(f'### {title_clean}')
            lines.append('')
            if url and url != "#":
                lines.append(f'> [{title_clean}]({url})  ·  🔥 {points} 点赞')
            else:
                lines.append(f'> {title_clean}  ·  🔥 {points} 点赞')
            lines.append('')
    else:
        lines.append('今日 AI 领域暂无重大融资消息。')
        lines.append('')
    
    # 📄 行业趋势
    lines.append('## 📄 行业趋势')
    lines.append('')
    for s in trends[:2]:
        title = s["title"]
        url = s.get("url", "")
        points = s["points"]
        title_clean = re.sub(r'\s*\([^)]*\)\s*$', '', title)
        short = title_clean.split(" – ")[0].split(" | ")[0].strip()
        if len(short) > 40:
            short = short[:40] + "..."
        lines.append(f'### {short}')
        lines.append('')
        if url and url != "#":
            lines.append(f'> [{title_clean}]({url})  ·  🔥 {points} 点赞')
        else:
            lines.append(f'> {title_clean}  ·  🔥 {points} 点赞')
        lines.append('')
    
    # Footer
    lines.append('---')
    lines.append('')
    lines.append('*本日报由 AI 从 Hacker News、GitHub Trending 等信息源自动聚合筛选，仅供参考，不构成任何投资建议。*')
    lines.append('')
    
    markdown = "\n".join(lines)
    
    output_path = f"/root/aitoolkit/content/daily/{date_str}.md"
    with open(output_path, "w") as f:
        f.write(markdown)
    
    print(f"Report generated: {output_path}", flush=True)
    print(f"Tools: {len(tools[:3])}, OSS: {len(oss_projects[:3])}, Funding: {len(funding)}, Trends: {len(trends[:2])}", flush=True)
    print(f"\n{'='*60}", flush=True)
    print(markdown, flush=True)

if __name__ == "__main__":
    main()
