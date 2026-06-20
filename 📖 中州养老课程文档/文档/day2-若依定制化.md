---
tags: [中州养老, 若依, 项目]
date: 2026-06-06
---
Day2 - 若依定制化 - UI定制 & swagger集成 & 代码模板改造 



1- UI界面定制化

	1- 浏览器标签页 - logo标识、标题

		1-  logo：UI资料目录 log 图标 favicon.ico -> public文件夹替换 favicon.ico

		2-  标题：

			- 根目录index.html 更换title 若依管理系统 -> 中州养老 （一闪而过）

			- 环境配置文件中 VITE_APP_TITLE 属性 若依管理系统 -> 中州养老 （生效）

			

	2- 首页页面 - logo标识、标题

		1- logo：UI资料目录 log 图标 favicon.ico -> src/assets/logo/logo.png

		2- 标题：依然是 VITE_APP_TITLE 属性

	

	3- 登录页面 - 标题、背景图

		1- 登录名称：src/views/login.vue 若依后台管理系统-> 中州养老

		2- 背景图：src/assets/images/login-background.jpg （src/views/login.vue中配置） ->   UI资料背景图

	

	4- 去除源码地址 & 文档地址 & 若依官网标识、菜单

		1- 使用VS Code全局搜索功能(搜索'源码地址')，注释掉 - 去除右上角的源码地址和文档地址

		2- 利用菜单功能，去除若依官网菜单项目

			- 删除时，发现提示已被分配，不能删除：找到普通角色，解除关联，即可删除

			

	5- 主题UI风格调整 - 改为绿色

		1- 点击右上角的头像，可以找到布局设置进行调整

		2- 前端代码中也有对应的操作，文件位置：src/setting.js

		3- 更换主题颜色：src/store/modules/settings.js -> theme: storageSetting.theme || '#409EFF' -> 改为 #00b8a0

		

2- 作业1讲解 - 创建新模块

3- 作业2讲解 - 快速开发【护理等级、护理计划】模块



4- 记录日志源码阅读

	1- 背景：系统管理 - 日志管理 - 操作日志 菜单 -> 可以查看所有的操作记录，包括详细信息

		操作模块、请求地址、请求方式、登录用户、IP、操作方法、请求参数、返回数据、操作状态、消耗时间、操作时间

	2- 核心代码：zzyl-freamwork 模块下的 LogAspect

		- 前置通知：记录当前时间

		- 返回后通知：handleLog() - 与异常通知互斥

		- 异常通知：handleLog() - 与返回后通知互斥

		- 结合 自定义注解 @Log 和 其中一个使用这个注解的Controller 理清切面中的代码逻辑，如：SysteMenuController

		- 其中最后记录操作日志的操作 是通过 线程池异步进行的，且延迟了10ms



5- 若依在线接口测试工具

	1- 位置：系统工具 -> 系统接口

	2- 介绍swagger 主要作用

		- 通过简单的注解配置，即可生成在线接口文档，减少编写接口文档工作量

		- 演示：testController 

	3- 项目中已集成

		- zzyl-admin依赖：springfox-boot-starter

		- zzyl-admin依赖： swagger-models

		- 核心配置类：SwaggerConfig

	4- 访问地址

		- 方式一：系统内部菜单访问 

		- 方式二：服务地址+/swagger-ui/index.html  --- >  http://localhost:8080/swagger-ui/index.html 

			- 【问题1】：401没有权限：拷贝token至 swagger Authorization  中

			- 【问题2】：/dev-api 前缀多余导致404：注释掉 SwaggerConfig createRestApi()中的 的 pathMapping

			

6- Swagger 转为 集成Knife4j

	1- knife4j 介绍

		- 是JavaMVC框架集成 Swagger 生成API文档的增强型解决方案，前身是 swagger-bootstrap-ui(像一把匕首小巧强悍)

		- 优势：友好界面、离线文档、在线调试、文档清晰、容易上手

	2- 点击链接，查看若依官网集成knife4j步骤

		- 官网： https://doc.ruoyi.vip/ruoyi-vue/document/cjjc.html

		- 添加依赖：knife4j-spring-boot-starter [com.github.xiaoymin 3.0.3] （zzyl-admin），swagger依赖就可以注释了

		- 修改前端若依跳转地址：views\tool\swagger\index.vue -> const url = ref(import.meta.env.VITE_APP_BASE_API + "/doc.html")

	3- 访问地址（swagger链接依然可以访问）

		- 方式一：系统内部菜单访问 （不能注释掉 SwaggerConfig createRestApi()中的 的 pathMapping）

		- 方式二：服务地址+/doc.html  --- >  http://localhost:8080/doc.html

			- 【问题1】：401没有权限：拷贝token至 knife4j Authorize 中

			- 【问题2】：/dev-api 前缀多余导致404：注释掉 SwaggerConfig createRestApi()中的 的 pathMapping

			-  该种方式，可以通过配置外链菜单方式访问，界面更大，方便操作，菜单名：系统接口-外部访问，类型为目录，外链：http://localhost:8080/doc.html

	4- 可以下载离线文档：Markdown等形式，还可下载json导入至ApiFox

	

