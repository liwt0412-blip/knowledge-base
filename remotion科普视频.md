---
tags: [Remotion, 视频, 科普, IndexTTS2, TOKEN, 设计系统, 工作流]
date: 2026-06-14
updated: 2026-07-16
---

# Remotion 科普视频制作

> 默认项目：`D:\workspece\GitHup\remotion`  
> 权威执行规范：项目根目录的 `AGENTS.md`。本笔记保存跨对话、跨视频可复用的流程和设计规则；具体组件 API、文件名、坐标和时长以项目代码及 `docs/` 为准。

## 一、当前结论

当前项目已经从“单条 MCP 视频”升级为可复用的 TOKEN 工程科普视频系统，包含：

- 数据驱动的视频计划与手写精细场景双层架构。
- TOKEN 统一品牌片头、人物、角标和片尾。
- Design System V2：设计 Token、运动语言、组合背景、Surface 材质、工程可视化组件。
- 模板场景、手写场景和品牌场景共用的字幕渲染与关键词高亮。
- 多 Composition 统一从默认 Remotion Studio 入口预览。
- 最终音频驱动时长、逐句字幕对齐、预览确认后再渲染和制作发布物料的生产流程。

在当前仓库中新开 Codex 窗口或制作新视频，可以直接复用这套系统。新建独立仓库时不会自动获得这些代码，需要迁移组件或将设计系统封装成公共包。

## 二、不可变的生产原则

1. **先确认脚本，再生成正式旁白**：脚本未锁定前只讨论结构，不批量生成最终音频。
2. **最终旁白是时间轴唯一基准**：场景时长、字幕、动画 Phase 和转场都由最终音频反推。
3. **字幕必须来自最终音频强制对齐**：禁止按场景总时长平均切分。
4. **画面表达工程关系**：优先展示问题、调用链、状态、错误、因果和结论，避免只堆字幕或泛科技装饰。
5. **数据集中维护**：视频计划、场景时长、背景、字幕和视觉描述放在 `src/video-data/`。
6. **先 Studio 预览，再渲染成片**：“预览”只代表 `npm run dev`，不等于导出 MP4。
7. **成片确认后才制作发布物料**：正式封面和发布文案不在预览阶段提前生成。

## 三、当前完整制作流程

```text
需求与素材确认
→ 口播脚本、钩子和场景拆分
→ 用户确认并锁定脚本
→ IndexTTS2 钩子试听
→ 按场景生成最终克隆旁白
→ 测量真实音频时长
→ 对最终旁白做逐句强制对齐
→ 反推场景帧数、字幕和动画触发点
→ 配置视频计划与视觉设计
→ 制作/复用场景组件
→ TypeScript、ESLint、音频和边界检查
→ Remotion Studio 前端预览
→ 用户明确确认渲染
→ 导出横屏 MP4
→ 自动提炼封面变量与提示词
→ 制作横屏/竖屏封面
→ 生成发布文案
```

### 1. 需求与素材确认

开始前确认尚未提供的信息：

- 原始文案或素材、视频主题和核心观点。
- 目标受众、发布平台、目标时长和画面比例。
- 视觉参考或本期需要强调的工程问题。
- 音色参考音频，以及上传第三方服务的明确授权。
- 本期主题标题和输出文件名。

TOKEN 固定介绍、固定结尾和品牌规则默认从项目代码读取，不要求每期重新填写。

### 2. 脚本、钩子和场景拆分

- 将原始素材改成适合口播的脚本，先设计钩子、冲突、解释路径、结论和收尾。
- 每个场景同时标注口播、视觉目标、核心关键词、情绪、工程对象和预期转场。
- 用户确认后锁定脚本；正式旁白生成后，若改文案，需要重新生成对应音频并重新对齐。

### 3. IndexTTS2 克隆旁白

