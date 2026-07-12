---
tags:
  - 面试
  - Java
  - AI应用
  - Bug排查
  - 真实开发
status: draft
priority: P0
created: 2026-07-11
---

# 真实开发高级排错案例-Java+AI

> 用途：回答“你遇到过什么有技术含量的 Bug / 线上问题 / 联调问题”。  
> 原则：不要只讲现象和修复，要讲影响范围、排查链路、关键日志、根因、修复和防复发。  
> 边界：这些案例用于面试表达训练，讲的时候要按自己真实参与深度收口，不要说成所有生产体系都是自己完整设计。

---

## 0. 面试官真正想听什么

面试官问 Bug，不是想听“我把注解写错了”，而是想判断：

- 你会不会复现问题。
- 你会不会按链路缩小范围。
- 你看不看日志、SQL、缓存、消息、线程上下文。
- 你能不能区分表象和根因。
- 你修完之后有没有防复发动作。

推荐回答结构：

```text
现象
  -> 影响范围
  -> 复现方式
  -> 排查路径
  -> 关键证据
  -> 根因
  -> 修复
  -> 防复发
```

---

## 1. 案例一：AI Tool 调用拿不到用户上下文，导致权限过滤失效风险

### 现象

AI 助手调用设备查询 Tool 时，普通油站用户问“查一下本站设备状态”，有时返回“无权限”或查不到数据；日志里 Tool 参数有 `stationCode`，但 Service 层拿到的当前用户组织范围为空。

### 影响范围

- 影响 AI Function Calling 里的业务 Tool。
- 普通 CRUD 接口可能正常，因为它们走了另一个权限解析链路。
- 风险点是：如果后端没有兜底，模型传入的 stationCode 可能绕过用户真实权限。

### 排查路径

```text
前端问题
  -> AI 接口请求头是否带 token
  -> Java AI 入口是否解析登录态
  -> Tool 执行线程是否还能拿到 ThreadLocal
  -> Service 查询是否拼接组织权限
  -> SQL 是否带 org/station 条件
```

### 关键证据

- Controller 入口能拿到 userId。
- Tool 执行时 `CurrentUserHolder.get()` 为空。
- SQL 日志里没有正常拼接用户组织范围。
- 同一个用户直接访问业务接口正常，说明不是角色配置缺失。

### 根因

AI Tool 调用链路和普通 Controller 链路不完全一样。普通接口在拦截器里解析 token 后写入 ThreadLocal，但 Tool 执行可能经过异步线程、模型回调或内部方法调用，导致 ThreadLocal 没有正确传递。

### 修复

- Java AI 入口显式构造 `UserContext`，包含 userId、role、orgCode、stationScope。
- Tool 方法不再只依赖模型参数，必须从 `UserContext` 读取权限范围。
- 如果 Tool 走异步线程，显式传递上下文，或在执行前重新绑定上下文。
- Tool 执行结束后清理 ThreadLocal，避免线程复用导致串用户。

### 防复发

- Tool 调用日志记录 `traceId + userId + userScopeHash + toolName`。
- 单测覆盖“无权限用户传入有权限外 stationCode”的场景。
- 规定所有 AI Tool 都必须走统一权限包装器，不能直接调用 Mapper。

### 面试回答

> 我遇到过 AI Tool 调用时用户上下文丢失的问题。普通接口能拿到当前用户，但 AI Tool 执行到 Service 层时 ThreadLocal 为空，导致权限过滤不稳定。排查时我先确认 token、Controller、Tool 参数都没问题，再看 SQL 和用户上下文，最后发现 Tool 链路和普通接口链路不完全一致，异步或内部调用时 ThreadLocal 没有传递。修复思路是把 userId、角色、组织范围封装成 UserContext，由 Java AI 入口显式传给 Tool，Tool 执行前统一做权限校验，而不是相信模型传参。

---

## 2. 案例二：AI 答案缓存按问题文本命中，导致不同权限用户看到不该看的答案

### 现象

一个地市管理员问过“查询某油站设备异常处理流程”后，普通油站用户再问相似问题，命中了缓存，答案里出现了超出当前用户范围的站点信息或引用来源。

### 影响范围

- 影响 AI 最终答案缓存。
- 不一定影响实时业务接口，因为业务接口本身有权限校验。
- 风险点是缓存绕过了“每次生成前的权限过滤”。

### 排查路径

```text
用户问题
  -> questionHash
  -> Redis cacheKey
  -> 是否包含 userScopeHash
  -> 缓存 value 是否包含 docId/version/source
  -> 文档引用是否属于当前用户权限
```

### 关键证据

- Redis key 只有 `scene + questionHash`。
- 不同用户问相似问题命中同一个 key。
- RAG 检索阶段本来有权限 filter，但缓存命中后没有重新走检索。

