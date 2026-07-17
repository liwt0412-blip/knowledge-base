---
tags:
  - Tianji
  - 学习记录
  - Redis
  - 合并写
  - 缓存一致性
status: implemented-unverified
created: 2026-07-15
---

# 播放进度 Redis 合并写与读缓存

> 状态：设计方案，尚未在当前项目完成实现、集成测试和压测。本文不得作为“已经上线并取得性能收益”的项目事实使用。

## 一、问题与优化边界

播放过程中，前端会周期性提交视频位置。当前实现每次请求都会查询并更新 `learning_record`，普通播放进度是学习记录链路中最频繁的写分支。

各分支频率和一致性要求不同：

| 分支 | 频率 | 是否允许延迟落库 | 设计选择 |
|---|---:|---:|---|
| 首次创建小节记录 | 每小节一次 | 不建议 | 同步写数据库 |
| 普通视频 `moment` 更新 | 播放期间周期发生 | 可以 | Redis 合并，延迟刷盘 |
| 视频首次完成 | 每小节最多一次 | 不可以 | 数据库事务和条件更新 |
| 考试完成 | 每小节有限次数 | 不可以 | 数据库事务和幂等校验 |
| 查询课程学习进度 | 读请求 | 可以读缓存 | Hash 整体读取 |

结论：只优化普通 `moment` 更新，不把全部学习记录逻辑异步化。

## 二、为什么选择一个课表一个 Hash

数据关系：

```text
learning_lesson.id（lessonId）
        ↓
learning_record.lesson_id
        ↓
每个sectionId对应一条学习记录
```

访问特征：

```text
提交进度：读写单个sectionId
查询课程进度：读取lessonId下全部sectionId
```

Redis Hash与该访问方式一致：

```text
Key：learning:record:{lessonId}
HashKey：sectionId
HashValue：学习记录缓存JSON
```

示例：

```text
learning:record:2076330661992062977

__loaded -> 1
42 -> {"id":1,"moment":242,"finished":true,"version":8,"updatedAt":1784109600000}
43 -> {"id":2,"moment":20,"finished":false,"version":3,"updatedAt":1784109500000}
```

不直接使用裸 `lessonId` 作为 Key，避免与其他业务缓存冲突。HashKey 直接使用小节 ID 即可，不需要重复写 `sectionId:` 前缀。

## 三、读缓存流程

`GET /learning-records/course/{courseId}` 仍先校验当前用户课表归属，再按 `lessonId` 读取记录缓存。

```text
查询当前用户的lesson
        ↓
读取 learning:record:{lessonId}.__loaded
   ├─ 存在 → HGETALL并转换为LearningRecordDTO
   └─ 不存在
        → 查询数据库全部学习记录
        → 读取Hash中可能存在的未刷盘热数据
        → 相同sectionId的moment取较大值
        → 批量回填Hash
        → 设置__loaded=1和TTL
        → 返回
```

必须保留 `__loaded`：写请求可能只写入一个小节，Hash 中有数据不代表整门课程的记录已经完整缓存。

数据库查询为空时也写 `__loaded=1`，防止空结果反复穿透数据库。

## 四、普通播放进度写入

普通视频更新只改变 `moment` 和最后更新时间：

```text
校验当前用户、课表和参数
        ↓
读取/初始化对应小节记录
        ↓
Lua：newMoment > oldMoment才更新
        ↓
增加version
        ↓
第一次变脏时加入dirty ZSet
        ↓
请求返回
```

禁止简单执行“Java先读Redis，再判断，再HSET”，否则乱序并发请求可能让播放位置回退。

## 五、dirty刷盘设计

缓存与刷盘任务分开：

```text
Hash：learning:record:{lessonId}
用途：提供最新状态和读缓存

ZSet：learning:record:dirty
Member：lessonId:sectionId
Score：flushAt
用途：记录尚未落库的数据
```

第一次变脏时使用 `ZADD NX` 设置刷盘时间。后续请求只覆盖 Hash，不持续延后第一次刷盘时间，避免用户持续播放时长时间不落库。

刷盘步骤：

1. 查询到期 dirty 成员。
2. 获取短期处理租约，避免多实例重复处理。
3. 读取 Hash 中的 `moment/version`。
4. 批量执行数据库更新，`moment` 使用 `GREATEST` 防止回退。
5. 当前版本仍等于已刷盘版本时清除 dirty；版本已变化则再次调度。
6. 保留 Hash 作为读缓存，不因刷盘成功而删除。

项目若采用 RabbitMQ，MQ更适合发布“小节首次完成”事件；普通位置仍以 Redis 最新状态为主。仅用 MQ 逐条更新数据库只能削峰，不能减少写次数。

## 六、首次完成必须同步落库

视频达到完成比例时执行数据库条件更新：

```sql
UPDATE learning_record
SET finished = 1,
    finish_time = #{finishTime},
    moment = GREATEST(COALESCE(moment, 0), #{moment})
WHERE lesson_id = #{lessonId}
  AND section_id = #{sectionId}
  AND finished = 0;
```