- 默认通过 `gradio_client` 调用 Hugging Face 官方 `IndexTeam/IndexTTS-2-Demo`。
- 优先复用 `$env:USERPROFILE\.cache\huggingface\token` 的本机认证，只验证是否存在和认证是否成功，禁止打印 Token。
- 音色是生物特征数据，向第三方上传前必须获得明确授权。
- 中文内容按 UTF-8 传递，避免 PowerShell 管道导致乱码。
- 先生成钩子短试听，确认音色、节奏和情绪后，再按场景批量生成。
- 按场景配置情绪，不让全片保持完全相同的语气。
- 保留参考音频和原始旁白；克隆结果使用独立、可辨识的文件名。

### 4. 音频驱动时间轴

- 读取最终旁白文件的真实时长。
- 对最终音频做逐句强制对齐，得到字幕开始和结束时间。
- 场景时长 = 最终旁白时长 + 必要的片头/片尾留白。
- 将秒数换算为帧，确定 `Sequence`、字幕、动画 Phase 和转场位置。
- 不在最终旁白生成前锁死视频总时长。

### 5. 当前默认视频结构

```text
Hook
→ TokenBrandIntro（TOKEN 简短自我介绍 + 本期主题）
→ 正文场景
→ 内容总结
→ TokenBrandOutro
```

- 不再默认使用无旁白的固定 4 秒 `TitleCard`。
- 品牌介绍和结尾的时长同样由最终克隆旁白决定。
- TOKEN 人物默认只在品牌介绍、一个关键讲解场景和固定结尾出现，避免全程贴图。
- 全片默认使用低透明度 `TOKEN_` 右上角标识。
- 人物不得遮挡字幕、标题、终端、卡片或关键图表；空间冲突时优先缩小或移动人物。

### 6. 视觉配置与场景制作

每个场景按内容选择视觉表达，而不是只选择装饰背景：

- 协议或调用关系：`CallChain`、`Connector`、数据包。
- 命令、日志或执行过程：`TerminalWindow`、终端型 `Surface`。
- 服务、工具或模块：节点型 `Surface`、状态灯。
- 性能、成功率、延迟或成本：`MetricStrip`。
- 故障、阻断或误区：warning Surface、错误连接、`FocusMask`。
- 结论与最终状态：result Surface、收束型运动语言。

旧场景会自动获得兼容层提供的新背景、GlassUI 修复和统一字幕高亮，但不会自动把原布局替换成调用链、数据包或指标条。想让旧视频完整呈现新版工程视觉，需要逐场景重设计；新视频可直接使用完整系统。

### 7. 检查与 Studio 预览

预览前检查：

- TypeScript 和 ESLint 是否通过。
- Composition 是否全部正常注册。
- 音频文件是否存在、格式能否被浏览器解码、时长是否匹配。
- 字幕时间码、关键词高亮、换行和安全区是否正确。
- 场景帧数、Phase、转场和声音是否同步。
- TOKEN 人物是否完整显示，是否遮挡核心内容或越界。
- 中文字符、终端文本和代码概念是否准确。

运行：

```powershell
cd D:\workspece\GitHup\remotion
npm run dev
```

默认 `npm run dev` 会打开完整项目入口。若只想看 AIServiceCompany，可使用：

```powershell
npm run dev:ai-service
```

### 8. 渲染与发布物料

只有用户明确说“渲染”“导出”“生成成片”或“生成 MP4”后，才执行：

```powershell
npx remotion render <CompositionId> out/<文件名>.mp4
```

MP4 完成并经用户确认后，再制作：

- 横屏封面：1920×1080。
- 竖屏封面：1080×1920，独立排版，不能直接裁切横屏版。
- 发布物料：3 个标题候选、正文短版、正文完整版、话题标签、首评互动引导。

封面主题、冲突、人物动作、情绪、主体和标题默认从最终脚本与成片自动提炼；只有敏感表达、人物形象改变、品牌方向偏离或标题存在重大歧义时才额外确认。

