function processPunctuation() {
  var input = document.getElementById('pr-input').value;
  var output = document.getElementById('pr-output');
  var stats = document.getElementById('pr-stats');
  if (!input.trim()) { output.textContent = '⚠️ 请输入文本'; stats.textContent = ''; return; }

  var removeMode = document.getElementById('pr-remove').checked;
  var keepSpace = document.getElementById('pr-whitespace').checked;

  var punctChars = String.fromCharCode(
    0x3001, 0x3002, 0xFF0C, 0xFF01, 0xFF1F, 0xFF1A, 0xFF1B,
    0x300C, 0x300D, 0x300E, 0x300F, 0x2018, 0x2019, 0x201C, 0x201D,
    0xFF08, 0xFF09, 0x3014, 0x3015, 0x300A, 0x300B, 0x2014, 0x2026,
    0x00B7, 0xFFE0, 0x3000
  ) + ',.!?;:\'\"()[]{}<>@#$%^&*_+=|\\/`~-';

  var result = '';
  var punctCount = 0;
  var otherCount = 0;

  for (var i = 0; i < input.length; i++) {
    var ch = input[i];
    if (punctChars.indexOf(ch) >= 0) {
      punctCount++;
      if (!removeMode) {
        result += ch;
      } else if (keepSpace) {
        result += ' ';
      }
    } else {
      otherCount++;
      result += ch;
    }
  }

  if (removeMode && keepSpace) {
    result = result.replace(/ +/g, ' ').trim();
  }

  output.textContent = result;
  stats.innerHTML = '<span>🔣 标点符号: ' + punctCount + ' 个</span><span>📏 原始字符: ' + input.length + ' → 处理后: ' + result.length + '</span><span>' + (removeMode ? '🗑️ 移除模式' : '🔍 保留模式') + '</span>';
}

function clearPunctuation() {
  document.getElementById('pr-input').value = '';
  document.getElementById('pr-output').textContent = '';
  document.getElementById('pr-stats').textContent = '';
}

function copyPunctuation() {
  var text = document.getElementById('pr-output').textContent;
  if (!text || text.indexOf('⚠️') === 0) return;
  navigator.clipboard.writeText(text).then(function() {
    var btn = document.getElementById('pr-copy-btn');
    btn.textContent = '✅ 已复制';
    setTimeout(function() { btn.textContent = '📋 复制结果'; }, 2000);
  }).catch(function() {});
}
