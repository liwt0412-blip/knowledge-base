---
title: AskXBOT-设计模式面试锚点
aliases:
  - AskXBOT设计模式
tags:
  - 面试准备
  - Java-AI
  - 设计模式
  - AskXBOT
status: active
created: 2026-07-31
updated: 2026-07-31
---

# AskXBOT 设计模式面试锚点

> 用途：被问"项目用了什么设计模式"时的答题底稿。只收录**真实代码可指认、抗追问**的模式用法。
> 代码锚点来自 `D:\workspece\GitHup\AIflowy\aiflowy`（AgentFlex 实现，与 AskXBOT 口径结构同构）；面试口径统一用 Spring AI Alibaba 术语表述（ToolCallback ≈ BaseTool，Advisor ≈ listener 链）。
> 规则来源：[[☕ Java笔记/设计模式适配-问题识别信号与项目锚点]]；职责边界遵守 [[AskXBOT企业级AI智能体平台-项目逐字稿]] §20 红线。

---

## 答题总叙事（被问"用了什么设计模式"时的推荐顺序）

1. **先讲两个适配器**：工具四形态统一 + ChatMemory 落地 MySQL——有代码、有动机、有"不用会怎样"；
2. **再讲一组工厂+策略**：SearcherFactory、LlmProvider、模型多态转换——强调"按配置/按类型选实现"，并主动说明选型时区分了枚举多态 vs 注册表形态；
3. **最后反向讲一个"故意不用"**：文档状态机不抽象成状态模式——展示反过度设计意识。

结构记忆：**两个适配器 + 一组工厂策略 + 一个知情不抽**。比平铺模式名词更抗追问。

---

## 一、Tool Calling 与 MCP 工具接入（模式密度最高，主讲）

### 1. 适配器模式 ★最强锚点

- **动机**：MCP 协议、HTTP 插件、内部工作流、知识库检索四种调用形态完全不同，对话主链路不能为每种来源写一套接入代码。
- **代码锚点**：`agentsflex/tool/` 下 `McpTool`、`PluginTool`、`WorkflowTool`、`DocumentCollectionTool` 全部 `extends BaseTool`，统一成框架工具接口（Spring AI 口径即统一为 `ToolCallback`）。
- **面试话术**：适配器模式的价值不是统一接口本身，而是新增一种工具来源时，对话主链路、Bot 白名单授权、审计日志零改动——这是开闭原则的落点。
- **不用会怎样**：每接一类工具就要改对话编排、权限校验和审计三处，工具类型一多主链路全是 if/else。

### 2. 建造者/工厂（动态工具构建）

- **动机**：租户自定义 HTTP 接口不是编译期存在的 Java 方法，工具定义要运行时从配置生成。
- **代码锚点**：`PluginTool` 从 `PluginItem` 的 JSON Schema（`inputData`）动态生成 `Parameter[]`（`getDefaultParameters`），运行时才组装出工具的名称、描述和参数 Schema。
- **面试话术**：静态能力用注解声明（Spring AI 口径 `@Tool`），动态能力按 JSON Schema 运行时构建 ToolCallback——这是两类工具的关键分界，也是"HTTP 接口怎么变成模型的 function 定义"的答案。

### 3. 工厂方法 + 策略（模型多态）

- **动机**：平台接多家模型供应商，上层业务不能依赖具体 SDK。
- **代码锚点**：`tinyflow/llm/LlmProviderImpl.getChatModel(modelId)` 按模型配置实例化对应 `Llm`；`Model.toChatModel() / toEmbeddingModel() / toRerankModel()` 按 provider 多态转换（`ModelServiceImpl` 中三种模型分别走校验）。
- **面试话术**：对应口径里的 ChatModelRegistry——上层只依赖 ChatModel/EmbeddingModel 抽象，切换 provider 不改调用方。

---

## 二、RAG 知识库与混合检索

### 1. 简单工厂

