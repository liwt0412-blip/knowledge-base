---
tags: [天机学堂, tj-remark, 点赞服务, Redis, RabbitMQ, XXL-Job, 项目实现, 联调]
status: integration-testing
created: 2026-07-19
updated: 2026-07-19
---

# tj-remark 点赞服务实现与联调

> 本文记录仓库中的真实实现、配置、验证结果和故障处理。设计依据与一致性边界见 [[08-tj-remark点赞服务Spec]]。

## 一、实现目标与当前范围

新增独立微服务 `tj-remark`，为其他微服务提供统一点赞能力。当前一期实际接入互动问答中的回答和评论：

- 前端业务类型统一使用 `QA`，后端兼容 `ANSWER`、`COMMENT`，进入 Redis、MySQL 和 MQ 前归一化为 `QA`；
- 支持点赞、取消点赞和批量查询当前用户已点赞 ID；
- Redis 承担高频状态、实时计数和待投递事件；
- RabbitMQ 异步同步计数与点赞关系；
- MySQL 保存可恢复的有效点赞关系；
- `tj-learning` 异步更新 `interaction_reply.liked_times`；
- 为通知、热度榜和行为分析提供行为事件出口。

当前未接入问题、课程和帖子点赞；`tj-message`、`tj-data` 的通知、热榜和分析消费者尚未实现。

## 二、接口实现

### 2.1 点赞或取消点赞

- 请求方式：`POST`
- 服务内路径：`/likes`
- 网关路径：`/rs/likes`
- 用户身份：从 `UserContext` 获取，不接收客户端用户 ID。

```json
{
  "bizId": 2078470584694067201,
  "bizType": "QA",
  "liked": true
}
```

相同目标状态按幂等成功处理：重复点赞或重复取消不重复改变计数，也不重复生成行为事件。

### 2.2 批量查询点赞状态

- 请求方式：`GET`
- 服务内路径：`/likes/list`
- 参数：`bizType`、`bizIds`
- 返回：当前用户已点赞的 `bizId` 列表，单次最多 200 个。

Controller 按项目真实规范返回 `void` 或原始 `List<Long>`；网关请求由 `WrapperResponseBodyAdvice` 包装为统一响应，内部 Feign 请求保持原始数据。

## 三、模块与代码变更

### 3.1 `tj-remark`

- `controller/LikeController`：点赞、取消和批量状态查询；
- `service/impl/LikeServiceImpl`：Redis 冷启动恢复、Lua 原子更新和查询；
- `service/LikeEventPublisher`：Stream 转发、计数聚合和 RabbitMQ 发布确认；
- `listener/LikePersistenceListener`：批量同步有效点赞关系；
- `handler/LikeCompensationJob`：XXL-Job 补偿入口；
- `mapper/LikedRecordMapper`：批量幂等插入和删除；
- `sql/20260718_liked_record.sql`：`liked_record` 建表脚本。

### 3.2 `tj-api`

- 新增行为事件、计数事件和关系持久化批次 DTO；
- 新增 `RemarkClient` 和 `RemarkClientFallback`；
- 在 `FallbackConfig` 注册 fallback Bean；
- `RemarkClient` 当前提供公共复用入口，但尚未被某个业务 Service 实际注入调用。

### 3.3 `tj-learning`

- 新增 `LikeCountListener`；
- 监听 `remark.count.qa`，兼容 `remark.count.answer/comment`；
- 按绝对计数更新 `interaction_reply.liked_times`；
- 使用事件版本和 Redisson 对象锁避免重复、乱序消息覆盖新值。

## 四、核心实现链路

```text
POST /likes
  → Lua 原子校验并修改用户点赞状态
  → 更新对象绝对计数与版本
  → 写 dirty Hash
  → XADD Redis Stream

Redis Stream
  → 服务内短周期任务读取
  → 发布行为事件和关系持久化批次
  → RabbitMQ broker confirm 后 XACK + XDEL

dirty Hash
  → 默认每 1 秒读取最新绝对计数
  → 发布 remark.count.qa
  → tj-learning 更新 interaction_reply.liked_times

关系持久化消息
  → tj-remark 单活消费者
  → 读取 Redis 最新关系状态
  → 最多 100 条批量插入/删除 liked_record
```

Redis 首次访问或数据丢失时，从 `liked_record` 懒加载用户点赞关系和对象计数。用户状态 Set、对象计数、版本、dirty 和 Stream 由 Lua 在同一个 Redis 原子边界中修改。

## 五、定时任务与补偿

