---
title: 'ffmpeg-skill 评测：给 Coding Agent 装一台「本地视频剪辑机」——42 个 FFmpeg 工具，无云无 API Key'
date: 2026-11-21
tags: ['ffmpeg-skill', 'FFmpeg', 'AI Agent', 'MCP', 'Agent Skill', 'Claude Code', '视频剪辑', '开源工具', 'MCP 服务器']
categories: ['AI 工具评测']
description: 'ffmpeg-skill 是一个开源 Agent Skill（约 9000 星）：给 Claude Code、Cursor、Codex 装上一套 42 个 FFmpeg 工具 + 机器可读契约 + MCP 服务器，裁剪、静音去除、字幕、响度、平台导出全在本机跑，无云、无 API Key，输出自动验证。一句话「把 1 小时访谈剪成 60 秒 Reels」即可执行。'
---

# ffmpeg-skill 评测：给 Coding Agent 装一台「本地视频剪辑机」——42 个 FFmpeg 工具，无云无 API Key

**ffmpeg-skill** 是一个开源的 **Agent Skill**，一句话定位：**让编程 Agent 拥有一台确定性、可验证的本地视频剪辑机**。它把 FFmpeg / FFprobe 封装成 **42 个类型化脚本工具**（裁剪、拼接、静音去除、画幅适配、字幕与卡拉OK、图形叠加、HDR 转 SDR、响度、多机位、交付检查、项目级渲染、批量目录），配一份**机器可读契约（SPEC）**和一个 **MCP 服务器**。Agent 不再手写 ffmpeg 命令、不再凭感觉猜帧率和编码，而是按「探测 → 无损编辑 → 检查 → 验证」的固定流程干活——全程本机，**无云、无 API Key、无 Python 第三方依赖**。

它 2026 年 6 月创建，五个月冲到 **约 9000 星标**（本周 GitHub Trending 在榜，周增 3,268），当前 v4.0.0。在「Agent 调视频工具」这个细分里，它是目前工程完成度最高的项目之一：契约、CI、MCP 三套文档字节级对齐，缺一个组件就拒绝执行而不是猜。

- **GitHub 星标**：8,966（Trending 在榜，本周 +3,268）
- **GitHub 仓库**：https://github.com/kajisho5/ffmpeg-skill
- **MCP 注册表**：io.github.kajisho5/ffmpeg-skill（https://registry.modelcontextprotocol.io）
- **技术栈**：Python 3.10+ 纯标准库 + FFmpeg 6.1+；Node 16+ 仅用于 npx 安装器
- **运行要求**：FFmpeg 6.1+（含 libx264、aac、libass 等滤镜；`doctor` 自动体检），macOS / Linux / Windows
- **最新版本**：v4.0.0（2026-11），支持 Claude Code / Cursor / Codex 插件、Gemini CLI 扩展、MCP 服务器

---

## 核心功能

### 1. 42 个类型化工具，替代手写 ffmpeg 命令

所有操作都是带类型参数的 Python 脚本，不经过 shell、不接受自由拼接的 filter graph。工具分六组：

| 组 | 工具（核心 12 个加粗） | 干什么 |
|---|---|---|
| 分析与检视 | **probe**、**look**、scenes | 测时长/帧率/画幅/HDR/音轨；拼联系表 PNG 给 Agent「看」结果；场景切换与高光建议 |
| 剪辑（24 个） | **cut**、**fit**、**silence**、join、crop、stabilize、reverse、pad、broll… | 裁段、画幅/时长适配、静音删除、拼接转场、稳定、遮幅等 |
| 音频 | **audio**、**loudness**、sync | 音频清理、响度归一（-14 LUFS 等）、多轨漂移对齐 |
| 画面 | **caption**、**graphics**、overlay、color | 烧录 SRT/ASS 字幕（逐词卡拉OK、平台安全区自动避让）、片头/角标/贴纸图形、叠加 |
| 交付 | **export**、**check**、proxy、report | 平台预设导出、按目标规格逐项验收 |
| 编排 | **render**、batch、multicam、verify | project.json 整片渲染、目录批量、多机位音轨对齐剪辑 |

关键设计：**能无损就不重编码**（`cut`/`loudness` 默认流拷贝），需要重编码时 Agent 才付编码代价；`--dry-run` 只打印命令不落盘，`--plan` 存成带输入指纹的计划文件，输入变了直接拒绝执行。

### 2. SPEC：机器可读契约，Agent 不靠猜

作者把这套模式叫 **SPEC（Self-Producing Execution Contract）**：每个工具的 `input_schema` **不是手写文档，而是运行时从脚本自己的 argparse 解析器直接生成**——加一个 flag，契约、MCP 工具表、文档自动同步，CI 里有漂移直接挂。契约写明每个工具吃什么、写什么、需要哪些 FFmpeg 组件、结果用哪个工具验证、是否要视觉检查（`mutates_input` 恒为 false）。

