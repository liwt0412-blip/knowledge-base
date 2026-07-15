---
tags:
  - 面试
  - Java
  - Bug排查
  - 真实开发
status: final
priority: P1
created: 2026-07-09
---

# 真实开发 Bug 排查面试回答

## 一、这份文档的定位

这份文档用于回答面试官这类问题：

- 你开发中遇到过什么 Bug？
- 你怎么定位问题？
- 你有没有真实项目排错经验？
- 你怎么看日志、SQL、接口和数据？
- 你怎么证明自己不是只会 CRUD？

核心口径：

> 我排查 Bug 时不会只盯代码，而是按请求链路、参数、权限、SQL、数据、缓存、编译产物逐层定位。很多问题看起来是代码错，最后根因可能是数据缺失、导包冲突、权限上下文没有注入，或者构建缓存没刷新。

使用建议：

- 本文偏“真实开发基础踩坑”，适合证明自己确实做过接口、权限、SQL、框架联调。
- 如果面试官问“有没有更复杂一点的排错”，优先看 [[真实开发高级排错案例-Java+AI]]。
- 主打项目深挖时，不要把 `@PathVariable`、导包冲突这类问题当成最强案例；它们适合做补充。

---

## 二、排查问题的通用方法

### 第一层：先复现

先确认问题是否稳定复现：

- 哪个接口；
- 什么参数；
- 哪个用户；
- 什么环境；
- 前端怎么操作；
- 后端有没有报错；
- 数据库是否有对应数据。

面试话术：

> 我一般先复现问题，不会直接猜。能稳定复现，排查效率会高很多；不能复现，就先补日志或让前端提供请求参数和响应结果。

### 第二层：按链路定位

后端问题一般按这条链路看：

```text
前端请求 -> 网关/拦截器 -> Controller -> Service -> Mapper/SQL -> 数据库/缓存 -> 返回值
```

每一层看一个问题：

- 请求路径和方法对不对；
- 参数有没有传到后端；
- Token 和用户上下文有没有解析；
- Service 是否进入；
- SQL 是否执行；
- 数据库是否有数据；
- 返回对象字段是否映射正确。

### 第三层：找根因，不只修表象

比如接口返回空，不一定是 SQL 写错，可能是：

- 关联表没有数据；
- 用户无权限；
- DTO 字段名不一致；
- 查询条件过严；
- 分页对象导错包；
- 当前用户上下文没有写入 ThreadLocal。

面试话术：

> 我会尽量找到根因，而不是看到空数据就改 SQL，看到 500 就乱加 try-catch。后端排错最重要的是把现象、日志、SQL 和数据对起来。

---

## 三、案例一：PageHelper 和 MyBatis Plus 的 Page 类冲突

### 问题现象

分页接口没有生效，SQL 没有加 `limit`，或者代码里 `Page` 类型不匹配。

### 根因

项目里同时引入了 PageHelper 和 MyBatis Plus。两个框架都有 `Page` 类：

- PageHelper：`com.github.pagehelper.Page`
- MyBatis Plus：`com.baomidou.mybatisplus.extension.plugins.pagination.Page`

MyBatis Plus 的分页拦截器只识别自己的 `Page`。如果导成 PageHelper 的 `Page`，拦截器不会生效。

另外，PageHelper 用 `getResult()`，MyBatis Plus 用 `getRecords()`。如果代码里写了 `getResult()`，IDE 可能自动把 import 又改回 PageHelper。

### 解决方式

- 删除 PageHelper 的 import；
- 使用 MyBatis Plus 的 `Page`；
- 获取数据用 `getRecords()`；
- 检查 Mapper 参数类型是否是 MP 的 `Page`；
- 避免 IDE 自动优化导入改错包。

### 面试回答

> 我遇到过一个分页不生效的问题。表面看 SQL 正常执行，但没有加 limit。后来发现项目里同时有 PageHelper 和 MyBatis Plus，`Page` 类导错包了。MP 的分页拦截器只识别自己的 `Page`，如果导成 PageHelper 的 `Page`，就不会触发分页。这个问题的经验是：框架迁移或混用时，要特别注意同名类和 API 差异，不能只看代码能编译。