## 四、已经确认并落地的五层设计系统

### 1. Design Tokens

文件：`src/design/tokens.ts`

统一管理颜色、字体、字号、间距、圆角、阴影和画面安全区。新组件不得继续散落创建互相冲突的“差不多”颜色和尺寸。

### 2. Motion Language

文件：`src/design/motion.ts`

五种运动预设：

- `impact`：钩子、碰撞、关键结论。
- `deliberate`：严谨解释和逐步展开。
- `flow`：协议、调用、数据传递。
- `quiet`：辅助信息和低干扰过渡。
- `system`：工程节点、状态切换和运行反馈。

动画只能使用 Remotion 的 `useCurrentFrame()`、`interpolate()` 和 `spring()`，禁止 CSS keyframes、CSS transition 和定时器。

### 3. Composable Background

文件：`src/components/Background.tsx`、`src/design/presets.ts`

新版背景支持：

- 旧的字符串背景：`orb / starfield / hexgrid / waves / stream / clean`。
- 可组合背景配方、场景焦点、镜头漂移和场景间交叉淡化。
- 工程 motif：`blueprint / topology / call-chain / logs`。
- 空气层：`grain / scanlines / dust`。

旧视频仍兼容原 API；新视频优先使用 `backgroundPresets`。

### 4. Surface Material System

文件：`src/components/Surface.tsx`

五类统一面板材质：

- `instrument`：指标、仪表和运行信息。
- `terminal`：命令、日志和执行结果。
- `node`：服务、工具、Agent 和协议节点。
- `warning`：异常、阻断和风险。
- `result`：最终结果和核心结论。

只让当前重点节点高亮，非重点节点保持低亮度，避免所有卡片同时发光。

### 5. Engineering Visuals

文件：`src/components/EngineeringVisuals.tsx`

可复用组件包括：

- `StatusRail`：章节、进度和运行状态。
- `Connector`：调用方向、传输、阻断和错误。
- `CallChain`：Client、MCP、Server、Tool 等连续调用节点。
- 数据包：沿连接关系表达请求与响应流动。
- `MetricStrip`：协议、延迟、成本、成功率等指标。
- `FocusMask`：压暗非重点区域，建立视觉焦点。

## 五、统一字幕与关键词高亮

相关文件：

- `src/components/CaptionOverlayCore.tsx`
- `src/components/CaptionOverlay.tsx`
- `src/components/SubtitleOverlay.tsx`
- `src/design/captions.ts`

当前行为：

- 模板场景、手写场景和 TOKEN 品牌场景共用同一字幕渲染内核。
- `SubtitleOverlay` 保留原调用方式，旧手写场景不用逐个修改即可获得统一高亮。
- 默认高亮 AI、Agent、MCP、API、Prompt、TOKEN、Function Calling、JSON-RPC、Spring AI 等工程术语。
- 支持全局关键词、视频级覆盖和场景级覆盖。
- 英文默认不区分大小写，支持别名和最长优先匹配。
- 可通过 `includeDefaultKeywords={false}` 关闭默认高亮。

## 六、当前项目架构与复用边界

```text
src/
├── Root.tsx                         # 注册所有 Composition
├── compositions/                   # 视频编排、音频、转场和品牌结构
├── video-data/                     # 视频计划、场景时长、字幕、背景和视觉描述
├── scenes/                         # 精细手写场景
├── templates/                      # 数据驱动通用模板
├── design/                         # tokens、motion、presets、caption 关键词
├── components/                     # 背景、GlassUI、Surface、工程组件和字幕
├── brand/                          # TOKEN 文案、人物和品牌场景
└── 配音/                           # 原始与最终克隆旁白
public/
├── assets/brand/token/             # TOKEN 人物透明素材
└── assets/sfx/token/               # 品牌音效母版和来源说明
docs/                               # 设计系统、品牌资产和发布流程
out/                                # 渲染成片
```

### 复用层级

