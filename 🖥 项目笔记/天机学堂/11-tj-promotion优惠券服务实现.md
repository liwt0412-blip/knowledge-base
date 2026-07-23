---
tags: [天机学堂, tj-promotion, 优惠券, MyBatis-Plus, 排错]
created: 2026-07-22
---

# 11-tj-promotion 优惠券服务实现

> 记录 tj-promotion（优惠券微服务）的真实代码位置、需求契约、排错过程与当前状态。
> 可复用的通用结论已抽取至 [[☕ Java笔记/MySQL保留关键字与MyBatisPlus反引号转义]]。

## 当前状态（2026-07-22 晚更新）

- 模块骨架已完成并编译通过：端口 8093、服务名 `promotion-service`、数据库 `tj_promotion`、网关路由 `/pm/**`（`/ps` 已被 pay 占用）。
- **管理端接口（7 个，全部编译通过）**：新增 `POST /coupons`、修改 `PUT /coupons/{id}`、分页 `GET /coupons/page`、详情 `GET /coupons/{id}`（含 scopes）、删除 `DELETE /coupons/{id}`、发放 `PUT /coupons/{id}/issue`（立刻/定时 + 期限二选一 XOR）、暂停 `PUT /coupons/{id}/pause`。
- **状态机已打通**：待发放 → 未开始/进行中 ⇄ 已暂停；编辑/删除仅待发放可用；发放允许待发放+已暂停。
- **兑换码链路（2026-07-22 完成）**：发放时 obtainWay=2 异步生成兑换码（Redis 号段分配 + S盒加权签名 + Base32 定长10位，`utils/CodeUtil.java` 含往返自测）；Bitmap 验重封装 `prs:code:status:{couponId}`（SETBIT 旧值判重）+ 号段起始 id hash；签名方案全文见 [[☕ Java笔记/兑换码设计-签名防伪与三层防爆破]]。
- 未实现：C 端领券/兑换接口（user_coupon 表 DDL 未到）、兑换码补偿 XXL-Job（异步失败现为人工补偿）、状态自动流转 Job（未开始→进行中→已结束）、防爆破限流锁定（随兑换接口一起上）。
- 需求契约：仓库 `docs/tj-promotion-新增优惠券接口-需求采集.md`（用户已确认）；官方 DDL：仓库 `docs/ref/tj_promotion.sql`。
- 关键契约点：金额单位为**分**；新增接口**不含时间字段**（期限在"发放"动作中设置）；`specific=true` 时同事务写 `coupon_scope`（type 固定 1=分类）；creater/updater 取 `UserContext`，取不到抛未授权。

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

## 关联

- 通用结论：[[☕ Java笔记/MySQL保留关键字与MyBatisPlus反引号转义]]
- 模块导航：[[00-天机学堂MOC]]
- 需求采集（仓库内）：`docs/tj-promotion-新增优惠券接口-需求采集.md`
