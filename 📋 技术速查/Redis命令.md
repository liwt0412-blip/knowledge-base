---
tags:
  - redis
date: 2026-06-04
---
# Redis 常用命令速查（含 Spring Data Redis Java 对应方法）

> **说明**：以下Java方法基于 `org.springframework.data.redis.core.RedisTemplate`（或 `StringRedisTemplate`）。
> 假设 bean 名为 `redisTemplate`，如果用的是 `StringRedisTemplate` 则需自行调整泛型。
> 所有 `opsForXxx()` 方法返回的都是对应的操作类（ValueOperations、HashOperations 等），建议用局部变量接一下。

---

## 📌 通用命令（所有数据类型通用）

| 命令 | 作用 | Java 对应方法 | 注意事项 |
|------|------|---------------|---------|
| `KEYS pattern` | 列出所有匹配的key，如 `KEYS *` | `redisTemplate.keys(pattern)` | **生产环境慎用！** 会阻塞Redis单线程，数据量大时卡死。生产用 `SCAN` 替代 |
| `SCAN cursor [MATCH pattern] [COUNT count]` | 游标式遍历key，每次返回一批 | 无直接封装，需通过 `RedisConnection.scan()` 操作底层连接 | 游标式非阻塞，`cursor=0` 开始，返回的cursor为0表示遍历完毕 |
| `EXISTS key` | 判断key是否存在，返回1/0 | `redisTemplate.hasKey(key)` | — |
| `TYPE key` | 返回key的数据类型（string/list/hash/set/zset） | `redisTemplate.type(key)` | — |
| `DEL key [key...]` | 删除一个或多个key | `redisTemplate.delete(key)` / `redisTemplate.delete(keys)` | 返回删除的数量 |
| `EXPIRE key seconds` | 设置key的过期时间（秒） | `redisTemplate.expire(key, timeout, TimeUnit.SECONDS)` | 过期后自动删除，常用于验证码、缓存 |
| `TTL key` | 查看key剩余存活秒数 | `redisTemplate.getExpire(key)` | `-1` 表示永不过期，`-2` 表示已过期/不存在 |
| `RENAME key newkey` | 重命名key | `redisTemplate.rename(oldKey, newKey)` | 如果newkey已存在，会覆盖，慎用 |
| `SELECT index` | 切换数据库（0-15，默认16个库） | 不推荐代码中切换，一般在 `application.yml` 配置 `spring.data.redis.database=0` | 生产环境尽量只用 `db0`，多库不利于管理 |
| `FLUSHDB` | 清空当前库所有key | `redisTemplate.getConnectionFactory().getConnection().flushDb()` | **!!! 生产环境绝不执行 !!!** |
| `DBSIZE` | 查看当前库key总数 | `redisTemplate.getConnectionFactory().getConnection().dbSize()` | — |

---

## 📦 String（字符串）— 最基础的数据类型

value最大512MB，可存文本、数字、JSON序列化字符串、二进制数据。

