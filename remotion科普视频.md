---
tags: [Remotion, 视频, 科普, Skill, 工作流]
date: 2026-06-14
---

# Remotion 科普视频制作

## 已安装的 Skill

**remotion-best-practices**（官方）
- 路径：`D:\.agents\skills\remotion-best-practices\`
- 71 条规则，Claude Code 启动时自动加载
- 内容：`useCurrentFrame()`、`interpolate()`、`spring()`、`<Sequence>`、`<Composition>` 等 API 的正确用法

## 核心约束（Skill 规定的）

1. **禁止 CSS animation / transition** — 所有动画必须用 `useCurrentFrame()` + `interpolate()` 驱动
2. **禁止 Tailwind 动画类名** — 不会正确渲染
3. **静态资源放 `public/`** — 用 `staticFile()` 引用
4. **组件化思维** — 每个场景拆成独立组件，用 `<Sequence>` 控制时序
5. **不在 prompt 里写视频** — prompt 只存引用，真正重复上下文放文件里

## 项目模板路径

`D:\workspece\GitHup\remotion\`

```
remotion/
├── src/
│   ├── Root.tsx              ← 注册 Composition（改时长、帧率在这里）
│   ├── Composition.tsx        ← 编排所有场景的 Sequence
│   ├── components/
│   │   └── Background.tsx     ← 6 种背景风格（orb/starfield/hexgrid/waves/stream/clean）
│   └── scenes/
│       ├── HookScene.tsx      ← 开场钩子
│       ├── ProblemScene.tsx   ← 问题场景
│       ├── USBAnalogyScene.tsx
│       ├── ArchitectureScene.tsx
│       ├── PrimitivesScene.tsx
│       ├── ComparisonScene.tsx
│       ├── ExampleScene.tsx
│       └── OutroScene.tsx     ← 结尾总结
├── public/                   ← 图片、音频、视频素材
├── package.json
└── remotion.config.ts
```

## 使用流程

### 1. 启动预览
```bash
cd D:\workspece\GitHup\remotion
npm run dev
# → http://localhost:3000
```

### 2. 让 AI 写视频
直接用自然语言描述，例如：
> "帮我做一个 3 分钟的科普视频，讲 XXX，1920×1080，30fps，Kurzgesagt 风格，包含：标题场景、概念讲解、图解对比、结尾总结"

### 3. 渲染导出
```bash
npx remotion render MCPExplainer out/视频名.mp4 --crf=18
```

## 背景切换

编辑 `src/components/Background.tsx` 第 167 行，6 种可选：

| 名称 | 风格 |
|------|------|
| `orb` | 彩色光斑漂浮 |
| `starfield` | 粒子星空 |
| `hexgrid` | 六边形几何网格 |
| `waves` | 流动波浪 |
| `stream` | 粒子流线 |
| `clean` | 极简渐变 |

## 关键数字

- 分辨率：1920×1080
- 帧率：30fps
- 30fps × 60秒 = 1800帧/分钟
- 3分钟视频 = 5400帧
- Composition 时长写在 `Root.tsx` 的 `durationInFrames` 里

## 配色体系（Kurzgesagt 风）

| 颜色 | 色值 | 用途 |
|------|------|------|
| 紫色 | `#6c5ce7` | 主强调色 |
| 青色 | `#4ecdc4` | 正面/完成 |
| 黄色 | `#ffe66d` | 高亮/警示 |
| 红色 | `#ff6b6b` | 否定/问题 |
| 白色 | `#ffffff` | 主文字 |
| 灰色 | `#8892b0` | 次要文字 |
| 背景 | `#0a0a1a` | 深色底 |

## 相关笔记

- [[AI Agent总览|🤖 AI Agent 总览]]
- [[抖音脚本-MCP协议Agent必知]]
