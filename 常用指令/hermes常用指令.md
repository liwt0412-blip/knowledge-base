---
tags:
  - 工具
date: 2026-06-04
---
## 一、系统级 CLI（终端直接敲 hermes ...）

### 1. 启停与进程管理

#### hermes

- 作用：默认进入**交互式聊天**（等价 hermes chat）
- 场景：日常用得最多，打开就聊、让它写代码 / 查资料 / 改配置。
- 示例：

bash



运行









```
hermes
```

#### hermes start

- 作用：启动 Agent 后台服务（daemon）
- 场景：需要**长期挂着、提供 API / 被其他工具调用**时；或者 chat 提示 “未运行” 时。

#### hermes stop

- 作用：停止后台 Agent 服务
- 场景：下班关机、要升级版本、重启排障。

#### hermes restart

- 作用：重启 Agent（stop + start）
- 场景：改了 config、技能装完、模型切换后，**让新配置生效**。

#### hermes status

- 作用：查看 Agent 运行状态、鉴权、模型提供商连通性

- 场景：

  - 聊天连不上：先 status 看是不是挂了、key 是不是错了
  - 换提供商（OpenRouter/Nous）后检查是否正常

  

- 常用：

bash



运行









```
hermes status
hermes status --all --deep   # 深度诊断，报障必带
```

------

### 2. 配置管理 hermes config

#### hermes config show

- 作用：打印当前完整配置（模型、key、路径、默认工具集）
- 场景：核对当前模型是不是 gpt-4o、provider 是不是 openrouter、默认技能开了哪些。

#### hermes config set <key> <value>

- 作用：修改配置项（不用手动改 yaml）
- 场景：

bash



运行









```
hermes config set model anthropic/claude-sonnet-4  # 默认模型
hermes config set provider openrouter                # 默认提供商
hermes config set memory_enabled true                 # 开启记忆
```

#### hermes config edit

- 作用：用默认编辑器打开 config.yaml
- 场景：复杂配置（如多环境、技能参数）一次性批量改。

#### hermes config path

- 作用：输出配置文件所在目录
- 场景：找不到配置文件、要备份 / 迁移 config。

------

### 3. 技能管理 hermes skills

#### hermes skills list

- 作用：列出**已安装、可用、官方推荐**的技能
- 场景：看现在装了哪些（如 github、terminal、web）、有没有需要的没装。

#### hermes skills install <skill-name>

- 作用：安装官方 / 社区技能
- 场景：

bash



运行









```
hermes skills install github-auth    # 让 Hermes 操作 GitHub
hermes skills install terminal        # 命令行执行权限
hermes skills install web             # 网页浏览/搜索
```

#### hermes skills uninstall <skill-name>

- 作用：卸载技能
- 场景：安全收紧（比如生产环境卸掉 terminal）、清理不用的技能。

------

### 4. 记忆管理 hermes memory

#### hermes memory search "关键词"

- 作用：在长期记忆中检索历史对话 / 知识点

- 场景：

  - 想不起来之前和 Hermes 聊过的某个方案
  - 跨会话找回之前的代码片段、需求记录

  

#### hermes memory export

- 作用：导出全部记忆为 JSON 备份
- 场景：换电脑、重装系统、归档项目历史。

#### hermes memory clear

- 作用：清空长期记忆（谨慎）
- 场景：换项目、不想 AI 带旧上下文干扰新任务。

------

### 5. 会话管理 hermes sessions

#### hermes sessions

- 作用：列出所有历史会话（ID、标题、时间、模型）
- 场景：找某一天的对话、删无用会话、导出重要会话。

#### hermes sessions delete <session-id>

- 作用：删除指定会话

- 场景：清理敏感对话、减少存储占用。

- ### 继续上一次对话（最常用）

  bash

  

  运行

  

  

  

  

  ```
  hermes --continue
  # 或简写
  hermes -c
  ```

  - **作用**：直接恢复**最近一次**的对话，不需要记 ID
  - **场景**：退出 Hermes 后，想接着刚才的话题继续聊

  ### 2. 恢复指定历史会话

  bash

  

  运行

  

  

  

  

  ```
  hermes --resume <会话ID>
  # 或简写
  hermes -r <会话ID>
  ```

  - **作用**：通过会话 ID 恢复任意历史对话

  - 步骤

    ：

    1. 先运行 `hermes sessions` 查看所有会话 ID
    2. 复制 ID，执行上面命令恢复

    

  ### 3. 聊天内恢复会话

  plaintext

  

  

  

  

  

  ```
  /resume <会话ID 或 会话名称>
  ```

------

### 6. 日志与排障

#### hermes logs

- 作用：实时跟踪日志（类似 tail -f）

