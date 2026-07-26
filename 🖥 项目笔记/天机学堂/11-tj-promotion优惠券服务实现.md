---
tags: [天机学堂, tj-promotion, 优惠券, MyBatis-Plus, 排错]
created: 2026-07-22
---

# 11-tj-promotion 优惠券服务实现

> 记录 tj-promotion（优惠券微服务）的真实代码位置、需求契约、排错过程与当前状态。
> 可复用的通用结论已抽取至 [[☕ Java笔记/MySQL保留关键字与MyBatisPlus反引号转义]]。

## 当前状态（2026-07-25 更新）

- 模块骨架：端口 8093、服务名 `promotion-service`、数据库 `tj_promotion`、网关路由 **`/pm/**`（管理端）+ `/prs/**`（学员端，课程前端硬编码前缀，07-25 补）**。
- **管理端接口（7 个）**：新增 `POST /coupons`、修改 `PUT /coupons/{id}`、分页 `GET /coupons/page`、详情 `GET /coupons/{id}`、删除 `DELETE /coupons/{id}`、发放 `PUT /coupons/{id}/issue`、暂停 `PUT /coupons/{id}/pause`。
- **C 端接口（2 个，07-25 完成）**：领券中心 `GET /coupons/list`（游客可见；available/received 券×用户联合判断，两次 SQL 封顶批量统计，obtainWay=MANUAL 过滤）；领取 `POST /user-coupons/{id}/receive`（登录 → 状态时间窗 → 枚举可见性 → 限领 count → 条件更新防超发 → 快照落库，同事务；UserCouponServiceImpl 直接注 CouponMapper 避免与 CouponServiceImpl 循环依赖）。
- **user_coupon 表**：官方 DDL 落 `src/main/resources/sql/20260725_user_coupon.sql`（一字未改；曾对比自研方案，官方胜在精简与课程对齐，差异点 order_id/状态索引记为观察项）。
- **状态机**：待发放 → 未开始/进行中 ⇄ 已暂停；编辑/删除仅待发放。
- **兑换码链路**：发放时 obtainWay=2 异步生成（Redis 号段 + S盒签名 + Base32 10位）；`@TransactionalEventListener(AFTER_COMMIT) + @Async` 事件驱动；Bitmap 验重 `prs:code:status:{couponId}`。方案见 [[☕ Java笔记/兑换码设计-签名防伪与三层防爆破]]。
- **兑换码兑换接口（07-26 完成）**：验签 → 解析 couponId/码id → 编程式 RLock（用户+券粒度）→ TransactionTemplate 内 bitmap 占位（`SETBIT` 判重）→ 码记录锁内重读 → 条件更新库存 → 落 user_coupon；bitmap 占位成功但 DB 失败时 catch 内复位码位（对称恢复，不留废码）。
- 未实现：我的优惠券列表（语义确认表已出，待开工）、兑换码补偿 XXL-Job、状态自动流转 Job、防爆破限流锁定。
- 需求契约：仓库 `docs/tj-promotion-新增优惠券接口-需求采集.md`；官方 DDL：`docs/ref/tj_promotion.sql`。
- 关键契约点：金额单位**分**；新增接口不含时间字段；`specific=true` 同事务写 `coupon_scope`（type=1 分类）；creater/updater 取 `UserContext`。
- 协作沉淀：[[🖥 项目笔记/00-从零启动新业务Playbook]]（本次协作复盘产出）；领券并发设计通用结论见 [[☕ Java笔记/领券防超发与事务内操作顺序]]。

## 排错：学员端领券 404 与游客匿名访问（2026-07-25）

### 现象

学员端前端调 `POST /prs/user-coupons/{id}/receive` 返回 404；游客访问领券中心报错。

### 根因（两层）

1. **404**：课程前端统一用 `/prs/**` 前缀访问 promotion-service，而我们网关只配了 `/pm/**`（当时 `/ps` 被 pay 占用自选的前缀，未对齐课程约定）。已在 tj-gateway bootstrap.yml 补 `/prs/**` 路由（两条并存）。注意 Nacos 网关配置若自含 routes 会覆盖本地，需同步。
2. **匿名访问**：读源码发现网关鉴权真实机制与表面配置不一致——
   - `AccountAuthFilter.isExcludePath` 匹配对象是 `方法:完整路径`（如 `GET:/prs/coupons/list`），普通路径 pattern 永远匹配不上：**`tj.auth.excludePath` 全部条目（含代码硬编码）实际是死配置**；
   - 真正放行在 `AuthUtil.checkAuth`：路径**未注册进权限表（Redis）即直接放行**——公开页面零配置；
   - 服务侧 `LoginAuthInterceptor` 才是游客的真正拦截点，tj-promotion bootstrap.yml 加 `tj.auth.resource.excludeLoginPaths: /coupons/list`（StripPrefix 后的路径，/pm /prs 共用一条）。

### 修复

