---
tags: [AI, LLM, Agent, RAG, MCP, 全景]
date: 2026-06-11
sources:
  - https://arxiv.org/abs/1706.03762
  - https://arxiv.org/abs/2106.09685
  - https://arxiv.org/abs/2005.11401
  - https://arxiv.org/abs/2210.03629
  - https://modelcontextprotocol.info/docs/introduction/
confidence: high
---

# AI 应用技术全景（2025-2026）

> 整合自：近年 AI 应用技术串讲文档 + Hermes Agent 深度讲解
>
> 覆盖 14 个核心技术方向，每个技术按"定义 → 要解决的问题 → 实现原理 → 最新进展"展开。

---

## 目录

1. [LLM（大语言模型）](#1-llm大语言模型)
2. [Prompt Engineering（提示词工程）](#2-prompt-engineering提示词工程)
3. [Fine-tuning（微调）](#3-fine-tuning微调)
4. [RAG（检索增强生成）](#4-rag检索增强生成)
5. [Function Calling（函数调用）](#5-function-calling函数调用)
6. [MCP（模型上下文协议）](#6-mcp模型上下文协议)
7. [Agent（智能体）](#7-agent智能体)
8. [Multi-Agent（多智能体）](#8-multi-agent多智能体)
9. [Context Engineering（上下文工程）](#9-context-engineering上下文工程)
10. [Agent Skill（智能体技能）](#10-agent-skill智能体技能)
11. [Harness Engineering（受控工程）](#11-harness-engineering受控工程)
12. [MoE（混合专家）](#12-moe混合专家)
13. [推理增强（Test-Time Compute）](#13-推理增强test-time-compute)
14. [模型架构创新（Mamba / MTP / FlashAttention）](#14-模型架构创新mamba--mtp--flashattention)

---

## 1. LLM（大语言模型）

### 定义

Transformer 架构的提出奠定了大模型时代基础，使基于注意力机制的生成模型成为主流。Decoder-Only（仅解码器）的 Transformer 架构变体是当下最为流行的架构。

### 要解决的问题

传统 RNN/LSTM 存在两个致命问题：① 长序列梯度消失，记不住远距离依赖；② 串行计算，无法并行训练。Transformer 用自注意力机制同时解决了这两个问题。

### 实现原理

- **自注意力（Self-Attention）**：每个 token 通过 Q/K/V 计算与所有其他 token 的关联权重，实现全局依赖建模
- **多头注意力（Multi-Head Attention）**：用多组 Q/K/V 并行学习不同的语义关系（语法、语义、指代等）
- **位置编码（Positional Encoding）**：因为注意力本身不感知位置顺序，需要注入位置信息（原始用正弦波，现代用 RoPE）
- **Decoder-Only 架构**：只保留 Transformer 的解码器部分，通过因果掩码（causal mask）实现自回归生成

### 核心演进（LLM 发展 6 阶段）

| 阶段 | 时间 | 关键模型 | 核心突破 |
|---|---|---|---|
| 统计语言模型 | ~2000–2012 | n-gram, NNLM, Word2Vec | 词嵌入，神经网络语言模型 |
| Attention + Seq2Seq | 2014–2016 | Bahdanau Attention | 注意力对齐机制 |
| Transformer 奠基 | 2017–2019 | **Transformer**, BERT, GPT, T5 | Attention Is All You Need，预训练-微调范式 |
| 大规模缩放 | 2020–2022 | **GPT-3**, Chinchilla, PaLM, LLaMA | In-Context Learning, Scaling Law, RLHF |
| 多模态+开源爆发 | 2023–2024 | **GPT-4**, Claude 3, LLaMA 3, Mixtral, DeepSeek-V2 | MoE, RAG, DPO, 长上下文 |
| 推理增强 | 2024–2026 | o1/R1, DeepSeek-V3, Claude 4, Gemini 2.0 | Test-Time Compute, Agent, MCP |

### 2025-2026 最新进展

- **DeepSeek-V3**：671B MoE，训练效率极高，超越多数闭源模型
- **LLaMA 4**：多模态 MoE，1M+ 上下文，Multi-Token Prediction
- **推理模型（o1/o3/R1/QwQ）**：推理时扩展成为新的 Scaling Law
- **上下文扩展**：YaRN、Ring Attention、SnapKV 等技术实现 2M-10M token 支持

---

## 2. Prompt Engineering（提示词工程）

### 定义

提示词是用来引导模型按照特定意图生成输出的输入指令，主要包含「系统提示词」和「用户提示词」。提示词工程是通过设计和优化提示词，使大模型更准确、可控地产生所需输出。是一种提升效果但不改变模型参数的**低成本调优手段**。

### 要解决的问题

LLM 基于概率生成，同样的输入可能产生不同质量的输出。Prompt Engineering 在不修改模型权重的前提下，通过输入设计来约束输出质量、格式和风格。

### 实现原理

- **系统提示词（System Prompt）**：设定模型角色、行为规则、输出约束，在对话开始前注入
- **思维链（Chain-of-Thought, CoT）**：引导模型在给出答案前先展示推理步骤，显著提升数学/逻辑问题准确率
- **Few-shot / Zero-shot**：在 prompt 中提供示例（few-shot）或不提供（zero-shot），让模型通过上下文学习完成任务
- **结构化输出**：用 XML/JSON 格式约束输出结构，便于程序解析

### 局限性

- 脆弱性：prompt 微调对输出影响大，小改动可能导致结果完全变化
- 上下文限制：受限于 LLM 的上下文窗口
- **2025 趋势**：推理模型（o1/R1）已内化 CoT 能力，外部 Prompt 工程的重要性正在下降

---

## 3. Fine-tuning（微调）

### 定义

微调是在已有模型基础上，用特定数据再训练，让模型更适合某个具体任务或场景。微调要训练的是模型的参数。LoRA 算法通过只训练少量低秩参数来进行微调，大幅降低了训练成本。

### 要解决的问题

通用 LLM 在特定领域（法律、医疗、企业数据）或特定风格（角色扮演、客服）上不够精准。重新训练大模型成本极高，微调通过小规模数据让模型适配专项任务。

### 实现原理

- **全量微调（Full Fine-tuning）**：更新所有模型参数，效果好但资源需求大
- **LoRA（Low-Rank Adaptation）**：冻结原模型参数，在注意力层插入低秩矩阵（A×B）进行训练，参数量减少 1000 倍以上
- **QLoRA**：在 LoRA 基础上对原始模型进行 4-bit 量化，进一步降低显存需求
- **DPO（Direct Preference Optimization）**：2024 年新范式，替代 RLHF，无需奖励模型，直接优化偏好对

### 微调 vs RAG

| 维度 | 微调 | RAG |
|---|---|---|
| 知识更新 | 重新训练 | 更新数据库即可 |
| 实时性 | 差（需要训练周期） | 好（即时检索） |
| 隐私 | 知识融入模型 | 知识不外泄 |
| 幻觉 | 可能记忆错误 | 可追溯来源 |

### 2025-2026 新进展

- **Self-Rewarding LM**：模型自我标注偏好数据，无需人工标注
- **Model Merging**：线性合并多个 LoRA 适配器产生更强模型（Tulu 3）
- **DPO++ / SimPO**：解决 DPO 的生成膨胀问题
- **Data-constrained Scaling Law**：数据重复 4 轮后收益递减

---

## 4. RAG（检索增强生成）

### 定义

先从外部知识库检索相关信息，再结合这些信息一起生成回答，从而提升模型的准确性和知识时效性。

> 论文：[Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks](https://arxiv.org/abs/2005.11401) (2020)

### 要解决的问题

LLM 的知识局限于训练数据截止时间，无法访问实时信息、私有文档、数据库，且易产生幻觉。把模型训大到能记住一切成本太高。

### 实现原理

- **分块 + 嵌入**：文档切块 → 嵌入模型转为向量 → 存入向量数据库
- **检索**：用户 query 转为向量 → 相似度搜索（余弦/内积）→ 找到 top-k 最相关 chunk
- **重排序（Rerank）**：用 cross-encoder 对检索结果二次排序，提高相关性
- **生成**：检索结果 + query 拼入 prompt 喂给 LLM
- **进阶变体**：迭代检索（IRC）、自适应检索（判断是否需要检索）、HyDE（假设文档嵌入）、RAPTOR（层次摘要检索）

### 2025-2026 新进展

- **长上下文 + RAG 融合**：上下文窗口达 1M+ 后，RAG 可注入更多检索结果
- **Agentic RAG**：Agent 自主决定何时检索、检索什么、如何组合多源信息
- **MCP RAG Server**：通过 MCP 协议暴露 RAG 能力，跨框架复用

---

## 5. Function Calling（函数调用）

### 定义

Function Calling 是让大模型按约定格式输出调用指令，从而由外部系统真正去执行具体操作的一种机制。Function Calling 让模型从"只会说话"变为"会调用工具"。

> 官方指南：https://platform.openai.com/docs/guides/gpt/function-calling

### 要解决的问题

LLM 只能输出文本，无法直接影响外部世界。Function Calling 提供了一个结构化桥梁：模型输出 JSON 格式的函数调用（函数名+参数），由应用程序执行。

### 实现原理

- **函数声明**：在 API 请求中注册可用的函数列表（名称、描述、参数 JSON Schema）
- **模型决策**：LLM 根据用户意图和函数描述，决定是否需要调用函数
- **参数解析**：模型生成符合 Schema 的 JSON 参数
- **外部执行**：应用程序调用真实函数，将结果注入下一轮对话

### 2025-2026 新进展

- **BFCL（Berkeley Function Calling Leaderboard）**：标准化工具调用评测，GPT-4o 约 92%，Qwen2.5-72B 约 91%
- **并行调用**：一次请求调用多个函数
- **嵌套调用**：函数 A 的结果作为函数 B 的参数
- **Spring AI @Tool 注解**：Java 生态中通过注解声明工具函数

---

## 6. MCP（模型上下文协议）

### 定义

MCP（Model Context Protocol）是一种标准化协议，用来让大模型以统一的方式连接外部工具、数据源和服务，从而获取上下文信息并执行操作。MCP 最重要的贡献之一是使工具可以跨 AI 应用复用，推动社区生态发展。

> 官方文档：https://modelcontextprotocol.info/docs/introduction/

### 要解决的问题

在 MCP 出现之前，每个 Agent 框架各自对接工具（LangChain 有自己的工具、OpenAI 有 Plugin、Claude 有 Tool Use），开发者需要为每个平台重复实现。MCP 统一了接口标准——**工具开发者写一次，所有兼容框架都能用**。

### 实现原理

- **传输层**：基于 JSON-RPC 2.0，支持 stdio（本地进程通信）和 SSE（远程通信）
- **MCP Server**：声明提供的工具（名称、参数 Schema、描述）和资源
- **MCP Client**：Agent 框架作为客户端，发现工具并调用
- **调用流程**：LLM 输出函数调用 → MCP Client 解析 → 调用 MCP Server → 结果回注上下文
- **类比**：MCP 之于 AI 应用 = USB-C 之于硬件设备

### 三大原语

| 原语 | 说明 |
|---|---|
| **Tools** | 可执行的操作（API 调用、数据库查询） |
| **Resources** | 可读取的数据（文件、文档） |
| **Prompts** | 可复用的提示模板 |

### 2025-2026 新进展

- **A2A（Agent-to-Agent Protocol, Google）**：MCP 的补充，解决 Agent 之间互操作
- **MCP 生态成熟**：Postgres、Slack、GitHub、文件系统等官方 MCP Server 均已发布
- **Spring AI MCP**：Spring AI 已内置 MCP 客户端支持

---

## 7. Agent（智能体）

### 定义

Agent 是一种能够基于目标进行"思考-行动-观察"循环、能够自主调用工具来完成复杂任务的智能系统。Agent 本质上是对人类的模拟。「提示词 + LLM + Tools」就可以构成一个最简单的 Agent。

> 论文：[ReAct: Synergizing Reasoning and Acting in Language Models](https://arxiv.org/abs/2210.03629) (2022)
>
> 博客：https://tw93.fun/2026-03-21/agent.html

### 要解决的问题

单次 LLM 调用只能"回答问题"，无法完成多步骤任务（如"订机票+查天气+安排行程"）。Agent 的循环机制让模型能自主规划、执行、反思、迭代。

### 实现原理

- **Agent Loop（核心循环）**：
  ```
  思考（Think） → 行动（Act / 调用工具） → 观察（Observe 结果） → 再思考...
  ```
- **ReAct 范式**：推理和行动交替进行，每一步的观察结果影响下一步推理
- **记忆（Memory）**：对话历史、工具调用记录等持久化状态
- **规划（Planning）**：将复杂任务分解为子步骤

### Agent 发展史（5 阶段）

| 时期 | 范式 | 代表 |
|---|---|---|
| 符号规划时代（1990s–2010s） | BDI 架构 + 符号推理 | STRIPS, JACK |
| RL 时代（2010s） | 策略网络 + 环境交互 | AlphaGo, DQN |
| LLM 觉醒（2022-2023） | ReAct + 提示工程 | AutoGPT, LangChain, BabyAGI |
| 框架爆发（2024-2025） | 多 Agent + 结构化编排 | AutoGen, CrewAI, MetaGPT, LangGraph |
| 推理 Agent（2025-2026） | 内化推理 + MCP/A2A 协议 | Claude Agentic, OpenAI Agent SDK |

### Agent 设计模式

- **单一 Agent**：最简形式，一个 LLM + 工具集
- **路由 Agent**：根据任务类型分发给不同的处理模块
- **并行 Agent**：同时执行多个独立子任务
- **Supervisor Agent**：主 Agent 协调多个 Specialist Agent
- **层级 Agent**：多级管理，适用于复杂企业流程

### 2025-2026 新进展

- **推理模型即 Agent**：o1/R1 自带推理链，Agent 输出工具调用 JSON 成为自然行为
- **MCP + A2A 成基础设施**：标准化工具接入和 Agent 间通信
- **Agent 工程化**：安全沙箱、可观测性（LangSmith）、评测标准化
- **AgentBench 2.0 / SWE-bench / GAIA**：Agent 能力标准化评测

---

## 8. Multi-Agent（多智能体）

### 定义

由多个分工协作的 Agent 共同完成任务，通过拆分任务与隔离上下文解决单 Agent 系统难以处理的复杂问题。需要谨慎使用以避免 Token 消耗量大、协作效率低、系统复杂度过高等问题。

> 参考：https://claude.com/blog/building-multi-agent-systems-when-and-how-to-use-them

### 要解决的问题

单 Agent 在任务过复杂时会出现上下文超长、注意力分散、工具选择混乱等问题。多 Agent 通过"专人专事"和"隔离上下文"来规避这些问题。

### 实现原理

- **角色分工**：不同 Agent 扮演不同角色（研究员、分析员、写作者、审核员）
- **对话式协作**（AutoGen 模式）：Agent 之间通过对话协商
- **管道式编排**（CrewAI 模式）：上一个 Agent 的输出作为下一个的输入
- **主管-专家**：Supervisor 分解任务并分配给 Specialist，汇总结果

### 主流框架对比

| 框架 | 特色 | 适用场景 |
|---|---|---|
| **AutoGen**（微软） | 多 Agent 对话协商，互相质疑 | 复杂决策、辩论式推理 |
| **CrewAI** | 角色扮演，管道式编排 | 内容生成、报告撰写 |
| **MetaGPT** | 模拟软件公司（PM→架构→开发→测试） | 软件工程自动化 |
| **LangGraph** | 有状态图编排，支持循环/条件跳转 | 灵活定制的复杂工作流 |

### 2025-2026 新进展

- **CrewAI Enterprise**：管理多 Agent 团队、角色、权限
- **MetaGPT v2**：SWE-bench 达 45% 通过率
- **A2A 协议**：不同厂商的 Agent 可以互相调用

---

## 9. Context Engineering（上下文工程）

### 定义

Agent 运行中需要提供给 LLM 的一切相关信息（如对话历史、用户输入、背景知识、工具结果等）都是上下文。上下文工程关注如何高质量筛选、压缩和组织上下文，从而最大化模型决策与推理能力。

> 参考：
> - https://blog.langchain.com/context-engineering-for-agents/ (LangChain)
> - https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents (Anthropic)

### 要解决的问题

LLM 上下文窗口有限，Agent 在循环运行中积累的历史消息、工具结果、中间推理可能快速填满窗口。不加筛选地全量注入会导致"迷失在中间（Lost in the Middle）"问题——模型会忽略窗口中间的信息。

### 实现原理

- **上下文压缩**：对历史对话进行摘要，替换完整内容
- **上下文窗口管理**：滑动窗口策略——保留最近的 N 轮对话 + 关键信息的摘要
- **优先级排序**：重要信息（用户目标、关键工具结果）放在开头和结尾
- **渐进式披露**：只在需要时才加载特定上下文（按需而非全量）
- **缓存**：重复的工具结果或知识不重复注入

### 2025-2026 新进展

- **长上下文模型降低工程难度**：1M+ 上下文窗口让"塞得下"不再是问题
- **但"找得到"仍是问题**：即使窗口够大，模型仍倾向于关注首尾信息
- **SnapKV**：自动压缩 KV cache 保留关键信息，压缩比 4-8 倍

---

## 10. Agent Skill（智能体技能）

### 定义

Agent Skills 是一种轻量级的开放格式，用于将一整套 Agent 能力（prompt、工具脚本、知识文件等）封装为可复用模块，从而实现低门槛分享与复用。Agent Skill 本质上约等于一个子 Agent。Agent Skill 特别适合 SOP 的沉淀和复用（离职的同事终将化作温暖的 Skill）。Agent 会在运行过程中按需激活不同 Skills、按需读取和使用 Skills 文件包里的内容（**渐进式披露**）。

> 参考：
> - https://claude.com/blog/equipping-agents-for-the-real-world-with-agent-skills
> - https://agentskills.io/home

### 要解决的问题

Agent 系统里，每次构建特定能力（代码审查、数据库查询、邮件处理）都需要从零写 Prompt 和配置。Agent Skill 将能力封装为可复用的标准化模块，降低重复劳动，并实现"即插即用"。

### 实现原理

- **Skill 包**：包含 SKILL.md（元信息+触发条件+指令）+ 引用文件（模板、脚本、知识库）
- **渐进式披露**：Agent 先读 SKILL.md 标题和描述，决定是否激活；激活后才读完整内容
- **按需加载**：同一 Agent 可以装载多个 Skill，运行中根据上下文选择调用
- **Hermes Agent 实现**：这是我的本体机制——每个 Skill 是一个独立的知识模块

---

## 11. Harness Engineering（受控工程）

### 定义

Harness Engineering 强调通过构建受控环境，让 Agent 在约束下高效可靠地完成长周期复杂任务。包含围绕 Agent 构建约束机制、反馈回路、可靠上下文等的一系列工程实践。

> OpenAI 视角：https://openai.com/zh-Hans-CN/index/harness-engineering/

### 要解决的问题

Agent 在自由运行时容易跑偏：陷入死循环、偏离目标、调用错误工具、产生幻觉。需要一套工程实践来"约束"和"引导"Agent，确保可靠执行。

### 实现原理

- **约束机制**：工具权限隔离、Prompt 注入防御、步骤验证
- **反馈回路**：中间结果检查、错误恢复机制、超时处理
- **受控上下文**：上下文窗口管理、关键信息锚定
- **沙箱执行**：代码执行在隔离环境，不污染宿主系统

### 与评测 Harness（lm-eval）的区别

同一个词在不同语境下含义不同：

| 维度 | Harness Engineering（工程） | lm-evaluation-harness（评测） |
|---|---|---|
| 目的 | 让 Agent 可靠运行 | 评测 Agent 能力 |
| 视角 | 构建者 | 评估者 |
| 产出 | 稳定可部署的 Agent 系统 | 标准化分数和排行榜 |
| 例子 | 沙箱、权限控制、超时恢复 | MMLU、GSM8K、GAIA |

两者互补：先用工程实践造好 Agent，再用评测框架验证。

---

## 12. MoE（混合专家）

### 定义

混合专家（Mixture of Experts）将模型分为多个"专家"子网络，每次只激活少数专家（如 top-2），通过门控网络（Router）决定每个 token 被哪些专家处理。在总参数量巨大的情况下保持计算量可控。

### 要解决的问题

稠密 Transformer 的参数和计算量是线性绑定的。参数从 70B 涨到 700B，计算量也要翻 10 倍。没有那么多 GPU。

### 实现原理

- **稀疏激活**：N 个专家 FFN，每个 token 只经过 k（k<<N）个专家，其他不参与计算
- **门控网络（Router）**：输出概率分布，选择 top-k 个专家，加权合并输出
- **负载均衡**：通过辅助损失函数确保专家被均匀使用，避免"富者愈富"

### 代表模型

| 模型 | 总参数 | 激活参数 | 专家数 |
|---|---|---|---|
| Mixtral 8x7B | 47B | 13B | 8 专家，top-2 |
| DeepSeek-V3 | 671B | 37B | 256 专家，top-8 |
| DBRX | 132B | 36B | 16 专家，top-4 |

### 2025-2026 新进展

- **异步 MoE（DeepSeek V4）**：降低 all-to-all 通信开销，单机 8×H100 跑 1.5T 参数
- **分层 MoE（Mistral Large）**：粗粒度（语法/语义）→ 细粒度的两阶路由
- **单机 MoE 部署**：异步共享 expert + 量化，MoE 模型已可单机运行

---

## 13. 推理增强（Test-Time Compute）

### 定义

推理增强允许模型在推理时投入额外计算（生成更多推理步骤、搜索多条路径），在更困难的问题上获得"计算时间换准确率"的提升。代表模型：OpenAI o1/o3、DeepSeek R1/R2、QwQ。

### 要解决的问题

标准 LLM 生成每个 token 只做一次前向传播，一锤子买卖。遇到数学证明、多步逻辑这类需要"反复试错"的问题，一次过大概率错。

### 实现原理

- **RL 训练推理链**：用 GRPO 训练模型，奖励只看最终答案正确性，模型必须自己学会生成长推理链才能答对
- **MCTS（蒙特卡洛树搜索）**：生成潜在推理步骤 → 打分 → 扩展/回溯 → 最佳路径聚合。思路和 AlphaGo 一样
- **Test-Time Compute Scaling**：不改变模型参数，在推理时多花算力换更高准确率——**这是新的 Scaling Law**

### 关键模型对比

| 模型 | 开源 | 推理机制 | 特点 |
|---|---|---|---|
| OpenAI o1/o3 | ✗ | 内部 CoT RL | 数学/代码大幅领先 |
| DeepSeek R1/R2 | ✓ | GRPO 训练 | 纯 RL，开源推理标杆 |
| QwQ-32B | ✓ | RL + CoT | 32B 媲美 o1 |
| Claude 4 | ✗ | 自洽性重采样+奖励重排 | MATH-500 提升 15% |

---

## 14. 模型架构创新（Mamba / MTP / FlashAttention）

### Mamba / SSM（状态空间模型）

**要解决的问题**：Transformer 的 O(n²) 复杂度在超长序列（>100K）上扛不住，KV cache 也越吃越多。

**实现原理**：
- 结构化状态空间模型将序列建模为线性动态系统
- **选择性机制（核心创新）**：让状态转移矩阵根据输入内容动态变化，具备类似注意力的"内容感知"能力
- 训练可并行（O(n) 卷积），推理退化为递归（常数状态，不需要 KV cache）

**现状**：Mamba-4 做了 SSM + 局部自注意力混合架构，长序列上优于同规模 Transformer。但尚未完全取代 Transformer。

### Multi-Token Prediction（MTP）

**要解决的问题**：传统每次只预测下一个 token，信息利用率低（一次学一个耦合目标）。

**实现原理**：
- 在最后一层隐藏状态上接出多个独立的分类头，分别预测 t+1, t+2, ..., t+K 个 token
- 总损失 = 主任务（t+1） + 辅助任务加权和
- LLaMA 4 正式采用，推理吞吐提升 2 倍，代码/数学推理显著受益

### FlashAttention

**要解决的问题**：Attention 的计算瓶颈不在 FLOPs，在 **内存带宽**——Q/K/V 在 HBM 和 SRAM 之间频繁搬移比计算还慢。

**实现原理**：
- **分块（Tiling）**：把 Q/K/V 切块，每次只加载一小块到 SRAM，在片上完成部分计算
- **在线 softmax**：边算边维护局部最大值和指数和，不需要等完整矩阵
- **重计算**：反向传播不存完整 attention 矩阵，重新在片上算一遍
- FlashAttention-4 在 H100 上达 500 TFLOPS 利用率

### 推测解码（Speculative Decoding）

**要解决的问题**：自回归生成每一步串行，GPU 利用率极低（受限于内存带宽而非算力）。

**实现原理**：
- **草稿模型**（小模型）快速生成 K 个候选 token
- **目标大模型**一次前向传播并行验证所有候选
- **拒绝采样**检查一致性，不一致则中断重采
- 加速比通常 2-3 倍

---

## 附录 A：LLM 核心知识点体系

| 概念 | 阶段 | 说明 |
|---|---|---|
| 词嵌入 | 1-2 | 将离散词映射为稠密向量（Word2Vec, GloVe） |
| 注意力机制 | 2-3 | 计算序列元素间关联权重 |
| Transformer | 3 | 纯注意力架构，奠定所有现代 LLM 基础 |
| 预训练-微调 | 3 | 先用无监督语料训练，再对下游任务微调 |
| Scaling Law | 4 | 模型性能随参数、数据、计算量幂律提升 |
| In-Context Learning | 4 | 不更新权重，通过输入示例完成任务 |
| RLHF | 4 | 基于人类反馈的强化学习对齐模型行为 |
| MoE | 5 | 稀疏专家网络，提高参数量而不增加计算 |
| RAG | 5 | 检索外部知识库，减少事实错误 |
| DPO | 5 | 直接偏好优化，简化对齐训练流程 |
| 推理时扩展 | 6 | 推理阶段多花算力换更深推理链 |
| Agent | 6 | 模型与环境交互、调用工具、多步规划执行 |

## 附录 B：Agent 评测 Benchmark

| Benchmark | 测什么 | 被称为 | SOTA（2025-2026） |
|---|---|---|---|
| **GAIA** | 多步推理+工具调用 | Agent 界的 MMLU | GPT-4o + Agent ~50-70% |
| **SWE-bench** | 修真实 GitHub issue | Agent 界的 HumanEval | Claude 3.5 ~49% |
| **WebArena** | 浏览器操作 | Agent 界的驾考路试 | 专业 Agent ~45% |
| **BFCL** | 函数/工具调用精度 | Agent 界的语法考试 | GPT-4o ~92% |
| **AgentBench** | 综合（OS/Web/DB/游戏等） | Agent 界的综合卷 | GPT-4o ~65% |

---

## 相关笔记

- [[SpringAI+AIGC应用/SpringAI+AIGC应用总览|Spring AI + AIGC 应用总览]] — Spring AI 课程笔记入口
- [[SpringAI+AIGC应用/part1-认识AI & 大模型应用开发|part1-认识AI & 大模型应用开发]] — AI 基础、Transformer、Ollama
- [[SpringAI+AIGC应用/part3-SpringAI高级|part3-SpringAI高级]] — MCP 协议、Spring AI Alibaba
- [[SpringAI+AIGC应用/Ollama命令和API详解|Ollama命令和API详解]]
- [[💼 面试/AI面试题|AI面试题]] — Spring AI、RAG、MCP 面试考点
- [[📖 中州养老课程文档/文档/day6-智能评估-集成AI大模型|day6-智能评估-集成AI大模型]] — 中州养老 AI 集成案例
- [[MOC-编程相关|MOC-编程相关]]
- [[MOC-日常学习|MOC-日常学习]]
