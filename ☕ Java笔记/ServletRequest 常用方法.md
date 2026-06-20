---
tags:
  - servlet
date: 2026-06-04
---
### 一、ServletRequest 常用方法（请求对象）

#### 1.获取请求参数

```java
// 获取单个请求参数（key=value）
String getParameter(String name)

// 获取同key多个值（复选框、下拉多选）
String[] getParameterValues(String name)

// 获取所有参数名
Enumeration<String> getParameterNames()

// 获取所有参数键值对
Map<String,String[]> getParameterMap()
```

2. #### 获取请求头信息

```java
// 根据头名称获取头值
String getHeader(String name)

// 获取所有请求头名称
Enumeration<String> getHeaderNames()
```

3. #### 获取客户端 / 服务器信息

```java
// 获取客户端IP
String getRemoteAddr()

// 获取请求协议 http/https
String getProtocol()

// 获取请求方式 GET/POST
String getMethod()
```

4. #### 域对象（请求域，一次请求内共享）

```java
// 存数据
void setAttribute(String name, Object o)

// 取数据
Object getAttribute(String name)

// 删数据
void removeAttribute(String name)
    
// 请求转发到指定路径
RequestDispatcher getRequestDispatcher(String path)
    
// 设置请求体编码（解决POST乱码）
void setCharacterEncoding(String env)
```



### 二、ServletResponse 常用方法（响应对象）



```java
// 字符输出流（输出文本、HTML、JSON）
PrintWriter getWriter()

// 字节输出流（下载文件、图片）
ServletOutputStream getOutputStream()
    
// 设置响应编码
void setCharacterEncoding(String charset)

// 设置响应类型 + 编码（最常用）
void setContentType(String type)
// 示例：response.setContentType("text/html;charset=UTF-8");
// 示例：JSON：application/json;charset=UTF-8
    
void setStatus(int sc)
// 常用：200成功、302重定向、404找不到、500服务器错误
    
void setHeader(String name, String value)
// 常用：设置缓存、定时跳转
    
// 重定向到另一个资源
void sendRedirect(String location)
    
// 直接返回404/500等错误页面
void sendError(int sc)
void sendError(int sc, String msg)
    
```



# 超精简记忆口诀

### ServletRequest（收数据）

拿参数：`getParameter`、`getParameterValues`

拿头：`getHeader`

存取值：`setAttribute / getAttribute`

转转发：`getRequestDispatcher`

设编码：`setCharacterEncoding`

### ServletResponse（发数据）

输出流：`getWriter` 文本、`getOutputStream` 文件

设类型：`setContentType`

重定向：`sendRedirect`

设状态：`setStatus`、`sendError`

## 相关笔记

- [[☕ Java笔记/Java笔记总览|Java笔记总览]]


- [[MOC-Spring框架]]
