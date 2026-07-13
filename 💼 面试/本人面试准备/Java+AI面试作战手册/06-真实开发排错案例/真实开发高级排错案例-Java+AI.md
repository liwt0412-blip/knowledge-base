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

> 真实性规则：当前五个高级案例在补齐原始证据前统一视为“方案推演”，不能使用“我遇到过”“线上发生过”“我们修复后”等事实句式。只有能对应到日志、代码、工单、提交记录或清晰个人记忆的案例，才可升级为“真实处理”或“参与联调”。

案例标签模板：

```text
案例性质：真实处理 / 参与联调 / 方案推演
本人动作：复现 / 定位 / 修改 / 测试 / 上线观察
证据锚点：接口、类名、日志字段、SQL、Redis Key、提交或工单
允许话术：我遇到过 / 我参与排查过 / 设计时重点防范过
```

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

**案例性质：方案推演，补齐证据后再升级。**

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

> 在设计 AI Tool 权限链路时，我重点检查过用户上下文在线程切换或内部调用中丢失的风险。普通接口可能能拿到当前用户，但 Tool 执行到 Service 层时 ThreadLocal 可能为空。排查思路是依次确认 token、Controller、Tool 参数、用户上下文和 SQL 权限条件。防护上把 userId、角色、组织范围封装成 UserContext，由 Java AI 入口显式传给 Tool，Tool 执行前统一做权限校验，而不是相信模型传参。

---

## 2. 案例二：AI 答案缓存按问题文本命中，导致不同权限用户看到不该看的答案

**案例性质：方案推演，补齐证据后再升级。**

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

> 在设计 AI 答案缓存时，我重点防范过缓存维度过粗导致跨权限复用的问题。这个风险本质不是 Redis 用法错，而是 AI 答案包含权限和知识库版本语义。安全设计是让 key 包含 scene、userScopeHash、kbVersion、questionHash，并区分最终答案缓存和 Tool 结构化结果缓存，避免缓存绕过权限过滤。

---

## 3. 案例三：SSE 流式输出中断后，会话历史出现半条回答或重复回答

**案例性质：方案推演，补齐证据后再升级。**

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

> 在梳理 SSE 流式输出时，我重点考虑过客户端中断导致会话历史不完整或重复写入的问题。排查重点是 SSE 连接生命周期、服务端异常日志和 message 落库逻辑。稳妥的设计是请求开始就创建 messageId，状态从 generating 流转到 completed、interrupted、failed 或 cancelled，并用 requestId 做重试幂等。

---

## 4. 案例四：文档更新后旧向量仍被召回，AI 回答旧制度

**案例性质：方案推演，补齐证据后再升级。**

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

> 在设计知识库更新链路时，我重点检查过旧向量、文档版本和答案缓存不一致的问题。排查不能只看文档表，而要沿着 document、chunk、Milvus metadata、检索 filter、答案缓存一路查。稳妥方案是用 docId + version 管理，新版本 indexed 后再切 activeVersion，旧版本 inactive，检索时只查生效版本，同时清理对应 kbVersion 的缓存。

---

## 5. 案例五：设备消息重复消费导致离线告警重复生成

**案例性质：方案推演，补齐证据后再升级。**

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

> 在设备告警链路设计中，我重点防范过消息重复消费导致重复告警的问题。排查重点是 RabbitMQ 消费日志、messageId、告警表唯一字段以及同一设备同一告警类型是否存在多条未恢复记录。稳妥方案是使用状态模型：已有 active 告警就更新 lastCheckTime，不重复插入；恢复时改为 recovered，并用唯一约束兜底。

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

> 我在 AI Tool 权限链路的方案复盘中重点分析过一个典型风险：普通业务接口能拿到当前用户，但 Tool 经过异步或内部调用后，Service 层的用户上下文可能为空。排查时不能直接改 SQL，而应从请求 token、Java AI 入口、Tool 调用链路、ThreadLocal、SQL 权限条件逐层确认。

