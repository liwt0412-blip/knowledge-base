---
tags:
  - git
date: 2026-06-04
---
# Git笔记

## 一、git的安装

安装步骤参考权威笔记：[Git安装与命令文档](../06.权威笔记/Git安装与命令文档.pdf)、[Git-版本控制工具](../06.权威笔记/Git-版本控制工具.md)



## 二、git的全局配置命令

全局配置命令在任意盘符输入cmd都可执行

```
# 设置用户名
git config --global user.name "richardqy"

# 设置密码
git config --global user.email "2690653735@qq.com"

# 查看配置信息
git config --list
```



## 三、git常用命令

### 1. 基础配置

| 功能         | 命令                                 |
| :----------- | :----------------------------------- |
| 设置用户名   | git config --global user.name 用户名 |
| 设置邮箱     | git config --global user.email 邮箱  |
| 查看配置信息 | git config --list                    |



### 2. 仓库初始化 & 克隆

| 功能           | 命令               |
| :------------- | :----------------- |
| 初始化本地仓库 | git init           |
| 克隆远程仓库   | git clone 仓库地址 |



### 3. 文件暂存操作

| 功能             | 命令             |
| :--------------- | :--------------- |
| 查看文件状态     | git status       |
| 单个文件加入暂存 | git add 文件名   |
| 所有文件加入暂存 | git add .        |
| 撤销暂存         | git reset 文件名 |



### 4. 提交本地仓库

| 功能                 | 命令                     |
| :------------------- | :----------------------- |
| 提交到本地仓库       | git commit -m "提交备注" |
| 修改最近一次提交备注 | git commit --amend       |
| 查看历史版本         | git log                  |
| 回溯版本             | git reset --hard 版本号  |



### 5. 分支操作

| 功能           | 命令                   |
| :------------- | :--------------------- |
| 查看所有分支   | git branch             |
| 创建新分支     | git branch 分支名      |
| 切换分支       | git checkout 分支名    |
| 创建并切换分支 | git checkout -b 分支名 |
| 合并分支       | git merge 分支名       |
| 删除本地分支   | git branch -d 分支名   |



### 6. 远程仓库操作

| 功能             | 命令                           |
| :--------------- | :----------------------------- |
| 关联远程仓库     | git remote add origin 远程地址 |
| 查看远程仓库     | git remote -v                  |
| 首次推送绑定分支 | git push -u origin 分支名      |
| 推送代码到远程   | git push origin 分支名         |
| 拉取远程代码     | git pull origin 分支名         |



### 7. 版本回退

| 功能           | 命令                    |
| :------------- | :---------------------- |
| 查看提交日志   | git log                 |
| 简洁查看日志   | git log --oneline       |
| 回退到指定版本 | git reset --hard 版本号 |
| 丢弃工作区修改 | git checkout -- 文件名  |



### 8. 暂存工作区（临时保存）

| 功能             | 命令           |
| :--------------- | :------------- |
| 临时保存修改     | git stash      |
| 查看临时保存记录 | git stash list |
| 恢复临时保存     | git stash pop  |



## 四、忽略文件

1. 项目根目录新建 `.gitignore`
2. 写入不需要提交的文件：

```
node_modules/
dist/
*.log
.env
```

- 忽略文件的规则
  - 忽略一个特定的文件：`path/file.ext` 
  - 忽略项目下所有这个名字的文件：`filename.ext`
  - 忽略项目下所有这个类型的文件：`*.class`
  - 忽略一个特定目录下的所用文件：`target/* `

## 相关笔记

- [[☕ Java笔记/Java笔记总览|Java笔记总览]]


- [[MOC-工具运维]]
