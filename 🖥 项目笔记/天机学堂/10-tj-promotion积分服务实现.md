---
tags: [天机学堂, tj-promotion, 积分, 实施记录]
created: 2026-07-19
status: 已实现，待环境联调
---

# 10-tj-promotion 积分服务实现

> 设计契约：仓库 `docs/specs/tj-promotion-points-service.md`（双向链接；设计目标、边界、验收标准以 Spec 为准，本文只记真实落地情况）。
> 课程参考资料：仓库 `docs/reference/points-ref-1.png` ～ `points-ref-7.png`。

## 实现范围

签到（纯 Redis Bitmap）+ 学习/问答积分（MQ 异步）+ 删除扣分 + 5 渠道预留（课程评论、学习笔记通道先开）+ 积分明细/今日积分/本周积分接口 + 赛季月结（XXL-Job）。排行榜查询接口、笔记/评论生产侧、签到历史归档均明确不做（见 Spec 第 1 节）。

## 真实代码位置

**新模块 `tj-promotion`（com.tianji.promotion，端口 8092，库 `tj_promotion`）**

| 位置 | 内容 |
|---|---|
| `constants/PromotionRedisConstants.java` | Redis 键与 TTL 收口（sign:/points: 全系列） |
| `constants/PromotionMqConstants.java` | 6 个消费队列名（路由键全在 tj-common） |
| `constants/PointsRouteRule.java` | 路由键+bizType → 渠道/分值/动作映射（不信生产侧传分） |
| `enums/PointsChannel.java` | 5 渠道枚举（type/名称/每日上限，签到 0=不限） |
| `service/impl/SignRecordServiceImpl.java` | 签到闭环：SETBIT 判重 → BITFIELD 低位连 1 算连续天数 → 1 分 + 7/14/28 天奖励；加分失败回滚签到位 |
| `service/impl/PointsRecordServiceImpl.java` | 积分核心：流水先行（唯一键裁决）→ Redis 榜/当日累计；扣分先查当月加分流水；异常回滚幂等键 |
| `service/impl/PointsBoardSeasonServiceImpl.java` | 赛季缓存、启动兜底建赛季、月结主流程 |
| `listener/PointsMessageListener.java` | learning.topic 上 6 队列全部预声明（3 生效 + 3 预留） |
| `handler/PointsBoardSeasonJob.java` | `@XxlJob("pointsBoardSeasonJob")` |
| `controller/` | SignRecordController（POST /sign-records）、PointsController（/points/today、/points/records、/points/week 原始 Integer） |
| `src/main/resources/sql/20260719_promotion_points.sql` | 3 张表 DDL |

**存量模块改动**

- 根 `pom.xml`：注册 tj-promotion
- `tj-common/MqConstants.java`：`REPLY_DELETED="reply.deleted"`、`REVIEW_NEW="review.new"`
- `tj-api`：`dto/points/PointsMessage.java`（userId/bizId/bizType/occurredAt，不带分值）；`client/points/PointsClient.java`（GET /points/week → Integer）+ fallback（降级 0 记完整堆栈）+ FallbackConfig 注册
- `tj-learning` 4 处埋点：`LearningRecordServiceImpl.addLearningRecord`（newlyFinished，事务提交后发 section.learned）；`InteractionQuestionServiceImpl.saveQuestion` / `InteractionReplyServiceImpl.saveReply`（审核 PASS 才发 reply.new）；`deleteQuestion` 与两处 `updateHidden`（仅"可见→隐藏/删除"跃迁发 reply.deleted，userId 传作者，un-hide 不发）；`LearningLessonServiceImpl.queryMyPlans` weekPoints 改 Feign 回填

## 验证结果

- 全仓库 `mvn compile -DskipTests`：27 个模块全部 BUILD SUCCESS（2026-07-19）。
- 独立代码评审（对照 Spec 验收条件）：主干 8 条验收逐条通过；发现 3 个严重问题已全部修复（见下节）。
- **未验证**：真实环境联调（Nacos/DB/XXL-Job/网关链路）、签到与积分的运行时行为、error.queue 重放演练——需在环境侧待办完成后进行。

## 评审修复记录（实现与 Spec 的偏差来源）

1. **扣分政策变更**：原 Spec"跨月删除仍扣固定分"废弃。扣分前必须查到当月加分流水（action=1），查不到不扣——防冤扣优先于防刷（PENDING 未加分内容被删不再误扣）。Spec 第 8 节已同步修订。
2. **幂等键失败回滚**：加分/扣分异常时先删 `points:granted:*` 再抛出，保证 error.queue 人工重放可重新入账（修复前重放会被幂等键静默吞掉）。
3. **唯一键先行裁决**：调整为先落流水、唯一键通过后才动 Redis 榜（修复前 Redis 幂等键丢失会导致榜单双加）。
4. 顺带修复：签到置位后加分失败回滚 bit；月结先建赛季刷新缓存再归档；清流水/删旧榜仅当上赛季 end_time 为昨天才执行（防月中人工补跑误清）。

## 环境侧待办（仓库外，联调前必须完成）

- [ ] Nacos：新建 `promotion-service.yaml`（参照 remark-service.yaml）
- [ ] MySQL：建库 `tj_promotion`，执行 `tj-promotion/src/main/resources/sql/20260719_promotion_points.sql`
- [ ] XXL-Job 调度中心：注册 `pointsBoardSeasonJob`，cron `0 11 0 1 * ?`（每月 1 号 00:11）
- [ ] Jenkins：新增 promotion-service 构建任务
- [ ] 联调验证 Spec 第 10 节验收条件 1~9（重点：签到连续奖励、问答审核拦截、删除扣分、预留通道手工发消息入账）

## 已知限制与待确认项

- **PENDING 人工过审的内容永远不得分**（un-hide 置 PASS 但不发 reply.new）：待与用户确认是否需要补发；若补发，注意与"恢复上架不回补"语义的区分。
- **问题被删除时级联删除的回答不扣分**（只扣提问者）：待确认口径。
- 问答三处埋点为事务内发 MQ（学习记录已是 afterCommit）：存在小窗口幻影分风险，后续可统一收敛为提交后发送。
- 每日上限为 check-then-act，极端并发可轻微越顶（影响小，如需严格可改 Lua 原子化）。
- 周榜 TTL 14 天，跨周删除的回扣只作用当前周 key，上周残留自然过期，无实际影响。

## 复用知识

- [[☕ Java笔记/事件驱动积分发放的幂等、防冤扣与重放清单]]（本次评审修复提炼的通用检查清单，双向链接）
