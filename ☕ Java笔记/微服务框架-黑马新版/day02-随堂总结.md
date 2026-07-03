---
tags: [微服务, OpenFeign, Gateway, 课堂总结]
date: 2026-07-01
sources:
  - 东哥随堂: 微服务阶段/day2-微服务02/课堂总结
---

# 微服务 Day2 随堂总结

## 1. OpenFeign

### 1.1 作用

声明式 HTTP Java 客户端，能够帮助我们更优雅便捷地发起 HTTP 请求。

### 1.2 快速入门

1. **引入依赖**：OpenFeign、LoadBalancer
2. **开启 Feign**：启动类标注 `@EnableFeignClients`
3. **编写 Feign 客户端（接口）**：
   - 接口上标注 `@FeignClient("要调用的微服务名称")`
   - 要调用的方法通过 SpringMVC 的风格声明（小技巧：可以直接从提供者方 Controller 拷贝）
4. **注入使用** Feign 客户端
5. **原理**（为什么接口能发请求）：动态代理（基于 JDK）

### 1.3 连接池配置

- OpenFeign 底层用的连接是基于 `HttpUrlConnection`，不支持连接池，效率不高
- **优化**：可以使用 Apache HttpClient、OkHttpClient（课程使用 OkHttp）
  - 引入依赖：`feign-okhttp`
  - 加入配置：`feign.okhttp.enable: true`

### 1.4 最佳实践

抽取 `feign-api` 模块，将跟 Feign 相关的一切内容放到此模块：

1. **依赖**：注册中心、OpenFeign、LoadBalancer、feign-okhttp
2. **Feign 客户端**（很多接口）
3. **业务 DTO**
4. **`@EnableFeignClients` 挪过来**（基于自动装配）：
   - 在 api 模块创建配置类 `ApiAutoConfiguration`，打上 `@EnableFeignClients`
   - 在 `resources/META-INF/spring/xx.imports` 中配置 `ApiAutoConfiguration` 全限类名

> **拓展 — SpringBoot 自动装配文件位置演变：**
>
> | SpringBoot 版本 | 配置文件 |
> |---|---|
> | ≤ 2.7.0 | `META-INF/spring.factories` |
> | 2.7.0 ~ 3.0 | 两者都支持 |
> | ≥ 3.0 | `META-INF/spring/xx.imports` |

### 1.5 日志配置

- **日志级别**：NONE、BASIC、HEADERS、FULL
- **使用步骤**：
  1. 创建一个普通类（`DefaultFeignConfig`），通过 `@Bean` 声明 `Logger.Level` 日志级别
  2. 配置：
     - **全局配置**：将该类配置到 `@EnableFeignClients` 的 `defaultConfiguration` 属性中
     - **局部配置**：将该类配置到 `@FeignClient` 的 `configuration` 属性中

## 2. 网关（Spring Cloud Gateway）

### 2.1 作用

微服务项目的网络关口，负责请求的**动态路由**以及**过滤拦截**（一般是鉴权）。

### 2.2 网关搭建

1. 创建新模块
2. 引入依赖：
   - 网关：`spring-cloud-starter-gateway`
   - 注册中心：`spring-cloud-starter-alibaba-nacos-discovery`
   - 负载均衡：`spring-cloud-starter-loadbalancer`
3. 编写启动类
4. 编写路由

### 2.3 动态路由

**配置示例：**

```yaml
routes:
  - id: item-service          # 路由规则 id，自定义，唯一
    uri: lb://item-service    # 路由目标微服务，lb 代表负载均衡
    predicates:               # 路由断言，判断请求是否符合规则
      - Path=/items/**        # 以请求路径做判断，以 /items 开头则符合
```

**断言工厂：**

指的就是 `predicates` 属性：根据请求的**特征**判断该请求是否符合当前路由。官网共 12 种（常见的：Before、After、Path…）。

### 2.4 过滤拦截（一般就是鉴权）

#### GatewayFilter（路由过滤器）

- **官网自带**（33 种）：`AddRequestHeader`…
- **自定义**：
  1. 编写一个类（如 `PrintAnyGatewayFilterFactory`），继承 `AbstractGatewayFilterFactory`，重写 `apply` 方法
  2. 配置文件中配置该过滤器：在路由的 `filter` 属性或 `default-filter` 中配置前缀即可：`- PrintAny`
  3. 如需自定义带参数的过滤器，额外步骤：
     - 在过滤器内部定义一个静态内部配置类，用于接收配置文件的数据
     - 重写 `shortcutFieldOrder` 方法，声明过滤器参数对应关系
     - 编写无参构造，委托其父类读取配置文件
