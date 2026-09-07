---
title: "用AI做Git提交信息自动化：零基础学会让ChatGPT帮你写Commit Message、PR描述和Release Notes（2026实战教程）"
date: 2026-09-07
description: "零基础学会用AI自动生成Git提交信息：从Commit Message到PR描述、Release Notes一键生成，告别每次手动码字的痛苦，让AI替你完成重复性的文案工作。"
tags: ["AI工具", "Git", "编程", "自动化", "ChatGPT", "教程", "开发者效率"]
categories: ["guides"]
image: /images/guides/ai-git-automation-cover.png
---

你是不是也遇到过这种场景——改了几十行代码，但在终端里 `git commit -m "fix bug"` 的时候却卡住了：这个改动到底该怎么描述？用英文还是中文？格式怎么写？

更痛苦的是，每次 PR 都要手动写描述，Release Notes 更是头疼。这些重复性的文案工作，其实完全可以交给 AI。

本篇教程将带你从零搭建一套 AI 驱动的 Git 工作流——让 ChatGPT 或 Claude 帮你自动生成 Commit Message、PR 描述和 Release Notes，全程不到 30 秒，而且比你自己写的更专业。

---

## 一、为什么 AI 写 Git 信息比你自己写更好？

先说一个反直觉的事实：**你自己写的 Commit Message，往往比你以为的要差。**

原因在于，写代码时你沉浸在技术细节里，很难跳出来说清楚这次改动的「业务价值」。而 AI 的优势在于：

- **结构化输出**：AI 知道 Conventional Commits 规范，能自动区分 feat/fix/refactor 等类型
- **多语言支持**：中文项目写中文，英文项目写英文，还能混合
- **批量处理**：一次生成整组提交的摘要，而不是每次改一行就思考一次
- **一致性**：同一项目的提交风格保持统一，不会因为当天心情而忽长忽短

---

## 二、方法一：用 AI 生成单个 Commit Message

这是最简单的用法——你只需要把改动的文件丢给 AI，它就能告诉你应该写什么提交信息。

### 步骤 1：获取本次改动的 Diff

在终端执行以下命令，把改动复制到剪贴板：

```bash
git diff --cached
# 或者查看所有未暂存的改动：
git diff
```

如果改动很多，可以只针对特定文件：

```bash
git diff -- path/to/your/file.py
```

### 步骤 2：让 AI 生成 Commit Message

把上面的 diff 粘贴到 ChatGPT（或 Claude、DeepSeek 等任何 AI 工具），然后发送如下提示词：

```
请根据以下 Git diff 生成符合 Conventional Commits 规范的提交信息。
要求：
1. 使用中文
2. 格式：type(scope): description
3. type 只能是 feat/fix/refactor/docs/chore/test/perf/build/ci/revert 之一
4. 如果有多处改动，请拆分多个 commit
5. 每个 commit 不超过 72 个字符

以下是 diff：
[粘贴你的 diff]
```

### 步骤 3：执行提交

AI 会输出类似这样的结果：

```
feat(auth): 添加 JWT Token 刷新机制

fix(api): 修复用户列表分页参数缺失导致 500 错误

refactor(db): 优化订单查询 SQL，移除 N+1 查询问题
```

直接复制执行：

```bash
git add src/auth/token.py
git commit -m "feat(auth): 添加 JWT Token 刷新机制"

git add src/api/users.py
git commit -m "fix(api): 修复用户列表分页参数缺失导致 500 错误"
```

### 进阶技巧：自定义提交风格

每个人的项目都有自己的风格。你可以让 AI「记住」你的偏好：

```
你是这个项目的提交助手。我们的项目风格是：
- 全部使用中文
- scope 使用简短的英文小写
- 不需要 body，只写一行 subject
- feat 表示新功能，fix 表示 bug 修复，chore 表示配置/工具变更

请根据以下 diff 生成符合上述风格的提交信息。

以下是 diff：
[粘贴你的 diff]
```

下次同样的项目，你可以在同一会话中继续用，AI 会自动沿用你设定的规则。

---

## 三、方法二：用 AI 自动生成 PR 描述

PR（Pull Request）描述是团队协作中最容易被忽视但最重要的文档。一个写得好 PR 描述，能让 Reviewer 节省大量时间，也能让未来的自己快速理解这段代码的上下文。

### 标准 PR 描述模板

一个好的 PR 描述通常包含以下几个部分：

| 部分 | 说明 |
|------|------|
| **类型** | feat / fix / refactor / docs 等 |
| **背景** | 为什么要改？解决了什么问题？ |
| **变更内容** | 具体改了什么？关键逻辑是什么？ |
| **测试方式** | 如何验证这个改动是正确的？ |
| **影响范围** | 有哪些地方可能受到影响？ |

