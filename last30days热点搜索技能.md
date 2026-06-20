---
tags: [Claude, Skill, 搜索, 研究, Reddit, 社交媒体]
date: 2026-06-14
---

# /last30days 热点搜索技能

## 一句话说明

AI 代理驱动的多平台搜索引擎，检索 **最近 30 天** Reddit、X、YouTube、Hacker News、Polymarket、GitHub 等平台上的真实用户讨论，按**用户参与度**（点赞、转发、真实做市资金）打分排序，由 AI 综合成一份简报。

> 不是 SEO 排名，是社交相关性排名。

## 已安装信息

- **安装路径**：`~/.agents/skills/last30days/`
- **引擎路径**：`~/.agents/skills/last30days/scripts/last30days.py`
- **Python**：3.12.4
- **斜杠命令**：`/last30days <话题>`

## 零配置可用数据源

| 数据源 | 说明 |
|--------|------|
| Reddit | 帖子 + 高赞评论，带点赞数，免费公开 JSON |
| Hacker News | 开发者社区共识，点数 + 评论数 |
| Polymarket | 真实资金做市赔率，不是观点是概率 |
| GitHub | 仓库 star 数、issue、PR 讨论 |
| WebSearch | Claude Code 内置网页搜索 |

## 需要 API Key 解锁的数据源

| 数据源 | 所需 Key |
|--------|----------|
| X / Twitter | `AUTH_TOKEN` + `CT0`（浏览器登录）或 `XAI_API_KEY` |
| YouTube | `SCRAPECREATORS_API_KEY` |
| TikTok | `SCRAPECREATORS_API_KEY` |
| Instagram Reels | `SCRAPECREATORS_API_KEY` |
| Threads | `SCRAPECREATORS_API_KEY` |
| Bluesky | `BSKY_HANDLE` + `BSKY_APP_PASSWORD` |
| Perplexity Sonar | `OPENROUTER_API_KEY` |

## 使用示例

```bash
# 查人（会议前快速了解对方）
/last30days Peter Steinberger

# 对比工具
/last30days OpenClaw vs Hermes vs Paperclip

# 出行前调研
/last30days Universal Epic Universe

# 学习新技术
/last30days Nano Banana Pro prompting

# 跟踪热点事件
/last30days Iran vs USA

# 输出可分享的 HTML 简报
/last30days OpenClaw --emit=html
```

## 实际适用的场景

- **见客户 / 面试前**：查出对方最近 30 天的推文、演讲、GitHub 动态
- **技术选型**：对比几个工具，看社区真实评价，而不是官网宣传
- **追热点**：某事件刚出来，Reddit 和 X 上第一时间怎么说的
- **出行前**：景点/酒店社区真实反馈，不是小红书精修图
- **快速学习**：一个新技术，社区总结了哪些最佳实践

## 核心原理

1. 你输入话题
2. 引擎并行搜索 Reddit、HN、Polymarket、GitHub（免费）等平台
3. 按**用户参与度**排序（不是 SEO）
4. AI 代理综合成一份带引用的简报

v3 版本新增：智能搜索（自动解析 X 账号、Reddit 子版块、YouTube 频道）、跨平台聚类合并、对比模式、ELI5 大白话模式。

## 相关笔记

- [[MOC-工具运维|🛠️ 工具运维]]
- [[MOC-编程相关|💻 编程相关]]
- [[remotion科普视频|Remotion 科普视频]]
