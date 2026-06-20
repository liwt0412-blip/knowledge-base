---
tags:
  - 项目/CRM
  - bug
date: 2026-06-04
---
# 🐛 Bug 日志

记录项目开发中遇到的 Bug 及解决方案。

---

<!--
新增格式：
## Bug #序号 - [日期] [项目]
- **问题描述**：
- **错误信息**：
- **根因分析**：
- **解决方法**：
- **相关文件**：
-->

## Bug #1 — 2026-05-05 mp-quickstart

### MyBatis Plus 依赖拉不下来
- **问题描述**：IDEA刷新Maven报 `Unresolved plugin: maven-clean-plugin:3.3.2`，MP依赖下载失败
- **错误信息**：插件Unresolved，依赖解析失败
- **根因分析**：
  1. pom.xml中MP版本写成了`3.5.15`（不存在，最新为`3.5.7`）
  2. Maven settings.xml阿里云镜像地址过期（`http://maven.aliyun.com/nexus/content/groups/public/` → 应改为`https://maven.aliyun.com/repository/public`）
  3. IDEA的`.idea/jarRepositories.xml`硬编码了Maven Central直连地址，绕过镜像
  4. Mapper接口未继承BaseMapper，MP自动装配链路不完整导致依赖解析失败
- **解决方法**：
  1. pom.xml版本改为`3.5.7`
  2. settings.xml阿里云镜像改为新地址
  3. 删除jarRepositories.xml
  4. Mapper继承BaseMapper
- **相关文件**：pom.xml, settings.xml, .idea/jarRepositories.xml, ActivityMapper.java, CourseMapper.java

---

## Bug #2 — 2026-05-05 mp-quickstart

### selectList 参数类型不匹配
- **问题描述**：`selectList(channel, type, status)` 编译报错，Required type为IPage/Wrapper/ResultHandler，Provided为Integer
- **错误信息**：`Required: IPage<Activity> / Wrapper<Activity> / ResultHandler, Provided: Integer`
- **根因分析**：BaseMapper的`selectList()`只接收`Wrapper<T>`一个参数，不能直接传业务字段
- **解决方法**：用QueryWrapper/LambdaQueryWrapper构建查询条件，`selectList(wrapper)`
- **相关文件**：ActivityServiceImpl.java, CourseServiceImpl.java

---

## Bug #3 — 2026-05-05 mp-quickstart

### String.equals(' ') 条件永远为false
- **问题描述**：QueryWrapper的eq条件`name != null && !name.equals(' ')`中后半段永远为true
- **根因分析**：Java单引号`' '`是char类型，`String.equals(char)`永远返回false（类型不同）。该条件相当于没写判空
- **解决方法**：改为`!name.equals("")`或`!name.trim().isEmpty()`
- **相关文件**：CourseServiceImpl.java 第72行

---

## Bug #4 — 2026-05-05 mp-quickstart

### Page类名冲突（PageHelper vs MyBatis Plus）
- **问题描述**：`Page pageInfo = activityMapper.selectPage(...)` 编译报错或运行时类型不匹配
- **错误信息**：import冲突，两个包都有`Page`类
- **根因分析**：PageHelper(`com.github.pagehelper.Page`)和MP(`com.baomidou.mybatisplus.extension.plugins.pagination.Page`)类名相同，不能同时import。且MP的Page用`getRecords()`取数据，PageHelper的Page用`getResult()`
- **解决方法**：改用MP分页后注释掉`com.github.pagehelper.Page`的import；取数据用`getRecords()`
- **相关文件**：ActivityServiceImpl.java

---

## Bug #5 — 2026-05-05 qk-parent

### 项目启动失败：pom配置未同步 + XML语法错误 + 依赖缺失 + Bean重复
- **问题描述**：qk-parent项目无法启动
- **根因分析**：
  1. 根pom.xml第2行 `<project>` → 多余的 `>` 破坏了XML
  2. qk-management/pom.xml仍用原生MyBatis，上次迁移只改了yml没改pom
  3. qk-common缺 `spring-boot-starter`，Spring注解无法解析
  4. qk-entity/pom.xml MP版本 `3.5.15`不存在，且引了完整starter
  5. application.yml `mapper-locations` 缺了点号