7- Swagger常用注解&使用

	1- 常用注解

		1- @Api(tag="")：用在Controller上，描述作用

		2- @ApiOperation("")：用在方法上，描述作用

		3- @ApiParam("")：用在方法参数上，描述单个形参含义，适用简单场景

		4- @ApiImplicitParam：用在方法参数上，描述形参含义，适用复杂场景

		5- @ApiModel：用在实体类上（DTO或VO），描述实体类作用

		6- @ApiModelProperty： 用在实体属性上，描述字段含义

	

	2- 代码实践

		- NrisingProjectController （AI实现：我已经引入了swagger依赖，请为该类添加swagger注解，使用 @Api 和 @ApiParam 注解，不需要 required 和 example属性）

		- 代码报错，因为缺失swagger model依赖：将 zzyl-admin 模块已注释的 swagger-models 依赖剪切放入 zzyl-common 模块

		- 访问验证：OK，但是 knife4j页面 实体类 NrisingProject 还缺失 备注说明（查询分页列表接口）

		

		- NrisingProject（AI实现：我已经引入了swagger依赖，请为该类添加swagger注解，使用 @ApiModel 和 @ApiModelProperty注解，不要example属性）

		- 访问验证：OK，但是 knife4j页面 实体类 BaseEntity 还缺失 备注说明（查询分页列表接口）

		

		- BaseEntity（AI实现：我已经引入了swagger依赖，请为该类添加swagger注解，使用 @ApiModel 和 @ApiModelProperty注解，不要example属性）

		- 访问验证：OK，但是 响应参数 还缺失 备注说明（查询分页列表接口）

		

		- 返回值TableDataInfo改造：controller接口返回的TableDataInfo改为：TableDataInfo<NursingProject>，加上泛型T，内部所有？换为T

		- 访问验证：OK，但是 获取护理项目详情接口 响应参数 还缺失 备注说明

		

		- 返回值 AjaxResult 改造：改为返回 R<T>，通过R.ok(xx)返回，因为AjaxResult本质是个Map，Swagger不知道具体类型，所以生成不了备注

		- 访问验证：OK（获取护理项目详情接口）



8- 模板引擎简介

	1- 若依生成代码的问题：没有swagger注解、没有lombok注解、代码风格没有集成mybatisplus，所以需要改造

	2- 课程目标：清楚velocity使用场景、了解velocity常用指令、能够使用velocity改造若依代码生成模板

	3- zzyl-generator 是代码生成模块，其中 resources/vm 目录下 .vm 结尾文件 就是生成代码的 velocity 关键模板文件

	   要想改造就要清楚 velocity 语法，以vm/java/domain.java.vm 为例，现在看不懂，但是语法和java类似

	4- 介绍：一种将模板和数据合并为一个成品文件的技术



9- Velocity模板引擎快速入门

	1- 介绍：一款基于Java的模板引擎，可以通过特定语法将Java对象数据填充到指定模板中，从而实现成品文件合成的效果

	2- 理解：velocity模板引擎(数据 + 模板) = 成品文件

	3- 应用场景：web应用程序视图展示数据、电子邮件生成、静态网页、【源代码生成】

	4- 快速入门，需求：将自定义数据 填充到 指定html页面

		1- resources/vms/index.html.vm 目录下新建模板文件

		2- 新建测试类VelocityTest，编写代码，步骤：

			1- 初始化velocity引擎 VelocityInitializer.initVelocity()

			2- 创建velocity上下文对象并存放数据 : VelocityContext context = new VelocityContext();  context.put("message", "你好朋友！");

			3- 获取模板：Template t = Velocity.getTemplate("vms/index.html.vm", "UTF-8");

			4- 获取输出流 -> 新建文件输出流 FileWriter writer = new FileWriter("zzyl-generator/src/main/resources/index.html");

			5- 合并模板 t.merge(context, writer);

			5- 关闭流：writer.close()  --字符流有一个1024的缓冲区，不到这个大小，无法自动写入，超过才会自动写，所以要close flush(字节流不用)

		3- 生成文件，右键 -> Open in -> Browser -> Edge打开

			

