---
tags:
  - redis
date: 2026-06-04
---
# Redis 常用命令速查

参考官方文档：[Redis实现性能优化](../06.权威笔记/Redis实现性能优化.md)

## 一、通用命令（所有数据类型通用）

| 命令 | 作用 | 注意事项 |
|------|------|---------|
| `KEYS pattern` | 列出所有匹配的key，如 `KEYS *` | **生产环境慎用！** 会阻塞Redis单线程，数据量大时卡死。生产用 `SCAN` 替代 |
| `SCAN cursor [MATCH pattern] [COUNT count]` | 游标式遍历key，每次返回一批 | 游标式非阻塞，`cursor=0` 开始，返回的cursor为0表示遍历完毕 |
| `EXISTS key` | 判断key是否存在，返回1/0 | — |
| `TYPE key` | 返回key的数据类型（string/list/hash/set/zset） | — |
| `DEL key [key...]` | 删除一个或多个key | 返回删除的数量 |
| `EXPIRE key seconds` | 设置key的过期时间（秒） | 过期后自动删除，常用于验证码、缓存 |
| `TTL key` | 查看key剩余存活秒数 | `-1` 表示永不过期，`-2` 表示已过期/不存在 |
| `RENAME key newkey` | 重命名key | 如果newkey已存在，会覆盖，慎用 |
| `SELECT index` | 切换数据库（0-15，默认16个库） | 生产环境尽量只用 `db0`，多库不利于管理 |
| `FLUSHDB` | 清空当前库所有key | **!!! 生产环境绝不执行 !!!** |
| `DBSIZE` | 查看当前库key总数 | — |



## （一）String（字符串）

value最大512MB，可存文本、数字、JSON序列化字符串、二进制数据。

| 命令 | 作用 | 注意事项 |
|------|------|---------|
| `SET key value` | 设置key-value | — |
| `SET key value EX 10` | 设置key-value并10秒后过期 | EX=秒，PX=毫秒 |
| `SET key value NX` | 只在key不存在时设置（分布式锁常用） | NX=Not eXists |
| `SET key value XX` | 只在key已存在时设置（更新） | XX=eXists |
| `GET key` | 获取value | key不存在返回nil |
| `MSET k1 v1 k2 v2` | 批量设置，原子操作 | 比逐条SET快，减少网络开销 |
| `MGET k1 k2 k3` | 批量获取 | 返回顺序和传入key一致，不存在的key返回nil |
| `INCR key` | value +1（原子自增） | key不存在则从0开始。**value必须是整数，否则抛错** |
| `INCRBY key n` | value +n | — |
| `DECR key` | value -1 | 同上 |
| `SETEX key seconds value` | SET + EXPIRE 合并命令 | 等同于 `SET key value EX seconds` |
| `SETNX key value` | 只在key不存在时设置 | 等同于 `SET key value NX` |
| `GETSET key value` | 设置新值并返回旧值 | 原子操作，用于更新计数器时获取旧值 |
| `STRLEN key` | 获取value的字节长度 | 中文一个UTF-8字符占3字节 |
| `APPEND key value` | 在原有value后追加 | key不存在则等同于SET |

#### String注意事项

- **JSON序列化**：存对象时用JSON字符串，但更新某个字段要取出来反序列化再改回去，可用Hash代替
- **INCR操作**：每个Redis单节点每秒能扛10万+ INCR，但**极端并发下会超卖**，高并发扣库存还需要配合Lua脚本或Redisson
- **大key问题**：value超过10MB就是大key，可能导致Redis阻塞、主从同步延迟



##  （二）Hash（哈希）

类似Java的 `Map<String, Map<field, value>>`，适合存一个对象的各种属性。

| 命令 | 作用 | 注意事项 |
|------|------|---------|
| `HSET key field value` | 设置hash中一个字段 | 字段已存在则覆盖 |
| `HGET key field` | 获取hash中一个字段 | — |
| `HMSET key f1 v1 f2 v2` | 批量设置（同HSET多参数，Redis 4.0+已合并） | 直接用 `HSET key f1 v1 f2 v2` |
| `HMGET key f1 f2` | 批量获取字段 | 不存在的字段返回nil |
| `HGETALL key` | 获取所有字段和值 | **大hash慎用！** 字段多时全量返回卡死 |
| `HKEYS key` | 获取所有字段名 | 同上，大hash慎用 |
| `HVALS key` | 获取所有值 | 同上，大hash慎用 |
| `HDEL key field [field...]` | 删除一个或多个字段 | — |
| `HEXISTS key field` | 判断字段是否存在 | — |
| `HLEN key` | 获取字段数量 | 比HGETALL快，只返回数量 |
| `HINCRBY key field n` | 字段值 +n（原子） | 字段值必须是整数 |
| `HSETNX key field value` | 只在字段不存在时设置 | 类似SETNX但针对hash字段 |

