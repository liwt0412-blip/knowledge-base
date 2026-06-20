---
tags: [AI, Agent, MCP, 协议, 抖音, 口播, 脚本, Remotion]
date: 2026-06-14
sources:
  - Agent知识: 推理+系统讲解
  - SpringAI高级: part3-SpringAI-MCP应用
confidence: high
---

# 抖音口播脚本：Agent 必须懂的 MCP 协议

**时长：** 约 76 秒
**格式：** Remotion 动画 + 配音，不露脸不实拍
**风格：** 聊天式科普，Kurzgesagt 配色

---

## 钩子（~8s / 240帧）

### 文案

你有没有想过，Agent 为什么能直接操作你的电脑？
打开浏览器、读你数据库、查你文件——它凭什么？
这里就不得不说现在 Agent 圈里最火的一个东西：MCP 协议。

### 画面

深色背景上细小光点粒子缓慢漂浮（starfield 背景）。

文字弹出效果：
- "打开浏览器 ✓" 从画面外弹入，带 overshoot 回弹（spring），同时画面轻微震动一下（translateX ±5px 快速来回）
- "读你数据库 ✓" 同上，从另一侧弹入
- "查你文件 ✓" 同上
- "凭什么？" 三行文字同时下沉消失，像被按进水里，带 ripple 波纹扩散
- "MCP" 三个字母逐个砸到画面中央（缩放入场 + 落地震动 + 光晕脉冲），每个字母落地时背景粒子被震散一圈

---

## 一、MCP 是什么（~18s / 540帧）

### 文案

MCP，全称 Model Context Protocol，模型上下文协议。
Anthropic——做 Claude 的那家公司——2024 年 11 月推出来的。

它干的就一件事：定一个标准，让大模型和外部工具之间说同一种话。
打个比方，它就是大模型世界的 Type-C 接口。鼠标、键盘、U 盘，以前各插各的口，Type-C 出来之后一个口全搞定。MCP 也是这个意思。

架构也简单。两方：MCP Client 是你这边的 Agent，MCP Server 是工具那边。
Client 问 Server "你有什么工具"，Server 说"我有这些，参数长这样"，然后 Agent 直接调。

### 画面

1. 全称浮现：字母像打字机逐个打出 "MCP = Model Context Protocol"，带光标闪烁。光标消失的同一帧，"Anthropic · 2024.11" 从上方掉落定住（spring）

2. 接口对比：
   - 左边：一堆不同形状接口从四面八方飞入堆成一团（方的、圆的、扁的），歪歪扭扭
   - 中间：Type-C 图标从中心生长出来（stroke-dasharray 描边动画 + 填充渐显）
   - 右边：杂乱接口被"吸"进 Type-C，每个接口依次缩小、旋转、飞入，像被磁铁吸走

3. 架构图：
   - Client 方块和 Server 方块从画面两侧滑入
   - 中间 JSON-RPC 箭头上粒子流持续流动
   - "有什么工具？" 气泡从 Client 冒出来，弹一下
   - Server 回复气泡弹回来

---

## 二、MCP 能干什么（~22s / 660帧）

### 文案

说两个我实际跑过的例子。

第一个，浏览器控制。我们给 Agent 接了一个叫 playwright 的 MCP Server，
然后问他：打开传智播客官网，总结一下内容。
他真的自己开了浏览器，访问网站，读完，把内容总结出来了。
代码一行没写，就配了一个 Server 地址。

第二个，IP 归属地查询。接的是高德地图的 MCP Server。
扔一个 IP 地址过去，他调高德的接口，查出所在地，返回给你。

你看这两个例子的共同点：工具不是我写的，也不是 Java 写的。
但因为他们遵循了 MCP 协议，我的 Spring AI 项目直接用就行。

### 画面

1. 浏览器控制：
   - 画面切为 IDE 风格，代码编辑器背景有代码行自动滚动效果（模糊绿色字符向下流动）
   - "打开传智播客官网，总结内容" 像终端打字逐字出现
   - 浏览器窗口从代码区右侧弹开（scale 0→1 + spring），网页内容从上到下滚入
   - 网页缩小，文字摘要逐行淡入
   - 底部标注从画面底部滑上，弹一下停住："playwright-mcp-server，一行安装，一行配置"

