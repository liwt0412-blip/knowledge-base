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

| 位置                                                     | 内容                                                                                                               |
| ------------------------------------------------------ | ---------------------------------------------------------------------------------------------------------------- |
| `constants/PromotionRedisConstants.java`               | Redis 键与 TTL 收口（sign:/points: 全系列）                                                                               |
| `constants/PromotionMqConstants.java`                  | 6 个消费队列名（路由键全在 tj-common）                                                                                        |
| `constants/PointsRouteRule.java`                       | 路由键+bizType → 渠道/分值/动作映射（不信生产侧传分）                                                                                |
| `enums/PointsChannel.java`                             | 5 渠道枚举（type/名称/每日上限，签到 0=不限）                                                                                     |
| `service/impl/SignRecordServiceImpl.java`              | 签到闭环：SETBIT 判重 → BITFIELD 低位连 1 算连续天数 → 1 分 + 7/14/28 天奖励；加分失败回滚签到位                                              |
| `service/impl/PointsRecordServiceImpl.java`            | 积分核心：流水先行（唯一键裁决）→ Redis 榜/当日累计；扣分先查当月加分流水；异常回滚幂等键                                                                |
| `service/impl/PointsBoardSeasonServiceImpl.java`       | 赛季缓存、启动兜底建赛季、月结主流程                                                                                               |
| `listener/PointsMessageListener.java`                  | learning.topic 上 6 队列全部预声明（3 生效 + 3 预留）                                                                          |
| `handler/PointsBoardSeasonJob.java`                    | `@XxlJob("pointsBoardSeasonJob")`                                                                                |
| `controller/`                                          | SignRecordController（POST /sign-records）、PointsController（/points/today、/points/records、/points/week 原始 Integer） |
| `src/main/resources/sql/20260719_promotion_points.sql` | 3 张表 DDL                                                                                                         |

**存量模块改动**

- 根 `pom.xml`：注册 tj-promotion
- `tj-common/MqConstants.java`：`REPLY_DELETED="reply.deleted"`、`REVIEW_NEW="review.new"`
- `tj-api`：`dto/points/PointsMessage.java`（userId/bizId/bizType/occurredAt，不带分值）；`client/points/PointsClient.java`（GET /points/week → Integer）+ fallback（降级 0 记完整堆栈）+ FallbackConfig 注册
- `tj-learning` 4 处埋点：`LearningRecordServiceImpl.addLearningRecord`（newlyFinished，事务提交后发 section.learned）；`InteractionQuestionServiceImpl.saveQuestion` / `InteractionReplyServiceImpl.saveReply`（审核 PASS 才发 reply.new）；`deleteQuestion` 与两处 `updateHidden`（仅"可见→隐藏/删除"跃迁发 reply.deleted，userId 传作者，un-hide 不发）；`LearningLessonServiceImpl.queryMyPlans` weekPoints 改 Feign 回填

## 验证结果

- 全仓库 `mvn compile -DskipTests`：27 个模块全部 BUILD SUCCESS（2026-07-19）。
- 独立代码评审（对照 Spec 验收条件）：主干 8 条验收逐条通过；发现 3 个严重问题已全部修复（见下节）。
- **2026-07-20 问答加分全链路联调通过**：提审提问 → `reply.new` 消息 → 消费 → `points_record` 流水（+5，type=4）→ Redis 当日累计 → `/points/today` 正确返回"课程问答 10/20"（两条流水合计）。同日签到 1 分显示正常。
- **未验证**：签到连续 7/14/28 天奖励、删除扣分链路、预留通道手工发消息、error.queue 重放演练、赛季月结 XXL-Job——需在环境侧待办完成后进行。

## 评审修复记录（实现与 Spec 的偏差来源）

1. **扣分政策变更**：原 Spec"跨月删除仍扣固定分"废弃。扣分前必须查到当月加分流水（action=1），查不到不扣——防冤扣优先于防刷（PENDING 未加分内容被删不再误扣）。Spec 第 8 节已同步修订。
2. **幂等键失败回滚**：加分/扣分异常时先删 `points:granted:*` 再抛出，保证 error.queue 人工重放可重新入账（修复前重放会被幂等键静默吞掉）。
3. **唯一键先行裁决**：调整为先落流水、唯一键通过后才动 Redis 榜（修复前 Redis 幂等键丢失会导致榜单双加）。
4. 顺带修复：签到置位后加分失败回滚 bit；月结先建赛季刷新缓存再归档；清流水/删旧榜仅当上赛季 end_time 为昨天才执行（防月中人工补跑误清）。