---

## 四、案例二：LEFT JOIN 结果全是 NULL，不一定是代码错

### 问题现象

列表接口能返回数据，但关联字段一直是 `null`，比如归属人姓名查不出来。

### 根因

SQL 是：

```sql
select c.*, u.name as assign_name
from clue c
left join user u on c.user_id = u.id
```

SQL 本身没问题，真正原因是：

- `clue.user_id` 为空；
- 或者 `clue.user_id` 有值，但 `user` 表没有对应 `id`。

### 解决方式

- 先查主表字段是否有值；
- 再查关联表是否存在对应记录；
- 必要时补测试数据或修复数据；
- 不要直接怀疑映射或代码。

### 面试回答

> 我遇到过 LEFT JOIN 后关联字段全是 null 的问题。一开始容易怀疑 resultMap 或 SQL 写错，但我把 SQL 单独拿到数据库执行后发现逻辑没错，根因是测试数据缺失，主表里的 user_id 在用户表里没有对应记录。这个问题让我形成一个习惯：查关联字段为空时，先验证数据关系，再看代码映射。

---

## 五、案例三：ThreadLocal 当前用户只 get 没 set

### 问题现象

业务代码里通过 `CurrentUserHolder.get()` 获取当前用户 ID，但返回一直是 `null`，导致操作记录里的 `userId` 为空。

### 根因

`CurrentUserHolder` 是基于 ThreadLocal 的。使用前必须由拦截器或过滤器在请求进入时调用 `set()`，请求结束后调用 `remove()`。

问题在于：

- 拦截器解析了 JWT；
- 但没有从 claims 里取用户 ID；
- 也没有调用 `CurrentUserHolder.set(userId)`；
- 请求结束后也没有 remove，存在内存泄漏风险。

### 解决方式

- 在 Token 拦截器中解析用户 ID；
- 请求进入时 `set()`；
- 请求结束时 `remove()`；
- 避免线程池复用导致脏数据。

### 面试回答

> 我遇到过 ThreadLocal 当前用户取不到的问题。Service 里一直 get 当前用户，但没人 set。最后定位到 Token 拦截器只校验了 JWT，没有把用户 ID 放进 ThreadLocal。修复时我在 preHandle 里 set，在 afterCompletion 里 remove。这个问题说明 ThreadLocal 必须成对使用，否则不是取不到值，就是线程复用时产生脏数据。

---

## 六、案例四：`@PathVariable` 误用 DTO

### 问题现象

查询接口报 500，提示缺少路径变量。

### 根因

Controller 写法类似：

```java
@GetMapping("/pool")
public Result list(@PathVariable ClueQueryDto queryDto) {
    ...
}
```

`@PathVariable` 只能绑定 URL 路径里的简单变量，比如 `/users/{id}`。查询 DTO 应该从 query string 绑定，不能用 `@PathVariable`。

### 解决方式

- 查询参数 DTO 不加注解，或用 `@ModelAttribute`；
- `@PathVariable` 只用于路径变量；
- 同时检查 URL 拼写，比如 `pool` 不要写成 `poll`。

### 面试回答

> 我遇到过一个接口 500，最后发现是把查询 DTO 标成了 `@PathVariable`。`@PathVariable` 适合绑定路径里的 id，不适合接收多个查询条件。查询 DTO 应该让 Spring MVC 从 query string 自动绑定。这个问题不难，但很典型，说明 Controller 参数绑定要和 HTTP 语义对应。

---

## 七、案例五：`@TableField(exist = false)` 没生效

### 问题现象

实体类字段已经标了 `@TableField(exist = false)`，但 MyBatis Plus 插入时仍然把这个字段写进 SQL，报数据库列不存在。

### 根因

常见原因不是注解本身错，而是：

- 增量编译产物没更新；
- `target/classes` 里还是旧 class；
- MyBatis Plus TableInfo 缓存了旧字段信息；
- 应用没有彻底重启。

### 解决方式

