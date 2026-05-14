     1|---
     2|title: "文本计数器"
     3|description: "在线统计文字数量 — 中英文字数、字符数、行数、段落数实时统计，支持粘贴文本或直接输入"
     4|keywords: ["文本计数器", "字数统计", "字符统计", "在线字数统计", "文字计数工具", "段落统计"]
     5|icon: "📝"
     6|type: "tools"
     7|categories: ["文本处理"]
     8|weight: 2
     9|---
    10|
    11|  12|  <textarea id="text-input" placeholder="在此输入或粘贴文本..." rows="10" oninput="updateStats()"></textarea>
    13|
    14|  <div class="stats-bar" id="text-stats">
    15|    <span>📝 字符: <strong id="char-count">0</strong></span>
    16|    <span>🔤 字数: <strong id="word-count">0</strong></span>
    17|    <span>📃 行数: <strong id="line-count">0</strong></span>
    18|    <span>📄 段落: <strong id="para-count">0</strong></span>
    19|    <span>🔢 数字: <strong id="digit-count">0</strong></span>
    20|    <span>␣ 空格: <strong id="space-count">0</strong></span>
    21|  </div>
    22|
    23|  <div class="btn-row">
    24|    <button class="btn btn-outline btn-sm" onclick="clearText()">🗑️ 清空</button>
    25|    <button class="btn btn-outline btn-sm" onclick="trimText()">✂️ 去除首尾空格</button>
    26|    <button class="btn btn-outline btn-sm" onclick="removeExtraSpace()">📏 合并连续空格</button>
    27|    <button class="btn btn-outline btn-sm" onclick="removeLineBreaks()">↔️ 去除换行</button>
    28|  </div>
    29|</div>
    30|
    31|<script>
    32|function updateStats() {
    33|  let text = document.getElementById('text-input').value;
    34|  let len = text.length;
    35|  let noSpace = text.replace(/\s/g, '');
    36|  // Chinese character count (including punctuation)
    37|  let chineseChars = (text.match(/[\u4e00-\u9fff\u3400-\u4dbf\uf900-\ufaff]/g) || []).length;
    38|  // Word count: split by whitespace for "words", count Chinese chars individually
    39|  let words = text.trim() ? text.trim().split(/\s+/).length : 0;
    40|  // For Chinese text, count each Chinese character as a word
    41|  let totalWords = words + chineseChars;
    42|  let lines = text ? text.split('\n').length : 0;
    43|  let paras = text ? text.split('\n\n').filter(p => p.trim()).length : 0;
    44|  let digits = (text.match(/\d/g) || []).length;
    45|  let spaces = (text.match(/\s/g) || []).length;
    46|  let chinesePunc = (text.match(/[，。、；：？！""''（）【】《》——……·]/g) || []).length;
    47|
    48|  document.getElementById('char-count').textContent = len;
    49|  document.getElementById('word-count').textContent = totalWords || 0;
    50|  document.getElementById('line-count').textContent = lines;
    51|  document.getElementById('para-count').textContent = paras;
    52|  document.getElementById('digit-count').textContent = digits;
    53|  document.getElementById('space-count').textContent = spaces;
    54|}
    55|
    56|function clearText() {
    57|  document.getElementById('text-input').value = '';
    58|  updateStats();
    59|}
    60|
    61|function trimText() {
    62|  let ta = document.getElementById('text-input');
    63|  ta.value = ta.value.trim();
    64|  updateStats();
    65|}
    66|
    67|function removeExtraSpace() {
    68|  let ta = document.getElementById('text-input');
    69|  ta.value = ta.value.replace(/\s+/g, ' ');
    70|  updateStats();
    71|}
    72|
    73|function removeLineBreaks() {
    74|  let ta = document.getElementById('text-input');
    75|  ta.value = ta.value.replace(/\n/g, ' ');
    76|  updateStats();
    77|}
    78|</script>
    79|
    80|<div class="tool-meta">
    81|  <p><strong>使用说明：</strong>直接在输入框中输入或粘贴文本，统计数据实时更新。</p>
    82|  <p><strong>统计项包括：</strong>总字符数、中英文词数、行数、段落数、数字数量、空格数量。</p>
    83|  <p><strong>适用场景：</strong>写作字数统计、SEO 文章长度检查、翻译工作量估算、社交媒体字数限制检查。</p>
    84|</div>
    85|