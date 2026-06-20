---
tags:
  - mybatis-plus
date: 2026-06-04
---
# MyBatisPlus笔记

## 一、环境准备

### （一）添加依赖

在需要用到操作数据库的模块的pom.xml文件中添加依赖：

注意JDK17以下的版本要使用MybatisPlus2，JDK17及以上的版本要使用MybatisPlus3，这两个版本的依赖的artifactId是不同的

```xml
<!-- JDK17: MyBatisPlus 3.5.8-->
<dependency>
	<groupId>com.baomidou</groupId>
		<artifactId>mybatis-plus-spring-boot3-starter</artifactId>
	<version>3.5.8</version>
</dependency>
```



### （二）添加核心配置

在application.yml文件中新增MyBatisPlus配置，同时**<span style="color:red">删除Mybatis相关的配置</span>**

如果配置了PageHelper插件，要注意，如果是2.1.0版本以下的，可能会与MyBatisPlus冲突，解决方式：要么删除PageHelper插件，用MyBatisPlus重写分页方法；要么就不使用MyBatisPlus。

```yaml
# MyBatisPlus配置
mybatis-plus:
  # 搜索指定包别名
  typeAliasesPackage: com.zzyl.**.domain
  # 配置mapper的扫描，找到所有的mapper.xml映射文件
  mapperLocations: classpath*:mapper/**/*Mapper.xml
  # 全局配置
  global-config:
    db-config:
      id-type: auto   #id生成策略为自增
  configuration: 
    map-underscore-to-camel-case: true    #字段与属性，自动转换为驼峰命名
```



### （三）新增核心配置类，删除MyBatisConfig

```java
package com.zzyl.framework.config;

import com.baomidou.mybatisplus.annotation.DbType;
import com.baomidou.mybatisplus.extension.plugins.MybatisPlusInterceptor;
import com.baomidou.mybatisplus.extension.plugins.inner.BlockAttackInnerInterceptor;
import com.baomidou.mybatisplus.extension.plugins.inner.OptimisticLockerInnerInterceptor;
import com.baomidou.mybatisplus.extension.plugins.inner.PaginationInnerInterceptor;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.transaction.annotation.EnableTransactionManagement;

/**
 * Mybatis Plus 配置
 */
@EnableTransactionManagement(proxyTargetClass = true)
@Configuration
public class MybatisPlusConfig {

    @Bean
    public MybatisPlusInterceptor mybatisPlusInterceptor() {
        MybatisPlusInterceptor interceptor = new MybatisPlusInterceptor();
        // 分页插件
        interceptor.addInnerInterceptor(paginationInnerInterceptor());
        // 乐观锁插件
        interceptor.addInnerInterceptor(optimisticLockerInnerInterceptor());
        // 阻断插件
        interceptor.addInnerInterceptor(blockAttackInnerInterceptor());
        return interceptor;
    }

    /**
     * 分页插件，自动识别数据库类型 https://baomidou.com/guide/interceptor-pagination.html
     */
    public PaginationInnerInterceptor paginationInnerInterceptor() {
        PaginationInnerInterceptor paginationInnerInterceptor = new PaginationInnerInterceptor();
        // 设置数据库类型为mysql
        paginationInnerInterceptor.setDbType(DbType.MYSQL);
        // 设置最大单页限制数量，默认 500 条，-1 不受限制
        paginationInnerInterceptor.setMaxLimit(-1L);
        return paginationInnerInterceptor;
    }

    /**
     * 乐观锁插件 https://baomidou.com/guide/interceptor-optimistic-locker.html
     */
    public OptimisticLockerInnerInterceptor optimisticLockerInnerInterceptor() {
        return new OptimisticLockerInnerInterceptor();
    }

    /**
     * 如果是对全表的删除或更新操作，就会终止该操作 https://baomidou.com/guide/interceptor-block-attack.html
     */
    public BlockAttackInnerInterceptor blockAttackInnerInterceptor() {
        return new BlockAttackInnerInterceptor();
    }
}
```



### （四）添加Service和Mapper层继承实现

- 在Mapper层继承 BaseMapper<T>
- 在Service层继承 Iservice<T>
- 在ServiceImpl层继承 ServiceImpl<TMapper, T>



### （五）在实体类上添加注解

- 在类名与数据库表名不对应的实体类上添加`@TableName("Xxx")`注解
- 在属性名与字段名不一致的成员变量上添加`@TableField("xxx")`注解
- 在实体类的扩展字段上添加`@TableField(exist = false)`注解
- 在需要指定主键的成员变量上添加注解`@TableId(value = "id", type = IdType.AUTO)`
  - type = IdType.AUTO：自动增长
  - type = IdType.INPUT：用户输入
  - type = IdType.ASSIGN_ID：雪花算法生成一个ID
  - type = IdType.ASSIGN_UUID：ASSIGN_UUID生成一个UUID



