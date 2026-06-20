---
tags: [AI, SpringAI]
date: 2026-06-11
---
# part3-SpringAI高级

> 由飞书 Word 文档转换，图片已本地化

**part3-SpringAI高级**  
**1. SpringAI-Alibaba应用学习**  

之前我们对接阿里云百炼平台一直都是用SpringAI中的OpenAI模块，不过由于阿里云百炼与OpenAI之间并不是完全兼容，所以还存在许多问题。

为了更好的与阿里云百炼平台对接，同时又能兼容SpringAI，阿里巴巴官方就在SpringAI的基础上推出了自己的集成API，Spring AI Alibaba.
**[该类型的内容暂不支持下载]**  
**1.1 快速入门(对话机器人)**  
接下来我们通过一个快速入门案例，学习如何对接Spring AI Alibaba.

**1.1.1 创建工程**  
首先，我们创建一个SpringBoot工程：

![Image](images/part3/image1.png)

**点击next，选择依赖：**  
只勾选一个Spring Web依赖坐标即可

**1.1.2 引入依赖坐标**  
引入alibaba的依赖坐标
**1.1.3 配置文件**  
接下来，理论上说，我们同样需要配置模型的关键信息：
- API_KEY
- BASE_URL
- 模型名称和参数等
参考官网：
**[该类型的内容暂不支持下载]**  
**不过，由于Spring AI Alibaba默认已经设定好了url路径，所以BASE_URL就可以省略了。**  

**我们修改application.yml配置， 内容如下：**  

**1.1.4 配置ChatClient**  
接下来，同样是配置ChatClient，我们在com.itheima.ai.config包下新建一个CommonConfiguration类，代码如下：

**1.1.5 对话接口**  
接下来，我们来定义对话接口。
在com.itheima.ai.controller包下新建一个ChatController类，代码如下：
**1.1.6 测试**  
启动项目，打开浏览器，访问：http://localhost:8080/ai/chat

![Image](images/part3/image2.png)

**1.2 SpringAI-Alibaba插件 **  
Spring AI Alibaba官方提供了很多的插件以及示例，这些插件可以拿来直接使用，简化了我们的开发。

![Image](images/part3/image3.png)

**1.2.1 案例 头条新闻**  
需求：我们想通过设置prompt提示词，然后问大模型一个问题“获取今日头条信息”，看看大模型是如何回答的？

![Image](images/part3/image4.png)

**1.2.1.1 介绍**  
Alibaba提供了获取今日头条新闻数据的插件，可以直接集成到项目中使用。

![Image](images/part3/image5.png)

今日头条gitee源码地址：
**[该类型的内容暂不支持下载]**  
今日头条github源码地址：
**[该类型的内容暂不支持下载]**  
**1.2.1.2 使用**  
**第一步，导入今日头条新闻的依赖坐标**  
**第二步，在application.yml中开启头条工具**  
**第三步，注册（调用）工具**  
**第一种方式全局配置**  
**第四步，对话接口**  


![Image](images/part3/image6.png)

**第五步，测试**  

![Image](images/part3/image7.png)

**1.2.2 练习：新浪新闻**  

![Image](images/part3/image8.png)


![Image](images/part3/image9.png)

**2. SpringAI-MCP应用**  
**2.1 什么是MCP**  
**2024年11月，Anthropic 公司（也就是发布 Claude 大模型的那家公司）正式推出了 Model Context Protocol，简称 MCP 协议，叫作模型上下文协议，是一种标准化协议。**  
**如果要打个比方，MCP 就像大模型世界的 Type-C 扩展坞 ——它让各种软件、工具、服务模块，都能像“插头”一样，统一地接入到大语言模型上，被模型灵活调用。**  
**简单来说，MCP 是连接「大模型（客户端）」与「外部工具（服务端）」的标准通信协议。它定义了一种通用格式，让模型可以像调用函数一样，调度搜索引擎、数据库、计算器、代码执行器，甚至其他模型或 API 服务。**  

![Image](images/part3/image10.png)

**MCP 的出现，统一了大模型调用工具的方法，从根本上解决了大模型在实际应用中的“调用混乱”和“接入难”问题。**  
**它为【大模型】与【外部工具 / 数据接口】之间的无缝集成，提供了一套标准化的协议和运行机制。开发者无需再设计复杂的提示词（Prompt），也不必手动绑定每一个接口逻辑，只需按照 MCP 规范对接，大模型就能自动识别、理解并调用外部工具。**  
**这大大降低了大模型调用海量软件、接口、数据库、服务等的门槛，让 AI 不再是“只能回答问题的助手”，而是真正的“自动调度工具的超级代理”。**  

