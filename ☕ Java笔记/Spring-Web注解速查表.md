---
tags: [Spring, SpringBoot, MyBatis, JUnit, 注解]
date: 2026-06-21
---

# Spring Web 阶段注解速查表

## 1. 声明 Bean — Spring IOC

| 注解 | 用途 |
|------|------|
| `@Component` | 不便于归类的 Bean 声明 |
| `@Controller` / `@RestController` | 控制层（`@RestController` = `@Controller` + `@ResponseBody`） |
| `@Service` | 服务（业务）层 |
| `@Repository` | 持久层 |
| `@Configuration` | 声明配置类 |
| `@Bean` | 方法上，声明第三方 Bean，默认 Bean 名 = 方法名 |

## 2. 依赖注入 — Spring DI

### 2.1 注入 Bean 对象

| 注解 | 用途 |
|------|------|
| `@Autowired` | Spring 提供，按类型装配 |
| `@Primary` | 同类型多 Bean 时，标注当前类为首选实现 |
| `@Autowired` + `@Qualifier` | 同类型多 Bean 时按名称指定 |
| `@Resource` | JDK 提供，默认按名称装配 |

### 2.2 注入配置项

| 注解 | 用途 | 注意 |
|------|------|------|
| `@Value("${...}")` | 读取单个配置项，打在属性上 | — |
| `@ConfigurationProperties(prefix="xxx")` | 读取多个配置项，打在类上 | ①类需提供 get/set 方法 ②也可在引用方用 `@EnableConfigurationProperties` 注册 |

## 3. 请求响应 — Spring MVC

### 3.1 请求方式 & 路径

| 注解 | 说明 |
|------|------|
| `@RequestMapping` | 通用请求映射 |
| `@GetMapping` | GET 请求 |
| `@PostMapping` | POST 请求 |
| `@PutMapping` | PUT 请求 |
| `@DeleteMapping` | DELETE 请求 |

### 3.2 接收请求参数

| 注解 | 用途 | 场景 |
|------|------|------|
| `@RequestParam` | 接收简单参数 `?id=1&name=xxx` | ①参数名与形参不一致时 ②设置默认值 ③接收数组 `?ids=1,2,3` → `List<Integer>` |
| `@RequestBody` | 接收 POST 请求的 JSON 参数 | — |
| `@PathVariable` | 接收路径变量 `/depts/1` | RESTful 风格 |

### 3.3 响应

| 注解 | 说明 |
|------|------|
| `@ResponseBody` | 指定响应数据以 JSON 格式返回（Spring MVC 序列化） |

## 4. 异常处理 — Spring MVC

| 注解 | 说明 |
|------|------|
| `@RestControllerAdvice` | `@ControllerAdvice` + `@ResponseBody`，全局异常处理，返回 JSON |
| `@ExceptionHandler` | 声明异常处理方法，形参为能处理的异常类型 |

## 5. AOP 相关 — Spring

| 注解 | 说明 |
|------|------|
| `@Aspect` | 声明切面类 |
| `@Pointcut` | 声明切入点表达式 |
| `@Before` | 前置通知：目标方法之前执行 |
| `@After` | 后置通知：目标方法之后执行，**无论是否抛异常总是执行** |
| `@Around` | 环绕通知：前后都执行，用 `joinPoint.proceed()` 放行 |
| `@AfterReturning` | 返回后通知：在 `@After` 之前执行，**抛异常就不执行** |
| `@AfterThrowing` | 异常通知：抛异常后执行，与 `@AfterReturning` 互斥 |

## 6. 事务管理 — Spring

| 注解 | 说明 |
|------|------|
| `@Transactional` | 可标注在类/方法/接口上 |
| `rollbackFor` | 声明回滚的异常类型 |
| `propagation` | 声明事务传播行为（REQUIRED / REQUIRES_NEW 等） |

## 7. MyBatis 相关

| 注解 | 说明 |
|------|------|
| `@Mapper` | 标注持久层接口，运行时产生动态代理并交给 Spring 容器 |
| `@Insert` | 插入 |
| `@Insert` + `@Options(useGeneratedKeys=true, keyProperty="id")` | 插入 + 主键回填 |
| `@Delete` | 删除 |
| `@Update` | 更新 |
| `@Select` | 查询 |

## 8. JUnit 单元测试 — Spring 支持

| 注解 | 说明 |
|------|------|
| `@SpringBootTest` | 在 Spring 环境下执行测试（会启动项目） |
| `@Test` | 声明单元测试方法 |
| `@BeforeEach` | 每个测试方法前执行一次 |
| `@AfterEach` | 每个测试方法后执行一次 |
| `@BeforeAll` | 所有测试方法前执行**一次** |
| `@AfterAll` | 所有测试方法后执行**一次** |
| `@ParameterizedTest` + `@ValueSource` | 多参数单元测试 |
| `@DisplayName` | 给测试起名字 |

## 9. 其他注解

### 9.1 Filter 定义和配置

| 注解 | 说明 |
|------|------|
| `@WebFilter` | 声明过滤器类，可指定过滤范围（路径） |
| `@ServletComponentScan` | 标注在启动类上，开启 Web 三大组件扫描（Servlet / Filter / Listener） |

### 9.2 Spring Task 定时任务

| 注解 | 说明 |
|------|------|
| `@Scheduled` | 标注定时方法，用 `cron` 属性指定时间（秒 分 时 日 月 周） |
| `@EnableScheduling` | 标注在启动类上，开启定时任务 |

### 9.3 自动配置原理

`@SpringBootApplication` 包含三个核心注解：

```
@SpringBootApplication
├── @SpringBootConfiguration       → @Configuration
├── @ComponentScan                 → 组件扫描
└── @EnableAutoConfiguration       → 自动配置
    └── @Import({AutoConfigurationImportSelector.class})
        └── 扫描 META-INF/spring/xxx.AutoConfiguration.imports（Spring Boot 3.x）
            或 META-INF/spring.factories（Spring Boot 2.7 以下）
            └── 配置文件中声明大量自动配置类（XxxAutoConfiguration）
                ├── @Configuration              → 声明配置类
                ├── @Bean                       → 方法返回值交给 Spring 容器
                └── @ConditionalOnXxx           → 条件装配
                    ├── @ConditionalOnClass       → 必须有某类的字节码（导了包）
                    ├── @ConditionalOnBean        → 容器中必须有某个 Bean
                    └── @ConditionalOnProperty    → 配置文件中必须有某个配置项
```

## 相关笔记

- [[../MOC-Spring框架|🏗️ Spring框架 MOC]]
- [[../MOC-Java基础|☕ Java基础 MOC]]
- [[Java笔记总览|Java笔记总览]]
