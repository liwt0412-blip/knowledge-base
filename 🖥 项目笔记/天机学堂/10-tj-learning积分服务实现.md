---
tags: [天机学堂, tj-learning, 积分, 实施记录]
created: 2026-07-19
status: 已实现，待环境联调
---

# 10-tj-learning 积分服务实现

> 设计契约：仓库 `docs/specs/tj-learning-points-service.md`（双向链接；设计目标、边界、验收标准以 Spec 为准，本文只记真实落地情况）。
> 课程参考资料：仓库 `docs/reference/points-ref-1.png` ～ `points-ref-7.png`。
> 注意：积分功能最初建于独立 `tj-promotion` 模块，2026-07-20 已迁入 `tj-learning`（见文末"重大变更"节）；2026-07-22 起 `tj-promotion` 模块名被**优惠券服务**复用，见 [[11-tj-promotion优惠券服务实现]]，两者不要混淆。

## 实现范围

签到（纯 Redis Bitmap）+ 学习/问答积分（MQ 异步）+ 删除扣分 + 5 渠道预留（课程评论、学习笔记通道先开）+ 积分明细/今日积分/本周积分接口 + 赛季月结（XXL-Job）。排行榜查询接口、笔记/评论生产侧、签到历史归档均明确不做（见 Spec 第 1 节）。

## 真实代码位置

> ⚠️ 本节描述的是迁入前的旧 `tj-promotion` 模块，**已作废**；当前代码在 `tj-learning`（com.tianji.learning），见文末"重大变更：2026-07-20 迁入 tj-learning"一节。

**~~新模块 `tj-promotion`（com.tianji.promotion，端口 8092，库 `tj_promotion`）~~（历史记录）**

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
| `handler/PointsBoardSeasonJob.java`                    | 月结任务链三个 handler：`pointsBoardSeasonJob`（准备）→ `pointsBoardArchiveJob`（归档）→ `pointsBoardCleanJob`（清理） |
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

- [x] MySQL：在 `tj_learning` 库执行 `tj-learning/src/main/resources/sql/20260719_learning_points.sql`（旧 `tj_promotion` 库若有数据可放弃——流水月底清零、赛季榜尚无数据）
- [x] XXL-Job 调度中心：`pointsBoardSeasonJob`（cron `0 11 0 1 * ?`）改绑 learning-service 执行器，原 promotion 执行器任务删除
- [x] RabbitMQ：原 `error.promotion-service.queue` 若滞留消息人工重放/清理；`promotion.points.*.queue` 名字未变，learning 启动后自动接管消费
- [x] 联调验证 Spec 第 10 节验收条件 1~9（重点：签到连续奖励、问答审核拦截、删除扣分、预留通道手工发消息入账）

## 2026-07-21 学霸积分榜查询接口落地（Spec 3.5/3.6）

- **背景**：Spec 第 1 节原列"排行榜查询接口下期实现"，本期补齐两个纯查询接口，积分链路本身零改动。数据底座早已就绪（当前赛季 Redis ZSet、月结归档 `points_board` 前 100、赛季表），只缺查询出口。
- **新增代码（`tj-learning`，7 个文件）**：
  - `controller/PointsBoardController.java`：`GET /boards`（榜单+我的排名）、`GET /boards/seasons/list`（赛季历史列表）；
  - `service/IPointsBoardService.java` + `service/impl/PointsBoardServiceImpl.java`：榜单查询核心；
  - `domain/query/PointsBoardQuery.java`（继承 PageQuery + season）、`domain/vo/PointsBoardVO.java`、`PointsBoardItemVO.java`、`PointsBoardSeasonVO.java`；
  - `IPointsBoardSeasonService.querySeasonList()`（实现类补方法，全部赛季按 id 倒序）。
- **关键设计决策**：
  - 数据源分叉：`season` 空/0 或等于当前赛季 id → Redis ZSet 实时榜；指定历史赛季 → `points_board` 归档表（当前赛季绝不能查表，月底才归档）；
  - 前 100 上限：Redis 分支分页窗口与 [0,100) 取交集，窗口外返回空列表不报错；DB 分支归档表天然只有前 100；
  - 未上榜语义：`rank=null, points=0`（待前端确认）；
  - 姓名回填：`UserClient.queryUserByIds` 一次批量查询（防 N+1），降级返回空列表时全部显示"未知用户"，不阻断榜单；
  - 赛季列表返回**全部赛季含当前**、最新在前，前端下拉统一用一个接口，选当前赛季时 `/boards` 自动走实时榜分支；
  - 赛季名沿用 `yyyy-MM`（课程示例"第一赛季"不采用）；赛季 id 按数字返回（课程文档 `"110"` 字符串写法是文档风格）；
  - 响应为课程契约自定义结构 `{rank, points, boardList}`，**不用** PageDTO。
