---
tags: [天机学堂, tj-remark, 点赞, Redis, RabbitMQ, Spec]
status: implemented-integration-testing
updated: 2026-07-19
---

# tj-remark 点赞服务 Spec

> 本文记录设计决策和一致性边界；仓库真实实现、配置、验证和联调故障见 [[09-tj-remark点赞服务实现与联调]]。

## 当前状态

核心链路已实现并通过编译与定向单元测试。Nacos 共享配置已确认，XXL-Job 执行器与 `likeEventCompensationJob` 已注册成功；当前处于真实点赞/取消点赞及异步计数链路联调阶段。仓库中的完整实施 Spec：

`D:\workspece\hemima\tjxt\tianji\docs\specs\tj-remark-like-service.md`

## 已确认决策

- 新服务名为 `tj-remark`，数据库为 `tj_remark`，有效点赞关系表为 `liked_record`。
- 一期仅支持学习服务的互动回答和评论，现有前端统一传 `QA`，对应 `interaction_reply`。后端兼容 `ANSWER`、`COMMENT` 并统一归一化为 `QA`；问题、课程、帖子暂不接入。
- 点赞和取消点赞接口为 `POST /likes`；批量查询当前用户已点赞对象为 `GET /likes/list`；均使用项目 `R<T>` 响应体。
- Redis 原子维护用户状态、对象计数和 Redis Stream 待投递事件；RabbitMQ 发布确认后才确认/裁剪 Stream，允许短暂冗余以避免宕机丢事件。
- 行为事件逐条发 MQ，服务于通知与行为分析；计数同步按对象在 1～3 秒窗口聚合，学习服务异步更新 `interaction_reply.liked_times`。
- 取消点赞删除 `liked_record` 中的有效关系；允许本人点赞，但不向本人发送通知。
- XXL-Job 只做待确认消息、计数/关系对账和死信补偿，不承担秒级实时投递。

## 数据模型边界

一期保留 `liked_record` 现有唯一索引 `(biz_id, user_id)`，因为回答与评论共用 `interaction_reply` 的 ID 空间。未来接入课程、帖子等独立表前，必须迁移为 `(biz_type, biz_id, user_id)`，否则不同业务类型的相同 ID 会冲突。

## 实施前置

- 在根 `pom.xml` 注册 `tj-remark`；
- 在 Nacos 配置该服务的数据库、Redis、RabbitMQ、XXL-Job 与网关路由；
- 补齐 RabbitMQ publisher confirm/return callback，使 Redis Stream 只在 broker 确认后 ack；
- `tj-learning` 新增计数事件消费者，并以事件版本保障重复、乱序投递不会覆盖新计数。

## 当前实现结果

- 已新增 `tj-remark` 模块并注册到根 Maven 工程；网关原有 `/rs/**` 路由可直接复用。
- 点赞入口使用 Lua 原子维护用户状态、绝对计数、版本、dirty 标记和 Redis Stream。
- Stream 消费组在 RabbitMQ publisher confirm 后才 `XACK + XDEL`，失败事件留在 pending 中重试。
- 行为事件逐条发送；计数按对象聚合；有效点赞关系通过单活 MQ 消费者批量写入 `liked_record`。
- 学习服务消费绝对计数，以 Redisson 对象锁和版本号避免重复、乱序消息覆盖新值。
- 已提供 `likeEventCompensationJob`，实时投递由服务内短周期任务负责，XXL-Job 用于补偿。
- `tj-message` 点赞通知、`tj-data` 热度榜/行为分析的消费端尚未实现；本次已提供 `remark.behavior.*` 可靠事件出口。
- `tj-api` 已提供 `RemarkClient` 与 fallback，其他微服务可以通过服务发现复用批量点赞状态查询。

## Feign 服务间复用

2026-07-19 已在 `tj-api` 新增：

- `com.tianji.api.client.remark.RemarkClient`
- `com.tianji.api.client.remark.fallback.RemarkClientFallback`
- `FallbackConfig` 中的 `RemarkClientFallback` Bean 注册

调用契约：

```java
List<Long> likedIds = remarkClient.queryLikedIds("QA", bizIds);
```

