---
tags:
  - mybatis
  - mybatis-plus
date: 2026-06-04
---
# MyBatis → MyBatis Plus 迁移记录

日期：2026-05-02

---

## 一、依赖变更

### 移除
```xml
<!-- 原 MyBatis（注释掉） -->
<dependency>
    <groupId>org.mybatis.spring.boot</groupId>
    <artifactId>mybatis-spring-boot-starter</artifactId>
    <version>3.0.3</version>
</dependency>

<!-- PageHelper（已删除） → 改用 MP 内置分页插件 -->
<dependency>
    <groupId>com.github.pagehelper</groupId>
    <artifactId>pagehelper-spring-boot-starter</artifactId>
    <version>1.4.6</version>
</dependency>
```

### 添加
```xml
<!-- qk-management/pom.xml -->
<dependency>
    <groupId>com.baomidou</groupId>
    <artifactId>mybatis-plus-spring-boot3-starter</artifactId>
    <version>3.5.8</version>
</dependency>

<!-- qk-common/pom.xml（提供 @Component/@Autowired 等注解编译依赖） -->
<dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter</artifactId>
</dependency>
```

---

## 二、配置变更

### application.yml
```yaml
# 改前（MyBatis 前缀，MP 不识别）
mybatis:
  configuration:
    log-impl: org.apache.ibatis.logging.stdout.StdOutImpl
    map-underscore-to-camel-case: true
  mapper-locations: classpath:mapper/*xml

# 改后（MP 前缀）
mybatis-plus:
  configuration:
    log-impl: org.apache.ibatis.logging.stdout.StdOutImpl
    map-underscore-to-camel-case: true
  mapper-locations: classpath:mapper/*.xml
```

---

## 三、新增文件

### MyBatisPlusConfig.java
```java
@Configuration
public class MyBatisPlusConfig {
    @Bean
    public MybatisPlusInterceptor mybatisPlusInterceptor() {
        MybatisPlusInterceptor interceptor = new MybatisPlusInterceptor();
        interceptor.addInnerInterceptor(new PaginationInnerInterceptor(DbType.MYSQL));
        return interceptor;
    }
}
```
路径：`qk-management/src/main/java/com/qkgj/config/MyBatisPlusConfig.java`

---

## 四、Mapper 层改动（5个文件）

### 改动模式
所有分页查询的 Mapper 方法，原来只有 DTO 参数，现在加 `Page` 作为**第一个参数**，并加 `@Param` 注解：

```java
// 改前
List<Activity> listActivities(ActivitiesDto dto);

// 改后
Page<Activity> listActivities(Page<Activity> page, @Param("dto") ActivitiesDto dto);
```

### 涉及文件
| Mapper | 方法 | 参数 |
|--------|------|------|
| `ActivitiesMapper.java` | `listActivities` | `(Page<Activity> page, @Param("dto") ActivitiesDto dto)` |
| `CourseMapper.java` | `listCourse` | `(Page<Course> page, @Param("dto") CourseDto dto)` |
| `UserMapper.java` | `getUser` | `(Page<UserDJ> page, @Param("dto") UserDto dto)` |
| `DeptMapper.java` | `selectByCondition` | `(Page<Dept> page, String name, Integer status)` |
| `RoleMapper.java` | `selectByCondition` | `(Page<Role> page, String name)` |

---

## 五、XML 层改动（3个文件）

### 改动模式
加了 `@Param("dto")` 后，XML 里的参数引用需要加 `dto.` 前缀：

```xml
<!-- 改前 -->
<if test="channel != null and channel != 0">
   and channel = #{channel}
</if>

<!-- 改后 -->
<if test="dto.channel != null and dto.channel != 0">
   and channel = #{dto.channel}
</if>
```

### 涉及文件（仅 DTO 参数的 XML）
| XML 文件 | 改动 |
|----------|------|
| `ActivitiesMapper.xml` | `channel`, `type`, `status` → `dto.channel`, `dto.type`, `dto.status` |
| `CourseMapper.xml` | `name`, `subject`, `target` → `dto.name`, `dto.subject`, `dto.target` |
| `UserMapper.xml` | `name`, `status`, `phone`, `deptId` → `dto.name`, `dto.status`, `dto.phone`, `dto.deptId` |

