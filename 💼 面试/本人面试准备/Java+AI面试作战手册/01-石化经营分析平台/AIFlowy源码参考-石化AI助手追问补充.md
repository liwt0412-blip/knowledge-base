---
tags:
  - 面试
  - 石化项目
  - AI助手
  - AIFlowy
  - JavaAI
  - 源码参考
  - 追问补充
status: draft
priority: P1
created: 2026-07-11
---

# AIFlowy源码参考-石化AI助手追问补充

> 用途：应对面试官追问 AI 助手工程细节时使用。  
> 定位：AIFlowy 是外部开源项目源码参考，用来补强理解和表达，不是石化项目事实。  
> 红线：不能说 AIFlowy 是我参与开发的项目；不能把 AIFlowy 的完整能力说成石化项目已经落地。

---

## 0. 一句话口径

如果面试官追问“你对企业级 AI 助手平台的理解是不是只停留在调用模型 API”，可以这样答：

> 石化项目里的 AI 助手不是完整的 Dify/Coze/AIFlowy 平台，它更偏企业业务系统中的智能助手模块。我主要做的是把集团 AI 底座接入省公司 Java 业务系统，重点在会话隔离、权限透传、Function Calling、RAG 联调、缓存和 SSE 流式输出。后面我也研究过 AIFlowy 这类 Java AI Agent 平台，对 Bot 配置、知识库分层、MCP 工具绑定和 Workflow 编排有了更系统的理解。

---

## 1. AIFlowy 对石化 AI 助手的参考价值

AIFlowy 参考项目路径：

```text
D:\workspece\GitHup\AIflowy\aiflowy
```

AIFlowy 是基于 Java 的企业级 AI 智能体开发平台，包含：

- Bot 构建与发布。
- RAG 知识库。
- AI Workflow 编排。
- 插件系统。
- MCP 接入和 Bot 绑定。
- 模型管理。
- API Key。
- 用户、角色、权限、日志、定时任务等后台能力。

对石化 AI 助手的价值不是“搬功能”，而是提供工程化参照：

```text
Bot 配置怎么管理
模型配置怎么解耦
conversationId 怎么做会话隔离
SSE 流式输出怎么组织
知识库 collection / document / chunk 怎么分层
工具/MCP 怎么注册和绑定到 Bot
Workflow 为什么要异步执行和查询状态
企业 AI 平台为什么还需要权限、API Key、日志和后台管理
```

---

## 2. 已落地 / 可借鉴 / 明确没做

### 2.1 石化 AI 助手已落地或可稳妥讲

- Java 作为 AI 助手业务入口。
- 登录态、用户上下文和权限透传。
- Redis 缓存高频问答或工具结果。
- Spring AI Function Calling 调用 Java 业务函数。
- Python RAG 服务负责文档处理、Embedding、Milvus 检索、Reranker。
- SSE 流式输出。
- conversationId 隔离会话。
- 会话历史落库或持久化保存。
- 低相关性兜底，不强行回答。

### 2.2 可以作为优化方向讲

- Bot 配置、模型配置、知识库配置进一步解耦。
- 不同助手绑定不同知识库和工具集。
- 工具注册、工具描述、参数 schema、权限校验、助手绑定关系平台化。
- 知识库按 collection / document / chunk 分层管理。
- 引入工作流编排来支持跨系统任务、人工确认、异步执行和状态查询。
- 后台增加 API Key、操作日志、模型调用日志、用量统计和效果反馈。

### 2.3 明确不要说成石化项目已做

- 完整 Dify/Coze/AIFlowy 级低代码平台。
- 完整 MCP 平台作为生产主链路。
- 可视化 Workflow 编排已经大规模落地。
- 多模型统一平台全部由我设计。
- 插件市场或完整插件生态。
- AIFlowy 源码是我参与开发的。

---

## 3. Bot 配置与模型配置解耦

AIFlowy 参考点：

