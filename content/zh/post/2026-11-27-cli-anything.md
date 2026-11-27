---
title: 'CLI-Anything 评测：让任何软件变成 AI Agent 的原生工具——一条命令自动生成 CLI，外加 CLI-Hub「应用商店」'
date: 2026-11-27
tags: ['cli-anything', 'HKUDS', 'AI Agent', 'CLI', 'Agent 原生', '开源工具', '自动化', 'MCP']
categories: ['AI 工具评测']
description: 'CLI-Anything（HKUDS，约 6.2 万星，Apache-2.0）把任意专业软件变成 AI Agent 可稳定调用的命令行工具：7 阶段全自动管线扫描源码生成带 --json、REPL、测试与 SKILL.md 的 CLI，CLI-Hub 一条 pip 命令浏览安装 80+ 社区 CLI，Agent 可经 meta-skill 自主发现并安装所需工具。'
---

# CLI-Anything 评测：让任何软件变成 AI Agent 的原生工具——一条命令自动生成 CLI，外加 CLI-Hub「应用商店」

**CLI-Anything** 的官方定位一句话：**「让所有软件原生支持 Agent」（Making ALL Software Agent-Native）**。它是香港大学数据智能实验室（HKUDS，LightRAG 背后的团队）2026 年 3 月开源的项目，核心思想很直白：AI Agent 推理很强、操控真实软件很弱，与其让 Agent「看截图、点像素」，不如把 GIMP、Blender、LibreOffice 这类专业软件直接变成一套**结构化、可组合、JSON 输出**的命令行接口——CLI 恰好是人类和 AI 共通的万能接口。

它 2026 年 3 月 8 日建库，8 个月冲到 **约 6.2 万星标**（2026-11-27 当日在 GitHub Trending 在榜），主仓 Apache-2.0、Python 实现。

- **GitHub 星标**：≈62,000（Trending 在榜）；5,600+ forks
- **GitHub 仓库**：https://github.com/HKUDS/CLI-Anything
- **CLI-Hub（CLI 应用商店）**：https://clianything.cc/
- **许可证**：Apache-2.0；主语言 Python（Click + pytest）
- **运行要求**：Python 3.10+；生成端需要一个前沿级 coding Agent（Claude Opus / GPT-5.x 档），成本是 token 消耗，工具本身免费
- **验证规模**：18 款专业软件实测（Blender、GIMP、Shotcut、LibreOffice、OBS、Krita、MuseScore、Draw.io、Zoom 等），2,280+ 项测试通过

---

## 核心功能

### 1. 7 阶段全自动管线：把任意软件「编译」成 Agent 原生 CLI

把软件路径或仓库地址扔给 `/cli-anything` 命令，一条指令跑完 7 个阶段：

| 阶段 | 干什么 |
|---|---|
| 1. 分析 Analyze | 扫描源码结构，把 GUI 操作映射到底层 API |
| 2. 设计 Design | 设计命令组、状态模型、输出格式（REPL + 子命令双模） |
| 3. 实现 Implement | 生成 Click CLI，含 `--json` 输出、undo/redo 会话管理 |
| 4. 规划测试 Plan | 产出 TEST.md，列单元 + E2E 测试计划 |
| 5. 写测试 Test | 实现完整测试套件（合成数据单测 + 真实软件 E2E） |
| 6. 文档 Document | 回写 TEST.md 结果，并生成 `SKILL.md` 供 Agent 技能发现 |
| 7. 发布 Publish | 打 setup.py，`pip install -e .` 直接上 PATH |

关键原则是**「面向软件建接口，而不是重造软件」**：生成的 CLI 产出合法的项目文件（MLT XML、ODF、SVG、bpy 脚本），渲染/导出全部委托给真实应用（`libreoffice --headless`、`blender --background`、`melt`、`sox`），零功能阉割、零玩具实现；后端缺失时测试直接失败而非跳过。

### 2. CLI-Hub：CLI 界的「pip + npm 应用商店」

```bash
pip install cli-anything-hub
cli-hub list                    # 浏览注册表
cli-hub search image            # 关键词搜索
cli-hub info gimp               # 查看某个 CLI
cli-hub install gimp            # 一条命令安装（底层装 cli-anything-gimp 包）
cli-hub launch gimp --help      # 直接运行
```

