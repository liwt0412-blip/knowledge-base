---
tags: [Git]
date: 2026-06-08
---
# 1. 初始化仓库（第一次用才执行）
git init

# 2. 把所有文件加入暂存区
git add .

# 3. 提交到本地仓库（你写错成 commti 了）
git commit -m "项目初始化"
# 关联远程仓库，origin是远程默认别名
git remote add origin https://gitee.com/xxx/xxx.git
# 查看是否绑定成功
git remote -v


推送 必须要先拿到开发者权限
# 第一次推送必须指定分支，默认本地主分支main/master二选一
# 新版git默认分支main
git push -u origin main
# 老项目默认master
# git push -u origin master

# 第一次推送必须指定分支，默认本地主分支main/master二选一
# 新版git默认分支main
git push -u origin main
# 老项目默认master
# git push -u origin master


完整版（只拉目标分支，不拉别的分支数据）
# 格式：git clone -b 分支名 --single-branch 仓库地址 只下载当前分支代码，不下载全仓库
git clone -b dev --single-branch https://gitee.com/xxx/demo.git


简写（克隆全仓库数据，默认切到目标分支，能后续切其他分支）
git clone -b dev https://gitee.com/xxx/demo.git
依旧下载全部分支历史，只是打开项目默认在 dev 分支。

浅克隆（只拉最新 1 次提交，极速下载）
git clone -b dev --single-branch --depth 1 https://gitee.com/xxx/demo.git

怎么合并分支
	在管理哪里有一个分支合并----然后选择需要合并的分支

## 相关笔记

- [[🖥 项目笔记/项目笔记总览|项目笔记总览]]

- [[MOC-项目实战.md|MOC-项目实战]]