| 命令 | 作用 | Java 对应方法 | 注意事项 |
|------|------|---------------|---------|
| `SET key value` | 设置key-value | `redisTemplate.opsForValue().set(key, value)` | 用 `StringRedisTemplate` 时value类型为String |
| `SET key value EX 10` | 设置key-value并10秒后过期 | `redisTemplate.opsForValue().set(key, value, 10, TimeUnit.SECONDS)` | EX=秒，PX=毫秒 |
| `SET key value NX` | 只在key不存在时设置（分布式锁常用） | `redisTemplate.opsForValue().setIfAbsent(key, value)` | NX=Not eXists，返回true/false |
| `SET key value XX` | 只在key已存在时设置（更新） | 无直接等价，可先 `hasKey` 再 `set`，或通过连接层操作 | XX=eXists |
| `GET key` | 获取value | `redisTemplate.opsForValue().get(key)` | key不存在返回null |
| `MSET k1 v1 k2 v2` | 批量设置，原子操作 | `redisTemplate.opsForValue().multiSet(Map.of(k1, v1, k2, v2))` | 比逐条SET快，减少网络开销 |
| `MGET k1 k2 k3` | 批量获取 | `redisTemplate.opsForValue().multiGet(List.of(k1, k2, k3))` | 返回List，顺序对应key |
| `INCR key` | value +1（原子自增） | `redisTemplate.opsForValue().increment(key)` | key不存在则从0开始。**value必须是整数，否则抛错** |
| `INCRBY key n` | value +n | `redisTemplate.opsForValue().increment(key, delta)` | delta可为负数 |
| `DECR key` | value -1 | `redisTemplate.opsForValue().decrement(key)` / `increment(key, -1)` | 同上 |
| `SETEX key seconds value` | SET + EXPIRE 合并命令 | `redisTemplate.opsForValue().set(key, value, Duration.ofSeconds(10))` | 等同于 `SET key value EX seconds` |
| `SETNX key value` | 只在key不存在时设置 | `redisTemplate.opsForValue().setIfAbsent(key, value)` | 同 SET NX |
| `GETSET key value` | 设置新值并返回旧值 | `redisTemplate.opsForValue().getAndSet(key, value)` | 原子操作，用于更新计数器时获取旧值 |
| `STRLEN key` | 获取value的字节长度 | `String.valueOf(redisTemplate.opsForValue().get(key)).length()` | 中文一个UTF-8字符占3字节（get后length()是字符数） |
| `APPEND key value` | 在原有value后追加 | `redisTemplate.opsForValue().append(key, value)` | key不存在则等同于SET |

### ⚠️ String注意事项
- **JSON序列化**：存对象时用JSON字符串，但更新某个字段要取出来反序列化再改回去，可用Hash代替
- **INCR操作**：每个Redis单节点每秒能扛10万+ INCR，但**极端并发下会超卖**，高并发扣库存还需要配合Lua脚本或Redisson
- **大key问题**：value超过10MB就是大key，可能导致Redis阻塞、主从同步延迟

---

## 🗂️ Hash（哈希）— 适合存对象/实体

类似Java的 `Map<String, Map<field, value>>`，适合存一个对象的各种属性。

| 命令 | 作用 | Java 对应方法 | 注意事项 |
|------|------|---------------|---------|
| `HSET key field value` | 设置hash中一个字段 | `redisTemplate.opsForHash().put(key, field, value)` | 字段已存在则覆盖 |
| `HGET key field` | 获取hash中一个字段 | `redisTemplate.opsForHash().get(key, field)` | — |
| `HMSET key f1 v1 f2 v2` | 批量设置 | `redisTemplate.opsForHash().putAll(key, Map.of(f1,v1, f2,v2))` | 参数是Map |
| `HMGET key f1 f2` | 批量获取字段 | `redisTemplate.opsForHash().multiGet(key, List.of(f1, f2))` | 返回List，不存在的为null |
| `HGETALL key` | 获取所有字段和值 | `redisTemplate.opsForHash().entries(key)` | 返回 `Map<HK, HV>`。**大hash慎用！** |
| `HKEYS key` | 获取所有字段名 | `redisTemplate.opsForHash().keys(key)` | 同慎用 |
| `HVALS key` | 获取所有值 | `redisTemplate.opsForHash().values(key)` | 同慎用 |
| `HDEL key field [field...]` | 删除一个或多个字段 | `redisTemplate.opsForHash().delete(key, field1, field2)` | 可变参数 |
| `HEXISTS key field` | 判断字段是否存在 | `redisTemplate.opsForHash().hasKey(key, field)` | — |
| `HLEN key` | 获取字段数量 | `redisTemplate.opsForHash().size(key)` | O(1) |
| `HINCRBY key field n` | 字段值 +n（原子） | `redisTemplate.opsForHash().increment(key, field, delta)` | 字段值必须是整数 |
| `HSETNX key field value` | 只在字段不存在时设置 | `redisTemplate.opsForHash().putIfAbsent(key, field, value)` | 类似SETNX但针对hash字段 |

### ⚠️ Hash注意事项
- **比String更适合存对象**：改一个字段不用整条序列化反序列化
- **大hash问题**：字段超过1000个要小心，`HGETALL` 会阻塞
- **HINCRBY**：适合做对象的某个数值字段（如：`opsForHash().increment("user:1001", "score", 10)`）