## 联调故障记录

### 2026-07-20 启动失败 NoClassDefFoundError: org/redisson/api/RLock

- 现象：IDEA 启动 promotion-service，组件扫描到 `PointsBoardSeasonServiceImpl` 时报 `NoClassDefFoundError: org/redisson/api/RLock`，进程退出。
- 根因：月结用了 tj-common 的 `@Lock`（Redisson 分布式锁），但 `tj-promotion/pom.xml` 照 tj-remark 模板抄——remark 不用 `@Lock` 所以没有 redisson 依赖。**tj-common 里 redisson 是 `provided` scope，不向下游传递**；仓库惯例是每个用到 `@Lock`/`RedissonClient` 的服务自己声明 `org.redisson:redisson`（trade/learning/course/pay 等均如此），版本由根 pom 管理（3.13.6）。
- 修复：`tj-promotion/pom.xml` 在 `spring-boot-starter-data-redis` 后补 `org.redisson:redisson` 依赖（无版本号，继承 dependencyManagement）。
- 验证：`mvn compile -pl tj-promotion -am` BUILD SUCCESS（2026-07-20）；待 IDEA 刷新 Maven 后重启确认。
- 经验：照 remark 模板建新服务时，一旦用 `@Lock` 就必须补 redisson 依赖——编译期不报错，启动期组件扫描才炸。

### 2026-07-20 points_board 建表失败（MySQL 8 保留字）

- 现象：执行 DDL 时 `points_board` 报 1064 语法错误，报错位置指向 `rank` 列；其余 2 张表成功。
- 根因：课程 DDL 写于 MySQL 5.7 时代，`rank` 自 MySQL 8.0.2 起是保留字（窗口函数 `RANK()`）。只给 DDL 加反引号不够——MyBatis-Plus 自动生成的 SQL 不会给列名加反引号，保留字列名到运行时还是会炸。
- 修复：列名 `rank` → `rank_no`，四处同步：DDL、`PointsBoard` PO（字段 rankNo）、`PointsBoardMapper` 自定义 SQL、归档逻辑 `setRankNo`。
- 验证：`mvn compile -pl tj-promotion -am` BUILD SUCCESS（2026-07-20）；DDL 脚本幂等（IF NOT EXISTS），重跑即可补建。
- 经验：引入课程/旧项目 DDL 到 MySQL 8 前，先扫一遍 8.0 新增保留字（rank、rows、system、recursive 等）。

### 2026-07-20 积分页"数据有、响应有、页面显示 0"（前端名称匹配失败）

- 现象：提问后 `points_record` 有流水、`/points/today` 响应里问答渠道 points=10，但前端"获取积分"页"课程问答"恒显示 0/20；签到却能正常显示 1。
- 排查路径：先排除 MQ（日志显示消息已消费、流水 INSERT 成功，且幂等键 SETNX 在落库之前，流水成功即证明 Redis 可达）→ 再查接口响应（数据正确）→ 最后定位前端。
- 根因：前端页面写死了一张渠道表（自有名称和上限），**按名称**去接口返回里匹配分值，匹配不上落默认 0。前端名称来自黑马旧版枚举 `PointsRecordType`（课程问答/课程笔记/课程评价），与本仓库 `PointsChannel` 的 desc（问答回答/学习笔记/课程评论）不一致；"每日签到"恰好同名所以能显示。前端写死上限（签到 2、评价 999）也与后端（0=不限、10）不同，进一步证明页面未直接渲染接口数据。
- 修复：`PointsChannel` 三个 desc 对齐前端（课程评价/课程问答/课程笔记），`PointsRecord`/`PointsRecordVO`/DDL 注释同步；**type 编码不动**（表里已有数据按本仓库编码落库）。重启 learning-service 后页面正常显示 10/20。
- 经验：①"数据有但页面没有"的排查顺序：**接口响应 → 页面渲染逻辑 → 匹配字段**，不要在后端和 MQ 里空转；②旧版课程枚举 `PointsRecordType` 编码与本仓库**完全不同**（签到 2/学习 1/问答 3/笔记 4/评价 5 vs 本仓库 1/2/3/4/5 对应签到/学习/评价/问答/笔记）——拿旧字典读新表会张冠李戴（type=4 旧=笔记、新=问答），接入旧课程代码或前端契约时必须先核对枚举编码映射。