| 使用场景 | 当前复用效果 |
|---|---|
| 当前仓库中新开窗口、新做视频 | 可直接读取 `AGENTS.md` 并复用完整系统 |
| 当前仓库的旧视频 | 自动获得背景兼容、GlassUI 修复和字幕高亮；工程布局需逐场景升级 |
| 当前仓库的新视频 | 可直接使用背景配方、Surface、调用链、数据包、指标条和运动预设 |
| 新建独立仓库 | 需要迁移 `design/`、相关 `components/`、品牌组件及规则，或封装公共包 |

新对话建议直接说明：

> 基于当前 Remotion 的完整 TOKEN 设计系统制作新视频，优先使用 Surface、调用链、数据包、指标条和统一字幕高亮。

## 七、当前 Composition 入口

默认 Studio 当前注册 7 个 Composition：

1. `AIServiceCompany`
2. `MCPExplainer`
3. `MCPExplainerTemplate`
4. `MCPHookStyleTest`
5. `LoopEngineering`
6. `AgentQuadrants`
7. `AgentQuadrantsBranded`

如果 Studio 只能看到 AIServiceCompany，通常是启动了专用入口。停止旧进程后重新运行 `npm run dev`，不要使用 `npm run dev:ai-service`。

## 八、TOKEN 默认视觉与品牌规则

默认方向：**暗色工程现场 + 真实问题冲突 + TOKEN 人物解释**。

视觉优先级：

```text
真实问题冲突
> 工程因果关系
> TOKEN 人物表达
> 科技 UI 装饰
```

- 优先展示调用链、终端状态、代码概念、错误标记和因果关系。
- 深色背景、玻璃 UI、紫青高光和黄红强调色只作为层级辅助。
- 避免通用赛博朋克、泛 AI 海报、过度霓虹和无意义粒子。
- TOKEN 人物使用独立透明 PNG，通过 `src/brand/TokenAvatar.tsx` 复用，禁止运行时从多人设定图裁切。
- 人物姿势、尺寸或坐标变化后，必须在 Studio 检查头发、手臂、手指、服装边缘、字幕安全区和素材遮挡。

## 九、Remotion 工程约束

- 场景根节点使用 `AbsoluteFill`。
- 场景动画使用帧驱动 API，禁止 CSS 动画和计时器。
- 终端文本统一使用 `TypewriterText`。
- 终端窗口统一使用 `TerminalWindow`。
- 卡片入场使用 `AnimatedCard` 或 `FadeSlideUp`。
- 场景标题和大字优先使用 `SectionTitle`。
- 图标与服务徽章使用 `IconBadge`。
- 随机数使用 Remotion `random(null)`，禁止 `Math.random()`。
- Phase 子组件接收偏移后的 `frame`，场景间淡入淡出可用 `interpolate()`。
- 人物、标题和关键图表必须避开字幕安全区。

## 十、已验证案例

### AI 协作四象限

Composition：`AgentQuadrants`、`AgentQuadrantsBranded`

该案例已经验证：

```text
脚本确认
→ 分场景情绪克隆
→ 最终音频驱动时序
→ TOKEN 品牌介绍与片尾
→ 工程化转场音效
→ Studio 预览
→ 成片渲染
→ 发布物料
```

### MCP 讲解视频

Composition：`MCPExplainer`、`MCPExplainerTemplate`、`MCPHookStyleTest`

该案例同时保留精细手写场景和数据驱动模板，可用于比较“定制表现力”和“批量复用效率”。MCP 数据计划已应用新版背景与场景设计预设。

## 十一、权威文档索引

项目内细节以以下文件为准：

- `AGENTS.md`：完整执行规范和默认工作流。
- `docs/design-system-v2.md`：五层设计系统与组件用法。
- `docs/caption-system.md`：统一字幕和关键词覆盖规则。
- `docs/token-brand-assets.md`：TOKEN 人物资产、坐标和遮挡规则。
- `docs/video-publish-package.md`：成片确认后的封面与发布文案流程。

