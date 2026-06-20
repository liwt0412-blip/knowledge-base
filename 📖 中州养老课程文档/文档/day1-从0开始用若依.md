---
tags: [中州养老, 若依, 项目]
date: 2026-06-06
---
Day1- 从0开始用若依



1、项目介绍&课程目标

	1- 为什么基于若依框架开发：快速开发、高度可定制、简化开发流程、易于维护和管理、社区支持更新迭代、工作需求

	2- 学习目标：

		1- 掌握项目核心业务流程、系统和技术架构

		2- 熟悉若依框架，包括功能、版本、特性等

		3- 能独立完成若依框架的前后端项目环境搭建

		4- 掌握前后端代码的结构及作用

		5- 能独立完成若依框架的代码生成的功能，完成单表CRUD

	

2、项目背景&技术架构

	1- 背景

		1- 国内老龄化程度日益加重，养老服务行业爆发式增长背景下 诞生的服务于养老院的智慧养老平台

		2- 2020年开始，养老行业的市场规模每年都以16%左右的增长比发展，2025年16万亿，预计2027年21万亿

	2- 业务流程：参观预约、到院参观、办理入退住、请假销假...

	3- 原型简单介绍：管理后台端（养老院员工使用）、家属端（老人家属使用- 查看老人信息、缴费、下单）

	4- 技术架构：

		展现层（vue\ElementPlus）、接入层（Nginx反向代理、负载均衡）、服务层（StringBoot、MVC、SpringCache、Knife4j、Mp、WebSocket）

		数据层（Mysql、Redis）、第三方（若依、华为IOT、阿里云OSS、百度千帆、通义灵码、禅道）

	

3- 若依框架介绍

	1- 介绍：一款基于Spring Boot、Spring Cloud等开源框架搭建的企业级开发平台    

	2- 目标：提供全面的解决方案，以简化企业级应用开发，提高开发效率

	3- 特点：模块化设计、前后端分离、权限管理、代码生成器、定时任务、易于集成

	4- 具体查看官方文档

	

4- 若依框架技术选型

	1- 选型：RuoYi-Vue - 一个 Java EE 企业级快速开发平台

	2- 技术选型：

		- Java EE 8   ---> jdk 11

		- Apache Maven 3 ---> 使用IDEA自带的Bundled (Maven 3) - idea安装目录-> plugins -> maven -> lib -> maven3

		- Apache MyBatis 3.5.x  ---> MyBatis Plus

		- Vue 2.6.x   ---->  Vue3		

		- Element 2.15.x     ---->  Element Plus



5、环境搭建-准备工作

	1- JDK：安装资料包中提供的JDK11

	2- Maven：IDEA自带的- 3.9.8（不用频繁修改maven配置，解决了一些兼容性问题）

		- 默认的setting文件和本地仓库配置在了 C:\Users\Administrator\.m2 中：桌面右键 -> 主题 -> 桌面图标设置

		- 将资料包中的【Maven配置文件、清理脚本、相关依赖】文件夹下setting.xml（已配置好阿里云） 和 del_lastUpdated.bat文件拷贝至 C:\Users\Administrator\.m2 下

	3- NodeJS - > 18, 目前安装的资料包提供的Node20 （node -v    npm -v）

	4- Mysql\Redis: 安装在了虚拟机

	

	5- 导入课程资料提供的虚拟机（前期主要是Mysql 和 Redis，前期可不使用虚拟机，Mysql和Redis部署在本地）

		- IP为：192.168.100.168 配置VMWare 网卡网段为192.168.100.0

		- 用户名密码：root/1234

		- Mysql用户名密码：root/heima123 端口 3306

		- Redis密码：123456  端口 6379