- Feign 服务名为 `remark-service`，公共路径为 `/likes`，调用 `GET /likes/list`。
- 参数为 `bizType` 和 `bizIds`，返回当前登录用户已点赞的业务 ID 列表；单次最多查询 200 个对象。
- 内部 Feign 请求不经过网关，Controller 直接返回原始 `List<Long>`，不能在客户端声明为 `R<List<Long>>`。
- 点赞服务异常时 fallback 记录完整异常堆栈并返回空列表。点赞状态属于非核心展示信息，因此降级不会阻断回答/评论列表；但调用方需要理解“空列表”也可能代表服务降级，而不一定表示用户确实未点赞。
- 该接口查询“当前登录用户”，依赖认证 SDK 的 Feign 用户信息透传。它适合同步处理用户请求；定时任务、MQ 消费者等没有用户上下文的场景不能直接调用，若未来需要后台查询，应另建显式传入用户 ID 的内部接口，并限制调用权限。
- `RequestIdRelayConfiguration` 已自动扫描 `com.tianji.api.client`，无需各业务服务再次声明 `@EnableFeignClients`；fallback 必须继续在 `FallbackConfig` 中注册，否则 Sentinel 无法取得对应工厂 Bean。

## 联调修复

- 2026-07-18：首次点击点赞按钮时报 `LikeBizType` 无法解析 `QA`。根因是前端沿用项目原有 `QA` 契约，而初版后端只声明 `ANSWER/COMMENT`。
- 修复方式：新增 `QA` 为统一存储和消息类型，`ANSWER/COMMENT` 仅作为兼容别名；计数路由新增 `remark.count.qa`，并补充 JSON 反序列化回归测试。
- 2026-07-18：初版 `LikeController` 显式返回 `R<T>`，功能正确但不符合本项目 Controller 的主流规范。项目实际由业务服务中的 `WrapperResponseBodyAdvice` 对网关请求统一包装：Controller 应返回 `void` 或原始业务数据，内部 Feign 请求则保持原始响应。
- 修复方式：`POST /likes` 的 Java 返回类型改为 `void`，`GET /likes/list` 改为直接返回 `List<Long>`；客户端经过网关后看到的外部契约仍然是统一的 `R<T>`，不会发生响应格式变化。

### 点赞数显示为 1，但数据库 `liked_times` 仍为 0

- 发生时间：2026-07-18。
- 现象：点击点赞后页面立即显示“点赞(1)”，`tj_remark.liked_record` 也成功写入，但 `tj_learning.interaction_reply.liked_times` 长时间保持 `0`。
- 首先排除：这不是正常的 1～3 秒计数聚合延迟。关系表已经完成插入/删除，只能证明 Redis Stream → MQ → 关系持久化链路正常，不能证明 `remark.count.*` 计数链路正常。
- 关键证据：RabbitMQ 的 `learning.reply.like.count.queue` 有消费者且无积压，但队列绑定中只有 `remark.count.answer`、`remark.count.comment`，缺少当前实际发布的 `remark.count.qa`。
- 根因：`learning-service` 在增加 `QA` 路由兼容代码之前已经启动，运行中的旧监听器没有声明 `remark.count.qa` 绑定；后续只编译代码但没有重启服务，因此新注解配置没有加载。
- 恢复方式：重启 `learning-service`，确认 RabbitMQ 队列出现 `remark.count.qa` 绑定，然后执行一次“取消点赞 → 重新点赞”重新产生计数事件。恢复后约 1～3 秒内 `liked_times` 正确更新。
- 排查顺序：先确认 `liked_record` 是否变化，再看 `remark.count.qa` 队列绑定、消费者数量和消息积压，最后核对计数事件 `bizId` 是否等于 `interaction_reply.id`；不要看到页面乐观加一就判断数据库链路成功。
- 防复发规则：修改 `@RabbitListener` 的交换机、路由键、队列或消息类型后，必须重启对应消费者并在 RabbitMQ 管理端验证实际绑定。编译成功不等于运行中 Bean 已更新。
- 可靠性隐患：当前 `RabbitTemplate` 设置 `mandatory=false` 是为了允许暂时没有通知/分析消费者的行为事件，但这也会让无法路由的计数事件可能被 broker confirm 后视作成功，继而删除 dirty 标记。后续应区分可选行为事件与必达计数/持久化事件：必达事件必须启用 returns 或预先校验绑定，不能把 publisher confirm 等同于“消息已被目标队列接收”。

## 运行与配置

- 服务注册名：`remark-service`；模块名：`tj-remark`；默认端口：`8091`。
- 网关入口：`/rs/**`，转发至 `lb://remark-service`，点赞接口需要登录态，不加入网关免登录列表。
- Nacos 复用：`shared-spring.yaml`、`shared-redis.yaml`、`shared-mybatis.yaml`、`shared-logs.yaml`、`shared-mq.yaml`、`shared-xxljob.yaml`。
- 服务自有配置至少确认 RabbitMQ publisher confirm：`spring.rabbitmq.publisher-confirm-type: correlated`。
- 可调参数：`tj.remark.outbox-poll-ms` 默认 `500` 毫秒，`tj.remark.count-publish-ms` 默认 `1000` 毫秒。
- 本地 XXL-Job 执行器建议固定端口 `tj.xxl-job.executor.port: 9991`，执行器 AppName 必须与服务注册的 `${spring.application.name}` 一致，即 `remark-service`。
- XXL-Job 任务：BEAN 模式，JobHandler 为 `likeEventCompensationJob`；当前按每分钟执行一次补偿。自动注册模式下无需手填机器地址，服务启动并注册后由调度中心获取地址。

