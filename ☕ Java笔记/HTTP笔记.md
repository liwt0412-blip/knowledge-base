---
tags:
  - http
date: 2026-06-04
---
# HTTP协议

**概念**：Hyper Text Transfer Protocal超文本传输协议，规定了浏览器和服务器之间数据传输的规则。

**特点**：

1. 基于TCP协议：面向连接，安全。
2. 基于请求-响应模型的：一次请求对应一次响应。
3. HTTP协议是无状态的协议：对于事务处理没有记忆能力，每次请求-响应都是独立的。

**缺点**：多次请求间不能共享数据。
**优点**：速度快。



## 一、HTTP请求数据格式

### 1. 请求信息

**请求行**：请求数据第一行（请求方式、资源路径、协议）

**请求头**：第二行开始，格式：key:value

**请求体**：POST请求，存放请求参数

**请求方式-GET**：请求参数在请求行中，如/depts?name="部"&status=1。GET请求大小在浏览器中是有限制的。

**请求方式-POST**：请求参数在请求体中，POST请求大小是没有限制的。

| 请求头名称      | 说明                                                         |
| --------------- | ------------------------------------------------------------ |
| Host            | 请求的主机名                                                 |
| User-Agent      | 浏览器版本，例如 Chrome 浏览器的标识类似 Mozilla/5.0 ... Chrome/79，IE 浏览器的标识类似 Mozilla/5.0 (Windows NT ...) like Gecko |
| Accept          | 表示浏览器能接收的资源类型，如 text/*，image/*或者*/* 表示所有； |
| Accept-Language | 表示浏览器偏好的语言，服务器可以据此返回不同语言的网页；     |
| Accept-Encoding | 表示浏览器可以支持的压缩类型，例如 gzip，deflate 等。        |
| Content-Type    | 请求主体的数据类型。                                         |
| Content-Length  | 请求主体的大小（单位：字节）。                               |



## 2. 获取请求信息

Web服务器（Tomcat）对HTTP协议的请求数据进行解析，并进行了封装（HttpServletRequest），在调用Controller方法的时候传递给了该方法。这样，就使程序员不必直接对协议进行操作，让Web开发更加便捷。

```java
@RequestMapping("/request")
public String request(HttpServletRequest request){
    // 获取请求参数
	String name = request.getParameter("name");
    // 获取URI 和URL
	String uri = request.getRequestURI();
	String url = request.getRequestURL();
    // 获取User-Agent
	String userAgent = request.getHeader("User-Agent");
    //  获取请求的查询字符串
	String method = request.getQueryString();
    //  获取请求协议
    String protocol = request.getProtocal();
	return "request success";
}
```

更多API请参考文档笔记：[07.ServletRequest 常用方法](07.ServletRequest 常用方法.md)



## 三、HTTP响应数据格式

**响应行**：响应数据第一行（协议、状态码、描述）

**响应头**：第二行开始，格式  key:value

**响应体**：最后一部分，存放响应数据



### 1. 响应头含义

| 响应头           | 含义                                                       |
| ---------------- | ---------------------------------------------------------- |
| Content-Type     | 表示该响应内容的类型，例如text/html，application/json      |
| Content-Length   | 表示该响应内容的长度（字节数）                             |
| Content-Encoding | 表示该响应压缩算法，例如gzip                               |
| Cache-Control    | 指示客户端应如何缓存，例如max-age=300表示可以最多缓存300秒 |
| Set-Cookie       | 告诉浏览器为当前页面所在的域设置cookie                     |



## 2. 响应状态码

### **1xx：信息响应（Informational）**

表示请求已被接收，需要继续处理。

| 状态码 | 英文名称            | 中文描述                                             |
| ------ | ------------------- | ---------------------------------------------------- |
| 100    | Continue            | 客户端应继续其请求                                   |
| 101    | Switching Protocols | 服务器根据客户端的请求切换协议（如升级到 WebSocket） |
| 102    | Processing          | 服务器已收到并正在处理请求，但无响应可用（WebDAV）   |



### **2xx：成功（Success）**

表示请求已成功被服务器接收、理解并接受。

| 状态码  | 英文名称                      | 中文描述                                           |
| ------- | ----------------------------- | -------------------------------------------------- |
| **200** | **OK**                        | **请求成功，最常见的状态码**                       |
| 201     | Created                       | 请求成功并且服务器创建了新的资源                   |
| 202     | Accepted                      | 服务器已接受请求，但尚未处理完成                   |
| 203     | Non-Authoritative Information | 服务器已成功处理请求，但返回的信息可能来自另一来源 |
| 204     | No Content                    | 服务器成功处理了请求，但没有返回任何实体内容       |
| 205     | Reset Content                 | 服务器成功处理了请求，要求客户端重置文档视图       |
| 206     | Partial Content               | 服务器成功处理了部分 GET 请求（常用于断点续传）    |



