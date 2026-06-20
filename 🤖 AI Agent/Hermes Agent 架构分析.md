# Hermes Agent 架构全景分析

> Nous Research 出品 | 开源 AI Agent 框架 | 对标 Claude Code / Codex / OpenClaw
> 作者：小帅 | 日期：2026-06-16

## 一、概述

Hermes Agent 是一个**provider-agnostic 的开源 AI Agent 框架**，核心定位是"通用任务执行引擎"。它可以跑在：

- **终端**（CLI 交互模式）
- **消息平台**（Telegram / Discord / Slack / 微信 / 飞书 / DingTalk / Signal 等 20+ 平台）
- **IDE**（通过 ACP 协议接入 VS Code / JetBrains / Zed）
- **Webhook**（事件驱动触发）

### 一句话总结

> Hermes = 一个**与提供商无关的对话引擎** + **20+ 消息平台适配层** + **自扩展的技能记忆系统**

---

## 二、整体架构（鸟瞰）

```
┌─────────────────────────────────────────────────────────────┐
│                     用户交互层                               │
│  CLI (prompt_toolkit)  │  Gateway (多平台)  │  ACP (IDE)   │
└────────────────────────────┬────────────────────────────────┘
                             │
┌────────────────────────────▼────────────────────────────────┐
│                        AIAgent 核心引擎                      │
│  run_conversation() — 工具调用 + LLM 通信的主循环            │
│                                                             │
│  ┌────────────┐  ┌──────────────┐  ┌──────────────────┐    │
│  │ Prompt     │  │ Context      │  │ Transport 层     │    │
│  │ Builder    │  │ Compressor   │  │ (Provider 适配)  │    │
│  └────────────┘  └──────────────┘  └──────────────────┘    │
│  ┌────────────┐  ┌──────────────┐  ┌──────────────────┐    │
│  │ 工具调度器  │  │ 记忆管理器    │  │ 凭证池           │    │
│  │ model_tools │  │ memory_    │  │ credential_pool │    │
│  │ .py         │  │ manager.py  │  │ .py             │    │
│  └────────────┘  └──────────────┘  └──────────────────┘    │
└─────────────────────────────────────────────────────────────┘
                             │
┌────────────────────────────▼────────────────────────────────┐
│                      基础设施层                               │
│  ┌──────┐ ┌──────┐ ┌──────┐ ┌──────┐ ┌──────┐ ┌──────┐    │
│  │工具集  │ │技能库  │ │内存库  │ │插件系统│ │Cron  │ │MCP   │
│  │35+工具│ │SKILL. │ │SQLite │ │ plugin│ │调度器 │ │Server │
│  │      │ │MD    │ │FTS5  │ │      │ │      │ │      │    │
│  └──────┘ └──────┘ └──────┘ └──────┘ └──────┘ └──────┘    │
└─────────────────────────────────────────────────────────────┘
```

### 分层职责

| 层 | 核心文件 | 职责 |
|---|---|---|
| **用户交互** | `cli.py`, `gateway/run.py`, `acp_adapter/` | 接收输入、格式化输出、跨平台适配 |
| **引擎核心** | `run_agent.py` (13.7K LOC) | 对话循环、工具调用、LLM 通信 |
| **提供商抽象** | `agent/transports/` | 将 OpenAI 格式消息转为各 Provider 原生格式 |
| **工具系统** | `model_tools.py`, `tools/*.py` | 工具发现、注册、执行 |
| **持久层** | `hermes_state.py`, `agent/memory_manager.py` | 会话存储、记忆、技能 |

---

## 三、核心引擎：AIAgent（run_agent.py）

这是整个系统的**心脏**，13,687 行 Python（含注释和工具函数）。

### 3.1 构造函数（约 60 个参数）

```python
class AIAgent:
    def __init__(self,
        base_url, api_key, provider,         # LLM 连接参数
        model, max_iterations=90,            # 模型 + 最大迭代
        enabled_toolsets, disabled_toolsets, # 工具集开关
        platform, session_id,                # 会话上下文
        credential_pool,                     # 多 API Key 轮询池
        skip_memory, skip_context_files,     # 功能开关
        # ... + 回调、线程/用户/聊天 ID、预算、回退模型、检查点等
    )
```

### 3.2 主循环：run_conversation()

这是最核心的逻辑——**同步循环体**：

```python
while (api_call_count < max_iterations and budget.remaining > 0) or grace_call:
    if interrupt_requested: break
    response = client.chat.completions.create(
        model=model, messages=messages, tools=tool_schemas
    )
    if response.tool_calls:
        for tool_call in response.tool_calls:
            result = handle_function_call(
                tool_call.name, tool_call.args, task_id
            )
            messages.append(tool_result_message(result))
        api_call_count += 1
    else:
        return response.content  # 纯文本回复 → 结束
```