10- Velocity模板引擎基础语法

	1- 利用domain.java.vm + NursingProject 对照讲解学习语法（两个文件 导包处代码顺序改为一致，改NursingProject）

		- ${variable}: 表示插入变量值。

		- #foreach 和 #end: 循环结构，用于遍历列表。

		- #if 和 #end: 条件判断结构。

		- #set: 设置变量。

		- #elseif: 条件分支。

	2- 小技巧：将光标点到某个 #if 上会 显示它对应的 #end 闭合处，反之也一样，还可以缩起来，方便查看结构



11- 若依代码生成流程

	1- 讲解 service.GenTableServiceImpl.generatorCode() 逻辑（理解即可）



12- 代码模板改造 - Lombok集成

	1- 父工程pom 管理 lombok 版本

	2- 在 zzyl-common 引入 lombok 依赖

	3- 改造 domain.java.vm 

		1- 类上添加注解，而后会自动导包

			- @Data

			- @NoArgsConstructor

			- @AllArgsConstructor

			

			import lombok.Data;

			import lombok.AllArgsConstructor;

			import lombok.NoArgsConstructor;

		

		2- 注释掉 domain.java.vm 中 get set tostring 部分

		3- 由于不需要tostring方法，注释掉导包处 ToStringBuilder、ToStringStyle



13- 项目中引入MybatisPlus

	1- 父工程pom 管理 mybatis-plus 版本

	2- 在 zzyl-common 引入 mybatis-plus 依赖

	3- 添加mybatisplus核心配置：application.yml 中，去除mybatis重叠的配置）

		注意： configLocation配置 不能动，仍然需要放在mybatis下，否则报错

	4- 拷贝讲义中mybatisplus核心配置类（分页插件）至 zzyl-framework 模块的config包中，并注释掉原有的 MybatisConfig中的所有代码

	5- 以NursingProject为例，集成MybatisPlus

		1- Mapper 继承 BaseMapper<NursingProject>  

		2- IService 继承 IService<NursingProject>

		2- ServiceImpl 继承 ServiceImpl<NursingProjectMapper,NursingProject>

		3- ServiceImpl 改造方法

			1- selectNursingProjectById -> return getById(id)

			2- insertNursingProject -> save(nursingProject) ? 1:0

			3- updateNursingProject -> updateById(nursingProject) ? 1:0

			4- deleteNursingProjectByIds -> removeByIds(Arrays.asList(ids)) ? 1:0

			5- deleteNursingProjectById -> removeById(id) ? 1:0

		4- Mapper 除了 selectNursingProjectList 都删掉

		5- mapper.xml中除了 selectNursingProjectList 相关保留，其他都删掉

	6- 测试

		- 分页查询正常

		- 编辑、新增异常：BaseEntity中的 searchValue、params 表中没有，需要忽略掉 @TableField(exists=false)



14- 代码模板改造 - MybatisPlus集成

	1- 改造 mapper.java.vm 

		- 导包

			import com.baomidou.mybatisplus.core.mapper.BaseMapper;

		- 类 extends BaseMapper<${ClassName}>

		- 除了 selectxxxList 方法保留，其他注释掉

		

	2- 改造 service.java.vm  

		- 导包

			import com.baomidou.mybatisplus.extension.service.IService;

		- 接口 extends IService<${ClassName}>

		

	3- 改造 serviceImpl.java.vm

		- 导包

			import com.baomidou.mybatisplus.extension.service.impl.ServiceImpl;

		- 类 extends ServiceImpl<${ClassName}Mapper, ${ClassName}>

		- 方法

			- 根据ID查询 - getById(${pkColumn.javaField})

			- 保存 -  save(${className}) ? 1 : 0;

			- 更新 - updateById(${className}) ? 1 : 0;

			- 批量删除 - removeByIds(Lists.of(${pkColumn.javaField}s)) ? 1 : 0;

			- 删除 - removeById(${pkColumn.javaField}) ? 1 : 0;

			

	4- 改造 mapper.xml.vm

		除了 selectNursingProjectList 相关保留，其他都删掉

	5- 重启项目测试 - 预览 NursingPlan模块代码 拷贝 至相应位置，测试CRUD		





15- 今日作业

	- 今日代码

	- swagger代码改造

	- LocalDateTime支持

## 相关笔记

- [[📖 中州养老课程文档/中州养老课程总览|中州养老课程总览]]
