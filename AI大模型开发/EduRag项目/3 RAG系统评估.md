---
tags:
  - RAG
  - RAGAS
  - 评估
  - EduRAG
title: RAG系统评估
description: RAGAS 评估框架：评估 RAG 系统的检索和生成质量
date: 2025-06-22
sources:
  - 黑马课程讲义: EduRAG项目
---

# 03-RAG系统评估

## 1. 概述

当我们为某个真实线上系统开发了检索增强生成 (RAG) 应用，那么在此应用正式上线提供服务前，我们需要评估 RAG 的表现到底是怎样的。如果发现现有的 RAG 效果不够理想，可能需要一些新的 RAG 算法流程来改进。在这之前，就需要对 RAG 流程进行评估，得到评估指标，然后才能进行自动化对比，观察改进的流程是否真的有效。

## 2. RAGAS评估框架

RAGAS (**R**etrieval **A**ugmented **G**eneration Assessment) 我们一般称为 Automated Evaluation of Retrieval Augmented Generation，即检索增强生成的自动评估。Ragas是一个大模型评测框架，可以评估检索增强生成（RAG）的效果，帮助分析模型的输出，了解模型在给定任务上的表现。

Github地址: <https://github.com/explodinggradients/ragas>

RAGAS的评估主要基于两个方向：检索部分和生成部分，那么针对不同的部分评估的指标也会有所区分。接下来，我们将分别介绍RAGAS评估框架所需的数据，评估指标，实际用例等。

### 2.1 数据说明

最开始的 RAGAs 在评估数据集时，不必依赖人工标注的标准答案，而是通过底层的大语言模型 (**LLM**) 来进行评估。所以只需要一个带有问题-答案对的评估数据集（QA 对），如：<https://huggingface.co/datasets/m-ric/huggingface_doc> 具体字段：

question：作为 RAG 管道输入的用户查询，输入。

answer：从 RAG 管道生成的答案，输出。

contexts：从用于回答question外部知识源中检索的上下文。

ground_truths：question的基本事实答案。这是唯一人工注释的信息。

### 2.2 评估指标

![](images/media/image1.png)

**评估检索（context）**的指标：提供了上下文相关性（context_relevancy）和上下文召回率（context_recall），这些可以衡量你的检索系统的性能，即检索的段落是否相关。

**评估生成（answer）**的指标：提供了忠实度（faithfulness），用以衡量生成的信息是否准确无误；以及答案相关性（answer_relevancy），用以衡量答案对问题的切题程度，即模型生成的答案是否恰当。

#### 2.2.1 上下文相关性 (Context Relevancy)

**核心概念**

**衡量检索到的上下文是否专注且无冗余** - 评估检索系统能否精准找到与问题直接相关的信息，避免无关内容的干扰。

**评估原理**

**目标**：惩罚包含冗余信息的检索结果

**方法**：使用LLM从检索到的上下文中提取与问题直接相关的句子

**计算公式**：

```
上下文相关性 = 提取的相关句子数量 / 上下文中的总句子数量

```

**实际例子**

**问题**："苹果公司成立于哪一年？"

**检索到的上下文**：

"苹果公司由史蒂夫·乔布斯、史蒂夫·沃兹尼亚克和罗纳德·韦恩于1976年4月1日创立。"

"公司最初主要销售个人电脑，后来扩展到消费电子产品。"

"苹果公司的总部位于加利福尼亚州的库比蒂诺。"

**评估过程**：

相关句子：只有第一句包含成立年份信息

总句子数：3句

得分：1/3 ≈ 0.33

#### 2.2.2 上下文召回率 (Context Recall)

**核心概念**

**衡量检索系统能否找到所有必要信息** - 评估检索内容是否完整覆盖回答问题所需的所有关键点。

**评估原理**

**依赖数据**：需要人工标注的ground_truth（标准答案）

**方法**：将标准答案分解为多个声明(claims)，检查每个声明是否能从上下文中找到支持

**计算公式**：

```
上下文召回率 = 被上下文支持的声明数量 / 总声明数量

```

**实际例子**

**问题**："介绍2010年世界杯决赛情况"

**标准答案**：

"2010年世界杯冠军是西班牙"

"西班牙在决赛中以1-0击败荷兰"

"决赛在南非约翰内斯堡举行"

**检索到的上下文**：

"西班牙在2010年世界杯决赛中击败了荷兰"

