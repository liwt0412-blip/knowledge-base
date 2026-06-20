---
tags: [面试, Python, RAG, LangChain, 大模型应用, 项目介绍]
title: 保小宝-保险RAG问答项目面试话术
description: 基于LangChain+RAG架构的保险智能问答系统，用于面试时介绍项目的完整话术
date: 2026-06-20
sources:
  - 黑马课程AI大模型开发-Day5综合案例
related_project: D:\workspece\PythonProject\python_plus\day05-langchain\e-综合案例\insurance-qa-assistant
---

# 保小宝 — 保险智能问答助手 · 面试话术

> 基于 RAG（检索增强生成）的保险咨询系统，支持流式输出

---

## 一、一句话项目定位（30 秒）

> **"这是一个基于 RAG 架构的保险智能问答系统。用户问理赔流程、保单条款等问题时，系统先从保险知识库中检索相关文档片段，再交给大模型生成精准回答，并支持 SSE 流式逐字输出。"**

---

## 二、技术栈（面试官爱问这个）

| 层面 | 技术选型 | 为什么选 |
|---|---|---|
| Web 框架 | **FastAPI** | 原生 async 支持，天然适合 SSE 流式输出 |
| 大模型 | **通义千问 Qwen-Max**（阿里百炼平台） | 中文能力强，OpenAI 兼容接口，切换成本低 |
| 向量模型 | **text-embedding-v3**（阿里百炼） | 在线 API，免去本地部署嵌入模型的运维成本 |
| 向量数据库 | **Chroma**（本地持久化） | 轻量级，零配置，适合项目初版快速验证 |
| 文档拆分 | **RecursiveCharacterTextSplitter** | 按 `\n\n` → `\n` → `。` → `，` 优先级递归拆，语义完整性最好 |
| 文档加载 | LangChain 社区加载器（TextLoader / PDFMinerLoader / CSVLoader） | 统一接口，支持 txt / pdf / csv 多种格式 |
| 流式传输 | **Server-Sent Events (SSE)** | 比 WebSocket 轻量，浏览器原生支持，只需一个 HTTP 连接 |

**如果再做一个类似的系统，哪些可以换？**

- Chroma → 生产环境可以换 **Milvus** 或 **Elasticsearch**（支持分布式、千万级向量）
- Qwen-Max → 可以换 **DeepSeek** / **GLM-4**，API 接口兼容
- 百炼 Embedding → 换本地 **BGE-M3**，省钱但需要 GPU 部署

---

## 三、项目架构（画图说话）

```
┌──────────────────────────────────────────────────────────┐
│                   知识库构建（离线）                        │
│                                                          │
│  保险条款.txt ─┐                                          │
│  理赔流程.pdf ──→ 文档加载器 → 文本拆分器 → 向量化 → Chroma  │
│  产品对比.csv ─┘         (递归拆分)   (Embedding)   (向量库) │
└──────────────────────────────────────────────────────────┘

                         ↓ 用户提问

┌──────────────────────────────────────────────────────────┐
│                   在线问答（实时）                          │
│                                                          │
│  用户问题 → 向量化 → Chroma 相似度检索(Top3)               │
│                           ↓                               │
│              检索到的文档片段 + 用户问题                    │
│                           ↓                               │
│              组装 Prompt → Qwen-Max → 生成答案            │
│                           ↓                               │
│              SSE 流式返回（逐 token 输出）                   │
└──────────────────────────────────────────────────────────┘
```

---

## 四、核心流程详解（面试深入问的）

### Step 1：知识库构建（离线一次性跑）

```python
# build_vectorstore.py

# ① 加载 data/ 目录下的所有 txt / pdf / csv
loader = match_file_type(file_name)  # TextLoader / PDFMinerLoader / CSVLoader
docs = loader.load()

# ② 递归拆分：优先按段落拆，不行按句子，再不行按逗号
splitter = RecursiveCharacterTextSplitter(
    separators=["\n\n", "\n", "。", "，", " ", ""],
    chunk_size=100,
    chunk_overlap=10
)
chunks = splitter.split_documents(docs)

# ③ 向量化并存到 Chroma
Chroma.from_documents(chunks, embeddings_model, persist_directory="./chroma_vsdb")
```

**面试可延展的话题：**

> **"chunk_size 怎么定的？为什么 100？"**
> 项目中设为 100 是因为保险条款句子较短，100 字刚好覆盖一个完整条款。实际调参时要看业务：法律条文 chunk_size 可以大一点（200-300），FAQ 类可以小一点（50-100）。chunk_overlap 设为 10%~20% 保证上下文连贯性。

> **"递归拆分器和固定字符拆分器的区别？"**
> 固定拆分器在字符数满了就切，可能会把一句话从中间砍断。递归拆分器有多级分隔符优先级，优先在段落边界切，切不了才降级到句子、逗号，语义完整性要好很多。

### Step 2：在线问答（FastAPI 服务）

