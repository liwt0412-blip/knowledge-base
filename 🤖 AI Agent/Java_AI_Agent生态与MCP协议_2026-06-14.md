# Java AI Agent 生态与 MCP 协议全景

> 整理时间：2026-06-14  
> 数据来源：GitHub API 实时数据

---

## 一、Java AI Agent 框架格局（2026-06）

### 核心框架对比

| 框架 | ⭐ | 背后势力 | 定位 | 适合场景 |
|------|-----|---------|------|---------|
| **LangChain4j** | 12.3K | 社区 | Java 版 LangChain，生态最全 | 想快速接入多种 LLM |
| **Spring AI Alibaba** | 10K | 阿里 | 阿里云集成 + Agentic 框架 | 国内企业、阿里云用户 |
| **Spring AI** | 8.9K | Spring 官方 | 正统 Spring 生态 AI 框架 | Spring 技术栈项目 |
| **LangGraph4j** | 1.7K | 社区 | Agent 工作流编排（Java） | 复杂多步骤 Agent |
| **JetBrains Koog** | 4.3K | JetBrains | Kotlin/JVM 企业级 Agent | Kotlin 项目 |
| **Agents-Flex** | 1K | 社区 | 轻量级 Java AI 框架 | 不想引入太重依赖 |
| **Solon-AI** | 401 | 国产 | 兼容 Java 8+ | 老项目改造 |

### 关键结论

1. **Spring AI 没有赢**——LangChain4j 12.3K > Spring AI 8.9K
2. **阿里押注 Spring AI**——fork 出 Spring AI Alibaba（10K），比官方还多
3. **LangChain4j + LangGraph4j** 是最完整的工具链
4. **Java 8 兼容**是中国特色需求——Solon-AI、mcp-java8-sdk 都在做

### 学习资源

| 项目 | ⭐ | 说明 |
|------|-----|------|
| **liyupi/yu-ai-agent** | 2.3K | Spring Boot 3 + Java 21 + Spring AI + ReAct Agent |
| **liyupi/yu-ai-code-mother** | 1.7K | Spring Boot 3 + LangChain4j + 微服务 |
| **langchain4j-examples** | 1.7K | LangChain4j 官方示例集 |

---

## 二、MCP 协议（Model Context Protocol）

### 是什么

AI Agent 连接外部工具的 **USB 标准接口**。

**之前：** 每个 Agent 平台各写一套对接代码  
**现在：** 写一个 MCP Server，所有 Agent 都能用

### 核心概念（三个）

```
Client (Agent)  ←→  MCP Server
     |                  |
     ├─ Tools     →  可调用的函数（搜索、查库、发邮件）
     ├─ Resources →  可读取的数据（文件、API 文档）
     └─ Prompts   →  预定义提示模板
```

### 传输层

| 方式 | 场景 |
|------|------|
| **stdio** | 本地进程通信（最常用） |
| **HTTP + SSE** | 远程服务 |

### Java 生态

| 项目 | ⭐ | 说明 |
|------|-----|------|
| **modelcontextprotocol/java-sdk** | 3.4K | 官方 Java SDK，Spring AI 团队联合维护 |
| **spring-ai-mcp** | 203 | Spring MCP 集成（已归档） |
| **mcp-annotations** | 42 | 注解驱动 MCP 开发 |
| **mcp-java8-sdk** | 49 | Java 8 兼容版 |

### Java 写 MCP Server（极简示例）

```java
@Tool(description = "查询老人健康数据")
public HealthData queryHealth(Long elderId) {
    return healthService.getLatest(elderId);
}
```

---

## 三、个人学习路线建议

### 当前阶段 → 目标

```
现在：黑马微服务学习中
      ↓
学完后：
  1. 跑通 yu-ai-agent（理解 Spring AI + ReAct Agent）
  2. 看 LangChain4j 官方 examples
  3. 给中州养老加 AI 功能（智能排班/健康分析）
  4. 写到简历 → 面试差异化王牌
```

### 为什么这条路值

- Java 程序员 90% 没碰过 AI Agent
- 长沙政务公司在搞智慧政务 = 需要"会 Java 又懂 AI"
- MCP 是 2026 最热基础设施协议，Java 是一等公民
- 学完 = Spring Boot + 微服务 + AI Agent 三件套

### 抖音选题

