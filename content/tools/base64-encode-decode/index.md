     1|---
     2|title: "Base64 编码/解码工具"
     3|description: "在线Base64编码解码工具 — 文本和文件的Base64转换，支持UTF-8中文编码，实时预览转换结果"
     4|keywords: ["Base64编码", "Base64解码", "Base64在线工具", "Base64转换", "文本编码", "在线编码"]
     5|icon: "🔐"
     6|type: "tools"
     7|categories: ["编码解码"]
     8|weight: 4
     9|---
    10|
    11|  12|  <div style="display:flex;gap:8px;margin-bottom:12px">
    13|    <button class="btn btn-sm" id="mode-encode" onclick="setMode('encode')">✏️ 文本 → Base64</button>
    14|    <button class="btn btn-sm btn-outline" id="mode-decode" onclick="setMode('decode')">✏️ Base64 → 文本</button>
    15|  </div>
    16|
    17|  <textarea id="b64-input" placeholder="在此粘贴文本..." rows="6">Hello, AI Toolkit! 你好，AI 工具包！</textarea>
    18|
    19|  <div class="btn-row">
    20|    <button class="btn" onclick="convertB64()">🔄 转换</button>
    21|    <button class="btn btn-outline btn-sm" onclick="clearB64()">🗑️ 清空</button>
    22|    <button class="btn btn-outline btn-sm" id="b64-copy-btn" onclick="copyB64Result()">📋 复制结果</button>
    23|    <button class="btn btn-outline btn-sm" onclick="swapB64()">↕️ 交换输入/输出</button>
    24|  </div>
    25|
    26|  <pre class="output-area" id="b64-output"></pre>
    27|  <div class="stats-bar" id="b64-stats"></div>
    28|</div>
    29|
    30|<script>
    31|let currentMode = 'encode';
    32|let modeEncode = document.getElementById('mode-encode');
    33|let modeDecode = document.getElementById('mode-decode');
    34|let b64Input = document.getElementById('b64-input');
    35|let b64Output = document.getElementById('b64-output');
    36|let b64Stats = document.getElementById('b64-stats');
    37|
    38|function setMode(mode) {
    39|  currentMode = mode;
    40|  if (mode === 'encode') {
    41|    modeEncode.className = 'btn btn-sm';
    42|    modeDecode.className = 'btn btn-sm btn-outline';
    43|    b64Input.placeholder = '在此粘贴文本...';
    44|  } else {
    45|    modeEncode.className = 'btn btn-sm btn-outline';
    46|    modeDecode.className = 'btn btn-sm';
    47|    b64Input.placeholder = '在此粘贴 Base64 字符串...';
    48|  }
    49|  convertB64();
    50|}
    51|
    52|function convertB64() {
    53|  let input = b64Input.value;
    54|  if (!input.trim()) { b64Output.textContent = ''; b64Stats.textContent = ''; return; }
    55|  try {
    56|    if (currentMode === 'encode') {
    57|      let encoded = btoa(unescape(encodeURIComponent(input)));
    58|      b64Output.textContent = encoded;
    59|      b64Stats.innerHTML = '<span>📏 原始: ' + input.length + ' 字符</span><span>📦 Base64: ' + encoded.length + ' 字符</span>';
    60|    } else {
    61|      let decoded = decodeURIComponent(escape(atob(input)));
    62|      b64Output.textContent = decoded;
    63|      b64Stats.innerHTML = '<span>📦 Base64: ' + input.length + ' 字符</span><span>📏 解码后: ' + decoded.length + ' 字符</span>';
    64|    }
    65|  } catch(e) {
    66|    b64Output.textContent = '❌ 转换失败: ' + e.message + '\n\n提示：Base64 解码要求输入是有效的 Base64 字符串。';
    67|    b64Stats.textContent = '';
    68|  }
    69|}
    70|
    71|function clearB64() {
    72|  b64Input.value = '';
    73|  b64Output.textContent = '';
    74|  b64Stats.textContent = '';
    75|}
    76|
    77|function copyB64Result() {
    78|  let text = b64Output.textContent;
    79|  if (!text || text.startsWith('❌')) return;
    80|  navigator.clipboard.writeText(text).then(() => {
    81|    let btn = document.getElementById('b64-copy-btn');
    82|    btn.textContent = '✅ 已复制';
    83|    setTimeout(() => btn.textContent = '📋 复制结果', 2000);
    84|  }).catch(() => {});
    85|}
    86|
    87|function swapB64() {
    88|  let output = b64Output.textContent;
    89|  if (!output || output.startsWith('❌')) return;
    90|  b64Input.value = output;
    91|  convertB64();
    92|}
    93|
    94|// Auto-convert on load
    95|convertB64();
    96|</script>
    97|
    98|<div class="tool-meta">
    99|  <p><strong>使用说明：</strong>选择编码或解码模式，输入文本后自动转换。</p>
   100|  <p><strong>支持中文：</strong>Base64 编码前会自动处理 UTF-8 中文编码，确保中文字符转换正确。</p>
   101|  <p><strong>适用场景：</strong>数据传输编码、简单数据混淆、API Token 处理、图片Base64编码。</p>
   102|</div>
   103|