## 功能范围核实（2026-07-20，对照课程大纲 6 类行为）

- 签到 ✅、提问/回答 ✅（含删除扣分，超出大纲）、学习-视频 ✅、**学习-考试 ✅**。
- 考试与视频**同一条积分链路**：`SectionType` 只有 VIDEO/EXAM 两种，`LearningRecordServiceImpl.isSectionFinished` 对考试小节"提交即完成"，首次完成统一走 `section.learned` 消息 +10（课程学习渠道）。tj-exam 只是题库管理，学员侧"做考试"走 tj-learning 学习记录提交，无需单独接积分。
- 写笔记/笔记被采集/评论：通道预留（队列、监听器、路由规则齐备），等功能本体上线只发消息即可接入。
- 结论：大纲要求范围全部落地，无缺口。

## 重大变更：2026-07-20 迁入 tj-learning

- 起因：前端约定积分/签到接口归属 learning 服务（`/ls/**`），独立 tj-promotion 模块废弃。
- 改动：24 个 Java 文件平移至 `com.tianji.learning.*`（`PromotionMqConstants`→`PointsMqConstants`、`PromotionRedisConstants`→`PointsRedisConstants`，其余类名不变）；Redis key 前缀与 MQ 队列名字面值原样保留，已有签到数据/榜单/未消费消息无缝衔接。`LearningLessonServiceImpl` 的 weekPoints 由 Feign（PointsClient）改为本地 `IPointsRecordService.queryWeekPoints()`，异常降级 0；tj-api 删除 PointsClient 及 fallback（PointsMessage 保留）。根 pom 移除 tj-promotion，网关删 `/prs/**` 路由，learning bootstrap 补 `shared-xxljob.yaml`，DDL 迁至 `tj-learning/src/main/resources/sql/20260719_learning_points.sql`（库改 tj_learning）。编译 BUILD SUCCESS。
- 经验：新模块归属先和前端路由约定对齐再动手；MQ 队列名/Redis key 在跨服务迁移时保持字面值不变可省掉数据迁移。

## 环境侧待办（仓库外，联调前必须完成）

> 2026-07-20 迁入 tj-learning 后以下为准（旧 promotion 项作废：promotion-service.yaml 可删、Jenkins promotion 任务不需要了）。

- [ ] Nacos：`learning-service.yaml` 补 XXL-Job 执行器端口（原 promotion 的 9992 已释放，直接复用；若与其他服务冲突再顺延）：

```yaml
xxl-job:
  executor:
    # 同一台机器同时启动多个 XXL-Job 执行器时，端口必须不同
    port: 9992
```

- [ ] MySQL：在 `tj_learning` 库执行 `tj-learning/src/main/resources/sql/20260719_learning_points.sql`（旧 `tj_promotion` 库若有数据可放弃——流水月底清零、赛季榜尚无数据）
- [ ] XXL-Job 调度中心：`pointsBoardSeasonJob`（cron `0 11 0 1 * ?`）改绑 learning-service 执行器，原 promotion 执行器任务删除
- [ ] RabbitMQ：原 `error.promotion-service.queue` 若滞留消息人工重放/清理；`promotion.points.*.queue` 名字未变，learning 启动后自动接管消费
- [ ] 联调验证 Spec 第 10 节验收条件 1~9（重点：签到连续奖励、问答审核拦截、删除扣分、预留通道手工发消息入账）

## 已知限制与待确认项

- **PENDING 人工过审的内容永远不得分**（un-hide 置 PASS 但不发 reply.new）：待与用户确认是否需要补发；若补发，注意与"恢复上架不回补"语义的区分。
- **问题被删除时级联删除的回答不扣分**（只扣提问者）：待确认口径。
- 问答三处埋点为事务内发 MQ（学习记录已是 afterCommit）：存在小窗口幻影分风险，后续可统一收敛为提交后发送。
- 每日上限为 check-then-act，极端并发可轻微越顶（影响小，如需严格可改 Lua 原子化）。
- 周榜 TTL 14 天，跨周删除的回扣只作用当前周 key，上周残留自然过期，无实际影响。

## 复用知识

- [[☕ Java笔记/事件驱动积分发放的幂等、防冤扣与重放清单]]（本次评审修复提炼的通用检查清单，双向链接）
- [[☕ Java笔记/前后端联调排错-接口有数据但页面不显示]]（2026-07-20 页面显示 0 故障提炼的联调排查路径与枚举映射核对清单，双向链接）
