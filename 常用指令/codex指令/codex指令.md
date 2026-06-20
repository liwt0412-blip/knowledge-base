---
tags:
  - 工具
  - codex
date: 2026-06-04
---
# 当前可用技能统计与使用说明

生成日期：2026-05-29  
当前目录：`D:\ai\codex`

## 1. 总览

当前会话可用技能共 **20 个**。

按来源统计：

| 来源 | 数量 | 技能 |
| --- | ---: | --- |
| Codex 系统技能 | 5 | `imagegen`, `openai-docs`, `plugin-creator`, `skill-creator`, `skill-installer` |
| 本地 agents 技能 | 15 | `caveman`, `diagnose`, `find-skills`, `grill-me`, `grill-with-docs`, `handoff`, `improve-codebase-architecture`, `prototype`, `setup-matt-pocock-skills`, `tdd`, `to-issues`, `to-prd`, `triage`, `write-a-skill`, `zoom-out` |

按用途统计：

| 类别 | 数量 | 技能 |
| --- | ---: | --- |
| 图片与视觉资产 | 1 | `imagegen` |
| OpenAI 文档/API 指南 | 1 | `openai-docs` |
| 技能/插件管理 | 5 | `plugin-creator`, `skill-creator`, `skill-installer`, `find-skills`, `write-a-skill` |
| 调试、测试、原型 | 3 | `diagnose`, `tdd`, `prototype` |
| 需求、Issue、项目流程 | 4 | `triage`, `to-issues`, `to-prd`, `setup-matt-pocock-skills` |
| 架构与代码理解 | 2 | `improve-codebase-architecture`, `zoom-out` |
| 方案追问与文档沉淀 | 2 | `grill-me`, `grill-with-docs` |
| 会话与沟通模式 | 2 | `handoff`, `caveman` |

## 2. 通用使用方法

这些技能不是你在终端里直接运行的命令，而是我在对话中可调用的工作流。你可以直接说：

- “用 `diagnose` 调试这个报错”
- “用 `tdd` 实现这个功能”
- “用 `prototype` 做几个 UI 原型”
- “用 `openai-docs` 查一下 Responses API 最新用法”
- “进入 `caveman` 模式，简短回答”
- “帮我找一个做部署检查的技能”

触发方式有两种：

1. **直接点名技能**：例如 `用 diagnose`、`/caveman`、`用 grill-me`。
2. **描述需求自动匹配**：例如你说“这个接口失败了，帮我 debug”，我会使用 `diagnose`；你说“把这个计划拆成 issue”，我会使用 `to-issues`。

## 3. 技能明细

### 3.1 `imagegen`

用途：生成或编辑位图图片，例如网站视觉图、产品图、游戏素材、UI mockup、透明背景素材、插画、信息图等。

适合场景：

- 生成新图片：封面图、落地页 hero 图、产品 mockup、游戏 sprite。
- 编辑已有图片：换背景、移除对象、改光照天气、合成多张图。
- 生成透明背景素材：默认先生成纯色背景，再本地抠图。

使用示例：

- “用 `imagegen` 生成一个科技博客封面图”
- “把这张图的背景去掉，导出透明 PNG”
- “给这个网页生成一张 hero 背景图”

注意事项：

- 如果是 SVG、图标系统、代码绘制图形，通常不使用这个技能，而是直接编辑代码或矢量文件。
- 项目要用的图片会保存到工作区中，不能只留在默认生成目录。

### 3.2 `openai-docs`

用途：查询 OpenAI 产品、API、模型选择、迁移和提示词升级的最新官方文档。

适合场景：

- 询问 OpenAI API 怎么用。
- 选择最新或最适合的 OpenAI 模型。
- 从旧模型/API 迁移到新模型/API。
- 需要官方文档引用和准确参数说明。

使用示例：

- “用 `openai-docs` 查 Responses API 的工具调用写法”
- “现在 OpenAI 最新推荐模型是什么？”
- “把这个项目从旧 Chat Completions 迁移到 Responses API”

注意事项：

- 涉及最新 OpenAI 文档时，应优先查官方文档。
- 不会凭记忆编造价格、参数或可用性。

### 3.3 `plugin-creator`

用途：创建或更新 Codex 插件目录，生成 `.codex-plugin/plugin.json`，可选生成 skills、hooks、scripts、assets、MCP、apps 等结构。

适合场景：