- **解决方法**：
  1. 根pom.xml修复XML语法
  2. qk-management: 原生MyBatis → mybatis-plus-spring-boot3-starter 3.5.7
  3. qk-common: 加 spring-boot-starter
  4. qk-entity: starter → mybatis-plus-annotation 3.5.7
  5. application.yml: `*xml` → `*.xml`
- **相关文件**：根pom.xml, qk-management/pom.xml, qk-common/pom.xml, qk-entity/pom.xml, application.yml

---

## Bug #6 — 2026-05-05 qk-parent

### LEFT JOIN 关联数据为 NULL — 非代码问题，数据库数据缺失
- **问题描述**：前端Clue列表页"归属人姓名"字段始终为空
- **错误信息**：无报错，SQL正常返回但 assign_name 列为 null
- **SQL日志**：`select c.*, u.name as assign_name from clue c left join user u on c.user_id = u.id` → assign_name 全部为 null
- **根因分析**：大部分 clue 记录的 `user_id` 为 NULL，仅一条 `user_id=2`，但 user 表中不存在 id=2 的用户，LEFT JOIN 匹配不到任何记录
- **解决方法**：向 user 表插入缺失的用户数据，或使用 clue 表中实际存在的 user_id
- **排查经验**：遇到 LEFT JOIN 关联字段全 NULL 时，先查关联表对应 ID 是否存在，不要直接怀疑代码或映射问题

---

## Bug #7 — 2026-05-05 qk-parent

### BusinessMapper 未继承 BaseMapper，导致 BusinessServicelImpl 红色波浪线

- **问题描述**：`BusinessServicelImpl extends ServiceImpl<BusinessMapper, Business>` 在 IDE 中报红色波浪线，要求重写所有方法
- **错误信息**：IDE 提示实现类需要实现 IService 接口的所有方法
- **根因分析**：`ServiceImpl<M, T>` 要求第一个泛型参数 M 必须继承 `BaseMapper<T>`。而 `BusinessMapper` 是个空接口，没有 `extends BaseMapper<Business>`，导致类型约束不满足，编译器认为实现类未实现 IService 的抽象方法
- **解决方法**：BusinessMapper 加 `extends BaseMapper<Business>`，同时加 `import com.baomidou.mybatisplus.core.mapper.BaseMapper` 和 `import com.qkgj.entity.Business`
- **相关文件**：`qk-management/src/main/java/com/qkgj/mapper/BusinessMapper.java`

---

## Bug #8 — 2026-05-06 qk-parent

### Business分页不生效 — Page类导错包（PageHelper vs MP）

- **问题描述**：`BusinessMapper.listbusiness()` 查询返回全表数据，没有分页效果
- **错误信息**：无报错，SQL正常执行但不加 LIMIT
- **根因分析**：
  1. `BusinessMapper.java` 和 `BusinessServicelImpl.java` 都导入了 `com.github.pagehelper.Page`（PageHelper的Page类）
  2. MyBatis Plus的 `PaginationInnerInterceptor` 只识别 `com.baomidou.mybatisplus.extension.plugins.pagination.Page`
  3. 传给Mapper的Page参数是PageHelper的Page → 拦截器不认识 → 不走分页逻辑
  4. 此外，Service层调用的是 `pageInfo.getResult()`，这是PageHelper的API，MP的Page用 `getRecords()`
- **为什么删了import又自己回来**：代码里同时用了 `Page<Business>` 和 `pageInfo.getResult()`。删掉PageHelper的import后，IDE发现两件事：
  1. `Page` 类未解析 → 自动搜索classpath，有两个候选（PageHelper的Page 和 MP的Page）
  2. `getResult()` 只在PageHelper的Page上存在，MP的Page没有这个方法
  3. IDE为了满足 `getResult()` 编译通过，自动选回了PageHelper的Page
