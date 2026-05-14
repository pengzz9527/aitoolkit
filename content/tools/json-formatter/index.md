---
title: "JSON 格式化/压缩工具"
description: "在线JSON格式化、压缩、验证工具。支持JSON解析、语法高亮、错误提示，一键格式化或压缩JSON数据"
keywords: ["JSON格式化", "JSON压缩", "JSON验证", "JSON解析", "JSON美化", "在线JSON工具"]
icon: "🔧"
type: "tools"
categories: ["开发工具"]
weight: 1
---

<div class="tool-widget">
  <textarea id="json-input" placeholder="在此粘贴 JSON 数据..." rows="8">{"name":"AI Toolkit","version":"1.0","features":["json格式化","文本计数","编码解码"],"active":true}</textarea>

  <div class="btn-row">
    <button class="btn" onclick="formatJSON()">✨ 格式化</button>
    <button class="btn btn-outline" onclick="compressJSON()">🗜️ 压缩</button>
    <button class="btn btn-outline btn-sm" onclick="validateJSON()">✅ 验证</button>
    <button class="btn btn-outline btn-sm" onclick="clearJSON()">🗑️ 清空</button>
    <button class="btn btn-outline btn-sm" id="json-copy-btn" onclick="copyJSON()">📋 复制</button>
  </div>

  <pre class="output-area" id="json-output"></pre>
  <div class="stats-bar" id="json-stats"></div>
</div>

<script>
let jsonOutput = document.getElementById('json-output');
let jsonStats = document.getElementById('json-stats');

function formatJSON() {
  let input = document.getElementById('json-input').value;
  if (!input.trim()) { jsonOutput.textContent = '⚠️ 请输入 JSON 数据'; jsonStats.textContent = ''; return; }
  try {
    let parsed = JSON.parse(input);
    jsonOutput.textContent = JSON.stringify(parsed, null, 2);
    let len = JSON.stringify(parsed).length;
    let lines = jsonOutput.textContent.split('\n').length;
    jsonStats.innerHTML = '<span>✅ 有效 JSON</span><span>📏 压缩后: ' + len + ' 字符</span><span>📃 ' + lines + ' 行</span>';
  } catch(e) {
    jsonOutput.textContent = '❌ JSON 解析错误:\n' + e.message;
    jsonStats.innerHTML = '<span style="color:#dc2626">❌ 无效 JSON</span>';
  }
}

function compressJSON() {
  let input = document.getElementById('json-input').value;
  if (!input.trim()) { jsonOutput.textContent = '⚠️ 请输入 JSON 数据'; return; }
  try {
    let parsed = JSON.parse(input);
    jsonOutput.textContent = JSON.stringify(parsed);
    jsonStats.innerHTML = '<span>✅ 已压缩</span><span>📏 ' + jsonOutput.textContent.length + ' 字符</span>';
  } catch(e) {
    jsonOutput.textContent = '❌ JSON 解析错误:\n' + e.message;
  }
}

function validateJSON() {
  let input = document.getElementById('json-input').value;
  if (!input.trim()) { jsonOutput.textContent = '⚠️ 请输入 JSON 数据'; return; }
  try {
    JSON.parse(input);
    jsonOutput.textContent = '✅ JSON 有效！';
    jsonStats.innerHTML = '<span style="color:#16a34a">✅ 语法正确</span>';
  } catch(e) {
    jsonOutput.textContent = '❌ JSON 无效:\n' + e.message;
    jsonStats.innerHTML = '<span style="color:#dc2626">❌ ' + e.message.split('(')[0].trim() + '</span>';
  }
}

function clearJSON() {
  document.getElementById('json-input').value = '';
  jsonOutput.textContent = '';
  jsonStats.textContent = '';
}

function copyJSON() {
  let text = jsonOutput.textContent;
  if (!text || text.startsWith('⚠️') || text.startsWith('❌')) return;
  navigator.clipboard.writeText(text).then(() => {
    let btn = document.getElementById('json-copy-btn');
    btn.textContent = '✅ 已复制';
    setTimeout(() => btn.textContent = '📋 复制', 2000);
  }).catch(() => {});
}

// Auto-format on load
formatJSON();
</script>

<div class="tool-meta">
  <p><strong>使用说明：</strong>粘贴 JSON 数据到输入框，点击「格式化」美化输出，点击「压缩」去除空白。</p>
  <p><strong>适用场景：</strong>API 调试、配置文件编辑、数据交换格式校验。</p>
  <p><strong>隐私说明：</strong>所有数据仅在浏览器本地处理，不会上传到任何服务器。</p>
</div>
