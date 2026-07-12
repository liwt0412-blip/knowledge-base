---
tags: [MOC, AI, Agent, MCP, 多Agent协作, 写作]
date: 2026-06-14
updated: 2026-07-11
---

# 🤖 AI Agent 总览

> 回到 [[00-入口|📂 知识库入口]]

本目录用于沉淀 AI Agent 的使用方法、Hermes/Codex 协作经验、MCP 与 Java Agent 学习资料，以及和 Agent 相关的写作/内容产出。

使用原则：这里不是所有 Agent 每次都要读的上下文。需要多 Agent 接力或长期记忆时，先读根目录的 [[00-我的长期上下文]]、[[00-当前主线]]、[[00-知识库地图]]。

---

## 1. 当前最有用

这些是当前阶段最值得优先维护和复用的笔记。

| 笔记 | 用途 | 读取时机 |
|---|---|---|
| [[AI协作四象限-让Agent按你的认知地图工作]] | 用四象限组织 Agent 任务、暴露盲区、沉淀隐性标准 | 不知道怎么给 Agent 下任务时 |
| [[codex-vs-hermes-agent]] | 判断 Codex、Hermes、Claude 分别适合做什么 | 多 Agent 分工时 |
| [[Loop Engineering 使用习惯]] | 给目标、不直接给步骤、先 explore、self-review、拆阶段 | 做复杂任务前 |
| [[Java_AI_Agent生态与MCP协议_2026-06-14]] | Java Agent、MCP、yu-ai-agent 学习路线 | 准备 Java + AI / MCP 内容时 |
| [[Hermes记忆备份/Hermes记忆迁移审计-2026-07-11]] | Hermes 记忆迁移判断和分流依据 | 审核或迁移 Hermes 记忆时 |

---

## 2. Agent 使用方法

这些笔记回答“怎么和 Agent 协作”。

- [[AI协作四象限-让Agent按你的认知地图工作]]  
  用 Johari 视窗拆解 AI 协作：已知的已知、已知的未知、未知的已知、未知的未知。

- [[Loop Engineering 使用习惯]]  
  记录更适合长期使用 Agent 的工作方式：给目标不给步骤、先侦察、写入项目约定、做完自审、拆阶段。

- [[codex-vs-hermes-agent]]  
  Codex 偏工程闭环，Hermes 偏长期个人 Agent 平台，Claude 偏推理和表达质量。

---

## 3. Hermes 资料

这些笔记用于理解和维护 Hermes，不默认作为当前事实。

- [[Hermes Agent 架构分析]]  
  Hermes 的整体架构、Transport、工具系统、Gateway、CLI、Skills、Memory、MCP 支持。

- [[Hermes Agent技能库/README|Hermes Agent 技能库]]  
  Hermes skills 能力清单。需要研究 Hermes 能做什么时再读。

- [[Hermes记忆备份/记忆备份-2026-07-11]]  
  Hermes 记忆历史备份。只作历史追溯，不默认加载。

- [[Hermes记忆备份/Hermes记忆迁移审计-2026-07-11]]  
  已经把 Hermes 记忆分流到长期上下文、当前主线、知识库地图后的审计记录。

---

## 4. MCP 与 Java Agent

这些笔记用于 Java + AI Agent 学习和面试素材扩展。

- [[Java_AI_Agent生态与MCP协议_2026-06-14]]  
  Java AI Agent 框架、MCP 协议、Java 写 MCP Server、yu-ai-agent 项目分析。

- [[抖音脚本-MCP协议Agent必知]]  
  MCP 协议的短视频口播脚本，是内容产物，不是技术主干。

- [[Agent即中间件-Jenkins的启示]]  
  从 Jenkins 类比 Agent：Pipeline、可观测性、插件生态、失败模式、人的角色变化。

- [[模型技术笔记]]  
  模型架构和模型动态的零散记录。后续可考虑迁移或合并到大模型基础模块。

---

## 5. 写作与内容表达

这些笔记用于减少 AI 味、保留人的表达，不属于 Agent 技术主线。

- [[人味儿写作-renwei-writing]]  
  人味儿写作方法论：位置、代价、手迹、7 条操作规则。

- [[人味儿写作-检查清单]]  
  检查文案是否过度 AI 化。

- [[人味儿写作-案例实录]]  
  一段文案三轮打磨的案例。

---

## 6. 读取策略

```text
要给 Agent 下任务 -> 读 AI协作四象限 / Loop Engineering
要判断任务给谁 -> 读 codex-vs-hermes-agent
要研究 Hermes -> 读 Hermes Agent 架构分析 / Hermes Agent技能库
要迁移 Hermes 记忆 -> 读 Hermes记忆迁移审计
要准备 Java + AI / MCP -> 读 Java_AI_Agent生态与MCP协议
要写内容或改稿 -> 读人味儿写作系列
```

不要把 Hermes 记忆备份当作当前事实。需要迁移时，先按 [[Hermes记忆备份/Hermes记忆迁移审计-2026-07-11]] 的规则审计。

---

## 7. 目录维护建议

- `AI Agent总览.md` 只做导航，不塞长内容。
- Hermes 记忆备份只增量保存，不默认读取。
- 工具版本号、端口、临时路径不写进本 MOC。
- 如果某篇笔记变成当前主线，应同步到根目录的 [[00-当前主线]] 或 [[00-知识库地图]]。

---

## 相关笔记

- [[00-我的长期上下文]]
- [[00-当前主线]]
- [[00-知识库地图]]
- [[MOC-编程相关|💻 编程相关]]
- [[SpringAI+AIGC应用/SpringAI+AIGC应用总览|🤖 Spring AI + AIGC]]
- [[MOC-日常学习|📖 日常学习]]
