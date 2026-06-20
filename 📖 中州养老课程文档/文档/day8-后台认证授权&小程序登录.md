---
tags: [中州养老, 项目]
date: 2026-06-06
---
Day7 - 后台认证授权、小程序登录



1- RBAC权限模型

	1- 今日内容介绍

		1- RBAC权限模型学习（包括业务和表关系）

		2- Spring Security 安全认证 和 权限认证

		3- 第三方接口调用方式

		4- 微信登录功能开发

		5- 校验token编码

	2- RBAC （Role Based Access Control）

		1- 概念：基于角色的访问控制，主要思想是 将多个功能（菜单）打包组合成一个角色，再将角色分配给用户，也就是说角色是功能的合集

		2- 优势：

			- 解耦用户 和 功能（菜单），降低操作错误率

			- 降低功能权限分配的繁琐程度

	3- ER图梳理RBAC模型关系（5张表）

		1- 通过 简图 分析即可，重点关注红色部分

		2- 用户表、角色表、功能表

			1- Menu：菜单表

			2- Role：角色表

			3- User：用户表

		3- 用户与角色的中间表（多对多）、角色与功能的中间表（多对多）

			1- Role_User 角色用户中间表：根据用户ID查询到多个角色ID

			2- Role_Menu 角色菜单中间表：根据角色ID查询到多个菜单ID -> 根据多个菜单ID去Menu表找到多个权限标识符

		4- 岗位与用户 多对多

		5- 部门与用户 一对多

		6- 部门与角色 多对多

		

2- SpringSecurity介绍

	1- 概念：一款基于Spring的安全性解决方案框架，主要包括 登录认证 与  登录之后的授权&校验、攻击防范、会话管理等

	2- 官网：结合Spring官网介绍，结合overview第一段：spring security是一款强大、高度定制化 认证与授权框架，它是一套基于spring基础应用的实际标准

	  		 spring security是一套专注于提供 认证与授权的Java框架

	3- 使用流程：结合讲义流程图

		1- 认证：访问登录接口 -> 校验验证码、用户名密码 -> 查询用户权限列表(权限标识符) ->  生成jwt令牌 -> 登录成功返回jwt

		2- 授权&校验：其他请求 -> 校验url是否需要拦截 -> 需要，校验token是否有效 -> 无效401，有效，校验是否有权限访问当前url -> 无权限401，有权限 -> 放行

		

3- SpringSecurity权限控制-登录认证

	1- 认证 Authentication，本质上就是登录

	2- 过程：访问登录接口 -> 校验验证码、用户名是否存在、密码是否正确、长度是否合理、是否在黑名单范围内 -> 

	        【spring security认证管理器】 -> 根据用户名密码查询用户 -> 查询用户具有的权限列表（权限标识-通过菜单看一下，管理员为 *;*;*） ->

			用户认证是否成功 -> 成功，生成jwt token

	3- 断点梳理源码流程 - SysLoginController.login()

		1、校验图形验证码是否正确

		2、登录前置校验 - loginPreCheck()

			1）、校验用户名密码是否为空、长度是否符合

			2）、校验用户名密码长度是否合理

			3）、校验当前用户IP是否在 IP 黑名单范围内

			以上任意一个校验不通过，异步记录登录失败日志(原因不一样)，并抛出对应异常

		3、调用SpringSecurity体系的AuthenticationManager对象进行权限认证 - authenticate()

        4、authenticate()底层会调用若依重写 SpringSecurity UserDetailsService 接口的实现类（UserDetailsServiceImpl）- 关键

			1）、验证用户是否存在

			2）、验证用户是否删除

			3）、验证用户是否禁用

			4）、验证密码是否正确

			5）、查询用户所具备的权限集合（权限标识符）

			6）、构建一个完整的LoginUser对象，将权限标识集合赋值给该对象并返回

		5、线程池异步记录 登录成功日志

		6、创建Token

			1）、生成一个UUID：001

			2）、以 login_tokens:001 为key，以LoginUser对象为value，将用户一切信息放入redis缓存，

			3）、生成JWT Token,以 login_user_key 为key，以001为value，存入JWT Token 的 payload负载部分 并设置有效期（若依默认配置30分钟，我们已修改为 30000）

			4）、将 token 返回前端

	

4- SpringSecurity权限控制-授权(RBAC)

	0- 概念 - 用户登录认证后，控制用户是否有权限访问 某些资源

	1- 登录时，会依次访问 SysLoginController.login()、.getInfo()、.getRouters()

	2- getInfo()：获取当前用户 权限、角色、当前用户基础信息

	3- getRouters()：获取路由组件关系（包括菜单列表）

	4- 演示创建用户 - 授权

		1- 系统管理 - 角色管理 - 修改普通角色 - 添加上【服务管理】权限

		2- 系统管理 - 用户管理 - 添加用户

			用户名：zhangsan   密码：zhangsan123   角色：普通角色    

		3- 使用 zhangsan 登录

			现象：左侧菜单少了很多 、F12 getRouters 返回的菜单少了很多、 getInfo中的 permissions 权限标识符 也发生变化，不再是 *;*;*, 而是一个集合

		

