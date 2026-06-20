---
tags: [中州养老, 部署, 项目]
date: 2026-06-06
---
Day6 - 项目自动化部署



1- 入住办理业务复习

	1- 包含智能健康评估 和 入住办理

	2- 先进行智能健康评估，评估建议入住，再进行入住办理

	

2- 定时任务 - 介绍&Cron表达式

	1- 需求：当合同表 contract 的start_date 小于了 当前时间，合同状态应该由未开始 变为 已生效，这就需要用到定时任务

	2- 概念：在指定时刻执行或者需要按照固定频率执行的任务

	3- 使用场景：定时发放优惠券、定时约定的时间执行的任务短信提醒、定时进行财务数据汇总、12306定时放票 等等

	4- 实现方案：多线程sleep、JDK API、Quartz分布式任务调度框架、SpringTask、XXL-JOB等等

	5- Cron表达式学习：

		- 所有定时任务框架中都通用，用来描述定时任务执行时机的表达式，由 秒 分 时 日 月 周 年 组成

		- 特殊符号 * ？ / - ， L W #  



3- 定时任务 - SpringTask入门

	1- 导依赖(spring-context) - springboot自带了

	2- 自定义任务类，编写定时任务方法，方法上标注 @Scheduled(cron = "") 注解

		- 在 nursing/task包 下编写任务类 MyTask，方法上标注 @Scheduled 注解

		- 启动类标注 @EnableScheduling 注解 开启SpringTask

		- 启动项目测试



4- 定时任务 - 若依

	1- SpringTask 弊端：定时任务执行周期 需要写死在代码中，任务启停不方便

	2- 若依定时任务支持（系统监控 - 定时任务）

		1- nursing/task包 下 新建一个定时任务类 HelloRuoyiJob，编写定时任务方法 ruoyiJob()，交给Spring容器管理即可

		2- 菜单中新建定时任务

			1- 调用方法处配置规则借鉴问号提示：ryTask.ryParams - zzyl-quartz模块有个类 RyTask, 类中有个方法ryParams

			   所以规则为：任务类Bean对象名.定时方法名 , 所以我们配置为：helloRuoyiJob.ruoyiJob

			2- 指定cron表达式（点击右方按钮图形化界面生成）  0/5 * * * * ?

			3- 【注意】：最后确定新增会失败，提示目标字符串不在白名单内：需要将定时任务所在包路径配置在 Constants.JOB_WHITELIST_STR 中

			4- 测试：可以点击右侧的执行一次，也可以将开关打开。 另外还可以查看任务执行日志

	3- 【注意事项】：

		1- 由于执行策略默认设置的为：立即执行，所以 定时任务停止后，再启动，会将停启期间的调度 也全部执行一遍。

		   调整：可以修改执行策略为：执行一次（再次启动立即执行一次） 或 放弃执行（再次启动不会有多余的执行，只会按照规则执行）

		2- 若依定时任务不依托于 SpringTask 机制

	

5- 合同状态定时更新

	1- nursing/task包 下新建一个定时任务类 ContractJob，编写定时任务方法 updateContractStatus，重启项目（否则报新增时报bean不存在）

	2- 菜单中新建定时任务，调用方法处配置：contractJob.updateContractStatus，cron表达式：0 0 1 * * ？

	3- 测试

		- 将数据库中 contract 合同表中某条数据的 start_date 和 end_date 修改为 包含当前时间，状态修改为 0

		- 定时任务菜单，点击执行一次，查看状态 是否改为了 1



6- 自动化部署 - 代码检查插件

	1- 阿里IDEA插件 - Alibaba Java Coding Guidelines 阿里Java开发手册 

	2- 安装

		1- 在线插件市场安装

		2- 资料包离线安装包安装（2021、2024版），通过Plugins右上方小齿轮 Install Plugin from Disk

	3- Tools（阿里编码规约扫描）或者 选中待扫描包右键（阿里编码规约扫描）

		1- BLOCKER 必须要修改的

		2- CRITICAL 紧要问题，建议修复，不影响系统运行

		3- MAJOR 重要的，一般是代码不规范，不影响系统运行



7- 项目开发模式介绍

	1- 瀑布模式：每个阶段严格按照顺序依次进行：需求分析 -> 设计 -> 编码 -> 测试 -> 部署 -> 运维

	2- 敏捷开发 & DevOps