注册表当前登记 **65 个自建/社区 harness（29 类）+ 18 个公共第三方 CLI（11 类）**，覆盖创意（图像、3D、视频、音频、乐谱）、生产力（Office、知识管理、直播）、AI 平台（本地 LLM、图像生成）、通信、开发五大类。`registry.json` 一变，Hub 即时更新——你提 PR 加一个软件，当天全社区可用。

### 3. Agent 原生设计：`--help` 即自描述，`--json` 即机器可读

每个生成的 CLI 都内置三件套：**每条命令支持 `--json`**（结构化输出供 Agent 消费，人读则出表格）；**Agent 通过标准 `--help` 和 `which` 发现全部能力**，无需额外解析层；**双交互模式**——裸跑命令进入有状态 REPL（Agent 会话），子命令模式用于脚本和流水线。每个 CLI 还自带一份 `SKILL.md`（YAML frontmatter + 命令组 + 示例 + Agent 专属指导），直接可被 Claude Code、Cursor、OpenClaw、nanobot、Gemini CLI 等框架消费。

### 4. meta-skill：让 Agent 自主发现并安装所需 CLI

装上元技能后，你只需对 Agent 说「在 CLI-Hub 里找合适的工具完成这个任务」，Agent 会自己浏览目录、挑选并安装匹配的 CLI、读它的 SKILL.md 再动手——全程无需人工干预：

```bash
npx skills add HKUDS/CLI-Anything --skill cli-hub-meta-skill -g -y
```

### 5. 三大使用场景：接管工作流 / 统一散装 API / 替代 GUI Agent

- **让 Agent 接管你的工作流**：把代码库扔给 `/cli-anything`，GIMP/Blender/Shotcut 搞创作，LibreOffice/OBS 干日常，立刻得到一套 Agent 可直接调用的完整 CLI；
- **把散装 API 统一成一个 CLI**：把 API 文档或 SDK 手册喂给 `/cli-anything`，得到一个**有状态、功能完整**的 CLI，把几十个裸 API 调用整合成逻辑清晰的命令组——能力更强、token 更省；
- **替代或增强 GUI Agent**：彻底告别截图与像素点击；对 GUI 软件跑过 `/cli-anything` 后，还能纯代码合成 Agent 任务、评估器与 Benchmark，迭代效率远高于「点-截-判」循环。

---

## 适用人群

- **Coding Agent 重度用户**（Claude Code / Cursor / Codex 用户）：把团队在用的专业软件变成 Agent 可控资产，批量任务（导入导出、格式转换、渲染）直接自动化；
- **Agent 开发者**：需要稳定、确定性工具接口的团队，CLI + JSON 比 GUI 自动化可靠得多，且天然可测试、可审计、可复现；
- **工作流自动化工程师**：把「人点按钮」的环节换成「Agent 跑命令」，尤其适合创意生产、办公文档、音视频管线；
- **软件作者/社区**：给你的开源软件贡献一个 harness 提 PR 进 CLI-Hub，等于给全社区 Agent 装了官方「遥控」；
- 不适用的：**目标软件既无源码也无文档的闭源产品**（现阶段不支持）、**不想装 Python 环境的纯 Node/Go 栈团队**（harness 包都是 Python）。

---

## 与同类工具对比

| 方案 | 脆弱点 | CLI-Anything 的差异 |
|---|---|---|
| **GUI/Computer-Use Agent**（截图 + 点击） | 像素级操作随 UI 改版即失效，时序依赖重 | 纯结构化命令，确定性执行，无截图无点击，可测试可复现 |
| **RPA / Playwright 浏览器自动化** | 只能覆盖浏览器，依赖 DOM 稳定 | 面向任意桌面软件与后端，headless 运行，无需显示器 |
| **MCP Server** | 通常暴露有限工具面，要逐个写 | 一次包装整个软件的功能面；生成的 CLI 还能反过来被 MCP 生态当工具调用 |
| **手写 API 封装 / 重新实现** | 重新实现砍掉 90% 功能，维护双份代码 | 直接委托真实软件渲染导出，零能力损失，单一数据源 |
| **软件自带 CLI** | 大量专业软件根本没有 CLI | 7 阶段管线自动补齐，测试与 SKILL.md 一并生成 |