### 让 AI 自动生成完整 PR 描述

把 diff 和相关的 issue 描述一起给 AI：

```
请帮我生成一个 GitHub PR 描述。

项目背景：[简单描述这个 PR 要解决什么问题，或者关联的 issue 编号]

以下是完整的 diff：
[粘贴 git diff HEAD~3 --stat 或完整 diff]

请按照以下格式输出：
## 📋 类型
- feat / fix / refactor / docs

## 📝 变更说明
[简要描述变更内容，2-3 句话]

## 🔍 背景
[这个问题为什么存在，之前是什么状态]

## ✅ 测试方法
[如何验证这个改动]

## ⚠️ 影响范围
[可能影响的功能模块]

## 📎 相关 Issue
[如果有，列出关联的 issue 号]
```

AI 会输出结构化的 PR 描述，你只需要复制到 GitHub 的 PR 表单里即可。

### 批量 PR 描述：一个 PR 包含多个提交

如果你的 PR 包含多个 commit，AI 可以帮你生成汇总描述：

```
我的 PR 包含以下 5 个 commit：
1. chore(deps): 升级依赖版本
2. fix(api): 修复登录超时问题
3. feat(auth): 添加登录重试机制
4. test(auth): 补充登录接口的单元测试
5. docs: 更新认证模块文档

请为这个 PR 生成一个简洁的描述，突出核心变更和测试覆盖情况。
```

---

## 四、方法三：用 AI 生成 Release Notes

每个版本发布前，都需要写 Release Notes。如果你经常发版，这绝对是一个重复性很高的任务。

### 从 Commit Log 生成 Release Notes

最聪明的做法是让 AI 从已有的 commit history 中提取关键变更：

```
请根据以下 Git log 生成 v2.3.0 版本的 Release Notes。

要求：
1. 按 feat / fix / refactor 分组
2. 每组用简短的句子描述，不要技术细节
3. 输出中英文两个版本
4. 重点突出对用户可见的变更

Git log：
[粘贴 git log --oneline v2.2.0..HEAD]
```

典型输出：

```
## 🆕 新增功能
- 支持 JWT Token 自动刷新
- 新增用户登录失败重试机制

## 🐛 Bug 修复
- 修复用户列表分页参数缺失导致的 500 错误
- 修复移动端页面布局错乱问题

## ⚡ 性能优化
- 优化订单查询 SQL，消除 N+1 查询
```

### 配合 AI 自动生成 CHANGELOG.md

如果你想把 Release Notes 直接写入 CHANGELOG.md，可以让 AI 格式化输出：

```
请将以下 Git log 转换为标准的 CHANGELOG 格式（Keep a Changelog 规范）：
[粘贴 git log]

格式要求：
## [版本] - 日期
### Added
### Changed
### Fixed
### Removed
```

---

## 五、方法四：用 AI 辅助 Git 问题解决

除了生成文案，AI 还能帮你解决 Git 使用中常见的棘手问题。

### 疑难场景 1：合并冲突解决

当 `git merge` 出现大量冲突时，把冲突文件的内容给 AI：

```
以下是 git merge 产生的冲突文件内容，请用「<<<<<< ORIGINAL ===== >>>>>> THEIRS」标记帮我分析：
1. 哪些冲突是合理的（两边都有意义）
2. 哪些冲突明显是多余的（可以一方胜出）
3. 给出最终的合并建议代码

以下是冲突内容：
[粘贴冲突文件]
```

### 疑难场景 2：还原误操作的提交

```
我不小心执行了 `git reset --hard`，丢失了最近 3 个 commit。
请帮我：
1. 解释 `git reflog` 的原理
2. 给出恢复这些 commit 的具体命令
3. 告诉我如何避免以后出现类似问题
```

### 疑难场景 3：复杂的分支策略

```
我有一个功能分支 feature/login，已经提交了 8 个 commit。
现在我需要把这个功能分成两个 PR：
- 第一个 PR：只包含认证逻辑（commit 1-4）
- 第二个 PR：包含 UI 部分（commit 5-8）

请告诉我如何用 git cherry-pick 或 git rebase 实现这个目标，同时保持历史清晰。
```

---

## 六、完整工作流示例：从 Commit 到 Release

下面是一个真实场景的完整流程，让你理解各个步骤如何串联：

### 场景：你开发了一个新功能和两个 bug 修复

**Step 1：查看本次改动的整体概览**

```bash
git diff --stat
```

