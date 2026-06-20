# 零基础 Java → Spring Boot → Java+AI 学习路线（8个月）

> 数据支撑来源：2026年6月 last30days 调研 — Reddit、bbs.itying.com、Pluralsight 2026 Tech Forecast、Stackademic、dev.to
>
> 核心结论：**先 Java 上岸，再 AI 溢价。** 纯 Java 在贬值，纯 AI 卷上天，两者叠加才是安全区，薪资溢价 40%+。

---

## 为什么先 Java 后 AI（而不是直接冲 AI）

| 维度 | 先 Java 后 AI | 直接冲 AI |
|------|-------------|----------|
| 首份工作周期 | 6-12 个月 | 2-3 年 |
| 数学门槛 | 不需要 | 线性代数 + 微积分 + 概率统计 |
| 被 AI 替代风险 | 初级 CRUD 有风险，但中级以上安全 | 初级调参岗正被 AutoML 吃掉 |
| 薪资天花板 | Java+AI 混合型 $160K+ | 纯 ML 也能到，但竞争人数多一个数量级 |
| 差异化 | 能做"把 AI 落到生产系统"的人，极少 | 会训模型的人多，会部署到生产的人少 |

**Reddit 获 22 赞的用户原话：** *"我一边死守 Java 一边强行学 ML，燃尽了两次。"*

---

## 八个月路线图

```
月1-2: Java 底子 ─────→ 控制台 CRUD 能写
月3-4: Spring Boot ───→ RESTful API 能搭  
月5:   项目实战 ──────→ 简历上有能讲的故事
月6:   面试 + AI 工具 ─→ LeetCode 中等 + Copilot 上手
月7:   投面循环 ──────→ 拿 offer
月8:   入职站稳 ──────→ 开始叠加 AI 技能
```

---

## 第 1 个月：Java 核心语法

**只学这一层，别碰框架。**

### 学习内容

- 变量、数据类型、运算符、流程控制（if/for/while）
- 面向对象三板斧：封装、继承、多态
- 集合框架：ArrayList、HashMap、HashSet（会用 + 懂原理）
- 异常处理：try-catch-finally、自定义异常
- IO 流：FileInputStream/OutputStream 的基本读写
- Java 8 lambda 表达式和 Stream API（2026 年面试必问）

### 验证标准

能不看资料写完一个"学生管理系统"控制台程序（增删改查 + 数据存文件），包含集合操作、异常处理、文件读写。

### 投入

每天 3-4 小时，周末全天。

---

## 第 2 个月：数据库 + 基础工具链

### 学习内容

- **MySQL**：增删改查、多表联查（JOIN）、索引原理、事务 ACID
- **JDBC**：用 Java 原生方式连接数据库，手写 SQL
- **Git**：init、add、commit、push、pull、branch、merge，GitHub 建仓
- **Linux 基础**：ls、cd、mkdir、rm、vim、tail、grep、ps、chmod
- **Maven**：依赖管理、pom.xml、mvn 命令

### 验证标准

把第 1 个月的"学生管理系统"改成 MySQL 存储 + JDBC 连接 + Maven 构建 + GitHub 提交。能在 Linux 虚拟机里启动和运行。

### 投入

继续每天 3-4 小时。

---

## 第 3 个月：Spring Boot 入门 + CRUD 实战

这是社区说的"人人都学会了"的那一层 —— 必须过，但别以为够了。

### 学习内容

- Spring Boot 自动配置原理（starter 是什么、怎么工作的）
- Controller-Service-Mapper 三层架构
- MyBatis-Plus（国内主流）/ JPA
- RESTful API 设计
- 参数校验（@Valid）
- 统一异常处理和统一响应体封装
- Swagger/Knife4j 接口文档

### 验证标准

做完一个完整的 RESTful API 项目 —— 比如"在线图书管理系统"，包含用户注册登录、图书 CRUD、借阅归还，接口文档自动生成，异常有统一处理。

### 投入

每天 3-4 小时，这个月代码量会很大。

---

## 第 4 个月：中间件 + 项目升级

这是简历上能拉开差距的开始。

### 学习内容

- **Redis**：String/Hash/List/Set/ZSet 五种类型、缓存穿透/击穿/雪崩的解决方案、分布式锁
- **Spring Security**：JWT 登录鉴权、权限控制
- **消息队列**：RabbitMQ 基础（发消息、消费消息、死信队列概念）
- **Docker**：写 Dockerfile、docker-compose 编排 Spring Boot + MySQL + Redis

### 验证标准

在第 3 个月的图书管理系统上加入 Redis 缓存 + JWT 登录 + Docker 一键部署。接口响应从 200ms 降到 20ms。

### 投入

每天 3-4 小时，Redis 和 Docker 是最重要的两个。

---

## 第 5 个月：项目实战（简历项目）

这里开始做"能在面试里讲的"项目，而不是教程项目。

### 项目方向（选一个）

1. **企业级后台管理系统** — RBAC 权限模型、多角色、菜单动态路由、操作日志、数据导出
2. **秒杀/抢购系统** — 限流、分布式锁（Redis）、库存扣减、异步下单（MQ）
3. **实时数据看板** — WebSocket 推送、定时任务、ECharts 图表、多数据源

### 验证标准

项目上线（云服务器或本地 Docker），GitHub README 写清楚架构图、技术选型理由、遇到的坑和解决方案。至少有一个可以讲 15 分钟的"难点突破"故事。

### 投入

每天 4-5 小时，这个月是核心竞争力建设。

---