---

## 📋 List（列表）— 双向链表

底层是双向链表，**头尾操作快**（O(1)），中间索引慢（O(N)）。

| 命令 | 作用 | Java 对应方法 | 注意事项 |
|------|------|---------------|---------|
| `LPUSH key value [value...]` | 从左侧（头部）插入 | `redisTemplate.opsForList().leftPush(key, value)` | 可批量传多个值 |
| `RPUSH key value [value...]` | 从右侧（尾部）插入 | `redisTemplate.opsForList().rightPush(key, value)` | — |
| `LPOP key` | 移除并返回左侧第一个元素 | `redisTemplate.opsForList().leftPop(key)` | 列表空时返回null |
| `RPOP key` | 移除并返回右侧第一个元素 | `redisTemplate.opsForList().rightPop(key)` | — |
| `LRANGE key start stop` | 获取指定范围元素 | `redisTemplate.opsForList().range(key, start, end)` | `0 -1` 表示所有元素。**大列表慎用全量** |
| `LLEN key` | 获取列表长度 | `redisTemplate.opsForList().size(key)` | O(1) |
| `LINDEX key index` | 根据索引获取元素 | `redisTemplate.opsForList().index(key, index)` | 从0开始 |
| `LSET key index value` | 设置指定索引的值 | `redisTemplate.opsForList().set(key, index, value)` | 索引必须存在，越界抛错 |
| `LREM key count value` | 删除指定值元素 | `redisTemplate.opsForList().remove(key, count, value)` | count>0 从左删，<0从右，=0删全部 |
| `LTRIM key start stop` | 只保留指定范围元素 | `redisTemplate.opsForList().trim(key, start, end)` | 常用于固定长度队列 |
| `BLPOP key [key...] timeout` | LPOP的阻塞版 | `redisTemplate.opsForList().leftPop(key, timeout, TimeUnit.SECONDS)` | 超时返回null |
| `BRPOP key [key...] timeout` | RPOP的阻塞版 | `redisTemplate.opsForList().rightPop(key, timeout, TimeUnit.SECONDS)` | 同上 |

### ⚠️ List注意事项
- **典型应用**：消息队列（LPUSH + BRPOP）、最新列表（LPUSH + LTRIM）
- **LTRIM + LPUSH**：实现固定大小列表：
  ```java
  opsForList().leftPush("logs", msg);
  opsForList().trim("logs", 0, 99);  // 只保留最新100条
  ```
- **LINDEX慢**：取中间元素慎用，量大用其他数据结构
- **阻塞队列**：`BRPOP` 是Redis实现简单队列的关键，但**没有ACK机制**、**消息丢失不重试**，生产级队列用RabbitMQ/Kafka/Redis Stream

---

## 🔄 Set（集合）— 无序不重复

| 命令 | 作用 | Java 对应方法 | 注意事项 |
|------|------|---------------|---------|
| `SADD key member [member...]` | 添加元素 | `redisTemplate.opsForSet().add(key, member1, member2)` | 重复添加自动忽略 |
| `SREM key member [member...]` | 删除元素 | `redisTemplate.opsForSet().remove(key, member1, member2)` | — |
| `SMEMBERS key` | 获取所有元素 | `redisTemplate.opsForSet().members(key)` | **大集合慎用！** 会阻塞 |
| `SCARD key` | 获取元素个数（基数） | `redisTemplate.opsForSet().size(key)` | O(1) |
| `SISMEMBER key member` | 判断元素是否存在 | `redisTemplate.opsForSet().isMember(key, member)` | O(1) |
| `SINTER key1 key2` | 交集（共有的） | `redisTemplate.opsForSet().intersect(key1, key2)` | 如：共同好友 |
| `SUNION key1 key2` | 并集（合并所有） | `redisTemplate.opsForSet().union(key1, key2)` | 如：好友推荐合并 |
| `SDIFF key1 key2` | 差集（在key1不在key2的） | `redisTemplate.opsForSet().difference(key1, key2)` | 如：新增好友识别 |
| `SPOP key [count]` | 随机移除并返回count个元素 | `redisTemplate.opsForSet().pop(key)` | 无count参数时pop一个 |
| `SRANDMEMBER key [count]` | 随机获取但不移除 | `redisTemplate.opsForSet().randomMember(key)` | 返回单个 |
| `SMOVE source dest member` | 将元素从一个集合移到另一个 | `redisTemplate.opsForSet().move(key, value, destKey)` | 原子操作 |