**Step 2：生成分组 Commit Message**

把 diff 给 AI，让它生成分组后的提交信息（参考第二节的方法）。

**Step 3：执行分组提交**

```bash
# 第一组：新功能
git add src/auth/
git commit -m "feat(auth): 添加 JWT Token 刷新机制和登录重试"

# 第二组：Bug 修复
git add src/api/
git commit -m "fix(api): 修复分页参数缺失和移动端布局问题"
```

**Step 4：生成 PR 描述**

```bash
# 查看完整的改动汇总
git log origin/main..HEAD --oneline
git diff origin/main...HEAD --stat
```

把以上输出给 AI，让它生成 PR 描述（参考第三节）。

**Step 5：生成 Release Notes**

当 PR 合并后，执行：

```bash
git log v2.2.0..HEAD --oneline
```

把输出给 AI，让它生成 Release Notes（参考第四节）。

---

## 七、进阶：自动化整个 Git 文案工作流

如果你觉得手动复制粘贴还不够方便，可以用脚本 + AI 实现半自动化：

### 方案 A：配置 AI 提示词模板（推荐新手）

在 ChatGPT 或 Claude 中创建一个「自定义指令」或「系统提示」：

```
你是一个专业的 Git 提交助手。你的任务是：
1. 分析用户提供的 diff，生成符合 Conventional Commits 规范的中文提交信息
2. 生成结构化的 PR 描述（包含类型、变更说明、背景、测试方法、影响范围）
3. 从 Git log 生成 Release Notes（按 feat/fix/refactor 分组）
4. 输出格式简洁，不要冗余解释
```

这样每次开启新会话，AI 都会自动以这个身份工作，你只需要粘贴 diff 即可。

### 方案 B：用本地脚本自动化（进阶）

如果你熟悉 Python，可以写一个简单的脚本，调用 AI API 自动生成提交信息：

```python
import subprocess
import json

# 获取 diff
result = subprocess.run(
    ["git", "diff", "--cached"],
    capture_output=True, text=True
)
diff_text = result.stdout

# 调用 AI API 生成提交信息
# （这里可以用 OpenAI、DeepSeek 等任意 API）
prompt = f"""
请根据以下 diff 生成符合 Conventional Commits 规范的提交信息，只输出 commit message，不要其他解释：

{diff_text}
"""

# 发送请求获取结果...
```

这个方案适合有编程基础、想要深度定制工作流的开发者。

---

## 八、常见问题的快速解答

**Q：Commit Message 应该用中文还是英文？**
A：看团队规范。国内项目用中文没问题，但如果是开源项目或国际化团队，建议用英文。AI 可以根据你的要求输出任意语言。

**Q：AI 生成的提交信息质量可靠吗？**
A：大部分情况下很可靠，但建议至少扫一眼，确保没有漏掉重要的业务逻辑变更。AI 擅长模式识别，但对业务上下文的理解可能不如你自己。

**Q：Can I use this for my work project?**
A: Absolutely! Just make sure your team agrees on the commit message format first.

**Q：AI 生成 PR 描述会泄露代码吗？**
A：这取决于你用的 AI 工具。ChatGPT Plus、Claude Pro 等付费版承诺不存储训练数据；免费版的公开会话可能会被用于模型训练。如果是敏感项目，建议使用本地部署的模型（如 Ollama + Llama 3）或在私密会话中使用。

---

## 九、总结

用 AI 辅助 Git 文案工作，核心思路是：**把重复性的格式工作交给 AI，把业务判断留给自己。**

- Commit Message → AI 生成，人工审核
- PR 描述 → AI 起草，人工补充业务背景
- Release Notes → AI 从 log 提取，人工确认重要变更

这套工作流不需要写任何代码，也不需要配置复杂的环境。你只需要：
1. `git diff` 或 `git log`
2. 粘贴给 AI
3. 复制结果执行

一天下来，你可以节省至少 20-30 分钟在 Git 文案上的时间——这些时间可以用来做更有价值的事，比如读一篇技术文章，或者去 [duckdblab.org/zh/](https://duckdblab.org/zh/) 学学数据分析的新技能。

如果你对自己的 Git 操作还不够熟练，推荐先看看本站的 [用AI做Python编程实战](/guides/ai-python-programming-guide/) 教程，里面有完整的 Git + Python 工作流介绍。另外，本站的 [.gitignore 生成器](/tools/gitignore-generator/) 和 [Diff 检查器](/tools/diff-checker/) 也是开发者的实用工具。

---

*喜欢这篇文章？试试把下次 Git 提交的信息直接丢给 AI，感受节省下来的时间吧。*