- `BotController`
- `ModelController`
- `ModelProviderController`
- `BotModelController`

### 面试官可能问

> 你们 AI 助手的模型配置是写死在代码里的吗？

### 稳妥回答

> 正式生产里不建议把模型、提示词、知识库和工具都写死在代码里。更合理的是把助手配置、模型配置、知识库配置和工具配置拆开。石化项目里我主要负责业务侧接入和关键链路实现，比如工具封装、RAG 联调、缓存、会话、SSE。后续如果做成更平台化的 AI 助手，可以参考 AIFlowy 这种 Bot + Model + Knowledge + Tool 的配置结构。

### 可追问展开

- Bot：保存助手名称、提示词、绑定模型、绑定知识库、绑定工具。
- Model：保存模型提供商、模型名、温度、TopP、最大输出长度等。
- Knowledge：保存业务知识库范围。
- Tool：保存工具描述、参数 schema 和权限边界。

回答重点：

> 配置解耦的价值是不同业务助手可以复用同一套底层能力，而不是每加一个助手就改代码。

---

## 4. conversationId 是会话隔离核心

AIFlowy 参考点：

- `BotController.generateConversationId`
- `BotController.chat`
- `BotConversation`
- `BotMessage`

### 面试官可能问

> 多轮对话怎么保证不串上下文？

### 稳妥回答

> 多轮对话一定要显式传 conversationId。用户每打开一个会话窗口，后端生成一个唯一 conversationId，后续所有消息、缓存、会话历史和流式输出都围绕这个 ID 关联。不能只靠用户 ID，因为同一个用户可能同时打开多个窗口；也不能只靠模型自己记忆，因为服务端要能审计和恢复上下文。

### 可追问展开

```text
userId         -> 谁在问
conversationId -> 哪个会话
messageId      -> 哪条消息
botId          -> 哪个助手
```

设计原则：

- `userId` 用于权限和数据范围。
- `conversationId` 用于隔离多轮上下文。
- `messageId` 用于消息追踪和失败重试。
- `botId` 用于区分不同助手配置。

和石化项目结合：

> Spring AI 使用 ChatMemory 或 Advisor 时，如果不显式传 conversationId，不同用户、不同窗口的上下文可能串在一起。入口层必须生成并透传 conversationId。

---

## 5. SSE 流式输出怎么回答

AIFlowy 参考点：

- `BotController.chat`
- `SseEmitter`
- `ChatSseEmitter`
- `ChatSseUtil`

### 面试官可能问

> AI 回答为什么要用 SSE？怎么处理连接中断？

### 稳妥回答

> AI 生成回答时间比较长，如果等完整结果再返回，用户体验会很差。SSE 可以让模型边生成边返回，前端逐步展示。后端要做的是创建 SseEmitter，把模型 token 或片段持续推给前端，同时处理超时、异常和用户中断。

### 可追问展开

- 建立 SSE 连接。
- 调用模型流式接口。
- 每收到一个片段就推送给前端。
- 完成后发送结束事件。
- 异常时发送错误事件并关闭连接。
- 重要消息可落库，方便刷新或追溯。

注意不要说：

> SSE 能保证一定不断。

更稳说法：

> SSE 只是流式传输方式，网络断开、浏览器刷新、服务端异常都可能中断，所以要有超时、异常关闭和必要的会话历史保存。

---

## 6. 知识库 collection / document / chunk 分层

AIFlowy 参考点：

- `DocumentCollectionController`
- `DocumentController`
- `DocumentChunkController`
- `VectorDatabaseController`
- `DocumentCollection`
- `Document`
- `DocumentChunk`

### 面试官可能问

> 你们知识库怎么管理？是不是直接把文件切块入向量库？

### 稳妥回答

> 不能只把文件切块丢进向量库。更合理的结构是知识库、文档、chunk 三层。知识库对应业务域或助手范围，文档保留文件来源、版本、权限和状态，chunk 才是最终参与检索的最小片段。