- 场景：

  - 对话报错、卡住：看详细报错栈
  - 技能执行失败：看工具调用日志

  

- 常用：

bash



运行









```
hermes logs
hermes logs --level debug   # 最全日志，排障必开
```

#### hermes doctor

- 作用：自动诊断配置、依赖、网络、API Key 问题
- 场景：新手最实用，一键检查所有常见坑。

bash



运行









```
hermes doctor
hermes doctor --fix   # 自动尝试修复（如补配置、装依赖）
```

#### hermes dump

- 作用：输出**可直接粘贴到 issue** 的配置摘要（脱敏 key）
- 场景：给社区 / 官方报 bug，不用手动整理信息。

------

### 7. 聊天模式（hermes chat）

#### hermes chat

- 作用：进入交互式聊天（同直接敲 hermes）

#### hermes chat -q "问题"

- 作用：**一次性问答**（非交互式，适合脚本 / 自动化）
- 场景：

bash



运行









```
hermes chat -q "写一个 Java 单例模式"
hermes chat -q "总结当前目录结构"
```

#### hermes chat --model <model>

- 作用：本次会话临时指定模型
- 场景：

bash



运行









```
hermes chat --model gpt-4o-mini   # 省钱快速
hermes chat --model claude-3-opus  # 长文本/深度思考
```

#### hermes chat --provider <provider>

- 作用：临时切换提供商（nous/openrouter/ollama）
- 场景：

bash



运行









```
hermes chat --provider ollama   # 本地模型（需 ollama serve）
hermes chat --provider openrouter
```

#### hermes --continue / -c

- 作用：**继续上次会话**（不用记 ID）
- 场景：聊到一半退出，下次直接接上。

#### hermes --resume <session-id> / -r

- 作用：恢复指定 ID 的历史会话
- 场景：打开很久以前的项目对话继续开发。

------

## 二、聊天内斜杠命令（/xxx，在 hermes chat 里用）

### 1. 会话控制

#### /new 或 /reset

- 作用：**新开空白会话**（清空上下文）
- 场景：上一个话题聊乱了、开始新需求、避免上下文污染。

#### /clear

- 作用：清屏 + 新开会话
- 场景：屏幕太乱、想干净界面重新聊。

#### /title <名字>

- 作用：给当前会话命名（方便后续 resume）
- 场景：

plaintext











```
/title 电商后台Java开发
```

#### /resume <名字或 ID>

- 作用：恢复命名会话
- 场景：回到「电商后台 Java 开发」会话继续。

#### /history

- 作用：查看当前会话完整历史
- 场景：回溯关键对话、复制之前代码。

#### /save

- 作用：手动保存当前会话
- 场景：重要对话怕丢，强制存档。

#### /retry

- 作用：**重发上一条消息**（重新生成回答）
- 场景：回答不满意、代码有错、想换一种写法。

#### /undo

- 作用：撤销**最后一轮**问答（用户 + 助手都删掉）
- 场景：上一句问错了、跑偏了，回退一步。

#### /quit 或 /exit

- 作用：退出聊天

------

### 2. 模型与工具

#### /model

- 作用：查看 / 切换当前会话模型
- 场景：中途想从 gpt-4o 切到 claude 处理长文本。

#### /tools 或 /toolsets

- 作用：列出当前可用工具（terminal/web/file/skill）
- 场景：确认 Hermes 能不能执行命令、能不能读文件。

#### /skills browse

- 作用：浏览可安装的技能中心

------

### 3. 上下文与资源

#### /usage

- 作用：显示当前会话 token 消耗、成本、上下文窗口占用
- 场景：怕超上下文限制、控制成本、看是不是要压缩。

#### /compress

- 作用：**压缩上下文**（精简历史，保留关键信息）
- 场景：对话很长、快到 token 上限，压缩后继续聊。

------

### 4. 后台任务（非常实用）

#### /background <任务>

- 作用：**新开后台会话**跑任务，主聊天不阻塞

- 场景：

  - 主聊天写代码，同时让它后台查最新技术文档
  - 后台分析整个项目代码漏洞，前台继续讨论需求

  

- 示例：

plaintext











```
/background 分析当前目录所有Java文件，列出安全问题
```

------

## 三、高频组合（直接抄）

1. 日常启动：

bash



运行









```
hermes
```

1. 连不上排障：

bash



运行









```
hermes status
hermes doctor
hermes logs --level debug
```

1. 一次性脚本问答：

bash



运行









```
hermes chat -q "解释Spring Boot自动配置原理"
```

1. 继续上次会话：

bash



运行









```
hermes --continue
```

1. 聊天里新开话题：

plaintext











```
/new
```

1. 回答不满意重生成：

plaintext











```
/retry
```

## 相关笔记

- [[MOC-工具运维]]