```python
# main.py — InsuranceQa 类

# ① 检索：问题向量化 → Chroma 相似度搜索
docs = chroma_db.similarity_search(query=question, k=3)

# ② 组装 Prompt
template = PromptTemplate.from_template("""
你是一个专业的保险顾问，名字叫保小宝。请根据以下信息回答问题。
检索到的内容: {context}
问题: {question}
答案:""")

# ③ 调用大模型
chain = template | chat_model
answer = chain.invoke({"context": docs, "question": question})
```

**面试可延展的话题：**

> **"为什么用 LCEL（`|` 链式调用）而不是传统的 Chain？"**
> LCEL 是 LangChain 的新一代管道式写法。好处：自动支持流式输出（`.astream()`），延迟初始化，类型安全，调试可以用 LangSmith 可视化。

### Step 3：流式输出（SSE）

```python
@router.post("/chat/stream")
async def chat_stream(request: ChatRequest):
    async def event_stream():
        async for token in qa.ask_stream(request.question):
            yield f"data: {json.dumps({'content': token})}\n\n"
        yield "data: [DONE]\n\n"

    return StreamingResponse(event_stream(), media_type="text/event-stream")
```

**面试可延展的话题：**

> **"为什么选 SSE 而不是 WebSocket？"**
> 1）场景是"一问一答"，不是双向实时通信，SSE 够用；2）SSE 走标准 HTTP，不需要 ws 协议握手，防火墙友好；3）浏览器原生 EventSource API 支持，前端接入成本低。但如果要做"流式过程中用户可打断"这类交互，WebSocket 更合适。

---

## 五、面试常见追问（准备好）

### Q1：怎么解决大模型幻觉？

> 我们项目用的是 RAG 方案。用户问题先检索知识库中相关的保险条款原文，再把这些原文片段作为上下文注入 Prompt，让模型**基于给定信息**回答，而不是凭空生成。如果检索到的信息不足，系统会直接说"无法回答"，不会编造。相比微调方案，RAG 的好处是更新知识只需更新文档库，不用重新训练模型。

### Q2：你用了哪些文档格式？不同格式处理有什么坑？

> 支持 txt、pdf、csv。txt 最简单直接读。PDF 用 PDFMinerLoader，复杂排版可能会乱，生产环境可以考虑把 PDF 先转 Markdown 再处理。CSV 自动按行拆分，每行生成一个 Document，适合产品对比表这类结构化数据。我们没用 Word 文档，如果需要可以用 UnstructuredWordDocumentLoader。

### Q3：怎么评估检索质量？

> 我们项目中只是做了功能验证，没有正式评估。生产环境需要做：1）**命中率评估** — 人工标注一批 QA 对，看 Top3 召回率；2）**chunk_size 调参实验** — 不同大小对比命中率；3）**重排序** — 初次检索后加一个 cross-encoder 做二次排序，提升 Top1 准确率。

### Q4：用户量上来后，这个架构能扛住吗？

> 目前单机跑，瓶颈在 Chroma 单机内存和 Qwen-Max API 的 QPS 限制。生产化方向：1）向量库换 Milvus 分布式集群；2）加 Redis 缓存高频问题；3）大模型换 DeepSeek 私有部署（vllm 推理加速）；4）FastAPI 加 uvicorn worker 数 + Nginx 反向代理做负载均衡。

### Q5：这项目你负责了哪些部分？

> （根据你自己实际情况说，示例）
> "整个项目从 0 到 1 都是我自己完成的——需求分析、技术选型、架构设计、编码实现。数据来源是课程给的保险文档，我独立完成了文档加载清洗、RAG 流程搭建、FastAPI 服务开发和流式输出对接。"

---

## 六、关键词速记

| 关键词 | 面试官听到会点头 |
|---|---|
| RAG | 检索增强生成，解决幻觉的主流方案 |
| LCEL | LangChain 管道式链调用，支持流式 |
| SSE | 服务端推送，比 WebSocket 轻量 |
| Chunk 策略 | 递归拆分 + 重叠窗口，保持语义 |
| Top-K 检索 | 设定 k=3，平衡相关性和上下文长度 |
| Embedding | 文本→稠密向量，数学距离衡量语义相似度 |

---

## 七、写在最后的话术

**如果面试官说："你这个项目看起来比较简单，就是调 API？"**

> "确实是调 API，但关键在于 RAG 的工程细节——文档怎么拆才能保证召回率？chunk_size 和 overlap 怎么调？检索结果怎么跟 Prompt 拼成有结构的上下文？流式输出时前端如何优雅展示？这些具体工程决策才是面试想考察的。而且这个架构可以快速迁移到其他业务场景，比如换成法律条款就是法律问答系统，换成运维手册就是 IT 知识库。"

---

## 相关笔记

- [[💼 面试/李文韬-石化项目AI方向面试专项素材]] — 石化项目AI助手面试素材（你的工作项目）
- [[python/Python笔记总览|Python笔记总览]]
- MOC: [[MOC-面试题]]