### ⚠️ Set注意事项
- **交/并/差集存结果**：`SINTERSTORE` → `redisTemplate.opsForSet().intersectAndStore(key1, key2, destKey)`
- **典型应用**：标签系统、好友关系、抽奖、UV统计

---

## 📊 Sorted Set（有序集合）— 带权重的Set

每个元素关联一个 **score（分数）** 用于排序，元素不重复，**底层跳表实现**。

| 命令 | 作用 | Java 对应方法 | 注意事项 |
|------|------|---------------|---------|
| `ZADD key score member [score member...]` | 添加元素和分数 | `redisTemplate.opsForZSet().add(key, value, score)` | member已存在则更新score |
| `ZREM key member [member...]` | 删除元素 | `redisTemplate.opsForZSet().remove(key, value1, value2)` | — |
| `ZRANGE key start stop [WITHSCORES]` | 按score升序获取指定范围 | `redisTemplate.opsForZSet().range(key, start, end)` | `0 -1` 全部 |
| `ZREVRANGE key start stop [WITHSCORES]` | 按score降序获取范围 | `redisTemplate.opsForZSet().reverseRange(key, start, end)` | 常用于排行榜topN |
| `ZRANK key member` | 获取元素排名（升序，从0开始） | `redisTemplate.opsForZSet().rank(key, value)` | 第一名是0 |
| `ZREVRANK key member` | 获取元素排名（降序） | `redisTemplate.opsForZSet().reverseRank(key, value)` | 第一名是0 |
| `ZSCORE key member` | 获取元素的分数 | `redisTemplate.opsForZSet().score(key, value)` | — |
| `ZINCRBY key increment member` | 给元素加分（原子） | `redisTemplate.opsForZSet().incrementScore(key, value, delta)` | 排行榜加分核心命令 |
| `ZCARD key` | 获取元素总数 | `redisTemplate.opsForZSet().zCard(key)` | O(1) |
| `ZCOUNT key min max` | 统计分数在[min,max]之间的元素数 | `redisTemplate.opsForZSet().count(key, min, max)` | — |
| `ZRANGEBYSCORE key min max` | 按分数范围获取元素 | `redisTemplate.opsForZSet().rangeByScore(key, min, max)` | `(80` 表示大于80不含80 |
| `ZREMRANGEBYRANK key start stop` | 按排名范围删除 | `redisTemplate.opsForZSet().removeRange(key, start, end)` | 常用于清理低分数据 |
| `ZREMRANGEBYSCORE key min max` | 按分数范围删除 | `redisTemplate.opsForZSet().removeRangeByScore(key, min, max)` | — |
| `ZINTERSTORE dest numkeys k1 k2 [WEIGHTS w1 w2] [AGGREGATE SUM/MAX/MIN]` | 交集计算并存入新key | `redisTemplate.opsForZSet().intersectAndStore(key1, key2, destKey)` | 权重和聚合需用 `Aggregate` / `Weights` |
| `ZUNIONSTORE dest numkeys k1 k2 [WEIGHTS w1 w2]` | 并集计算并存入新key | `redisTemplate.opsForZSet().unionAndStore(key1, key2, destKey)` | 同上 |

### ⚠️ Sorted Set注意事项
- **经典场景**：排行榜、延迟队列（score存时间戳）、限流
- **跳表 vs 红黑树**：Redis用跳表而不是红黑树，因为跳表范围查询简单，且写操作更少锁竞争
- **ZINTERSTORE计算量大**：大集合交集耗时，建议异步计算或缓存结果
- **score相同按字典序排**：同分时按member的字典序

---

## 🎯 Bitmap（位图）— 节约内存的布尔标记