一句话定位：MCP 解决「Agent 怎么调工具」，GUI Agent 解决「Agent 怎么操作界面」，CLI-Anything 解决的是「**没有界面的软件，Agent 也能全功能用上**」——它把交互范式从模仿人类感知，拉回到 Agent 的强项：结构化数据与程序化控制。

---

## 如何使用

### 第一步：装消费端 CLI-Hub（立即可用）

```bash
pip install cli-anything-hub
cli-hub search blender
cli-hub install blender
cli-anything-blender --help        # Agent 与人都能自发现
cli-anything-blender --json render # 机器可读输出
```

注意：目标真实软件（Blender/GIMP/LibreOffice…）必须已安装，CLI 只是结构化接口，渲染仍由它完成。

### 第二步：装生成端插件，给新软件造 CLI

以 Claude Code 为例：添加 `HKUDS/CLI-Anything` 插件市场 → 安装 CLI-Anything 插件，然后：

```text
/cli-anything ./gimp          # 7 阶段全自动，产出可安装的 cli-anything-gimp
```

产物在 `agent-harness/` 下，`cd agent-harness && pip install -e .` 后：

```bash
which cli-anything-gimp       # 已在 PATH
cli-anything-gimp            # 裸跑进 REPL
cli-anything-gimp --json export --format png
```

### 第三步：迭代与校验

```text
/cli-anything:refine ./gimp "我需要更多图像批处理和滤镜相关的 CLI"   # 差距分析定向扩面
/cli-anything:test ./gimp      # 跑测试回写 TEST.md
/cli-anything:validate ./gimp  # 对照 HARNESS.md 标准校验
```

### 第四步：让 Agent 自主逛 CLI-Hub

```bash
npx skills add HKUDS/CLI-Anything --skill cli-hub-meta-skill -g -y
```

之后直接对 Agent 下任务（如「在 CLI-Hub 找合适工具，把这个播客剪成 10 条竖屏短视频」），Agent 会自主浏览目录、按能力挑选安装（支持 `--capability` 只装任务所需、`--dry-run` 预览）、读 SKILL.md 并执行。

### 第五步（进阶）：把散装 API 整合成一个 CLI

把一个 Web 服务的 API 文档 / SDK 手册目录喂给 `/cli-anything`，得到有状态命令组 + JSON 输出 + 测试的完整 CLI——一个工具顶几十个裸端点调用，省 token 且可组合。

---

## 总结

CLI-Anything 回答的问题是：**Agent 时代，几万个为人设计的软件，凭什么不能直接被 AI 操控？** 它的方案是「7 阶段全自动生成 + 真实软件硬依赖 + JSON/REPL/SKILL.md 三件套 + CLI-Hub 注册表 + meta-skill 自主发现」，把「软件接入 Agent」从一个个性工程变成了一条流水线。8 个月 6 万星、18 款专业软件实测、2,280+ 测试通过，Apache-2.0 可商用，目前是这个赛道最完整的开源方案。对 coding agent 用户，装一次 CLI-Hub 就能让 Agent 直接调起你本机的 Blender/GIMP/LibreOffice；对 Agent 开发者，它给出的确定性 CLI 接口比 GUI 自动化高一个可靠性等级。

**扣分点：**

- **生成吃前沿模型**：7 阶段管线要烧 token，弱模型生成质量断崖，成本取决于你用的 Agent；
- **硬依赖真实软件**：后端没装测试直接失败（这是设计原则，但对「只想跑 CLI 不想装 GIMP」的场景不友好）；
- **Python 打包**：harness 全是 Click 包，Node/Go 项目要额外带 Python 环境；
- **E2E 覆盖不均**：部分 harness（如 Zoom、NotebookLM）缺真实后端测试；
- **闭源无文档软件暂不在射程内**：路线图里，但现阶段「无源码、无文档」接不了。

**推荐指数：⭐⭐⭐⭐☆（4/5）**

- **Claude Code / Cursor 用户** → 装 CLI-Hub + meta-skill，专业软件自动化直接开跑；
- **Agent 开发者** → 把 CLI 生成器接入你的 Agent 框架，用确定性接口替代 GUI 自动化；
- **开源软件作者** → 给项目贡献 harness 提 PR，进 CLI-Hub 享全社区分发；
- **纯 GUI 爱好者 / 不想装 Python** → 暂不需要，继续用鼠标。