#### Hash注意事项
- **比String更适合存对象**：改一个字段不用整条序列化反序列化
- **大hash问题**：字段超过1000个要小心，`HGETALL` 会阻塞
- **HINCRBY**：适合做对象的某个数值字段（如：`HINCRBY user:1001 score 10` 给用户加分）



##  （三）List（列表）— 双向链表

底层是双向链表，**头尾操作快**（O(1)），中间索引慢（O(N)）。

| 命令 | 作用 | 注意事项 |
|------|------|---------|
| `LPUSH key value [value...]` | 从左侧（头部）插入 | 可批量插入 |
| `RPUSH key value [value...]` | 从右侧（尾部）插入 | 可批量插入 |
| `LPOP key` | 移除并返回左侧第一个元素 | 列表空时返回nil |
| `RPOP key` | 移除并返回右侧第一个元素 | — |
| `LRANGE key start stop` | 获取指定范围元素 | `0 -1` 表示所有元素。**大列表慎用全量** |
| `LLEN key` | 获取列表长度 | O(1) |
| `LINDEX key index` | 根据索引获取元素 | 从0开始，负数从尾算 |
| `LSET key index value` | 设置指定索引的值 | 索引必须存在，越界抛错 |
| `LREM key count value` | 删除指定值元素 | count>0 从左删count个，<0从右删，=0删全部 |
| `LTRIM key start stop` | 只保留指定范围元素，其余删除 | 常用于固定长度队列（如只保留最新100条） |
| `BLPOP key [key...] timeout` | LPOP的阻塞版，没元素就等 | 超时返回nil，timeout=0无限等待 |
| `BRPOP key [key...] timeout` | RPOP的阻塞版 | 同上 |

####  List注意事项
- **典型应用**：消息队列（LPUSH + BRPOP）、最新列表（LPUSH + LTRIM）
- **LTRIM + LPUSH**：实现固定大小列表 `LPUSH logs msg && LTRIM logs 0 99` 只保留最新100条
- **LINDEX慢**：取中间元素慎用，量大用其他数据结构
- **阻塞队列**：`BRPOP` 是Redis实现简单队列的关键，但**没有ACK机制**、**消息丢失不重试**，生产级队列用RabbitMQ/Kafka/Redis Stream



## （四）Set（集合）

| 命令 | 作用 | 注意事项 |
|------|------|---------|
| `SADD key member [member...]` | 添加元素 | 重复添加自动忽略 |
| `SREM key member [member...]` | 删除元素 | — |
| `SMEMBERS key` | 获取所有元素 | **大集合慎用！** 会阻塞 |
| `SCARD key` | 获取元素个数（基数） | O(1) |
| `SISMEMBER key member` | 判断元素是否存在 | O(1)，比List的查找快 |
| `SINTER key1 key2` | 交集（共有的） | 如：共同好友 |
| `SUNION key1 key2` | 并集（合并所有） | 如：好友推荐合并 |
| `SDIFF key1 key2` | 差集（在key1不在key2的） | 如：新增好友识别 |
| `SPOP key [count]` | 随机移除并返回count个元素 | 适合抽奖 |
| `SRANDMEMBER key [count]` | 随机获取但不移除 | `count>0`不重复，`count<0`可重复 |
| `SMOVE source dest member` | 将元素从一个集合移到另一个 | 原子操作 |

#### Set注意事项
- **交集/并集/差集**：数据量大时计算开销大，可把结果存起来 `SINTERSTORE dest k1 k2`
- **典型应用**：标签系统、好友关系、抽奖、UV统计
- **去重特性**：天然去重，适合存储用户ID集合



## （五）Sorted Set（有序集合，带权重的Set）

每个元素关联一个 **score（分数）** 用于排序，元素不重复，**底层跳表实现**。

