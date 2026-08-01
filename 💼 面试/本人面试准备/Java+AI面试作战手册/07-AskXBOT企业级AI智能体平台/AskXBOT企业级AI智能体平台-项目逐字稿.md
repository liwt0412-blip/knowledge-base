---
title: AskXBOT企业级AI智能体平台-项目逐字稿
aliases:
  - AskXBOT项目逐字稿
  - Spring AI Alibaba智能体平台逐字稿
tags:
  - 面试准备
  - Java-AI
  - Spring-AI-Alibaba
  - 智能体
  - RAG
  - 逐字稿
status: draft
created: 2026-07-29
updated: 2026-07-29
architecture: Spring AI Alibaba落地方案
---

# AskXBOT 企业级 AI 智能体平台 项目逐字稿

> [!important] 口述定位
> AskXBOT 是本人参与落地的企业级 AI 智能体平台，官网为 [xbotspace.com](https://www.xbotspace.com)。本人只认领 Bot 对话与会话记忆、RAG 知识库与混合检索、Tool Calling 与 MCP 工具接入三个模块；其他模块按团队协作口径表述。

---

## 1、项目整体介绍

### 1.1、快速介绍版（开场用，45-60 秒，含技术演进线）

```text
我这几年的经历是一条从业务系统到 AI 平台的线。2023 到 2025 年我在石化经营分析平台做后端，那是 Spring Cloud Alibaba 微服务架构，后期我在平台上落地了 AI 智能助手：Java 侧接 Spring AI，查实时业务数据走 Function Calling，知识类问题转发给独立的 Python RAG 服务，回答用 SSE 流式返回。

那段落地经历让我看到一个共性问题：知识检索、工具调用、会话管理在每个项目里都各写各的，跨语言链路维护成本也高。所以 2025 年下半年到现在，我参与了 AskXBOT 这个企业级 AI 智能体开发平台，它做的就是把这类能力平台化：AI 核心链路用 Spring AI Alibaba 统一落地，支持 Bot 构建、RAG 知识库、会话记忆、Tool Calling 和 MCP 工具接入。

我负责三个模块：Bot 对话与会话记忆、RAG 知识库与混合检索、Tool Calling 与 MCP 工具接入。相比石化时期，RAG 从 Python 独立服务演进成 Java 侧向量加 BM25 双路召回混合检索，工具调用从硬编码 Function 演进成 @Tool、HTTP、MCP 三类工具统一治理。这三条链路您想深入哪一块都可以展开。
```

> 备考备注（不朗读）：
> - 时间线与简历一致：石化 2023.06-2025.06，AskXBOT 2025.07-至今，开场就把两个项目串起来，后续被追问哪个都能接。
> - 面试官顺着石化追问时，切到石化表述/逐字稿口径（AI 助手 + IoT 两模块）；顺着 AskXBOT 追问时，走本文件 1.2 详细版。
> - 当前口径是完成三个模块的设计与核心链路研究，真实实现范围以代码和测试为准；被追问实现深度时按事实核验表逐级升级，不主动交底。

### 1.2、详细介绍版（被追问负责模块时用，约 2 分钟）

```text
好的，我按我负责的三个模块分别展开。技术底座是 JDK 17、Spring Boot 3、Spring AI Alibaba，模型通过 DashScope 接入百炼上的 Qwen、DeepSeek 和 Embedding 模型，数据层是 MySQL、Redis、Milvus、Elasticsearch，异步入库用 RocketMQ，流式输出用 Spring WebFlux。

第一个模块是 Bot 对话与会话记忆。系统根据 Bot 配置选择 ChatModel，用 ChatClient 组装系统提示词、会话记忆、RAG Advisor 和工具。这里的一个关键设计是记忆与历史分离：MessageChatMemoryAdvisor 只负责最近会话窗口，控制上下文成本；完整聊天记录单独写 MySQL，用于展示、审计和上下文重建。用户提问后通过 stream API 获取 Flux，以 SSE 增量返回前端，阻塞调用会切到受控的 Scheduler，不占 EventLoop。

第二个模块是 RAG 知识库与混合检索。入库侧：文档上传后先写对象存储和任务表，RocketMQ 异步解析，TikaDocumentReader 读取、TokenTextSplitter 切片，Metadata 写入租户、版本和 ACL，Chunk 同时写入 Milvus 和 Elasticsearch。查询侧：向量召回和 BM25 并行执行，按 Chunk ID 去重后 RRF 融合，再经 Rerank 二次排序和权限过滤，最后由自定义 RetrievalAugmentationAdvisor 注入 Prompt。权限过滤前置到检索条件里，不是在生成后补救。单路超时自动降级到另一路，两路都失败就明确返回知识库不可用，不让模型自由编造。

第三个模块是 Tool Calling 与 MCP 工具接入。内部 Java 方法用 @Tool，动态 HTTP 接口按 JSON Schema 生成 ToolCallback，外部能力通过 Spring AI MCP Client 接入，三类工具统一成 ToolCallback。运行时按租户和 Bot 加载工具白名单，可信身份通过 ToolContext 由服务端注入，不信任模型生成的身份参数；写操作要求幂等键和人工确认，所有调用记录 traceId、耗时和结果用于审计。

整体看，这个方案的亮点不是堆框架，而是把记忆、检索、工具的责任边界分清楚，同时补上权限、幂等、降级和可观测性。
```

### 1.3、项目业务背景（素材块，追问"为什么做这个平台"时用）

```text
企业落地大模型时，真正的问题不是少一个聊天窗口，而是模型调用、企业知识和业务系统彼此割裂。

一方面，不同部门各自接模型，Prompt、会话上下文和日志重复建设；另一方面，企业制度、产品资料和客服文档没有进入模型上下文，回答容易产生幻觉；另外，大模型即使能回答，也不能安全地查询订单、创建工单或调用内部系统。

所以我们设计了一个企业级智能体平台：管理员创建 Bot，配置模型和 Prompt，绑定知识库以及 Tool/MCP 白名单；用户提问后，系统完成权限校验、会话记忆、知识检索和工具调用，再通过 SSE 返回答案、引用与工具状态，并把聊天历史和工具审计记录落库。
```

### 1.4、我的职责边界（素材块，追问"你具体负责什么"时用）

```text
我负责三个模块。

第一，Bot 对话与会话记忆；第二，RAG 知识库与混合检索；第三，Tool Calling 与 MCP 工具接入。

Agent Graph、平台级部署运维和其他管理功能属于项目整体或团队协作模块。我会讲清它们与我负责模块的接口，但不会说成由我负责实现。
```

---

## 2、架构与技术选型

### 2.1、为什么选 Spring AI Alibaba？

```text
第一，它建立在 Spring AI 的统一抽象之上，ChatModel、ChatClient、Advisor、VectorStore、ChatMemory 和 ToolCallback 可以直接融入 Spring Boot 工程。

第二，它对阿里云百炼和国内模型生态支持更直接，同时提供 Agent Framework 和 Graph，适合 Java 团队做工作流和多智能体。

第三，Spring 的依赖注入、配置管理、Actuator 和 Micrometer 能复用企业现有工程体系，不需要额外引入一套完全不同的运行时。
```

### 2.2、Spring AI 与 Spring AI Alibaba 的关系？

```text
Spring AI 提供通用抽象，例如 ChatModel、ChatClient、Advisor、Memory、VectorStore、Tool Calling 和 MCP。

Spring AI Alibaba 在此基础上增加 DashScope 模型适配，并提供面向 Agent、Graph、多智能体、Nacos 和国内生态的扩展。项目中通用 AI 调用遵循 Spring AI 抽象，复杂 Agent 编排使用 Spring AI Alibaba。
```

### 2.3、项目是微服务吗？

```text
第一阶段采用模块化单体。Bot、知识库、模型和工具关系紧密，先通过 application、domain、infrastructure 和 ai-adapter 做模块隔离。

文档解析、Embedding 和工作流执行属于资源模型不同的重任务，等压测证明需要独立扩缩容时再拆服务。这样避免为了微服务而微服务。
```

---

## 3、我负责的三个核心业务

### 3.1、Bot 对话与会话记忆

```text
业务背景：平台会有客服、销售、内部知识助手等多个 Bot，它们都需要模型调用和连续对话。如果每个 Bot 单独维护上下文，会出现重复开发、消息顺序混乱和历史记录不可追溯。

总体思路：我把 ChatClient 作为统一对话入口，通过 Advisor 链按需组合会话记忆、RAG 和审计。记忆和历史分离：框架只认 ChatMemory 接口，但企业要求完整记录落库可审计，所以我们用适配器模式实现了 BotMessageMemory，把 MySQL 消息表适配成框架的 ChatMemory，只给模型最近窗口；完整聊天记录由 ai_message 表承担，按 conversationId 加 sequenceNo 保序落库。

实现细节：请求进入后先校验租户、用户、Bot 和会话权限，根据 Bot 配置从 ChatModelRegistry 获取 ChatModel，再使用 MessageChatMemoryAdvisor 加载最近上下文。模型通过 stream 返回 Flux，服务端按 domain 加 type 的统一事件信封转成 SSE 推送；断流或失败也记录消息状态，阻塞的落库和外部 HTTP 调用切到受控 Scheduler，不占 EventLoop。

难点、优点和注意点：难点是消息保序、并发请求、流式中断以及 Memory 和 History 的边界。优点是不同 Bot 可以复用同一条对话链路并动态切换模型。注意不能把 Redis 当作唯一聊天记录，也不能宣称用了 Flux 就代表数据库和外部 HTTP 调用全部非阻塞。
```

### 3.2、RAG 知识库与混合检索

```text
业务背景：企业制度、产品手册和客服资料不会自动存在于大模型参数中，而且文档包含编号、型号、专有名词和访问权限，只做向量检索容易漏召回，直接把全文交给模型又会增加成本和幻觉。

总体思路：我设计了异步文档入库、Milvus 向量召回、Elasticsearch BM25 召回、结果融合、Rerank、ACL 过滤和引用返回的完整链路。检索引擎侧要解决两个问题：多知识库索引隔离、检索引擎可替换，所以我们用工厂模式实现 SearcherFactory，按知识库 ID 和配置创建检索器——每个知识库独立索引，ES 侧索引名按 rag_ 加知识库 ID 生成，引擎类型通过配置切换。

实现细节：上传文件先写对象存储和 ai_document_index_task 索引任务表，再通过 RocketMQ 异步解析。TikaDocumentReader 读取内容，TokenTextSplitter 切片，Metadata 写入 tenantId、knowledgeBaseId、documentVersionId 和 ACL。Chunk 同时写 Milvus 与 ES，文档状态走 UPLOADED 到 AVAILABLE 的状态机，双索引都成功才对外可见。查询时两路并发召回，按 Chunk ID 去重，RRF 或加权融合后调用 RerankService，最终由自定义 Advisor 注入 Prompt。

难点、优点和注意点：难点是 MySQL、Milvus、ES 多存储一致性，Embedding 模型升级以及效果、延迟、成本的平衡。优点是语义检索和精确词检索互补，检索索引可以重建。注意 ACL 应尽量在召回阶段过滤，Rerank 也要设置超时和降级，不能把自定义 RerankService 说成框架自动提供。
```

### 3.3、Tool Calling 与 MCP 工具接入

```text
业务背景：智能体如果只能回答问题，不能查询订单、创建工单或调用内部系统，业务价值有限；但模型直接调用任意接口又会带来越权、SSRF、重复写入和审计缺失。

总体思路：我把内部 Java 方法、动态 HTTP API 和外部 MCP 工具统一适配为 ToolCallback——这是适配器模式，解决的是新增一类工具来源时对话主链路、授权和审计零改动的问题——代码里对应 PluginTool 承接 HTTP 插件、McpTool 承接 MCP 协议，都收口到同一个工具接口，再按租户和 Bot 用 ai_bot_tool 白名单表控制可见工具，执行层统一处理参数校验、权限、幂等、超时与审计。

实现细节：稳定的内部能力使用 @Tool，租户自定义 HTTP 接口根据 JSON Schema 动态构建工具定义，MCP Server 通过 Spring AI MCP Client Starter 连接并转换为工具。可信的 tenantId、userId 和 traceId 通过 ToolContext 传入，不接受模型生成。写操作要求 idempotencyKey，高风险操作先返回确认事件，ai_tool_execution_log 记录工具、参数摘要、耗时、状态和错误码。

难点、优点和注意点：难点是工具协议统一、外部服务稳定性、重复调用和安全治理。优点是 Bot、Agent 和工作流都能复用同一套工具能力。注意密钥不能进入 Prompt，HTTP 工具必须限制协议、域名、端口和重定向，MCP 工具列表也需要缓存、健康检查和刷新机制。
```

---

## 4、Bot 对话主链路

### 4.1、用户发一个问题后发生什么？

```text
第一步，校验登录用户、租户、Bot、会话和资源权限。

第二步，根据 Bot 的 provider、modelName 和模型参数，从 ChatModelRegistry 获取 ChatModel，并构建 ChatClient。

第三步，加入 MessageChatMemoryAdvisor，从 ChatMemory 中读取最近会话窗口。

第四步，如果 Bot 绑定知识库，加入基础 QuestionAnswerAdvisor 或自定义 RetrievalAugmentationAdvisor。

第五步，根据 Bot 与工具的关联配置，通过 ToolCallbackResolver 得到本轮可见的 ToolCallback，同时由服务端通过 ToolContext 注入 tenantId、userId 和 traceId。

第六步，调用 ChatClient 的 stream API 获取 Flux，Controller 以 text/event-stream 返回。完整消息写入 MySQL，ChatMemory 只保存模型需要的上下文。
```

### 4.2、为什么使用 Advisor？

```text
Advisor 把横切能力从业务主流程中拆出来。会话记忆、RAG、日志、安全检查都可以独立实现，再按顺序组成调用链。

它类似责任链模式。顺序很重要，因为前一个 Advisor 修改后的上下文会交给下一个。例如先加载会话历史，再做问题检索，可能比只拿当前一句问题更准确。
```

### 4.3、为什么不直接调用 ChatModel？

```text
ChatModel 更底层，适合精确控制 Prompt 和用户控制的工具循环。ChatClient 在其上提供 Fluent API，能更方便地组合 Advisor、Memory、Options 和 Tools。

普通 Bot 对话优先 ChatClient；特殊工具循环或者 Graph 节点内需要更细控制时再使用 ChatModel。
```

### 4.4、多模型怎么切换？

```text
平台模型表保存 provider、modelName、endpoint、密钥引用和默认参数。ChatModelRegistry 根据 Bot 配置返回对应 ChatModel。

百炼模型使用 DashScope Starter，其他提供商使用 Spring AI 相应 Starter。上层只依赖 ChatModel 接口，不直接依赖具体 SDK。
```

---

## 5、会话记忆

### 5.1、ChatMemory 和 Chat History 有什么区别？

```text
ChatMemory 是模型本轮推理需要的有限上下文，重点是控制 Token 和保留重要信息；Chat History 是完整聊天记录，用于用户查看、审计和分析。

项目用 MessageWindowChatMemory 保存最近消息，通过 MessageChatMemoryAdvisor 自动带入 Prompt；完整历史写 MySQL。长会话使用最近窗口加历史摘要，不能把全部历史无限塞给模型。
```

### 5.2、为什么不用 Redis List 直接拼接？

```text
自己拼接也能实现，但 Spring AI 的 ChatMemory 和 Advisor 把存储策略、窗口策略和 Prompt 装配解耦，后续可以切换 JDBC、Redis 或自定义 Repository。

完整历史仍由业务表管理，因为 ChatMemory 不等于审计历史。
```

### 5.3、工具调用消息会自动存吗？

```text
不能想当然。Spring AI 官方文档提示，部分版本中工具调用中间消息不会自动写入 ChatMemory。

如果业务需要完整审计，我会在 ToolCallingManager 或工具执行监听器中记录 tool name、参数摘要、执行结果、耗时和错误，再按需要把关键结果写回记忆。
```

---

## 6、RAG 文档入库

### 6.1、文档如何变成可检索数据？

```text
用户上传文件后，接口先把原文件写 OSS 或 MinIO，并在 MySQL 建文档任务，状态为 UPLOADED。之后发送 RocketMQ 消息异步处理。

消费者使用 TikaDocumentReader 解析 PDF、Word 等文件，再用 TokenTextSplitter 切片。每个 Document 的 Metadata 包含 tenantId、collectionId、source、version 和 ACL。

然后调用 MilvusVectorStore.add 写向量索引，同时写 Elasticsearch BM25 索引。两边成功后，文档状态才改为 AVAILABLE。
```

### 6.2、为什么用异步任务？

```text
解析、Embedding 和索引写入都可能耗时或失败，不能让上传请求一直等待。MQ 可以解耦和削峰，上传接口只返回 taskId，前端查询处理状态。

MQ 不自动解决重复消费，消费端仍然使用 documentId 加 version 做幂等。
```

### 6.3、多存储一致性怎么保证？

```text
MySQL 是事实源，Milvus 和 ES 是可重建索引。文档有 UPLOADED、PARSING、INDEXING、AVAILABLE、FAILED、DELETING 等状态。

更新时先构建新版本索引，完成后切换可见版本；删除时先让文档不可见，再异步清理双索引和原文件。XXL-Job 定期扫描失败任务和索引差异。
```

### 6.4、Embedding 模型切换怎么办？

```text
不能只改模型名。不同 Embedding 模型的维度和向量空间不同。

我会新建 Milvus Collection，用新模型重建全部向量，完成离线验证或双读验证后切换知识库版本，最后再清理旧 Collection。
```

---

## 7、混合检索与 Rerank

### 7.1、完整检索流程是什么？

```text
收到问题后，可先做 Query 改写。然后使用独立线程池并行查询 Milvus 向量召回和 Elasticsearch BM25。

两路结果按 documentId 去重，使用 RRF 或归一化加权融合，再调用 RerankService 对候选集二次排序。之后做 ACL 校验、相似度过滤和 TopK 截断，组装成 Spring AI Document，由自定义 RetrievalAugmentationAdvisor 注入 Prompt。
```

### 7.2、为什么不只用 QuestionAnswerAdvisor？

```text
QuestionAnswerAdvisor 适合单 VectorStore 的基础 RAG。我们的场景还包含 ES 精确召回、Rerank、ACL、引用和降级，所以需要使用 RetrievalAugmentationAdvisor 的模块化思路，或者实现自定义 Advisor。
```

### 7.3、Rerank 是 Spring AI Alibaba 自动提供的吗？

```text
不能这样说。Spring AI Alibaba 为 Chat、Embedding、Advisor 和 VectorStore 提供核心支撑；项目把百炼或独立 Rerank API 封装成 RerankService，接在融合召回之后。这属于项目自己的检索编排。
```

### 7.4、RRF 和加权打分怎么选？

```text
向量分数和 BM25 分数尺度不同，没有做校准时，RRF 只看排名更稳健。如果有标注集并对分数做过归一化和验证，可以使用加权融合获得更细控制。
```

### 7.5、一路检索失败怎么办？

```text
Milvus 失败就使用 ES，ES 失败就使用 Milvus，Rerank 失败回退到融合排序。两路都失败时明确返回知识库不可用，不让模型基于常识自由回答。

每次降级都要记录 Trace 和指标，否则线上只看到回答质量波动却不知道原因。
```

### 7.6、如何评估效果？

```text
检索层看 Recall@K、MRR、NDCG 和无结果率；生成层看答案正确率、引用命中率和幻觉率；工程层看召回耗时、Rerank 耗时、首字延迟和成本。

没有评测集就不说准确率提升百分比。
```

---

## 8、Tool Calling

### 8.1、Spring AI 如何定义工具？

```text
固定业务方法可以用 @Tool 和 @ToolParam；动态工具实现 ToolCallback；需要根据名称动态选择时实现 ToolCallbackResolver；执行生命周期由 ToolCallingManager 管理。

ChatClient 把工具名称、描述和 JSON Schema 发给模型。模型返回工具名和参数后，ToolCallingManager 执行 ToolCallback，把结果返回模型，模型再生成最终答案。
```

### 8.2、ToolContext 有什么用？

```text
ToolContext 用来传递不应该由模型生成的服务端上下文，例如 tenantId、userId、权限范围和 traceId。

工具不能相信模型参数里的租户 ID，否则可能产生越权访问。
```

### 8.3、怎么防止重复执行写工具？

```text
写操作需要用户确认、服务端幂等键和业务层唯一约束。还要限制单轮工具次数、总耗时和并发。

不能因为模型只输出了一次 Tool Call 就认为网络重试、流重连或 Agent 循环不会重复执行。
```

### 8.4、HTTP 工具有哪些风险？

```text
主要风险是 SSRF、密钥泄漏、超时和超大响应。需要域名白名单、协议限制、内网 IP 拦截、连接与读取超时、响应体上限、敏感 Header 脱敏和审计。
```

---

## 9、MCP

### 9.1、MCP 如何接入？

```text
项目使用 Spring AI MCP Client Starter，通过配置建立 SYNC 或 ASYNC Client，可以连接 STDIO 或 SSE 类型的 MCP Server。

Starter 会把 MCP Server 暴露的工具适配成 ToolCallbackProvider。平台取得 ToolCallback 数组后，再根据 Bot 权限选择工具交给 ChatClient 或 Agent。
```

### 9.2、MCP 和普通 HTTP 插件有什么区别？

```text
MCP 提供标准的工具发现、Schema 和调用协议，适合已经支持 MCP 的工具服务；普通 HTTP 插件适合大量存量企业接口。

两者最终都适配成 ToolCallback，上层对话链路不感知具体接入协议。
```

### 9.3、MCP 生产化要注意什么？

```text
需要请求超时、健康检查、连接重建、工具列表刷新和 Bot 级授权。高风险工具仍要二次确认，不能因为使用标准协议就默认安全。
```

---

## 10、团队协作模块：Agent Framework 与 Graph

### 10.1、什么时候用 ReactAgent？

```text
当任务步骤不完全确定，需要模型根据当前状态自主选择工具时使用 ReactAgent，例如开放式资料研究。

如果只是固定问答加一次检索，ChatClient 加 Advisor 就够了，不需要强行上 Agent。
```

### 10.2、Graph 的核心概念是什么？

```text
StateGraph 定义整体流程；Node 是模型、工具或业务逻辑执行单元；Edge 定义固定或条件路由；OverAllState 在节点之间传递共享状态。

Graph Runtime 负责执行、流式事件、状态持久化和中断恢复。它适合流程可控、需要审计和人工确认的企业任务。
```

### 10.3、Agent 和 Graph 如何结合？

```text
让 Agent 负责理解意图和动态推理，让 Graph 负责流程边界和状态。

例如生成经营分析报告：Graph 先并行执行知识库检索和指标查询，再让报告 Agent 汇总，中间增加人工确认节点，最后调用文件生成工具。
```

### 10.4、为什么不让一个 Agent 包办？

```text
单 Agent 灵活，但调用路径、成本和结果不稳定。涉及写操作、审批或合规时，需要确定性流程、状态记录和人工确认点，所以用 Graph 约束。
```

---

## 11、SSE 流式输出

### 11.1、为什么用 WebFlux？

```text
Spring AI 流式调用返回 Reactor Flux。Controller 使用 text/event-stream，把模型增量实时推送给前端，用户能更早看到首字。

SSE 适合服务端单向推送；如果未来是实时双向语音，再考虑 WebSocket。
```

### 11.2、项目的事件协议是什么？

```text
统一使用 domain、type 和 payload。domain 区分 llm、tool、workflow 和 system；type 区分 message、thinking、tool_call、status、error 和 done。

前端不把业务语义写死在大量 SSE event name 中，便于未来扩展。
```

### 11.3、使用 Flux 就是全链路非阻塞吗？

```text
不是。MyBatis-Plus、JDBC 和部分工具是阻塞调用，如果直接跑在 Netty EventLoop 会拖慢其他请求。

这些调用要切到受控的 boundedElastic 或独立 Scheduler，并设置并发上限。只有经过实际链路检查和压测，才能说非阻塞改造完成。
```

### 11.4、客户端断开后怎么办？

```text
需要监听取消信号，尽量终止下游模型订阅和不必要的工具调用；同时记录会话状态。对于已经执行的写工具不能简单回滚，需要靠幂等和业务补偿处理。
```

---

## 12、权限和安全

### 12.1、知识库怎么防越权？

```text
把 tenantId、collectionId、departmentId 或 ACL 写进 Document Metadata。检索时在 Milvus 和 ES 中前置过滤，召回后、注入 Prompt 前再做一次业务权限校验。

不能先召回无权内容，再指望模型不泄漏。
```

### 12.2、模型密钥如何保护？

```text
数据库只保存加密后的密钥或密钥引用，接口返回时脱敏。日志不能打印完整 Prompt、Header 和密钥；生产环境优先接入密钥管理服务。
```

### 12.3、提示词注入怎么处理？

```text
外部文档只作为不可信数据上下文，不能把文档中的指令当系统指令执行。系统提示词明确指令优先级，工具权限由服务端控制，不由模型决定。

高风险动作增加确认节点，并对检索内容、工具参数和输出做审计。
```

---

## 13、异常、降级和可观测性

### 13.1、模型不可用怎么办？

```text
区分配置错误、限流、超时和供应商故障。配置错误不可重试；限流和临时超时有限次数退避重试；必要时按业务允许范围切换备用模型。

SSE 已经开始后通过 error 事件通知前端并结束流。
```

### 13.2、需要监控哪些指标？

```text
模型侧看请求量、首字延迟、完整延迟、Token、错误率和费用；RAG 看各路召回耗时、候选数、Rerank 耗时和空召回率；工具看调用次数、耗时、失败率和重复调用；工作流看节点耗时、中断数和恢复失败数。

通过 Micrometer、Prometheus 和 Grafana 建立指标，Trace 中串联 conversationId、requestId 和 toolCallId。
```

### 13.3、能不能记录完整 Prompt？

```text
调试环境可以受控开启，生产环境默认不能全量记录，因为里面可能包含用户隐私、企业文档和工具结果。应该脱敏、采样并设置访问权限和保留周期。
```

---

## 14、你负责模块的表结构是怎么设计的？

我没有按页面功能堆表，而是先区分配置态、运行态和检索投影。

Bot 和会话模块以 `ai_bot` 为配置中心，通过 `ai_bot_model` 配置主模型和降级模型；`ai_conversation` 保存会话元数据，`ai_message` 保存完整消息历史，并使用会话内的 `sequence_no` 保证稳定排序。Spring AI 的 `ChatMemory` 只保存模型当前需要的有限上下文，不能替代消息历史表。

RAG 模块把 `ai_document`、`ai_document_version` 和 `ai_document_chunk` 分开。文档重新上传或重新切片时创建新版本，旧会话引用的版本仍然可追溯。MySQL 保存文档、版本、切片元数据和索引任务状态；Milvus 保存向量，Elasticsearch 保存 BM25 检索字段，它们都是可以由 MySQL 事实数据重建的检索投影。

Tool 和 MCP 模块通过 `ai_bot_tool`、`ai_bot_mcp_tool` 做 Bot 级白名单授权，`ai_tool_execution_log` 记录调用参数摘要、耗时、结果、错误和 traceId。对于写操作，调用方必须传 `idempotencyKey`，数据库以租户和幂等键做唯一约束，避免模型重试造成重复扣减或重复创建。

项目的工作流表属于团队协作模块。我只说明与本人模块的边界：工作流能够调用经过 Bot 授权的 Tool/MCP，并复用工具执行审计；工作流定义、版本和实例表不表述为由我负责。

跨模块使用 `ai_bot_knowledge_base` 和 `ai_bot_workflow` 做绑定，异步索引、审计等场景用 `ai_outbox_event` 保证业务数据和消息投递最终一致。详细字段和索引见 [[AskXBOT企业级AI智能体平台-核心表结构设计]]。

---

## 15、微服务和模块边界怎么设计？

```text
第一阶段采用模块化单体，不为了简历好看直接拆微服务。Bot、知识库和工具之间的配置关系紧密，先在 application、domain、infrastructure 和 ai-adapter 层做清晰隔离。

出现独立扩缩容和故障隔离需求后，可以拆成 ai-chat-service、knowledge-service、document-index-worker 和 tool-integration-service。Chat 服务拥有 Bot、会话和消息表；Knowledge 服务拥有知识库、文档和 Chunk 元数据；索引 Worker 消费 RocketMQ 任务并写 Milvus、ES；Tool 服务拥有工具注册、授权和执行日志。团队的 workflow-service 只通过 API 或事件调用已授权工具。

拆分原则是服务拥有自己的数据，禁止跨服务直接连表。文档入库使用任务表或 Outbox 配合 MQ 保证最终一致性；用户对话这种同步链路不为了微服务而强行经过 MQ。
```

---

## 16、竞品有哪些？项目差异在哪里？

```text
我主要对比 Dify、FastGPT 和 RAGFlow。

Dify 的优势是通用低代码平台、工作流和插件生态比较完整，并且有云服务和企业自托管方案。FastGPT 在中文知识库问答、可视化工作流和私有化交付方面更突出。RAGFlow 更强调深度文档解析、混合检索、Rerank 和面向 Agent 的上下文层。

我们的设计不宣称功能数量或生态规模超过它们。差异化目标是面向已有 Java 和 Spring 技术体系的企业，用 Spring AI Alibaba 接入国内模型，并复用企业现有的账号、权限、Nacos、RocketMQ、监控和内部业务接口。我的三个模块重点补齐会话可追溯、知识权限隔离、Tool/MCP 授权、幂等和审计。
```

官方参考：[Dify Enterprise](https://dify.ai/zh/pricing/dify-enterprise)、[FastGPT 商业版](https://doc.fastgpt.cn/zh-CN/guide/version/commercial)、[RAGFlow](https://ragflow.io/)。

---

## 17、项目靠什么盈利？

```text
这个项目适合采用开源或社区能力获客，再通过企业级服务变现。

第一类收入是 SaaS 订阅，按团队席位、Bot 数、知识库容量、调用额度和高级治理能力分档收费。第二类是模型、Embedding、Rerank 和向量存储等资源用量服务费。第三类是私有化部署和商业授权，为数据敏感客户提供本地部署、SSO、审计、高可用和升级维护。第四类是企业定制和系统集成，例如接入 OA、CRM、ERP、LDAP 和内部模型。第五类是培训、技术支持和 SLA 服务。

商业闭环是社区版降低试用门槛，SaaS 帮客户验证场景，真正有数据安全、权限治理和内部系统接入要求的客户再升级到私有化部署和定制服务。

这只是项目商业模式设计，不能说成已经产生真实收入或拥有付费客户。
```

---

## 18、项目难点回答

### 难点一：把 AI 能力放进统一工程模型

```text
我用 ChatClient 作为调用入口，用 Advisor 组合记忆和 RAG，用 ToolCallback 统一业务工具和 MCP，避免每个 Bot 各写一套模型逻辑。
```

### 难点二：RAG 效果、延迟和权限同时满足

```text
向量和 BM25 提高覆盖率，Rerank 提高排序质量，但会增加延迟。因此使用并行召回、融合、超时降级和候选数控制，同时把 ACL 前置到检索阶段。
```

### 难点三：Tool/MCP 灵活性与企业安全冲突

```text
模型需要动态选择工具，但企业又要求权限可控、写操作不能重复、外部地址不能任意访问。我通过 Bot 工具白名单、ToolContext 可信身份、幂等键、HTTP 地址限制、高风险确认和执行审计，在扩展性与安全之间做平衡。
```

---

## 19、如果让我继续实施

```text
第一步，梳理本人负责模块的代码与版本基线，锁定 BOM 和 Starter 版本，复核 DashScope Chat、Embedding、Memory、Tool Calling 和 SSE 主链路。

第二步，建立小型公开知识库，跑通 Tika 解析、Token 切片、Milvus、ES 和 Rerank，并准备 30 到 50 个标注问题形成基线。

第三步，实现一个内部 @Tool、一个动态 HTTP ToolCallback 和一个 MCP 工具，验证 Bot 白名单、ToolContext、幂等、超时和高风险确认。

第四步，补幂等、降级、权限和可观测性，并以 Git 提交、测试报告、评测结果和运行截图升级面试口径。
```

---

## 20、面试红线问答

### Q：AskXBOT 是你真实参与的项目吗？

```text
是，AskXBOT 是我参与落地的企业级 AI 智能体项目。我的职责集中在 Bot 对话与会话记忆、RAG 知识库与混合检索、Tool Calling 与 MCP 工具接入，其他模块按团队协作边界说明。
```

### Q：你具体完成到什么程度？

```text
我会按三个负责模块分别说明完成内容，并用对应代码、Git 提交、接口文档、测试结果和运行记录支撑。没有证据的数据、性能指标或团队模块，不表述为本人独立完成。
```

### Q：你具体负责哪些模块？

```text
我负责三个模块：Bot 对话与会话记忆、RAG 知识库与混合检索、Tool Calling 与 MCP 工具接入。Agent Graph、平台部署和运维属于项目整体或团队协作范围，我只讲与本人模块的接口边界。
```

### Q：为什么这仍然值得讲？

```text
因为我不是只背框架名，而是能把 ChatClient、Advisor、Memory、RAG、Tool、MCP、Agent 和 Graph 映射到完整业务链路，并说明权限、一致性、阻塞边界和降级。下一步会用真实实现把设计口径升级为项目事实。
```

---

## 21、口述练习清单

- [ ] 能讲清 Spring AI 与 Spring AI Alibaba 的关系；
- [ ] 能讲清 ChatClient、Advisor、ChatMemory 和 ToolCallback；
- [ ] 能画出文档入库与混合检索链路；
- [ ] 能解释 RRF、Rerank、ACL 和单路降级；
- [ ] 能解释 ToolContext 与工具幂等；
- [ ] 能解释 MCP 如何变成 ToolCallback；
- [ ] 能说明 Agent Graph 是团队协作模块，以及它如何调用本人负责的 Tool/MCP；
- [ ] 能解释 Flux 不等于全链路非阻塞；
- [ ] 始终把本人职责限定在三个明确负责模块；
- [ ] 不说无证据的准确率、并发量和上线规模。

---

## 关联文档

- [[AskXBOT企业级AI智能体平台-项目表述]]
- [[AskXBOT企业级AI智能体平台-核心表结构设计]]
- [[AskXBOT-设计模式面试锚点]]
- [[SpringAI+AIGC应用/SpringAI+AIGC应用总览]]
- [[邻圈同城社交-项目逐字稿]]

