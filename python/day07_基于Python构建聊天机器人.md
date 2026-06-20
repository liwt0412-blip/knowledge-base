---
tags: [Python]
date: 2026-06-10
---

# day07_基于Python构建聊天机器⼈


## 项⽬基本概述

### 后端模型：利⽤ Ollama 平台的 Qwen 模型，该模型具备出⾊的⾃然语⾔处理能⼒，能够理解和⽣成⾃然语⾔⽂本，为聊天机器⼈提供核⼼的对话处理功能。

### 前端界⾯：采⽤ Streamlit 框架搭建⽤⼾界⾯，Streamlit 是⼀个简单易⽤的 Python 库，能够快速创建美观、交互式的 Web 应⽤，使⽤⼾能够通过⽹⻚与聊天机器⼈进⾏实时对话。


## 项⽬的运⾏环境

### 安装ollama软件并且本地部署⼤模型

###  安装python解释器和pycharm开发⼯具

### 在python解释器上安装streamlit和ollama库

## 项⽬前端⻚⾯----Streamlit

### Streamlit 是⼀个开源 Python 库。它旨在让数据科学家和⼯程师能够以最少的代码和配置，将他们的数据分析和模型展⽰转化为交互式的 Web 应⽤。Streamlit 的设计⽬标是简单易⽤，同时保持⾼度的灵活性和可定制性。 官⽹地址: https://streamlit.io

### Streamlit常⻅组件

#### Streamlit 提供了许多内置组件，⽤于创建交互式界⾯
• ⽂本和标题：st.write(), st.title(), st.header(), st.subheader()等
• 输⼊控件：st.text_input(), st.slider(), st.selectbox(), st.checkbox(), st.button()等
• 显⽰数据：st.dataframe(), st.table(), st.json()等
• 显⽰图表：st.pyplot(), st.altair_chart(), st.bokeh_chart(), st.plotly_chart()等
• 布局：st.sidebar(), st.columns(), st.expander()等

##### https://docs.streamlit.io/develop/api-reference

### Streamlit⼊⻔案例

#### 在pythonchar中用命令行打开 streamlit run 文件名  TAB自动补齐

## 4.项⽬后端模型对话

### 基于Ollama模块调⽤⼤模型

#### 代码块
# 1.导包
# 注意: 必须提前安装ollama: pip install ollama
import ollama
# 2.ollama调⽤本地⼤模型
# ⽼版本ollama默认直接访问: http://127.0.0.1:11434/
# 新版本需要创建客⼾端对象
new_ollama = ollama.Client(host="http://127.0.0.1:11434")
# 发送请求获取响应
result = new_ollama.chat(
model="qwen2:0.5b",
messages=[
{"role": "user", "content": "给我讲⼀个笑话"}
]
)
# 解析响应结果
print(result.message.content)


### 抽取Ollama调⽤模型⼯具类

## 相关笔记

- [[python/Python笔记总览|Python笔记总览]]


- [[MOC-日常学习]]