MCP 服务器同样没有自己的工具表：`tools/list` 启动时从契约翻译，默认只暴露核心 12 个省上下文，`FFMPEG_SKILL_MCP_FULL=1` 可列出全部 42 个；另外提供 5 条预制工作流（`reel` / `podcast` / `multicam` / `delivery_check` / `hdr`），Agent 按名字取整条命令序列，不用自己拼。

### 3. 探测先行 + 执行后验证，结果自己「看」

每个任务先跑 `probe.py`（含 VFR 变帧率检测、Dolby Vision、色彩标签、全部音轨），Agent 基于**测量值**而不是文件名做决策。画面类操作执行后自动 `look.py` 出联系表 PNG，多模态 Agent 直接看图确认；音频任务则明确标注「无需看图」。报告里必须写明检查过的图片路径，「做完不打开结果」这种事从流程上杜绝。

### 4. 平台模板：一条命令出 TikTok/Reels 规格成品

`render.py talk.mp4 --template tiktok --cues cues.txt` 自动填好整套模板：9:16 裁切、字幕逐词弹出且**避开 TikTok 描述栏与点赞列的安全区**、-14 LUFS 响度、平台导出预设，最后对成品跑 `check.py --platform tiktok` 逐项验收。Reels 等其他平台同理，`--template all` 一次出全社交平台套装。

### 5. 全本地零上传，转写引擎可选装

默认不碰网络：不传云端、不要 API Key、Python 零第三方依赖。字幕烧录可直接喂已有 SRT/ASS；需要语音转文字时选装本地 ASR（`pip install faster-whisper` 最简单，Parakeet / whisper.cpp 亦可），**音频不出本机**。没有转写引擎时 `--transcribe` 会直接拒绝并打印安装命令，而不是默认按英语猜。

---

## 适用人群

- **用 Claude Code / Cursor / Codex 做视频内容的人**：播客主、开发者做教程、访谈/直播回放转多平台切片——一句话描述需求，Agent 自动编排 probe→cut→fit→caption→export→check 全链路；
- **内容自动化 / 批量分发管线**：`batch.py` 对目录按内容哈希缓存批量处理，`--watch` 模式持续监听新文件，接 CI 或定时任务；
- **隐私敏感场景**：企业内训、涉密素材、本地合规要求——全程本机，音频视频零上传；
- **MCP / Agent 工具开发者**：SPEC「契约从代码生成、CI 防漂移」的架构本身就是很好的范本，`contract --json` 可直接被上层 Agent 系统消费。

**不太适合：**

- **非开发者**：需要 Node + FFmpeg + npx 命令行环境，且收益要接给 Agent 用才完整；
- **专业非线性剪辑（PR / DaVinci / FCP 精修）**：定位是「确定性引擎」而非时间线编辑器（`render.py` 可导出 FCPXML/EDL/OTIO 给专业剪辑器，但精修不在它手里）；
- **需要 GUI 拖拽体验的用户**：v4 新增的审查页（`npx ffmpeg-skill review project.json`）能看时间线与测量值、编辑字幕，但仍偏工作流工具而非剪映式体验。

---

## 与同类工具对比

| 维度 | ffmpeg-skill | 手写 ffmpeg 命令 | Remotion（JS 生成视频） | 剪映/CapCut |
|------|-------------|------------------|------------------------|-------------|
| 形态 | 42 个类型化工具 + 契约 + MCP | shell 字符串 | React 程序化渲染 | GUI 剪辑器 |
| Agent 友好 | **结构化参数、契约可读、结果自验证** | 靠 LLM 记忆拼命令，易猜错帧率/编码 | 需 Agent 写 React，生态偏生成式 | 不可被 Agent 调用 |
| 隐私 | **全本地，无 API Key** | 本地 | 本地 | 在线为主 |
| 平台交付 | **TikTok/Reels 等安全区模板内置 + 逐项 check** | 手工算安全区 | 需自己写 | 手动 |
| 验证 | **probe + check + look 联系表闭环** | 无，「跑完就算完」 | 无 | 人眼 |
| 上手 | 需 Node + FFmpeg + Agent 环境 | 零门槛但门槛在会用 ffmpeg | 需前端工程 | 零门槛 |

结论：**ffmpeg-skill 切的是「让 Agent 可靠地剪视频」这块地**——手写 ffmpeg 灵活但 Agent 会猜错且不验证；Remotion 强在程序化生成，真实素材的裁剪/音轨/交付不是主场；剪映是人用的 GUI。ffmpeg-skill 把「探测→无损编辑→验收」做成确定性流水线，契约与文档 CI 防漂移，工程化程度远超同类。短板是：个人维护、版本迭代快（v0.12 时还是 28 个工具，v4 已 42 个）、需要 Agent 环境才发挥全部价值。