"2010年世界杯冠军是西班牙，这是西班牙首次赢得世界杯"

**评估过程**：

声明1："2010年世界杯冠军是西班牙" → ✅ 支持

声明2："西班牙在决赛中以1-0击败荷兰" → ❌ 未提及具体比分

声明3："决赛在南非约翰内斯堡举行" → ❌ 未提及地点

得分：1/3 ≈ 0.33

#### 2.2.3 忠实度 (Faithfulness)

**核心概念**

**衡量生成答案是否严格基于给定上下文** - 检测模型是否"编造"了上下文中不存在的信息（幻觉问题）。

**评估原理**

**提取陈述**：从生成答案中提取所有事实陈述

**验证支持**：检查每个陈述是否能从上下文中推断出来

**计算比例**：

```
忠实度 = 被上下文支持的陈述数量 / 总陈述数量

```

**实际例子**

**上下文**："苹果公司成立于1976年，创始人是乔布斯、沃兹尼亚克和韦恩"

**生成答案**："苹果公司由乔布斯和沃兹尼亚克于1976年创立，总部在库比蒂诺"

**评估过程**：

陈述1："苹果公司由乔布斯和沃兹尼亚克创立" → ✅ 部分正确（漏了韦恩）

陈述2："成立于1976年" → ✅ 正确

陈述3："总部在库比蒂诺" → ❌ 上下文中未提及

得分：2/3 ≈ 0.67

#### 2.2.4 答案相关性 (Answer Relevancy)

**核心概念**

**衡量生成答案与原始问题的匹配程度** - 评估答案是否真正回答了问题，而不是答非所问。

**评估原理**

**问题生成**：基于生成答案反推可能的问题

**相似度计算**：比较生成问题与原始问题的语义相似度

**平均得分**：

```
答案相关性 = 所有生成问题与原始问题的平均相似度

```

**实际例子**

**原始问题**："如何学习Python编程？"

**生成答案**："建议从基础语法开始，多写代码练习，参考官方文档"

**评估过程**：

从答案生成的可能问题：

"学习Python的方法有哪些？" → 高相似度

"Python入门建议？" → 高相似度

"编程学习步骤？" → 中等相似度

计算平均相似度得分

#### 2.2.5 总结对比

  ------------------ -------------- -------------- ---------------------- ------------------
  **指标**           **评估对象**   **核心目标**   **依赖数据**           **问题表现**

  **上下文相关性**   检索系统       精准无冗余     问题+上下文            检索信息不聚焦

  **上下文召回率**   检索系统       完整覆盖       问题+上下文+标准答案   遗漏关键信息

  **忠实度**         生成系统       基于事实       问题+答案+上下文       编造虚假信息

  **答案相关性**     生成系统       切题回答       问题+答案              答非所问
  ------------------ -------------- -------------- ---------------------- ------------------

## 3. RAGAS 评估脚本

### 3.1 功能描述

ragas_evaluate.py脚本用于评估RAG系统的性能，具体功能包括：

**数据集加载**：从JSON文件加载包含问题、答案、上下文和真实答案的评估数据集。

**数据格式转换**：将JSON数据转换为RAGAS要求的Dataset格式。

**环境配置**：使用LangChain的OpenAI模型和嵌入模型初始化RAGAS评估环境。

**评估执行**：计算四个核心指标：

**Faithfulness（忠实度）**：答案是否忠于上下文。

**Answer Relevancy（答案相关性）**：答案与问题的匹配程度。

**Context Relevancy（上下文相关性）**：上下文是否与问题相关。

**Context Recall（上下文召回率）**：上下文是否包含所有必要信息。

**结果输出与保存**：打印评估结果并保存为CSV文件，便于后续分析。

### 3.2 评估脚本

安装依赖

```bash
pip install ragas

```

详细代码：

