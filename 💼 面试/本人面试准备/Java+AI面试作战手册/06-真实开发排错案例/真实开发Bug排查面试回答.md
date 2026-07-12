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

## 九、最终背诵版

如果面试官问“你遇到过什么 Bug”，可以这样答：

> 我印象比较深的是一个分页不生效的问题。项目里同时用了 PageHelper 和 MyBatis Plus，两个框架都有 `Page` 类。代码能编译，但导包导成了 PageHelper 的 `Page`，导致 MyBatis Plus 的分页拦截器识别不到，所以 SQL 没有加 limit。后来我把 import 改成 MP 的 `Page`，并把 `getResult()` 改成 `getRecords()` 才解决。
>
> 这个问题给我的经验是，排查 Bug 不能只看表面报错，要结合框架原理、SQL 日志、实际导包和运行时行为一起看。类似的我还遇到过 LEFT JOIN 字段为空其实是数据缺失、ThreadLocal 当前用户只 get 没 set、`@PathVariable` 误用 DTO 这些问题。它们都说明后端排查要按链路定位，而不是靠猜。
