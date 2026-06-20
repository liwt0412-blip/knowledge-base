---
tags:
  - 工具
  - docker
date: 2026-06-04
---
# Docker 常用命令整理

> 学完 Docker 的常用速查手册，按使用场景分类。

---

## 一、镜像管理（Image）

| 操作 | 命令 |
|------|------|
| 拉取镜像 | `docker pull <镜像名>:<标签>` |
| 查看本地镜像 | `docker images` |
| 删除镜像 | `docker rmi <镜像ID或名称>` |
| 强制删除镜像 | `docker rmi -f <镜像ID>` |
| 构建镜像（Dockerfile）| `docker build -t <镜像名>:<标签> .` |
| 查看镜像历史 | `docker history <镜像名>` |

**示例：**
```bash
docker pull nginx:latest
docker pull ubuntu:22.04
docker images
docker rmi ubuntu:22.04
docker build -t my-app:v1 .
```

---

## 二、容器管理（Container）

### 2.1 创建与运行

| 操作 | 命令 |
|------|------|
| 运行容器（前台）| `docker run <镜像名>` |
| 运行容器（后台）| `docker run -d <镜像名>` |
| 运行并端口映射 | `docker run -d -p 宿主机端口:容器端口 <镜像名>` |
| 运行并指定名称 | `docker run -d --name <容器名> <镜像名>` |
| 运行并交互进入 | `docker run -it <镜像名> /bin/bash` |
| 运行并自动删除（用完即焚）| `docker run --rm <镜像名>` |
| 运行并挂载目录 | `docker run -v /宿主机路径:/容器路径 <镜像名>` |
| 设置环境变量 | `docker run -e 变量名=值 <镜像名>` |

**组合示例：**
```bash
docker run -d --name my-nginx -p 8080:80 nginx
docker run -it --rm ubuntu:22.04 /bin/bash
docker run -d -v /mydata:/app/data --name my-app my-app:v1
```

### 2.2 查看容器

| 操作 | 命令 |
|------|------|
| 查看运行中的容器 | `docker ps` |
| 查看所有容器（含停止的）| `docker ps -a` |
| 查看容器日志 | `docker logs <容器名或ID>` |
| 持续跟踪日志 | `docker logs -f <容器名或ID>` |
| 查看容器详细信息 | `docker inspect <容器名或ID>` |
| 查看容器资源占用 | `docker stats` |

### 2.3 进入容器

```bash
docker exec -it <容器名或ID> /bin/bash    # 进入容器（推荐）
docker attach <容器名或ID>                # 附加到容器（不推荐）
```

### 2.4 启停与删除

| 操作 | 命令 |
|------|------|
| 启动已停止的容器 | `docker start <容器名或ID>` |
| 停止容器 | `docker stop <容器名或ID>` |
| 重启容器 | `docker restart <容器名或ID>` |
| 强制停止 | `docker kill <容器名或ID>` |
| 删除容器 | `docker rm <容器名或ID>` |
| 强制删除运行中的容器 | `docker rm -f <容器名或ID>` |
| 删除所有已停止的容器 | `docker container prune` |

---

## 三、网络管理

| 操作 | 命令 |
|------|------|
| 查看网络列表 | `docker network ls` |
| 创建网络 | `docker network create <网络名>` |
| 指定网络运行容器 | `docker run --network <网络名> <镜像名>` |
| 查看网络详情 | `docker network inspect <网络名>` |

---

## 四、数据卷（Volume）

| 操作 | 命令 |
|------|------|
| 创建数据卷 | `docker volume create <卷名>` |
| 查看所有数据卷 | `docker volume ls` |
| 挂载数据卷 | `docker run -v <卷名>:<容器路径> <镜像名>` |
| 删除数据卷 | `docker volume rm <卷名>` |

---

## 五、Dockerfile 常用指令

```dockerfile
FROM openjdk:17                    # 基础镜像
WORKDIR /app                       # 工作目录
COPY target/app.jar app.jar        # 复制文件到镜像
ADD app.tar /app                   # 复制并自动解压
RUN apt update && apt install -y   # 构建时执行命令
CMD ["java", "-jar", "app.jar"]    # 容器启动命令
ENTRYPOINT ["java", "-jar"]        # 入口点（不可被覆盖）
EXPOSE 8080                        # 声明端口
ENV JAVA_HOME=/usr/lib/jvm         # 环境变量
```

---

## 六、常用组合套路

### 拉取并运行 Nginx
```bash
docker run -d --name web -p 80:80 nginx
```

### 跑一个 MySQL
```bash
docker run -d --name mysql8 \
  -e MYSQL_ROOT_PASSWORD=123456 \
  -p 3306:3306 \
  mysql:8.0
```

### 构建 Java 项目镜像
```bash
# 先把 jar 包打出来
mvn clean package -DskipTests

# 写一个简单 Dockerfile（上面第五段参考）
docker build -t my-java-app:v1 .
docker run -d -p 8080:8080 --name app my-java-app:v1
```

### 清理垃圾（空间回收）
```bash
docker system prune               # 清理停止的容器、无用网络、悬空镜像
docker system prune -a            # 清理所有未使用的镜像（更激进）
docker image prune                # 只清理悬空镜像
```

---

## 七、快速记忆口诀

```
run    跑容器         ps       看容器列表
exec   进容器         logs     看日志
stop   停容器         rm       删容器
images 看镜像         pull     拉镜像
build  打镜像         push     推镜像
prune  清垃圾         inspect  看详情
```

---

> 文件位置：桌面 → `Docker常用命令整理.md`

## 相关笔记

- [[MOC-工具运维]]
