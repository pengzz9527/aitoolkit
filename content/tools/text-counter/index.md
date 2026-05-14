---
title: "文本计数器"
description: "在线统计文字数量 — 中英文字数、字符数、行数、段落数实时统计，支持粘贴文本或直接输入"
keywords: ["文本计数器", "字数统计", "字符统计", "在线字数统计", "文字计数工具", "段落统计"]
icon: "📝"
type: "tools"
categories: ["文本处理"]
weight: 2
---

<div class="tool-widget">
  <textarea id="text-input" placeholder="在此输入或粘贴文本..." rows="10" oninput="updateStats()"></textarea>

  <div class="stats-bar" id="text-stats">
    <span>📝 字符: <strong id="char-count">0</strong></span>
    <span>🔤 字数: <strong id="word-count">0</strong></span>
    <span>📃 行数: <strong id="line-count">0</strong></span>
    <span>📄 段落: <strong id="para-count">0</strong></span>
    <span>🔢 数字: <strong id="digit-count">0</strong></span>
    <span>␣ 空格: <strong id="space-count">0</strong></span>
  </div>

  <div class="btn-row">
    <button class="btn btn-outline btn-sm" onclick="clearText()">🗑️ 清空</button>
    <button class="btn btn-outline btn-sm" onclick="trimText()">✂️ 去除首尾空格</button>
    <button class="btn btn-outline btn-sm" onclick="removeExtraSpace()">📏 合并连续空格</button>
    <button class="btn btn-outline btn-sm" onclick="removeLineBreaks()">↔️ 去除换行</button>
  </div>
</div>

<script>
function updateStats() {
  let text = document.getElementById('text-input').value;
  let len = text.length;
  let noSpace = text.replace(/\s/g, '');
  // Chinese character count (including punctuation)
  let chineseChars = (text.match(/[\u4e00-\u9fff\u3400-\u4dbf\uf900-\ufaff]/g) || []).length;
  // Word count: split by whitespace for "words", count Chinese chars individually
  let words = text.trim() ? text.trim().split(/\s+/).length : 0;
  // For Chinese text, count each Chinese character as a word
  let totalWords = words + chineseChars;
  let lines = text ? text.split('\n').length : 0;
  let paras = text ? text.split('\n\n').filter(p => p.trim()).length : 0;
  let digits = (text.match(/\d/g) || []).length;
  let spaces = (text.match(/\s/g) || []).length;
  let chinesePunc = (text.match(/[，。、；：？！""''（）【】《》——……·]/g) || []).length;

  document.getElementById('char-count').textContent = len;
  document.getElementById('word-count').textContent = totalWords || 0;
  document.getElementById('line-count').textContent = lines;
  document.getElementById('para-count').textContent = paras;
  document.getElementById('digit-count').textContent = digits;
  document.getElementById('space-count').textContent = spaces;
}

function clearText() {
  document.getElementById('text-input').value = '';
  updateStats();
}

function trimText() {
  let ta = document.getElementById('text-input');
  ta.value = ta.value.trim();
  updateStats();
}

function removeExtraSpace() {
  let ta = document.getElementById('text-input');
  ta.value = ta.value.replace(/\s+/g, ' ');
  updateStats();
}

function removeLineBreaks() {
  let ta = document.getElementById('text-input');
  ta.value = ta.value.replace(/\n/g, ' ');
  updateStats();
}
</script>

<div class="tool-meta">
  <p><strong>使用说明：</strong>直接在输入框中输入或粘贴文本，统计数据实时更新。</p>
  <p><strong>统计项包括：</strong>总字符数、中英文词数、行数、段落数、数字数量、空格数量。</p>
  <p><strong>适用场景：</strong>写作字数统计、SEO 文章长度检查、翻译工作量估算、社交媒体字数限制检查。</p>
</div>