- `mvn clean compile`；
- 删除 `target` 目录；
- 重启项目；
- 检查编译后的 class 时间戳；
- 确认注解 import 正确。

### 面试回答

> 我遇到过 `@TableField(exist = false)` 明明加了但插入 SQL 还带这个字段的问题。最后不是注解错，而是增量编译和框架缓存导致旧 class 没更新。处理方式是 clean 编译、删除 target、重启服务。这个问题提醒我，排查时不能只看源代码，还要考虑编译产物和运行时缓存。

---

## 八、案例六：权限字段不能相信前端

### 问题现象

登录后前端拿不到角色标识，后续权限功能失效。

### 根因

角色标识 `roleLabel` 必须从数据库根据用户和角色关系查询，不能由前端传入。否则用户可以伪造角色。

如果用户没有绑定角色，或者角色表没有对应数据，系统应拒绝登录或返回权限异常，而不是让前端补字段。

### 面试回答

> 我遇到过角色标识为空导致权限功能失效的问题。最后确定 roleLabel 不能由前端传，必须由后端根据用户角色关系查出来。因为权限字段是安全边界，不能相信客户端。这个思路也和 AI 工具调用一样：模型或前端只能提出意图，真正权限判断必须在后端。

---

## 九、案例七：RabbitMQ 队列持久化参数不一致，设备消息堆积但消费者未启动

> 真实性边界：用户确认该问题发生在石化经营分析平台的设备消息消费链路。以下仅记录已确认的现象、日志、根因和修复，不扩展为未核实的线上影响。

### 问题现象

设备上报消息已经发送到 RabbitMQ，在管理页面可以看到队列中有待消费消息，但设备消息消费者没有打印消费日志，相关业务处理没有执行。

### 排查过程与证据

1. 先确认生产端：RabbitMQ 管理页面能看到消息进入目标队列，因此问题不在“消息是否发送成功”。
2. 再确认消费端：设备服务启动日志中出现：

```text
PRECONDITION_FAILED - inequivalent arg 'durable':
received 'false' but current is 'true'
```

3. 检查消费者的队列声明，发现持久化参数写成了：

```java
@Queue(name = QUEUE_NAME, durable = "ture")
```

4. `ture` 是 `true` 的拼写错误。消费者端声明被解析为非持久化（`false`），而 Broker 中同名队列已经是持久化队列（`true`）。RabbitMQ 不允许同名队列的关键属性不一致，因此拒绝消费者声明，监听器没有成功启动。

### 根因

不是“MQ 有消息却没有消费”，而是消费者启动时重新声明队列，声明参数与 Broker 中已有队列不一致，触发 `PRECONDITION_FAILED`。

```text
生产者发送成功
    → Broker 队列中存在消息
    → 消费者声明队列时 durable 参数冲突
    → Listener 容器未成功启动
    → 消息持续堆积
```

### 修复方式

把持久化参数修正为精确的 `"true"`，并确保与 Broker 中已有队列属性一致：

```java
@RabbitListener(bindings = @QueueBinding(
        value = @Queue(name = QUEUE_NAME, durable = "true"),
        exchange = @Exchange(name = EXCHANGE_NAME, type = ExchangeTypes.TOPIC),
        key = ROUTING_KEY
))
```

修复后重启学习服务，并按以下顺序验证：

1. 启动日志不再出现 `PRECONDITION_FAILED`；
2. RabbitMQ 管理页面显示该队列存在消费者；
3. 发送一条设备消息后，消费者打印消费日志；
4. 确认对应设备消息的业务处理恢复。

### 防复发措施

- 交换机、队列名、路由键统一放在 `MqConstants`，避免手写字符串不一致。
- 队列关键属性（`durable`、`exclusive`、`autoDelete`）在生产者/消费者声明中保持一致。
- 服务启动后关注 Listener 容器日志，不能只看应用端口是否启动成功。
- 联调检查同时验证：消息数量、消费者数量、消费日志和最终业务数据。
- 不要为了消除冲突直接删除已有队列；先确认队列属性和消息是否需要保留，再统一声明配置。

