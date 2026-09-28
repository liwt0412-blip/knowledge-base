---
title: "蟹堡王来了个分单员：Jev 到底是什么？"
status: 待发布
priority: normal
version: v1
date: 2026-09-27
updated: 2026-09-27
task_id: jev-bikini-bottom-v1
script_approved: true
voice_sample_approved: true
voice_final_approved: true
render_authorized: true
target: 抖音
aspect_ratio: "16:9"
estimated_duration: "实测269.57秒，8087帧，30fps"
writing_style: TOKEN人味儿写作
hook_type: "虚构比奇堡订单分流演示"
voice: "默认本地IndexTTS 2.5；沿用src/配音/hook.m4a前9秒与已确认参数"
source:
  - https://typesafe.ai/blog/introducing-system-one-models-and-jev
  - https://docs.typesafe.ai/introduction
  - https://docs.typesafe.ai/system-one
  - https://docs.typesafe.ai/primitives
  - https://docs.typesafe.ai/confidence
  - https://docs.typesafe.ai/introduction/machine-learning-primer
source_evidence: D:/workspece/GitHup/remotion/out/jev-bikini-bottom-v1/research-v1.md
script_snapshot: D:/workspece/GitHup/remotion/out/jev-bikini-bottom-v1/narration-v1.json
storyboard: D:/workspece/GitHup/remotion/out/jev-bikini-bottom-v1/storyboard-v1.md
next_action: "MP4已生成，等待成片反馈；按本期发布物料流程继续，未确认本期结束"
composition_id: JevBikiniBottom
video_output: D:/workspece/GitHup/remotion/out/jev-bikini-bottom-v1/JevBikiniBottom-illustrated-v1.mp4
rendered_at: 09/27/2026 10:46:48
studio_url: http://localhost:3002/JevBikiniBottom
preview_approved: true
review_authority: "用户委托助手审核中间产物，并在Studio预览后明确要求：帮我渲染出来；成片终验尚未确认"
preview_record: D:/workspece/GitHup/remotion/out/jev-bikini-bottom-v1/preview-v1.md
---

# 蟹堡王来了个分单员：Jev 到底是什么？

本期判断：Jev 把有范围的语义判断交给软件使用；输出类型受约束，业务正确性仍需数据验证与流程兜底。

本稿等待确认。比奇堡故事为本期原创假设示例，不冒充动画原剧集；所有画面演示值都标注示意，尚未调用 Jev API。以下仅“完整口播”各段正文送入配音。

## 完整口播

### 蟹堡王的分单员

给比奇堡编个小故事。蟹堡王的订单一下堆到了柜台上。派大星要加一个蟹黄堡，有人想退钱，还有人问店几点关门。蟹老板装上一台分单机，只让它选：厨房、收银台、问询台。它读完顾客的话，选好去处，订单就被送到对应窗口。海绵宝宝继续做汉堡。这台机器负责的那一步，就很接近 Jev 要做的事：给程序一个可以接着执行的判断。

### TOKEN 品牌介绍

我是 Token。我平时写 Java，也在折腾怎么把 AI 真正用进开发。这个账号，记录的就是这些过程。这期先从 Jev 决策模型开始。

### Jev 到底是什么

Jev 是 TypeSafe AI 推出的模型，官方把它归为 System One，强调快速、范围明确的判断。你把当前信息和问题交给它，并提前规定答案的类型。它返回选项、分数或概率，代码再决定下一步怎么走。普通大模型也能输出结构化结果。Jev 的取舍是专门做这类判断，当前不生成文章、代码，也不写推理解释。

### 三种问题，三种输出

回到蟹堡王。同一张订单，可以问三种问题。该送哪个窗口？在列好的选项里选一个，这叫 Choice。顾客催得有多急？先定好不急、催单、强烈催单这些等级，再给出位置，这叫 Score。顾客有没有要求退款？返回一个零到一之间的概率，这叫 Noul。它表示答案为“是”的概率，不能拿来当退款金额。模型给出判断后，真正把单子送出去的，仍然是程序。

### 怎么把判断装进软件

接到真实系统里，输入可以是顾客消息、订单记录和店里的处理规则。能用代码核对的金额、订单号，照常用代码核对；需要理解顾客意思的地方，再交给模型。官方介绍，Jev 会并行处理同一份信息上的独立问题，不用逐字写出一段回答。如果后一个问题必须用到前一个答案，程序就要分两次调用。不要把整家餐厅怎么经营，一口气塞成一个问题。

### 不确定时怎么办

