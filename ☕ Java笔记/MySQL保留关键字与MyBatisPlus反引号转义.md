---
tags: [MySQL, MyBatis-Plus, 排错, 保留关键字, DDL]
created: 2026-07-22
---

# MySQL 保留关键字与 MyBatis-Plus 反引号转义

> 适用：任何使用 MyBatis-Plus（或 MyBatis 自动生成 SQL）+ MySQL 的项目。
> 来源：天机学堂 tj-promotion `specific` 字段排错（2026-07-22），项目过程见 [[🖥 项目笔记/天机学堂/11-tj-promotion优惠券服务实现]]。

## 问题模式

- **现象**：`BadSqlGrammarException` / `SQLSyntaxErrorException`，报错文本 `near 'xxx, ...'`，其中 `xxx` 是某个列名；而 MyBatis-Plus 打印的 SQL 字段、参数看起来完全正常。
- **根因**：该列名是 MySQL **保留关键字**。建表 DDL 中带反引号（`` `xxx` ``）所以能建表成功，但 MyBatis-Plus 根据实体字段自动生成的 INSERT/UPDATE/SELECT 不带反引号，运行时才炸。
- **隐蔽性**：编译、启动、连接池初始化全部正常，只有真实执行到该 SQL 才报错，是典型的"运行时才暴露"问题。

## 修复

在 PO 字段上显式声明带反引号的列名：

```java
@TableField("`specific`")
private Boolean specific;
```

MyBatis-Plus 会将注解值原样拼入所有自动 SQL。纯 XML 手写的 SQL 则需在 SQL 里自行加反引号。

## 高频踩坑保留字（建表/建实体前先扫一遍）

`specific`、`order`、`key`、`desc`/`describe`、`rank`（8.0 新增）、`system`、`group`、`values`、`status` 安全但 `state`/`type`/`name` 等非保留字无需处理。
完整清单以官方为准：https://dev.mysql.com/doc/refman/8.0/en/keywords.html （带 (R) 标记的是保留字）。

## 预防检查清单（接入第三方/官方 DDL 时）

1. 拿到 DDL 先扫所有**带反引号**的列名——反引号就是"我是关键字或特殊名"的信号，对应的 PO 字段必须加 `@TableField` 反引号转义。
2. 不能只验证"表能建出来"：建表成功 ≠ MyBatis-Plus 能操作该表，必须以一次真实 insert/select 作为验收。
3. 代码生成器（MP generator）生成的实体不会自动加反引号，生成后需人工比对 DDL 反引号列。

## 失效边界

- 仅适用于保留关键字场景；`near` 报错也可能由其它语法问题引起，需先确认报错位置紧邻的 token 是否为列名。
- 若项目统一开启了全局转义（如 MP 的 `columnFormat` 或自定义元对象处理器），可替代逐字段注解，但要验证对 `@TableField` 显式指定的列不会二次转义。

## 关联

- 项目排错实例：[[🖥 项目笔记/天机学堂/11-tj-promotion优惠券服务实现]]
- 入口：[[00-Java开发与工程实践入口]]
