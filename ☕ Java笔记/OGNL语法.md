---
tags:
  - ognl
date: 2026-06-04
---
# OGNL语法

## 一、OGNL 是什么？一句话版

OGNL 是 **Object-Graph Navigation Language（对象图导航语言）**，在 MyBatis 里，它就是用来在 XML 的 `test` 属性中：

- 读取参数对象的属性
- 做逻辑判断
- 调用对象的方法
- 处理集合

MyBatis 的 `<if>`、`<where>`、`<foreach>` 等标签，都是用它来解析表达式的。

## 二、最基础：访问参数 / 对象属性

### 1. 直接访问参数属性

假设你的参数是一个对象：

```java
public class Dept {
    private String name;
    private Integer status;
}
```

在 XML 中，直接写属性名就能访问：

```xml
<!-- 判断 name 是否非空 -->
<if test="name != null and name != ''">
  and name = #{name}
</if>

<!-- 判断 status 是否为 1 -->
<if test="status == 1">
  and status = #{status}
</if>
```

> 注意：OGNL 会自动从方法的参数对象中，按 `getter` 规则找属性（`name` → `getName()`）。

### 2. 访问 Map 中的键

如果参数是一个 `Map`：

```java
Map<String, Object> params = new HashMap<>();
params.put("keyword", "测试");
params.put("pageSize", 10);
```

XML 中直接写键名即可：

```xml
<if test="keyword != null and keyword != ''">
  and name like concat('%',#{keyword},'%')
</if>
```

## 三、逻辑运算符（最常用）

和 Java 语法几乎一致，直接套用即可：

| 运算符      | 含义       | 示例                          |      |                              |
| :---------- | :--------- | :---------------------------- | :--- | :--------------------------- |
| `==`        | 等于       | `status == 1`                 |      |                              |
| `!=`        | 不等于     | `status != null`              |      |                              |
| `and`       | 并且（&&） | `name != null and name != ''` |      |                              |
| `or`        | 或者（     |                               | ）   | `status == 0 or status == 1` |
| `not` / `!` | 非         | `!name.isEmpty()`             |      |                              |

> 注意：在 XML 中写 `&&` 会被当成特殊字符，所以用 `and` 更安全，这是 MyBatis 中的通用写法。

## 四、字符串处理常用方法

OGNL 可以直接调用 Java 字符串的常用方法，这是 MyBatis 中最常用的技巧：

### 1. 判断字符串是否为空

```xml
<!-- 非空判断（推荐写法） -->
<if test="name != null and name != ''">
  and name like concat('%',#{name},'%')
</if>

<!-- 用 isEmpty() 方法 -->
<if test="name != null and !name.isEmpty()">
  and name like concat('%',#{name},'%')
</if>
```

### 2. 字符串包含判断

```xml
<!-- 判断 name 是否包含 "admin" -->
<if test="name != null and name.contains('admin')">
  and name like '%admin%'
</if>
```

### 3. 字符串长度判断

```xml
<!-- 判断 name 长度是否大于 3 -->
<if test="name != null and name.length() > 3">
  and name = #{name}
</if>
```

## 五、数字 / 布尔判断

### 1. 数字判断（包含边界值）

```xml
<!-- 状态为 0 或 1 -->
<if test="status == 0 or status == 1">
  and status = #{status}
</if>

<!-- 年龄大于等于 18 -->
<if test="age != null and age >= 18">
  and age >= #{age}
</if>
```

### 2. 布尔值判断

```java
// 参数对象
public class User {
    private Boolean isAdmin;
}
```

XML 中直接写属性名即可：

```xml
<!-- isAdmin 为 true 时拼接 -->
<if test="isAdmin">
  and role = 'admin'
</if>

<!-- 为 false 时拼接 -->
<if test="!isAdmin">
  and role = 'user'
</if>
```

## 六、集合 / 数组常用语法（搭配 `<foreach>`）

### 1. 判断集合是否为空

```java
List<Integer> ids = Arrays.asList(1,2,3);
```

XML 中：

```xml
<if test="ids != null and !ids.isEmpty()">
  and id in
  <foreach collection="ids" item="id" open="(" separator="," close=")">
    #{id}
  </foreach>
</if>
```

### 2. 集合大小判断

```xml
<!-- 集合大小大于 0 时才拼接 -->
<if test="ids != null and ids.size() > 0">
  and id in (...)
</if>
```

## 七、进阶：多参数对象访问

如果你的方法有多个参数，比如：

```java
List<Dept> list(String name, Integer status);
```

XML 中可以用 `param1`/`param2` 或 `arg0`/`arg1` 访问：

```xml
<if test="param1 != null and param1 != ''">
  and name = #{param1}
</if>

<if test="param2 != null">
  and status = #{param2}
</if>
```

更推荐的做法是用 `@Param` 注解给参数命名：

```java
List<Dept> list(@Param("name") String name, @Param("status") Integer status);
```

XML 中直接用命名访问：

```xml
<if test="name != null and name != ''">
  and name = #{name}
</if>
```

## 八、避坑指南（新手必看）

1. **`test` 里的字符串要加单引号**

   ```xml
   <!-- 正确 -->
   <if test="status == 1">
   <if test="name != null and name != ''">
   
   <!-- 错误！双引号会和 XML 属性冲突 -->
   <if test="name != null and name != """>
   ```

   **`and` 和 `or` 的优先级**

   `and` 优先级高于 `or`，复杂判断一定要加括号：

   ```xml
   <!-- 正确 -->
   <if test="status != null and (status != '' or status == 0)">
   
   <!-- 错误！可能出现逻辑问题 -->
   <if test="status != null and status != '' or status == 0">
   ```

2. **不要用 `&&`/`||`，用 `and`/`or`**

   XML 会把 `&&` 当成特殊字符解析，导致报错。

   ## 九、最常用的万能模板（直接套用）

```xml
<!-- 字符串非空判断 -->
<if test="xxx != null and xxx != ''">
  and 字段名 like concat('%',#{xxx},'%')
</if>

<!-- 数字非空判断 -->
<if test="xxx != null">
  and 字段名 = #{xxx}
</if>

<!-- 集合非空判断 -->
<if test="ids != null and !ids.isEmpty()">
  and 字段名 in
  <foreach collection="ids" item="id" open="(" separator="," close=")">
    #{id}
  </foreach>
</if>
```

## 相关笔记

- [[☕ Java笔记/Java笔记总览|Java笔记总览]]

- [[☕ Java笔记/Mybatis映射文件标签总结|MyBatis XML 映射]]