8- 项目部署 - CICD

	1- 持续集成：频繁地、一天多次将代码集成到主干

	   优点：可以快速发现错误、防止分支大幅偏离主干

	   目的：让产品可以快速迭代，同事保持高质量

	   核心：集成到主干，必须通过自动化测试（通过git history 和 代码上的 名字 都可以 看到历史变更）

	2- 持续交付：持续集成的下一步 - 频繁地将软件最新版 交付给 质量团队或者 用户，以供评审

	3- 持续部署：持续交付的下一步 - 当代码通过评审，能【自动部署 - Jenkins】到生产环境，进入生产阶段

	4- CICD流程

		IDEA开发 -> git push -> Git服务器 -> git pull -> 持续集成工具（Jenkins- 集成了maven、git） -> Jenkins-pileline 流水线

	5- Jenkins-pipelins流水线

		拉取最新代码 -> 清理、编译、测试、打包 -> 更新工程镜像 -> 停止旧服务 -> 启动部署



9- 项目部署- Jenkins介绍&安装

	1- 介绍部署环境：【git\maven\jdk】+【docker\docker-compose】+【redis\mysql】+【nginx】(除了Nginx虚拟机中都已经安装好)

		验证

		- git --version

		- mvn -v

		- java -version

		- docker ps

			

	2- 安装这些软件的 shell 脚本

	3- Jenkins介绍&安装

		- 启动：docker start jenkins

		- 访问：http://192.168.100.168:8000/ ，用户名：zzyl 密码：itcast

	



10- 项目部署 - 多环境配置

	1- application.yml 通过 profile.active 激活了 application-druid.yml

	2- 将 application-druid.yml 内容合并至 application.yml 文件，删除 application-druid.yml，验证项目能否正常启动

	3- 复制 application.yml 文件为 application-dev.yml、application-test.yml、application-prod.yml，修改test项目端口为8000，prod为9000

	4- application.yml 只保留 spring.profile.active ： prod，验证项目端口是否发生变化（前端还能否访问）



11- 项目部署 - 整体部署思路

	1- 前端部署 - Nginx（反向代理|负债均衡）

	2- 后端部署 - Jenkins



12- 后端项目部署 - Jenkins流水线介绍

	1- 概念：用于定义和执行 自动化 构建、测试和部署过程的一种方式

	2- 在声明式流水线中，整个流水线的过程被定义在一个pipeline块中，其中包含了该流水线执行所需的【所有阶段】 和 【指令】。

		1- 过程举例：开始 -> 切换分支 -> 工具安装（maven|jdk） -> 清理workspace -> 拉取Git代码 -> maven打包 -> 构建镜像 -> 部署服务 -> 后置行为 -> 结束 

		2- 指令举例

			pipeline {  

				agent any // 指定流水线运行的节点，any 表示该流水线可以运行在任何可用的节点上  

				stages {  

					stage('Stage Name1') { // 定义该流水线的阶段 1 

						steps {  

							// 定义该阶段执行的步骤  

							echo 'Hello, World!'   

						}  

					},

					stage('Stage Name2') { // 定义该流水线的阶段 2 

						steps {

							// 定义该阶段执行的步骤  

							echo 'Hello, World!'  

						}

					}

				}

			}

					

