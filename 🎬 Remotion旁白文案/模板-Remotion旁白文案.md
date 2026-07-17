---
title: Remotion 旁白文案模板
tags:
  - Remotion
  - 旁白文案
  - 模板
status: template
priority: normal
version: v0.1
writing_style: TOKEN人味儿写作
writing_review: pending
date:
updated:
source: "[[来源笔记]]"
target: 抖音
estimated_duration:
aspect_ratio: "16:9"
composition_id:
video_output:
cover_horizontal:
cover_vertical:
publish_copy:
completed_at:
waived_deliverables: []
blocked_reason:
next_action:
---

# 《视频标题》

> [!note] 状态填写
> 新选题使用 `待创作`；形成旁白草稿后改为 `待审核`。不要保留 `template`，否则不会进入创作队列。

## 基本信息

- 状态流转：待创作 / 待审核 / 已确认 / 配音中 / 已配音 / 制作中 / 待预览 / 待渲染 / 待发布 / 已完成
- 版本：v0.1
- 来源笔记：[[来源笔记]]
- 目标平台：抖音
- 目标时长：约 X 秒
- 视频比例：横屏 16:9
- Remotion Composition：待定
- 下一步：补充在 YAML `next_action`

## 核心观点

用一句话写清楚这条视频到底想让观众记住什么。

## TOKEN 写作转换

创作前完整读取：

- [[🤖 AI Agent/Hermes Agent技能库/token-人味儿写作]]
- [[🤖 AI Agent/Hermes Agent技能库/token-事后检查清单]]

- [ ] 已读取来源笔记全文
- [ ] 已区分事实、来源观点、TOKEN 判断和未知项
- [ ] 开头使用真实问题或共鸣，没有编造亲身经历
- [ ] 正文按“问题 → 方案 → 原理 → 限制/判断”推进
- [ ] 文案干净直接，没有宣传腔、意义拔高和硬造金句
- [ ] 已对整篇原创稿执行事后检查
- [ ] 已设置 `writing_review: passed`
## 旁白结构

### Hook

从观众遇到过的问题或一个具体工程冲突切入。

### TOKEN 品牌介绍

使用项目当前确认版本；每期只替换主题，不在单条文案里复制维护固定内容。

### 正文

按“问题 → 解决方式 → 背后机制 → 限制或判断”推进。每段只承担一个观点，并给出具体工程对象或例子。

### 内容总结

收束本期核心判断，不替代 TOKEN 固定结尾。

### TOKEN 固定结尾

从项目 `src/brand/token.ts` 读取，不在此处分散维护。

## 场景拆分草案

| 场景 | 旁白目的 | 关键词 | 工程画面目标 | 预计时长 |
|---|---|---|---|---:|
| Hook | 抓住注意力 |  | 真实问题冲突 | 秒 |
| TokenBrandIntro | 介绍 TOKEN 与本期主题 | TOKEN | 品牌过渡 | 秒 |
| 正文 1 | 解释问题 |  | 调用链/终端/节点 | 秒 |
| 正文 2 | 给出机制或标准 |  | Surface/数据包/指标条 | 秒 |
| 正文 3 | 说明限制 |  | warning/FocusMask | 秒 |
| 内容总结 | 收束观点 |  | result Surface | 秒 |
| TokenBrandOutro | 固定收尾 | TOKEN | 品牌结尾 | 秒 |

## 事实与审核清单

- [ ] 外部来源已记录
- [ ] 数字和时间范围有来源
- [ ] 推测已标注为判断或观点
- [ ] 没有把绝对判断写成事实
- [ ] 用户已确认旁白
- [ ] 音色上传已获得明确授权
- [ ] 最终旁白时长已测量
- [ ] 字幕已根据最终音频强制对齐
- [ ] Studio 预览已确认
- [ ] 用户已明确授权渲染

## 制作产物

> 在制作过程中逐项回写。路径不存在时不要填写完成状态。

- Composition ID：
- 最终 MP4：
- 横屏封面：
- 竖屏封面：
- 发布文案：
- 最终确认日期：
- 放弃的交付物及原因：无

## 发布物料

### 标题候选

1.
2.
3.

### 发布正文短版



### 发布正文完整版



### 话题标签



### 首评互动引导



## 版本记录

| 版本 | 日期 | 修改内容 | 状态 |
|---|---|---|---|
| v0.1 |  | 初稿 | 待审核 |

