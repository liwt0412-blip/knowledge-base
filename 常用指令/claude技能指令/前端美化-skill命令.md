---
tags: [前端, 工具]
date: 2026-05-27
---
Taste-Skill 可用命令
=====================================

代码类技能（输出代码）
-------------------------------------

/taste-skill
  默认主技能 (v2)，根据需求推断设计语言，可调三个旋钮：VARIANCE / MOTION / DENSITY。
  适用：落地页、作品集、前端重设计。

/taste-skill-v1
  v1 原版，行为稳定不变。如果 v2 在你的项目里出问题，用这个回退。

/gpt-tasteskill
  GPT / Codex 的严格版，布局变化更大，GSAP 动效更强，反模板化更激进。

/image-to-code-skill
  图片→分析→代码流水线。先生成参考图，分析，再按图实现前端。

/redesign-skill
  重设计现有项目。先审计 UI 问题（布局/间距/层级/样式），再修复。

/soft-skill
  高端柔和风格：大量留白、低对比度、spring 弹性动效、精品字体。
  适合：奢侈品牌、生活美学、高端消费品。

/minimalist-skill
  极简编辑风：Notion / Linear 那种克制、干净的界面。
  适合：工具型产品、SaaS、笔记类应用。

/brutalist-skill
  工业粗野主义：硬朗机械感、Swiss 字体、强对比、实验性布局。
  适合：设计师作品集、先锋品牌、创意机构。

/output-skill
  防截断：强制模型输出完整代码，禁止 "// ..." 占位符注释。

/stitch-skill
  Google Stitch 兼容规则，支持导出 DESIGN.md 格式。


图片生成技能（只出参考图，不出代码）
-------------------------------------

/imagegen-frontend-web
  生成网页设计参考图：Hero、落地页、多段式布局，强调字体/间距/艺术方向。

/imagegen-frontend-mobile
  生成移动端设计参考图：iOS / Android 界面、流程、mockup 套图。

/brandkit
  生成品牌板：Logo 方向、调色板、字体搭配、品牌应用示例。


三个可调旋钮（仅 /taste-skill v2）
=====================================
安装后编辑 .claude/skills/taste-skill/SKILL.md 顶部数值：

  DESIGN_VARIANCE  1-10   布局实验性   (1=保守居中  10=大胆不对称)
  MOTION_INTENSITY 1-10   动效程度     (1=仅hover  10=滚动+磁吸)
  VISUAL_DENSITY   1-10   信息密度     (1=大量留白  10=密集仪表盘)