本质是String类型，按位操作，一个位存一个布尔状态。

| 命令 | 作用 | Java 对应方法 | 注意事项 |
|------|------|---------------|---------|
| `SETBIT key offset value` | 设置指定偏移位的值（0/1） | `redisTemplate.opsForValue().setBit(key, offset, true/false)` | offset从0开始，最大2^32-1 |
| `GETBIT key offset` | 获取指定偏移位的值 | `redisTemplate.opsForValue().getBit(key, offset)` | 返回boolean |
| `BITCOUNT key [start end]` | 统计位为1的数量 | 无直接封装，需通过 `RedisConnection.bitCount(key)` | 适合日活统计 |
| `BITOP op destkey key [key...]` | 位运算（AND/OR/XOR/NOT） | `redisTemplate.opsForValue().bitOp(BitOperation.AND, destKey, key1, key2)` | 如：7天连续签到 |
| `BITPOS key bit [start end]` | 查找第一个指定值的位置 | `redisTemplate.opsForValue().bitField(key, ...)` 或通过连接层 | — |

### ⚠️ Bitmap注意事项
- **典型应用**：用户签到（用365位记录一年签到）、日活统计
- **偏移量注意**：offset从0开始，用户ID直接当偏移量的话，ID太大会占用大量内存
- **12亿用户？**：`setBit(key, 1200000000, true)` 会开辟约143MB，慎用

---

## 📍 HyperLogLog（基数统计）— 估算唯一值数量

用于**估算**不重复元素的数量，标准误差0.81%，每个key只占12KB内存。

| 命令 | 作用 | Java 对应方法 | 注意事项 |
|------|------|---------------|---------|
| `PFADD key element [element...]` | 添加元素 | `redisTemplate.opsForHyperLogLog().add(key, element1, element2)` | 重复自动忽略 |
| `PFCOUNT key [key...]` | 估算基数（不重复数量） | `redisTemplate.opsForHyperLogLog().size(key)` | 多个key传入集合 |
| `PFMERGE destkey sourcekey [sourcekey...]` | 合并多个HyperLogLog | `redisTemplate.opsForHyperLogLog().union(destKey, sourceKey1, sourceKey2)` | 合并后再size()得到并集估算 |

### ⚠️ HyperLogLog注意事项
- **只能估算数量，不能获取元素**！想知道具体哪些元素访问过？用Set
- **误差0.81%**：数据量大时准，小数据量可能偏大
- **内存优势**：存10亿个不重复值也只占12KB，但**不能取出元素**

---

## 🗺️ GEO（地理空间）— 存储经纬度坐标

基于Sorted Set实现，内部用 **Geohash编码**。

| 命令 | 作用 | Java 对应方法 | 注意事项 |
|------|------|---------------|---------|
| `GEOADD key longitude latitude member` | 添加地点坐标 | `redisTemplate.opsForGeo().add(key, new Point(lng, lat), member)` | 经度在前纬度在后 |
| `GEOPOS key member [member...]` | 获取地点坐标 | `redisTemplate.opsForGeo().position(key, member)` | 返回 List<Point> |
| `GEODIST key m1 m2 [unit]` | 计算两点距离 | `redisTemplate.opsForGeo().distance(key, m1, m2)` | 默认米，可指定 Metrics.KILOMETERS |
| `GEORADIUS key lng lat radius unit` | 查找指定半径内的地点 | `redisTemplate.opsForGeo().radius(key, new Circle(lng, lat, radius), args)` | 常用功能：附近的xx |
| `GEORADIUSBYMEMBER key member radius unit` | 以指定成员为中心查找 | `redisTemplate.opsForGeo().radius(key, member, new Distance(radius, metrics))` | 不用输入经纬度 |
| `GEOSEARCH key [FROMMEMBER m] [FROMLONLAT lng lat] BYRADIUS r unit [WITHCOORD] [WITHDIST]` | Redis 6.2+ 新版搜索 | `redisTemplate.opsForGeo().search(key, reference, searchParams, args)` | 新API，功能更强 |