## 第 6 个月：面试突击 + AI 工具入门

### 算法与系统设计

- **算法**：LeetCode 热门 100 的中等难度刷一遍（2026 年中等是底线）
- **系统设计**：短链系统、限流器、消息队列设计、分布式 ID 生成 —— 每个能画图讲 10 分钟
- **JVM 基础**：内存模型、GC 算法、常见调优参数
- **Spring Cloud 核心组件**：Nacos、Gateway、Feign、Sentinel

### 同步启动 AI 工具层

- GitHub Copilot 或 Cursor 上手日常编码
- 用 ChatGPT/Claude 做代码审查和问题排查
- 让 AI 帮你生成单元测试

### 验证标准

- 能不看资料讲清楚"你项目里最难的一个技术点"
- 能在白板上画出项目的架构图
- LeetCode 中等题 30 分钟内独立 AC

### 投入

每天 5-6 小时（如果已离职全职学）或 3-4 小时（在职）。

---

## 第 7 个月：投递 + 面试反馈循环

- 海投 50-100 家，拿到 5-10 个面试
- 每次面试录音回顾（自己听自己讲的技术点是否清晰）
- **面完一家立刻补漏** —— 被问到不会的，当天查当天学

### 目标岗位

初级/中级 Java 开发，薪资区间国内 8K-15K RMB/月（成都/杭州）或 12K-22K（北京/上海）。

### 验证标准

拿到至少 1 个 offer。

---

## 第 8 个月：入职 + 站稳

- 前两周：读懂项目代码、搞清楚部署流程、跟老员工结对
- 第一个月：独立完成一个中小需求（从需求评审到上线）
- 开始在工作中用 AI 工具提效（1 个中级 + AI ≈ 2-3 个初级）

---

## 上岸之后的 Java+AI 四层技能树

从这里开始叠加 AI 技能。详细展开见上次对话，这里只列骨架：

### 第一层：AI 工具增效（即时回报，0-3 个月）

- GitHub Copilot / Cursor → 代码补全和重构，直接提速 30-50%
- Claude / ChatGPT 做代码审查和架构咨询
- AI 生成单元测试和文档

### 第二层：Spring AI + LLM 集成（中期回报，3-12 个月）

- Spring AI 核心：统一 ChatClient API 对接多模型
- RAG（检索增强生成）落地：企业文档 + LLM 问答
- Vector Store 集成：Redis、Pgvector、Milvus
- Function Calling：让 LLM 调用已有 Java Service

### 第三层：Java 在 ML 基础设施中的角色（长期回报，1-2 年）

- Apache Kafka / Flink 做实时 ML Pipeline
- Spring Boot + ML Model Serving（gRPC / ONNX Runtime）
- Virtual Threads（Project Loom）高并发推理网关

### 第四层：AI 安全与治理（差异化溢价）

- AI 生成代码的安全审计
- Prompt Injection 防御
- 数据合规（GDPR / 个保法）

### 薪资跃升路径

| 阶段 | 预期薪资 | 时间 |
|------|---------|------|
| 纯 Java 上岸 | 国内 8K-15K / 月 | 6-8 个月 |
| Java + AI 工具增效 | 国内 12K-18K / 月 | 入职后 3-6 个月 |
| Java + Spring AI 落地 | 国内 18K-30K / 月 | 入职后 1-1.5 年 |
| Java + ML 基础设施 | 国内 30K-50K+ / 月 | 入职后 2-3 年 |

---

## 三个最容易翻车的地方

1. **第 1-2 个月追新技术** — 基础语法阶段不要碰 Spring、不要碰 Redis、不要看"2026 最新技术栈"文章。地基不牢后面全白费。
2. **项目只跟着教程敲** — 教程项目面试官一眼能认出来。第 5 个月的项目必须是你自己从零设计、遇到真实 bug、踩过坑的。那个"能讲 15 分钟的难点故事"比 GitHub star 数重要十倍。
3. **追求 100% 掌握再推进** — 60% 能动手就够了。Java 生态没有"学会了"的那一天，就是在项目里一边踩坑一边补。

---

## 核心信源

- [bbs.itying.com - Java 就业市场 2026 数据](https://bbs.itying.com/topic/6a2cba6044a60a004aad0407)
- [bbs.itying.com - 2026 招聘市场底层逻辑](https://bbs.itying.com/topic/6a2cba9244a60a004aad040e)
- [BSWEN - Spring Boot vs AI/ML 职业路径](https://docs.bswen.com/blog/2026-02-11-spring-boot-vs-aiml-career-path/)
- [Pluralsight 2026 Tech Forecast](https://www.pluralsight.com/content/dam/rebrand2025/resource-center/2026-tech-forecast/2026-pluralsight-forecast.pdf)
- [Stackademic - Everyone Learned Spring Boot, That's Why It's No Longer Enough](https://blog.stackademic.com/everyone-learned-spring-boot-thats-exactly-why-it-s-no-longer-enough-29830833cb22)
- [dev.to - Why Senior Java Developers Are Still in High Demand in 2026](https://dev.to/naveenkumar1/why-senior-java-developers-are-still-in-high-demand-in-2026-412h)
- [Eonreality - The Death of Code Monkeys](https://eonreality.com/wp-content/uploads/2025/06/Whitepaper-83-The-Death-of-Code-Monkeys.pdf)
- [上海人才 - AI Agent 人才需求激增](https://english.shanghai.gov.cn/en-Latest-TalentsinShanghai/20260323/e4638f3a9eec486eb7493205f4f51eb5.html)
