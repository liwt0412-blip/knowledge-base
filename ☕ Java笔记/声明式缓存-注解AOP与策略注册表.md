---
tags: [缓存, AOP, 设计模式, SpEL, 面试]
created: 2026-07-27
---

# 声明式缓存：注解 + AOP 骨架与策略注册表

> 用途：需要给查询类方法加缓存、或要支持多种缓存介质可切换时的设计参考；也是理解 Spring Cache `@Cacheable` 底层原理的拆解笔记。
> 来源：黑马微服务课程 global-cache 课件（教学版代码，非自有项目），经复盘提炼；面试口径为"学习课程代码并复盘其设计"，不冒领为项目产出。

## 一、识别信号（什么场景该想到这套做法）

- 方法**入参相同时返回值稳定**，且被高频重复调用，下游（DB / 远程接口）是瓶颈——典型如详情页、字典、配置类查询；
- 同一项目要支持**多种缓存介质可切换**（Redis / Caffeine / Memcached），且未来可能继续增加；
- 不想让缓存代码侵入业务方法，希望"加个注解就生效"；
- 被问"Spring Cache 的 key 是怎么生成的 / 能不能自己实现一个 @Cacheable"。

## 二、做法与代码骨架（三件套）

**1. Cache-Aside AOP 骨架**（所有声明式缓存的公共结构）：

```java
@Around("... && @annotation(cache)")
public Object doAround(ProceedingJoinPoint pjp, Cache cache) {
    String key = 解析key(cache, pjp);           // SpEL 动态 key
    Object result = 策略.getCacheData(key);      // 1 查缓存
    if (!ObjectUtils.isEmpty(result)) return result; // 2 命中直接返回
    result = pjp.proceed();                     // 3 未命中放行回源
    策略.setCacheData(key, result, cache.timeout(), cache.timeUnit()); // 4 写缓存
    return result;
}
```

**2. SpEL 动态 key 解析**：`StandardEvaluationContext` 把方法参数名→参数值绑定为变量，`SpelExpressionParser` 解析 `#user.name`、`T(xxx).staticMethod()`、`#user.age lt 10` 等表达式，多段 key 用逗号分隔逐段求值后拼接（group:key1:key2）。

**3. 策略注册表**（策略模式的"注册表"形态，消除类型分支）：

```java
// 策略类上用自定义注解标记类型，而非实现接口方法自报家门
@Component @CacheType(REDIS)
public class RedisCache implements CacheStrategy { ... }

// 启动时从容器收集所有策略 Bean，按注解值注册进 EnumMap
Map<String, CacheStrategy> beans = ctx.getBeansOfType(CacheStrategy.class);
beans.values().forEach(b -> map.put(
    b.getClass().getAnnotation(CacheType.class).value(), b));
```

关键收益：**新增一种缓存介质只需新建一个类打注解，路由表自动注册，不改任何 if-else**。`EnumMap` 以枚举为 key，底层数组实现，性能与类型安全优于 HashMap。

## 三、适用条件与失效边界

- ✅ 适用：读多写少、回源结果可容忍短暂不一致的查询；需要介质可切换的通用缓存层。
- ❌ 不适用 / 必须改造后才能上生产：
  - **缓存穿透**：恶意或无效 key 永远 miss 直打 DB → 需缓存空结果（短 TTL）或布隆过滤器；
  - **缓存击穿**：hotkey 失效瞬间大量并发回源 → 需互斥锁或单飞（singleflight）；
  - **强一致写场景**：本结构只有读侧，写后一致性要靠 evict/延时双删等另行设计（参考 [[高频最新状态的Redis合并写模式]]、[[热冷分离-实时榜Redis与历史归档表的双数据源查询]]）；
  - 多实例部署时本地缓存介质（Caffeine）各实例数据不一致，只适合允许短窗口偏差的场景。

## 四、教学版缺陷清单（面试抗追问弹药）

1. 穿透/击穿均未处理：无空值缓存、无互斥；
2. `getKey()` 短路判断有 bug：`(!key.contains("#") || !key.contains("T("))` 应为 `&&`，现条件几乎恒真，只含 `T()` 的动态 key 不会被解析；
3. Caffeine/Memcached 实现是 HashMap 占位：非线程安全、`timeout` 参数被忽略（无过期语义）；
4. 策略表用 static + ApplicationContextAware 回调持有，更 Spring 的写法是构造注入 `List<CacheStrategy>` / `Map<String, CacheStrategy>`；
5. 切面切在 Controller 层：无事务语义，多入口复用时粒度不对，生产应切 Service 层；
6. 命中判断 `ObjectUtils.isEmpty` 会把空串/空集合误判为 miss 回源；
7. `SpelExpressionParser` 每次 new，线程安全应做 static final 单例；
8. 相比 Spring Cache 缺：evict/put 语义、condition/unless 条件缓存、KeyGenerator 抽象、多级缓存组合。

## 五、与 Spring Cache 的对照

| 维度 | 本套自研 | Spring Cache |
|---|---|---|
| 读+写 | `@Cache` | `@Cacheable` |
| 删除 | 无 | `@CacheEvict` |
| 无论缓存直接写 | 无 | `@CachePut` |
| key 生成 | 手写 SpEL 解析 | KeyGenerator + SpEL |
| 介质切换 | `@CacheType` 注解 + 注册表 | CacheManager 抽象 |

结论：造这个轮子的价值在于理解官方轮子的骨架，工程上优先用 Spring Cache / JetCache 既有抽象。

## 关联

- 模式索引：[[☕ Java笔记/设计模式适配-问题识别信号与项目锚点]]（策略行锚点）
- 读侧之外的缓存一致性设计：[[☕ Java笔记/高频最新状态的Redis合并写模式]]、[[☕ Java笔记/热冷分离-实时榜Redis与历史归档表的双数据源查询]]
- AOP 基础：[[☕ Java笔记/AOP笔记]]
- 规则来源：[[00-我的长期上下文]] §4 复用知识规则
