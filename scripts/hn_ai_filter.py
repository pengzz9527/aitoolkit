#!/usr/bin/env python3
import json, urllib.request, urllib.error, sys

# Fetch multiple HN stories and extract AI-relevant ones
ids_url = "https://hacker-news.firebaseio.com/v0/topstories.json"
ids_resp = urllib.request.urlopen(ids_url, timeout=15)
ids = json.loads(ids_resp.read())

ai_keywords = [
    'ai', 'llm', 'gpt', 'claude', 'gemini', 'openai', 'anthropic', 'meta',
    'machine learning', 'deep learning', 'neural', 'transformer', 'model',
    'chatgpt', 'llama', 'mistral', 'cohere', 'perplexity', 'hugging',
    'diffusion', 'stable diffusion', 'sora', 'vision', 'rag',
    'agent', 'agentic', 'foundation model', 'open source', 'ollama',
    'grok', 'xai', 'cursor', 'coding agent', 'ai coding', 'autogpt',
    'openrouter', 'fireworks', 'replicate', 'databricks',
    'langchain', 'langgraph', 'llama.cpp', 'vllm', 'sglang', 'mllm',
    'multimodal', 'reasoning', 'o1', 'o3', 'deepseek', 'qwen', 'gemma',
    'claude code', 'claude desktop', 'claude computer', 'claude sonnet',
    'claude opus', 'grok 3', 'grok 4', 'gemini 2', 'gemini 3',
    'openai o3', 'openai o4', 'sora video', 'deepresearch', 'o1 pro',
    'ai search', 'agi', 'artificial general intelligence', 'prompt',
    'fine-tune', 'fine tuning', 'rlhf', 'reinforcement learning',
    'mixture of experts', 'moe', ' MoE', 'kv cache', 'quantization',
    'inference', 'serve', 'v0', 'gpt-4o', 'gpt-4.5', 'gpt-5',
    'claude-4', 'claude 4', 'sonnet 4', 'opus 4',
    'ai news', 'ai launch', 'ai tool', 'ai product',
    'chatbot', 'conversational ai', 'llm agent', 'coding assistant'
]

stories = []
for sid in ids[:50]:
    try:
        story_url = f"https://hacker-news.firebaseio.com/v0/item/{sid}.json"
        story_resp = urllib.request.urlopen(story_url, timeout=10)
        story = json.loads(story_resp.read())
        if story.get('type') == 'story':
            stories.append(story)
    except:
        pass

# Filter for AI-related content
for s in stories:
    title_lower = s.get('title', '').lower()
    text_lower = (s.get('text', '') or '').lower()
    combined = title_lower + ' ' + text_lower
    if any(kw in combined for kw in ai_keywords):
        title = s.get('title', '')
        url = s.get('url', '') or f"https://news.ycombinator.com/item?id={s.get('id')}"
        points = s.get('points', 0)
        comments = s.get('descendants', 0)
        print(f"[{points} pts, {comments} comments] {title} | {url}")
