---
tags:
  - 工具
  - claude-code
date: 2026-06-04
---
# Matt Pocock Skills —— 中文详细指令手册

> 原文仓库: https://github.com/mattpocock/skills
> 这是一套面向**真正工程实践**（而非 vibe coding）的 Claude Code 技能集合。每个技能都是小而精、可组合的，基于数十年的工程经验设计。

---

## 目录

- [安装与配置](#安装与配置)
- [Engineering（工程技能）](#engineering工程技能)
  - [/grill-with-docs —— 带文档的深度质询](#grill-with-docs--带文档的深度质询)
  - [/grill-me —— 深度质询（无文档版）](#grill-me--深度质询无文档版)
  - [/tdd —— 测试驱动开发](#tdd--测试驱动开发)
  - [/diagnose —— 结构化调试](#diagnose--结构化调试)
  - [/to-prd —— 生成 PRD](#to-prd--生成-prd)
  - [/to-issues —— 拆分为 Issues](#to-issues--拆分为-issues)
  - [/triage —— Issue 分类](#triage--issue-分类)
  - [/zoom-out —— 放大视角](#zoom-out--放大视角)
  - [/improve-codebase-architecture —— 改善代码架构](#improve-codebase-architecture--改善代码架构)
  - [/prototype —— 构建原型](#prototype--构建原型)
  - [/setup-matt-pocock-skills —— 初始化配置](#setup-matt-pocock-skills--初始化配置)
- [Productivity（生产力技能）](#productivity生产力技能)
  - [/caveman —— 原始人极简模式](#caveman--原始人极简模式)
  - [/handoff —— 会话交接](#handoff--会话交接)
  - [/write-a-skill —— 编写新技能](#write-a-skill--编写新技能)
- [Misc（其他技能）](#misc其他技能)
  - [git-guardrails —— Git 安全防护](#git-guardrails--git-安全防护)
  - [/migrate-to-shoehorn —— 迁移到 shoehorn](#migrate-to-shoehorn--迁移到-shoehorn)
  - [/scaffold-exercises —— 脚手架练习题](#scaffold-exercises--脚手架练习题)
  - [/setup-pre-commit —— 配置 Pre-commit 钩子](#setup-pre-commit--配置-pre-commit-钩子)
- [技能组合使用场景](#技能组合使用场景)

---

## 安装与配置

### 在线安装

```bash
npx skills@latest add mattpocock/skills
```

安装过程中会出现交互式选择器，勾选你需要的技能，**务必勾选 `/setup-matt-pocock-skills`**。

### 初始化配置

安装后在 Claude Code 中运行：

```
/setup-matt-pocock-skills
```

它会问你三个问题：

1. **Issue 追踪器**：GitHub Issues / GitLab / 本地 Markdown 文件 / 其他
2. **Triage 标签**：你的 issue 标签命名习惯（如 `bug`、`enhancement`、`needs-triage` 等）
3. **领域文档布局**：单上下文（一个 `CONTEXT.md` + `docs/adr/`）还是多上下文（monorepo 风格）

> 注意：在中国大陆环境安装时可能遇到 GitHub 连接问题。可以配置代理后重试，或手动将仓库克隆到本地后链接。

---

## Engineering（工程技能）

日常编码必备的 10 个技能。

---

### /grill-with-docs —— 带文档的深度质询

**触发词**：开始一个新功能前、需要理清设计方案、想对齐认知

**作用**：Agent 会像面试官一样不断追问你的方案，每个问题一个一个来，逐步深入到决策树的每个分支。在质询过程中，会同步更新 `CONTEXT.md`（术语表）和 ADR（架构决策记录）。

**详细流程**：

1. **领域感知**：Agent 先读取 `CONTEXT.md` 了解项目的共享语言，读取 `docs/adr/` 了解历史架构决策
2. **术语挑战**：当你使用模糊或与术语表冲突的词汇时，Agent 会立刻指出——"你的术语表定义'取消'是 X，但你似乎在说 Y，到底是哪个？"
3. **场景压力测试**：Agent 会构造具体的边界场景来逼你精确化概念边界
4. **代码交叉验证**：Agent 会去读代码，检查你说的是否和代码一致。如果不一致，当场指出——"你的代码取消的是整个订单，但你说支持部分取消，哪个是对的？"
5. **实时更新 CONTEXT.md**：每当你确定一个术语，Agent 立刻写入 `CONTEXT.md`，不等、不攒
6. **按需创建 ADR**：只有在满足以下三个条件时才写 ADR：
   - **难以逆转**：改主意的代价很大
   - **缺少上下文会令人困惑**：未来读者会问"为什么这么做？"
   - **真实权衡的结果**：有真正的替代方案，你选了其中一个


**什么时候用**：
- 开始一个新功能开发前
- 设计方案感觉模糊，需要逼自己理清思路
- 多人协作，需要建立共享语言
- 项目缺乏文档，想顺带建立领域知识库

**注意**：CONTEXT.md 只放术语和定义，不放实现细节。它不是规格说明，而是术语表。

---

### /grill-me —— 深度质询（无文档版）

**触发词**：想被追问方案、非编码场景、快速对齐

**作用**：和 `/grill-with-docs` 一样的质询流程，但不更新文档。适合快速讨论、非代码决策、或你不想要文档副产品的场景。

**核心指令翻译**：
> 不断地追问我的计划，直到我们达成共识。沿着决策树的每个分支走到底，逐个解决决策之间的依赖关系。每个问题都要给出你的推荐答案。每次只问一个问题，等我给出反馈后再问下一个。如果一个问题可以通过探索代码库来回答，就去读代码而不是问我。

**什么时候用**：
- 非技术方案的讨论（产品方向、流程设计等）
- 不需要持久化文档的快速决策
- 你已经有完善的文档体系，不想额外维护

---

### /tdd —— 测试驱动开发

**触发词**：构建功能、修 bug、想要集成测试、测试先行开发

**核心理念**：测试应该通过公共接口验证行为，而非验证实现细节。代码可以完全重写，测试不应该变。

**好的测试** vs **坏的测试**：

| 好的测试 | 坏的测试 |
|---------|---------|
| 集成风格，通过公共 API 测试 | 耦合实现细节 |
| 描述**什么**行为 | 描述**如何**实现 |
| 重构后测试仍然通过 | 重构后测试断裂 |
| 像一份规格说明 | 测试私有方法、mock 内部协作者 |

**反模式——水平切片**（千万别这样做）：

```
❌ 错误（水平切片）：
  RED:   写 test1, test2, test3, test4, test5
  GREEN: 写 impl1, impl2, impl3, impl4, impl5

✅ 正确（垂直切片/示踪子弹）：
  RED→GREEN: test1→impl1
  RED→GREEN: test2→impl2
  RED→GREEN: test3→impl3
  ...
```

为什么水平切片是灾难？因为你批量写的测试是在测试**想象中的**行为而非**实际**行为，测试变得对真实变化不敏感——行为坏掉了测试还绿着，行为没变测试却红了。

**完整工作流**：

1. **规划阶段**
   - 确认接口变更
   - 确认要测试哪些行为（按优先级排序）
   - 寻找"深模块"机会（小接口，深层实现）
   - 设计可测试的接口
   - 列出要测试的行为（不是实现步骤）
   - **获得用户批准**

2. **示踪子弹**（第一条测试）
   - RED：写一个测试验证一个行为 → 测试失败
   - GREEN：写最少代码让测试通过 → 测试通过
   - 这条示踪子弹证明了整条路径端到端可行

3. **增量循环**（后续每个行为）
   - RED：写下一条测试 → 失败
   - GREEN：最少代码 → 通过
   - 一次只写一个测试
   - 只为当前测试写足够的代码
   - 不要预测未来的测试
   - 保持测试关注可观察的行为

4. **重构阶段**
   - 所有测试通过后才进入重构
   - 提取重复代码
   - 深化模块（将复杂性移入简单接口背后）
   - 每步重构后立即运行测试
   - **绝不在 RED 状态重构**

**每个周期的检查清单**：
```
[ ] 测试描述的是行为，不是实现
[ ] 测试只使用公共接口
[ ] 测试能经受内部重构的考验
[ ] 代码刚好够过当前测试
[ ] 没有添加投机性功能
```

**什么时候用**：
- 开始新功能开发
- 修复复杂 bug
- 重构高风险代码
- 想建立自动化防护网

---

### /diagnose —— 结构化调试

**触发词**：调试、排查 bug、性能回归、程序崩溃、报错

**六个阶段**（跳过阶段需要明确说明理由）：

**Phase 1 — 建立反馈循环（最关键的阶段！）**

> 这是整个技能的核心。如果你有一个快速、确定性、Agent 可运行的通过/失败信号，你就能找到根因。如果没有，盯着代码看多久都没用。
>
> 在这个阶段要不遗余力。大胆、有创造力、拒绝放弃。

构建反馈循环的 10 种方法（按推荐顺序）：

1. **失败测试**：在离 bug 最近的缝隙处写一个失败的测试
2. **curl/HTTP 脚本**：对运行中的 dev 服务器发送请求
3. **CLI 调用**：传入固定输入，将 stdout 与已知正确的快照做 diff
4. **无头浏览器脚本**：Playwright/Puppeteer 驱动 UI，断言 DOM/控制台/网络
5. **重放捕获的追踪**：保存真实请求/负载/事件日志到磁盘，隔离重放
6. **一次性测试台**：启动最小系统子集，用单个函数调用触发 bug 路径
7. **属性/模糊测试**：如果是"偶尔出错"，运行 1000 次随机输入找失败模式
8. **二分定位**：如果在两个已知状态之间出现，自动化二分查找
9. **差分循环**：新旧版本用相同输入，对比输出差异
10. **人机协作 bash 脚本**：最后手段。如果必须人工点击，用脚本驱动人工操作

**迭代优化反馈循环**：
- 能不能更快？（缓存 setup、跳过无关初始化、缩小测试范围）
- 信号能不能更精确？（断言具体症状，不只是"没崩溃"）
- 能不能更确定性？（固定时间、种子 RNG、隔离文件系统、冻结网络）

一个 30 秒的抖动循环比没有好不了多少。一个 2 秒的确定性循环是调试超能力。

**非确定性 Bug**：目标不是干净复现，而是**提高复现率**。并行跑 100 次、加压力、缩小时间窗口、注入 sleep。50% 复现率的 bug 可以调试，1% 的不行。

**如果实在无法建立循环**：停下来，明确说明。列出你尝试过的所有方法。向用户索要环境和产物——不要在没有循环的情况下继续。

**Phase 2 — 复现**
- 运行循环，亲眼看到 bug
- 确认循环产生的是**用户描述的**故障模式——不是碰巧在附近的另一个问题
- 跨多次运行验证可复现性
- 捕获精确的症状（错误信息、错误输出、慢时序）

**Phase 3 — 提出假设**
- 生成 **3-5 个有序假设** 后再测试，避免锚定在第一个想法
- 每个假设必须是**可证伪的**
- 格式："如果 X 是根因，那么改变 Y 会让 bug 消失 / 改变 Z 会让它更糟"
- 如果无法陈述预测，这个假设就是直觉——要么细化，要么丢弃
- **在测试前给用户看排序列表**（用户可能有领域知识可以瞬间重排序），但不要等用户——用户 AFK 时就按自己的排序继续

**Phase 4 — 插入探针**
- 每个探针必须映射到 Phase 3 的具体预测
- **一次只改一个变量**
- 工具优先级：调试器/REPL > 定点日志 > "全部打日志然后 grep"
- 所有调试日志用唯一前缀标记，如 `[DEBUG-a4f2]`，清理由一个 grep 搞定
- 性能回归不用日志——先做基线测量，再二分定位，先测量后修复

**Phase 5 — 修复 + 回归测试**
- **在修复前写回归测试**——但只在有"正确缝合处"的时候
- "正确缝合处"是测试能演练**真实 bug 模式**的地方。如果可用的缝合处太浅（单调用者测试当 bug 需要多调用者时），那里的回归测试给的是虚假安全感
- 如果没有正确缝合处——**这本身就是发现**，记下来。代码架构阻碍了 bug 被锁定
- 如果有正确缝合处：把最小化复现变成失败测试 → 看它失败 → 应用修复 → 看它通过 → 在原始（未最小化）场景重新运行 Phase 1 反馈循环

**Phase 6 — 清理 + 复盘**
- [ ] 原始复现不再复现
- [ ] 回归测试通过（或缺少缝合处已文档化）
- [ ] 所有 `[DEBUG-...]` 标记的探针已删除
- [ ] 一次性原型已删除（或移到明确标记的调试位置）
- [ ] 被证明正确的假设写在了 commit/PR 信息中
- 然后问：**什么能预防这个 bug？** 如果答案涉及架构变更（没有好的测试缝合处、纠缠的调用者、隐藏耦合），用具体信息移交给 `/improve-codebase-architecture`

---

### /to-prd —— 生成 PRD

**触发词**：想从当前对话创建 PRD、把讨论变成正式需求文档

**作用**：不采访你——直接从当前对话上下文和代码库理解中合成一份 PRD，发布到项目的 issue 追踪器。

**流程**：

1. 探索代码库，使用项目的领域术语
2. 勾画需要构建或修改的主要模块，主动寻找可以隔离测试的"深模块"
3. 和你确认模块划分和测试范围
4. 按模板写 PRD，发布到 issue 追踪器，打上 `ready-for-agent` 标签

**PRD 模板包含**：
- **问题陈述**：用户面临的问题（用户视角）
- **解决方案**：解决方案（用户视角）
- **用户故事**：一长串编号的用户故事，格式为"作为 <角色>，我想要 <功能>，以便 <收益>"
- **实现决策**：模块划分、接口变更、技术澄清、架构决策、Schema 变更、API 契约
- **测试决策**：什么算好测试、哪些模块要测试、参考哪种已有测试
- **不在范围内**：明确排除的内容
- **补充说明**：其他补充信息

**注意**：不要在 PRD 中包含具体文件路径或代码片段（会很快过时）。唯一的例外是原型产出了比文字更精确的决策片段（状态机、reducer、schema、类型形态）。

---

### /to-issues —— 拆分为 Issues

**触发词**：把方案/Spec/PRD 变成实现任务、拆分工作

**作用**：把一个方案拆成多个可以**独立认领**的 issue，使用示踪子弹垂直切片。

**核心概念——垂直切片 vs 水平切片**：

垂直切片（示踪子弹）：每个 issue 是一刀纵切所有层的完整路径
水平切片（反模式）：每个 issue 是一个层的工作（所有 schema 改完 -> 所有 API 改完 -> 所有 UI 改完）

切片规则：
- 每个切片交付一条狭窄但**完整**的路径（schema → API → UI → 测试）
- 一个切片完成后可以**独立演示或验证**
- 宁可多分几个薄切片，不要少分几个厚切片

**切片类型**：
- **AFK**（Away From Keyboard）：Agent 可以独立实现和合并，不需要人工干预
- **HITL**（Human In The Loop）：需要人工介入——如架构决策、设计审查

优先选 AFK。

**流程**：

1. 从对话上下文或用户传入的 issue 获取素材
2. （可选）探索代码库
3. 起草垂直切片列表
4. 展示给用户确认：粒度是否合适？依赖关系是否正确？HITL/AFK 标记对吗？
5. 按依赖顺序发布到 issue 追踪器

**Issue 模板包含**：
- 父 issue 引用
- 要构建什么（端到端行为，不写层到层的实现）
- 验收标准（checklist）
- 阻塞关系

---

### /triage —— Issue 分类

**触发词**：管理 issue、审查新 issue、准备给 Agent 的 issue、管理工作流

**Triage 角色体系——一个小型状态机**：

**两类分类角色**（category）：
- `bug` —— 东西坏了
- `enhancement` —— 新功能或改进

**五种状态角色**（state）：
- `needs-triage` —— 维护者需要评估
- `needs-info` —— 等待提交者补充信息
- `ready-for-agent` —— 已完全指定，AFK Agent 可以接手
- `ready-for-human` —— 需要人工实现
- `wontfix` —— 不予处理

每个已分类的 issue 应该恰好有一个分类角色和一个状态角色。

**状态流转**：
```
未标记 → needs-triage → needs-info → needs-triage（提交者回复后）
                       → ready-for-agent
                       → ready-for-human
                       → wontfix
```

**使用方式**：
- `/triage` "看看需要我关注什么" → 列出三类 buckets（未标记/needs-triage/needs-info有新回复）
- `/triage` "来看下 #42" → 深入分类某个 issue
- `/triage` "把 #42 移到 ready-for-agent" → 快速状态覆盖

**分类单个 issue 的流程**：
1. 读完整 issue（正文、评论、标签、提交者、日期）
2. 推荐分类和状态，附推理和代码库摘要
3. （仅 bug）先尝试复现，再进入质询
4. 如需充实细节，运行 `/grill-with-docs`
5. 应用结果：打标签、写 Agent 简报、或关闭

**每个由 AI 在 Triage 过程中发布的 issue/评论必须以 `> *This was generated by AI during triage.*` 开头。**

---

### /zoom-out —— 放大视角

**触发词**：对代码不熟悉、想了解代码在系统中的位置

**这是给它一句话指令的快捷技能**：

> 我对这片代码不熟悉。往上一层抽象。用项目的领域术语，给我一张所有相关模块和调用者的地图。

**什么时候用**：
- 打开一个陌生文件，想知道"这段代码在整个系统中扮演什么角色"
- 看到一个函数，想知道谁在调用它、它又依赖什么
- 想从"局部理解"切换到"全局视野"

---

### /improve-codebase-architecture —— 改善代码架构

**触发词**：改善架构、找重构机会、合并紧密耦合的模块、让代码库更可测试、更适合 AI 导航

**核心理念**：寻找"深化"机会——把浅模块变成深模块的改造。

**专属术语**（统一使用这套语言，不要漂移）：
- **模块（Module）**：任何有接口和实现的东西（函数、类、包、切片）
- **接口（Interface）**：调用者使用模块需要知道的一切：类型、不变量、错误模式、排序、配置
- **实现（Implementation）**：内部的代码
- **深度（Depth）**：接口处的杠杆率——大量行为藏在简单接口后面。**深** = 高杠杆。**浅** = 接口几乎和实现一样复杂
- **缝合处（Seam）**：接口所在的地方；可以不就地编辑而改变行为的位置（不用"边界"这个词）
- **适配器（Adapter）**：在缝合处满足接口的具体东西
- **杠杆（Leverage）**：调用者从深度中获得的收益
- **局部性（Locality）**：维护者从深度中获得的收益——变更、bug、知识集中在一处

**删除测试**：想象删除这个模块。如果复杂性消失了，那它是个传话筒（pass-through）。如果复杂性重新出现在 N 个调用者中，那它在发挥作用。

**完整流程**：

1. **探索**：用 Agent 工具走查代码库，感知摩擦点——
   - 理解一个概念需要在多个小模块间跳转？
   - 哪些模块是"浅"的（接口几乎和实现一样复杂）？
   - 哪些纯函数只是为了可测试性而抽出来，但真正的 bug 藏在它们如何被调用中？
   - 哪些模块紧密耦合，跨越了它们的缝合处？
   - 哪些部分没测试，或难以通过当前接口测试？

2. **生成 HTML 报告**：写到系统临时目录（`%TEMP%`），自动在浏览器打开。报告包含——
   - 每个候选方案的卡片：涉及文件、问题描述、解决方案、收益（用局部性和杠杆解释）
   - **前后对比图**：手绘风格的架构对比
   - 推荐强度徽章：`Strong` / `Worth exploring` / `Speculative`
   - 使用 Tailwind CSS（CDN）和 Mermaid（CDN）做可视化
   - 用 CONTEXT.md 的词汇描述领域概念，用上面定义的术语描述架构
   - 如果候选方案与现有 ADR 冲突，在卡片中明确标出警告

3. **质询循环**：用户选定一个候选方案后，进入深度讨论——
   - 走查设计树：约束、依赖、深化后模块的形态、缝合处背后是什么、哪些测试存活
   - 实时更新 CONTEXT.md（新术语）
   - 如果用户以"有分量的理由"拒绝候选方案，主动提议写 ADR 防止未来再被提出

**建议每几天在代码库上跑一次。**

---

### /prototype —— 构建原型

**触发词**：构建原型、验证数据模型/状态机、UI 设计选项、"原型一下"、"让我玩玩看"、"试几种设计"

**核心理念**：原型是**回答一个问题的抛弃式代码**。问题决定了原型的形态。

**两条分支**：

| 问题 | 分支 | 产物 |
|------|------|------|
| "这个逻辑/状态模型对吗？" | [LOGIC 分支] | 小型可交互终端 App，把状态机推到纸面上难以推理的 case |
| "这个该长什么样？" | [UI 分支] | 多个截然不同的 UI 变体，通过 URL 参数和浮动底栏切换 |

**两条分支通用的规则**：

1. **从第一天就标记为抛弃式**：原型代码放在它真正会被使用的位置附近（靠近它要原型的模块或页面），但命名要让随便看一眼的人就知道这是原型不是生产代码
2. **一个命令就能跑**：用项目已有的 task runner
3. **默认无持久化**：状态在内存中。持久化是原型要**检验**的东西，不是它依赖的东西
4. **跳过打磨**：不写测试、不加多余的错误处理、不抽象。目的是快速学点什么然后删掉
5. **暴露状态**：每次操作后打印或渲染完整的相关状态
6. **完成后删除或吸收**：原型的价值在于它的**答案**，不是它的代码。把答案捕获到某个持久的地方（commit message、ADR、issue），然后删掉原型

---

### /setup-matt-pocock-skills —— 初始化配置

**触发词**：首次安装后运行、为仓库配置 skills

**作用**：为当前仓库创建 `docs/agents/` 目录，写入三个配置文件，并在 `CLAUDE.md` 或 `AGENTS.md` 中添加 `## Agent skills` 块。

**写入的文件**：
- `docs/agents/issue-tracker.md` —— Issue 追踪器配置
- `docs/agents/triage-labels.md` —— Triage 标签词汇映射
- `docs/agents/domain.md` —— 领域文档布局 + 消费规则

**会在 CLAUDE.md（或 AGENTS.md）中添加的块**：
```markdown
## Agent skills

### Issue tracker
...

### Triage labels
...

### Domain docs
...
```

这些配置信息被以下技能消费：`to-issues`、`to-prd`、`triage`、`diagnose`、`tdd`、`improve-codebase-architecture`、`zoom-out`。

---

## Productivity（生产力技能）

日常非编码工作流工具。

---

### /caveman —— 原始人极简模式

**触发词**：减少 token、极简回复、省字数

**作用**：Agent 切换到极简沟通模式，砍掉 ~75% 的 token 用量，同时保持技术准确性。

**丢弃的内容**：
- 冠词（a/an/the）
- 填充词（just/really/basically/actually/simply）
- 客套话（sure/certainly/of course/happy to）
- 模糊措辞

**保留的内容**：
- 技术术语精确不变
- 代码块原样保留
- 错误信息引用原样

**模式对比**：
```
❌ 正常模式：
"Sure! I'd be happy to help you with that. The issue you're experiencing is likely caused by the token expiry check using < instead of <=. Here's how we can fix it:"

✅ Caveman 模式：
"Bug in auth middleware. Token expiry check use < not <=. Fix:"
```

**自动清晰度例外**：以下情况临时退出 caveman 模式——
- 安全警告
- 不可逆操作确认
- 多步骤序列，片段顺序可能导致误解
- 用户要求澄清或重复问题

**开启**：说 "caveman mode" / "less tokens" / "be brief"
**关闭**：说 "stop caveman" / "normal mode"

---

### /handoff —— 会话交接

**触发词**：交接给另一个 Agent 继续工作

**用法**：`/handoff <下一阶段要做什么>`

**作用**：把当前对话压缩成一份交接文档，保存在操作系统临时目录（不是当前工作区）。

**包含内容**：
- 当前进度和上下文
- 已经完成了什么
- "建议的技能"部分——建议下一个 Agent 调用哪些 skills
- 已创建的产物引用（PRD、计划、ADR、issue、commit、diff）

**应被排除的内容**：
- 已经在其他产物中捕获的内容（引用路径或 URL 即可）
- 敏感信息（API 密钥、密码、个人身份信息）

---

### /write-a-skill —— 编写新技能

**触发词**：创建新 skill

**流程**：
1. **收集需求**：问用户——技能覆盖什么任务/领域？具体用例？需要脚本还是纯指令？
2. **起草技能**：创建 SKILL.md + 补充文件 + 工具脚本
3. **审查**：和用户一起检查

**技能文件结构**：
```
skill-name/
├── SKILL.md           # 主指令（必须）
├── REFERENCE.md       # 详细文档（如需要）
├── EXAMPLES.md        # 使用示例（如需要）
└── scripts/           # 工具脚本（如需要）
    └── helper.js
```

**Description 字段的重要性**：description 是 Agent 判断"是否应该加载这个技能"的**唯一依据**。它出现在 system prompt 中，Agent 根据用户请求和 description 做匹配。写好 description：
- 第一句：这个技能做什么
- 第二句：什么时候触发（"Use when..."）
- 最多 1024 字符

---

## Misc（其他技能）

偶尔使用但保留的工具。

---

### git-guardrails —— Git 安全防护

**触发词**：防止危险 git 操作

**作用**：设置 Claude Code 的 PreToolUse hook，在执行前拦截危险命令。

**默认拦截**：
- `git push`（所有变体，包括 `--force`）
- `git reset --hard`
- `git clean -f` / `git clean -fd`
- `git branch -D`
- `git checkout .` / `git restore .`

**流程**：
1. 问用户：项目级（`.claude/settings.json`）还是全局（`~/.claude/settings.json`）？
2. 复制拦截脚本到 `.claude/hooks/block-dangerous-git.sh`
3. 在 settings.json 中添加 PreToolUse hook
4. 问用户是否要自定义拦截列表
5. 验证：运行测试确认 hook 生效

当命令被拦截时，Claude 会收到"没有权限执行此命令"的消息。

---

### /migrate-to-shoehorn —— 迁移到 shoehorn

**触发词**：替换测试中的 `as` 断言

**作用**：把测试文件中的 `as` 类型断言迁移到 `@total-typescript/shoehorn`，让部分测试数据在保持类型安全的前提下通过编译。

**迁移对照**：

| 之前 | 之后 |
|------|------|
| `data as Request` | `fromPartial(data)` |
| `data as unknown as Request` | `fromAny(data)` |

三个核心函数：
- `fromPartial()` — 传入部分数据，仍然通过类型检查
- `fromAny()` — 传入故意错误的数据（保留自动补全）
- `fromExact()` — 强制完整对象（后期可用它替换 fromPartial）

---

### /scaffold-exercises —— 脚手架练习题

**触发词**：创建练习目录结构

**作用**：按特定目录结构创建练习题（section → exercise → problem/solution/explainer），然后运行 `pnpm ai-hero-cli internal lint` 验证。

**目录命名规范**：
- Section：`XX-section-name/`（如 `01-retrieval-skill-building`）
- Exercise：`XX.YY-exercise-name/`（如 `01.03-retrieval-with-bm25`）

**每个 exercise 需要的变体文件夹**：
- `problem/` — 学生工作区（含 TODO）
- `solution/` — 参考实现
- `explainer/` — 概念材料（无 TODO）

---

### /setup-pre-commit —— 配置 Pre-commit 钩子

**触发词**：添加 pre-commit hooks、Husky、lint-staged

**作用**：在当前仓库设置 Husky pre-commit 钩子，包含：
- **lint-staged** + Prettier（格式化所有暂存文件）
- **typecheck** 脚本
- **test** 脚本

自动检测包管理器（npm/pnpm/yarn/bun），安装依赖，初始化 Husky，创建 `.lintstagedrc` 和 `.prettierrc`（如果缺少），最后提交配置。

---

## 技能组合使用场景

### 场景 1：从零开始一个新功能

```
1. /grill-with-docs     → 深度质询，理清方案，建立共享语言
2. /to-prd              → 把质询结果合成 PRD，发布到 issue 追踪器
3. /to-issues           → 把 PRD 拆成可独立实现的垂直切片
4. /tdd                 → 对每个切片，红绿重构循环实现
5. /diagnose            → 遇到 bug 时结构化排查
```

### 场景 2：修复一个复杂 Bug

```
1. /diagnose            → 建立反馈循环 → 复现 → 假设 → 修复 → 回归测试
2. /zoom-out            → （如果发现系统性问题）了解耦合的全貌
3. /improve-codebase-architecture → 如果架构助长了这个 bug，找出重构机会
```

### 场景 3：AI 接手一个 Issue

```
1. /triage              → 维护者分类 issue，打上 ready-for-agent
2. Agent 开始工作
3. /zoom-out            → Agent 如果不熟悉相关代码，放大看全貌
4. /tdd                 → Agent 用 TDD 实现
5. /handoff             → 如果需要换一个 Agent 继续
```

### 场景 4：代码库维护日

```
1. /improve-codebase-architecture → 生成架构审查报告
2. 挑选一个候选方案进行 grilling
3. /tdd                 → 在重构过程中用测试保护行为不变
```

### 场景 5：团队协作对齐

```
1. /grill-with-docs     → 建立 CONTEXT.md 共享语言
2. /triage              → 日常 issue 管理，write agent briefs
3. /handoff             → 在不同开发者/Agent 间传递上下文
```

---

## 文件结构与约定

运行 `/setup-matt-pocock-skills` 后，仓库中会形成以下结构：

```
/
├── CONTEXT.md              ← 领域术语表（由 grill-with-docs 维护）
├── CLAUDE.md               ← 包含 ## Agent skills 块
├── docs/
│   ├── adr/                ← 架构决策记录
│   │   ├── 0001-xxx.md
│   │   └── 0002-xxx.md
│   └── agents/             ← skills 配置文件
│       ├── issue-tracker.md
│       ├── triage-labels.md
│       └── domain.md
└── src/
```

多上下文的 monorepo：
```
/
├── CONTEXT-MAP.md          ← 指向各上下文的 CONTEXT.md
├── docs/
│   └── adr/                ← 系统级决策
├── src/
│   ├── ordering/
│   │   ├── CONTEXT.md
│   │   └── docs/adr/       ← 上下文级决策
│   └── billing/
│       ├── CONTEXT.md
│       └── docs/adr/
```

---

> 这些技能的设计哲学：**软件工程基础比以往任何时候都重要**。AI 加速了编码，也加速了软件熵增。这些技能是对工程基础的最佳实践封装。
>
> 原仓库: https://github.com/mattpocock/skills

## 相关笔记

- [[MOC-工具运维]]