**关键特性：**
- 消息格式始终是 OpenAI 格式（`{role, content}`），传输层负责转换
- 工具调用结果追加到消息列表，保持 LLM 上下文连续性
- `IterationBudget` 控制预算，防止无限循环
- `max_iterations` 默认 90，代理子任务也共享此限制

### 3.3 UI 反馈

- **KawaiiSpinner** (agent/display.py)：LLM 响应等待时的动画表情
- **活动流**：工具调用结果用 `┊` 前缀输出，实时展示进展
- 支持 `/verbose` 切换输出详细程度（off → new → all → verbose）

---

## 四、提供商抽象层（Transport 体系）

这是 Hermes **与 LLM 提供商解耦的关键设计**。

### 4.1 设计模式：策略模式

```
agent/transports/
├── base.py               # ProviderTransport 抽象基类
├── chat_completions.py   # OpenAI 兼容协议（~16 家提供商）
├── anthropic.py          # Anthropic Messages API
├── codex.py              # OpenAI Codex Responses API
├── bedrock.py            # AWS Bedrock
└── types.py              # NormalizedResponse 统一返回类型
```

### 4.2 每个 Transport 的职责

```python
class ProviderTransport(ABC):
    def convert_messages(self, messages, **kwargs) -> Any
    def convert_tools(self, tools, **kwargs) -> Any
    def build_kwargs(self, model, messages, tools, **kwargs) -> dict
    def normalize_response(self, raw_response, **kwargs) -> NormalizedResponse
```

| 方法 | 作用 |
|---|---|
| `convert_messages` | 将 OpenAI 格式转为提供商原生格式（如 Anthropic 的 system + messages 拆分） |
| `convert_tools` | 工具 Schema 格式转换（不同提供商参数定义不同） |
| `build_kwargs` | 构造 API 调用所需的关键字参数 |
| `normalize_response` | 将提供商原始响应归一化为统一结构 |

### 4.3 支持的 20+ 提供商

覆盖全面：OpenRouter、Anthropic、OpenAI、DeepSeek、Gemini、xAI/Grok、HuggingFace、GLM、MiniMax、Kimi、阿里 DashScope、小米 MiMo、AWS Bedrock、本地 Ollama/LM Studio 等。

---

## 五、工具系统（Tool System）

### 5.1 架构

```
tools/
├── registry.py           # 中央注册表 — 所有工具在此登记
└── *.py                  # 每个工具一个文件，自动发现
    ├── file_operations.py
    ├── terminal.py (environments/)
    ├── web_search (browser_* 系列)
    ├── delegate_tool.py
    └── ...
```

### 5.2 注册模式

每个工具文件通过 `registry.register()` 注册：

```python
registry.register(
    name="example_tool",
    toolset="web",              # 归属的工具集
    schema={...},               # OpenAI Function Calling 格式
    handler=handler_fn,         # 执行函数
    check_fn=check_fn,          # 环境检查（工具仅在条件满足时显示）
    requires_env=["API_KEY"],   # 所需环境变量
)
```

> 自动发现：`tools/*.py` 中有顶层 `registry.register()` 调用即可被导入，无需手动注册。

### 5.3 工具集（Toolsets）

定义在 `toolsets.py`，目前 35+ 工具分属约 20 个工具集：

| 工具集 | 工具内容 |
|---|---|
| `web` | 网页搜索与内容提取 |
| `browser` | 浏览器自动化（Browserbase / Camofox / Chromium） |
| `terminal` | Shell 命令（支持 local / docker / ssh / modal 后端） |
| `file` | 文件读写、搜索、编辑 |
| `code_execution` | 沙箱化 Python 执行 |
| `vision` | 图片分析 |
| `image_gen` | AI 图像生成 |
| `delegation` | 子任务委派（子代理） |
| `cronjob` | 定时任务管理 |
| `memory` | 跨会话持久记忆 |
| `skills` | 技能浏览与管理 |
| `mcp` | MCP 服务器工具 |

---

## 六、Gateway：消息网关

这是 Hermes 从 CLI 工具变为**多平台 Agent**的关键架构。

### 6.1 架构

```
gateway/
├── run.py           # GatewayRunner — 主管理类、生命周期
├── session.py       # 网关会话管理、消息路由
├── platforms/       # 各平台适配器（一个文件一个平台）
│   ├── telegram.py
│   ├── discord.py
│   ├── slack.py
│   ├── weixin.py
│   ├── feishu.py
│   ├── dingtalk.py
│   ├── email.py
│   ├── signal.py
│   └── ... 共 20+
└── builtin_hooks/   # 内置钩子扩展点
```