---

## 8. 两个核心 Bug 案例：证据化训练稿

> 使用规则：下面的时间、ID、类名、表名和日志都是演练样例，不是生产证据。练习时可以使用；正式面试前必须替换为自己能够确认的细节。确认不了事故真实发生时，只能说“设计时重点防范过”，不能说“线上发生过”或“我最终定位到”。

### 8.1 异步 Tool 调用导致用户上下文丢失

#### 案例卡

| 项目 | 内容 |
|---|---|
| 案例性质 | 方案推演；补齐真实日志、代码或个人记忆后再升级 |
| 核心技术 | Spring AI Tool、ThreadLocal、线程池、数据权限 |
| 面试价值 | 能同时体现链路排查、并发基础和安全边界 |
| 安全开场 | “在设计 AI Tool 权限链路时，我重点检查过一个跨线程上下文风险。” |

#### 现象

普通设备接口查询正常，但通过 AI 助手调用设备查询 Tool 时，偶尔返回“无权访问”或查不到数据。Controller 入口能够取得用户信息，进入 Tool 对应的 Service 后，当前用户却为空。

#### 演练日志

```text
2026-05-18 10:21:43.126 INFO  [http-nio-8080-exec-7]
traceId=8f62b1 userId=10328 orgCode=CS-042
AI request received, question=查询本站离线设备

2026-05-18 10:21:43.487 INFO  [ai-tool-executor-3]
traceId=8f62b1 toolName=queryOfflineDevices stationCode=CS-042

2026-05-18 10:21:43.490 WARN  [ai-tool-executor-3]
traceId=8f62b1 currentUser=null permissionScope=null

2026-05-18 10:21:43.493 WARN  [ai-tool-executor-3]
traceId=8f62b1 tool execution rejected reason=USER_CONTEXT_MISSING
```

关键证据不是一句 `currentUser=null`，而是线程从 `http-nio-8080-exec-7` 切换成了 `ai-tool-executor-3`。普通 ThreadLocal 不会自动复制到线程池工作线程。

#### 问题代码演练

```java
public ToolResult queryOfflineDevices(String stationCode) {
    LoginUser user = UserContextHolder.get();
    if (user == null) {
        throw new AccessDeniedException("用户上下文不存在");
    }
    return deviceService.queryOfflineDevices(
        stationCode,
        user.getDataScope()
    );
}
```

入口代码如果这样切换线程，就可能丢失上下文：

```java
UserContextHolder.set(loginUser);

CompletableFuture.supplyAsync(
    () -> toolService.queryOfflineDevices(stationCode),
    toolExecutor
);
```

#### 个人排查动作

1. 使用同一账号分别调用普通设备接口和 AI 查询接口，排除角色配置差异。
2. 确认两次请求携带相同 Token、用户 ID 和油站编码。
3. 在 Controller、AI 入口、Tool 和 SQL 执行前记录同一个 `traceId`。
4. 对比线程名，发现入口线程有用户信息，Tool 线程的 ThreadLocal 为空。
5. 检查 `CompletableFuture` 或 Tool 执行器配置，确认发生线程切换。
6. 将根因收敛为“用户上下文依赖隐式 ThreadLocal，异步执行时没有显式传递”，而不是数据库或权限配置错误。

#### 修复代码演练

后端认证完成后显式构造上下文：

```java
public record ToolUserContext(
    Long userId,
    String orgCode,
    Set<String> stationScope
) {}
```

```java
ToolUserContext context = new ToolUserContext(
    loginUser.getUserId(),
    loginUser.getOrgCode(),
    permissionService.getStationScope(loginUser)
);

return toolExecutor.execute(
    () -> toolService.queryOfflineDevices(stationCode, context)
);
```

Tool 不能相信模型提供的 `stationCode`，必须用后端权限范围再次校验：

