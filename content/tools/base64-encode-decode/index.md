---
title: "Base64 编码/解码工具"
description: "在线Base64编码解码工具 — 文本和文件的Base64转换，支持UTF-8中文编码，实时预览转换结果"
keywords: ["Base64编码", "Base64解码", "Base64在线工具", "Base64转换", "文本编码", "在线编码"]
icon: "🔐"
type: "tools"
categories: ["编码解码"]
weight: 4
---

<div class="tool-widget">
  <div style="display:flex;gap:8px;margin-bottom:12px">
    <button class="btn btn-sm" id="mode-encode" onclick="setMode('encode')">✏️ 文本 → Base64</button>
    <button class="btn btn-sm btn-outline" id="mode-decode" onclick="setMode('decode')">✏️ Base64 → 文本</button>
  </div>

  <textarea id="b64-input" placeholder="在此粘贴文本..." rows="6">Hello, AI Toolkit! 你好，AI 工具包！</textarea>

  <div class="btn-row">
    <button class="btn" onclick="convertB64()">🔄 转换</button>
    <button class="btn btn-outline btn-sm" onclick="clearB64()">🗑️ 清空</button>
    <button class="btn btn-outline btn-sm" id="b64-copy-btn" onclick="copyB64Result()">📋 复制结果</button>
    <button class="btn btn-outline btn-sm" onclick="swapB64()">↕️ 交换输入/输出</button>
  </div>

  <pre class="output-area" id="b64-output"></pre>
  <div class="stats-bar" id="b64-stats"></div>
</div>

<script>
let currentMode = 'encode';
let modeEncode = document.getElementById('mode-encode');
let modeDecode = document.getElementById('mode-decode');
let b64Input = document.getElementById('b64-input');
let b64Output = document.getElementById('b64-output');
let b64Stats = document.getElementById('b64-stats');

function setMode(mode) {
  currentMode = mode;
  if (mode === 'encode') {
    modeEncode.className = 'btn btn-sm';
    modeDecode.className = 'btn btn-sm btn-outline';
    b64Input.placeholder = '在此粘贴文本...';
  } else {
    modeEncode.className = 'btn btn-sm btn-outline';
    modeDecode.className = 'btn btn-sm';
    b64Input.placeholder = '在此粘贴 Base64 字符串...';
  }
  convertB64();
}

function convertB64() {
  let input = b64Input.value;
  if (!input.trim()) { b64Output.textContent = ''; b64Stats.textContent = ''; return; }
  try {
    if (currentMode === 'encode') {
      let encoded = btoa(unescape(encodeURIComponent(input)));
      b64Output.textContent = encoded;
      b64Stats.innerHTML = '<span>📏 原始: ' + input.length + ' 字符</span><span>📦 Base64: ' + encoded.length + ' 字符</span>';
    } else {
      let decoded = decodeURIComponent(escape(atob(input)));
      b64Output.textContent = decoded;
      b64Stats.innerHTML = '<span>📦 Base64: ' + input.length + ' 字符</span><span>📏 解码后: ' + decoded.length + ' 字符</span>';
    }
  } catch(e) {
    b64Output.textContent = '❌ 转换失败: ' + e.message + '\n\n提示：Base64 解码要求输入是有效的 Base64 字符串。';
    b64Stats.textContent = '';
  }
}

function clearB64() {
  b64Input.value = '';
  b64Output.textContent = '';
  b64Stats.textContent = '';
}

function copyB64Result() {
  let text = b64Output.textContent;
  if (!text || text.startsWith('❌')) return;
  navigator.clipboard.writeText(text).then(() => {
    let btn = document.getElementById('b64-copy-btn');
    btn.textContent = '✅ 已复制';
    setTimeout(() => btn.textContent = '📋 复制结果', 2000);
  }).catch(() => {});
}

function swapB64() {
  let output = b64Output.textContent;
  if (!output || output.startsWith('❌')) return;
  b64Input.value = output;
  convertB64();
}

// Auto-convert on load
convertB64();
</script>

<div class="tool-meta">
  <p><strong>使用说明：</strong>选择编码或解码模式，输入文本后自动转换。</p>
  <p><strong>支持中文：</strong>Base64 编码前会自动处理 UTF-8 中文编码，确保中文字符转换正确。</p>
  <p><strong>适用场景：</strong>数据传输编码、简单数据混淆、API Token 处理、图片Base64编码。</p>
</div>
