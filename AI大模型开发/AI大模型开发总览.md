---
tags:
  - MOC
  - AI大模型
  - Python
  - RAG
  - LangChain
created: 2026-06-22
---

# AI 大模型开发

> Python 技术栈的 AI / 大模型项目实战。与 [[SpringAI+AIGC应用/SpringAI+AIGC应用总览|SpringAI+AIGC应用（Java）]] 互补。

## 项目实战

### EduRAG 智能答疑系统

**环境搭建**
- [[1 环境搭建和Milvus向量数据库|1 环境搭建和Milvus向量数据库]] — RAG项目搭建、Milvus概念、索引类型（FLAT/IVF/HNSW）、相似度度量、混合搜索
- [[1.1Milvus环境搭建（自己搭建）|1]] — Docker 部署 Milvus（etcd + minio + milvus）完整流程
- [[1.2挂载虚拟机|1]] — VMware 虚拟机 NAT 网络配置

**核心模块**
- [[2 RAG问答系统-核心模块|2 RAG问答系统-核心模块]] — base 模块、配置管理、检索、生成等核心流程
- [[EduRag项目/mysql_qa-BM25快速检索模块|mysql_qa-BM25 快速检索]] — BM25 + MySQL + Redis 关键词匹配，RAG 系统的快路由
- [[2.3文档解析工具(扩展)|文档解析工具]] — PDF/DOCX/PPTX/Images 解析 + RapidOCR + 文本切分器
- [[2.2BERT微调|2]] — BERT 文本分类微调、FAQ 意图识别实战
- [[2.1向量模型和重排序模型|2 向量模型和重排序模型]] — BGE-M3 向量模型 + Reranker 重排序

**评估与集成**
- [[3 RAG系统评估|3 RAG系统评估]] — RAGAS 评估框架、检索与生成质量评测
- [[4 系统集成和发布|4 系统集成和发布]] — FAQ + RAG 融合、对话历史、流式输出、FastAPI 部署

**简历**
- [[5 EduRAG简历参考|EduRAG 简历参考]] — 项目简历话术，含技术栈、项目背景、个人职责

## 关联基础

- [[AI大模型开发基础/AI大模型开发基础总览|AI大模型开发基础]] — Python基础 → LangChain 入门
- [[python/Python笔记总览|Python笔记总览]] — Python 语法与工具

## 相关领域

- [[SpringAI+AIGC应用/SpringAI+AIGC应用总览|SpringAI+AIGC应用]] — Java 技术栈 AI 开发
- [[SpringAI+AIGC应用/AI应用技术全景|AI应用技术全景（2025-2026）]] — 技术全景参考
- [[SpringAI+AIGC应用/持久化VectorStore|持久化VectorStore]] — 向量数据库持久化

## 相关笔记

- [[MOC-日常学习]]
- [[MOC-编程相关]]
