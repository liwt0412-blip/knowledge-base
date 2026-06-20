---
tags:
  - 工具
  - openclaw
date: 2026-06-04
---
# OpenClaw 常用指令大全--如果是国内版请在openclaw后面加-cn（OpenClaw-cn）

## 一、基础指令

| 指令 | 说明 |
|------|------|
| `openclaw --help` | 显示帮助信息，查看所有可用命令 |
| `openclaw --version` | 查看当前安装的 OpenClaw 版本号 |
| `openclaw status` | 查看 OpenClaw 整体运行状态，包括配置、连接状态等 |
| `openclaw onboard` | 初始化配置向导，首次安装后运行 |

---

## 二、Gateway 服务管理

| 指令 | 说明 |
|------|------|
| `openclaw gateway start` | 启动 Gateway 服务，开始接收消息 |
| `openclaw gateway stop` | 停止 Gateway 服务 |
| `openclaw gateway restart` | 重启 Gateway 服务，配置更改后常用 |
| `openclaw gateway status` | 查看 Gateway 运行状态、端口、连接信息 |

---

## 三、模型管理

| 指令 | 说明 |
|------|------|
| `openclaw models list` | 列出所有已配置的 AI 模型及其状态 |
| `openclaw models add <provider/model>` | 添加新的模型，如 `openclaw models add openai/gpt-4` |
| `openclaw models remove <model>` | 移除指定的模型配置 |
| `openclaw models default <model>` | 设置默认使用的模型 |

---

## 四、技能管理（Skills）

| 指令 | 说明 |
|------|------|
| `clawhub list` | 列出所有可用的技能包 |
| `clawhub install <skill>` | 安装指定技能，如 `clawhub install tavily-search` |
| `clawhub uninstall <skill>` | 卸载已安装的技能 |
| `clawhub update <skill>` | 更新指定技能到最新版本 |
| `clawhub update --all` | 更新所有已安装的技能 |
| `clawhub info <skill>` | 查看技能的详细信息和使用说明 |

### 推荐安装的技能

| 技能名 | 功能说明 | 安装命令 |
|--------|----------|----------|
| `tavily-search` | 网络搜索能力，让 AI 能查资料 | `clawhub install tavily-search` |
| `find-skills` | 自动寻找解决问题的技能 | `clawhub install find-skills` |
| `proactive-agent` | 自我迭代升级的主动代理 | `clawhub install proactive-agent` |
| `weather` | 查询天气信息 | `clawhub install weather` |
| `feishu-doc` | 飞书文档读写操作 | `clawhub install feishu-doc` |
| `feishu-wiki` | 飞书知识库导航 | `clawhub install feishu-wiki` |

---

## 五、配置管理

| 指令 | 说明 |
|------|------|
| `openclaw config get <key>` | 获取指定配置项的值 |
| `openclaw config set <key> <value>` | 设置配置项的值 |
| `openclaw config edit` | 用编辑器打开配置文件进行手动编辑 |
| `openclaw config path` | 显示配置文件的路径位置 |

### 常用配置项

| 配置项 | 说明 | 示例 |
|--------|------|------|
| `model` | 默认使用的模型 | `openclaw config set model moonshot/kimi-k2.5` |
| `agents.defaults.model.primary` | 主模型配置 | 需编辑配置文件 |
| `tools.web.search.enabled` | 启用网络搜索 | `openclaw config set tools.web.search.enabled true` |

---

## 六、日志与调试

| 指令 | 说明 |
|------|------|
| `openclaw logs` | 查看最近的日志 |
| `openclaw logs --follow` | 实时跟踪日志输出（类似 tail -f） |
| `openclaw logs --limit <n>` | 查看最近 n 条日志 |
| `openclaw doctor` | 运行诊断检查，自动发现并修复常见问题 |

---

## 七、会话与子代理

| 指令 | 说明 |
|------|------|
| `openclaw sessions list` | 列出所有活跃的会话 |
| `openclaw sessions history <id>` | 查看指定会话的历史消息 |
| `openclaw sessions kill <id>` | 强制结束指定会话 |
| `openclaw subagents list` | 列出所有子代理 |
| `openclaw subagents kill <id>` | 结束指定子代理 |

---

## 八、认证与账户

| 指令 | 说明 |
|------|------|
| `openclaw auth login <provider>` | 登录指定服务商，如 `openclaw auth login openai` |
| `openclaw auth logout <provider>` | 登出指定服务商 |
| `openclaw auth list` | 列出所有已认证的账户 |
| `openclaw auth status` | 查看当前认证状态 |

---

## 九、插件管理

| 指令 | 说明 |
|------|------|
| `openclaw plugins list` | 列出所有已安装的插件 |
| `openclaw plugins install <plugin>` | 安装插件 |
| `openclaw plugins uninstall <plugin>` | 卸载插件 |
| `openclaw plugins enable <plugin>` | 启用插件 |
| `openclaw plugins disable <plugin>` | 禁用插件 |

---

## 十、快捷操作

| 指令 | 说明 |
|------|------|
| `openclaw chat` | 启动交互式聊天模式 |
| `openclaw run <file>` | 运行指定的脚本文件 |
| `openclaw upgrade` | 检查并升级 OpenClaw 到最新版本 |

---

## 使用技巧

1. **Tab 补全**：大部分命令支持 Tab 键自动补全
2. **帮助信息**：任何命令加 `--help` 可查看详细用法，如 `openclaw gateway --help`

   

---

## 相关笔记

- [[MOC-工具运维]]
