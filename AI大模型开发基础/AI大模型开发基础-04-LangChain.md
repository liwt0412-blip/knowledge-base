---
tags: [LangChain, AI, 大模型, LLM]
title: AI大模型开发基础-04-LangChain
description: LangChain概述：核心功能、应用场景、环境搭建、模型调用
date: 2026-06-18
sources:
  - 黑马课程讲义: AI大模型开发基础课程
---
## 04-LangChain
## 1 LangChain概述
LangChain由Harrison Chase创建于2022年10月，它是围绕LLMs（大语言模型）建立的一个框架
从与OpenAI等顶级大模型供应商集成到复杂的对话系统、智能搜索、推荐系统等，LangChain提供了丰富的功能和灵活的接口
LangChain目前有三个语言的实现：**python**、nodejs、Java(LangChain4J)
LangChain官方网址：https://www.langchain.com/
LangChain中文官方网址：https://www.langchain.com.cn/
LangChainAPI文档：https://python.langchain.com/api_reference/
![](images/media/image1.png)
### 1.1 核心功能
**API集成：**LangChain支持与多种大模型API的集成，包括OpenAI、Azure、Google等，方便用户快速接入并使用这些模型
**上下文管理：**LangChain通过内置的上下文管理工具，能够在对话中保留上下文信息，使得与用户的互动更加智能、自然
**多模态支持：**LangChain支持文本、图像、视频等多种模式的数据输入与处理，进一步拓宽了应用场景
**定制化：**LangChain提供了灵活的定制接口，允许开发者根据具体需求调整模型的行为、输出格式等，打造专属的智能应用
### 1.2 应用场景
**对话式AI助手：**借助LangChain的上下文管理功能，可以构建更加自然、连贯的对话系统，用于智能客服、虚拟助手等
**智能搜索与推荐：**通过集成大模型API，LangChain可以为网站或应用添加智能搜索与推荐功能，提升用户体验
**内容生成与优化：**使用LangChain，开发者可以构建自动生成内容的工具，包括文章写作、代码生成等，大幅提升效率
**中大型RAG系统：**使用LangChain各个组件配合使用，构建企业级知识库检索系统
### 1.3 架构
LangChain简化了LLM应用程序生命周期的每个阶段：
开发：使用LangChain的开源[构建模块](https://www.langchain.com.cn/docs/concepts/#langchain-expression-language-lcel)、[组件](https://www.langchain.com.cn/docs/concepts/)和[第三方集成](https://www.langchain.com.cn/docs/integrations/platforms/)构建应用程序，使用[LangGraph](https://www.langchain.com.cn/docs/concepts/#langgraph)构建具有流式处理和人机协作支持的有状态代理
生产化：使用[LangSmith](https://docs.smith.langchain.com/)检查、监控和评估您的链，以便您可以持续优化并自信地部署
部署：将您的LangGraph应用程序转变为生产就绪的API和助手，使用[LangGraph Cloud](https://langchain-ai.github.io/langgraph/cloud/)
![](images/media/image2.png)
具体来说，该框架由以下开源库组成：
**langchain-core**: 聊天模型和其他组件的基本抽象
**langchain-community**: 由社区维护的第三方集成
合作伙伴库（例如 langchain-openai、langchain-anthropic 等）：一些集成已进一步拆分为自己的轻量级库
**langchain**: 组成应用程序认知架构的链、代理和检索策略。
[**LangGraph**](https://langchain-ai.github.io/langgraph): 通过将步骤建模为图中的边和节点，构建强大且有状态的多参与者应用程序
[**LangServe**](https://www.langchain.com.cn/docs/langserve/): 将LangChain链部署为REST AP。
[**LangSmith**](https://docs.smith.langchain.com/): 一个开发者平台，让您调试、测试、评估和监控LLM应用程序
### 1.4 常见组件
一个LangChain的应用是需要多个组件共同实现的，常见的组件如下：
**Models**：模型，各种类型的模型和模型集成，比如GPT-4
**Prompts**：提示，包括提示管理、提示优化和提示序列化
**Memory**：记忆，用来保存和模型交互时的上下文状态
**Indexes**：索引，用来结构化文档，以便和模型交互
**Chains**：链，一系列对各种组件的调用
**Agents**：代理，决定模型采取哪些行动，执行并且观察流程，直到完成为止
### 1.5 快速入门
需求：我们使用LangChain来调用本地ollama的qwen2.5:7b模型，实现简单对话
## ① 安装依赖
由于要使用langchain，有两个必备的包：langchain和langchain-community，还有就是ollama的包
```
  Bash
  # 安装langchain
  pip install langchain==1.0.7
  # 社区集成库
  pip install langchain-community==0.4.1
  # 安装langchain-ollama
  pip install langchain-ollama==1.0.0
```
## ② 代码实现
```
  Python
  01-入门案例
  """*
  *使用langchain调用ollama中部署的qwen2.5:7b大模型, 让他写一首关于秋天的诗*
  *"""*
  *# 1. 导包*
  *from langchain_ollama import ChatOllama*
  *# 2. 创建大模型*
  *chat = ChatOllama(model="qwen2.5:7b")*
  *# 3. 准备提示词*
  *prompt = "你是一位浪漫主义诗人,请帮我写一首关于秋天的诗"*
  *# 4. 调用大模型*
  *result = chat.invoke(prompt)*
  *# 5. 输出结果*
  *print(result)*
  *print(result.content)
```
## 2 Models组件
现在市面上的模型多如牛毛，各种各样的模型不断出现，LangChain模型组件提供了与各种模型的集成，并为所有模型提供了一个精简的统一接口
官方文档：https://python.langchain.com/docs/concepts/chat_models/
LangChain目前支持三种类型的模型：LLMs（大模型）、Chat Models（聊天模型）、Embeddings Models（向量模型）
**LLMs**: 大语言模型接收文本字符作为输入，返回的也是文本字符
**聊天模型**: 基于LLMs, 不同的是它接收聊天消息（一种特定格式的数据）作为输入，返回的也是聊天消息
**向量模型**: 接收文本作为输入, 返回的是浮点数列表
在这里我们主要使用的是**聊天模型**，下面也以它为样例给大家做介绍
### 2.1 消息类型
聊天消息包含下面几种类型，使用时需要按照约定传入合适的值
**SystemMessage:** 可以用于指定模型具体所处的环境和背景，如角色扮演等
**HumanMessage**: 人类消息就是用户信息，由人给出的信息发送给LLMs的提示信息
**AIMessage**: 就是AI输出的消息，可以是针对问题的回答
**ChatMessage**: Chat消息可以接受任意角色的参数，但是在大多数时间，我们应该使用上面的三种类型
```
  Python
  01-消息类型
  """
  聊天消息包含下面几种类型，使用时需要按照约定传入合适的值
  - SystemMessage: 可以用于指定模型具体所处的环境和背景，如角色扮演等
  - HumanMessage: 人类消息就是用户信息，由人给出的信息发送给LLMs的提示信息
  - AIMessage: 就是 AI 输出的消息，可以是针对问题的回答
  - ChatMessage: Chat消息可以接受任意角色的参数，但是在大多数时间，我们应该使用上面的三种类型
  """
  # 导包
  from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
  #创建message对象
  message_list = \[
  SystemMessage(content="你是一个诗人,请使用浪漫主义的风格写诗"),
  HumanMessage(content="写一首秋天的诗"),
  AIMessage("秋风虽萧瑟，却也暖人心")
  \]
  print(message_list)
```
### 2.2 调用大模型（Ollama）
接下来使用Chat模型调用Ollama平台，注意：Langchain提供了ChatOllama来完成跟Ollama平台的对接
```
  Python
  *"""*
  *接下来使用Chat模型调用Ollama平台，注意：Langchain提供了ChatOllama来完成跟Ollama平台的对接*
  *"""*
  *# 1. 导包*
  from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
  from langchain_ollama import ChatOllama
  *# 2. 创建大模型*
  model = ChatOllama(model="qwen2.5:7b")
  *# 3. 准备提示词*
  messages = \[
  SystemMessage(content="你是一个诗人,请使用浪漫主义的风格写诗"),
  HumanMessage(content="写一首秋天的诗")
  \]
  *# 4. 调用大模型*
  result = model.invoke(messages)
  *# 5. 输出结果*
  print(result.content)
```
### 2.3 调用大模型（百炼）
接下来使用Chat模型调用百炼平台，注意：Langchain提供了ChatOpenAI来完成跟实现了OpenAI规范的平台对接
```
  Shell
  # 安装langchain-openai
  pip install langchain-openai==1.0.3
  Python
  *"""*
  *接下来使用Chat模型调用百炼平台，注意：Langchain提供了ChatOpenAI来完成跟实现了OpenAI规范的平台对接*
  *"""*
  *# 1. 导包*
  from langchain_openai import ChatOpenAI
  from langchain_core.messages import SystemMessage, HumanMessage
  import os
  *# 2. 创建大模型*
  model = ChatOpenAI(
  model="qwen-max", *# 模型名称*
  base_url="https://dashscope.aliyuncs.com/compatible-mode/v1", *# 百炼的通用端点*
  api_key=os.getenv("OPENAI_API_KEY") *# api_key*
  )
  *# 3. 准备提示词*
  messages = \[
  SystemMessage("你是一位浪漫主义诗人"),
  HumanMessage("请帮我写一首关于秋天的诗")
  \]
  *# 4. 调用大模型*
  chunks = model.stream(messages)
  *# 5. 处理返回结果*
  for chunk in chunks:
  print(chunk.text, end="", flush=True)
  *# # 4. 调用大模型*
  *# result = model.invoke(messages)*
  *#*
  *# # 5. 处理返回结果*
  *# print(result.content)*
```
## 3 Prompts组件
Prompts组件主要用于构建提示词，可以方便提示词的动态书写
官方文档：https://python.langchain.com/docs/concepts/prompt_templates/
### 3.1 字符串提示模板
字符串模版适用于简单提示词中含有一些变量的情况，例如：我的邻居姓**{lastname}，**他生了个儿子，给他儿子起个名字
template = PromptTemplate.from_template("我的邻居姓{lastname}，他生了个儿子，给他儿子起个名字")
prompt = template.invoke({"lastname": "张"})
```
  Python
  """*
  *字符串模版适用于简单提示词中含有一些变量的情况，例如：我的邻居姓{lastname}，他生了个儿子，给他儿子起个名字*
  *"""*
  *# 1. 导包*
  *from langchain_openai import ChatOpenAI*
  *from langchain_core.prompts import PromptTemplate*
  *import os*
  *# 2. 创建大模型对象*
  *model = ChatOpenAI(*
  * model="qwen-max", # 模型名称*
  * base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",*
  * api_key=os.getenv("OPENAI_API_KEY")*
  *)*
  *# 3. 提示词*
  *# 3-1 构建提示词模版*
  *template = PromptTemplate.from_template("我的邻居姓{lastname}，他生了个儿子，给他儿子起个名字")*
  *# 3-2 创建提示词*
  *prompt = template.invoke({"lastname": "张"})*
  *# 4. 调用大模型*
  *result = model.invoke(prompt)*
  *# 5. 处理结果*
  *print(result.content)
```
### 3.2 ChatPrompt模板
ChatPrompt主要应用在跟大模型聊天对话的场景下。 构造和使用ChatPromptTemplate的常用方法如下：
template = ChatPromptTemplate(\[
("system", "你是一个诗人"),
("user", "请写一首关于{topic}的{style}风格的诗"),
\])
```
  Python
  """*
  *ChatPrompt主要应用在跟大模型聊天对话的场景下。 构造和使用 ChatPromptTemplate 的常用方法如下：*
  *prompt_template = ChatPromptTemplate(\[*
  * ("system", "你是一个诗人"),*
  * ("user", "请写一首关于{topic}的{style}风格的诗"),*
  *\])*
  *"""*
  *# 1. 导包*
  *from langchain_openai import ChatOpenAI*
  *from langchain_core.prompts import ChatPromptTemplate*
  *import os*
  *# 2. 创建大模型*
  *model = ChatOpenAI(*
  * model="qwen-max", # 模型名称*
  * base_url="https://dashscope.aliyuncs.com/compatible-mode/v1", # 百炼的通用端点*
  * api_key=os.getenv("OPENAI_API_KEY") # api_key*
  *)*
  *# 3. 准备提示词*
  *# 3-1 创建提示词模版*
  *template = ChatPromptTemplate(\[*
  * ("system", "你是一个诗人"),*
  * ("user", "你要写一首关于{topic}的{style}风格的诗")*
  *\])*
  *# 3-2 根据模版创建提示词*
  *prompt = template.invoke({"topic": "秋天", "style": "婉约"})*
  *# 4. 调用大模型*
  *result = model.invoke(prompt)*
  *# 5. 处理返回结果*
  *print(result.content)
```
### 3.3 few-shot模版
在构建提示词的过程中，引入少量示例是一种简单而高效的引导生成方式，能够有效提升模型的表现。
每一个示例通常以字典形式组织，其中键表示输入变量，值则是对应的具体内容。
针对不同类型的模型（例如传统LLM和聊天模型）可以分别选用 FewShotPromptTemplate 或 FewShotChatMessagePromptTemplate 来实现这一方法
## 需求说明：
让大模型通过一个词来获得反义词，比如：**开心**，反义词为**难过**，我们通过少量样本组装到提示词中，让大模型更好的输出反义词的内容
```
  Python
  """*
  *让大模型通过一个词来获得反义词，比如：开心，反义词为难过，我们通过少量样本组装到提示词中，让大模型更好的输出反义词的内容*
  *"""*
  *# 1. 导包*
  *from langchain_openai import ChatOpenAI*
  *from langchain_core.prompts import PromptTemplate, FewShotPromptTemplate*
  *import os*
  *# 2. 创建大模型对象*
  *model = ChatOpenAI(*
  * model="qwen-max", # 模型名称*
  * base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",*
  * api_key=os.getenv("OPENAI_API_KEY")*
  *)*
  *# 3. 提示词*
  *# 3-1 准备样例*
  *examples = \[*
  * {"word": "开心", "antonym": "难过"},*
  * {"word": "高", "antonym": "矮"}*
  *\]*
  *# 3-2 准备样例模版*
  *template = PromptTemplate(template="现在有一个单词是单词:{word},反义词:{antonym}")*
  *# 3-3 准备提示词模版*
  *few_shot_template = FewShotPromptTemplate(*
  * example_prompt=template, # 提示词示例模版*
  * examples=examples, # 提示词示例数据*
  * prefix="你是一个汉语言文学专家, 请给出对应单词的反义词", # 提示词前缀(身份)*
  * suffix="现在有一个单词是:{w},它的反义词是:" # 提示词后缀(具体问题)*
  *)*
  *# 3-4 模版中填充值*
  *prompt = few_shot_template.format(w="粗")*
  *# 4. 调用大模型*
  *result = model.invoke(prompt)*
  *# 5. 处理结果*
  *print(result.content)
```
## 4 Chains组件
Chain（链）是构建大模型应用的核心编排机制，其价值在于处理那些需要多步骤协作的复杂任务
它通过标准化的接口将离散的组件（如提示模板、LLM模型、记忆系统、外部工具等）串联成一个可执行、可复用的完整工作流
它并非创造新组件，而是通过精妙的组合，让每个组件的优势得以叠加和互补，从而实现单一模型或工具无法完成的复杂功能
一个典型的链式服务，其构建过程通常涵盖以下四种关键模式：
## 固化指令流：LLM + 提示模板
**描述**：将静态的提示模板与动态的用户输入结合后，再提交给LLM。这是最基础的链，确保了每次请求的结构化和标准化
**场景**：生成特定格式的邮件、代码或报告
## 知识增强流：LLM + 外部数据
**描述**：在提问前，先从外部知识源（如数据库、搜索引擎、文档）检索相关信息，并将其作为上下文填入提示词中，极大地提升了问答的准确性和专业性
**场景**：构建智能客服、企业知识库问答系统
## 情境对话流：LLM + 长期记忆
**描述**：将对话历史作为"记忆"存储在特定组件中，并在每次新的交互中自动将相关历史记录作为上下文传递给LLM
**场景**：开发有长期记忆的个性化聊天机器人、心理咨询助手
## 决策流水线：LLM + LLM
**描述**：将任务拆解成多个由不同LLM负责的子步骤，前一个LLM的输出结果，经过处理后，作为下一个LLM的输入
**场景**：先让一个LLM分析用户需求并生成数据分析大纲，再让另一个擅长代码的LLM根据大纲编写具体的SQL查询语句
### 4.1 提示词 \| 大模型
针对上一小节的提示模版例子，字符串提示模板里面，我们可以用链来连接提示模版组件和模型，进而可以实现代码的更改：
```
  Python
  *"""*
  *提示词 \| 大模型 的意思是将提示词模版交给大模型出来*
  *"""*
  *# 1. 导包*
  from langchain_openai import ChatOpenAI
  from langchain_core.prompts import PromptTemplate
  from langchain_core.output_parsers import StrOutputParser
  import os
  *# 2. 创建大模型对象 - 使用正确的API端点*
  model = ChatOpenAI(
  model="qwen-max",
  base_url="https://dashscope.aliyuncs.com/compatible-mode/v1", *# 百炼的通用端点*
  api_key=os.getenv("OPENAI_API_KEY"),
  )
  *# 3. 构建提示词模板 + 大模型的链（固化指令流）*
  *# 3-1 构建提示词模板*
  template = PromptTemplate.from_template("我的邻居姓{lastname}，他生了个儿子，给他儿子起个名字")
  *# 3-2 将提示词模板跟大模型组装一条链（使用LCEL管道操作符）*
  chain = template \| model \| StrOutputParser()
  *# 4. 调用链*
  result = chain.invoke({"lastname": "孙"})
  *# 5. 处理结果*
  print(result)
```
---
## 相关笔记
- [[AI大模型开发基础-05-LangChain]] — LangChain Index组件
- [[AI大模型开发基础-01-Python基础]] — Python基础
- MOC: [[MOC-日常学习]]