### 三层解释

| 层级 | 作用 | 面试讲法 |
|---|---|---|
| Collection | 业务域或知识库范围 | 比如操作手册、安全规范、运维案例可以分不同集合 |
| Document | 原始文档和版本来源 | 记录文件名、上传人、更新时间、权限、是否启用 |
| Chunk | 检索粒度 | 控制 embedding、召回、rerank 和上下文拼接 |

### 对常见追问的帮助

#### chunk size 为什么这么设？

> chunk 不是越大越好，也不是越小越好。小 chunk 召回更精确，但容易丢上下文；大 chunk 上下文完整，但噪声更多。更合理的是子块用于检索，父块用于生成，或者根据文档标题、段落、表格结构做切分。

#### 文档更新后旧向量怎么处理？

> 文档更新时不能只追加新 chunk。要能根据 documentId 或 version 找到旧 chunk，标记失效或删除，再写入新 chunk。线上为了安全，也可以先新版本入库，验证后切换生效状态。

#### 权限过滤怎么做？

> 权限不能等模型生成后再过滤。文档或 chunk 入库时就要带组织、角色、业务域、状态等元数据；检索时带上当前用户权限范围，只召回用户能看的内容。

---

## 7. 工具注册、Function Calling 与 MCP 绑定

AIFlowy 参考点：

- `PluginController`
- `PluginItemController`
- `McpController`
- `BotMcpController`
- `BotPluginController`
- `McpService`

### 面试官可能问

> Function Calling 是不是在 Prompt 里写几个函数名就行？

### 稳妥回答

> 不能只靠 Prompt。工具调用要工程化管理，至少包括工具注册、工具描述、参数 schema、后端校验、权限过滤和助手绑定关系。模型只负责理解意图和生成参数，真正能不能查、查哪些数据，必须由后端决定。

### 工具调用分层

```text
工具注册
  -> 工具描述 / 参数 schema
  -> Bot 绑定可用工具
  -> 模型选择工具并生成参数
  -> 后端参数校验
  -> 后端权限校验
  -> 执行业务查询
  -> 结果脱敏和结构化返回
```

### 石化项目落地讲法

> 比如 `getDeviceStatus`、`queryAlarmList`、`queryCustomerSummary` 这些工具，不是模型想调就能调。后端会校验 stationCode、deviceId、时间范围，再根据当前用户组织和油站权限拼接查询条件。AI 只负责选择工具，权限边界永远在后端。

### MCP 口径

不要主动说 MCP 是石化当前生产主链路。

可以说：

> 石化项目当前主要是 Spring AI Function Calling。MCP 我理解成更标准化的工具接入协议，类似把外部工具服务统一暴露给模型。后续如果工具越来越多，可以考虑 MCP 化，便于工具发现、注册和跨系统复用。

---

## 8. Workflow 异步编排

AIFlowy 参考点：

- `WorkflowController.runAsync`
- `WorkflowController.getChainStatus`
- `WorkflowController.resume`
- `WorkflowController.singleRun`
- `WorkflowExecResult`
- `WorkflowExecStep`

### 面试官可能问

> 你这个 AI 助手能不能执行复杂业务流程？

### 稳妥回答

> 当前石化 AI 助手主要定位是问答和工具调用，不是完整低代码工作流平台。它可以查设备、查告警、查客户概览，也可以基于知识库回答制度和操作问题。但如果后续要做跨系统审批、巡检任务自动化、异常处理闭环，就需要引入 workflow 编排能力。

### Workflow 为什么要异步

复杂流程可能包括：

- 多个工具调用。
- 条件分支。
- 人工确认。
- 等待外部系统返回。
- 失败重试。
- 执行状态展示。

所以不能只用同步接口：