## 相关笔记

- [[🤖 AI Agent/AI协作四象限-让Agent按你的认知地图工作]]
- [[🤖 AI Agent/抖音脚本-MCP协议Agent必知]]
- [[AI Agent总览|🤖 AI Agent 总览]]
- [[MOC-编程相关|💻 编程相关]]


## 十二、知识库创作队列与自动回写

固定创作目录：

```text
D:\KnowledgeBase\小帅的知识库\🎬 Remotion旁白文案
```

以后提出“从知识库继续创作”时，Agent 只扫描该目录，不扫描整个知识库。未完成状态包括：

```text
待创作 / 待审核 / 已确认 / 配音中 / 已配音 / 制作中 / 待预览 / 待渲染 / 待发布
```

默认按 `priority` 和日期选择下一条文案，并读取其 `source` 来源笔记。多个候选无法唯一确定时先展示给用户选择。

完整闭环为：

```text
读取未完成文案与来源笔记
→ 按真实阶段继续制作
→ Studio 预览
→ 用户授权渲染
→ MP4
→ 横竖封面
→ 标题、发布正文、标签、首评
→ 回写全部产物路径
→ 用户确认本期结束
→ status: 已完成
```

只有成片、发布物料和路径回写全部完成，且用户确认结束后，才能标记 `已完成`。暂停、失败或缺少任一默认交付物时保持真实状态，并填写 `blocked_reason` 或 `next_action`。

队列入口：[[🎬 Remotion旁白文案/00-Remotion旁白文案MOC]]  
新文案入口：[[🎬 Remotion旁白文案/模板-Remotion旁白文案]]



## 十三、原始素材转 TOKEN 旁白

从知识库原始素材生成可用旁白时，默认先读取：

- [[🤖 AI Agent/Hermes Agent技能库/token-人味儿写作]]
- [[🤖 AI Agent/Hermes Agent技能库/token-事后检查清单]]

创作链路：

```text
读取来源笔记全文
→ 区分事实、来源观点、TOKEN 判断和未知项
→ 提炼一句话核心观点
→ 共鸣钩子
→ 问题 → 方案 → 原理 → 限制/判断 → 具体结论
→ 接入 TOKEN 品牌介绍与固定结尾
→ 对整篇新稿执行事后检查
→ 保存为 status: 待审核
→ 用户确认后进入正式配音
```

写作要求：干净、直接、少修饰；不编经历，不写宏大开头、宣传腔、万能展望和硬造金句。可以保留技术时间线、版本对比和表格结构，但最终旁白必须自然、能说出口。外部文档负责事实骨架，TOKEN 的转述负责把问题、机制和判断讲清楚。



## 十四、场景语义背景策略（已落地）

新视频不再默认使用星空或大光斑作为正文背景。背景按场景内容自动选择：

```text
钩子 → starfield + topology
TOKEN 品牌过渡 → orb + blueprint
协议/调用 → stream + call-chain
系统/工具 → hexgrid + topology
对比/决策 → blueprint 工程边界
故障/风险 → logs + warning focus
总结/结果 → clean + restrained blueprint
普通正文 → clean 工程画布
```

项目实现位于 `src/design/background-policy.ts`，详细规则见 `docs/background-policy.md`。数据驱动场景中的旧字符串会按场景类型自动升级；手写 Composition 使用 `backgroundForRole()`。完整对象背景配方仍可作为明确的自定义覆盖。

当前已接入 MCP、LoopEngineering、AIServiceCompany、AgentQuadrants 及品牌版本。`starfield` 和 `orb` 只承担钩子或品牌过渡，不再作为正文默认策略。



## 16. 默认场景系统已落地（2026-07-16）

Remotion 项目不再只是“具备组件”，而是已经把组件接入默认生产链路。

### 自动生效