只有影响行数为 `1` 才表示首次完成，才能在同一事务中执行：

```text
learning_lesson.learned_sections + 1
更新latest_section_id/latest_learn_time
判断课程是否全部完成
```

事务成功后再把缓存 `finished` 更新为 `true`，或失效对应字段使下一次读取回源。数据库事务失败时不能让 Redis 单独保留完成状态。

## 七、与当前代码的映射

当前主要修改点位于：

```text
tj-learning/src/main/java/com/tianji/learning/service/impl/LearningRecordServiceImpl.java
```

建议职责拆分：

```text
queryLearningRecordByCourse
  → 课表归属查询 + 完整读缓存

addLearningRecord
  → 业务分支协调

普通moment更新
  → Redis原子合并 + dirty调度

首次创建/首次完成/考试
  → 数据库事务

后台刷盘组件
  → dirty拉取、租约、批量更新、版本确认
```

不要把 Redis、MQ、SQL、完成判断全部继续堆进一个 Service 方法，应抽取明确的缓存组件和刷盘组件。

## 八、数据库与接口前提

- `(lesson_id, section_id)` 最终应有唯一约束，防止并发首次创建产生重复记录。
- `moment`、`duration` 使用统一单位，前端在 `duration <= 0` 时不应上报完成判断。
- 服务端不能相信前端 `lessonId`，仍需校验课表属于当前用户且未失效。
- 数据库仍是 `finished`、`finishTime`、`learnedSections` 和课程状态的最终事实。

## 九、失效与清理

以下场景删除整个课表缓存，并清除对应 dirty 任务：

- 用户删除失效课程；
- 退款事件删除课程权益；
- 课表重建或数据修复；
- 缓存结构版本升级。

Hash TTL 应大于最大刷盘延迟、重试和故障恢复窗口。定时任务清理“dirty存在但Hash不存在”的孤儿成员。

## 九点一、当前实现与排错方法

当前项目已实现第一版 Redis Hash + ZSet 调度代码，但尚未完成真实Redis集成测试、并发压测和故障演练，因此只能称为“已编码、待验证”，不能宣称已经获得具体性能收益。

当前Key：

```text
Hash：learning:record:{lessonId}
ZSet：learning:record:flush
Lock：lock:learning:record:flush:{lessonId}:{sectionId}
```

Redis客户端中看到的 `learning (2)` 是按冒号分组后的命名空间，不是一个真实Key。Hash只剩一个小节并被删除后，整个Hash会自动消失；延迟刷库成功后ZSet成员被移除，ZSet为空时也会消失。因此排查时必须使用真实lessonId：

```redis
TTL learning:record:2076330661992062977
HGETALL learning:record:2076330661992062977
ZRANGE learning:record:flush 0 -1 WITHSCORES
```

排查顺序是：

```text
1. 看Hash是否存在、TTL是否正常
2. 看ZSet是否还有待刷库member和score
3. 看MySQL学习记录的moment是否已经刷入
4. 看刷盘日志是否出现成功、失败或重试
5. 看是否是首次完成后主动清理缓存
```

这个判断方法可复用于所有“Hash保存最新状态、ZSet保存待处理任务、MySQL保存最终事实”的高并发合并写场景。

## 十、分阶段实施

### 阶段1：正确性

- 数据库唯一约束或等价幂等措施。
- 首次完成使用条件更新。
- 普通进度只允许前进。
- 完成状态与累计小节数保持事务一致。

### 阶段2：Redis读缓存

- 一个lesson一个Hash。
- 完整加载标记和空结果缓存。
- 写缓存与数据库回源数据正确合并。

### 阶段3：合并写

- Lua原子更新。
- dirty ZSet、租约和批量刷盘。
- 刷盘失败重试和服务重启恢复。

### 阶段4：验证

- 单元测试：进度不回退、完成只累计一次。
- 并发测试：乱序和重复请求。
- 故障测试：Redis短暂不可用、刷盘实例宕机。
- 压测：对比数据库写QPS、接口延迟、缓存命中率和刷盘延迟。

## 十一、真实性边界与面试表达

当前只能表述为：

> 我针对播放进度高频更新分析并设计了 Redis Hash 合并写方案。设计上以课表 ID 聚合、小节 ID 作为 HashKey，使单小节更新和整门课程读取都能命中同一份缓存；普通播放位置延迟合并落库，首次完成仍由数据库事务保证幂等。目前该方案处于设计阶段，尚未完成压测，不能宣称具体性能收益。

完成编码、集成测试和压测后，才能将状态从 `design` 修改为 `implemented/verified`，并记录真实指标。

## 关联笔记

- [[03-学习记录与学习计划接口设计]]
- [[☕ Java笔记/高频最新状态的Redis合并写模式]]
- [[☕ Java笔记/Java全套代码质量与优化规范]]