- 创建新的个人 Codex 插件。
- 给插件添加 marketplace 元数据。
- 更新本地插件开发版本并刷新 cachebuster。

使用示例：

- “用 `plugin-creator` 创建一个 personal plugin”
- “给这个插件加 marketplace 配置”
- “帮我 scaffold 一个带 skills 和 scripts 的插件”

注意事项：

- 插件名会规范化为小写 hyphen-case。
- 生成后应运行插件校验脚本。

### 3.4 `skill-creator`

用途：创建或更新 Codex 技能，强调技能设计原则、触发描述、资源组织和验证。

适合场景：

- 你想新增一个 Codex 技能。
- 你已有 `SKILL.md`，想改得更可靠。
- 你需要决定是否加入脚本、references、assets。

使用示例：

- “用 `skill-creator` 帮我设计一个数据库迁移技能”
- “检查这个技能的 description 是否容易触发”

注意事项：

- 技能描述很重要，因为它决定模型什么时候加载技能。
- 技能文件应保持简洁，复杂内容放到引用文件或脚本中。

### 3.5 `skill-installer`

用途：从 curated 列表或 GitHub 仓库安装 Codex 技能到 `$CODEX_HOME/skills`。

适合场景：

- 列出可安装技能。
- 安装官方 curated 或 experimental 技能。
- 从公开或私有 GitHub 仓库安装技能。

使用示例：

- “列出可安装的 curated skills”
- “安装 openai/skills 里的某个技能”
- “从这个 GitHub repo 安装技能”

注意事项：

- 安装通常需要网络权限。
- 安装后通常需要重启 Codex 才能加载新技能。

### 3.6 `find-skills`

用途：搜索开放技能生态，帮助发现适合某个任务的技能，并给出安装建议。

适合场景：

- 你问“有没有做 X 的技能？”
- 你想扩展 agent 能力。
- 你需要找某个领域的工具、模板或工作流。

使用示例：

- “帮我找一个 React 性能优化技能”
- “有没有做 changelog 的 skill？”
- “找一个 PR review 相关技能”

注意事项：

- 推荐前应考虑安装量、来源可信度和仓库质量。
- 可配合 `skill-installer` 安装。

### 3.7 `diagnose`

用途：按严格调试流程处理 bug、报错、性能回退和不稳定失败。

核心流程：

1. 建立可重复反馈环路。
2. 复现问题。
3. 提出 3 到 5 个可证伪假设。
4. 有针对性地加探针或日志。
5. 修复并补回归测试。
6. 清理临时代码并总结根因。

适合场景：

- 程序报错、测试失败、接口异常。
- 性能突然变慢。
- 问题偶发，需要提高复现率。

使用示例：

- “用 `diagnose` 调试这个失败”
- “这个页面有时候空白，帮我 debug”
- “测试在 CI 上随机失败”

注意事项：

- 核心是先建立可运行的失败信号，而不是直接猜原因。
- 临时 debug 日志应带唯一前缀，最后清理。

### 3.8 `tdd`

用途：用测试驱动开发的红绿重构循环实现功能或修 bug。

核心原则：

- 测试行为，不测试实现细节。
- 一次只写一个测试，再写最小实现。
- 不把所有测试一次性写完。
- 通过公共接口验证系统行为。

适合场景：

- 用户明确要求 TDD。
- 需要先写集成测试。
- 要新增功能且希望测试保护行为。

使用示例：

- “用 `tdd` 做这个功能”
- “按 red-green-refactor 修这个 bug”
- “先写集成测试再实现”

注意事项：

- 重构只能在测试通过后做。
- 优先写能穿过真实代码路径的测试。

### 3.9 `prototype`

用途：创建一次性原型，用来快速验证设计、状态机、业务逻辑或 UI 方向。

两条路线：

- 逻辑原型：可运行的终端小程序，验证状态和业务规则。
- UI 原型：同一路由下做多个明显不同的视觉方案，可切换比较。

适合场景：

- “先做个能玩的版本看看”
- 状态机或数据模型难以纸面判断。
- 想比较几个 UI 设计方向。

使用示例：

- “用 `prototype` 做三个界面方案”
- “给这个审批流做个终端原型”
- “我想先玩一下这个交互”

注意事项：

- 原型默认是一次性代码，应清楚标记。
- 不追求测试、持久化和完整错误处理。

### 3.10 `triage`