### ⚠️ GEO注意事项
- **经纬度顺序**：`GEOADD` / `Point` 参数是 **经度在前，纬度在后**，写反了直接错
- **底层是ZSET**：`redisTemplate.opsForZSet().remove(key, member)` 可以删除GEO元素
- **Spring Data Redis 2.7+** 支持 `search()` 方法（对应GEOSEARCH），低版本没有

---

## 🧵 Stream（流）— Redis 5.0+ 消息队列

Redis自家的消息队列数据结构，支持消费者组、ACK、消息持久化。

| 命令 | 作用 | Java 对应方法 | 注意事项 |
|------|------|---------------|---------|
| `XADD key * field value [field value...]` | 追加消息 | `redisTemplate.opsForStream().add(StreamRecord.object(key).field(field, value))` | `*` 让Redis自动生成ID |
| `XRANGE key start end [COUNT n]` | 按ID范围读取消息 | `redisTemplate.opsForStream().range(key, Range.create(Cursor.Bound.inclusive(start), Cursor.Bound.inclusive(end)))` | `- +` 表示所有 |
| `XREAD COUNT n BLOCK ms STREAMS key [key...] id [id...]` | 阻塞读取新消息 | `redisTemplate.opsForStream().read(StreamReadOptions.empty().count(n).block(Duration.ofMillis(ms)), StreamOffset.create(key, ReadOffset.from(id)))` | `$` 表示只读最新的 |
| `XGROUP CREATE key groupname id [MKSTREAM]` | 创建消费者组 | `redisTemplate.opsForStream().createGroup(key, ReadOffset.from(id), groupName)` | `MKSTREAM` 不存在时自动创建流 |
| `XREADGROUP GROUP group consumer COUNT n BLOCK ms STREAMS key >` | 消费者组方式消费 | `redisTemplate.opsForStream().read(Consumer.from(group, consumer), StreamReadOptions.empty().count(n), StreamOffset.create(key, ReadOffset.lastConsumed()))` | `>` 表示只读未消费过的 |
| `XACK key group id [id...]` | 确认消息已处理 | `redisTemplate.opsForStream().acknowledge(key, group, recordId)` | 不ACK的消息会一直挂起 |
| `XPENDING key group` | 查看待处理/挂起的消息 | `redisTemplate.opsForStream().pending(key, group)` | 返回 PendingMessages 摘要 |
| `XDEL key id [id...]` | 删除指定ID的消息 | `redisTemplate.opsForStream().delete(key, recordId)` | — |
| `XTRIM key MAXLEN n` | 裁剪到最多n条 | `redisTemplate.opsForStream().trim(key, n)` | 控制stream无限增长 |
| `XLEN key` | 获取stream消息总数 | `redisTemplate.opsForStream().size(key)` | — |
| `XINFO STREAM key` | 查看stream详情 | 无直接方法，需通过 `RedisConnection.streamInfo()` | — |

### ⚠️ Stream注意事项
- **StreamRecord工具类**：Spring Data Redis 推荐使用 `StreamRecords.object(key)...` 构造消息
- **消息ID**：自动生成的ID格式 `1680000000000-0`，前半部分毫秒时间戳，自动有序
- **挂起消息**：消费了但没ACK的消息会留在Pending列表，重连后可能会重复投递，要做好幂等
- **XTRIM**：stream如果不裁剪会无限增长，占满内存

---

## ⚡ 性能与监控

这些命令在Java代码中不常用，更多是运维人员在redis-cli里执行。

