---
title: "URL 编码/解码工具"
description: "在线URL编码解码工具 — 对URL中的特殊字符进行编码转换，支持中文URL编码解码、Query String处理"
keywords: ["URL编码", "URL解码", "URL转码", "在线URL编码", "中文URL编码", "百分号编码", "Query String"]
icon: "🔗"
type: "tools"
categories: ["编码解码"]
weight: 3
---

<div class="tool-widget">
  <textarea id="url-input" placeholder="输入需要编码或解码的文本..." rows="6">https://example.com/search?q=AI工具&lang=中文</textarea>

  <div class="btn-row">
    <button class="btn" onclick="encodeURL()">🔐 Encode（编码）</button>
    <button class="btn btn-outline" onclick="decodeURL()">🔓 Decode（解码）</button>
    <button class="btn btn-outline btn-sm" onclick="clearURL()">🗑️ 清空</button>
    <button class="btn btn-outline btn-sm" id="url-copy-btn" onclick="copyURLResult()">📋 复制结果</button>
  </div>

  <pre class="output-area" id="url-output"></pre>
</div>

<script>
function encodeURL() {
  let input = document.getElementById('url-input').value;
  if (!input.trim()) { document.getElementById('url-output').textContent = '⚠️ 请输入文本'; return; }
  try {
    document.getElementById('url-output').textContent = encodeURIComponent(input);
  } catch(e) {
    document.getElementById('url-output').textContent = '❌ 编码失败: ' + e.message;
  }
}

function decodeURL() {
  let input = document.getElementById('url-input').value;
  if (!input.trim()) { document.getElementById('url-output').textContent = '⚠️ 请输入文本'; return; }
  try {
    document.getElementById('url-output').textContent = decodeURIComponent(input);
  } catch(e) {
    document.getElementById('url-output').textContent = '❌ 解码失败: ' + e.message + '\n\n提示：如果包含 % 但不是有效的 URL 编码，请检查输入内容。';
  }
}

function clearURL() {
  document.getElementById('url-input').value = '';
  document.getElementById('url-output').textContent = '';
}

function copyURLResult() {
  let text = document.getElementById('url-output').textContent;
  if (!text || text.startsWith('⚠️') || text.startsWith('❌')) return;
  navigator.clipboard.writeText(text).then(() => {
    let btn = document.getElementById('url-copy-btn');
    btn.textContent = '✅ 已复制';
    setTimeout(() => btn.textContent = '📋 复制结果', 2000);
  }).catch(() => {});
}
</script>

<div class="tool-meta">
  <p><strong>使用说明：</strong>输入需要编码或解码的文本，点击对应按钮即可转换。</p>
  <p><strong>URL编码</strong>（百分比编码）将非ASCII字符和特殊字符转换为 % 后跟两位十六进制数的格式。</p>
  <p><strong>适用场景：</strong>API 请求参数处理、中文 URL 转换、爬虫开发、Query String 解析。</p>
</div>