| 命令 | 作用 | 注意事项 |
|------|------|---------|
| `ZADD key score member [score member...]` | 添加元素和分数 | member存在则更新score |
| `ZREM key member [member...]` | 删除元素 | — |
| `ZRANGE key start stop [WITHSCORES]` | 按score升序获取指定范围 | `0 -1` 全部 |
| `ZREVRANGE key start stop [WITHSCORES]` | 按score降序获取范围 | 常用于排行榜topN |
| `ZRANK key member` | 获取元素排名（升序，从0开始） | 第一名是0 |
| `ZREVRANK key member` | 获取元素排名（降序） | 第一名是0 |
| `ZSCORE key member` | 获取元素的分数 | — |
| `ZINCRBY key increment member` | 给元素加分（原子） | 排行榜加分核心命令 |
| `ZCARD key` | 获取元素总数 | O(1) |
| `ZCOUNT key min max` | 统计分数在[min,max]之间的元素数 | — |
| `ZRANGEBYSCORE key min max` | 按分数范围获取元素 | `(80` 表示大于80不含80 |
| `ZREMRANGEBYRANK key start stop` | 按排名范围删除 | 常用于清理低分数据 |
| `ZREMRANGEBYSCORE key min max` | 按分数范围删除 | — |
| `ZRANK key member` | 返回元素排名 | — |
| `ZINTERSTORE dest numkeys k1 k2 [WEIGHTS w1 w2] [AGGREGATE SUM/MAX/MIN]` | 交集计算并存入新key | 适合多维度综合排名 |
| `ZUNIONSTORE dest numkeys k1 k2 [WEIGHTS w1 w2]` | 并集计算并存入新key | 适合合并排行榜 |

#### Sorted Set注意事项
- **经典场景**：排行榜、延迟队列（score存时间戳）、限流
- **跳表 vs 红黑树**：Redis用跳表而不是红黑树，因为跳表范围查询简单，且写操作更少锁竞争
- **ZINTERSTORE计算量大**：大集合交集耗时，建议异步计算或缓存结果
- **score相同按字典序排**：同分时按member的字典序



## （六）Bitmap（位图，节约内存的布尔标记）

本质是String类型，按位操作，一个位存一个布尔状态。

| 命令 | 作用 | 注意事项 |
|------|------|---------|
| `SETBIT key offset value` | 设置指定偏移位的值（0/1） | offset从0开始，最大2^32-1（512MB） |
| `GETBIT key offset` | 获取指定偏移位的值 | — |
| `BITCOUNT key [start end]` | 统计位为1的数量 | 适合日活统计（有多少人签到） |
| `BITOP op destkey key [key...]` | 位运算（AND/OR/XOR/NOT） | 如：7天连续签到 = 7个bitmap做AND |
| `BITPOS key bit [start end]` | 查找第一个指定值的位置 | — |

####  Bitmap注意事项
- **典型应用**：用户签到（user:sign:1001 用365位记录一年）、日活统计
- **偏移量注意**：offset从0开始，用户ID直接当偏移量的话，ID太大会占用大量内存
- **12亿用户？**：`SETBIT key 1200000000 1` 会开辟1200000000/8/1024/1024 ≈ 143MB，慎用
- **选型与键设计**：何时该用位图、键维度怎么定，见 [[Bitmap标志位存储模式-连签统计与验重]]



## （七）HyperLogLog（基数统计，估算唯一值数量）

用于**估算**不重复元素的数量，标准误差0.81%，每个key只占12KB内存。

| 命令 | 作用 | 注意事项 |
|------|------|---------|
| `PFADD key element [element...]` | 添加元素 | 重复自动忽略 |
| `PFCOUNT key [key...]` | 估算基数（不重复元素数量） | 多个key时先合并再估算 |
| `PFMERGE destkey sourcekey [sourcekey...]` | 合并多个HyperLogLog | 合并后destkey的PFCOUNT是并集估算 |

#### HyperLogLog注意事项
- **只能估算数量，不能获取元素**！想知道具体哪些元素访问过？用Set
- **误差0.81%**：数据量大时准，小数据量可能偏大
- **内存优势**：存10亿个不重复值也只占12KB，但**不能取出元素**



## （八）GEO（地理空间，存储经纬度坐标）

基于Sorted Set实现，内部用 **Geohash编码**。

| 命令 | 作用 | 注意事项 |
|------|------|---------|
| `GEOADD key longitude latitude member` | 添加地点坐标 | 经度在前纬度在后，注意顺序！ |
| `GEOPOS key member [member...]` | 获取地点坐标 | — |
| `GEODIST key m1 m2 [unit]` | 计算两点距离 | 单位：m/km/mi/ft |
| `GEORADIUS key lng lat radius unit` | 查找指定半径内的地点 | 常用功能：附近的xx |
| `GEORADIUSBYMEMBER key member radius unit` | 以指定成员为中心查找 | 不用输入经纬度 |

#### GEO注意事项
- **经纬度顺序**：`GEOADD` 参数是 **经度在前，纬度在后**，写反了直接错
- **底层是ZSET**：`ZREM key member` 可以删除GEO元素，`ZRANGE key 0 -1` 可遍历
- **Redis 6.2+ 新增**：`GEOSEARCH` 和 `GEOSEARCHSTORE` 替代旧的GEORADIUS系列



## （九）Stream（流，Redis 5.0+ 消息队列）

Redis自家的消息队列数据结构，支持消费者组、ACK、消息持久化。

