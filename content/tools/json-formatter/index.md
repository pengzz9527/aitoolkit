     1|---
     2|title: "JSON 格式化/压缩工具"
     3|description: "在线JSON格式化、压缩、验证工具。支持JSON解析、语法高亮、错误提示，一键格式化或压缩JSON数据"
     4|keywords: ["JSON格式化", "JSON压缩", "JSON验证", "JSON解析", "JSON美化", "在线JSON工具"]
     5|icon: "🔧"
     6|type: "tools"
     7|categories: ["开发工具"]
     8|weight: 1
     9|---
    10|
    11|<textarea id="json-input" placeholder="在此粘贴 JSON 数据..." rows="8">{"name":"AI Toolkit","version":"1.0","features":["json格式化","文本计数","编码解码"],"active":true}</textarea>
    12|
    13|  <div class="btn-row">
    14|    <button class="btn" onclick="formatJSON()">✨ 格式化</button>
    15|    <button class="btn btn-outline" onclick="compressJSON()">🗜️ 压缩</button>
    16|    <button class="btn btn-outline btn-sm" onclick="validateJSON()">✅ 验证</button>
    17|    <button class="btn btn-outline btn-sm" onclick="clearJSON()">🗑️ 清空</button>
    18|    <button class="btn btn-outline btn-sm" id="json-copy-btn" onclick="copyJSON()">📋 复制</button>
    19|  </div>
    20|
    21|  <pre class="output-area" id="json-output"></pre>
    22|  <div class="stats-bar" id="json-stats"></div>
    23|</div>
    24|
    25|<script>
    26|let jsonOutput = document.getElementById('json-output');
    27|let jsonStats = document.getElementById('json-stats');
    28|
    29|function formatJSON() {
    30|  let input = document.getElementById('json-input').value;
    31|  if (!input.trim()) { jsonOutput.textContent = '⚠️ 请输入 JSON 数据'; jsonStats.textContent = ''; return; }
    32|  try {
    33|    let parsed = JSON.parse(input);
    34|    jsonOutput.textContent = JSON.stringify(parsed, null, 2);
    35|    let len = JSON.stringify(parsed).length;
    36|    let lines = jsonOutput.textContent.split('\n').length;
    37|    jsonStats.innerHTML = '<span>✅ 有效 JSON</span><span>📏 压缩后: ' + len + ' 字符</span><span>📃 ' + lines + ' 行</span>';
    38|  } catch(e) {
    39|    jsonOutput.textContent = '❌ JSON 解析错误:\n' + e.message;
    40|    jsonStats.innerHTML = '<span style="color:#dc2626">❌ 无效 JSON</span>';
    41|  }
    42|}
    43|
    44|function compressJSON() {
    45|  let input = document.getElementById('json-input').value;
    46|  if (!input.trim()) { jsonOutput.textContent = '⚠️ 请输入 JSON 数据'; return; }
    47|  try {
    48|    let parsed = JSON.parse(input);
    49|    jsonOutput.textContent = JSON.stringify(parsed);
    50|    jsonStats.innerHTML = '<span>✅ 已压缩</span><span>📏 ' + jsonOutput.textContent.length + ' 字符</span>';
    51|  } catch(e) {
    52|    jsonOutput.textContent = '❌ JSON 解析错误:\n' + e.message;
    53|  }
    54|}
    55|
    56|function validateJSON() {
    57|  let input = document.getElementById('json-input').value;
    58|  if (!input.trim()) { jsonOutput.textContent = '⚠️ 请输入 JSON 数据'; return; }
    59|  try {
    60|    JSON.parse(input);
    61|    jsonOutput.textContent = '✅ JSON 有效！';
    62|    jsonStats.innerHTML = '<span style="color:#16a34a">✅ 语法正确</span>';
    63|  } catch(e) {
    64|    jsonOutput.textContent = '❌ JSON 无效:\n' + e.message;
    65|    jsonStats.innerHTML = '<span style="color:#dc2626">❌ ' + e.message.split('(')[0].trim() + '</span>';
    66|  }
    67|}
    68|
    69|function clearJSON() {
    70|  document.getElementById('json-input').value = '';
    71|  jsonOutput.textContent = '';
    72|  jsonStats.textContent = '';
    73|}
    74|
    75|function copyJSON() {
    76|  let text = jsonOutput.textContent;
    77|  if (!text || text.startsWith('⚠️') || text.startsWith('❌')) return;
    78|  navigator.clipboard.writeText(text).then(() => {
    79|    let btn = document.getElementById('json-copy-btn');
    80|    btn.textContent = '✅ 已复制';
    81|    setTimeout(() => btn.textContent = '📋 复制', 2000);
    82|  }).catch(() => {});
    83|}
    84|
    85|// Auto-format on load
    86|formatJSON();
    87|</script>
    88|
    89|<div class="tool-meta">
    90|  <p><strong>使用说明：</strong>粘贴 JSON 数据到输入框，点击「格式化」美化输出，点击「压缩」去除空白。</p>
    91|  <p><strong>适用场景：</strong>API 调试、配置文件编辑、数据交换格式校验。</p>
    92|  <p><strong>隐私说明：</strong>所有数据仅在浏览器本地处理，不会上传到任何服务器。</p>
    93|</div>
    94|