## 二、两层增删改查方法名的区别

|      | Controller层                        | ServiceImpl层                               |
| ---- | ----------------------------------- | ------------------------------------------- |
| 增加 | save                                | insert                                      |
| 删除 | remove                              | delete                                      |
| 修改 | update                              | update                                      |
| 查询 | get                                 | select                                      |
| 多查 | list（可传Wrapper对象，不传就全查） | selectList（可传Wrapper对象，不传也是全查） |



## 三、Wrapper用法

Wrapper 是 MyBatisPlus（MP）最核心的功能，**专门用来拼接复杂的 SQL 条件**（where、order by、group by、having 等），不用写 XML，纯 Java 代码就能实现复杂查询，非常方便。

### （一）Wrapper 是什么？有哪些？

Wrapper = **条件构造器**，用来生成 SQL 的 `where` 条件。

MP 提供 2 个最常用的实现类：

1. **QueryWrapper**：用于**查询、删除**，只查需要的字段，可排序、分组
2. **UpdateWrapper**：用于**更新**，可以灵活设置 `set` 字段

### （二）Wrapper使用方法示例

```java
// 查询 name = 张三
QueryWrapper<User> wrapper = new QueryWrapper<>();
wrapper.eq("name", "张三");
List<User> list = userMapper.selectList(wrapper);
```

对应SQL：

```mysql
SELECT * FROM user WHERE name = '张三'
```

### （三）条件查询方法

#### 1. 基础条件方法（最常用）

| 方法名 | 含义        | 对应 SQL | 示例写法                   |
| :----- | :---------- | :------- | :------------------------- |
| **eq** | 等于 =      | =        | eq (User::getName, "张三") |
| **ne** | 不等于！=   | !=       | ne(User::getAge, 18)       |
| **gt** | 大于 >      | >        | gt(User::getAge, 20)       |
| **ge** | 大于等于 >= | >=       | ge(User::getAge, 18)       |
| **lt** | 小于 <      | <        | lt(User::getAge, 30)       |
| **le** | 小于等于 <= | <=       | le(User::getAge, 60)       |

------

#### 2. 模糊查询方法

| 方法名        | 含义          | 对应 SQL      | 示例写法                        |
| :------------ | :------------ | :------------ | :------------------------------ |
| **like**      | 全模糊 % 值 % | LIKE '% 值 %' | like (User::getName, "张")      |
| **likeLeft**  | 左模糊 % 值   | LIKE '% 值'   | likeLeft (User::getName, "三")  |
| **likeRight** | 右模糊 值 %   | LIKE ' 值 %'  | likeRight (User::getName, "张") |
| **notLike**   | 不包含        | NOT LIKE      | notLike (User::getName, "李")   |

------

#### 3. 范围 / 空值查询

| 方法名         | 含义       | 对应 SQL        | 示例写法                        |
| :------------- | :--------- | :-------------- | :------------------------------ |
| **between**    | 在区间内   | BETWEEN A AND B | between(User::getAge, 18, 30)   |
| **notBetween** | 不在区间内 | NOT BETWEEN     | notBetween(...)                 |
| **in**         | 在集合中   | IN(...)         | in(User::getId, List.of(1,2,3)) |
| **notIn**      | 不在集合中 | NOT IN          | notIn(...)                      |
| **isNull**     | 字段为空   | IS NULL         | isNull(User::getEmail)          |
| **isNotNull**  | 字段非空   | IS NOT NULL     | isNotNull(User::getEmail)       |

------

#### 4. 逻辑 / 组合条件

| 方法名     | 含义          | 作用                   |
| :--------- | :------------ | :--------------------- |
| **and**    | 并且（默认）  | 多条件直接拼接就是 AND |
| **or**     | 或者          | 拼接 OR 条件           |
| **nested** | 嵌套条件      | 用于包裹复杂括号条件   |
| **last**   | 追加 SQL 末尾 | 直接拼语句（慎用）     |

------

#### 5. 排序 / 分页

| 方法名          | 含义 | 示例                             |
| :-------------- | :--- | :------------------------------- |
| **orderByAsc**  | 升序 | orderByAsc(User::getCreateTime)  |
| **orderByDesc** | 降序 | orderByDesc(User::getCreateTime) |



### （四）多条件拼接