- **解决方法**：
  1. 两个文件的 `import com.github.pagehelper.Page` → `import com.baomidou.mybatisplus.extension.plugins.pagination.Page`
  2. `pageInfo.getResult()` → `pageInfo.getRecords()`
  3. 改完手动删除旧import，不要让IDE自动优化导入（或者关掉"Optimize imports on save"）
- **相关文件**：
  - `BusinessMapper.java`（第4行 import）
  - `BusinessServicelImpl.java`（第4行 import，第21行 getResult()→getRecords()）
  - `BusinessMapper.xml`（第7行 c.*→b.*，SQL注入修复）

---

## Bug #9 — 2026-05-06 qk-parent

### 前端登录未传入 roleLabel → 后端无法识别角色 → 权限功能失效

- **问题描述**：登录时如果数据库没有对应角色标识（`roleLabel` 为空），后续按角色分配线索等权限功能全部无法使用
- **错误信息**：无报错，但前端拿不到角色标识，权限控制失效
- **根因分析**：
  1. `UserMapper.findByUsername()` 使用 inner join（`user u, role r where u.role_id = r.id`）获取角色标签，这是**必要的权限约束**
  2. 如果用户没有绑定角色或角色不存在，该用户根本登不进来，更拿不到 roleLabel
  3. LoginVo 中的 roleLabel 为空 → 前端/后续接口无法识别用户角色 → 分配线索等功能无法判断权限
  4. ⚠️ 这不是代码 Bug，而是业务层的强制权限校验。内聚设计：用户必须有角色才能登录，否则一切权限相关功能都无法使用
- **注意点**：
  1. 新增用户时必须在 role 表中有对应角色且绑定 `role_id`，否则该用户无法登录
  2. 不能通过前端传入 roleLabel，必须从数据库查询，防止伪造角色
- **相关文件**：
  - `UserMapper.java`（第31-32行，findByUsername 的 inner join SQL）
  - `UserServiceImpl.java`（第97-99行，构建 LoginVo）

---

## Bug #10 — 2026-05-06 qk-parent

### ClueTrackRecord.remark 列不存在 — `@TableField(exist = false)` 未生效

- **问题描述**：伪线索操作时，INSERT INTO clue_track_record 报 `Unknown column 'remark'`
- **错误信息**：`java.sql.SQLSyntaxErrorException: Unknown column 'remark' in 'field list'`
- **SQL日志**：`INSERT INTO clue_track_record ( clue_id, user_id, type, create_time, remark ) VALUES ( ?, ?, ?, ?, ? )`
- **根因分析**：
  1. `ClueTrackRecord.java` 第72行已添加 `@TableField(exist = false) private String remark;`
  2. 字段 `assignName`（同样标注 `@TableField(exist = false)`）正常排除，`remark` 却被写入 SQL
  3. 推测为增量编译导致的 .class 文件未更新，或者 MP 的 TableInfo 缓存持有了旧映射
- **解决方法**：mvn clean compile 后重启项目。若持续出现则检查 target/classes/ 下 .class 文件的时间戳是否最新，或删除整个 target 目录重新编译
- **相关文件**：
  - `qk-entity/src/main/java/com/qkgj/entity/ClueTrackRecord.java`（第71-72行）
  - `qk-management/src/main/java/com/qkgj/service/impl/ClueServiceImpl.java`（第103-107行，faseClue 调用 insert）

---

## Bug #11 — 2026-05-06 qk-parent

### 线索池列表查询：URL 路径拼写错误 + `@PathVariable` 误用