5- SpringSecurity权限控制-权限校验

	1- 流程&背景：发起请求 -> 校验url是否需要拦截 -> 需要，校验token是否有效 -> 无效401，有效，校验是否有权限访问当前url -> 无权限401，有权限 -> 放行

	   在若依中，上述流程的 控制是 借助 SpringSecurity 实现，若依中有个 SpringSecurity 的核心配置类：SecurityConfig

	2- 原理

		1- SecurityConfig：校验当前URL是否需要放行，配置了需要放行的资源（注册、验证码、登录、静态资源、swagger）

		2- 经过SecurityConfig配置了token过滤器

			1、从请求头拿到token

			2、解析token是否合法

			3、根据login_user_key拿到负载部分的uuid 001

			4、拼接login_tokens:001，根据这个key拿到redis存储的LoginUser对象

			5、如果LoginUser对象不为空，为缓存中的LoginUser对象续期，如果生存时间小于20分钟，更新续期时间为30分钟

			6、将LoginUser对象放入SpringSecurity上下文中

		3- 具体功能的权限校验

			1、后续将访问某一个controller的某一个方法，方法上打上了SpringSecurity核心注解 @PreAuthorize

			2、这个注解中定义了一个表达式：@ss.hasPermi('serve:project:remove')

			3、表达式将返回一个boolean，如果为true证明有权限访问，如果为false，提示没有权限，其中hasPermi校验逻辑为：

				1、去SpringSecurity上下文中拿到当前登录人对象：LoginUser

				2、判断该对象的权限集合set中是否包含 *:*:* 或者 表达式传入的 权限标识符(serve:project:remove)

				3、如果包含返回true，否则false

	3- 断点测试（zhangsan 用户）

		1- 登录

			- 断点经过 JwtAuthenticationTokenFilter.doFilterInternal（放行）

		2- 访问功能URL，如 获取护理项目详细信息 getInfo

			- 断点经过 JwtAuthenticationTokenFilter.doFilterInternal 进行token校验（见5.2.2）

			- 断点经过 PermissionService.hasPermi('serve:project:query') 进行权限校验

			- 断点经过 NursingProjectController.getInfo()

			

			- 如果将 NursingProjectController.getInfo() 上的 权限标识符改为：serve:project:query22，重启测试，报无权限

		3- 退出登录

			- 断点经过 LogoutSuccessHandlerImpl.onLogoutSuccess



6- 三方接口 和 Hutool 工具包简介

	1- 三方接口调用介绍：结合 微信登录接口 介绍 什么是第三方接口 以及 调用的接口关键四要素

	2- 三方接口调用技术：Http请求客户端（很多）：

		- Hutool（推荐）：轻量级、简单易用 - 结合官方文档介绍（针对JDK自带的 HttpUrlConnection 做的封装，使Http请求无比简单）

		- HttpClient：包体量庞大、API难用、JDK11以上支持不太好

		- OkHttp：学习成本较高

		- Spring的RestTemplate：后期学

	

7- HttpUtil发起Get请求

	zzyl-admin 新建 HutoolHttpTest 测试类编写测试代码

	1- 向百度发起 get 请求

	2- 向本项目发起 查询护理项目 分页列表 的 get 请求

	3- 向本项目发起 查询护理项目 分页列表 的 get 请求，携带token



8- HttpUtil发起Post请求

	1- 向本项目发起 新增护理项目 的 post 请求

	2- 向本项目发起 新增护理项目 的 post 请求，携带token



	3- 导入 HttpClientUtil 和 HttpClientTest 演示使用 HttpClient 实现一样的效果

	

