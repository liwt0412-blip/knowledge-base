---
tags: [Clash, 代理, 网络, 排查, WSL]
date: 2026-07-16
---

# Clash 代理问题排查指南

> WSL + Windows 环境下的代理故障排查，基于实战踩坑总结。

---

## 架构原理

你的网络环境分**两层**，互不影响：

```
┌─────────────────────────────────────────────────┐
│                  Windows（本机）                  │
│                                                  │
│  Edge/Chrome ──→ 系统代理 ──→ 127.0.0.1:7890    │
│                   (注册表)         │              │
│                                    │              │
│  ┌─────────────────────────────────┤              │
│  │           Clash                 │              │
│  │  监听 0.0.0.0:7890 (TCP+UDP)   │              │
│  │  监听 [::]:7890                │              │
│  └──────────────┬──────────────────┘              │
│                 │                                 │
├─────────────────┼─────────────────────────────────┤
│     WSL         │                                 │
│                 ▼                                 │
│  curl/wget ──→ HTTP_PROXY ──→ 172.30.144.1:7890  │
│               (环境变量)        (WSL 网关 IP)      │
└────────────────────────────────────────────────────┘
```

| 层 | 代理方式 | 配置位置 | 独立开关 |
|----|---------|---------|---------|
| WSL | 环境变量 `http_proxy` | `~/.bashrc` / 当前 shell | 改环境变量 |
| Windows 本机 | 系统代理（注册表） | `HKCU\...\Internet Settings` | Clash 面板「System Proxy」 |
| 浏览器插件 | 插件自身配置 | SwitchyOmega 等 | 插件开关 |

**关键：WSL 不依赖 Windows 系统代理。** WSL 直连 `172.30.144.1:7890`（WSL 网关），只要 Clash 在跑就行。Windows 本机浏览器走的是系统代理，需要 `ProxyEnable=1`。

---

## 排查三步法（2 分钟搞定）

### ① 检查系统代理开关

打开 Clash for Windows 面板，看 **System Proxy** 是不是蓝色/开启状态。

如果关了 → 打开。浏览器立刻重启。

### ② 检查节点状态

看 Clash 面板当前选中节点的**延迟数值**。超时/红色 → 换一个节点。

不同节点可能封不同网站（如 OpenAI 封常见机场 IP → 换标「ChatGPT」「AI」的节点）。

### ③ 重启浏览器

**系统代理不是实时的。** 浏览器启动时读取一次，之后不会刷新。代理状态变了必须重启浏览器。

如果 ①②③ 都正常还是不通 → 可能是节点封了特定网站（如 421 Misdirected Request），换节点就行。

---

## 常见故障矩阵

| 现象 | WSL 通？ | Windows 通？ | 原因 | 解法 |
|------|---------|-------------|------|------|
| 全断 | ❌ | ❌ | Clash 没跑 / 节点挂了 | 重启 Clash / 切节点 |
| 浏览器不通、WSL 通 | ✅ | ❌ | 系统代理关了 | Clash 面板开启 System Proxy |
| 浏览器不通、代理开着 | ✅ | ❌ | 浏览器没重启 | 关掉浏览器重新打开 |
| Google 通、ChatGPT 不通 | ✅ | ❌ (API) | 节点被 OpenAI 封 | 换节点（421 = 被封） |
| 系统代理反复掉 | ✅ | 时好时坏 | 其他程序抢注册表 | 检查代理插件/安全软件 |

---

## 反复掉代理（系统代理自动关闭）

**症状：** Clash 面板 System Proxy 开着，但 `ProxyEnable` 反复变成 0。

**可能原因：**

1. **浏览器代理插件**（SwitchyOmega 等）在修改系统代理设置，与 Clash 冲突
2. **安全软件/防火墙**重置了代理注册表
3. **其他翻墙软件残留**（V2Ray、SSR 等）与 Clash 竞争

**排查方法：**

```powershell
# 查看当前系统代理状态
Get-ItemProperty 'HKCU:\Software\Microsoft\Windows\CurrentVersion\Internet Settings' | Select ProxyEnable, ProxyServer

# 查看是否有其他代理/翻墙进程
Get-Process | Where-Object { $_.ProcessName -match 'proxy|vpn|switchy|surge|netch|ssr|trojan' }
```

**如果确认是插件问题：** 关掉浏览器的代理插件，只用 Clash 管理系统代理。

---

## WSL 侧诊断命令

```bash
# 测试到 Clash 代理的连通性
curl -s --connect-timeout 5 -x http://172.30.144.1:7890 -o /dev/null -w "%{http_code}\n" https://www.google.com
# 期望: 200 或 302

# 测试绕代理直连（确认网络本身没问题）
curl -s --connect-timeout 5 --noproxy '*' -o /dev/null -w "%{http_code}\n" https://www.baidu.com
# 期望: 200

# 测试 TCP 连通性
timeout 3 bash -c 'echo "" > /dev/tcp/172.30.144.1/7890 && echo "OK" || echo "FAIL"'
# 期望: OK
```

---

## Windows 侧诊断命令

```powershell
# 测试代理是否生效（显式指定代理）
curl.exe -s -o NUL -w '%{http_code}' --connect-timeout 10 --proxy 127.0.0.1:7890 https://www.google.com
# 期望: 200 或 302

# 检查 Clash 是否在监听
netstat -ano | findstr ":7890"
# 期望: 0.0.0.0:7890 LISTENING
```

---

## 踩坑实录（2026-07-16）

- **情景：** 电脑突然不能翻墙，WSL 正常但 Edge 不通
- **原因 1：** 系统代理不知何时被关了（`ProxyEnable=0`）
- **原因 2：** 当前节点同时挂了（Google 返回 000，OpenAI 返回 421）
- **原因 3：** 手动开启系统代理后，不知什么程序反复把它关掉
- **教训：** WSL 和 Windows 本机是两套代理体系，一个通不等于另一个通。浏览器不会热加载系统代理，必须重启。

---

## 相关笔记

- [[常用指令总览|🛠️ 常用指令总览]]
- [[hermes常用指令|Hermes Agent 常用指令]]
- [[MOC-工具运维|MOC-工具运维]]