- **Spec 同步**：第 1 节范围修订 + 新增 3.5（榜单）、3.6（赛季列表）契约。
- **验证状态**：代码完成但**未编译验证**——本机命令行无 JDK（JAVA_HOME 未配、常见目录无安装、IDEA 内置 JBR 未找到；Maven 存在于 `~/.m2/wrapper/dists` 但缺 JAVA_HOME 无法运行），待 IDEA `Ctrl+F9` 构建 `tj-learning` 并重启后自测：`GET /ls/boards/seasons/list` 拿赛季 id → `GET /ls/boards?season=` 验证历史分支 → 无参调 `/boards` 验证当前赛季实时榜。
- **环境备忘**：本机命令行编译验证不可用，Maven 在 `C:\Users\ALIENWARE\.m2\wrapper\dists\apache-maven-3.9.14-bin\...\bin\mvn.cmd`，配好 JAVA_HOME 指向 IDEA 所用 JDK 后可用。

### 2026-07-21 业务变更：历史赛季"我的排名"任意名次可查（全量归档）

- **需求**：查询榜单/历史榜单时，当前用户 100 名开外也要显示真实排名，不再按未上榜隐藏。
- **分析**：当前赛季分支（Redis `ZRevRank`）天然不受前 100 限制，零改动；瓶颈在历史赛季——月结原只归档前 100，100 名开外无数据可查。
- **改动**：
  1. `archiveSeasonBoard`：`reverseRangeWithScores(key, 0, 99)` → `(key, 0, -1)` 全量归档；
  2. `queryHistorySeasonBoard`：归档全量后展示层自行截断前 100（pageSize 超剩余名额裁尾部）；"我的排名"查全量表，任意名次可返回；
  3. **`rank_no` 由 `tinyint` 改 `int`**：tinyint 最大 255，全量归档后第 256 名写入溢出——只存前 100 时掩盖了这个问题。DDL 文件、Spec、PO 注释同步；已建表需手动 `ALTER TABLE points_board MODIFY COLUMN rank_no int NOT NULL`（`CREATE TABLE IF NOT EXISTS` 不改已有表列类型）。
- **最终语义**：`boardList` 仍只显示前 100；`rank/points` 当前与历史赛季都返回真实名次（可 >100）；整赛季一分未得才 `rank=null, points=0`。
- **经验**：①展示截断与数据归档是两件事——"页面只显示前 N"不等于"数据只存前 N"，归档范围要按"历史还要回答什么问题"来定（本次：还要回答"我排第几"）；②数值类型容量要按业务的未来上限选型（名次跟着用户量走，tinyint 的 255 上限在需求变更时立即变成炸弹），DDL 评审应把"该列的最大可能值"列为检查项。

## 海量存储与物理分表实施（2026-07-21，已落地）

> 全量归档后 `points_board` 年行数 = 月得分用户 × 12。经讨论最终采用**物理分表方案**（对齐课程思路并补齐工程细节），已于当日实施。原"分区表首选"预案及分区 vs 分表决策对比保留在下方备查——若未来赛季间要求强隔离或单库容量到顶，仍可按预案升级。

**实施要点（真实代码）**：

- **分表结构**：`points_board_{seasonId}` 每赛季一张表 + `points_board_template` 模板表（永不插数据、永不删除，新分表 `CREATE TABLE IF NOT EXISTS ... LIKE template` 克隆结构含全部索引）；逻辑名 `points_board` 物理上不存在，仅作 PO `@TableName` 锚点；
- **表名路由**：`PointsBoardTableContext`（ThreadLocal）+ MyBatis-Plus `DynamicTableNameInnerInterceptor`；拦截器注册在 learning 自己的 `LearningMybatisConfig`（tj-common 的 `MybatisPlusInterceptor` 带 `@ConditionalOnMissingBean` 自动让位），**链顺序：动态表名 → 分页 → 自动填充**——先改表名分页才基于新表生成 count SQL，反了 count 打逻辑表；
- **版本坑（2026-07-21 排错，已验证 jar）**：MP 3.4.3 的 `DynamicTableNameInnerInterceptor` 只有无参构造 + `setTableNameHandlerMap(Map<String, TableNameHandler>)` 一个注册入口，**没有** `setTableNameHandler`、也没有 handler 构造器（均为 3.5.x API）；Map 按表名精确路由，只挂 `"points_board"` 即可，未命中表自动放行，handler 内无需再判表名。真实签名经解析本地 `.m2` jar 的 class 常量池确认；
- **ThreadLocal 防串表**：所有入口统一 `withSeason()` 收口 try/finally remove——Tomcat 线程池复用，不清理会让下个请求读到上个请求的表名（偶发写错表、难复现）；未设路由访问 `points_board` 直接报表不存在，是**有意的"失败要响"**，漏包 withSeason 测试期即暴露；
- **写入路径**：归档插入显式 `${tableName}` 传参（`insertIgnoreBatch(tableName, list)`），低频内部链路不依赖拦截器改写 DML；月结归档前 `createTableIfAbsent` 幂等建表，无需新增定时任务；**分批 500 行/批**（2026-07-22 修订，原单条全量 INSERT——防十万级用户撞 max_allowed_packet / binlog 突刺，批间无事务、INSERT IGNORE 幂等保证断点重跑安全）；
- **迁移**：`sql/20260721_points_board_sharding.sql`——rank_no 改 int（幂等）→ 原单表 RENAME 为 points_board_1 → 建模板表；
- **XXL-Job 任务链（2026-07-22 修订为分片广播）**：月结三段子任务链——`pointsBoardSeasonJob`（主任务 cron 不变：建新赛季+刷新缓存+幂等建上赛季分表，路由"第一个"）→ 子任务 `pointsBoardArchiveJob`（**分片广播**：各实例按 `XxlJobHelper.getShardIndex/getShardTotal` 切 ZSet 排名区间归档，rank 全局连续；非分片触发 shardTotal=1 等价全量）→ 子任务 `pointsBoardCleanJob`（清流水+删旧榜；分片广播下每个分片完成都会触发清理，**数量闸门**：分表行数 ≥ ZSet 成员数才放行，先触发的被拦住等下一分片；`@Lock` 与月末窗口守卫保留）；归档/清理调度类型"无"；复合入口 `settleSeason()` 保留供手动全量补跑；
- **已知边界**：跨赛季"我的所有历史"查询当前接口不需要；将来需要时 UNION ALL 或加 `user_season_points` 汇总表。

