# 面试题：Spring AI + LangChain 双框架 — 2026.06.29

---

> 石化项目里 Java 用 Spring AI，Python 用 LangChain。**两个框架都调大模型，为什么要分开？用一个不行吗？各自负责什么？**

## 标准答案（60秒）

石化项目的 AI 层分两边，不是冗余，是各自在对方做不了的事上发力。

**Java 侧用 Spring AI 做企业集成。** Spring AI 有 Spring 容器的概念——@Tool 注解把后端的业务 Bean 直接暴露给 LLM。LLM 看到函数列表，自己判断什么时候调、调哪个、传什么参数，后端只负责执行。比如"查 430101 加油站当月销售额"，LLM 调了 `queryStationSales` 拿到真实数据就回答了。零跨语言，类型安全，事务边界完整。

**Python 侧用 LangChain 做 RAG 管道。** 石化有大量操作手册、安全规程，用户问"离心泵振动超标怎么处理"——这不是查数据库能回答的，得从文档里找。LangChain 的 NLP 流程很完善：文档加载、jieba 分词、BGE-M3 双向量嵌入（稠密做语义、稀疏做词汇匹配）、Milvus 混合检索、Reranker 重排序，最后交给 LLM 生成答案。这一套在 Java 生态没有等价实现——BGE-M3 的稀疏向量、SPARSE_INVERTED_INDEX 索引，都只在 pymilvus 里有。

**两边不是互相调用，是单向。** Java Gateway 判断 LLM 没调函数 → 说明这不是查数据的问题 → REST 转发 Python 走 RAG。Python 不调回来。

**换过来根本做不了，不是慢了。** 不是"延迟"问题——LangChain 调 @Tool 要 HTTP 绕路丢类型安全，Spring AI 做 BGE-M3 稀疏向量 Java 生态没等价物。

一句话：**Spring AI 管查数据，LangChain 管查文档。**

---

## 结构速记

```
① Java 侧 → 做什么？       → @Tool 暴露 Bean → 举例
② Python 侧 → 做什么？     → RAG 管道 → 举例
③ 怎么分？                 → 单向调用 → 不调回来
④ 为什么不合并？           → Java 没 BGE-M3，Python 没 Spring 容器
```

---

## 练习记录

| 轮次 | 日期 | 得分 | 问题 |
|------|------|------|------|
| 1 | 06.29 | 25 | Spring AI 说窄了，LangChain 只说分块 |
| 2 | 06.29 | 40 | 企业集成 vs NLP 管道框架对 |
| 3 | 06.29 | 30 | 退步，只剩 Function Calling |
| 4 | 06.29 | 45 | "绕路"听进去了 |
| 5 | 06.29 | 65 | 三点全说 |
| 6 | 06.29 | 78 | 框架稳固 |

**发音钉子（待加 TypeWords）**：LangChain、RAG、鉴权