### 6.2 核心设计

- **Agent 缓存**：`_AGENT_CACHE_MAX_SIZE=128`，LRU + 空闲 TTL（1h）淘汰
- **每个平台/会话一个 AIAgent 实例**，隔离上下文
- **消息转换**：平台原生消息 → 统一内部格式 → 路由到对应 AIAgent
- **命令审批**：`/approve`、`/deny` 机制，网关用户可审批 shell 命令
- **异步**：基于 `asyncio`，支持多平台同时运行

### 6.3 支持的 20+ 平台

Telegram、Discord、Slack、WhatsApp、Signal、Matrix、Mattermost、Email、SMS、Home Assistant、DingTalk、飞书、WeCom（企业微信）、Weixin（微信）、BlueBubbles（iMessage）、API Server、Webhook 等。

---

## 七、CLI 层

### 7.1 技术栈

- **prompt_toolkit**：输入框、自动补全、历史
- **Rich**：横幅、面板渲染
- **KawaiiSpinner**：API 等待动画

### 7.2 斜杠命令（Slash Commands）

集中注册在 `hermes_cli/commands.py` 的 `COMMAND_REGISTRY` 中：

```
COMMAND_REGISTRY = [
    CommandDef(name="new", aliases=["reset"], ...),
    CommandDef(name="model", ...),
    CommandDef(name="retry", ...),
    CommandDef(name="skills", ...),
    ...
]
```

消费方自动派生：
- CLI 进程 → `process_command()`
- Gateway → `resolve_command()` + `GATEWAY_KNOWN_COMMANDS`
- Telegram → BotCommand 菜单
- Slack → `/hermes` 子命令
- 自动补全 → `SlashCommandCompleter`

> 所有下游消费方都从中央 `COMMAND_REGISTRY` 派生，**改一处即可通用于所有平台**。

### 7.3 皮肤引擎

`hermes_cli/skin_engine.py` — 数据驱动的 CLI 主题系统，支持自定义横幅颜色、旋转表情、工具前缀等。

---

## 八、技能系统（Skills）

这是 Hermes **差异化核心竞争力之一**——自改进机制。

### 8.1 技能格式

每个技能是一个带 YAML frontmatter 的 `SKILL.md`：

```yaml
---
name: my-skill
description: 什么情况下自动加载
version: 1.0.0
---
# 技能正文

分步骤说明 + 命令 + 陷阱提示
```

### 8.2 生命周期

1. **创建**：复杂任务成功后可保存为技能（`skill_manage(action='create')`）
2. **更新**：使用中发现问题 → 立即更新（`skill_manage(action='patch')`）
3. **加载**：下次遇到匹配任务时自动加载到 system prompt
4. **冻结**：可将已安装的外部技能从符号链接转为本地副本（防源仓库删除）

### 8.3 来源

- 内置技能（`hermes-agent/skills/`）
- 可选技能（`hermes-agent/optional-skills/`）
- 中心仓库（`hermes skills install` 从 Hub 安装）
- 本地仓库（符号链接或拷贝）
- 技能命令：`/skill name` 可手动加载

---

## 九、记忆系统（Memory）

### 9.1 双轨记忆

| 记忆类型 | 内容 | 存储位置 |
|---|---|---|
| `memory` | 环境事实、项目约定、工具技巧 | SQLite（默认）/ Honcho / Mem0 |
| `user` | 用户偏好、习惯、个性 | SQLite（默认） |

### 9.2 写入时机（自动）

- 用户纠正你
- 用户说"记住这个"
- 发现环境细节（OS、已安装工具）
- 学到解决方案
- 识别出稳定的工作流

### 9.3 关键规则

- 不保存：任务进度、一次性结果、临时 TODO
- 当前会话信息用 `session_search` 翻历史，不用记忆
- 过程知识存为 skill，事实知识存入记忆

---

## 十、插件系统

`plugins/` 目录下，类型：

| 插件类型 | 功能 |
|---|---|
| `memory/*` | 记忆后端（Honcho、Mem0、Supermemory） |
| `context_engine/*` | 上下文引擎 |
| `image_gen` | 图像生成 |
| `spotify` | Spotify 控制 |
| `disk-cleanup` | Windows C 盘清理 |
| `observability` | 可观测性 |

插件通过 `hermes plugins install` 管理。

---

## 十一、Cron 调度器

位于 `cron/` 目录：

```
cron/
├── jobs.py        # 作业定义与序列化
└── scheduler.py   # 调度器主循环
```

### 设计要点