> ⚠️ 三个要留意的点：
> 1. **FFmpeg 构建差异**：需要 6.1+ 且带完整滤镜（libass 等）；部分 Homebrew 默认版缺 libass/libfreetype，`doctor --json` 的 `tools` 字段能看到逐工具可用性，别只看总 `ok`；
> 2. **视觉验证依赖多模态 Agent**：`look.py` 只出 PNG，「看懂画面」是调用方 Agent 的视觉能力，纯脚本调用方要自己给裁切锚点（默认居中裁）；
> 3. **迭代快、个人项目**：五个月从 28 工具到 42 工具，契约与插件形态仍在快速演进，生产管线建议锁定版本。

---

## 如何使用

### 第一步：装 FFmpeg + 装 Skill

```bash
# FFmpeg 本体（一次）
sudo apt install ffmpeg        # Ubuntu/Debian；macOS 用 Homebrew，Windows 用 gyan.dev 构建

# 安装 skill（Claude Code / Cursor / Codex / 全装）
npx ffmpeg-skill
npx ffmpeg-skill --cursor
npx ffmpeg-skill --all

# 体检：ffmpeg/ffprobe 及每个工具需要的组件是否齐全
npx ffmpeg-skill doctor
```

### 第二步：让 Agent 干活（Claude Code / Cursor / Codex 对话里直接说）

> 「把 `interview.mp4` 的 0:45–3:10 和 5:00–6:30 留下来，做成正好 60 秒的 Reels。」

Agent 依次执行：`probe.py` → `cut.py --segments 0:45-3:10,5:00-6:30` → `fit.py --duration 60 --aspect 9:16 --fit crop` → `export.py --preset reels` → `check.py --platform reels` → `look.py`，最后报告「final.mp4：59.98s，1080×1920，30fps，AAC 立体声」并附上它检查过的联系表图片。

### 第三步：平台模板一键交付（不用 Agent 也能用）

```bash
# 字幕文件已有（cues.txt）时，一条命令出 TikTok 规格成品
python3 ~/.claude/skills/ffmpeg-skill/render.py talk.mp4 --template tiktok --cues cues.txt

# 先 dry-run 看它会执行什么 ffmpeg 命令，不落盘
python3 .../render.py talk.mp4 --template tiktok --dry-run
```

### 第四步：接入 MCP（无 shell 的客户端）

```json
{
  "mcpServers": {
    "ffmpeg-skill": {
      "command": "python3",
      "args": ["/Users/you/.claude/skills/ffmpeg-skill/mcp/server.py"]
    }
  }
}
```

默认只列核心 12 个工具，其余 30 个按名字 `tools/call` 可达；想要完整工具表设 `FFMPEG_SKILL_MCP_FULL=1`。MCP 注册表地址 `io.github.kajisho5/ffmpeg-skill`，或 `npx -y ffmpeg-skill mcp`。

### 需要语音转字幕？

```bash
pip install faster-whisper     # 最简单，首跑自动下载模型，音频不出本机
npx ffmpeg-skill contract --json | head -40   # 查看任意工具完整参数契约
```

---

## 总结

ffmpeg-skill 回答了一个很实际的问题：**让 Agent 操作 FFmpeg，如何不再靠猜？** 它的方案是「42 个类型化工具 + 从代码自动生成的机器可读契约 + 执行后强制验证 + 全本地零上传」，把探测、无损编辑、平台安全区、响度、交付验收全部工程化，SPEC 的「契约即代码、CI 防漂移」设计在同类 Agent Skill 里相当少见。对个人创作者和自动化管线，「一句话出全平台规格切片 + 自动验收」是实打实的效率提升；对开发者，它本身就是一份 Agent 工具架构的范本。

**扣分点：**

- **个人维护项目**：五个月大版本从 28 工具迭代到 42 工具，形态仍在演进，生产环境要锁版本；
- **环境门槛**：Node + FFmpeg 6.1+（完整滤镜构建）+ Agent 环境三件套，macOS 默认 Homebrew ffmpeg 可能缺 libass 需自查；
- **视觉验证看调用方**：联系表 PNG 要靠多模态 Agent 看，非视觉调用方得自己给裁切决策；
- **无 GUI 时间线**：精修场景仍需 PR / DaVinci / FCP（可导出 FCPXML/EDL/OTIO 衔接）。

**推荐指数：⭐⭐⭐⭐☆（4/5）**

- **播客 / 访谈 / 课程创作者（用 Agent 写代码的那种）** → **强烈建议装**，`npx ffmpeg-skill` + 一段话需求，多平台规格切片全在本机；
- **内容自动化管线** → `batch.py --watch` + 平台模板 + check 验收，可接 CI 定时批量；
- **MCP / Agent 工具开发者** → 读它的 `contract --json` 与 SPEC 实现，值得抄作业；
- **不用 Agent、只想拖拽剪视频** → 直接选剪映/CapCut，本工具不是给这个场景的。