- **问题描述**：`GET /clues/poll` 接口使用 `@PathVariable` 绑定 `ClueQueryDto`，Spring 无法解析，报500
- **错误信息**：Spring MVC 找不到路径变量 `clueQueryDto`，抛出 `MissingPathVariableException`（运行时500）
- **根因分析**：
  1. `@PathVariable` 只能绑定 URL 路径中的简单类型参数（如 `{id}`→`Integer`），不能绑定 DTO 对象
  2. `ClueQueryDto` 是多个查询参数的聚合，应该使用 `@ModelAttribute` 或不加注解让 Spring 自动绑定 query string
  3. URL 路径命名为 `"poll"`（投票），实际应为 `"pool"`（池）
- **解决方法**：
  1. `@PathVariable ClueQueryDto clueQueryDto` → 去掉 `@PathVariable`
  2. `@GetMapping("poll")` → `@GetMapping("pool")`
- **相关文件**：
  - `ClueController.java`（第105-106行）

---

## Bug #12 — 2026-05-06 qk-parent

### CurrentUserHoler 只取了没放值 — 永远返回 null

- **问题描述**：`ClueServiceImpl` 中多处调用 `CurrentUserHoler.get()` 获取当前用户 ID，但没有任何代码调用 `set()`
- **错误信息**：无报错，但 `get()` 返回 null，跟进记录/伪线索的 `userId` 写入 NULL
- **根因分析**：
  1. `CurrentUserHoler` 基于 ThreadLocal 实现，使用前必须由拦截器或过滤器调用 `set()` 注入当前用户ID
  2. `TokenInterceptor.preHandle()` 解析 JWT 后仅验证签名，未提取 `claims.get("id")` 并调用 `CurrentUserHoler.set()`
  3. `afterCompletion()` 也未调用 `remove()` 清理 ThreadLocal（潜在内存泄漏）
- **解决方法**：
  1. `TokenInterceptor` 解析 token 后：`Integer userId = (Integer) JwtUtils.parseToken(token).get("id"); CurrentUserHoler.set(userId);`
  2. 实现 `afterCompletion()` 方法：`CurrentUserHoler.remove();`
- **相关文件**：
  - `qk-common/src/main/java/com/qkgj/common/utils/CurrentUserHoler.java`
  - `qk-management/src/main/java/com/qkgj/interceptor/TokenInterceptor.java`
  - `qk-management/src/main/java/com/qkgj/service/impl/ClueServiceImpl.java`（第105、147行）

---

## Bug #13 — 2026-05-07 qk-parent

### Business 根据ID查询不回显跟进历史 — resultType 不支持集合映射

- **问题描述**：`GET /businesses/{id}` 返回的 Business 对象中 `trackRecords` 始终为 null
- **错误信息**：无报错，但前端展示跟进记录列表为空
- **根因分析**：
  1. 原 SQL 用 `resultType` 做自动映射，搭配 `btr.*` 查询跟进记录表
  2. `resultType` 只支持平铺映射，不认识 `List<BusinessTrackRecord>` 这种集合字段
  3. `btr.*` 的列名（`id`, `user_id`, `next_time`, `create_time`）跟 `b.*` 同名，后读的覆盖前面的，数据乱掉
  4. MyBatis 多行结果也只取第一行 → `trackRecords` 永远 null
- **解决方法**：
  1. 新增 `<resultMap id="BusinessWithTrackResultMap">`，显式声明 Business 全部字段映射
  2. 加入 `<collection property="trackRecords" ofType="BusinessTrackRecord">` 一对多集合映射
  3. `btr.id as btr_id` 等别名化，避免与 b.* 列名冲突
  4. `resultType` → `resultMap="BusinessWithTrackResultMap"`
- **相关文件**：
  - `BusinessMapper.xml`（第28-79行，新增 resultMap + 修改 select）

---

## Bug #14 — 2026-05-07 qk-parent

### 转客户功能完全失效（Controller 调用被注释 + 缺 insert）