- 场景角色自动决定语义背景、Surface 材质、运动语言、强调色与状态。
- 数据驱动模板自动使用状态轨、调用链、节点、数据包和指标条表达工程因果关系。
- `AnimatedCard`、`FadeSlideUp`、`SectionTitle` 在场景上下文内自动消费统一设计策略。
- 主要 Composition 默认启用 TOKEN 视觉外壳、右上角角标和统一转场。
- 模板、品牌场景及主要内容框使用统一安全区，预留字幕位置。
- 字幕关键词高亮继续通过 `captionKeywords` 配置，字幕时间以最终旁白强制对齐为准。

### 新视频复用方式

以后新开对话制作视频时，先读取项目 `AGENTS.md`，再按以下链路执行：

`知识库未完成文档 → TOKEN 写作规则 → 脚本确认 → 克隆旁白 → 强制对齐字幕 → 场景计划 → 默认场景系统 → Studio 预览 → 用户授权渲染 → 发布物料 → 知识库标记完成`

正文场景只需提供场景类型、视觉数据、字幕和必要的设计覆盖；其余由 `src/design/scene-policy.ts` 自动解析。完整说明见项目 `docs/default-scene-system.md`。

### 必须显式完成的部分

- TOKEN 视觉外壳能自动提供角标，但带旁白的品牌介绍和品牌结尾仍要显式加入场景计划。
- 品牌场景时长必须以最终克隆旁白为准，不能写死。
- Studio 视觉验收不能自动省略，必须检查字幕安全区、人物遮挡、元素越界和转场音频解码。
- 用户只说“预览”时不得渲染 MP4。

### 默认映射

| 场景角色 | 默认 Surface | 默认动作 | 默认工程视觉 |
|---|---|---|---|
| hook | warning | impact | 状态 + 指标 |
| brand | result | deliberate | 品牌状态 |
| protocol | terminal | flow | 调用链 |
| system | node | system | 节点图 + 指标 |
| decision | instrument | deliberate | 对比数据包 |
| failure | warning | impact | 阻断连接 |
| conclusion | result | quiet | 结果指标 |
| neutral | instrument | deliberate | 状态轨 |

### Hook 后固定震撼转场（2026-07-16）

- `Hook → TokenBrandIntro/titleCard` 现在是项目固定转场，不再由单个视频临时添加。
- 统一通过 `src/components/SceneTransitions.tsx` 的 `variant: "hook-brand"` 启用。
- 固定复用 `src/配音/震撼.mp3`，并包含提前 12 帧进入、冲击闪光、扩散环和旁白下淡出。
- 普通场景仍使用标准工程扫光音效。
- 禁止在品牌场景内部再次播放同一震撼音效，避免声音重复叠加。

### Hook 固定转场音频隔离规则（修订）

- 固定资产改为 `src/配音/shared/hook-brand-impact-v1.mp3`。
- 该资产保留原冲击峰值音量，长度约 0.5 秒。
- Hook 场景末尾必须预留至少 15 帧无旁白区；冲击音效只在这 15 帧播放。
- 音频在 `TokenBrandIntro` 开始帧准确结束，禁止与品牌旁白重叠；视觉闪光和扩散环可以继续跨场景。
- 以后禁止用“先让音效压住人声、再降低音量”的方式处理该转场，也禁止在品牌场景内部重复播放震撼音效。

### Hook 固定震撼转场最终规则（0–2.5 秒）

- 固定顺序：`Hook 完全结束 → 75 帧独立震撼转场 → TokenBrandIntro/titleCard`。
- 转场直接使用原始 `src/配音/震撼.mp3` 的 0–2.5 秒，保持当前峰值音量。
- 品牌场景和品牌旁白必须等 75 帧音效完全结束后再开始，音频重叠固定为 0 帧。
- 时间轴辅助函数会自动把后续场景起始帧和 Composition 总时长增加 75 帧。
- 禁止在品牌场景内部重复播放震撼音效。