## 实时任务与 XXL-Job 的混合方案

当前没有为了完成练习而把所有短周期任务都迁移到 XXL-Job，而是按任务实时性拆分职责：

| 职责 | 当前机制 | 选择原因 |
|---|---|---|
| Redis Stream 待投递事件转发 | 服务内 `@Scheduled`，默认每 500ms | 需要毫秒到秒级响应，不应依赖分钟级调度 |
| 点赞计数聚合发布 | 服务内 `@Scheduled`，默认每 1s | 在降低 MQ 消息量的同时保证展示计数较快收敛 |
| Pending 重试、dirty 计数补偿 | XXL-Job `likeEventCompensationJob` | 适合分钟级补偿、失败重试、执行记录和人工触发 |
| 后续全量对账、死信巡检 | XXL-Job | 属于运维补偿任务，不属于实时请求链路 |

这一混合方案比“全部交给 XXL-Job”更适合真实项目：避免高频调度产生额外网络和日志开销，也避免调度中心异常直接阻断实时消息转发。XXL-Job 在这里是安全网，不是实时消息泵。

当前实现仍有生产化优化空间：Redis Stream 转发可由 500ms 轮询进一步改为 `StreamMessageListenerContainer` 或阻塞式常驻消费，减少空轮询和延迟；计数聚合仍保留短周期触发，XXL-Job 继续承担补偿与对账。多实例部署时必须继续依赖 Redis Stream 消费组、幂等处理、事件版本和分布式互斥，不能把 `@Scheduled` 的单机执行假设当作一致性保障。

练习要求与工程决策需要区分：若目标只是演示 XXL-Job，可以增加独立演示任务；不应为了形式上“替代 SpringTask”而让秒级实时链路完全依赖 XXL-Job。

## 联调验收清单

1. 重启 `remark-service` 与 `learning-service`，确保新枚举、MQ 路由和消费者生效。
2. 前端使用 `bizType: "QA"` 调用 `POST /rs/likes` 点赞；成功后 `/rs/likes/list` 应立即返回该 `bizId`。
3. `tj_remark.liked_record` 最终出现一条 `biz_type = 'QA'` 的有效关系。
4. `tj-learning.interaction_reply.liked_times` 应在约 1～3 秒内同步为最新绝对计数。
5. 再次发送 `liked: false` 后，Redis 状态立即取消，数据库关系最终删除，`liked_times` 最终减一。
6. 重复点赞或重复取消不应重复改变计数；RabbitMQ 重复或乱序消息不应让旧值覆盖新值。
7. XXL-Job 日志出现 `LikeCompensationJob#compensate` 注册信息，只能说明处理器注册成功；仍需以接口、数据库与计数三处结果验证完整链路。

## 当前未完成边界

- `tj-message` 的点赞通知消费者尚未实现。
- `tj-data` 的热度榜与行为分析消费者尚未实现。
- 课程、问题、帖子点赞尚未接入；接入独立业务 ID 空间前必须先把唯一索引迁移为 `(biz_type, biz_id, user_id)`。
- 尚需完成真实环境下点赞、取消点赞、重复请求、服务宕机重投和补偿任务的完整联调记录。

## 关键代码入口

- 仓库实施 Spec：`docs/specs/tj-remark-like-service.md`
- 服务入口：`tj-remark/src/main/java/com/tianji/remark/RemarkApplication.java`
- 点赞业务：`tj-remark/src/main/java/com/tianji/remark/service/impl/LikeServiceImpl.java`
- Redis Stream 转发：`tj-remark/src/main/java/com/tianji/remark/service/LikeEventPublisher.java`
- 补偿任务：`tj-remark/src/main/java/com/tianji/remark/handler/LikeCompensationJob.java`
- 学习服务计数消费者：`tj-learning/src/main/java/com/tianji/learning/listener/LikeCountListener.java`
- 建表脚本：`tj-remark/src/main/resources/sql/20260718_liked_record.sql`

## 跨项目复用知识

- [[☕ Java笔记/高频最新状态的Redis合并写模式]]：已抽取“关系状态、聚合最新值、行为事件”三类数据语义，Lua 原子边界、可靠 outbox、confirm 与路由成功的区别，以及实时任务与补偿任务的职责划分。
- [[☕ Java笔记/微服务公共API契约与Feign降级边界]]：已抽取公共 API 模块、Feign 契约、fallback 语义、当前用户上下文限制、自动装配和批量调用检查清单。