13- 后端项目部署 - Jenkins流水线配置

	1- 新家流水线 - 名称：zzyl-admin  类型：流水线   

					描述：中州养老后端部署流水线

					选择：参数化构建过程-Extend Choice Paramter，填写：

		1- name：services

		2- Description：请选择您要部署的服务

		3- 选择 Basic Parameter Types - Check Boxes    

			1- Delimiter：,

			2- Choose Source for value: zzyl-admin

		4- 添加参数 - 字符参数

			1- 名称：GIT_URL

			2- 默认值：git仓库地址

		5- 添加参数 - List Git branch

			1- Name：GIT_TAG

			2- Description：请选择Tag或者Branch部署：

			3- Repository URL：git仓库地址

			4- Credentials: 添加 - Jenkins

				1- Domain：选择全局凭证

				2- 用户名：liuweidong0008@163.com

				3- 密码: xxx

				4- ID：Gitee_ID

			5- 回来选择上新建的凭证 liuweidong0008@163.com/***

			6- Paramter Type选择: Branch Or Tag 

		6- 添加参数 - 字符参数

			1- 名称：DOCKER_TAG

			2- 默认值：V1.0

		7- 保存

	2- 左侧菜单 - 配置 - 流水线

		1- 选择：Pipeline script from SCM

			1- SCM选择：Git

				1- Repository URL：git仓库地址

				2- Credentials: 选择 之前建的凭证

				3- 最下面脚本路径：Jenkinsfile

			2- 应用保存

	3- Dashboard 首页查看验证 - zzyl-admin

		1- 点进去查看任务详情

		2- 点击左侧带单 Build with Parameters

		



14- 后端项目部署 - 代码中流水线配置

	1- 解读 Jenkinsfile（放在项目根目录）

		1- stage1 - 清理工作空间

		2- stage2 - 拉取Git代码

			1- 打印: 当前分支：${GIT_TAG}、当前服务：${services}

			2- 指定: 检出分支：GIT_TAG、用户名密码凭证：Gitee_ID、Git地址：GIT_URL

		3- stage3 - maven打包

			1- sh "mvn clean install -DskipTests"

		4- stage4 - 构建镜像

			1- 打印: 镜像名称：${DOCKER_TAG}

			2- 指定: 模块名称：${ds}为项目名 zzyl-admin、镜像名称：${DOCKER_TAG}、dockerfile位置（zzyl-admin下）

			3- 执行：sh "cd ./${ds}/target/ && docker build -t ${ds}:${DOCKER_TAG} -f ../Dockerfile ."

		5- stage5- 部署服务

			1- 打印：服务名称：${ws} 为项目名 zzyl-admin

			2- 指定: 服务名称：${ws} 为项目名 zzyl-admin、镜像名称：${DOCKER_TAG}

			3- 执行：sh "chmod +x ./${ws}/deploy.sh && sh ./${ws}/deploy.sh ${ws} ${DOCKER_TAG}"，其中最后的 ${ws} ${DOCKER_TAG}为传进去的两个参数

		6- post - 打印：任务构建完毕



	2- 将 Jenkinsfile 放在项目根目录

	3- zzyl-admin 目录下 新建 Dockerfile 和 deploy.sh 

	3- 从在线讲义拷贝 Dockerfile和 deploy.sh内容，其中  Dockerfile 需要配置 阿里OSS的 ID 和 SECRET 的环境变量

	4- 修改 application-prod.yml 中数据库和 redis的地址为 ：192.168.100.168, redis 密码 为 123456

	5- commit & push

	6- 刷新 Jenkins 发现 zzyl-admin 流水线左侧菜单 Build with Parameters GIT_TAG 能看到 master 分支了

	



15- 后端项目部署 - 执行部署

	zzyl-admin 流水线左侧菜单 Build with Parameters 

	1- 勾选 zzyl-admin

	2- 选择分支 master

	3- 点击build 根据根目录下的流水线文件 Jenkinsfile 开始构建 - 到首页查看构建日志 - 直到最后success（持续大概2分钟）

	4- 测试：将前端 vite.config.js 后端代理的target 地址修改为 ：http://192.168.100.168:9000 重启本地前端，测试 localhost 是否能正常登录访问 



16- 前端项目部署

	1- 前端项目打包 

		1- 多环境介绍

			1- env.development 开发环境

			2- evn.prodution 生产环境

			3- env.staging 预发布/测试环境 

		2- 打包：

			1- 点击vs code npm脚本中的 build:prod 进行打包，本质上就是执行命令：npm run build:prod，使用的是 evn.prodution 文件

			2- 打包完成 会生成 【dist】 目录，由于 vite.config.js 中配置 了 VITE_BUILD_COMPRESS = gzip，所以 dist 目录中的文件进行了压缩

			

	2- 创建 nginx 容器 

		docker run -d \

		--name zzyl-vue \

		-v /usr/local/zzyl-vue/html:/usr/share/nginx/html \

		-v /usr/local/zzyl-vue/conf:/etc/nginx/conf.d \

		-v /usr/local/zzyl-vue/logs:/var/log/nginx \

		-p 80:80 \

		nginx:latest

		

	3- 将 前端打好的包 放入 /usr/local/zzyl-vue/html 目录，挂载至容器内部

	4- 将 day9课程资料中的 zzyl-vue.conf 文件放入 /usr/local/zzyl-vue/conf 目录，挂载至容器内部

	5- 重启容器：docker restart zzyl-vue

	6- 测试：访问 192.168.100.168 进入系统测试功能是否正常，测试护理项目图片能否正常上传（F12查看OSS图片上传地址）

	

17- 日志 - 查看容器日志

	1- 查看解读 zzyl-admin 下 logback.xml 配置的日志规则

		1- 日志文件 存放位置： /home/ruoyi/logs

		2- 日志输出格式 - 对照日志文件看

		3- 4个 appender：console、file_info、file_error、sys-user（AsyncFactory.sys_user_logger）（包括日志滚动规则）

	2- 日志文件查看

		1- windows：D://home/ruoyi/logs

		2- Linux: 

			- docker方式：docker logs -f zzyl-admin

			- 文件方式：需要到容器内部home/ruoyi/logs目录看，但是 deploy.sh 创建容器时已经挂载出来了

				- 目录：/usr/local/zzyl-admin/logs

				- 查看命令：cat、tail、less、grep 等等

		

18- 日志 - ELK日志管理

	1- 介绍 ELK 成员 

		1- ElasticSearch：一款基于Lucene的搜索引擎，存储 和 搜索日志数据（搜索快速高效）

		2- Logstash：一款 日志收集 和 清洗转换增强的工具，可从各种数据源（文件、数据库、网络）中收集日志，并将数据转化成ES可理解的格式

		3- Kibana：用于可视化展示日志

		

	2- 介绍工作流程

		1- Logstash 动态收集、筛选、过滤 来自于分布式部署的后端日志

		2- Logstash 收集处理后的 日志交给 ElasticSearch 进行存储、搜索、分析

		3- ElasticSearch 中的日志 交给 Kibana 进行 可视化展示、搜索

		

	3- 环境装备

		1- 启动容器： docker start es kibana logstash

		2- zzyl-admin模块中引入logstash相关的依赖

			<dependency>

				<groupId>net.logstash.logback</groupId>

				<artifactId>logstash-logback-encoder</artifactId>

				<version>6.6</version>

			</dependency>

		3- zzyl-admin模块新增日志文件：logback-logstash.xml，内容见在线讲义

			- 对比logback.xml 添加了 logstash 的 appender

			- 该 appender 中通过<destination> 指定了 logstash的服务地址和端口：192.168.100.168:5044

		4- 集成 logback-logstash.xml 

			1- 由于目前使用的是 application.prod 文件（生产环境），所以在该文件中集成，添加如下配置

				logging:

					config: classpath:logback-logstash.xml

		5- 重启后端项目

		6- 前端配置 vite.config.js 的 target地址：localhost:9000，重启

		7- 浏览器访问 多个模块（正常的 | 非正常的），产生日志会自动上报至 logstash

		

	4- ELK查看日志

		1- 访问kibana: http://192.168.100.168:5601/ 

		2- 索引管理 

		   1- 点击 左侧菜单 - Management -> Stack Management -> 索引管理 （或者右上角的 管理 -> 索引管理）

		   2- 可以看到，日志文件都是按照日期进行区分的，每天一个日志索引文件，可以点进去查看当天的索引映射

		3- 添加索引模式 

		   1- 如果想用kibana方便的查看日志的数据，可以添加索引模式

		   2- 点击 左侧菜单的 索引模式 -> 创建索引模式 -> 输入 log-2025.08.20*

		   3- 能看到完全匹配了 log-2025.08.20 这个索引，点击【下一步】，【时间字段】选择 【@timestamp】 -> 【创建】，能看到索引映射中的所有字段

		4- 检索日志 

		   1- 打开左侧菜单 -> Analytics -> Discover

		   2- 第二行 搜索栏可输入 搜索条件 进行日志搜索，同时右侧还可选择 时间范围 -> 

				1- * 匹配任意多个字符、 ？匹配单个字符

				2- ：等值匹配、：* 匹配任意形式、and 、or

				3- 示例

					如：level.keyword : ERROR and  message.keyword :  请求参数类型*  

					解读：匹配查询 "level.keyword" 等于 "ERROR" 并且 "message.keyword" 等于 "请求参数类型" 开头 的所有日志

					

					如：message.keyword : *listByDeptId*

					解读：匹配 message.keyword 包含 listByDeptId 关键字的所有日志

					

					如：@timestamp < "2024"  @timestamp < "2024-09"  @timestamp:"2024-09-05"   @timestamp < "2024-09-02T21:55:59.484" 

					解决：根据日志时间查询



19- 作业

	1- 合同状态自动更新

	2- 项目部署 - 自行体验一遍即可

	3- 开通小程序测试号、安装微信小程序开发工具

## 相关笔记

- [[📖 中州养老课程文档/中州养老课程总览|中州养老课程总览]]