6、后端环境搭建

	1- 官网指定地址下载ZIP包源码（RuoYi-Vue前后端分离版）：https://gitee.com/y_project/RuoYi-Vue

	2- 剪切至桌面，双击打开发现所有包名、模块名，都是若依开头，包括数据库连接信息，很多地方需要定制化，这需要用到 【若依修改器-资料包已提供】

	3- 打开资料文件里提供的的若依修改器官网：https://gitee.com/lpf_project/RuoYi-MT/releases，查看其作用

	4- 打开【若依修改器】开始修改

		1- 选择zip包、RuoYi-Vue版本

		2- 目录名、项目名、artifactId 均为 zzyl

		3- 包名、groupId为 com.zzyl

		4- 站点名称为 中州养老

		5- 文件 -> 配置参数：

			- 数据库配置：是否启用配置为True、IP地址为：192.168.100.168，端口号3306、名称zzyl、账号root、密码 heima123

			- Redis配置：IP地址 192.168.100.168、端口号 6379、密码 123456

		6- 开始执行，桌面上会生成一个文件夹，剪切内部的zzyl并用IDEA打开

	5- 确认项目名、包名、数据库配置、Reids配置 有没有问题，发现【Redis密码没有设置】，改一下：123456

	6- 修改项目JDK版本为11，其中moudles每个模块都要改为JDK11，麻烦，快捷修改：修改pom文件的 <java.version> 为 11，刷新即可

	7- 解压资料里提供的maven仓库到 .m2/repository (也可以自己下载)

	8- Idea settings中，搜索encoding，修改文件编码为 UTF-8

	

7、运行后端项目

	1- 导入SQL

		1- 修改sql目录中sql脚本，第一行添加：create database if not exists zzyl_day1; use zzyl_day1;

		2- IDEA导入sql

	2- 启动类启动，访问localhost:8080 验证

	3- Git托管-推送至远程仓库



8、运行前端项目

	1- 项目自带的zzyl-vue模块，是基于vue2开发的，我们使用vue3版本，若依前后端分离版，查找到同步更新 前端版代码

		1- 链接：https://gitcode.com/yangzongzhuan/RuoYi-Vue3

		2- 建议使用资料包提供的：【前端初始代码】目录中的RuoYi-Vue3-master，在官方基础上修复了一些Bug

		3- 解压到自己代码目录，改名为 zzyl-vue

	2- zzyl-vue根目录，cmd -> code . 用vscode打开

	3- 下载依赖：alt+F12打开终端输入：【npm install】

	4- vite.config.js 配置 target 代理地址为：http://localhost:8080

	5- 启动项目：终端 【npm run dev】，或者NPM脚本点击按钮启动、package.json调试启动 都可以

	6- 访问 localhost:80 测试

	7- 托管至Git

		1- git init  

		2- git remote add origin 远程仓库地址

		3- git add .

		4- git commit -m "Day1 - 项目初始化代码"

		5- git push origin master

		6- git branch -b dev0926 (git branch + git checkout)

		7- git branch -avv 查看所有分支

		8- git push origin dev0926



9、熟悉后端代码

	1- 根 pom 文件依赖及对应版本

	2- zzyl-admin - web模块 - controller层，如：验证码图片接口

	3- zzyl-system - 系统模块 - service、mapper层，以及domain

	4- zzyl-common - 公共模块 - 工具类、配置、常量、过滤器、枚举、注解、异常处理、core（BaseController）、公共Result

	5- zzyl-framework - 框架模块 - 切面（日志、数据源、数据权限）、配置（图形验证码、mybatis、redis、security、线程池）

	6- zzyl-generator - 代码生成模块 - 前后端

	7- zzyl-quartz - 定时任务模块

	8- 模块间的依赖关系

		admin -> framework -> system -> common

			  -> generator -> common

			  -> quartz -> common



10、后端配置 & 表结构

	1- application-druid.yml - 数据库配置

	2- application.yml - 

		- 若依配置：版本、版权年份、本地存储文件路径、是否获取IP地址开关、图形验证码类型

		- 环境配置：端口、日志

		- 用户配置：密码错误最大重试次数 5、密码锁定时间 10分钟

		- Spring配置：i18n、激活环境 druid、文件上传大小限制 10M 20M、热部署开关 true、redis配置

		- token配置： token请求头名字 Authorization、秘钥、有效期 30分钟

		- mybatis配置： 别名包、mapper.xml位置、全局配置文件位置

		- pagehelper配置

		- swagger配置：是否开启 true、请求路径 /dev-api

	3、表结构

		- 默认19张表：基本都不会去动（ge 代码生成、sys-dict 数据字典、sys-job 定时任务、sys-log 日志、sys_xx权限）

		