```text
runAsync      -> 启动执行
getStatus     -> 查询状态
resume        -> 人工确认后继续
singleRun     -> 单节点测试
execStep      -> 记录每一步结果
```

### 可作为后续演进方向

> 如果后续做智能巡检助手，可以让 AI 先识别异常，再查询设备状态，再生成处理建议，必要时创建工单或等待人工确认。这种就不适合一次同步调用完成，更适合 workflow 异步编排。

---

## 9. 企业级 AI 平台为什么需要权限、API Key、日志

AIFlowy 参考点：

- 系统管理模块。
- API Key。
- Sa-Token 权限注解。
- Bot、Document、MCP、Workflow 的后台管理接口。

### 面试官可能问

> AI 助手接进企业系统，除了模型效果，还要注意什么？

### 稳妥回答

> 企业 AI 助手首先不是玩具，它要接业务数据，所以权限、审计、日志、API Key、数据范围、模型调用成本都要考虑。比如用户能不能查某个油站、某个客户、某份制度文档，不能交给模型判断，必须由后端权限体系控制。

### 可展开点

- 登录态：确认谁在使用。
- 角色权限：决定能不能访问功能。
- 数据权限：决定能查哪些组织、油站、客户、文档。
- API Key：给外部系统调用时做身份和限流。
- 操作日志：记录谁问了什么、调用了什么工具。
- 模型日志：记录模型、token、耗时、异常。
- 反馈数据：用户点赞/点踩，用于优化检索和提示词。

---

## 10. 面试高频追问速查

### Q1：你这个 AI 助手和 Dify/Coze/AIFlowy 有什么区别？

> Dify、Coze、AIFlowy 更像通用 AI 应用平台，强调 Bot 配置、工具插件、知识库、Workflow、发布和管理。石化项目里的 AI 助手更偏企业业务系统里的一个智能模块，重点是接入已有 Java 微服务、权限体系和业务数据。我们不追求做完整平台，而是优先解决一线员工查操作、查设备、查制度、查异常的问题。

### Q2：你们有没有做可视化工作流？

> 当前没有把可视化 Workflow 作为主链路。当前主要是问答、RAG 和工具调用。Workflow 更适合后续做巡检、审批、工单这类跨系统长流程时引入。

### Q3：知识库为什么要分 collection / document / chunk？

> collection 用于业务域隔离，document 用于来源、版本、权限和状态管理，chunk 用于检索粒度控制。这样才能处理文档更新、权限过滤、引用来源和检索调优。

### Q4：工具调用怎么防止越权？

> 模型只负责选择工具和生成参数，后端不信任模型参数。后端会校验参数格式、业务对象是否存在、当前用户是否有组织和数据权限，最终 SQL 或业务查询必须带权限条件。

### Q5：conversationId 为什么重要？

> userId 只能说明是谁，conversationId 才能说明是哪一次会话。同一个用户可以开多个窗口，如果不传 conversationId，多轮上下文和缓存可能串。

### Q6：为什么不是所有问题都走 RAG？

> 能查实时业务数据的问题应该走 Function Calling，比如设备状态、告警列表、客户概览。RAG 更适合查操作手册、制度规范、培训资料。两者分工不同。

### Q7：AIFlowy 你是怎么用的？

> 我把它当成 Java AI 平台源码参考，重点看 Bot 对话、知识库、MCP、Workflow、模型管理这些模块的工程组织方式。它帮助我把石化 AI 助手里的会话、工具、知识库和权限问题理解得更系统，但它不是我的项目经历。

---

## 11. 给 AI 检索的关键词

```text
AIFlowy
石化AI助手
AI助手追问
Java AI应用
Bot配置
模型配置
conversationId
SSE流式输出
知识库分层
DocumentCollection
Document
DocumentChunk
Function Calling
工具注册
工具绑定
MCP
BotMcp
Workflow
runAsync
getChainStatus
权限过滤
API Key
日志审计
RAG权限
旧向量处理
chunk size
```