| 命令 | 作用 | Java 对应方法 | 注意事项 |
|------|------|---------------|---------|
| `PING` | 测试连接是否正常 | `redisTemplate.getConnectionFactory().getConnection().ping()` | 返回PONG |
| `INFO` | 查看Redis服务器状态信息 | `redisTemplate.getConnectionFactory().getConnection().serverCommands().info()` | — |
| `INFO memory` | 查看内存使用详情 | `redisTemplate.getConnectionFactory().getConnection().serverCommands().info("memory")` | — |
| `MONITOR` | 实时打印所有命令 | **Java无封装，也不该用** | **生产环境绝不能用！** 性能暴跌 |
| `SLOWLOG GET n` | 查看最近n条慢查询 | 无封装，需通过连接层原生命令 | — |
| `CLIENT LIST` | 查看所有客户端连接 | `redisTemplate.getConnectionFactory().getConnection().getClientList()` | — |
| `CLIENT KILL addr:port` | 断开指定客户端连接 | `redisTemplate.getConnectionFactory().getConnection().killClient(host, port)` | — |
| `CONFIG GET *` | 获取配置项 | `redisTemplate.getConnectionFactory().getConnection().getConfig("*")` | — |
| `CONFIG SET parameter value` | 修改配置（运行时生效） | `redisTemplate.getConnectionFactory().getConnection().setConfig(parameter, value)` | 重启后丢失 |
| `SAVE` | 同步生成RDB快照 | `redisTemplate.getConnectionFactory().getConnection().save()` | **阻塞主进程** |
| `BGSAVE` | 后台异步生成RDB快照 | `redisTemplate.getConnectionFactory().getConnection().bgSave()` | 不阻塞 |
| `FLUSHALL` | 清空所有库所有key | `redisTemplate.getConnectionFactory().getConnection().flushAll()` | **!!! 毁灭操作 !!!** |

---

## 🧠 实战经验总结

### 1. key命名规范
推荐用 `项目名:业务:对象名:ID` 格式，冒号分割
```
user:1001:profile
order:20260401:count
```
Java中建议常量统一管理：
```java
private static final String KEY_PREFIX = "app:user:";
redisTemplate.opsForValue().set(KEY_PREFIX + userId + ":profile", jsonStr);
```

### 2. 过期时间
- **必须设置**：几乎所有业务key都应该设置过期时间
- Java写法：
  ```java
  // 基础过期
  redisTemplate.opsForValue().set(key, value, 1, TimeUnit.HOURS);
  // 防止雪崩——加随机偏移
  long expire = 3600 + new Random().nextInt(300);
  redisTemplate.expire(key, expire, TimeUnit.SECONDS);
  ```

### 3. 大key
- **阈值**：单个String > 10MB、Hash字段 > 5000、List长度 > 10000 就是大key
- **Java排查**：用 `redisTemplate.getConnectionFactory().getConnection().serverCommands().dbSize()`

### 4. 热key
- **现象**：某个key被超高频率访问，导致单节点CPU打满
- **Java解决**：加本地缓存（Caffeine）作为一级缓存 + Redis作为二级缓存
- 或者把key拆成多个副本 `user_hot_1 ~ user_hot_N`，读时随机选一个

### 5. 原子性与Lua脚本
- `opsForValue().increment(key)` 是原子的，但组合操作不是
- Java执行Lua脚本：
  ```java
  DefaultRedisScript<Long> script = new DefaultRedisScript<>();
  script.setScriptText("redis.call('set', KEYS[1], ARGV[1]); return redis.call('expire', KEYS[1], ARGV[2])");
  script.setResultType(Long.class);
  redisTemplate.execute(script, List.of("mykey"), "myvalue", "3600");
  ```

### 6. 序列化问题（常见坑！）
- **默认 `RedisTemplate<Object, Object>` 用JDK序列化**，存进去的key在redis-cli看到的是乱码（如 `\xac\xed...`）
- 解决方案：
  ```java
  // 方案A：直接用 StringRedisTemplate（推荐）
  @Autowired
  private StringRedisTemplate stringRedisTemplate;

  // 方案B：自定义 RedisTemplate 配置
  @Bean
  public RedisTemplate<String, Object> redisTemplate(RedisConnectionFactory factory) {
      RedisTemplate<String, Object> template = new RedisTemplate<>();
      template.setConnectionFactory(factory);
      template.setKeySerializer(new StringRedisSerializer());
      template.setHashKeySerializer(new StringRedisSerializer());
      template.setValueSerializer(new GenericJackson2JsonRedisSerializer());
      template.setHashValueSerializer(new GenericJackson2JsonRedisSerializer());
      return template;
  }
  ```

## 相关笔记
- [[☕ Java笔记/Redis的常用命令|Spring Data Redis Java 方法对照]]
- [[💼 面试/Redis面试题|Redis 面试题]]
