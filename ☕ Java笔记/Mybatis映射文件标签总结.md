---
tags:
  - mybatis
date: 2026-06-04
---
# mybatis的xml映射文件标签

## 一、常用核心标签

### `<if>` 条件判断

作用：动态拼接 SQL，**非空才拼接**

```xml
<select id="findUser" resultType="User">
    SELECT * FROM user
    WHERE 1=1
    <if test="name != null and name != ''">
        AND name LIKE CONCAT('%',#{name},'%')
    </if>
    <if test="age != null">
        AND age = #{age}
    </if>
</select>
```



### `<where>` 智能 where 标签

作用：**自动去掉多余的 AND / OR**，不用写 WHERE 1=1

```xml
<select id="findUser" resultType="User">
    SELECT * FROM user
    <where>
        <if test="name != null">
            AND name = #{name}
        </if>
        <if test="age != null">
            AND age = #{age}
        </if>
    </where>
</select>
```



### `<set>` 智能更新标签

作用：更新时**自动处理逗号**，避免语法错误

```xml
<update id="updateUser">
    UPDATE user
    <set>
        <if test="name != null">name=#{name},</if>
        <if test="age != null">age=#{age},</if>
    </set>
    WHERE id=#{id}
</update>
```



### `<resultMap>` 结果映射（超级重要）

作用：

- 数据库字段 `user_name` → 实体属性 `userName`
- 一对一、一对多查询必须用它

```xml
<resultMap id="UserMap" type="User">
    <id column="id" property="id"/>
    <result column="name" property="name"/>
    <result column="age" property="age"/>
</resultMap>

<select id="selectList" resultMap="UserMap">
    SELECT id,name,age FROM user
</select>
```



## 二、高级常用标签

### `<foreach>` 循环（in 查询）

作用：拼接 `IN (1,2,3)`

```xml
<select id="selectByIds" resultType="User">
    SELECT * FROM user WHERE id IN
    <foreach collection="ids" open="(" separator="," close=")" item="id">
        #{id}
    </foreach>
</select>
```



### `<sql>` + `<include>` 抽取重复 SQL

作用：把重复字段抽出来复用

```xml
<sql id="Base_Column">
    id,name,age,email
</sql>

<select id="selectOne" resultType="User">
    SELECT <include refid="Base_Column"/> FROM user WHERE id=#{id}
</select>
```



## `<choose>` `<when>` `<otherwise>`

作用：相当于 **if...else if...else**

```xml
<select id="findUser" resultType="User">
    SELECT * FROM user
    <where>
        <choose>
            <when test="name != null">
                name = #{name}
            </when>
            <when test="age != null">
                age = #{age}
            </when>
            <otherwise>
                status = 1
            </otherwise>
        </choose>
    </where>
</select>
```

这个标签与<if>标签的区别在于，<if>标签是三个条件都判断，而这个标签是从上往下执行，只要其中有一个成立，就不执行后面的分支。



### `<trim>` 万能格式化标签

可以自定义去除前后多余字符，`where` 和 `set` 底层就是它。

```xml
<trim prefix="WHERE" prefixOverrides="AND |OR ">
  ...
</trim>
```



## 三、一对多 / 多对多标签

### `<association>` 多对一（单个对象）

```xml
<resultMap id="OrderMap" type="Order">
    <id column="order_id" property="id"/>
    <result column="order_no" property="orderNo"/>
    <!-- 多对一：多个订单对应一个用户 -->
    <association property="user" javaType="User">
        <result column="name" property="name"/>
    </association>
</resultMap>
```



### `<collection>` 一对多（集合）

```xml
<resultMap id="UserMap" type="User">
    <id column="id" property="id"/>
    <!-- 一对多：一个用户多个订单 -->
    <collection property="orderList" ofType="Order">
        <result column="order_no" property="orderNo"/>
    </collection>
</resultMap>
```

注意：多对一和一对多的用法、业务场景不一样，不可以相互替换。

以用户、订单举例：

实体

```java
// 用户 一对多 订单
class User{
    private Long id;
    private List<Order> orderList;
}
// 订单 多对一 用户
class Order{
    private Long id;
    private User user;
}
```

多对一association（查订单带出所属用户）

```xml
<resultMap id="OrderMap" type="Order">
    <id column="o_id" property="id"/>
    <association property="user" javaType="User">
        <id column="u_id" property="id"/>
        <result column="u_name" property="name"/>
    </association>
</resultMap>
```

一对多collection（查用户带出全部订单）

```xml
<resultMap id="UserMap" type="User">
    <id column="u_id" property="id"/>
    <collection property="orderList" ofType="Order">
        <id column="o_id" property="id"/>
    </collection>
</resultMap>
```

### 转换逻辑

1. 查订单看用户：只能用`association`，不能换成 collection
2. 查用户看订单：只能用`collection`，不能换成 association
3. **切换查询主体**，就能从一对多变成多对一查询，实现业务层面的数据转换，标签语法不可互换

## 相关笔记

- [[☕ Java笔记/Java笔记总览|Java笔记总览]]

- [[☕ Java笔记/MybatisPlus笔记|MyBatis Plus 笔记]]
- [[☕ Java笔记/OGNL语法|OGNL 语法详解]]