- 第1期：MCP 是什么（USB 接口比喻）
- 第2期：5 分钟用 Java SDK 写 MCP Server
- 第3期：Agent 怎么调用 MCP 工具
- 第4期：实战——给 Spring Boot 项目加 MCP

---

## 四、关键项目链接

| 项目 | GitHub |
|------|--------|
| LangChain4j | https://github.com/langchain4j/langchain4j |
| Spring AI | https://github.com/spring-projects/spring-ai |
| Spring AI Alibaba | https://github.com/alibaba/spring-ai-alibaba |
| LangGraph4j | https://github.com/langgraph4j/langgraph4j |
| MCP 官方规范 | https://github.com/modelcontextprotocol/modelcontextprotocol |
| MCP Java SDK | https://github.com/modelcontextprotocol/java-sdk |
| yu-ai-agent | https://github.com/liyupi/yu-ai-agent |

---

## 五、yu-ai-agent 项目深度剖析

> 本地路径：`D:\workspece\GitHup\yu-ai-agent`

### 项目概览

鱼皮（程序员鱼皮）的 AI 开发实战教学项目，两个核心模块：

| 模块 | 功能 | 核心技术 |
|------|------|---------|
| AI 恋爱大师 | 多轮情感对话 + RAG 知识库问答 | Spring AI ChatClient/Advisor/ChatMemory |
| YuManus 智能体 | ReAct 模式自主规划，搜索→抓取→下载→生成 PDF | Agent 工作流 + MCP 服务 |

### 架构设计（三层继承）

```
BaseAgent              ← 状态管理、消息上下文、步数控制(max 10步)、SSE流式输出
  └─ ReActAgent        ← think() + act() 抽象模板
       └─ ToolCallAgent ← 具体实现：调LLM→获取工具列表→执行工具→循环直到完成
```

**ReAct 循环流程：**

```
用户输入 → think(): 调LLM分析 → LLM返回 [搜索, 抓取, 下载]
        → act(): 逐个执行工具，记录结果
        → 结果喂回 LLM → 再 think() → ...
        → LLM 决定调 doTerminate → FINISHED
```

### 技术栈

| 组件 | 版本 | 说明 |
|------|------|------|
| Spring Boot | 3.4.4 | 主框架 |
| Java | 21 | 需要升级（当前项目用 JDK 11） |
| Spring AI | 1.0.0 | AI 框架核心 |
| Spring AI Alibaba | 1.0.0.2 | 阿里云百炼集成 |
| LangChain4j | 1.0.0-beta2 | 辅助集成 |
| PGVector | — | 向量数据库 |
| Ollama | — | 本地模型部署 |
| MCP Client | Spring AI Starter | MCP 协议客户端 |

### 手写 vs 框架

关键设计决策：鱼皮**禁用了 Spring AI 内置工具调用机制**，自己手写消息上下文管理。

```java
this.chatOptions = DashScopeChatOptions.builder()
    .withInternalToolExecutionEnabled(false)  // 关掉框架自动模式
    .build();
```

说明 Spring AI 的自动模式在复杂 Agent 场景下不够灵活——这个经验值得记住。

### MCP 实战：图片搜索服务

独立 MCP Server 模块，极简实现：

```java
@Service
public class ImageSearchTool {
    @Tool(description = "search image from web")
    public String searchImage(@ToolParam(description = "Search query keyword") String query) {
        // 调用 Pexels API
    }
}
```

支持 stdio 和 SSE 两种传输模式。

### 六个内置工具

| 工具 | 功能 |
|------|------|
| WebSearchTool | 联网搜索 |
| WebScrapingTool | 网页抓取 |
| ResourceDownloadTool | 资源下载 |
| PDFGenerationTool | PDF 生成 |
| FileOperationTool | 文件操作 |
| TerminalOperationTool | 终端操作 |

### 学习建议

1. **先不急着跑**——需要阿里云百炼 API Key + PostgreSQL + Pexels API Key，环境成本不低
2. **先看 B 站第一期免费视频**：https://www.bilibili.com/video/BV1Eq5DzcE9o
3. **学完微服务后再动手**——项目假设 Spring Boot 已经很熟
4. **完整教程需付费**（编程导航会员），先看第一期判断值不值

### 学习路线

```
现在 → 继续黑马微服务
学完后 → B站看第一期 → 决定是否加入编程导航
       → 跑通 → 给中州养老加 AI 功能（智能排班/健康分析）
       → 写到简历
```