### 根因

缓存 key 设计过粗，只按问题文本或归一化问题缓存，没有把用户权限范围、知识库版本、业务场景放进 key。缓存命中后直接返回最终答案，等于绕过了检索阶段权限过滤。

### 修复

```text
ai:answer:{scene}:{userScopeHash}:{kbVersion}:{questionHash}
ai:tool:{toolName}:{userScopeHash}:{paramHash}
ai:rag:{kbVersion}:{userScopeHash}:{questionHash}
```

- 最终答案缓存必须绑定 `userScopeHash`。
- 知识库答案缓存绑定 `kbVersion`。
- 实时业务数据短 TTL，或只缓存结构化中间结果。
- 缓存 value 记录 docId、version、source，便于文档更新时清理。

### 防复发

- 加缓存命中日志：traceId、cacheKeyHash、userScopeHash、kbVersion。
- 用两个不同权限账号跑同一问题，确认不会互相命中最终答案。
- 低置信度兜底答案不长期缓存。

### 面试回答

> 我遇到过 AI 缓存设计过粗的问题。最开始只按问题 hash 缓存答案，后来发现不同权限用户问相似问题可能命中同一个答案。这个问题本质不是 Redis 用法错，而是 AI 答案里包含权限和知识库版本语义。修复时我把 key 改成 scene、userScopeHash、kbVersion、questionHash 的组合，并区分最终答案缓存和 Tool 结构化结果缓存，避免缓存绕过权限过滤。

---

## 3. 案例三：SSE 流式输出中断后，会话历史出现半条回答或重复回答

### 现象

用户问 AI 时关闭页面或网络断开，再次进入会话后，有时看到半截回答；如果用户马上重试，可能出现两条相似回答，或者上一条仍显示生成中。

### 影响范围

- 影响 AI 助手会话体验。
- 影响审计和排查，因为不知道这条回答是成功、失败还是被取消。
- 如果没有停止下游生成，还会浪费模型 token。

### 排查路径

```text
SSE 连接建立
  -> 首 token 时间
  -> 前端断开事件
  -> 服务端是否捕获 IOException / onCompletion
  -> 模型调用是否取消
  -> message 状态是否更新
  -> 重试是否复用 requestId
```

### 关键证据

- message 表只有 content，没有 status。
- 服务端只在生成完成后落库，中断时没有统一状态。
- 用户重试没有 requestId / messageId 去重。

### 根因

流式输出把“生成过程”和“消息落库”绑定得太松。正常完成时可以保存完整答案，但前端断开、模型异常、服务端超时时，缺少状态机和幂等控制。

### 修复

消息状态：

```text
generating
  -> completed
  -> interrupted
  -> failed
  -> cancelled
```

处理方式：

- 请求开始时创建 messageId，状态置为 `generating`。
- 流式过程中临时累积已输出 token。
- 正常结束置为 `completed`。
- 前端断开置为 `interrupted` 或 `cancelled`。
- 模型异常置为 `failed`，记录错误码。
- 重试时使用 requestId / messageId 做幂等，避免重复写 completed。

### 防复发

- 日志记录 traceId、messageId、首 token 时间、输出 token 数、断开原因。
- 前端区分生成中、已中断、失败、已完成。
- 对长回答设置超时和最大输出长度。

### 面试回答

> 我遇到过 SSE 流式回答中断后会话历史不一致的问题。用户断开页面后，服务端有时没有把消息状态更新清楚，导致历史里出现半条回答或重试后两条回答。排查时我看了 SSE 连接生命周期、服务端异常日志和 message 落库逻辑，最后发现缺少生成状态机。修复思路是请求开始就创建 messageId，状态从 generating 流转到 completed、interrupted、failed 或 cancelled，并用 requestId 做重试幂等。

---

## 4. 案例四：文档更新后旧向量仍被召回，AI 回答旧制度

### 现象

知识库更新了新版操作手册，但用户问操作步骤时，AI 仍然引用旧文档片段，答案和新制度不一致。

### 影响范围

- 影响 RAG 问答准确性。
- 影响引用来源可信度。
- 如果制度、安全规范过期，风险比普通问答错误更高。

### 排查路径

```text
文档上传记录
  -> document version
  -> chunk version
  -> Milvus metadata
  -> 检索 filter 是否带 activeVersion/enabled
  -> answer cache 是否仍绑定旧 kbVersion
```

### 关键证据

- document 表新版本是 enabled。
- Milvus 中旧版本 chunk 仍可被召回。
- RAG filter 只按 docType 查询，没有过滤 version / enabled。
- Redis 中存在旧 `kbVersion` 的答案缓存。

### 根因