网关补 `/prs/**` 路由；服务层加 excludeLoginPaths；Nacos 里误加的 `/prs/coupons/list` excludePath 条目建议删除（不是生效机制）。

### 教训

**配置是否生效要读源码验证真实匹配逻辑，不照抄既有配置条目**——既有配置可能是从未生效的死配置。通用结论与面试表述见 [[☕ Java笔记/兑换码设计-签名防伪与三层防爆破]] 关联节与 [[💼 面试/本人面试准备/Java+AI面试作战手册/05-补强项目/天机学堂-优惠券兑换码与防爆破设计]]。

## 排错：新增优惠券报 BadSqlGrammarException（2026-07-22）

### 现象

调用 `POST /coupons` 报 `BadSqlGrammarException`：`SQLSyntaxErrorException ... near 'specific, discount_value, ...' at line 4`。MyBatis-Plus 打印的 INSERT 语句本身字段、参数完全正常。

### 根因

`specific` 是 **MySQL 保留关键字**。官方 DDL 中建表写作 `` `specific` ``（带反引号）所以建表成功；但 MyBatis-Plus 根据 PO 字段自动生成的 SQL 不带反引号，MySQL 解析到 `specific` 即报语法错误。此类错误在**编译期和启动期都不暴露**，只有真实执行 SQL 时才出现。

### 修复

`tj-promotion/.../domain/po/Coupon.java`：

```java
@TableField("`specific`")
private Boolean specific;
```

### 验证方式

- `mvn clean package -pl tj-promotion -am -DskipTests` 编译通过（2026-07-22）。
- 运行时验证：重启服务后重新调用 `POST /coupons`（待用户确认）。

### 环境备忘

- 本机无全局 mvn；Maven 3.9.14 位于 `~/.m2/wrapper/dists/apache-maven-3.9.14-bin/...`。
- JDK 11 真实路径：`D:\devlop\JDk\jdk-11.0.20_windows-x64_bin\jdk-11.0.20`（注意是双层目录），Git Bash 中需显式设置 `JAVA_HOME` 指向该路径。

## C 端压测验证实录（2026-07-25/26）

### JMeter 适配（课程 jmx 不能直接用）

课件 `day10/资料/jmeter/领取优惠券.jmx` 适配后存仓库 `tmp/领取优惠券-适配.jmx`，改动：端口 8092→8093、券 id 换成本库真实 id、CSV 码文件路径指向 `tmp/exchangeCode.txt`（100 个真实码，由管理端发放后从 DB 导出）、网关组 token 过期故整组禁用。**教训：压测脚本第一优先级是核对"环境四要素"——端口、业务 id、数据文件、鉴权 token**，连接拒绝类报错先查服务是否启动，再查这四项。

### 排错与事故

1. **LockAspect AOP 绑定异常**：IDEA 启动后 `@Lock` 接口全部报 `JoinPointMatch was NOT bound`，根因未锁定（4 轮最小复现均通过），修复为反射取注解，免疫一类绑定失败。详见 [[☕ Java笔记/领券防超发与事务内操作顺序]] 坑 3。
2. **Jackson 日期格式坑**：项目全局 `spring.jackson.date-format=yyyy-MM-dd HH:mm:ss`（空格分隔），DTO `@ApiModelProperty(example)` 写的是 ISO `T` 分隔——Knife4j 预填 example 直接反序列化失败。**example 必须服从项目全局格式，不能照抄课件 ISO 写法**。
3. **限领=1 实测超领 10 张**（= HikariCP 连接池大小）：锁粒度"用户+码"+ RR 快照读 + 连接池并发度三因素叠加。修复为"用户+券"统一锁 + 兑换侧编程式 RLock/TransactionTemplate。完整分析见 [[☕ Java笔记/领券防超发与事务内操作顺序]] 事故实录节。
4. **bitmap 键 TTL 静默失效**：生成码时 expire 落在不存在的键上，修复为先占位建键再 expire。见 [[☕ Java笔记/兑换码设计-签名防伪与三层防爆破]]。

### 压测结论与对账方法

- 多人抢同一码：100 线程 1 成功 + 99"已被使用"（bitmap 原子占位生效）；单用户持 100 码：修复后 1 成功 + 99"超出限领"。
- **三方对账 SQL 一致性判据**：`已核销码数（exchange_code.status=2） = user_coupon 记录数 = coupon.issue_num`，三者不等即有漏洞。
- **一次性测试数据管理**：兑换码用一次即废（status=2 + bitmap 置位），重置环境要**双清**——DB `UPDATE exchange_code SET status=1, user_id=0` + Redis `DEL prs:code:status:{couponId}`，只清一边会数据不一致；`prs:code:base:*`（号段）和 `prs:code:serial`（计数器）不能动，动了码会错位。

## 关联

- 通用结论：[[☕ Java笔记/MySQL保留关键字与MyBatisPlus反引号转义]]
- 模块导航：[[00-天机学堂MOC]]
- 需求采集（仓库内）：`docs/tj-promotion-新增优惠券接口-需求采集.md`