```java
// 默认L多个条件自动用and连接
// status = 1 AND age > 18 AND name LIKE '%张%';
QueryWrapper<User> wrapper = new QueryWrapper<>();
wrapper.eq("status", 1)
       .gt("age", 18)
       .like("name", "张");

// 手动使用or
// status = 1 OR age > 30;
wrapper.eq("status", 1)
       .or()
       .gt("age", 30);

//复杂嵌套条件（优先级）
// (status=1) AND (age>18 OR name LIKE '%张%')
wrapper.eq("status", 1)
       .and(w -> w.gt("age", 18).or().like("name", "张"));


// 排序、指定查询字段============
QueryWrapper<User> wrapper = new QueryWrapper<>();

// 只查 id, name, age 三个字段
wrapper.select("id", "name", "age");

// 排序：age 升序，id 降序
wrapper.orderByAsc("age")
       .orderByDesc("id");
//============================


// 分组与聚合查询
// 按 status 分组，统计每组人数
wrapper.select("status", "count(*) as count")
       .groupBy("status")
       .having("count(*) > 2");
```



## 四、LambdaQueryWrapper用法

**解决硬编码字符串写错字段名的问题**，用 **Lambda 表达式**直接引用实体类字段。这是企业开发**最推荐**的写法！

```java
// 写法 1
LambdaQueryWrapper<User> wrapper = new LambdaQueryWrapper<>();
wrapper.eq(User::getName, "张三")
       .gt(User::getAge, 18);

// 写法 2（更简洁）
LambdaQueryWrapper<User> wrapper = Wrappers.lambdaQuery();
wrapper.eq(User::getStatus, 1);
```

**优点**：

- 编译时检查字段，不会写错
- 重构字段名时自动同步
- 代码更优雅



## 五、UpdateWrapper（更新专用）

用于**动态更新字段**，可以使用`setSql`来插入sql语句，比 `updateById` 更灵活。

```java
UpdateWrapper<User> wrapper = new UpdateWrapper<>();
// 1. 更新条件
wrapper.eq("id", 10)
       .eq("status", 1);

// 2. 普通赋值
wrapper.set("name", "新名字");

// 3. age 在原来基础上 +1
wrapper.setSql("age = age + 1"); 

// 执行更新
userMapper.update(null, wrapper);
```

对应SQL：

```mysql
UPDATE user 
SET name = '新名字', age = age + 1 
WHERE id = 10 AND status = 1
```

Lambda 版（推荐）：

```java
LambdaUpdateWrapper<User> wrapper = Wrappers.lambdaUpdate();
wrapper.eq(User::getId, 10)
       .eq(User::getStatus, 1)
       .set(User::getName, "新名字")
       .setSql("age = age + 1"); // 自增
userMapper.update(null, wrapper);
```



## 六、实用技巧

### （一）动态拼接查询语句

```java
String name = null; // 前端没传
Integer age = 20;

LambdaQueryWrapper<User> wrapper = Wrappers.lambdaQuery();
wrapper.eq(name != null, User::getName, name)  // 条件为true才拼接
       .gt(age != null, User::getAge, age);
```

**所有 Wrapper 方法都支持第一个参数传 boolean**，非常方便！



### （二）查询一条数据

```java
User user = userMapper.selectOne(wrapper);
```

注意：确保结果**只有一条**，否则报错。



### （三）查询总数

```java
Long count = userMapper.selectCount(wrapper);
```



### （四）清空所有条件

```java
wrapper.clear();
```



## 七、完整案例示例

```java
@Service
public class UserServiceImpl implements UserService {

    @Autowired
    private UserMapper userMapper;

    @Override
    public List<User> getUserList(String name, Integer minAge, Integer maxAge) {
        // 1. 创建 Lambda 条件构造器
        LambdaQueryWrapper<User> wrapper = Wrappers.lambdaQuery();

        // 2. 动态条件
        wrapper.like(StringUtils.hasText(name), User::getName, name);
        wrapper.ge(minAge != null, User::getAge, minAge);
        wrapper.le(maxAge != null, User::getAge, maxAge);

        // 3. 只显示正常用户
        wrapper.eq(User::getStatus, 1);

        // 4. 排序
        wrapper.orderByDesc(User::getId);

        // 5. 查询
        return userMapper.selectList(wrapper);
    }
}
```

## 相关笔记

- [[☕ Java笔记/Java笔记总览|Java笔记总览]]

- [[📋 技术速查/MyBatis迁移到MP记录|MyBatis → MP 迁移实录]]
- [[☕ Java笔记/Mybatis映射文件标签总结|MyBatis XML 标签总结]]