用途：分诊 issue，把问题推进到 `needs-triage`、`needs-info`、`ready-for-agent`、`ready-for-human` 或 `wontfix`。

适合场景：

- 创建或整理 issue。
- 查看哪些 issue 需要处理。
- 判断 bug/feature request 是否足够清楚。
- 给 AFK agent 准备可执行 issue brief。

使用示例：

- “用 `triage` 看看哪些 issue 需要我处理”
- “把 #42 分诊一下”
- “把 #42 移到 ready-for-agent”

注意事项：

- 依赖项目 issue tracker 和标签映射。
- 发布到 issue tracker 的 triage 评论需要带 AI 生成免责声明。

### 3.11 `to-issues`

用途：把计划、PRD 或规格拆成多个可独立领取的 issue。

核心方法：

- 使用 vertical slice / tracer bullet。
- 每个 issue 应覆盖端到端的一小段完整行为。
- 区分 AFK 和 HITL：AFK 可交给 agent 实现，HITL 需要人工决策或评审。

适合场景：

- 把大功能拆成任务。
- 把 PRD 拆成 implementation tickets。
- 为多个 agent 并行工作准备 issue。

使用示例：

- “用 `to-issues` 把这个计划拆成 issue”
- “把这个 PRD 拆成可交给 agent 的任务”

注意事项：

- 先让用户确认粒度、依赖关系和 HITL/AFK 标记，再发布。
- 不应修改或关闭父 issue。

### 3.12 `to-prd`

用途：根据当前对话和代码上下文生成 PRD，并发布到项目 issue tracker。

PRD 内容通常包括：

- Problem Statement
- Solution
- User Stories
- Implementation Decisions
- Testing Decisions
- Out of Scope
- Further Notes

适合场景：

- 你已经讨论了一段需求，希望沉淀成 PRD。
- 需要给后续 agent 或团队成员一个明确产品需求文档。

使用示例：

- “用 `to-prd` 把我们刚才讨论的内容写成 PRD”
- “把这个功能整理成 PRD 并发到 issue tracker”

注意事项：

- 这个技能倾向于综合已有上下文，不会反复采访用户。
- 依赖 issue tracker 配置。

### 3.13 `setup-matt-pocock-skills`

用途：为一组工程技能初始化项目配置，让它们知道 issue tracker、triage 标签和 domain docs 的位置。

适合场景：

- 第一次在某个 repo 使用 `to-issues`、`to-prd`、`triage`、`diagnose`、`tdd`、`improve-codebase-architecture` 或 `zoom-out`。
- 项目缺少 `AGENTS.md` / `CLAUDE.md` 中的技能配置。
- 技能不知道 issue tracker 或 domain docs 在哪里。

使用示例：

- “用 `setup-matt-pocock-skills` 初始化这个 repo 的 agent 配置”
- “这些工程技能找不到 issue tracker，帮我配置一下”

注意事项：

- 会探索仓库后询问 issue tracker、标签和 domain docs 布局。
- 不会在已有 `CLAUDE.md` 时随意创建 `AGENTS.md`，会优先编辑现有文件。

### 3.14 `improve-codebase-architecture`

用途：分析代码库架构，寻找能让模块更深、更可测试、更容易被 agent 理解的重构机会。

关注点：

- 哪些模块过浅，只是转发复杂度。
- 哪些接口泄漏实现细节。
- 哪些调用关系让测试困难。
- 哪些地方缺少清晰 seam、adapter、locality 和 leverage。

适合场景：

- 想做架构体检。
- 想找重构机会。
- 代码太散、太耦合、难测试。

使用示例：

- “用 `improve-codebase-architecture` 看看这个项目哪里值得重构”
- “帮我找几个深模块机会”

注意事项：

- 输出通常是可视化 HTML 报告。
- 会先读 `CONTEXT.md` 和 ADR，避免违背已有架构决策。

### 3.15 `zoom-out`

用途：当你不熟悉某块代码时，让我从更高抽象层画出相关模块、调用者和整体关系。

适合场景：

- 刚进入一个陌生代码区域。
- 想知道某个模块在系统里怎么被调用。
- 修 bug 前需要先理解上下文。

使用示例：

- “用 `zoom-out` 解释这个目录在系统中的位置”
- “先 zoom out，告诉我这些模块怎么连起来”

注意事项：

- 它偏理解和导览，不直接改代码。
- 会尽量使用项目的领域词汇。