```python
\# 导入pandas库，用于数据处理和保存CSV文件
import pandas as pd
\# 导入ragas库的evaluate函数，用于执行RAG评估
from ragas import evaluate
\# 导入ragas的评估指标，包括忠实度、答案相关性、上下文相关性和上下文召回率
from ragas.metrics import (
faithfulness,
answer_relevancy,
context_precision,
context_recall
)
\# 导入datasets库的Dataset类，用于构建RAGAS所需的数据格式
from datasets import Dataset
\# 导入langchain_openai的嵌入模型和聊天模型，用于评估时的语义计算和推理
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
\# 导入json库，用于加载JSON格式的评估数据集
import json

\# 1. 加载生成的数据集
\# 使用with语句打开JSON文件，确保文件正确关闭，指定编码为utf-8
with open("rag_evaluation_dataset.json", "r", encoding="utf-8") as f:
\# 将JSON文件内容加载到data变量中，data为包含多个数据条目的列表
data = json.load(f)

\# 2. 转换为RAGAS格式
\# 创建字典eval_data，将JSON数据转换为RAGAS要求的字段格式
eval_data = {
\# 提取每个数据条目的question字段，组成问题列表
"question": [item["question"] for item in data],
\# 提取每个数据条目的answer字段，组成答案列表
"answer": [item["answer"] for item in data],
\# 提取每个数据条目的context字段，组成上下文列表（每个context为列表）
"contexts": [item["context"] for item in data],
\# 提取每个数据条目的ground_truth字段，组成真实答案列表
"ground_truth": [item["ground_truth"] for item in data]
}
\# 使用Dataset.from_dict将字典转换为RAGAS所需的Dataset对象
dataset = Dataset.from_dict(eval_data)

\# 3. 配置RAGAS评估环境
\# 初始化ChatOpenAI模型，指定使用gpt-4模型，并设置OpenAI API密钥
llm = ChatOpenAI(model="gpt-4", openai_api_key="your_openai_api_key")
\# 初始化OpenAI嵌入模型，用于计算语义相似度，设置API密钥
embeddings = OpenAIEmbeddings(openai_api_key="your_openai_api_key")

\# 4. 执行评估
\# 调用evaluate函数，传入数据集、评估指标、LLM模型和嵌入模型
result = evaluate(
\# 传入转换好的Dataset对象
dataset=dataset,
\# 指定使用的评估指标列表
metrics=[
faithfulness, \# 忠实度：答案是否基于上下文
answer_relevancy, \# 答案相关性：答案与问题的匹配度
context_relevancy, \# 上下文相关性：上下文是否仅包含相关信息
context_recall \# 上下文召回率：上下文是否包含所有必要信息
],
\# 传入配置好的LLM模型
llm=llm,
\# 传入配置好的嵌入模型
embeddings=embeddings
)

\# 5. 输出并保存结果
\# 打印评估结果标题
print("RAGAS评估结果：")
\# 打印评估结果，包含各指标的分数
print(result)
\# 将评估结果转换为pandas DataFrame，便于保存
result_df = pd.DataFrame([result])
\# 将DataFrame保存为CSV文件，文件名为ragas_evaluation_results.csv，不保存索引
result_df.to_csv("ragas_evaluation_results.csv", index=False)

```

**数据集格式**：

RAGAS要求数据集包含question、answer、contexts（列表格式）和ground_truth四个字段。

contexts必须是列表，即使每个问题只对应一个上下文（如["context text"]）。

**评估指标**：

**Faithfulness**：依赖LLM（如gpt-4）判断答案是否基于上下文，避免生成无关内容。

**Answer Relevancy**：使用嵌入模型（OpenAIEmbeddings）计算答案与问题的语义相似度。

**Context Relevancy**：评估上下文是否仅包含与问题相关的信息，减少冗余。

**Context Recall**：检查上下文是否覆盖所有必要信息，需高质量的ground_truth支持。

**环境配置**：

ChatOpenAI用于生成评估所需的推理（如判断忠实度），需指定模型（如gpt-4）和API密钥。

OpenAIEmbeddings用于计算语义相似度（如答案相关性），需确保API密钥有效。

可替换为其他LLM（如通义千问），需适配LangChain的模型接口。

**结果分析**：

评估结果为字典，包含各指标的分数（0-1，1为最佳），如：

```json
{
'faithfulness': 0.95,
'answer_relevancy': 0.92,
'context_relevancy': 0.90,
'context_recall': 0.93
}

```

结果保存为CSV文件（ragas_evaluation_results.csv），便于统计分析和多次运行比较。

**迁移性**：

代码结构通用，可用于任何RAG系统评估，只需替换数据集和LLM配置。

可扩展指标（如answer_correctness）或添加自定义数据处理逻辑（如过滤低质量数据）。



---

## 相关笔记

- [[AI大模型开发总览|AI大模型开发总览]]
- [[1 环境搭建和Milvus向量数据库|环境搭建和Milvus向量数据库]]