| 命令 | 作用 | 注意事项 |
|------|------|---------|
| `XADD key * field value [field value...]` | 追加消息（* 让Redis自动生成ID） | ID格式：`时间戳-序号` |
| `XRANGE key start end [COUNT n]` | 按ID范围读取消息 | `- +` 表示所有 |
| `XREAD COUNT n BLOCK ms STREAMS key [key...] id [id...]` | 阻塞读取新消息 | `$` 表示只读最新的 |
| `XGROUP CREATE key groupname id [MKSTREAM]` | 创建消费者组 | `MKSTREAM` 让stream不存在时自动创建 |
| `XREADGROUP GROUP group consumer COUNT n BLOCK ms STREAMS key >` | 消费者组方式消费 | `>` 表示只读未分发给自己的消息 |
| `XACK key group id [id...]` | 确认消息已处理 | 不ACK消息会一直挂起 |
| `XPENDING key group` | 查看待处理/挂起的消息 | 消费了没ACK的消息会在这里 |
| `XDEL key id [id...]` | 删除指定ID的消息 | — |
| `XTRIM key MAXLEN n` | 裁剪到最多n条 | 控制stream无限增长 |
| `XLEN key` | 获取stream消息总数 | — |
| `XINFO STREAM key` | 查看stream详情 | — |

####  Stream注意事项
- **比List队列强在哪**：消费者组、消息持久化、ACK机制、多消费者互不冲突
- **消息ID**：自动生成的ID `1680000000000-0` 前半部分毫秒时间戳，后半部分序号，自动有序
- **挂起消息**：消费了但没ACK的消息会留在Pending列表，重连后可能会重复投递，要做好幂等
- **XTRIM**：stream如果不裁剪会无限增长，占满内存



## 二、性能与监控

| 命令 | 作用 | 注意事项 |
|------|------|---------|
| `PING` | 测试连接是否正常，返回PONG | — |
| `INFO` | 查看Redis服务器状态信息 | 包括内存、连接数、命中率 |
| `INFO memory` | 查看内存使用详情 | `used_memory_human` 是直观的内存用量 |
| `MONITOR` | 实时打印所有命令（调试用） | **生产环境绝不能用！** 性能暴跌，QPS直接腰斩 |
| `SLOWLOG GET n` | 查看最近n条慢查询 | 慢查询阈值默认10ms，`CONFIG SET slowlog-log-slower-than 10000` |
| `CLIENT LIST` | 查看所有客户端连接 | — |
| `CLIENT KILL addr:port` | 断开指定客户端连接 | — |
| `CONFIG GET *` | 获取配置项 | 只读安全 |
| `CONFIG SET parameter value` | 修改配置（运行时生效） | 重启后丢失，需同步修改redis.conf |
| `SAVE` | 同步生成RDB快照 | **阻塞主进程**，生成期间不能服务，生产用 `BGSAVE` |
| `BGSAVE` | 后台异步生成RDB快照 | fork子进程做，不会阻塞主线程 |
| `FLUSHALL` | 清空所有库所有key | **!!! 全Redis实例级别的毁灭操作 !!!** |



## 三、实战经验总结

### 1. key命名规范
推荐用 `项目名:业务:对象名:ID` 格式，冒号分割，Redis CLI里用冒号会自动折叠树形结构
```
user:1001:profile
order:20260401:count
app:login:token:uuid
```

### 2. 过期时间
- **必须设置**：几乎所有业务key都应该设置过期时间（验证码5分钟，token 7天，缓存1小时）
- **雪崩**：大量key同时过期，瞬间打穿缓存到DB。解决办法：过期时间加随机值（`EXPIRE base + random(0,300)`）

### 3. 大key
- **阈值**：单个String > 10MB、Hash字段 > 5000、List长度 > 10000 就是大key
- **危害**：阻塞Redis单线程、主从同步延迟、内存不均
- **排查**：用 `redis-cli --bigkeys` 扫描（只能在业务低峰期跑）

### 4. 热key
- **现象**：某个key被超高频率访问，导致单节点CPU打满
- **解决**：本地缓存 + Redis（多级缓存）、把key拆成多个副本（key_1 ~ key_N 分摊读压力）

### 5. 原子性与Lua脚本
- Redis单线程保证每个命令原子，但**多个命令不是原子的**
- 需要原子操作多个命令时，用Lua脚本：`EVAL "redis.call('set', KEYS[1], ARGV[1]) redis.call('expire', KEYS[1], ARGV[2])" 1 mykey myvalue 3600`

## 相关笔记

- [[☕ Java笔记/Java笔记总览|Java笔记总览]]

- [[📋 技术速查/Redis命令|完整 Redis 命令参考]]
- [[📋 技术速查/Redis性能优化|Redis 性能优化实战]]