- `@Scheduled` 每 500ms 处理 Redis Stream，承担实时投递；
- `@Scheduled` 每 1s 聚合并发布最新点赞计数；
- XXL-Job `likeEventCompensationJob` 当前按分钟执行，重试仍留在 Stream 或 dirty 中的任务；
- XXL-Job 执行器 AppName 为 `remark-service`，本地自动注册，不手填机器地址。

这是“实时处理 + 调度补偿”的混合方案。XXL-Job 是安全网，不承担秒级实时消息泵。

## 六、配置与部署事实

- Maven 模块：`tj-remark`；
- Nacos 注册名：`remark-service`；
- 数据库：`tj_remark`；
- 服务端口：`8091`；
- 网关：`/rs/** → lb://remark-service`；
- RabbitMQ：复用 `shared-mq.yaml`，publisher confirm 使用 `correlated`；
- Redis、MyBatis、日志和 XXL-Job 均复用项目共享配置；
- Jenkins 部署命令已按模块规划为：

```bash
ssh root@192.168.150.101 "/usr/local/src/script/startup.sh -c tj-remark -n tj-remark -d tj-remark -p 8091"
```

Jenkins 任务已完成配置讨论，但尚未记录一次正式构建部署成功结果，不能标记为已部署验证。

## 七、已完成验证

- `tj-api`、`tj-remark`、`tj-learning` 相关模块定向构建成功；
- `LikeFormDTOTest` 验证前端 `QA` JSON 契约；
- `LikePersistenceListenerTest` 验证关系批量落库；
- `LikeCountListenerTest` 验证计数消费幂等/版本逻辑；
- XXL-Job 日志确认 `LikeCompensationJob#compensate` 注册成功；
- 真实页面完成点赞与取消操作；
- `tj_remark.liked_record` 可观察到 `QA` 关系插入和删除；
- 修复 MQ 绑定后，`interaction_reply.liked_times` 在约 1～3 秒内正确更新。

## 八、联调问题与修复

### 8.1 前端传 `QA`，后端枚举无法解析

- 现象：`LikeBizType` 反序列化报错，只接受 `ANSWER/COMMENT`；
- 根因：设计枚举时没有先核对前端真实契约；
- 修复：增加 `QA`，将 `ANSWER/COMMENT` 作为兼容别名，统一归一化为 `QA`；
- 验证：增加 JSON 反序列化回归测试。

### 8.2 Controller 手动返回 `R<T>`

- 现象：功能可用，但与项目多数 Controller 风格不一致；
- 根因：把“统一响应体”错误理解成所有 Controller 都应显式返回 `R<T>`；
- 修复：点赞接口返回 `void`，查询接口返回 `List<Long>`，由网关请求的 ResponseBodyAdvice 自动包装。

### 8.3 页面显示点赞 1，数据库计数仍为 0

- 现象：页面乐观更新为 1，`liked_record` 已插入，但 `interaction_reply.liked_times` 长时间为 0；
- 证据：计数队列有消费者且无积压，但实际绑定只有 `remark.count.answer/comment`，缺少 `remark.count.qa`；
- 根因：修改监听器代码后只完成编译，运行中的旧 `learning-service` 没有重启，因此 RabbitMQ 没有加载新绑定；
- 修复：重启 `learning-service`，确认管理端出现 `remark.count.qa` 绑定，再执行一次取消和重新点赞；
- 结果：计数异步更新成功。

## 九、当前风险与后续任务

1. `RabbitTemplate mandatory=false` 会让不可路由的必达计数消息可能被误判成功；应区分可选行为事件和必达计数/持久化事件，补充 returns 处理。
2. `liked_record` 当前唯一索引为 `(biz_id, user_id)`；接入课程、帖子等独立 ID 空间前必须迁移为 `(biz_type, biz_id, user_id)`。
3. Redis Stream 固定消费者名和多实例 dirty 扫描仍需进一步加固 pending 认领和去重策略。
4. `RemarkClient` 已存在于公共 API 模块，但尚未在业务 Service 中形成真实调用链。
5. `tj-message` 点赞通知、`tj-data` 热度榜和行为分析消费者尚未实现。
6. 尚需记录 Jenkins 正式部署、服务宕机重投、RabbitMQ 不可路由和 Redis 恢复的完整演练结果。

## 十、关联文档

- 设计 Spec：[[08-tj-remark点赞服务Spec]]
- 通用合并写：[[☕ Java笔记/高频最新状态的Redis合并写模式]]
- 通用 Feign 契约：[[☕ Java笔记/微服务公共API契约与Feign降级边界]]

