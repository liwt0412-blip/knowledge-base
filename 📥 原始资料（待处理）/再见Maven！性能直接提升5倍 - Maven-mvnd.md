---
tags: [Maven, 构建工具, mvnd, GraalVM, 开发效率]
date: 2026-07-21
source: https://mp.weixin.qq.com/s/ybDDKkSXQlC5C7lGVDxV5w
original: juejin.cn/post/7394073179483947008
---

# 再见Maven！性能直接提升5倍

> 来源：微信公众号转载，原始来源 [juejin.cn/post/7394073179483947008](https://juejin.cn/post/7394073179483947008)，抓取日期 2026-07-21

---

## Maven-mvnd 是什么

Maven-mvnd（简称 mvnd）是 Apache Maven 团队借鉴 Gradle 和 Takari 的优点，衍生出来的更快的构建工具，是 Maven 的强化版。解决 Maven 构建慢的问题，又不需要重新学习。

## 解决的痛点

1. **构建速度慢**：MVND 维护一个长期运行的 Maven 守护进程（Daemon），避免每次构建时 JVM 重复启动
2. **资源消耗高**：守护进程在构建之间保持活跃，减少 CPU/内存浪费，CI/CD 环境尤其受益
3. **频繁构建延迟**：缩短等待时间，提高开发效率
4. **多项目构建优化**：守护进程可被多个构建请求共享
5. **易于迁移**：与 Maven 用法一致，无需学习新工具语法

## 核心特性

- **嵌入 Maven**：不需要单独安装 Maven，无缝切换
- **守护进程架构**：长期运行的后台进程，一个守护进程可处理多个连续请求
- **GraalVM 本地可执行文件**：启动更快、使用内存更少
- **JIT 代码保留**：JVM 的即时编译器生成的本机代码在守护进程生命周期内保留，减少重复编译开销

## 安装与使用

### 下载
https://github.com/mvndaemon/mvnd/releases

### 安装
直接解压，配置环境变量：
- `JAVA_HOME`
- `MAVEN_HOME`
- `MAVEN_MVND_HOME`
- 将 `bin` 目录添加到 `PATH`

### 测试
```bash
mvnd -v
```

### 使用
用法与 Maven 完全一致：
```bash
# Maven
mvn clean package -Dmaven.test.skip=true

# Maven-mvnd（直接替换 mvn → mvnd）
mvnd clean package -Dmaven.test.skip=true
```

### 配置兼容
在安装目录 `/conf/mvnd.properties` 末尾添加：
```properties
maven.settings=F:/javaee/apache-maven-3.6.3/conf/settings.xml
```
也可以指定 JDK 路径（如果没配 `JAVA_HOME`）。

## 打包对比

| 工具 | 命令 |
|------|------|
| Maven | `mvn clean package -Dmaven.test.skip=true` |
| mvnd | `mvnd clean package -Dmaven.test.skip=true` |

子项目越多，mvnd 相对速度优势越明显。如果项目模块很多，可以在测试、生产环境使用 mvnd 辅助打包。

## 总结

Maven-mvnd = Maven 的兼容性 + Gradle 的速度优势。通过 GraalVM 本地镜像 + 守护进程，启动快、内存少、JIT 优化代码可复用。无需改 POM、无需学新工具，把 `mvn` 换成 `mvnd` 即可。

---

## 相关笔记

- [[00-原始资料说明]]