### **3xx：重定向（Redirection）**

需要客户端采取进一步的操作才能完成请求。

| 状态码  | 英文名称              | 中文描述                                                     |
| ------- | --------------------- | ------------------------------------------------------------ |
| 300     | Multiple Choices      | 针对请求，服务器可执行多种操作                               |
| **301** | **Moved Permanently** | **请求的网页已永久移动到新位置（SEO会转移权重）**            |
| **302** | **Found**             | **临时移动。客户端应继续使用原有 URI（早期版本常误用于303）** |
| 303     | See Other             | 对应当前请求的响应可以在另一个 URI 上找到，客户端应使用 GET 方法获取 |
| 304     | Not Modified          | 资源未修改（直接使用本地缓存），不返回实体内容               |
| 307     | Temporary Redirect    | 临时重定向，且不允许改变请求方法（如 POST 必须保持为 POST）  |
| 308     | Permanent Redirect    | 永久重定向，且不允许改变请求方法                             |



### **4xx：客户端错误（Client Error）**

服务器无法处理请求，通常是因为客户端发送的报文有误。

| 状态码  | 英文名称                      | 中文描述                                             |
| ------- | ----------------------------- | ---------------------------------------------------- |
| **400** | **Bad Request**               | **语义有误，服务器无法理解（如参数格式错误）**       |
| **401** | **Unauthorized**              | **当前请求需要用户验证（未登录或Token失效）**        |
| 402     | Payment Required              | 保留状态码，预期用于电子现金或支付系统               |
| **403** | **Forbidden**                 | **服务器拒绝执行请求（已登录但无权限访问）**         |
| **404** | **Not Found**                 | **请求的资源在服务器上不存在**                       |
| 405     | Method Not Allowed            | 禁用请求中指定的方法（如对只读接口发起了 POST）      |
| 406     | Not Acceptable                | 服务器无法提供符合请求头要求的资源（如语言、格式）   |
| 407     | Proxy Authentication Required | 需要代理授权                                         |
| 408     | Request Timeout               | 客户端在服务器准备等待的时间内没有发出请求           |
| 409     | Conflict                      | 请求与服务器当前的状态发生冲突（如重复上传）         |
| 410     | Gone                          | 资源已永久不可用（比 404 更明确，通常用于 API 废弃） |
| 411     | Length Required               | 服务器不接受没有 Content-Length 的请求               |
| 412     | Precondition Failed           | 请求头中的先决条件评估为假                           |
| 413     | Payload Too Large             | 请求实体过大，超过服务器愿意处理的范围               |
| 414     | URI Too Long                  | 请求的 URI 过长，服务器无法解析                      |
| 415     | Unsupported Media Type        | 不支持的媒体类型（如上传了非预期的文件格式）         |
| 416     | Range Not Satisfiable         | 请求的范围无法满足（如请求的文件片段超出文件大小）   |
| 417     | Expectation Failed            | 服务器无法满足请求头中 Expect 字段的要求             |
| 418     | I'm a teapot                  | （愚人节彩蛋）我是一个茶壶，拒绝冲泡咖啡             |
| 429     | Too Many Requests             | 用户在给定的时间内发送了太多请求（触发限流）         |



### **5xx：服务器错误（Server Error）**

服务器在处理有效请求时发生了内部错误。

| 状态码  | 英文名称                   | 中文描述                                               |
| ------- | -------------------------- | ------------------------------------------------------ |
| **500** | **Internal Server Error**  | **服务器内部错误，通用错误消息**                       |
| 501     | Not Implemented            | 服务器不支持当前请求所需的功能                         |
| **502** | **Bad Gateway**            | **作为网关或代理的服务器，从上游服务器收到了无效响应** |
| **503** | **Service Unavailable**    | **服务器暂时处于超负载或停机维护状态**                 |
| 504     | Gateway Timeout            | 作为网关或代理的服务器，未及时从上游服务器收到请求     |
| 505     | HTTP Version Not Supported | 服务器不支持请求中所使用的 HTTP 协议版本               |

## 相关笔记

- [[☕ Java笔记/Java笔记总览|Java笔记总览]]


- [[MOC-Spring框架]]
