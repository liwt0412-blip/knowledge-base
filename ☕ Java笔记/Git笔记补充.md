---
tags:
  - git
date: 2026-06-04
---
# 版本控制工具\-Git

## 引入

在企业中，进行项目开始时，我们基本全部都是团队协作开发，也就是说同时有好几个人，甚至于几十个，几百个人同时开发一个大的项目。

![Image](https://internal-api-drive-stream.feishu.cn/space/api/box/stream/download/authcode/?code=ZjE0MTZhMTNiNjVhNWIwYTE2ZWI4ZTNiZTU2ODc5ZjhfZDVjMzM1ZGNmZTQyNDUxMGJjYTk5OWYzNjE0YWE3YTZfSUQ6NzUyMzEyMTI4MzA4MDA0NDU2M18xNzgwMDU2NjcwOjE3ODAxNDMwNzBfVjM)

那他们开发的是同一个项目，也就意味着他们共享的其实是同一套代码。 然后大家再思考一下，如果是团队协作开发，A开发定义了一个工具类，B开发要想使用这个工具类，该怎么办呢，团队内部的各个成员之间如何共享代码呢？ 

飞秋、QQ、微信发送? U盘拷贝? No，No，No，这些方法都不靠谱，太繁琐了，企业开发中，只需要让各个开发人员，连接同一个代码仓库，每个人的代码变更，都传到这个代码仓库中，其他人再从代码仓库下载代码即可。

![Image](https://internal-api-drive-stream.feishu.cn/space/api/box/stream/download/authcode/?code=MmJlZGZiY2QwMTliOGQzNmFlYjc1YWVjYjBkZGQxMGNfMmI5YzFkOGZhMGQ3ZGU0YWE1OGFkNGQ2ZTA1MmE1ZjJfSUQ6NzUyMzEyNDc4MDUxNDYyMzUxNl8xNzgwMDU2NjcwOjE3ODAxNDMwNzBfVjM)

而我们要想，能够在自己的电脑上操作这个代码仓库，往其中上传代码，从里面下载代码，我们自己的电脑上就必须要安装一个对应的版本控制工具，而目前最为流行的版本控制工具，当属Git。

![Image](https://internal-api-drive-stream.feishu.cn/space/api/box/stream/download/authcode/?code=YmI5MTMzYTZmM2IwMWUwMWI3ZWY2MWY2N2UyZDFmNGNfMmYyNzAwY2Q3Njc3NDYzZGMyNjFkZDM2NjE1NWE1ZTNfSUQ6NzUyMzEyNTE3NDgwMDc0NDQ1Ml8xNzgwMDU2NjcwOjE3ODAxNDMwNzBfVjM)



## 介绍与安装

### 介绍

![Image](https://internal-api-drive-stream.feishu.cn/space/api/box/stream/download/authcode/?code=Yjg1NWIwMTkyZDIyYjA4YzVlMDQ2MTkxMmIxMmE1NDZfZDVhZmU5ZTIzMzg0YjJiYTBkM2RiN2JmNWE3Y2M4NjdfSUQ6NzUyMzEyNTYyNjc3Njg5NTQ4OV8xNzgwMDU2NjY5OjE3ODAxNDMwNjlfVjM)

- Git是一个开源免费的分布式版本控制工具，主要用于管理项目开发中的源代码文件（如：java类、xml文件、html页面等），在软件开发中被广泛应用。

- 作用：

    - 代码回溯：Git在管理文件过程中会记录日志，方便回退到历史版本

    - 版本切换：Git存在分支的概念，一个项目可以有多个分支（版本），可以任意切换

    - 多人协作：Git支持多人协作，即一个团队共同开发一个项目，每个团队成员负责一部分代码，通过Git就可以管理和协调

    - 远程备份：Git通过仓库管理文件，在Git中存在远程仓库，如果本地文件丢失还可以从远程仓库获取



### 安装

- 下载Git安装包：[https://git\-scm\.com/downloads](https://git-scm.com/downloads)

![Image](https://internal-api-drive-stream.feishu.cn/space/api/box/stream/download/authcode/?code=ZjE5OGYwNWZkZGE5N2JlODY1NTAzOGZjZmQ2Yzc3YWFfNTBmYTRmY2M5ODQyMjhhNzZiN2ZhNTk5Y2Y1MjZmNzBfSUQ6NzUyMzEyNjE0MjY3OTEzODMyM18xNzgwMDU2NjcwOjE3ODAxNDMwNzBfVjM)

下载完成后得到安装文件 （此安装包课程资料中已经提供）：

![Image](https://internal-api-drive-stream.feishu.cn/space/api/box/stream/download/authcode/?code=NTkxOGJkYWFhZDY0NzUyZWY2N2Q0ODUzYjM0NTYyZmRfOTdiZTEwY2Q3Yzg0NTMzOGQ5ZTcwODE0ZDRlZTkxMjVfSUQ6NzUyMzEyNjI2ODUyMTQxNDY3NV8xNzgwMDU2NjcwOjE3ODAxNDMwNzBfVjM)

直接双击完成安装即可，安装完成后可以在任意目录下点击鼠标右键，如果能够看到如下菜单则说明安装成功：

![Image](https://internal-api-drive-stream.feishu.cn/space/api/box/stream/download/authcode/?code=YjAyNTEyNTM4MWU0MGY1NDhlMjg3Nzc3YzFmM2I0ZDZfYWY2N2NjNGE5YTNhNjk1NDU3ZGZkYTU2NjE3OTAxNjNfSUQ6NzUyMzEyNzA3NjMxMTUxNTEzN18xNzgwMDU2NjcwOjE3ODAxNDMwNzBfVjM)



### Git操作流程

![Image](https://internal-api-drive-stream.feishu.cn/space/api/box/stream/download/authcode/?code=MzlmMzcwYzM3ZmE4YzUwYzIxZmNlZTA0OTQ0NDg0MTJfY2M0MGQ4MzAyMmExOWQ3N2Y0YWI0MDczMDM4ZjRhYTNfSUQ6NzUyMzEyOTQ4MzE3NDU3NjEzMl8xNzgwMDU2NjcwOjE3ODAxNDMwNzBfVjM)

- 工作区：也称为工作目录，主要用于存放开发的项目代码。

- 暂存区：一个临时保存修改文件的地方。

- 本地仓库：也称为版本库，版本库中存储了很多配置信息，以及操作日志、文件版本信息等。

- 远程仓库：一个远端的仓库，各个开发人员可以通过这个远程仓库进行交互。



## 代码托管服务

Git中存在两种类型的仓库，即 **本地仓库 **和 **远程仓库**。那么我们如何搭建Git **远程仓库 **呢？

我们可以借助互联网上提供的一些代码托管服务来实现，其中比较常用的有GitHub、码云、GitLab等。

![Image](https://internal-api-drive-stream.feishu.cn/space/api/box/stream/download/authcode/?code=MTY3YWE0ZTMzMDM4ZTIzZmIxODEzMDg0NjMyNjZiMTVfMWY2OTg3MzY1ZGI1NGViZGEwNzkxYWZkYTM4ZjFmZjVfSUQ6NzUyMzEzMDc2MDY5MTc2MTE1M18xNzgwMDU2NjY5OjE3ODAxNDMwNjlfVjM)

|**名称**|**网址**|**说明**|
|---|---|---|
|GitHub|https://github\.com/|一个面向开源及私有软件项目的托管平台，因为只支持Git 作为唯一的版本库格式进行托管，故名gitHub|
|Gitee|https://gitee\.com/|国内的一个代码托管平台，由于服务器在国内，所以相比于GitHub，码云速度会更快|
|GitLab|https://about\.gitlab\.com/|一个用于仓库管理系统的开源项目，使用Git作为代码管理工具，并在此基础上搭建起来的web服务|

那这里，我们选择访问速度更快，对初学者也比较友好的Gitee （中文的）。

![Image](https://internal-api-drive-stream.feishu.cn/space/api/box/stream/download/authcode/?code=ZWI4YWE1MjIzZmMyOGQxOTEyNDg0NmFkMWFkMGZjMDVfMjcyNDZkNTQ1OTNmM2Y2MTgzZjgyZDE1ZDc1NzJmZTRfSUQ6NzUyMzEzMjQzMDU1NTI1MDY5MF8xNzgwMDU2NjcwOjE3ODAxNDMwNzBfVjM)

具体操作步骤如下：



1\)\. 访问Gitee官网，注册码云账号。

注册链接：https://gitee\.com/signup

![Image](https://internal-api-drive-stream.feishu.cn/space/api/box/stream/download/authcode/?code=Mzc5NWZhZTMyZDU3OTRlNmI0NWMxMjIzYTZlNjg1OTlfZTA5ODgxYTljODZhNjllN2Y0YzIwZDU4ODE4NmZhNjFfSUQ6NzUyMzEzMjcwMTA5NzM0NTAyOF8xNzgwMDU2NjY5OjE3ODAxNDMwNjlfVjM)



2\)\. 登录码云。

注册完成后可以使用刚刚注册的邮箱进行登录（地址： https://gitee\.com/login ）

![Image](https://internal-api-drive-stream.feishu.cn/space/api/box/stream/download/authcode/?code=YzExYjBiOGYzODhmODBlZTJhYWIwOWIxNmI4OWYzMDZfOWY2ZDg3ODgwMzg3Nzg2YmUzYmY4ZDdiNTBiNDUwNWJfSUQ6NzUyMzEzMjk5NzM5OTY5MTI2Nl8xNzgwMDU2NjcwOjE3ODAxNDMwNzBfVjM)



3\)\. 创建远程仓库。

登录成功后可以创建远程仓库，操作方式如下：

![Image](https://internal-api-drive-stream.feishu.cn/space/api/box/stream/download/authcode/?code=ZWJjNTU3NjBmNzE5OTg3NTFhNzE0M2E4NDQyNjdmZmVfODA5ZjQ5YTYxNjUyYTE3ODBjYjRmY2MxMzg5MmQxNGZfSUQ6NzUyMzEzMzMzNTc1OTkyOTM2M18xNzgwMDU2NjcwOjE3ODAxNDMwNzBfVjM)

页面跳转到新建仓库页面：

![Image](https://internal-api-drive-stream.feishu.cn/space/api/box/stream/download/authcode/?code=MGYyYzk3MWY4ZDljNjRjOTQzYjBhM2U0OWEzMjcwZDlfOGYxYTEwM2ZhNzI5ZDc1N2M2MWM2OWQ5OTg4NDA2N2NfSUQ6NzUyMzEzMzg1MTE0NjQwMzg0MV8xNzgwMDU2NjY5OjE3ODAxNDMwNjlfVjM)

![Image](https://internal-api-drive-stream.feishu.cn/space/api/box/stream/download/authcode/?code=NTg0OWEyYTE3MTUxMGQwNDczZDQwMDg5MjdmNTk0MDJfM2Y0YmEyYmNjYTgwOWM3YWZiMmUxMTk2ZTMzMTlmYzhfSUQ6NzUyMzEzNTMyMzcxODE1NjI5MV8xNzgwMDU2NjcwOjE3ODAxNDMwNzBfVjM)

好的，那到此呢，关于Git的安装以及远程仓库的账号准备，这些准备工作，我们就已经搞定了。 那接下来，我们要来学习的就是Git中的常见操作。



## Git常用命令

### Git全局配置

当安装Git后首先要做的事情是设置用户名称和email地址。这是非常重要的，因为每次Git提交都会使用该用户信息。在Git 命令行中执行下面命令：

- **设置用户信息** 

    - `git config \-\-global user\.name \&\#34;itcast\&\#34;`

    - `git config \-\-global user\.email \&\#34;``itcast@itcast\.cn``\&\#34;`

- **查看配置信息**

    - `git config \-\-list`

**注意：**上面设置的user\.name和user\.email并不是我们在注册码云账号时使用的用户名和邮箱，此处可以任意设置（但是建议设置为自己的信息）。



那如何执行上述的命令呢？ 具体的步骤如下：

1\)\. 在任意目录下，右键，选择 `Open Git Bash here`

![Image](https://internal-api-drive-stream.feishu.cn/space/api/box/stream/download/authcode/?code=NjkwMGRhZDA4ZGUwMWYyODViNDYxZjQ5MmJmOTMwZDNfZWM2ZTMzZWVhMzRiODM1ZTA4Y2ViMGVjMmJmMWUzMDZfSUQ6NzUyMzEzNjM5MjYzOTk4NzczMV8xNzgwMDU2NjY5OjE3ODAxNDMwNjlfVjM)



2\)\. 打开命令行后，就可以执行上述的命令了。

![Image](https://internal-api-drive-stream.feishu.cn/space/api/box/stream/download/authcode/?code=MDViOTg0OWJkOGZmMTUyZjEwYzJlN2MxYTM1ZjhlODRfZDMwY2YxMzk3ZDA5M2U4YWQwM2FhZWI1ZTc3MGY4YmJfSUQ6NzUyMzEzNzEyMTg5NjIzNTAyN18xNzgwMDU2NjcwOjE3ODAxNDMwNzBfVjM)



### Git本地仓库操作

![Image](https://internal-api-drive-stream.feishu.cn/space/api/box/stream/download/authcode/?code=MmJkZGUwMjk4ZGUwMjQwOTM1ZjQyZjVlZGVhZmJkMzRfNjAxMTgxNzA1MTlmOThjNDQ3NDNlZmYxOWJhOWQzYzJfSUQ6NzUyMzEzODA1Njc1NzEzMzMxNF8xNzgwMDU2NjcwOjE3ODAxNDMwNzBfVjM)

本地仓库操作的命令，主要涉及到以下几个：



#### git init 

- 语法：`git init`

- 作用： 创建一个本地仓库

- 演示：

在我们的磁盘目录下，创建一个文件夹，专门来演示Git的操作。比如在D盘下，创建一个空文件夹 `git\-repo` 。然后进入这个目录后，右键菜单，选择 `Open Git Bash here`

![Image](https://internal-api-drive-stream.feishu.cn/space/api/box/stream/download/authcode/?code=YjE1Y2RiZWFhMzE5NWMzNDhkNjliMjNhMzZiM2Q4MmVfYzdhNDE1NjA4N2JkOWRlYmMyZGNjYjEwZTA5MjdmMThfSUQ6NzUyMzEzOTQxNjIyNDQ5NzY2Nl8xNzgwMDU2NjcwOjE3ODAxNDMwNzBfVjM)



然后，在命令行中执行命令，git init 就可以创建出一个git本地仓库。如果在当前目录中看到\.git文件夹（此文件夹为隐藏文件夹）则说明Git仓库创建成功 。

![Image](https://internal-api-drive-stream.feishu.cn/space/api/box/stream/download/authcode/?code=OThlZDdiMDFkN2M3YTAzOGFkMmQ1ZjA1NGFjODdmODVfYTJhY2EyNDI3MDI3YWNiZWY2M2ExNWQzY2Y5YjcwMjlfSUQ6NzUyMzEzOTkwNDA2MDUyMjQ5OF8xNzgwMDU2NjY5OjE3ODAxNDMwNjlfVjM)

这个\.git隐藏文件夹是Git版本控制系统的核心，里面存储了Git本地仓库所有的元数据、版本库信息、暂存区信息 。

如果将\.git文件夹删除了，这个本地仓库也就不复存在了。



#### git status

- 语法：`git status`

- 作用：查看当前工作目录和暂存区文件的状态

- 演示：

由于目前，工作目录中还没有任何的文件，所以执行git status看不到任何有效信息，只是提示我们没有任何提交的文件。

![Image](https://internal-api-drive-stream.feishu.cn/space/api/box/stream/download/authcode/?code=NDA1NDAyNTQ3MjcwMTQ4MDNmM2Y5NGYwMTY4OTAzNDRfMjFjNDVhZmFmNTcwMzBlOWUyMDRiMDQ5ZTViYzIyNmVfSUQ6NzUyMzE0MjExMTUyMDQ0MDMyMV8xNzgwMDU2NjY5OjE3ODAxNDMwNjlfVjM)



我们在工作目录下新建一个文件 `1\.txt`，然后再执行git status看看效果。

![Image](https://internal-api-drive-stream.feishu.cn/space/api/box/stream/download/authcode/?code=N2UxMzllZTFjM2YyMDA4NjA3YzAxMGMzNGVhMjU5YzVfMTQzMDcxYjkwNjVjY2ZkMzg2NjM2OGQ5ODg0YzUzZTNfSUQ6NzUyMzE0MzEzNDQ4Mjg0MTYxOV8xNzgwMDU2NjcwOjE3ODAxNDMwNzBfVjM)

我们可以看到工作目录中的文件状态为 `Untracked`，表示文件未跟踪，未被纳入版本控制。文件的状态会随着我们执行Git的命令发生变化，Git工作区中的文件存在如下两类状态：

- Untracked 未跟踪（未被纳入版本控制）

- Tracked 已跟踪（被纳入版本控制）

    - Unmodified 未修改状态

    - Modified 已修改状态

    - Staged 已暂存状态



#### git add 

- 语法：`git add \&lt;file\&gt;`

- 作用：将新增/修改的文件加入暂存区。

- 演示：

![Image](https://internal-api-drive-stream.feishu.cn/space/api/box/stream/download/authcode/?code=YjlmNGJiN2UwYmNiYTYwYjVkNGJlZjk4OTY5YzlhY2RfZDYzMjdkZTc2NDY1OTVlOTI5MzE5NDIwMTdjYmUxZThfSUQ6NzUyMzE0NzM5NTEwMzIyNzkyM18xNzgwMDU2NjY5OjE3ODAxNDMwNjlfVjM)



此时，我们再修改一下 `1\.txt` 文件中的内容，然后再通过 `git status` 看一下状态 。

![Image](https://internal-api-drive-stream.feishu.cn/space/api/box/stream/download/authcode/?code=OTg1NmFkNjQyOTU4OGE0MWEzNmE5YzIxNDhkNWJhZDVfYzNjODgwNGY5ZWY5ZWU1MDNiMjEwZmVlYjliMjVlOWVfSUQ6NzUyMzE0ODUyNzUzNTA3OTQyN18xNzgwMDU2NjcwOjE3ODAxNDMwNzBfVjM)

如果暂存区的文件的被修改，我们可以通过 git add \.\.\. 再次加入暂存区。

![Image](https://internal-api-drive-stream.feishu.cn/space/api/box/stream/download/authcode/?code=OGJmOWE1MDczMjQ2Y2I5MTJlY2FlNTNjOGU3YjVmYzlfZTYwYjk4OWUzZjc3YTAxYmUyNWVhY2FmOTAxMThlNmZfSUQ6NzUyMzE1MDQyNTQ0NDg1OTkwNV8xNzgwMDU2NjY5OjE3ODAxNDMwNjlfVjM)



#### git  reset

git reset 命令的作用是将暂存区的文件 **取消暂存 **或者是 **切换到指定版本**

- 取消暂存：`git reset \&lt;file\&gt;`

![Image](https://internal-api-drive-stream.feishu.cn/space/api/box/stream/download/authcode/?code=YTg5YTNjZGNhNmU0Y2Y2MDAyYThlM2NmY2M1Yzc2NGZfMjM2NjMxMDNlMGNhMTM5YmJlYzVkNzA5ODczYTI1MjRfSUQ6NzUyMzE1MDgzMTQzMjk0MTU3Ml8xNzgwMDU2NjY5OjE3ODAxNDMwNjlfVjM)



- 切换到指定版本命令格式：`git reset \-\-hard 版本号`

![Image](https://internal-api-drive-stream.feishu.cn/space/api/box/stream/download/authcode/?code=ZmFkOTRhZTk4NjFiMmFmNmE2YmNhM2QzYWM5Y2U4ZmFfNWU1ZWYwZWZmYzY3NmY1MWI0ODI2YzlmZjVjMTU1MjlfSUQ6NzUyMzE1NDY3MTY3NzcwMjE0N18xNzgwMDU2NjcwOjE3ODAxNDMwNzBfVjM)

**注意：**每次Git提交都会产生新的版本号，通过版本号就可以回到历史版本



#### git commit

- 作用：是将暂存区的文件修改提交到版本库

- 语法：`git commit \-m \&lt;备注信息\&gt; \&lt;文件名\&gt;`

- 说明：

    - \-m：代表message，每次提交时需要设置，会记录到日志中

    - 可以使用通配符 \* 一次提交多个文件，如果不指定文件名，表示将暂存区的文件，全部提交

- 演示：

![Image](https://internal-api-drive-stream.feishu.cn/space/api/box/stream/download/authcode/?code=YzUxMTZlZGY1OGZiNWUzY2FmMzZhY2RmNzg3YzRmMzBfNTlkZDQ2ODE3MDY1ZDBmYjM2OGJjOWZiOTlhYjlkOGZfSUQ6NzUyMzE1Mjk2ODg4MzM4ODQ0NF8xNzgwMDU2NjY5OjE3ODAxNDMwNjlfVjM)





#### git log

- 作用：查看提交日志

- 语法：`git log`

- 演示：

![Image](https://internal-api-drive-stream.feishu.cn/space/api/box/stream/download/authcode/?code=NGI0YjhjNTllNjFmMDE1Y2RlNTNkOWQyMmMyMGU1MThfNjA2NGI1Y2RiZWM5ODA1M2U5M2Q0ZTBhOWMwY2U1MTRfSUQ6NzUyMzE1MzM0NjY1OTQ1MDg4NF8xNzgwMDU2NjcwOjE3ODAxNDMwNzBfVjM)

在日志中，我们可以看到具体是谁（全局配置中配置的用户名和邮箱），什么时间，提交了代码，具体的版本号是多少都可以看到。



多修改几次文件，多提交几次后，再看日志：

![Image](https://internal-api-drive-stream.feishu.cn/space/api/box/stream/download/authcode/?code=YWVlZTZkOWFhZmE1NzliYzJiNDY4YzVmZTNkN2QwYjFfZGU1YThjZGVmODJjZjc5MWY3NjBhODExYzgxNGU1ZGVfSUQ6NzUyMzE1NDExNzYzNzM3Mzk1Nl8xNzgwMDU2NjcwOjE3ODAxNDMwNzBfVjM)



### Git远程仓库操作

本地仓库操作的命令，讲解完毕之后，接下来我们再来讲解远程仓库的操作命令。具体流程如下：

![Image](https://internal-api-drive-stream.feishu.cn/space/api/box/stream/download/authcode/?code=YzQzYTJlZjEzY2I5M2FkODM4NTFjNWJlNTA3ZmEzYTdfYTEwNTczM2ZlNTFlOTEyZmY3MzA0ZmQ3ZDE5ZDYxNDVfSUQ6NzUyMzE1NTE0MTA5MjkwMDg2Nl8xNzgwMDU2NjY5OjE3ODAxNDMwNjlfVjM)

常见命令如下：

|**命令**|**描述**|**示例**|
|---|---|---|
|git remote \[\-v\]|查看本地仓库|git remote \-v|
|git remote add \&lt;short\-name\&gt; \&lt;url\&gt;|添加远程仓库|git remote add origin [https://gitee\.com](https://gitee.com)\.\.\.|
|git clone \&lt;url\&gt;|从远程仓库克隆|git clone [https://gitee\.com](https://gitee.com)\.\.\.|
|git push \&lt;shortname\&gt; \[branchname\]|推送到远程仓库|git push origin master|
|git pull \&lt;shortname\&gt; \[branchname\]|从远程仓库拉取|git pull origin master|



#### git remote 

如果要查看已经配置的远程仓库服务器，可以执行 git remote 命令，它会列出每一个远程服务器的简称。

![Image](https://internal-api-drive-stream.feishu.cn/space/api/box/stream/download/authcode/?code=ZTI1NjliZGMyYjU4ZWMwN2ZhNDkyYjE3OTliYjk0Y2FfOTFjOGE2YTYwMTNmZDBmZmJkMDkyZmM2NmE0NTgxNGZfSUQ6NzUyMzE1NjU1NjUxMDkwNDMyM18xNzgwMDU2NjY5OjE3ODAxNDMwNjlfVjM)

目前，我们的这个本地仓库并未配置任何的远程仓库，所以没有任何信息输出。



如果配置了远程仓库，则会查询出对应的远程仓库，如下：

![Image](https://internal-api-drive-stream.feishu.cn/space/api/box/stream/download/authcode/?code=NjY4NzEwYjhjMjg5NzE4ZmUyMTRiY2Q5YjJkNTkxOGZfNjg4OTY2NWM2YmQ3ZjhjYzVhYTVkZDYxYjIyOWJmZmVfSUQ6NzUyMzE1NzUzMDU1ODUxMzE1Nl8xNzgwMDU2NjY5OjE3ODAxNDMwNjlfVjM)



#### git remote add

- 作用：配置、添加远程仓库

- 语法：`git remote add 简称 远程仓库地址`

- 样例：`git remote add origin ``https://gitee\.com/dawn\_code/my\-repo1\.git`

- 演示：

![Image](https://internal-api-drive-stream.feishu.cn/space/api/box/stream/download/authcode/?code=NmEzMTQ2MDBiZmU4ZDNjMTA5ZTcwZjdkMjhkNGNlZmVfMTI3NDQ0MTNjOWI5YjI1MTdkYTM2NTIwNjIyNTc0NGJfSUQ6NzUyMzE1NzQwOTQ2NzQ2NTczMF8xNzgwMDU2NjY5OjE3ODAxNDMwNjlfVjM)

注意：一个本地仓库可以关联多个远程仓库，多个远程仓库的地址的简称不能重复。（一般只会关联一个）



#### git push

- 作用：将本地仓库的文件推送到远程仓库中。

- 语法：`git push 远程仓库简称 分支名称`

- 样例：`git push origin master`

- 演示：

由于我们要访问远程仓库了，而访问远程仓库是需要输入账号、密码的，所以需要在弹窗中输出用户名、密码。（仅仅在第一次访问gitee时需要输入，后续就不用了，因为windows系统会自动记录账号密码）

![Image](https://internal-api-drive-stream.feishu.cn/space/api/box/stream/download/authcode/?code=MDljMjA0ZmQyOGRjZWNhN2Q5MzE0YmQ3NDU2NTliNTZfZTk3MmIxMmNkZmY0YzdhM2MyOGEyZjJhMTkyOWVlMzZfSUQ6NzUyMzE1OTQzNjExMTk3MDMyM18xNzgwMDU2NjY5OjE3ODAxNDMwNjlfVjM)

![Image](https://internal-api-drive-stream.feishu.cn/space/api/box/stream/download/authcode/?code=ZGZkOTgxMWRmYzQzZjBlMjkxOTVmNTczZjAxYzQ2NjhfOTcwZGIyNTI1MjdhYTk4MWIxOTgzMTkwZWE0MjhjMWVfSUQ6NzUyMzE1OTc0NTYxNDU3NzY2N18xNzgwMDU2NjcwOjE3ODAxNDMwNzBfVjM)





#### git clone

- 作用：Git 克隆的是该 Git 仓库服务器上的几乎所有数据（包括日志信息、历史记录等）下载到本地，获得一份Git 远程仓库的拷贝。

- 语法：`git clone 远程仓库地址`

- 样例：`git clone ``https://gitee\.com/dawn\_code/my\-repo1\.git`

![Image](https://internal-api-drive-stream.feishu.cn/space/api/box/stream/download/authcode/?code=OTg5MmYzNzQ2ODM5YzlkN2Y2MTEyYWFhNzEzNWJlNjVfYWJjZmRjNTNkNDg1N2M2ODU3Zjk0MGI1YTg5NDU5NGZfSUQ6NzUyMzE4NDMzMTIwMTIwMDE1Nl8xNzgwMDU2NjY5OjE3ODAxNDMwNjlfVjM)

克隆之后，可以看到有一个目录 my\-repo1，这个就是我们克隆的仓库对应的目录。进入 my\-repo1 这个目录，就可以看到里面的文件。

![Image](https://internal-api-drive-stream.feishu.cn/space/api/box/stream/download/authcode/?code=YjE4YjA1YjcxOTc4OTVjZmNiNGQyNTMyZGQ3MDAyZGRfZDg5YjVhNGQ1MzZiYjRhZjVlYTNlNzU4OGY2YTZhNDZfSUQ6NzUyMzE4NDkzOTE3Nzc3MTAxMV8xNzgwMDU2NjcwOjE3ODAxNDMwNzBfVjM)

**提示：**由于这个本地仓库是从远程仓库克隆下来的，所以这个本地仓库已经自动关联的这个远程仓库。



#### git pull

- 作用：从远程仓库获取最新版本并合并到本地仓库

- 语法：`git pull 远程仓库简称 分支名称`

- 样例：`git pull origin master`

![Image](https://internal-api-drive-stream.feishu.cn/space/api/box/stream/download/authcode/?code=MDA5YTJkM2E1ZTIzNDYzOWU3YmY0ZGEzZmFjYWQxMGJfZTAzNjNlMjkwZDZkYWQ4M2YyOTIxZjY2NGUxZTM4ZDBfSUQ6NzUyMzE4NjcyMjUzNDI3NzEyMl8xNzgwMDU2NjcwOjE3ODAxNDMwNzBfVjM)

**注意：**如果当前本地仓库不是从远程仓库克隆，而是本地创建的仓库，并且仓库中存在文件，此时再从远程仓库拉取文件的时候会报错（fatal: refusing to merge unrelated histories ）

解决此问题可以在git pull命令后加入参数\-\-allow\-unrelated\-histories



### Git分支操作

- 分支是Git 使用过程中非常重要的概念。使用分支意味着你可以把你的工作从开发主线上分离开来，以免影响开发主线。

- 本地仓库和远程仓库中都有分支，同一个仓库可以有多个分支，各个分支相互独立，互不干扰。

- 通过 `git init` 命令创建本地仓库时默认会创建一个`master`分支。

![Image](https://internal-api-drive-stream.feishu.cn/space/api/box/stream/download/authcode/?code=MDFjYzkyMjY0Y2JjMTM4NzNiYjExYzA0OWVmNWM5YjlfOTJhODY1YzExNDU4MWYxYzVhNDFhODc2OGI0MTQ1NWNfSUQ6NzUyMzE4Nzg0MDkzODc4NjgzNV8xNzgwMDU2NjY5OjE3ODAxNDMwNjlfVjM)



分支的操作指令包括:

|**命令**|**描述**|**示例**|
|---|---|---|
|git branch|查看分支|git branch \-v|
|git branch \&lt;branch\-name\&gt;|创建分支|git branch v1|
|git checkout \&lt;branch\-name\&gt;|切换分支|git checkout v1|
|git push \&lt;short\-name\&gt; \&lt;branch\-name\&gt;|推送至远程仓库分支|git push origin v1|
|git merge \&lt;branch\-name\&gt;|合并指定分支到当前分支|git merge v1|
|git branch –d \&lt;branch\-name\&gt;|删除分支|git branch –d v1|



#### 查看分支

- 查看分支命令：`git branch`

    - `git branch`               列出所有本地分支

    - `git branch \-r`         列出所有远程分支

    - `git branch \-a`         列出所有本地分支和远程分支

![Image](https://internal-api-drive-stream.feishu.cn/space/api/box/stream/download/authcode/?code=Y2I4ZDM1ZmIxOWFjY2E4MDJiNTQyNjM5YTAxNGM2MjlfYjkwYjEzNjY0NDFmNjliYzNmODRhMjE2M2ZmZWI0M2VfSUQ6NzUyMzE4OTcyNzk4Mjg5NTEwNV8xNzgwMDU2NjY5OjE3ODAxNDMwNjlfVjM)



#### 创建分支

- 格式：`git branch 分支名称`

- 样例：`git branch v1`

![Image](https://internal-api-drive-stream.feishu.cn/space/api/box/stream/download/authcode/?code=NGIyNmE0YzJlNDg2M2UwYzgxNTZmM2M5OTk0ZThjMmFfYjZhN2E4M2UxM2Y5M2E4YzBkZDVjODM2YjNlM2RhYzZfSUQ6NzUyMzE5MDE1NTc5MzU0NzI2OF8xNzgwMDU2NjY5OjE3ODAxNDMwNjlfVjM)



#### 切换分支

一个仓库中可以有多个分支，切换分支命令格式：`git checkout 分支名称`，例如：`git checkout b1`

![Image](https://internal-api-drive-stream.feishu.cn/space/api/box/stream/download/authcode/?code=YWE3M2JkOThhZDU3NGI2OGM0NzEzOTcwZjMwNmFiMzBfNDdhZDVlOWRmMWI3OGI4NjYzZTY4MWQyYzZlZmQ1ZmZfSUQ6NzUyMzE5MDU1NDA3MzQzMjA2N18xNzgwMDU2NjcwOjE3ODAxNDMwNzBfVjM)

**提示：**在命令行的后面会显示出当前所在分支，如上图所示 \(b1\)。



#### 推送分支至远程

- 推送至远程仓库分支命令格式：`git push 远程仓库简称 分支命令`

- 样例：`git push origin b1`

![Image](https://internal-api-drive-stream.feishu.cn/space/api/box/stream/download/authcode/?code=ZjEzMWM5NTllM2Q4YWI3NTJhZGYyZWQxMzFhZTJjZDdfYTYwYjM0NzA1YjA5N2NmMzIyNTVkZDMyZmJmODBkNTBfSUQ6NzUyMzE5MTMzMjQzNzk4MzIzNV8xNzgwMDU2NjY5OjE3ODAxNDMwNjlfVjM)

推送完成后可以查看远程仓库：

![Image](https://internal-api-drive-stream.feishu.cn/space/api/box/stream/download/authcode/?code=NzJlYWRlN2ExNWRiNTRiODU2ZTgyYjUxMGI0OTZmZjRfN2NiM2MyNGVkOTJkZTExOGM4MDMyNTk5NGNiN2M4MDBfSUQ6NzUyMzE5MTUyNzI1MTA5OTY1MV8xNzgwMDU2NjcwOjE3ODAxNDMwNzBfVjM)



#### 合并分支

- 合并分支就是将两个分支的文件进行合并处理，命令格式：`git merge 分支`，表示将指定分支代码合并到当前分支

- 样例：`git merge b1` \(注意: 操作之前，需要切换到master分支； 表示将b1分支的代码，合并到master分支\)

![Image](https://internal-api-drive-stream.feishu.cn/space/api/box/stream/download/authcode/?code=MGU4OTA2NTJhMjgwMjZmOGYzODFhZjBhYmJhNmEyYTVfMWU2ZDQ5Njc4N2QyOWM0MTY1YTY4ZTU5ZGRhNWYwYzhfSUQ6NzUyMzE5MjI2ODMxNzUwNzU4N18xNzgwMDU2NjY5OjE3ODAxNDMwNjlfVjM)



#### 删除分支

如果指定的分支，不需要了，可以直接将分支删除掉。

- 命令：`git branch \-d 分支名`

- 样例：`git branch \-d b1`

![Image](https://internal-api-drive-stream.feishu.cn/space/api/box/stream/download/authcode/?code=YzY1MGJlMjVjOGQ1YzUzMmViMzdmNGM4NjljMzk2M2JfM2M1OWEzNDg5MzdlZGJhMDY5OTM5OTEwNmUyMjFmZjVfSUQ6NzUyMzE5MjgwNTc3NTE5NjE2NF8xNzgwMDU2NjY5OjE3ODAxNDMwNjlfVjM)



好嘞，那到此呢，关于Git的常用操作，我们就已经学习完毕了。但是我们在项目开发中啊，一般并不会使用命令来操作Git，而是要在IDEA这样的开发工具中集成Git，对项目的代码进行版本控制。 

而关于IDEA中如何集成Git，那这个呢，我们在讲解完项目搭建之后，我们再来继承操作。



## IDEA集成Git

1\)\. IDEA关联本地安装的Git

![Image](https://internal-api-drive-stream.feishu.cn/space/api/box/stream/download/authcode/?code=ODRmNWM5Mzk0N2ExODNkMDM4YTU4Yzg0ZjkxN2NmOThfMmI0OTUyNTI5MGFlODc3MTZiNWNmODY2MWFkMTExYzlfSUQ6NzUyNDYwODc5Njc3MTgxMTMzMF8xNzgwMDU2NjcwOjE3ODAxNDMwNzBfVjM)



2\)\. 创建Git本地仓库

![Image](https://internal-api-drive-stream.feishu.cn/space/api/box/stream/download/authcode/?code=MDk4YjM3YTg3MDMyMzFiN2MyNDVkYjcwMDc5YjVmMjNfYzA1NDk2ZTZmODlhYTg5MDIzZDlhMDY0NjVkMTJjYWFfSUQ6NzUyNDYwOTUyMzU1NDkyNjU5NF8xNzgwMDU2NjY5OjE3ODAxNDMwNjlfVjM)

![Image](https://internal-api-drive-stream.feishu.cn/space/api/box/stream/download/authcode/?code=YTRhNzhlNDBiMDE4ZjZiMWVjMjM1OWU5YmU2ZjFiNGNfYTVhNDZiYmI5NjVjZmIyYzdhMTY4ZGFjY2M4ZTM2NjhfSUQ6NzUyNDYxMDA1MzA3NTc3OTU4N18xNzgwMDU2NjcwOjE3ODAxNDMwNzBfVjM)



3\)\. 将项目源代码提交到本地仓库

大家可以思考一下，我们的项目要交给Git进行版本控制，是所有的文件全部都交给Git版本控制吗 ？ 

其实并不是。 我们只需要将项目的源代码交给Git版本控制即可，其他的target、\.idea等文件夹，这些并不是项目的源代码，所以这些是不需要交给Git版本控制的。在Git中，我们可以将这些忽略的文件，统一定义在 \.gitignore文件中，git就会忽略这些文件。

定义`\.gitignore`文件，配置需要忽略的文件，`\.gitignore`文件配置如下：

```XML
target/
.idea/
*.log
*.iml
*.class
```

![Image](https://internal-api-drive-stream.feishu.cn/space/api/box/stream/download/authcode/?code=ZDcwOGRjYzk0ZjFhOTk2MDg3NGEyOTRlMWRjODg0MWRfNTY4MWIzZTUyNjQ4ODlmYTIzZDNhYzIwNTA3NjAzODhfSUQ6NzUyNDYxNTU3NjQxODIzODQ2OF8xNzgwMDU2NjY5OjE3ODAxNDMwNjlfVjM)



提交代码

![Image](https://internal-api-drive-stream.feishu.cn/space/api/box/stream/download/authcode/?code=OGM3NWFhZjVlNjViY2JlMzhiZDZlZWNlODZiYTJlNmVfOWRlYmU1YWVlMjIzOTM2MTQ3MDM3NzcxNTE3ZmVjNjZfSUQ6NzUyNDYxMDQwNTA2NDEzMDU2MV8xNzgwMDU2NjY5OjE3ODAxNDMwNjlfVjM)



![Image](https://internal-api-drive-stream.feishu.cn/space/api/box/stream/download/authcode/?code=MTYyMGFkMjk0ZjQ1NGMyYWFhMjU3M2ZiMDQxNTYyNTdfZWVkNjllODdlN2M1Nzg2NWM2YWFiODQzNzYwNTVhOTNfSUQ6NzUyNDYxNjIzNjgyMzU5Mjk2Ml8xNzgwMDU2NjcwOjE3ODAxNDMwNzBfVjM)



3\)\. 创建Git远程仓库 

![Image](https://internal-api-drive-stream.feishu.cn/space/api/box/stream/download/authcode/?code=Mjg5MDkzMmUwODA1NzFiOGM2MjI3ZGU1YTU4MjkwM2FfYTIxZTYyNTBmNzliMGZiMDlmMzBkY2U0ODk4ZTg2MzNfSUQ6NzUyNDYxNjg0NTQ0NzkwNTI5OV8xNzgwMDU2NjcwOjE3ODAxNDMwNzBfVjM)

![Image](https://internal-api-drive-stream.feishu.cn/space/api/box/stream/download/authcode/?code=NDhmNmM3NWM0NTQzZjg4MmY0OGE0MTJhZTcwMTk4NDZfNjQ1Y2U2Y2M5MmNiYjlkMDczMWFiNDljNDc3Yjg4MWRfSUQ6NzUyNDYxNzAyNTcyNzg4OTQzNl8xNzgwMDU2NjcwOjE3ODAxNDMwNzBfVjM)



4\)\. 将项目源代码推送到远程仓库

![Image](https://internal-api-drive-stream.feishu.cn/space/api/box/stream/download/authcode/?code=ZDc2NDcxOTlhMTA1MmExODJkMGUxNDc2NGY1ZjI2MzlfMjc3YzI3ZWQyMzU5ZGMxMDdmMzMzYTQzYzg5NjU0MGRfSUQ6NzUyNDYxNzE2NjY5MzMwMjI5MV8xNzgwMDU2NjY5OjE3ODAxNDMwNjlfVjM)

配置远程仓库:

![Image](https://internal-api-drive-stream.feishu.cn/space/api/box/stream/download/authcode/?code=MzMyOWEzYzlmNGEzZWFiNWQ1OTk2MjlmN2MyNDk2OTlfNzRjYjhiNTliZDhlNjYwZTQ2MDQ0OTM0ZjIwMmM4ZjVfSUQ6NzUyNDYxNzQ2MTgxMDk4NzAxMV8xNzgwMDU2NjY5OjE3ODAxNDMwNjlfVjM)

推送到远程仓库:

![Image](https://internal-api-drive-stream.feishu.cn/space/api/box/stream/download/authcode/?code=ZmU1YjdkODNlODY3ZDhlZjNkMDE0ZGRjMWFjMTg1ZGZfNjFkMTVkYzc5NTFkZDg0OWU4ZThlYTJhOWE2MWE2YWNfSUQ6NzUyNDYxNzU5MjgxNzE3MjUwOF8xNzgwMDU2NjcwOjE3ODAxNDMwNzBfVjM)



打开远程仓库，可以看到代码已经上传上来了。

![Image](https://internal-api-drive-stream.feishu.cn/space/api/box/stream/download/authcode/?code=Mjc2NGJkYzgzYjIyMjdiYjE0MTQ4YjY1NDczNTlmZWZfZjM3NTRhY2I4MGZhNGIxZWI0YTQ0YjI1ZWYxYWU3YWVfSUQ6NzUyNDYxNzgzMTE3NzA2MDM1Nl8xNzgwMDU2NjcwOjE3ODAxNDMwNzBfVjM)

## 相关笔记

- [[☕ Java笔记/Java笔记总览|Java笔记总览]]


- [[MOC-工具运维]]