```java
public ToolResult queryOfflineDevices(
        String stationCode,
        ToolUserContext context) {

    if (!context.stationScope().contains(stationCode)) {
        throw new AccessDeniedException("无权查询该油站");
    }

    return deviceService.queryOfflineDevices(stationCode);
}
```

#### 防复发

- 所有业务 Tool 统一经过权限包装器，禁止直接调用 Mapper。
- 日志记录 `traceId、userId、toolName、scopeHash`，但不记录完整敏感权限数据。
- 增加越权测试：普通油站用户传入其他油站编码必须失败。
- 异步任务结束后清理线程上下文，防止线程复用串用户。
- 不把 `InheritableThreadLocal` 当成线程池场景的通用修复方案。

#### 60 秒回答

> 在设计 AI Tool 权限链路时，我重点检查过一个跨线程上下文风险。相同用户直接调用设备接口正常，但 Tool 如果运行在独立线程池中，Service 里通过 ThreadLocal 取得的用户可能为空。排查思路是用同一账号复现，然后在 Controller、AI 入口、Tool 和 SQL 前记录同一个 traceId、用户 ID 和线程名。如果入口线程有用户而 Tool 线程没有，就能把问题收敛到线程切换。修复上不能相信模型传入的油站编码，也不能只依赖隐式 ThreadLocal，而是由 Java 入口显式构造经过认证的 UserContext，传给 Tool 后再次校验数据权限，同时补充越权测试和统一权限包装器。

### 8.2 MQ 重复消费导致设备离线告警重复

#### 案例卡

| 项目 | 内容 |
|---|---|
| 案例性质 | 方案推演；补齐真实告警记录、消费日志或代码后再升级 |
| 核心技术 | RabbitMQ、至少一次投递、业务幂等、事务、Outbox |
| 面试价值 | 能体现消息可靠性、数据库约束和故障边界 |
| 安全开场 | “在设备告警链路设计中，我重点防范过重复投递造成重复告警的问题。” |

#### 现象

同一台设备在几秒内生成两到三条“设备离线”告警，并向运维人员重复发送通知。页面去重只能隐藏现象，数据库中实际存在多条未恢复告警。

#### 演练数据

```sql
SELECT id, device_id, alarm_type, status, created_at
FROM device_alarm
WHERE device_id = 'DEV-10482'
ORDER BY created_at DESC;
```

```text
98121  DEV-10482  OFFLINE  ACTIVE  2026-05-20 08:31:02
98122  DEV-10482  OFFLINE  ACTIVE  2026-05-20 08:31:03
98125  DEV-10482  OFFLINE  ACTIVE  2026-05-20 08:31:06
```

#### 演练日志

```text
08:31:02.112 INFO messageId=hb-10482-174769 attempt=1
deviceId=DEV-10482 event=OFFLINE consumer=alarm-consumer-1

08:31:02.180 ERROR messageId=hb-10482-174769
alarmInserted=true alarmId=98121 notificationResult=TIMEOUT

08:31:03.205 INFO messageId=hb-10482-174769 attempt=2 redelivered=true
deviceId=DEV-10482 event=OFFLINE consumer=alarm-consumer-2

08:31:03.242 INFO messageId=hb-10482-174769
alarmInserted=true alarmId=98122 notificationResult=SUCCESS
```

这组证据形成的链路是：第一次消费已经插入告警，后续通知超时导致消费没有正常结束，消息被重新投递；第二次消费缺少业务幂等，又插入了一条告警。

#### 问题代码演练

```java
@RabbitListener(queues = "device.alarm.queue")
@Transactional
public void consume(DeviceAlarmEvent event) {
    alarmService.createAlarm(event);
    notificationService.send(event);
}
```

问题不只是“忘了 ACK”，还包括：

- 消费者错误地假设一条消息只会处理一次；
- 告警创建没有唯一约束或业务状态幂等；
- 告警状态变更和外部通知耦合，通知失败会放大重试影响；
- 网络超时存在“对方已成功、调用方认为失败”的不确定状态。