![Image](images/part3/image11.png)



![Image](images/part3/image12.png)

在上图中，上方代表MCP客户端软件，比如Cusor、Claude Desktop，下方代表MCP服务端，比如海量的软件和API接口。MCP的协议增强了AI大模型的能力
看上去，似乎和Tool Calling差不多，也是增强大模型的能力，不同的是，MCP是标准，更通用。
再举两个场景来说明：
- 在SpringAI中编写的Tools，可以放到Python中使用吗？，显然是不可以的，要想让Python中使用，就得使用Python语言重写一次Tool，才能使用，这就是不通用性的体现。
- 在企业项目开发中，我们采用了Spring AI框架来构建智能体。这些智能体通常需要执行一系列通用功能，如天气查询、商品检索及下单等。基于以往的做法，每当开发新项目时，都需要重新编写实现这些功能的工具（Tool），这显然不利于代码复用。为解决这一问题，可以采用MCP标准进行服务器端开发，并将这些常用工具封装成服务接口。这样一来，其他的智能体只需通过调用该服务即可轻松访问所需功能，从而极大地提高了代码的复用性和开发效率。
**2.2 SpringAI-MCP**  
**2.2.1 技术架构**  
SpringAI对MCP做了支持，简化了Java项目中的MCP开发。参考文档：
**[该类型的内容暂不支持下载]**  
Spring AI MCP采用模块化架构，有SSE和Stdio两种方式。

**MCP Client客户端**  

![Image](images/part3/image13.png)

MCP 客户端是模型上下文协议 (MCP) 架构中的关键组件，负责建立和管理与 MCP 服务器的连接。它实现了协议的客户端功能，处理以下操作：
- 协议版本协商以确保与服务器的兼容性
- 能力协商以确定可用功能
- 消息传输和 JSON-RPC 通信
- 工具发现和执行
- 资源访问和管理
- 提示系统交互
- 可选功能：
- 根部管理
- 采样支持
- 同步和异步操作
- 传输选项：
- 基于 Stdio 的传输，用于基于进程的通信
- 基于 Java HttpClient 的 SSE 客户端传输（同步）
- 用于反应式 HTTP 流的 WebFlux SSE 客户端传输（异步）
**MCP Server服务端**  

![Image](images/part3/image14.png)

MCP 服务器是模型上下文协议 (MCP) 架构中的基础组件，为客户端提供工具、资源和功能。它实现了协议的服务器端，负责：
- 服务器端协议操作实现
- 工具曝光和发现
- 基于 URI 访问的资源管理
- 及时提供和处理模板
- 与客户进行能力谈判
- 结构化日志记录和通知
- 并发客户端连接管理
- 同步和异步 API 支持
- 传输选项：
- 基于 Stdio 的传输，用于基于进程的通信
- 基于 Servlet 的 SSE 服务器传输
- 用于反应式 HTTP 流的 WebFlux SSE 服务器传输
- 用于基于 servlet 的 HTTP 流的 WebMVC SSE 服务器传输

**2.2.2 MCP Client入门实战**  
**2.2.2.1 功能需求**  
接下来我们通过两个案例的方式来实现MCP Client快速入门
我们需要给AI大模型增强2个功能如下：
- 打开浏览器，浏览网页，并总结网页中的内容
- 提问：打开网站：https://www.itcast.cn/，总结下这个网站的内容
- 输入一个IP地址，让大模型解析出这个IP地址的所在地
- 提问：查询IP所在地：223.11.151.28
显然，大模型如果不做增强的话，是做不到的，下面我们就基于MCP进行实现。

**2.2.2.2 基础工程准备**  
使用git拉取代码，基础工程地址：https://gitee.com/Loong-li/spring-ai-mcp-demo.git

![Image](images/part3/image15.png)

拉取完成后，启动服务，已经实现了基本的大模型对话功能，进行测试。（确保系统环境变量中存在OPENAI_API_KEY信息）

![Image](images/part3/image16.png)


**2.2.2.3 实战1：控制浏览器**  
需求如下：
向大模型提问：打开网站：https://www.itcast.cn/，总结下这个网站的内容，就会进行相对应的操作

![Image](images/part3/image17.png)

下面我们来增强下大模型。
**第一步，检查电脑上是否安装好node,npm,npx等指令，并能够执行npx命令，如果不能执行，则重新安装nodejs**  

![Image](images/part3/image18.png)


**第二步，先在本机通过npm安装@executeautomation/playwright-mcp-server，如下：**  

![Image](images/part3/image19.png)




**第三步，在spring-ai-mcp-client模块中增加依赖：**  

