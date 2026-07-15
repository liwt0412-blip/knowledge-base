---
tags: [Remotion, 视频, 科普, IndexTTS2, 工作流]
date: 2026-06-14
updated: 2026-07-14
---

# Remotion 科普视频制作

> 默认项目：`D:\workspece\GitHup\remotion`
> 权威执行规范：项目根目录的 `AGENTS.md`。本笔记记录跨项目可复用的方法，具体组件、文件名和时长以项目代码为准。

## 一、核心原则

1. **先定脚本，再生成旁白**：口播没有确认前，不生成正式音频。
2. **最终音频是时间轴唯一基准**：场景时长、字幕和动画触发点由最终克隆音频反推，不能在配音前锁死。
3. **字幕来自最终音频对齐**：逐句强制对齐，禁止按场景总时长平均分配。
4. **数据驱动**：场景时长、背景、字幕和视觉描述集中维护在 `src/video-data/`。
5. **先预览后成片**：先确认声音和短预览，再渲染完整 MP4。

## 二、开始制作前需要的信息

当提出“根据某份文案制作视频”时，先确认尚未提供的内容：

- 原始文案或素材
- 主题和核心观点
- 目标受众与发布平台
- 目标时长和画面比例
- 视觉风格或参考案例
- 音色参考音频及上传第三方服务的明确授权
- 钩子后固定标题场景的文案
- 输出文件名

## 三、标准生产流程

### 1. 设计并确认脚本

- 把原始文案改造成口播稿，先设计钩子、正文结构、转折和收尾。
- 按语义拆分场景，并标注每个场景的视觉目标、关键词和情绪。
- 用户确认口播后锁定脚本，再进入语音生成。

### 2. 使用 IndexTTS2 克隆音色

本机已经验证成功的默认方式：

- 通过 `gradio_client` 调用 Hugging Face 官方 `IndexTeam/IndexTTS-2-Demo` Space。
- 优先复用 `$env:USERPROFILE\.cache\huggingface\token` 中的本机认证；只验证认证是否成功，不打印或记录 Token 内容。
- 上传参考音频前必须获得明确授权，因为音色属于生物特征数据。
- 中文文案使用 UTF-8 传递，避免 PowerShell 管道造成乱码。
- 按场景设置情绪向量和语气，不使用全片完全相同的情绪参数。
- 先生成钩子试听，确认音色、节奏和情绪后再批量生成。
- 保留原始音频；克隆音频使用 `*-clone.wav` 等独立名称。

### 3. 用最终音频建立时间轴

- 使用最终克隆音频测量每个场景的真实时长。
- 对最终音频做逐句强制对齐，生成字幕的开始帧和结束帧。
- 场景时长 = 旁白真实时长 + 必要的片头/片尾留白。
- 动画 Phase、字幕、转场和 Sequence 帧数都以此时间轴为准。

### 4. 生成场景与固定标题页

默认结构：

```text
Hook → TitleCard → 正文场景 → Outro
```

- 钩子后插入约 4 秒的通用标题场景。
- 标题页默认使用 `TitleCard`、`orb` 背景和统一的冲击型转场音效。
- 标题从视频计划数据读取，标题页不承载正文旁白。
- 正文场景根据语义选择终端、卡片、对比、流程图或总结模板，避免只把字幕堆到画面上。

### 5. 音效与混音

- 场景转场保持同一声音风格，关键转场使用更有冲击力的 whoosh/impact。
- 音效出现时不得遮盖旁白，必要时降低音量或避开人声重音。
- 正文节奏由旁白主导，音效只负责强调结构变化。

### 6. 检查、预览和渲染

检查内容：

- TypeScript 和 ESLint
- 音频文件是否存在、时长是否匹配
- 字幕是否越界或抢拍
- 场景帧数和转场位置
- 中文字符是否正常
- 短预览中的音色、节奏、字幕和转场

用户确认预览后再渲染完整视频。

## 四、当前项目架构

```text
src/
├── Root.tsx                         # 注册 Composition
├── compositions/                   # 视频编排与音频、转场
├── video-data/                     # 场景计划、时长、字幕、背景、视觉描述
├── scenes/                         # 精细手写场景
├── templates/                      # 数据驱动通用模板
├── components/                     # Background、TitleCard、字幕和 GlassUI
└── 配音/                           # 原始与克隆旁白
public/
└── covers/                         # 视频封面
docs/                               # 发布文案和项目说明
out/                                # 渲染成片
```

重要变化：

- Composition 总时长由视频计划自动计算，不再固定写死在 `Root.tsx`。
- 背景在对应的 `src/video-data/*.ts` 场景 `background` 字段中选择，不直接修改 `Background.tsx`。
- 每条视频可以注册独立 Composition ID，例如 `AgentQuadrants`。

## 五、常用命令

```powershell
cd D:\workspece\GitHup\remotion
npm run dev
```

打开 Remotion Studio 预览后，渲染指定 Composition：

```powershell
npx remotion render AgentQuadrants out/AgentQuadrants.mp4
```

通用形式：

```powershell
npx remotion render <CompositionId> out/<文件名>.mp4
```

如果 `npm run dev` 因端口冲突失败，先检查并结束残留的 `remotion studio` 进程。

## 六、Remotion 动画约束

- 所有动画使用 `useCurrentFrame()`、`interpolate()`、`spring()`。
- 禁止 CSS animation、CSS transition 和定时器驱动动画。
- 场景根节点使用 `AbsoluteFill`。
- 随机数使用 Remotion 的 `random(null)`，避免逐帧不一致。
- 终端、卡片、标题和图标优先复用项目组件，不在场景中重复造轮子。
- 详细组件规范、Phase 规则和视觉参数以项目 `AGENTS.md` 为准。

## 七、已验证案例：AI 协作四象限

Composition ID：`AgentQuadrants`

项目内产物：

- 视频数据与口播字幕：`src/video-data/agent-quadrants.ts`
- Composition：`src/compositions/AgentQuadrantsComposition.tsx`
- 克隆旁白：`src/配音/agent-quadrants/*-clone.wav`
- 封面：`public/covers/agent-quadrants-cover.png`
- 发布文案：`docs/agent-quadrants-publish-copy.md`
- 最终成片：`out/AgentQuadrants.mp4`

该案例验证了“脚本确认 → 分场景情绪克隆 → 最终音频驱动时序 → 固定标题页 → 转场音效 → 预览 → 成片”的完整链路。

## 相关笔记

- [[🤖 AI Agent/AI协作四象限-让Agent按你的认知地图工作]]
- [[🤖 AI Agent/抖音脚本-MCP协议Agent必知]]
- [[AI Agent总览|🤖 AI Agent 总览]]
- [[MOC-编程相关|💻 编程相关]]