- 调度器**运行在 Gateway 进程中**，不在 CLI 会话中
- 支持 cron 表达式 / 间隔（`30m`）/ ISO 时间戳
- 作业可跨会话持久化
- 作业输出可发送到任何连接的平台
- 支持 `no_agent=True` 无 LLM 模式（纯脚本 watchdog）
- 支持 `context_from` 链式作业

---

## 十二、ACP 适配器（IDE 集成）

`acp_adapter/` 目录——实现了 **Agent Communication Protocol**：

```
acp_adapter/
├── server.py       # ACP 服务器
├── session.py      # 会话管理
├── tools.py        # 工具桥接
├── auth.py         # 认证
├── permissions.py  # 权限控制
└── events.py       # 事件推送
```

通过 ACP 协议，Hermes 可接入 VS Code、JetBrains、Zed 等 IDE，作为 AI 编码助手。

---

## 十三、MCP 支持

Hermes 既是 MCP 客户端也是 MCP 服务端：

- **客户端模式**：`hermes mcp add NAME --url URL` 配置 MCP 服务器，工具自动注入
- **服务端模式**：`hermes mcp serve` 将自身暴露为 MCP 服务器，供其他 Agent 调用

---

## 十四、关键设计决策

### 14.1 为什么选择 OpenAI 格式作为内部统一格式？

所有 Provider Transport 的输入输出都是 OpenAI 消息格式。Transport 层负责：
- **入方向**：转换成 Provider 原生格式
- **出方向**：将 Provider 原生响应归一化为统一结构

**好处**：切换 Provider 只需切换 Transport，核心逻辑不变。

### 14.2 为什么消息角色强制交替？

设计规定不能连续两个同角色消息（user-user 或 assistant-assistant）。这维护了 prompt caching 的有效性，也与主流 LLM API 约定一致。

### 14.3 为什么 Skills 是 SKILL.md 而不是代码？

- **低心智负担**：纯 Markdown，人和 LLM 都能读写
- **与 Claude Code 兼容**：相同格式的 skill 可直接共用
- **无版本依赖**：不用考虑 Python 版本冲突
- **即时生效**：保存即加载，无需编译或重启

### 14.4 为什么 Gateway 是异步而核心循环是同步？

- **Gateway**：需要同时监听 20+ 平台的消息，异步是自然选择
- **核心循环**：`run_conversation()` 是典型的请求-响应模式，同步更简单可控

---

## 十五、与竞品对比

| 特性 | Hermes Agent | Claude Code | Codex | OpenClaw |
|---|---|---|---|---|
| 开源 | ✅ MIT | ❌ | ❌ | ✅ |
| 多个 LLM Provider | ✅ 20+ | ❌ 仅 Anthropic | ❌ 仅 OpenAI | ✅ |
| 消息平台 | ✅ 20+ | ❌ | ❌ | ❌ |
| 技能自学习 | ✅ | ✅ | ❌ | ❌ |
| 跨会话记忆 | ✅ | ❌ | ❌ | ❌ |
| IDE 集成 | ✅ ACP | ✅ VS Code | ✅ VS Code | ❌ |
| MCP 支持 | ✅ 双端 | ✅ 客户端 | ✅ 客户端 | ❌ |
| Cron 调度 | ✅ | ❌ | ❌ | ❌ |
| 插件系统 | ✅ | ❌ | ❌ | ❌ |

---

## 十六、文件依赖链

```
tools/registry.py          (零依赖 — 被所有工具文件引用)
      ↑
tools/*.py                 (导入时调用 registry.register())
      ↑
model_tools.py             (导入 registry + 触发工具发现)
      ↑
run_agent.py, cli.py, batch_runner.py, gateway/
```

---

## 十七、开发/部署路径总结

```bash
# 配置
~/.hermes/config.yaml       # 设置（模型、Provider、工具集开关）
~/.hermes/.env              # API Key（不提交版本控制）
~/.hermes/skills/           # 技能文件
~/.hermes/sessions/         # 会话记录（SQLite + FTS5）
~/.hermes/logs/             # agent.log / errors.log / gateway.log

# 关键脚本
hermes                      # 交互模式
hermes gateway run          # 启动消息网关（含 Cron 调度器）
hermes doctor --fix         # 自检与修复
hermes setup                # 配置向导
```

---

## 核心洞见

> Hermes Agent 不是一个简单的"AI 聊天工具"。它是一个**通用的 AI Agent 运行平台**，核心引擎与交互方式完全解耦——同一套对话推理逻辑，通过 Gateway 适配 20+ 平台、通过 CLI 面向终端、通过 ACP 嵌入 IDE、通过 MCP 与其他 Agent 互联。Skills + Memory 使其具备持续的自我进化能力。