11、熟悉前端代码

	1- 代码结构

		1- vite.config.js : vue项目的核心配置信息，如前端端口号 80、访问前缀 /dev-api、后端访问代理地址 localhost:8080 等

		2- package.json : 项目配置文件，包括项目名、版本号、依赖、版本等

		3- node_moudles：下载的第三方包存放目录

		4- src：源代码目录

			1- main.js ：入口文件

			2- App.vue ：根组件

			3- components：组件目录，存放通用组件

			4- assets：静态资源目录，存放图片、字体等

			5- *.vue：是vue项目中的组件文件，也称为单文件组件，会将一个组件的逻辑（JS）、模版（HTML）、样式（CSS）封装在同一个文件中

			6- router：index.js 路由

			7- views：我们的主战场，如：monitor/job/index.vue 逐个查看结构 template、script setup、style

			

	2- 以 monitor/job/index.vue 为例查看代码

		1- template：elementplus各个组件：表单、行、表格、对话框，包括VUE 各种指令 v-model v-bind v-on v-for v-show v-if

		2- script setup：

			1- 组合式API写法、ref声明响应式数据模型

			2- function getList：发起异步请求，listJob方法 从 @/api/monitor/job 导入

				3- job.js 中方法的写法（url、method、params），request方法从 @/utils/request 导入

					4- request.js 中 创建了axios实例，请求前缀在meta.env.VITE_APP_BASE_API变量中声明

						5- VITE_APP_BASE_API变量跟环境有关，配在环境文件中的，npm run dev使用的是 .env.development文件，build:prod 使用的是 .env.production 文件

			3- @ 和 ~ 指向地址 是在	 vite.config.js 文件中配置



12、功能快速开发 - 护理项目

	1- 系统工具 - 代码生成 模块，以 sys_dict_data 为例看一下生成的代码，其中SQL这块，需要说明【字典数据表】代码生成会生成二级菜单，但是父菜单需要自己创建

	2- 创建【服务管理】父菜单

		- 系统管理 - 菜单管理 - 新增

			菜单类型：【目录】   排序：0  菜单名称：【服务管理】  非外链  路由地址：【serve】  显示状态、菜单状态：正常

		- 刷新验证菜单

	3- 创建 护理项目 的表结构：nursing_project

	4- 代码生成

		- 系统工具 - 代码生成 : 导入 nursing_project，右侧按钮 （预览、编辑、删除、同步-表结构发生了变化使用、下载）

		- 点击编辑按钮

			- 基本信息

				表名称、表描述、实体类名称、作者 ruoyi、备注 无  (通常保持默认即可，无需修改)

			- 字段信息

				- 表信息   

					- 序号、表字段列名、表字段描述、表字段物理类型

				- Java实体 

					- Java类型【字段为int类型的要从Long改为Integer】、Java属性名

				- 数据库

					- 是否插入：向数据库插入时是否需要用户指定值，通常 id、创建人、更新人、备注、创建时间、更新时间不需要

					- 是否编辑：向数据库修改时是否需要用户指定值，通常 id、创建人、更新人、备注、创建时间、更新时间不需要

				- 前端

					- 是否列表：前端页面分页列表中是否展示该值

					- 是否查询：前端页面条件查询表单 是否生成该项 的控件（该值是否参与 条件 查询）

					- 查询方式：如果参与查询，数据库查询时，如何进行匹配（如，like？ =？）

					- 是否必填：新增、修改时，表单中是否是必填

					- 显示类型：新增、修改的表单控件类型（文本框、下拉框、日期控件、图片上传、文件上传等等）

					- 字典类型：对应的在若依中新建的字典类型

			- 生成信息

				- 生成模板：单表、多表							   - 前端类型：Vue3 ElementPlus模板

				- 生成包路径：com.zzyl.serve（后端包路径）		   - 生成模块名：serve（决定前端 view 和 api下的 目录名）

				- 生成业务名：project（决定views/模块名下的业务目录名 和 api/模块名下的js名）  - 生成功能名：护理项目

				- 生成代码方式：zip压缩包						   - 上级菜单：勾选上级菜单

				

			

	5- 生成代码，拿到压缩包解压，结构

		- projectMenu.sql

		- main

			- java

			- resources

		- vue

			- api

				- serve

					- project.js

			- views

				- serve

					- project

						- index.vue

		- 1、执行sql文件：创建该业务（护理项目）菜单 和 对应按钮（查询、新增、修改、删除、导出） 至 sys_menu表

			- 系统管理 - 菜单管理 - 服务管理 - 护理项目菜单 - 修改：

				- 可以看到：路由地址【project】、组件路径【server/project/index】 权限字符【serve:project:list】

				- 修改一下图标

		- 2、拷贝 main目录下的 java 和 resource 目录至 zzyl 的 main目录下

		- 3、拷贝 vue/views/serve 目录至 zzyl-vue 的 views 目录下

		- 4、拷贝 vue/api/serve 目录至 zzyl-vue 的 api 目录下

		- 5、重启项目，测试护理项目模块 CRUD	

		

