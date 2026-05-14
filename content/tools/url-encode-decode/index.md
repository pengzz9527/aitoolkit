     1|---
     2|title: "URL 编码/解码工具"
     3|description: "在线URL编码解码工具 — 对URL中的特殊字符进行编码转换，支持中文URL编码解码、Query String处理"
     4|keywords: ["URL编码", "URL解码", "URL转码", "在线URL编码", "中文URL编码", "百分号编码", "Query String"]
     5|icon: "🔗"
     6|type: "tools"
     7|categories: ["编码解码"]
     8|weight: 3
     9|---
    10|
    11|  12|  <textarea id="url-input" placeholder="输入需要编码或解码的文本..." rows="6">https://example.com/search?q=AI工具&lang=中文</textarea>
    13|
    14|  <div class="btn-row">
    15|    <button class="btn" onclick="encodeURL()">🔐 Encode（编码）</button>
    16|    <button class="btn btn-outline" onclick="decodeURL()">🔓 Decode（解码）</button>
    17|    <button class="btn btn-outline btn-sm" onclick="clearURL()">🗑️ 清空</button>
    18|    <button class="btn btn-outline btn-sm" id="url-copy-btn" onclick="copyURLResult()">📋 复制结果</button>
    19|  </div>
    20|
    21|  <pre class="output-area" id="url-output"></pre>
    22|</div>
    23|
    24|<script>
    25|function encodeURL() {
    26|  let input = document.getElementById('url-input').value;
    27|  if (!input.trim()) { document.getElementById('url-output').textContent = '⚠️ 请输入文本'; return; }
    28|  try {
    29|    document.getElementById('url-output').textContent = encodeURIComponent(input);
    30|  } catch(e) {
    31|    document.getElementById('url-output').textContent = '❌ 编码失败: ' + e.message;
    32|  }
    33|}
    34|
    35|function decodeURL() {
    36|  let input = document.getElementById('url-input').value;
    37|  if (!input.trim()) { document.getElementById('url-output').textContent = '⚠️ 请输入文本'; return; }
    38|  try {
    39|    document.getElementById('url-output').textContent = decodeURIComponent(input);
    40|  } catch(e) {
    41|    document.getElementById('url-output').textContent = '❌ 解码失败: ' + e.message + '\n\n提示：如果包含 % 但不是有效的 URL 编码，请检查输入内容。';
    42|  }
    43|}
    44|
    45|function clearURL() {
    46|  document.getElementById('url-input').value = '';
    47|  document.getElementById('url-output').textContent = '';
    48|}
    49|
    50|function copyURLResult() {
    51|  let text = document.getElementById('url-output').textContent;
    52|  if (!text || text.startsWith('⚠️') || text.startsWith('❌')) return;
    53|  navigator.clipboard.writeText(text).then(() => {
    54|    let btn = document.getElementById('url-copy-btn');
    55|    btn.textContent = '✅ 已复制';
    56|    setTimeout(() => btn.textContent = '📋 复制结果', 2000);
    57|  }).catch(() => {});
    58|}
    59|</script>
    60|
    61|<div class="tool-meta">
    62|  <p><strong>使用说明：</strong>输入需要编码或解码的文本，点击对应按钮即可转换。</p>
    63|  <p><strong>URL编码</strong>（百分比编码）将非ASCII字符和特殊字符转换为 % 后跟两位十六进制数的格式。</p>
    64|  <p><strong>适用场景：</strong>API 请求参数处理、中文 URL 转换、爬虫开发、Query String 解析。</p>
    65|</div>
    66|