**不需要改的 XML**：参数是简单类型（String/Integer）直接匹配参数名的，如 DeptMapper/RoleMapper 仍用 `#{name}`。

---

## 六、Service 层改动（5个文件）

### 改动模式
```java
// 改前（PageHelper）
PageHelper.startPage(dto.getPage(), dto.getPageSize());
List<Entity> list = mapper.list(dto);
PageInfo info = PageInfo.of(list);
return new PageResult(info.getTotal(), info.getList());

// 改后（MyBatis Plus）
Page<Entity> page = new Page<>(dto.getPage(), dto.getPageSize());
mapper.list(page, dto);  // 不接返回值，Page 对象被动填充
return new PageResult(page.getTotal(), page.getRecords());
```

### 涉及文件
| ServiceImpl | 改动 |
|-------------|------|
| `ActivitiesServiceImpl.java` | PageHelper → `Page<Activity>` |
| `CourseServiceImpl.java` | PageHelper → `Page<Course>` |
| `UserServiceImpl.java` | PageHelper → `Page<UserDJ>` + 隐藏密码改为 `page.getRecords().forEach(...)` |
| `DeptServiceImpl.java` | PageHelper → `Page<Dept>` |
| `RoleServiceImpl.java` | PageHelper → `Page<Role>` |

---

## 七、遇到的问题及解决方案

### 问题1：PageHelper 和 MyBatis Plus 的 jsqlparser 版本冲突
- **错误**：`java.lang.ClassNotFoundException: net.sf.jsqlparser.statement.select.SelectBody`
- **原因**：MP 3.5.8 自带 jsqlparser 5.0，PageHelper 用的老版本不兼容
- **解决**：从根 pom.xml 和 qk-management/pom.xml 中删除 PageHelper 依赖

### 问题2：配置前缀不兼容
- **错误**：项目运行但 SQL 不执行
- **原因**：MP 不识别 `mybatis:` 前缀的配置
- **解决**：`application.yml` 中 `mybatis:` 改为 `mybatis-plus:`

### 问题3：`@Param` 缺少 import
- **错误**：`java: 找不到符号 类 Param`
- **原因**：加了 `@Param("dto")` 但没加 import
- **解决**：在 CourseMapper/ActivitiesMapper/UserMapper 中添加 `import org.apache.ibatis.annotations.Param;`

### 问题4：XML 参数名不匹配（最隐蔽）
- **现象**：`{ "total": 7, "rows": [] }` — COUNT 有数据，SELECT 返回空
- **原因**：方法从单参数 `(Dto dto)` 变成双参数 `(Page page, Dto dto)` 后，XML 的 `#{name}` 无法匹配到 DTO 中的字段
- **解决**：加 `@Param("dto")` + XML 中引用改为 `#{dto.name}` / `#{dto.channel}` / 等
- **注意**：此问题仅发生在**第二个参数是 DTO 对象**的情况；若第二个参数是 String/Integer 等简单类型则无需改

### 问题5：Mapper 方法返回 `List<>` 时分页数据为空
- **现象**：COUNT 正确但 `page.getRecords()` 始终为空
- **原因**：MP 的分页拦截器需要在方法上标注 `Page<>` 返回类型才能正确填充 Page 对象
- **解决**：Mapper 方法返回类型从 `List<Entity>` 改为 `Page<Entity>`，Service 中不再接返回值

---

## 八、总结：MyBatis → MP 迁移检查清单

- [ ] 添加 MP 依赖，删除 MyBatis 依赖
- [ ] 删除 PageHelper 依赖
- [ ] 新增 `MyBatisPlusConfig` 注册分页插件
- [ ] `application.yml` 中 `mybatis:` → `mybatis-plus:`
- [ ] Mapper 方法加 `Page` 参数，返回 `Page<>`
- [ ] DTO 参数加 `@Param("dto")`
- [ ] XML 中参数引用改为 `dto.xxx`
- [ ] Service 中改为 `new Page<>()`，不接返回值

## 相关笔记
- [[☕ Java笔记/MybatisPlus笔记|MyBatis Plus 使用指南]]
- [[🖥 项目笔记/CRM/Bug日志|MP 迁移踩坑]]