13- 若依生成的后端代码解读

		

14- 若依生成的前端代码解读

	



15- 今日作业 

	1- 新建 zzyl-nursing-platform 模块，把 serve 护理项目模块代码挪过来

	2- 快速开发【护理计划】、【护理等级】模块

		1- 导入SQL

			-- 护理项目护理计划关系表

			CREATE TABLE `nursing_project_plan` (

				`id` bigint NOT NULL AUTO_INCREMENT,

				`plan_id` bigint NOT NULL COMMENT '计划id',

				`project_id` bigint NOT NULL COMMENT '项目id',

				`execute_time` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '计划执行时间',

				`execute_cycle` int NOT NULL COMMENT '执行周期 0 天 1 周 2月',

				`execute_frequency` int NOT NULL COMMENT '执行频次',

				`create_time` datetime DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',

				`update_time` datetime DEFAULT CURRENT_TIMESTAMP COMMENT '更新时间',

				`create_by` bigint DEFAULT NULL COMMENT '创建人id',

				`update_by` bigint DEFAULT NULL COMMENT '更新人id',

				`remark` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '备注',

				PRIMARY KEY (`id`) USING BTREE

			) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci ROW_FORMAT=DYNAMIC COMMENT='护理计划和项目关联表';



			-- 护理计划表

			CREATE TABLE `nursing_plan` (

				`id` bigint NOT NULL AUTO_INCREMENT COMMENT '编号',

				`sort_no` int DEFAULT NULL COMMENT '排序号',

				`plan_name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL DEFAULT '' COMMENT '名称',

				`status` tinyint NOT NULL DEFAULT '0' COMMENT '状态（0禁用 1启用）',

				`create_time` datetime DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',

				`update_time` datetime DEFAULT CURRENT_TIMESTAMP COMMENT '更新时间',

				`create_by` bigint DEFAULT NULL COMMENT '创建人id',

				`update_by` bigint DEFAULT NULL COMMENT '更新人id',

				`remark` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '备注',

				PRIMARY KEY (`id`) USING BTREE,

				UNIQUE KEY `plan_name` (`plan_name`) USING BTREE

			) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci ROW_FORMAT=DYNAMIC COMMENT='护理计划表';



			-- 护理等级表

			CREATE TABLE `nursing_level` (

				 `id` bigint NOT NULL AUTO_INCREMENT COMMENT '主键ID',

				 `name` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '等级名称',

				 `lplan_id` bigint NOT NULL COMMENT '护理计划ID',

				 `fee` decimal(10,2) NOT NULL COMMENT '护理费用',

				 `status` tinyint(1) NOT NULL DEFAULT '1' COMMENT '状态（0：禁用，1：启用）',

				 `description` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '等级说明',

				 `remark` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '备注',

				 `create_time` datetime DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',

				 `update_time` datetime DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',

				 `create_by` bigint DEFAULT NULL COMMENT '创建人id',

				 `update_by` bigint DEFAULT NULL COMMENT '更新人id',

				 PRIMARY KEY (`id`) USING BTREE,

				 UNIQUE KEY `name` (`name`) USING BTREE

			) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci ROW_FORMAT=DYNAMIC COMMENT='护理等级表';

			

	2- 代码生成

	3- 执行SQL，前后端代码 分别导入至IDEA、vscode

## 相关笔记

- [[📖 中州养老课程文档/中州养老课程总览|中州养老课程总览]]
