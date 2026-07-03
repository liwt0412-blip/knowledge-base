---
tags: [Java, SpringMVC, Spring, 面试]
title: SpringMVC执行流程
description: SpringMVC 核心执行流程——DispatcherServlet、HandlerMapping、HandlerAdapter、ViewResolver 各组件职责与协作过程
date: 2026-07-02
sources:
  - Agent讲解
confidence: high
---

# SpringMVC 执行流程

## 要解决的问题

浏览器发一个 HTTP 请求过来，后端怎么找到对应的处理方法、把参数传进去、再把结果渲染成页面返回？

如果每个 Servlet 都自己解析 URL、自己拿参数、自己写 HTML，代码又臭又长。SpringMVC 用一个**中央调度器**（DispatcherServlet）统一接管所有请求，把"找谁处理""参数怎么绑""结果怎么渲染"这些脏活全抽出来，开发者只写业务方法。

## 核心执行流程（7 步）

```
请求 → DispatcherServlet → HandlerMapping → HandlerAdapter → Controller → ModelAndView → ViewResolver → 响应
```

| 步骤 | 组件 | 做什么 |
|------|------|--------|
| 1 | 客户端 | 发 HTTP 请求到 `DispatcherServlet` |
| 2 | HandlerMapping | 根据请求 URL 找到对应的 Controller 方法（Handler） |
| 3 | HandlerAdapter | 适配调用 Controller 方法（支持多种 Handler 类型） |
| 4 | Controller | 执行业务逻辑，返回 ModelAndView |
| 5 | ViewResolver | 把逻辑视图名（如 `"index"`）解析成物理视图路径（如 `/WEB-INF/views/index.jsp`） |
| 6 | View 渲染 | 用 Model 数据填充视图模板，生成 HTML |
| 7 | 响应 | DispatcherServlet 把最终的 HTML 返回给客户端 |

## 每一步为什么存在

### DispatcherServlet（前端控制器）

所有请求的统一入口。在 `web.xml` 里配 `url-pattern = /`，拦截一切。

**为什么需要它**：如果没有中央调度器，每个请求都要自己解析 URL、自己找处理类 —— 代码重复且耦合。

### HandlerMapping（处理器映射器）

回答一个问题：**这个 URL 归谁管？**

维护一张映射表，把 `/user/login` → `LoginController.login()` 存起来。你的 `@RequestMapping`、`@GetMapping` 注解就是往这张表里注册。

### HandlerAdapter（处理器适配器）

看起来像多余的一层 —— 为什么不直接调 Controller？

因为 SpringMVC **不假设 Handler 一定是 `@Controller`**。可以是 `HttpRequestHandler`、可以是 `Servlet`。HandlerAdapter 用**适配器模式**统一调用方式：不同 Handler 包装成统一接口，DispatcherServlet 不用关心底层怎么调的。

### Controller（处理器）

你的业务代码。接收参数、调 Service、返回结果。

参数绑定在这里自动完成：Spring 把请求参数名和方法参数名对上，自动注入。前端传 `?name=Tom`，后端方法写 `String name`，自动绑定。

### ModelAndView → ViewResolver → View

返回页面分成两步：

1. Controller 返回**逻辑视图名**（`"user-list"`），不和具体文件路径耦合
2. ViewResolver 按**前缀+后缀**拼出物理路径（`/WEB-INF/views/user-list.jsp`）

**这层的价值**：换模板引擎（JSP → Thymeleaf）只改 ViewResolver 配置，Controller 代码一行不动。

## 辅助组件

### 拦截器（HandlerInterceptor）

在 Handler 执行前后插一道。类似 Servlet Filter，但能拿到 Handler 的具体信息（哪个类、哪个方法、什么注解）。

三个切入点：
- `preHandle`：Controller 方法执行前（可以做权限校验）
- `postHandle`：Controller 执行后、视图渲染前
- `afterCompletion`：视图渲染完成后（清理资源）

### 异常处理器（HandlerExceptionResolver）

统一捕获 Controller 抛的异常，跳错误页或返 JSON。你的 `@ControllerAdvice` + `@ExceptionHandler` 底层就是这个机制。

## 面试嘴替版

> 所有请求先到 DispatcherServlet——它是一个中央调度器。DispatcherServlet 调 HandlerMapping，根据 URL 找到对应的 Controller 方法。然后通过 HandlerAdapter 适配调用 Controller，执行业务逻辑。Controller 返回 ModelAndView——Model 是数据，View 是逻辑视图名。DispatcherServlet 把 View 交给 ViewResolver，解析成真正的视图路径，渲染 HTML，最后把响应返回给客户端。
>
> 这个流程里，HandlerMapping 解决"谁处理"，HandlerAdapter 解决"怎么调"，ViewResolver 解决"怎么渲染"。三层解耦，换任何一环都不影响其他。

## 相关笔记

- [[MOC-Spring框架]]
- [[☕ Java笔记/Java笔记总览|Java笔记总览]]
- [[☕ Java笔记/接参笔记|接参笔记]]（请求参数绑定）
- [[☕ Java笔记/全局异常处理器|全局异常处理器]]