### 面试回答

> 我在石化经营分析平台的设备消息链路里遇到过 RabbitMQ 已经有消息、但消费者没有处理的情况。我没有先怀疑业务代码，而是先看管理页面确认消息确实进入了队列，再看消费者启动日志。日志提示 `PRECONDITION_FAILED`，说同名队列的 durable 参数不一致。继续检查后发现队列声明把 `durable = "true"` 写成了 `"ture"`，消费者声明被当成非持久化，而 Broker 里已有队列是持久化的，所以 RabbitMQ 拒绝声明，监听器没有成功启动。修复拼写并重启后，我再通过消费者数量、消费日志和设备消息业务处理结果验证恢复。这个问题让我形成了一个习惯：MQ 消息不消费时，按生产端、Broker、消费者启动、监听方法、业务落库的链路排查，不能只盯监听方法。

---

## 十、案例八：视频播放进度持续返回 400

> 真实性边界：该问题发生在天机学堂项目的本地接口联调中，用于记录真实排错过程；不包装成石化经营分析平台或线上生产事故。

### 问题现象

用户观看视频时，前端约每 15 秒调用一次学习记录接口，后端持续返回：

```text
BadRequestException: 视频时长或播放进度不合法
```

课表查询 SQL 每次都返回一条数据，因此最初可以排除“课表不存在、用户不匹配或课程失效”。

### 请求证据

浏览器 Network 中的请求负载为：

```json
{
  "lessonId": "2076330661992062977",
  "sectionId": "42",
  "moment": 59.249392,
  "duration": 0,
  "sectionType": 1,
  "commitTime": "2026-07-13 16:10:51"
}
```

其中 `moment` 表示已经播放到约第 59 秒，`duration` 表示视频总时长。总时长为 0 时，服务端无法判断是否达到 50% 完成条件。

### 根因与定位

异常固定发生在视频完成条件校验中：

```java
if (duration == null || duration <= 0 || moment == null || moment > duration) {
    throw new BadRequestException("视频时长或播放进度不合法");
}
```

请求每隔约 15 秒重复一次，而 `duration` 始终为 0，所以每次都会稳定触发相同异常。根因是前端播放器没有正确取得或传递视频总时长，不是课表 SQL 或学习记录 Mapper 查询失败。

### 修复方向

- 前端应在播放器元数据加载完成后读取总时长，并把 `moment`、`duration` 统一转换为整数秒后提交。
- 总时长尚未就绪时，应暂停上报，而不是持续发送 `duration=0`。
- 如果后端选择兼容 `duration<=0`，只能保存播放位置并保持小节未完成，不能按 50% 规则判定完成。
- DTO 校验和 Service 规则必须一致：若 Service 要求总时长大于 0，DTO 不应只声明 `@Min(0)`。

### 面试复盘价值

这个案例说明，接口持续报同一业务异常时，应先把请求负载、堆栈行号和已执行 SQL 对齐。SQL 查询成功只能证明前置数据存在，不能证明后续业务参数合法；周期性重复报错通常意味着调用端在持续发送相同的无效状态。

---

## 十一、最终背诵版

如果面试官问“你遇到过什么 Bug”，可以这样答：

> 我印象比较深的是一个分页不生效的问题。项目里同时用了 PageHelper 和 MyBatis Plus，两个框架都有 `Page` 类。代码能编译，但导包导成了 PageHelper 的 `Page`，导致 MyBatis Plus 的分页拦截器识别不到，所以 SQL 没有加 limit。后来我把 import 改成 MP 的 `Page`，并把 `getResult()` 改成 `getRecords()` 才解决。
>
> 这个问题给我的经验是，排查 Bug 不能只看表面报错，要结合框架原理、SQL 日志、实际导包和运行时行为一起看。类似的我还遇到过 LEFT JOIN 字段为空其实是数据缺失、ThreadLocal 当前用户只 get 没 set、`@PathVariable` 误用 DTO，以及 RabbitMQ 队列声明参数不一致导致消费者没有启动。这些问题都说明后端排查要按链路定位，而不是靠猜。