- **问题描述**：调用 `PUT /businesses/toCustomer/{id}` 返回 success，但 Business 状态未更新、Customer 表未新增记录
- **根因分析**（共3个问题）：
  1. **Controller 第96行**：`businessService.businessByCustomer(id);` 被注释掉了 → 端点永远返回 success 但什么都不做
  2. **ServiceImpl 第111-128行**：`businessByCustomer()` 创建了 Customer 对象，设了 businessId/createTime/updateTime，但**全程没有调用 `customerMapper.insert(customer)`** → 数据没落库
  3. **`BeanUtils.copyProperties(businessById, customer)`**：Business 的 `id`（商机ID）被复制成 Customer 的 `id`（客户ID，自增主键）。如果后续加上 insert，同一商机转两次客户会报主键冲突
- **解决方法**：
  1. 取消 Controller 第96行的注释
  2. ServiceImpl 加 `customerMapper.insert(customer)`
  3. insert 前加 `customer.setId(null)` 让 MySQL 自增
- **相关文件**：
  - `BusinessController.java`（第96行）
  - `BusinessServicelImpl.java`（第111-128行）

---

## Bug #15 — 2026-05-07 qk-parent

### 修改客户接口 JSON 参数未解析（缺 @RequestBody）

- **问题描述**：`PUT /customers` 请求后，数据库客户记录无变化
- **根因分析**：
  1. `CustomerController.java` 第49行：`public Result updateCusromer(Customer customer)` — 参数前**没有 `@RequestBody`**
  2. PUT 请求传 `Content-Type: application/json`，不加 `@RequestBody` 时 Spring 不会解析 JSON body
  3. `customer` 对象所有字段为 null，`updateById(customer)` 只改了 `updateTime`，其他字段不变
  4. 同文件第40行：`getCusromerByid` 声明为 `private`，Spring 无法路由 → 根据ID查客户 404
- **解决方法**：
  1. Controller 第49行：`Customer customer` → `@RequestBody Customer customer`
  2. ServiceImpl 第64行：删掉无用的 `@RequestBody`（只在 Controller 层有效）
  3. Controller 第40行：`private` → `public`
- **相关文件**：
  - `CustomerController.java`（第40行、第49行）
  - `CustomerServiceImpl.java`（第64行）

---

## Bug #16 — 2026-05-07 qk-parent

### 公海池列表查询 private 方法导致404

- **问题描述**：`GET /businesses/pool` 返回 404
- **根因分析**：`BusinessController.java` 第74行 `listPool` 方法声明为 `private`，Spring MVC 无法反射调用 private 方法 → 路由无效 → 404
- **解决方法**：`private` → `public`
- **相关文件**：
  - `BusinessController.java`（第74行）

---

## Bug #17 — 2026-05-09 qk-parent

### LogAspect 中 result.toString() 对 void 方法报空指针

- **问题描述**：调用 `updateCourse` 等 void 方法时，返回 HTTP 500，控制台打印 `NullPointerException: Cannot invoke "Object.toString()" because "result" is null`
- **错误信息**：`java.lang.NullPointerException: Cannot invoke "Object.toString()" because "result" is null at com.qkgj.aop.LogAspect.aroundAdvice(LogAspect.java:44)`
- **根因分析**：
  - `@Around` 中 `pjp.proceed()` 执行 void 方法时返回 null
  - `.returnValue(result.toString())` 直接对 null 调 toString()
  - 同时 `@Builder` 使用不规范：`new OperateLog().builder()` 应为 `OperateLog.builder()`
  - Pointcut 中 `delet*` 少了个 `e`（应为 `delete*`）
- **解决方法**：
  1. `result.toString()` → `result != null ? result.toString() : "void"`
  2. `new OperateLog().builder()` → `OperateLog.builder()`
  3. `delet*` → `delete*`
- **相关文件**：
  - `LogAspect.java`（第24、38、44行）

## 相关笔记

- [[🖥 项目笔记/项目笔记总览|项目笔记总览]]

- [[📋 技术速查/MyBatis迁移到MP记录|MyBatis → MP 迁移记录]]
