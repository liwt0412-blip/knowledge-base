---
tags:
  - 工具
  - docker
date: 2026-06-04
---
# Docker Compose 常用命令 & 配置整理

> 配合 Docker 命令一起用，Compose 用来编排多容器项目。

---

## 一、核心概念

Docker Compose 通过一个 `docker-compose.yml`（或 `compose.yaml`）文件定义多个服务（容器），一条命令启动整个项目。

```yaml
version: '3.8'
services:
  服务名A:
    image: xxx
  服务名B:
    image: yyy
```

---

## 二、常用命令（在 docker-compose.yml 所在目录执行）

### 2.1 启动与停止

| 操作 | 命令 |
|------|------|
| 启动所有服务（前台）| `docker compose up` |
| 启动所有服务（后台）| `docker compose up -d` |
| 停止并删除容器 | `docker compose down` |
| 停止并删除容器+网络+卷 | `docker compose down -v` |
| 重启服务 | `docker compose restart` |
| 停止服务（不删除）| `docker compose stop` |
| 启动已停止的服务 | `docker compose start` |

### 2.2 查看与调试

| 操作 | 命令 |
|------|------|
| 查看运行中的服务 | `docker compose ps` |
| 查看日志（全部）| `docker compose logs` |
| 持续跟踪日志 | `docker compose logs -f` |
| 查看某个服务的日志 | `docker compose logs <服务名>` |
| 进入某个容器 | `docker compose exec <服务名> /bin/bash` |
| 查看配置 | `docker compose config` |

### 2.3 构建与更新

| 操作 | 命令 |
|------|------|
| 构建/重新构建镜像 | `docker compose build` |
| 构建并启动（常用）| `docker compose up -d --build` |
| 重建某个服务 | `docker compose up -d --build <服务名>` |

### 2.4 清理

```bash
docker compose down          # 停止并清理容器/网络
docker compose down -v       # 连数据卷一起清（小心数据丢失）
```

---

## 三、docker-compose.yml 配置详解

### 3.1 基本结构

```yaml
services:
  web:          # 服务名
    image: nginx:latest
    container_name: my-nginx   # 容器名（可选）
    ports:
      - "8080:80"              # 宿主机端口:容器端口
    volumes:
      - ./html:/usr/share/nginx/html   # 挂载目录
    environment:
      - NGINX_HOST=localhost
    restart: always            # 重启策略
    depends_on:
      - api                    # 依赖的服务（先启动谁）

  api:
    build: ./api               # 用 Dockerfile 构建
    ports:
      - "8081:8081"
    depends_on:
      - db
    environment:
      SPRING_PROFILES_ACTIVE: prod

  db:
    image: mysql:8.0
    environment:
      MYSQL_ROOT_PASSWORD: root123
      MYSQL_DATABASE: myapp
    volumes:
      - mysql_data:/var/lib/mysql   # 命名卷

volumes:
  mysql_data:                  # 声明命名卷
```

### 3.2 常用配置项速查

| 配置项 | 作用 | 示例 |
|--------|------|------|
| `image` | 指定镜像 | `nginx:latest` |
| `build` | 指定 Dockerfile 目录 | `./app` |
| `ports` | 端口映射 | `"8080:80"` |
| `volumes` | 挂载目录或卷 | `./data:/app/data` |
| `environment` | 环境变量 | `MYSQL_ROOT_PASSWORD=123` |
| `env_file` | 从文件加载环境变量 | `./.env` |
| `depends_on` | 依赖关系 | `- db` |
| `restart` | 重启策略 | `always / no / on-failure / unless-stopped` |
| `container_name` | 自定义容器名 | `my-app` |
| `networks` | 指定网络 | `- frontend` |
| `command` | 覆盖默认启动命令 | `npm run start` |
| `healthcheck` | 健康检查 | 见下面 |
| `working_dir` | 工作目录 | `/app` |
| `user` | 运行用户 | `node` |

### 3.3 重启策略

```yaml
restart: "no"               # 不自动重启（默认）
restart: always             # 容器退出总是重启
restart: on-failure         # 非正常退出才重启
restart: unless-stopped     # 除非手动停止，否则一直重启
```

---

## 四、常用实战模板

### 4.1 Nginx + 静态页面

```yaml
services:
  web:
    image: nginx:alpine
    ports:
      - "80:80"
    volumes:
      - ./www:/usr/share/nginx/html
      - ./nginx.conf:/etc/nginx/conf.d/default.conf
```

### 4.2 Spring Boot + MySQL

```yaml
services:
  app:
    build: .
    ports:
      - "8080:8080"
    environment:
      SPRING_DATASOURCE_URL: jdbc:mysql://db:3306/myapp?useSSL=false
      SPRING_DATASOURCE_USERNAME: root
      SPRING_DATASOURCE_PASSWORD: root123
    depends_on:
      db:
        condition: service_healthy

  db:
    image: mysql:8.0
    environment:
      MYSQL_ROOT_PASSWORD: root123
      MYSQL_DATABASE: myapp
    volumes:
      - mysql_data:/var/lib/mysql
    healthcheck:
      test: ["CMD", "mysqladmin", "ping", "-h", "localhost"]
      interval: 10s
      timeout: 5s
      retries: 5

volumes:
  mysql_data:
```

### 4.3 Nginx + Vue 前端 + Spring Boot 后端

```yaml
services:
  frontend:
    build: ./frontend
    ports:
      - "80:80"
    depends_on:
      - backend

  backend:
    build: ./backend
    ports:
      - "8080:8080"
    environment:
      SPRING_PROFILES_ACTIVE: prod
    depends_on:
      - redis
      - mysql

  mysql:
    image: mysql:8.0
    environment:
      MYSQL_ROOT_PASSWORD: root123
    volumes:
      - mysql_data:/var/lib/mysql

  redis:
    image: redis:7-alpine

volumes:
  mysql_data:
```

---

## 五、易错点 & 避坑

| 坑 | 说明 |
|----|------|
| `depends_on` 只保证启动顺序，不保证服务就绪 | 应用里要加重试逻辑，或用 `condition: service_healthy` |
| `docker compose down` 会删容器，数据卷默认保留 | 加 `-v` 才会删卷，小心数据丢失 |
| `docker compose` vs `docker-compose` | 新版 Docker 用 `docker compose`（无横杠），旧版用 `docker-compose` |
| 容器间通信用服务名，不要用 IP | 比如 app 连 db 写 `jdbc:mysql://db:3306/...` |
| 修改 yml 后要重新 up 才生效 | `docker compose up -d` 重新加载即可 |

---

## 六、新手学习路线

```
Docker 基础 → Docker Compose → Docker Swarm/K8s
     ↓
先跑单个容器 → 用 Compose 编排多个 → 上生产
```

学 Compose 的阶段，照着上面的模板自己改来跑，比死记命令快得多。

---

> 文件位置：桌面 → `DockerCompose常用命令整理.md`

## 相关笔记

- [[MOC-工具运维]]