9- 微信登录-需求分析&小程序环境准备

	1- 小程序登录原型分析 & 在线讲义登录流程分析

	2- 小程序环境搭建

		1- 安装小程序开发工具 - https://developers.weixin.qq.com/miniprogram/dev/devtools/stable.html（资料包已有 - 可更新至最新版）

		2- 导入 Day10 资料下的 小程序代码 mp-weixin， APPID 选择 测试号的那个, 不使用云服务

		3- 选择机型、介绍小程序开发工具 界面、勾选不校验合法域名  

	3- 问题解决

		- 定位到首页，小程序总是会自动跳转到 登录页，原因是因为 首页会自动访问/member/roomTypes，后端报401没有权限（根路径配置在 utils/env.js中的）

		- 解决：在 SecurityConfig 类中 将 /member/** 添加到 放行URL中

		- 重启测试 - 一直停留在首页，问题得到解决，只是 roomType 接口报 404

		- 解决：在controller包下 建 member 包，将资料中的 MemberRoomTypeController.java 拷入，重启测试，解决 



10- 微信登录-思路分析

	1- 根据 微信官方的 时序图 和 点击登录按钮前端发送的数据 介绍微信登录思路（三个角色：小程序、开发者服务器、微信服务器 ）

	2- 微信登录本质：拿授权code 去换 openId

		1、微信小程序（外卖） 

			每一个用户在该小程序的唯一标识（openId）

		2、OpenId的意义

			1、能够唯一标识在当前小程序的身份

			2、可以与我们后台维护的用户产生关联（记录：用户昵称、头像、id、openId）

			3、后续调用微信功能，都要用到这个openId

		3、如何获取openId？

			1、用户点了授权	

			2、微信小程序调用一个login接口，获取用户的授权码：code

			3、前端拿着code，调用后端接口（后端微信登录）

	3- 将openId 与 我们后台用户进行关联

	4- 介绍什么是 unionId：某个用户在整个微信开放平台下的 唯一标识

	

11- 微信登录-表结构&接口说明

	1- 表名：family_member（家属）

		CREATE TABLE `family_member` (

		  `id` BIGINT NOT NULL AUTO_INCREMENT COMMENT '主键',

		  `phone` VARCHAR(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '手机号',

		  `name` VARCHAR(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '名称',

		  `avatar` VARCHAR(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '头像',

		  `open_id` VARCHAR(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT 'OpenID',

		  `gender` INT DEFAULT NULL COMMENT '性别(0:男，1:女)',

		  `create_time` TIMESTAMP NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',

		  `update_time` TIMESTAMP NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',

		  `create_by` BIGINT DEFAULT NULL COMMENT '创建人',

		  `update_by` BIGINT DEFAULT NULL COMMENT '更新人',

		  `remark` VARCHAR(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '备注',

		  PRIMARY KEY (`id`) USING BTREE

		) ENGINE=INNODB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci ROW_FORMAT=DYNAMIC COMMENT='老人家属';

		

	2- 主要存储：头像、性别、名称、openId、手机号（可变更）

	3- 复制讲义建表语句，新建表

	4- 小程序登录接口 四要素介绍

		- POST

		- 请求携带：code（换取openId）、nickName、phoneCode（换取手机号）

		- 请求返回：token、nickName



12- 微信小程序登录-基础代码准备

	1- 结合在线讲义流程图，介绍最终实现思路（5.6.1）

	2- 若依代码生成 - family_member

		0- int 修改为 integer - 1处

		1- 包路径：com.zzyl.nursing

		2- 生成模块名：nursing

		3- 生成业务名：member

	3- 将 FamilyMemberController 移至 memeber 包下，修改url路径，去除所有方法，编写login接口，调用 familyMemberService login方法



13- 编写获取openid接口

	1- 新建 WechatService 和 WechatServiceImpl，编写 getOpenId() 方法 - 根据 授权code 换取 opendId

		- 参考在线讲义的微信官方文档- https://developers.weixin.qq.com/miniprogram/dev/OpenApiDoc/user-login/code2Session.html

	2- zzym-admin 新建 测试类 WechatTest 进行单元测试（code 从小程序 login 控制台获取，只能使用一次，否则报：code bean used）

		

14- 编写获取手机号接口

	1- 在 WechatServiceImpl 中 编写 getPhoneNumber() - 根据 phonecode 换取 手机号

		- 参考在线讲义的微信官方文档 - - 参考在线讲义的微信官方文档- https://developers.weixin.qq.com/miniprogram/dev/OpenApiDoc/user-info/phone-number/getPhoneNumber.html

	2- zzym-admin 测试类 WechatTest 进行单元测试（phonecode 从小程序 login 控制台获取，只能使用一次，否则报：invalid code hint）



15- 小程序登录-步骤分析

	根据流程图分析小程序登录代码逻辑 - service层编写好注释

	1- 调用微信后台接口，获取openId

    2- 根据openId查询数据库，判断用户是否存在（不存在就是新用户）

    3- 如果是新用户，构建用户对象(需要放入openId)

    4- 调用微信后台接口，获取手机号

    5- 新增或者修改用户信息-手机号（需要生成用户昵称）

    6- 把用户ID和昵称封装到token

    7- 把token和昵称封装到LoginVo并返回



16- 小程序登录-代码实现

	1- 编码实现即可，有几个注意事项

		1- zzyl-nursing-plaform 需要依赖 zzyl-framwork 模块

		2- TokenService 中的 createToken 需要开发为 public



17- 小程序登录-拦截器

	0- 意义：拦截解析请求头中的token，并将 userId 放入 ThreadLocal

	1- 将资料中的 UserContext 粘贴到 zzyl-common utils包

	2- zzyl-framwork 中的 interceptor 包下 新建 MemberIntercepter 

	3- 将 拦截器 添加到 SpringMVC中：ResourcesConfig

	4- 测试：等作业完成可测试接口中是否能通过 ThreadLocal 获取 userId



18- 作业 

	1- 分页查询护理项目

	2- 根据护理项目ID查询护理项目信息

## 相关笔记

- [[📖 中州养老课程文档/中州养老课程总览|中州养老课程总览]]