**原预案备查（未采用路径）**：

- 分区表（PARTITION BY RANGE (season)）：分区裁剪、月结 Job 幂等 ADD PARTITION、DROP PARTITION 清理红利、主键需含分区键、不用 MAXVALUE 兜底；优势是应用零改动、天然支持跨赛季查询、无 DDL 权限问题；
- 分区 vs 分表决策对比：分表翻盘的三个条件——赛季间强物理隔离（合规独立下线）、单实例容量到顶（分库范畴）、查询永远单赛季不跨片；
- 冷热分级：主库留近 12~24 赛季，更老迁归档库/OLAP，保留策略需产品确认；
- 终选分库分表：ShardingSphere-JDBC 按 user_id 分片，见 [[☕ Java笔记/分库分表选型-演进阶梯与ShardingSphere]]。

## 月结可靠性分析：Redis 未持久化但数据被清理的风险（2026-07-21）

**顺序保护（正常失败路径不丢数据）**：`settleSeason()` 步骤刻意排序为 建新赛季+刷新缓存 → 归档 → 清流水+删旧榜。归档抛异常则删除不执行，Job 标失败可重跑（INSERT IGNORE + IF NOT EXISTS 幂等）；删除失败则旧榜残留，重跑去重后补删；破坏性步骤仅当上赛季 end_time 恰为昨天才执行。Job 完全不跑也安全——榜 key 无 TTL，数据在 Redis 静候，`currentSeasonId()` 查库兜底建赛季。

**三个真实风险窗口**：

1. **最大风险：Redis 当月唯一副本**。赛季榜整月只在 Redis（DB 无副本），月中实例重启无 AOF / 主从切换丢未同步数据 / maxmemory 逐出 `points:board:*` → 月结归档空榜且流程"正常"走完，无声丢失。这是架构取舍的固有代价，非月结逻辑 bug。加固：AOF everysec、逐出策略隔离 points:*/sign:*；隐形兜底是 `points_record` 月底才清，当月可拿流水重放重建榜单；
2. **毫秒级竞态**：Job 先刷新赛季缓存再归档；恰在刷新前读到旧赛季 id、归档读 ZSet 之后才 ZINCRBY 的请求，分会落旧榜躲过归档后被删——损失为个别用户少几分，弱一致场景接受；
3. **Job 未改绑执行器**（环境待办项）：Job 不跑不丢数据但榜单不翻月，是当前最易落地的风险。

**加固措施（按性价比）**：① Redis AOF + 逐出策略隔离；② XXL-Job 失败告警 + 每月 1 号人工核对分表行数；③ 重方案（一般不值）：月结前快照旧榜到 staging 表。

## 已知限制与待确认项

- **PENDING 人工过审的内容永远不得分**（un-hide 置 PASS 但不发 reply.new）：待与用户确认是否需要补发；若补发，注意与"恢复上架不回补"语义的区分。
- **问题被删除时级联删除的回答不扣分**（只扣提问者）：待确认口径。
- 问答三处埋点为事务内发 MQ（学习记录已是 afterCommit）：存在小窗口幻影分风险，后续可统一收敛为提交后发送。
- 每日上限为 check-then-act，极端并发可轻微越顶（影响小，如需严格可改 Lua 原子化）。
- 周榜 TTL 14 天，跨周删除的回扣只作用当前周 key，上周残留自然过期，无实际影响。

## 复用知识

- [[☕ Java笔记/事件驱动积分发放的幂等、防冤扣与重放清单]]（本次评审修复提炼的通用检查清单，双向链接）
- [[☕ Java笔记/前后端联调排错-接口有数据但页面不显示]]（2026-07-20 页面显示 0 故障提炼的联调排查路径与枚举映射核对清单，双向链接）
- [[☕ Java笔记/热冷分离-实时榜Redis与历史归档表的双数据源查询]]（2026-07-21 积分榜接口提炼的读路径热冷分流模式，双向链接）
- [[☕ Java笔记/Bitmap标志位存储模式-连签统计与验重]]（2026-07-21 签到/兑换码提炼的位图选型四问框架与键设计，双向链接）
