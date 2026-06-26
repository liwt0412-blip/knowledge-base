---
tags: [NAS, 运维, 私有云, 工具]
date: 2026-06-25
sources:
  - Agent知识: 讲解/推理
confidence: high
---

# NAS 入门与选购指南

## 一句话定义

**NAS (Network Attached Storage) = 插网线的硬盘盒，自带操作系统，全家设备都能访问。**

本质上是一台低功耗小电脑，7×24 开机，通过局域网（或外网穿透）提供文件存储和各类服务。

## 要解决什么问题

| 场景 | NAS 之前 | NAS 之后 |
|---|---|---|
| 多台电脑共享文件 | U 盘拷来拷去 / 微信传 | 统一存储，任意设备访问 |
| 手机照片备份 | 百度网盘 / iCloud（交月费 + 隐私焦虑）| 自动备份到自己的硬盘 |
| 代码/项目存储 | 每台机器各拷一份，版本混乱 | 集中存储 + Git 私服 |
| 跑后台服务（MySQL/Redis/Jenkins） | 买云服务器（月付几十到几百）| NAS 上 Docker 一劳永逸 |
| 看电影 | 会员充了又充，资源不齐 | Plex/Jellyfin 自建影音库 |

核心卖点：**数据在自己手里，一次投入，长期使用。**

## 常见协议

NAS 通过网络协议对外暴露存储空间，不同设备用不同协议：

| 协议 | 全称 | 适用设备 | 特点 |
|---|---|---|---|
| **SMB/CIFS** | Server Message Block | Windows、Linux | 最主流、Win 原生支持 |
| **NFS** | Network File System | Linux、Mac | 性能好，Unix 系首选 |
| **AFP** | Apple Filing Protocol | Mac（老版本） | 已逐渐被 SMB 取代 |
| **WebDAV** | Web Distributed Authoring and Versioning | 跨平台、远程访问 | 基于 HTTP，适合外网 |
| **iSCSI** | Internet Small Computer System Interface | 服务器虚拟化 | 块级存储，像本地硬盘 |

**你主要用到的：SMB。** Windows 上网址栏输 `\\192.168.x.x` 就能访问 NAS 共享文件夹。

---

## 主流品牌（2026 年格局）

### 1. 群晖 Synology — 软件王者

- 系统 DSM（DiskStation Manager），业界公认最好用的 NAS 系统
- 套件生态丰富：Docker、Synology Drive、Photos、Active Backup for Business
- 缺点：**贵**（同配置比友商贵 30%~50%"品牌溢价"）
- 适合：愿意为软件体验付费的开发者

### 2. 威联通 QNAP — 硬件良心

- 同价位硬件配置碾压群晖（更多盘位、更大内存、2.5GbE 网口）
- 系统 QTS/QuTS hero，功能也全但 UI 不如 DSM 精致
- 适合：追求性价比、愿意折腾、对 ZFS 文件系统有需求

### 3. 极空间 / 绿联 — 国产新势力

- 价格最低、上手门槛最低（极影视 / 极相册开箱即用）
- 系统封闭，可玩性不如群晖/威联通
- 适合：不想折腾、纯粹备份+看电影的用户

### 品牌速选

| 需求 | 推荐 |
|---|---|
| 要 Docker 折腾 + 最佳软件体验 | **群晖 DS224+ 或 DS923+** |
| 同预算要更高配置 | **威联通 TS-464** |
| 纯粹备份照片+看电影 | **极空间 Z4 Pro** |

---

## Docker 玩法（和你最相关的部分）

NAS 本质是一台 24 小时开机的 Linux 小服务器，装 Docker 后能跑几乎所有轻量服务：

| 服务 | 用啥 | 场景 |
|---|---|---|
| Git 私服 | Gitea / GitLab CE | 代码不上云端，家里 Git |
| 数据库 | MySQL / PostgreSQL / Redis | 本地开发测试环境 |
| CI/CD | Jenkins / Drone | 自动构建部署 |
| 项目管理 | 飞书文档平替 Outline / Wiki.js | 团队知识库 |
| 影音 | Plex / Jellyfin / Emby | 自建流媒体 |
| 智能家居 | Home Assistant | 联动米家/HomeKit |
| 密码管理 | Vaultwarden (Bitwarden 轻量实现) | 密码不上云 |
| 图床 | Chevereto / Lsky Pro | 写 Markdown 自建图床 |
| 下载 | qBittorrent / Aria2 | 离线下载 |

**对你来说最实用的组合**：Docker 跑 MySQL + Redis 当本地开发环境 → 项目连 `192.168.x.x:3306` 不走 localhost，跟真实部署环境一致。

---

## 选购要点

| 关注点 | 建议 |
|---|---|
| **盘位数** | 最少 2 盘位（1 块存数据 + 1 块备份/扩容），推荐 4 盘位 |
| **RAID** | 不用管花哨模式，两块盘做 RAID 1（镜像）最安全，坏一块数据还在 |
| **网口** | 至少千兆（1GbE），2.5GbE 更好。你家里上千兆路由器就跑满，没必要追万兆 |
| **内存** | 可扩展最好，装 Docker 后 2G 起步，推荐 4G~8G |
| **硬盘** | 必须用 NAS 专用盘（希捷酷狼 / 西数红盘），普通桌面盘 7×24 跑半年就挂 |
| **功耗** | 一般 15W~30W，24小时开机一个月电费 5~10 块，不心疼 |

---

## 和你的技术栈关联

1. **Java 开发环境**：Docker Compose 一键启动 MySQL + Redis + Nacos + RabbitMQ，不用在开发机上装一堆服务
2. **Spring Boot 项目部署**：NAS 上跑 Docker 容器，本地 push 镜像 → NAS pull 启动，模拟生产部署流程
3. **面试加分**：运维话题提到"在家搭过 NAS 跑 Docker 服务" → 证明你有 Linux + 网络 + 容器化的实操经验
4. **知识库备份**：Obsidian Vault 放 NAS 上，Mac/Win/WSL 三端读写同一份笔记

---

## 相关笔记

- [[常用指令/常用指令总览|🛠️ 常用指令总览]]
- [[MOC-工具运维|🛠️ 工具运维]]
- [[常用指令/Docker常用命令整理|Docker 常用命令]]
- [[常用指令/DockerCompose常用命令整理|Docker Compose 常用命令]]
- [[常用开发网站收藏]]（选购参考）
