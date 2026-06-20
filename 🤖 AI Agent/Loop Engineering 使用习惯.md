# Loop Engineering 使用习惯

> **核心心法：别写步骤，写目标。**
> 给 Agent 的目标越接近"做什么"、越远离"怎么做"，Loop 越有价值。

---

## 一、六条习惯

### ① 给目标，不给步骤

```
❌ "打开 UserController.java，第45行加个 @GetMapping..."
✅ "UserController 的 /users 接口加分页，参考项目里其他接口的风格"
```

### ② 复杂任务先 explore 侦察

让 Agent 先读项目结构，回来汇报，你再给任务。避免它盲猜。

```
Claude Code: explore 这个项目的包结构和数据流
Hermes: 读一遍项目结构，告诉我有什么潜在问题
```

### ③ AGENTS.md 固化项目约定

在项目根目录写 AGENTS.md，把常用约定写进去（数据库、框架、代码风格）。Agent 每次启动自动读，不用你重复说。

### ④ 做完让 Agent self-review

```
做完了？review 一下你改的代码，告诉我有无风险
```

Agent 自己检查自己，是 Loop 闭环的关键。

### ⑤ 复杂任务拆阶段

```
❌ "帮我做一个用户注册 + 验证码 + 创建账号功能"
✅ "先设计数据库表 → 我确认 → 再写后端接口 → 再写前端页面"
```

每阶段结束你确认，不会一条路走到黑。

### ⑥ 让 Agent 主动发现坑

```
现有代码有什么潜在的坑？读一遍告诉我
```

Agent 自己扫描推理，你只需要听汇报、做决策。

---

## 二、旧习惯 vs 新习惯对照表

| 旧习惯（Prompt Engineering） | 新习惯（Loop Engineering） |
|------------------------------|---------------------------|
| 告诉 Agent 怎么做 | 告诉 Agent 做什么 |
| 每个步骤亲手指挥 | AGENTS.md 定规则 |
| 改完立刻检查每一行 | 让 Agent review 自己 |
| 遇到问题手动排查 | 让 Agent 先探险再汇报 |
| 给模糊指令靠运气 | 给清晰目标靠规则 |

---

## 三、操作要点

**Claude Code：**
- 用 `explore` 命令让 Agent 先侦察
- 项目根目录放 CLAUDE.md / AGENTS.md
- 自带 `claude init` 生成初始 CLAUDE.md

**Hermes Agent：**
- 本项目根目录已有 AGENTS.md（即本文件所在的知识库根目录）
- 每天日常对话就是在练 Loop Engineering