### 3.16 `grill-me`

用途：对一个计划或设计进行连续追问，直到关键决策、依赖和边界都清楚。

适合场景：

- 你有一个方案，想被严格挑战。
- 想发现隐藏假设。
- 想在实现前把设计树走完。

使用示例：

- “用 `grill-me` 拷问我的方案”
- “我准备这么设计，帮我 relentlessly grill”

注意事项：

- 一次问一个问题。
- 如果问题能通过读代码回答，我会优先读代码。

### 3.17 `grill-with-docs`

用途：结合项目领域文档和 ADR 来追问设计，并在概念澄清后更新 `CONTEXT.md` 或创建 ADR。

适合场景：

- 设计涉及项目领域概念。
- 想检查方案是否和已有 domain language 冲突。
- 需要把讨论中确定的术语或决策沉淀到文档。

使用示例：

- “用 `grill-with-docs` 压测这个架构方案”
- “结合 CONTEXT.md 来问我这个领域模型设计”

注意事项：

- `CONTEXT.md` 只放领域词汇，不放实现细节。
- ADR 只在决策难逆转、没有上下文会令人困惑、确实存在权衡时创建。

### 3.18 `handoff`

用途：把当前对话压缩成交接文档，方便另一个 agent 或下一次会话继续。

适合场景：

- 当前上下文很长，需要交接。
- 要暂停工作，之后继续。
- 想让另一个 agent 接手。

使用示例：

- “用 `handoff` 写一份交接文档”
- “总结当前进展，下一轮继续修 bug”

注意事项：

- 交接文档保存到系统临时目录，不放当前项目目录。
- 会隐去 API key、密码、个人敏感信息。

### 3.19 `caveman`

用途：极简压缩沟通模式，减少废话和 token 消耗，但保留技术准确性。

适合场景：

- 你希望我回答极短。
- 长任务中只要关键状态。
- 你明确说 “caveman mode”、“be brief”、“less tokens”。

使用示例：

- “进入 `caveman` 模式”
- “后面都简短回答”
- “stop caveman” 或 “normal mode” 可恢复正常模式。

注意事项：

- 触发后会持续生效，直到你要求退出。
- 涉及危险操作确认、多步骤易误读说明时，会临时恢复清晰表达。

### 3.20 `write-a-skill`

用途：创建新的 agent skill，强调结构、渐进披露、引用文件和脚本资源。

适合场景：

- 想写一个新的本地技能。
- 想把某个重复工作流程封装成技能。
- 想设计 `SKILL.md`、`REFERENCE.md`、`EXAMPLES.md` 和 `scripts/`。

使用示例：

- “用 `write-a-skill` 写一个发布检查技能”
- “把这个工作流封装成 skill”

注意事项：

- 需要先明确任务领域、使用场景、是否需要脚本和参考材料。
- `description` 要写清楚触发条件，因为它决定技能是否会被加载。

## 4. 推荐组合用法

常见组合：

| 目标 | 推荐技能组合 |
| --- | --- |
| 调试复杂 bug | `diagnose`，必要时配合 `zoom-out` |
| 测试驱动实现功能 | `tdd` |
| 先验证设计再实现 | `prototype` -> `grill-me` 或 `grill-with-docs` |
| 把想法变成项目任务 | `to-prd` -> `to-issues` -> `triage` |
| 第一次在项目里使用工程技能 | `setup-matt-pocock-skills` |
| 做架构改进 | `zoom-out` -> `improve-codebase-architecture` -> `grill-with-docs` |
| 创建 agent 能力 | `find-skills` 或 `skill-installer`，必要时 `write-a-skill` / `skill-creator` |
| 做 OpenAI API 相关开发 | `openai-docs` |
| 生成图片资产 | `imagegen` |

## 5. 你可以直接这样对我说

- “用 `diagnose` 修这个报错，直到测试通过。”
- “用 `tdd` 给这个功能加测试并实现。”
- “用 `prototype` 做三个 UI 版本，我想比较一下。”
- “用 `openai-docs` 查官方文档，给我带引用。”
- “用 `to-issues` 把这份计划拆成 AFK issue。”
- “用 `improve-codebase-architecture` 给这个 repo 做架构体检。”
- “用 `write-a-skill` 帮我创建一个技能。”
- “进入 `caveman` 模式。”

## 相关笔记

- [[MOC-工具运维]]