- **代码锚点**：`config/SearcherFactory.getSearcher(collectionId)`：按配置类型（lucene/elasticSearch）+ 知识库 ID 动态构建检索器实例，每个知识库独立索引目录/索引名（ES 用 `rag_{collectionId}`，Lucene 用独立目录）。
- **面试追问点**：同时回答"多知识库索引怎么隔离"。

### 2. 策略模式（配置路由形态）

- **代码锚点**：`DocumentSearcher` 统一抽象，Lucene/ES 两个实现，按 `rag.searcher.type` 配置切换。
- **面试话术（主动加分）**：按 [[☕ Java笔记/设计模式适配-问题识别信号与项目锚点]] 的三形态判别——类型集合封闭（就两个检索引擎）、实现是配置驱动而非按参数 new，所以选"配置选择/工厂"形态而**不是**注解注册表；主动说出为什么没用注册表，比只报名字更可信。

### 3. 状态机：知情不抽象（反向加分点）

- **代码锚点**：文档生命周期 `UPLOADED → PARSING → INDEXING → AVAILABLE / FAILED / DELETING`（逐字稿 §6.3），用枚举字段 + 状态校验实现。
- **面试话术**：被问"为什么不用状态模式"时答——迁移规则就几条 if，引入状态类体系是负收益，属于知情不抽。能讲清"什么时候不用模式"比硬套模式更能体现工程判断。

### 4. 观察者/事件驱动 + Outbox

- **动机**：解析、Embedding、索引写入耗时不确定，不能阻塞上传接口；业务落库与消息投递要最终一致。
- **代码锚点/口径**：RocketMQ 异步入库，`ai_outbox_event` 保证最终一致；消费端按 文档ID+版本 幂等。
- ETL 三段式（DocumentReader → Transformer → Writer）是框架的模板方法骨架，属于**框架既有设计**，讲时归框架。

---

## 三、Bot 对话与会话记忆

### 1. 适配器模式（第二个锚点）

- **动机**：框架只认 ChatMemory 接口，但企业要求完整聊天记录落 MySQL 可审计。
- **代码锚点**：`agentsflex/memory/BotMessageMemory implements ChatMemory`：`getMessages(count)` 查 `BotMessage` 表最近 N 条反序拼装成框架 Message；`addMessage` 回写业务表。另有 `DefaultBotMessageMemory` / `PublicBotMessageMemory` 两个变体，按 Bot 可见范围策略选择。
- **面试话术**：这就是"Memory 与 History 分离"口径的代码载体——存储策略是我们的实现，框架只依赖接口；ChatMemory 承担上下文窗口，MySQL 承担完整历史，两者职责不同。

### 2. 责任链 ⚠️ 口径红线：框架既有

- **事实**：Advisor 链（Spring AI）/ listener 链（AgentFlex）是框架提供的机制；**自有贡献是自定义节点**（混合检索 RetrievalAugmentationAdvisor、ACL 过滤、审计），不是链本身。
- **红线**：被问"这是你的设计吗"必须区分"框架的链 vs 我写的节点"，不冒领。逐字稿 §4.2"它类似责任链模式"的表述保持。

---

## 四、反过度设计自检（沿用通用红线）

被追问"为什么这里不用 XX 模式"时的通用防线（详见 [[☕ Java笔记/设计模式适配-问题识别信号与项目锚点]] §二）：

1. 能直写不抽象——没有第二个调用方的"通用方法"不抽；
2. 同一形态出现第二次才抽取；
3. 模式是结果不是目标——"这里有分支发散问题，策略能收拢"，不是"找个地方塞模式"；
4. 框架已有的不重复造、不冒领（责任链、ETL 骨架、Spring 单例均归框架）。

---

## 关联文档

- [[AskXBOT企业级AI智能体平台-项目逐字稿]]
- [[AskXBOT企业级AI智能体平台-项目表述]]
- [[☕ Java笔记/设计模式适配-问题识别信号与项目锚点]]
- [[00-我的长期上下文]] §2 设计模式主动适配规则