- 通过 `OrderedGatewayFilterFactory` 指定顺序

#### GlobalFilter（全局过滤器）

1. 实现 `GlobalFilter` 接口
2. 定义顺序：
   - 实现 `Ordered` 接口，重写 `getOrder` 方法，返回值越小优先级越高
   - 过滤器类上添加 `@Order` 注解：`@Order(1)`

#### 过滤器执行流程原理

1. 请求到达网关内部的 `DispatcherHandler`
2. `DispatcherHandler` 调用 `HandlerMapping`（默认实现 `RoutePredicateHandlerMapping`），根据请求特征找到对应的路由（路由断言），并将路由存储到上下文，然后将请求交给 `WebHandler` 处理（默认实现 `FilterWebHandler`）
3. `WebHandler` 将该路由上的过滤器放入集合并排序，形成过滤器链，依次执行 pre 逻辑（责任链模式）：
   - 过滤器跟 Web Filter 一样有 pre 前置和 post 后置阶段
   - 最后一个过滤器叫 `NettyRoutingFilter`，负责请求的最终路由动作，路由到某个微服务
4. 请求到达微服务，执行逻辑，而后依次倒序执行 filter post 逻辑

### 2.5 实现黑马商城的登录鉴权

#### 网关 — 全局过滤器（负责登录鉴权）

1. 获取请求 URL
2. 判断是否需要放行
3. 获取请求头 token
4. 校验解析 token，如果报错（不合法、过期、为空），返回 401 没有权限
5. 将解析出的 userId 放入请求头（`user-info`）

#### 微服务（common 工程）— MVC 拦截器（负责获取用户信息向后传递）

**定义步骤：**
1. 编写 `preHandle`：存 userId
2. 编写 `afterCompletion`：清理 ThreadLocal 中的 userId
3. 编写配置类，实现 `SpringMvcConfigurer`，重写 `addInterceptor` 方法（`MvcConfig`）
4. 加载方式：
   - **方式一**：通过自动装配原理，将 `MvcConfig` 全限类名配置到 `hm-common/resources/META-INF/spring.factories`
   - **方式二**：通过 `@Import` 方式：
     - 定义注解 `@EnableUserInfoInterceptor`，打上 `@Import(MvcConfig.class)`
     - 需要该拦截器的微服务启动类上标注 `@EnableUserInfoInterceptor`
5. `MvcConfig` 上要通过 `@ConditionalOnClass(DispatcherServlet.class)` 条件装配，防止网关依赖该模块报错

**拦截器逻辑：**
1. 获取请求头 `user-info` 中的 userId
2. 存入 ThreadLocal

#### feign-api 模块 — Feign 拦截器（负责微服务之间用户信息的传递）

**原理**：在 Feign 发起远程调用之前拦截请求，添加自定义逻辑（如：从 ThreadLocal 取出 userId 存入请求头）

**步骤：**
1. 创建拦截器类，实现 `RequestInterceptor` 接口，实现 `apply` 方法
2. 在 Feign 的默认配置类（`DefaultFeignConfig`）中，`@Bean` 声明拦截器类

**逻辑：**
1. 从 ThreadLocal 获取 userId
2. 存入请求头中

---

### 拓展：Hikari 连接池项目启动初始化

```java
@RequiredArgsConstructor
@ConditionalOnClass(DispatcherServlet.class)
@Configuration
public class HikariInitConfig implements CommandLineRunner {
    private final DataSource dataSource;

    @Override
    public void run(String... args) throws Exception {
        // try-with-resources 自动关闭资源
        try (Connection connection = dataSource.getConnection()) {
            System.out.println("✅ HikariCP 初始化成功!");
        }
        // Try-with-Resources 语法（JDK 7+ 特性）：
        // 要求资源对象（如 Connection）实现 AutoCloseable 接口。
        // 编译器会自动插入 finally 块并调用 close()，确保资源释放。
        // 连接池行为：
        // dataSource.getConnection() 从 HikariCP 池中借出连接。
        // connection.close() 实际将连接标记为空闲，归还给连接池。
    }
}
```

| 写法 | 代码示例 | 缺点 |
|---|---|---|
| Try-with-Resources | `try (Connection c = dataSource.getConnection()) {}` | 无 |
| 传统 finally 关闭 | `try { Connection c = ...; } finally { c.close(); }` | 冗长，易漏写 close() |

## 相关笔记

- [[day02-微服务02|day02 正课笔记]]
- [[微服务框架-黑马新版|课程总索引]]
- [[MOC-Spring框架]]