文档更新只更新了业务表状态，但向量库里的旧 chunk 没有标记 inactive，检索 filter 也没有限制 activeVersion。同时答案缓存没有跟知识库版本绑定，导致旧答案继续返回。

### 修复

- 文档按 `docId + version` 管理。
- 新版本状态先是 `indexing`，完成后再切换 `activeVersion`。
- 旧版本标记 `inactive`，检索只查 `enabled=true AND version=activeVersion`。
- 缓存 key 增加 `kbVersion`。
- 旧向量先软删除，确认稳定后异步物理清理。

### 防复发

- 上传新版本后跑固定测试问题，确认不再召回旧 chunk。
- answer_source 记录 docId、chunkId、version。
- 文档更新流程结束时触发缓存清理。

### 面试回答

> 我遇到过知识库文档更新后 AI 仍引用旧内容的问题。排查时不是只看文档表，而是沿着 document、chunk、Milvus metadata、检索 filter、答案缓存一路查。最后发现旧向量仍在召回范围里，缓存也没有绑定知识库版本。修复时改成 docId + version 管理，新版本 indexed 后再切 activeVersion，旧版本 inactive，检索时只查生效版本，同时清理对应 kbVersion 的缓存。

---

## 5. 案例五：设备消息重复消费导致离线告警重复生成

### 现象

设备离线扫描或消息消费后，同一设备同一类型告警出现多条未恢复记录，页面上看起来像设备频繁异常。

### 影响范围

- 影响设备告警准确性。
- 影响地市或油站处理优先级。
- 消息重试时可能放大重复数据。

### 排查路径

```text
RabbitMQ 消息
  -> consumer 是否重复消费
  -> ack 时机
  -> 告警唯一键
  -> 当前是否已有 active 告警
  -> 数据库唯一约束
  -> 重试/死信记录
```

### 关键证据

- 同一 deviceId、alarmType、alarmStartTime 存在多条 active 记录。
- 消费日志里同一个 messageId 有多次处理。
- 插入告警前没有查询未恢复告警，也没有唯一约束兜底。

### 根因

消息系统只能保证至少一次投递时，消费者必须自己做幂等。原逻辑每次扫描或每次消费异常状态都直接 insert 告警，没有用“未恢复告警只更新”的状态模型。

### 修复

- 告警按 `deviceId + alarmType + alarmStatus(active)` 判断是否已有未恢复记录。
- 已有 active 告警只更新 `lastCheckTime`，不重复插入。
- 设备恢复后把告警状态改为 `recovered`，记录 recoverTime。
- 数据库加业务唯一约束或唯一索引兜底。
- 消费成功后 ack，失败进入重试或死信队列。

### 防复发

- 用重复 messageId 回放测试，确认只生成一条 active 告警。
- 消费日志记录 messageId、deviceId、alarmType、处理结果。
- 监控 active 告警重复数量。

### 面试回答

> 我遇到过设备告警重复生成的问题。表面看是页面多了几条告警，实际根因是消息重复消费和告警幂等没做好。排查时我看了 RabbitMQ 消费日志、messageId、告警表唯一字段，发现同一设备同一告警类型有多条未恢复记录。修复时改成状态模型：如果已有 active 告警就更新 lastCheckTime，不再插入；恢复时改 recovered，并用唯一约束兜底。

---

## 6. 这些案例怎么选

如果面试官问“讲一个你最有代表性的 Bug”，优先讲：

1. AI Tool 用户上下文丢失。
2. AI 答案缓存权限污染。
3. 文档更新后旧向量仍被召回。

如果面试官偏 Java 后端基础，讲：

1. 设备消息重复消费导致告警重复。
2. ThreadLocal 当前用户只 get 没 set。
3. MyBatis Plus 分页导包冲突。

如果面试官偏 AI 应用，讲：

1. RAG 权限过滤和缓存失效。
2. SSE 中断后的消息状态机。
3. 旧向量和知识库版本回滚。

---

## 7. 最终背诵版

> 我遇到过一个比较典型的 AI 应用排错问题：AI Tool 调用时普通业务接口能拿到当前用户，但 Tool 执行到 Service 层时用户上下文为空，导致权限过滤不稳定。排查时我没有直接改 SQL，而是从请求 token、Java AI 入口、Tool 调用链路、ThreadLocal、SQL 权限条件一路查，最后发现 AI Tool 链路和普通 Controller 链路不完全一致，异步或内部调用时 ThreadLocal 没有正确传递。
>
> 修复时我把 userId、角色、组织范围封装成 UserContext，由 Java AI 入口显式传给 Tool，Tool 执行前统一做参数校验和权限校验，并在日志里记录 traceId、toolName、userScopeHash。这个问题给我的经验是，AI 应用里模型只是理解意图，真正的数据权限和安全边界必须落在后端，不能依赖模型参数或前端字段。