**第四步，增加mcp-server.json文件：**  

![Image](images/part3/image20.png)

添加以下内容


**找对应的mcp-server服务器，可以参考这个网站1:**  
**[该类型的内容暂不支持下载]**  

![Image](images/part3/image21.png)

**这个网站找不到的话，那么可以参考下面这个网站2：**  
**[该类型的内容暂不支持下载]**  

![Image](images/part3/image22.png)


**第五步，在application.yml中配置mcp客户端信息**  
**第六步，在CommConfig中配置Tools**  
**第七步，重启服务，进行测试：**  
注意：idea一定要用管理员方式打开，有可能启动会报错

![Image](images/part3/image23.png)

apifox进行测试

![Image](images/part3/image24.png)

自动打开浏览器，并访问 https://www.itcast.cn/这个网站

![Image](images/part3/image25.png)

**原理分析：**  
通过上面的实战，已经可以看到大模型可以控制浏览器了，是怎么做到的呢？
实际上，底层的实现也是基于Tool Calling实现的，由于配置了mcpServers，就拥有了好多的工具，注册到SpringAI中。

![Image](images/part3/image26.png)

而这些工具的开发，并不是我们自己做的，也不是用java开发的，是别人开发好的，遵循了MCP协议，所以就可以集成到SpringAI中使用了，而这工具就是用来控制浏览器的，所以就实现了上面的效果。

**2.2.2.4 实战2：查询IP地址所在地**  
需求如下：
向大模型提问：查询ip所在地：223.11.151.238，就可以查询到ip地址的所在地。要想实现这个功能，可以借助与高德地图服务来实现，也不需要我们自己来对接，直接基于写好的MCP服务即可。
**第一步，查找MCP服务**  
https://mcp.so/zh/

![Image](images/part3/image27.png)

用法：

![Image](images/part3/image28.png)

**第二步，通过npm安装高德地图mcp服务**  
注意：采用管理员方式打开cmd窗口

![Image](images/part3/image29.png)

**第三步，增加mcp-server.json文件信息**  

**第四步，测试**  
重启服务，进行测试：

![Image](images/part3/image33.png)


![Image](images/part3/image34.png)

**2.2.2.5 练习作业：MCP操作Redis**  
按照上述的操作方法，为大模型增加Redis的操作工具。参考：
**[该类型的内容暂不支持下载]**  

![Image](images/part3/image35.png)

**2.2.3 MCP Server入门实战**  
**2.2.3.1 功能需求**  
前面我们都是使用的已经写好的MCP Server，实际上，也可以自己来实现的。
**接下来，我们将写一个自己的天气查询服务，将他封装成MCP Server，这样需要的天气查询服务的大模型，就可以直接集成了。**  

![Image](images/part3/image36.png)

**2.2.3.2 mcp-server工程准备**  

![Image](images/part3/image37.png)

**2.2.3.2.1 创建spring-ai-mcp-server**  

![Image](images/part3/image38.png)

**2.2.3.2.2 导入依赖坐标**  
**2.2.3.2.3 application.yml**  
**2.2.3.2.4 启动类**  
**2.2.3.2.5 返回值对象WeatherDTO **  
**2.2.3.2.6 创建工具Tool**  

**2.2.3.2.7 MCPServer配置**  
把定义好的工具对外暴露
**2.2.3.2.8 启动测试**  
浏览器访问地址：http://localhost:8081/sse

![Image](images/part3/image39.png)

说明，MCPServer已经启动成功。

**2.2.3.3 在MCPClient服务中集成MCPServer服务**  
只需要在MCPClient中指定服务地址即可。
application.yml
启动服务，打断点可以看到，已经有天气的工具了：

![Image](images/part3/image40.png)

**2.2.3.4 整体功能测试**  

![Image](images/part3/image41.png)

**2.2.3.5 优化**  
**上面虽然可以通过接口查询天气数据了，但是接口中还是需要传递城市id,这样很不方便，我们希望，用户输入城市名称，就可以查询天气数据，所以，这里就需要从 城市名 --->城市id 转化的需求**  
怎么做呢？也是可以交给大模型做的。
首先，我们需要知道城市名与城市id的对应列表，这里我已经整理出来了（通过AI整理的，只保留了省会城市），如下：


![Image](images/part3/image42.png)

把上述数据，加入到系统提示词中，大模型就能够找到城市对应的cityId，进行查询了：
修改commonfig配置文件中的提示词
重启，测试：

![Image](images/part3/image43.png)


![Image](images/part3/image44.png)

**可以看到，大模型已经正常识别城市了，并且完成 城市 → 城市id 的转化。**  