麻烦出在派大星这句话：“把刚才那个退掉。”退的是汉堡，还是饮料？缺少记录时，答案可能在几个选项间分散。Jev 的 Choice 和 Score 会返回概率分布，以及从分布算出的置信度，程序可以据此转给人工。TypeSafe 还用一种叫 RLCD 的训练方法，目标是让预测概率更符合实际发生的频率。比如一大批报八成概率的判断，理想情况下应当约有八成成立。这不保证眼前这一单正确；置信度本身也不能直接读成正确率。

### 格式对了，内容仍可能错

所以，看到宣传里的“不会幻觉”，别理解成它不会判断错。答案只能落在规定范围内，它仍然可能把退款送到厨房。如果选项只有厨房和收银台，丢东西的顾客又该去哪？选项要留出其他或人工处理。自动处理的门槛，也得拿自己的数据来测。Jev 当前只接收文本；片中的比奇堡图片是我们讲故事用的，并没有交给它识别。

### 回到蟹堡王

要写一封解释退款原因的回复，继续让擅长生成文字的模型来写。要在大量请求里反复做分类、评分和分流，Jev 值得放进候选，再测准确率、延迟和成本。回到蟹堡王，清楚的订单送去对应窗口，说不清的先追问，涉及退钱还得核对记录和权限。Jev 可以承担其中的判断环节。整家店怎么运转，仍然要把流程写清楚。

## 画面与声音约定

- 分层插画＋角色动作＋订单路径动态图。复用用户目录里的透明人物、汉堡、柜台、窗口与场景背景。
- 以蟹堡王分单故事开头，正文仍沿用同一套故事对象作解释；TOKEN 在品牌介绍、关键边界讲解和结尾选择性出现。
- 开场结束后保留独立 2.5 秒 hook-brand 转场，再进入品牌旁白，音效与两侧旁白不重叠。
- 原素材背景是竖构图，横屏不能硬拉伸。优先局部布景配合前景柜台构成横屏舞台；必要时另做匹配横背景。
- 画面中的 Choice、Score、Noul、订单、概率、关键状态由代码叠加，字幕基于最终旁白强制对齐。
- 配音使用已确认的本地 IndexTTS 2.5，默认参考 hook.m4a 前9秒、seed=20260922，不额外施加情绪向量；先听本期钩子短样，不自动换引擎。

## 开场备选

推荐 A（本稿）：订单涌入柜台，分单机把各单送到不同窗口。先展示工作，再说名字，便于观众理解输入、有限选项和程序执行的分工。
B（异常入口）：派大星只说“把刚才那个退掉”，机器停在两个选项间。先讲不确定性，再倒回正常分流，优点是冲突集中，缺点是认识 Jev 前要先理解概率。
C（任务差异）：蟹老板要给顾客写道歉信，分单机只吐出“收银台”。先展示工具用错，再解释适用范围，优点是直接，缺点是观众可能先误解为模型无能。

## 核验摘要

定义、输出类型、文本输入范围与并行独立问题来自 TypeSafe 官方文档；RLCD 和概率校准为官方训练目标介绍。片中不引用“快193倍”“便宜444倍”等厂商特定评测数字，不宣称实测、不宣称零判断错误。本期未调用 Jev，不展示假装来自真实接口的结果。

来源与逐条边界见 research-v1.md；分镜见 storyboard-v1.md。脚本确认、短样认可、最终音频认可保留真实记录，交付范围止于 Studio 预览。


## 本次制作产物（Studio 待预览）

- 用户指令：继续，后续你帮我审核。助手依此完成中间审核；不是用户亲自试听或确认前端的记录。
- Studio：[JevBikiniBottom](http://localhost:3002/JevBikiniBottom)，约4分30秒，1920×1080 / 30fps。
- 预览说明：D:/workspece/GitHup/remotion/out/jev-bikini-bottom-v1/preview-v1.md
- 最终声音审核：D:/workspece/GitHup/remotion/out/jev-bikini-bottom-v1/voice-review-v2.md
- 字幕与时间轴：D:/workspece/GitHup/remotion/src/video-data/jev-bikini-bottom-media.ts
- 画面与播放检查：D:/workspece/GitHup/remotion/out/jev-bikini-bottom-v1/studio-review-v1.json
- MP4已完成；封面与发布文案按后续物料阶段记录，本期尚未标记完成。原始审核快照及v1/v2音频均保留。

## MP4 成片

- 授权：用户在Studio预览后明确要求：帮我渲染出来。
- 文件：D:/workspece/GitHup/remotion/out/jev-bikini-bottom-v1/JevBikiniBottom-illustrated-v1.mp4
- 检查：1920×1080，30fps，8087帧；完整视频与音频解码通过。
- 记录：D:/workspece/GitHup/remotion/out/jev-bikini-bottom-v1/render-check-v1.json
- 成片终验与本期结束尚未确认。