2. IP 归属地：
   - 输入框文字逐字打出
   - 地图标记（pin）从上方掉落钉在画面中
   - 钉住瞬间地图底色从灰变彩色，定位点脉冲一圈波纹
   - "所在地：北京市" 从 pin 旁弹出（scale 1→1.3→1，spring）
   - 底部标注："高德地图 MCP Server"

3. 对比汇总：
   - playwright（Node.js 图标）和高德（Go 图标）分列左右
   - 中间 MCP 协议层是发光圆环，持续脉冲
   - 两个图标同时向环发射光线，汇聚后射向 Spring AI（Java 图标）

---

## 三、MCP 跟 Function Calling 的区别（~20s / 600帧）

### 文案

很多人听到这会说：这不就是 Function Calling 吗？
对，底层确实是 Function Calling。但区别不在机制，在标准。

Function Calling 是 OpenAI 定义的一套调用格式。
你在 Spring AI 里写了一个 Tool，Python 的项目用不了。因为格式不通用，语言绑死了。

MCP 不一样。他的 Server 用什么语言写的无所谓——Node.js 写的 playwright、Go 写的高德、Java 写的天气——只要遵循 MCP 协议，任何 Agent 框架都能调。

所以一句话：Function Calling 是工具调用的机制，MCP 是工具调用的标准。
一个管"怎么调"，一个管"谁都能调"。

### 画面

1. 弹幕式质疑：
   - "这不就是 Function Calling 吗？" 以对话框形式从右下角弹出（模拟弹幕），字体偏小偏灰，弹完后缩回去消失

2. Function Calling 问题：
   - Java Tool → Spring AI 箭头绿色顺畅
   - 往 Python 项目的箭头撞上红墙碎裂（粒子炸开），红墙上打出 "不通用，需重写"

3. MCP 解决方案：
   - Node.js、Go、Java 三个 Server 图标从三个方向旋转飞入
   - 汇聚到中间 MCP 协议层（发光六边形或圆形）
   - 从 MCP 层延伸三根光线，分别连接 Spring AI（绿勾）、LangChain（绿勾）、Claude Desktop（绿勾）
   - 三个勾用 SVG path 手写笔画动画描出来

4. 总结定格：
   - 左边 "Function Calling" 放大，下面打出 "机制"（手写描边）
   - 右边 "MCP" 放大，下面打出 "标准"（手写描边）
   - 底部文字 "一个管怎么调，一个管谁都能调" 逐字依次亮起

---

## 收尾（~8s / 240帧）

### 文案

你可以在 mcp.so 这些网站上找到现成的 MCP Server，浏览器、数据库、文件系统、GitHub、Slack，什么都有。
你想让 Agent 有更多能力，就用更多的 MCP 服务就行。

### 画面

1. mcp.so 界面：
   - 不是截图，卡片从画面深处飞出——浏览器、数据库、文件系统、GitHub、Slack
   - 像牌一样依次展开成扇形或网格
   - 每张卡片飞到位时有旋转+缩放过渡，停下后微微浮动（hover 动画）

2. Agent 汇聚：
   - Agent 图标在画面中央
   - 周围卡片一张一张飞入 Agent（缩小、旋转、像被吸进去）
   - 每并入一张，Agent 图标亮一圈光晕，颜色从暗紫渐变到亮蓝
   - 最后 Agent 整体脉冲一次，光晕散开

3. 定格字幕：
   - 画面底部从暗到亮浮现 "mcp.so — 找到你需要的 MCP 服务"
   - 文字出现后光标闪烁三下，消失

---

## 全局特效

以下效果贯穿全片，不单独写入每段：

1. **背景**：全程 starfield 或 orb 背景，粒子持续缓慢移动
2. **转场**：场景之间用一帧极短白闪或粒子聚散过渡
3. **图标**：所有工具图标统一线性 SVG，配色从 Kurzgesagt 色表取（紫 #6c5ce7、青 #4ecdc4、黄 #ffe66d、红 #ff6b6b、白 #ffffff、灰 #8892b0、底 #0a0a1a）

---

## 相关笔记

- [[AI Agent总览|🤖 AI Agent 总览]]
- [[MOC-编程相关]]
- [[remotion科普视频]]
- [[../SpringAI+AIGC应用/part3-SpringAI高级|part3-SpringAI高级]]