#### 个人排查动作

1. 按设备 ID 查询告警表，确认存在多条 `ACTIVE` 告警，而不是前端重复渲染。
2. 对比记录的创建时间、告警类型和消息 `messageId`。
3. 在 RabbitMQ 消费日志中确认相同 `messageId` 被多次处理，并检查 `redelivered`。
4. 查看第一次消费完整链路，确认告警落库后通知接口发生超时。
5. 检查消费者代码和表约束，确认既无幂等判断，也无唯一约束兜底。
6. 将根因定义为“至少一次投递语义 + 业务幂等缺失 + 通知链路耦合”，而不是简单归因于 RabbitMQ 重复消息。

#### 修复代码演练

活动告警使用状态幂等：

```java
@Transactional
public DeviceAlarm handleOffline(DeviceAlarmEvent event) {
    DeviceAlarm active = alarmRepository.findActive(
        event.getDeviceId(),
        AlarmType.OFFLINE
    );

    if (active != null) {
        active.setLastDetectedAt(event.getOccurredAt());
        active.setRepeatCount(active.getRepeatCount() + 1);
        alarmRepository.update(active);
        return active;
    }

    return alarmRepository.insert(DeviceAlarm.activeOffline(event));
}
```

数据库唯一约束作为并发兜底。具体实现可使用独立活动告警表，或者维护只对活动记录生效的业务唯一键：

```text
activeKey = deviceId + ':' + alarmType
```

告警和通知解耦：

```java
@Transactional
public void handleOffline(DeviceAlarmEvent event) {
    DeviceAlarm alarm = alarmService.createOrRefresh(event);
    outboxService.save(NotificationEvent.from(alarm));
}
```

独立消费者处理 Outbox 或通知事件。通知失败只重试通知，不重复创建告警。

#### 防复发

- 数据库唯一约束作为最终兜底，不能只做“先查再插”。
- 所有消费者按重复投递设计，并记录 `messageId、deliveryTag、redelivered`。
- 告警使用 `ACTIVE -> RECOVERED` 状态机，同类活动告警只保留一条。
- 通知失败不能回滚或重复执行已经正确完成的告警状态变更。
- 增加相同消息连续投递三次、两个消费者并发处理的集成测试。

#### 60 秒回答

> 在设备告警链路设计中，我重点防范过重复投递造成重复告警的问题。排查这类问题时，我会先按设备 ID 查告警表，确认数据库确实存在多条活动告警，再用 messageId 关联 RabbitMQ 消费日志。如果第一次消费已经落库，但后续通知超时导致消息重新投递，而第二次又插入告警，就说明根因是至少一次投递语义叠加业务幂等缺失。修复上，同一设备同一告警类型只能有一条 ACTIVE 记录，已有告警就刷新最后检测时间，并增加唯一约束兜底；通知通过独立事件或 Outbox 处理，通知失败只重试通知，不重复创建告警。最后补充重复投递和并发消费的集成测试。

### 8.3 升级为真实案例前的核验清单

- [ ] 项目确实存在异步 Tool、线程池或类似的用户上下文传递问题。
- [ ] 项目确实使用 RabbitMQ 或其他消息中间件处理设备或告警事件。
- [ ] 已将演练类名、表名、日志字段替换为真实或能够确认的项目结构。
- [ ] 能明确说出本人实际执行了复现、定位、修改、测试中的哪些动作。
- [ ] 至少能回答两层追问，不依赖背诵虚构细节。
>
> 修复时我把 userId、角色、组织范围封装成 UserContext，由 Java AI 入口显式传给 Tool，Tool 执行前统一做参数校验和权限校验，并在日志里记录 traceId、toolName、userScopeHash。这个问题给我的经验是，AI 应用里模型只是理解意图，真正的数据权限和安全边界必须落在后端，不能依赖模型参数或前端字段。
