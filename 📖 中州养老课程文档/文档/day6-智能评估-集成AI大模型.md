---
tags: [AI, 中州养老, 项目]
date: 2026-06-07
---
Day5 - 智能评估-集成AI大模型2- 解读申请入住表单 - 路由配置和父子组件

	1- 功能说明

		- 入退管理 - 入住办理 - 发起入住申请 或者 查看详情，都会进入详情页面，该页面包含四部分：老人信息、家属信息、入住配置、签约办理

		- 为什么 进行子组件抽取，然后由父组件引入？因为如果放在一起，难以维护、复用性差！所以企业级开发中，一般会进行抽取

			入住列表：index.vue

			入住详情：details.vue

				基本信息：ApplyForm.vue

				家属信息：Family.vue

				入住配置：ConfigurationForm.vue

				签约办理：TransacForm.vue

	2- 路由配置

		- 入住办理列表： URL（http://localhost/enterQuit/checkIn） 

			系统菜单：入退管理（路由-enterQuit） -> 入住办理（路由-checkIn） -> 组件路径（nursing/checkIn/index）

		- 点击【申请入住】或者【查看详情】：URL（http://localhost/enterQuit/checkInInfo    ?id=1&type=read）

			系统菜单：入退管理（路由-enterQuit） -> 入住详情（路由-checkInInfo）-> 组件路径（nursing/checkIn/details）

			

	3- 父子组件通信应用

		- 当提交入住信息时，需要将 4个子组件 数据 传递到 父组件 details.vue

		- 当查询入住信息时，需要将 父组件 details.vue 数据 传递到 4个子组件中



1- 作业讲解 - 查询入住详情

	1- CheckInController.detail()

	2- 入住详情页面 是由四个部分构成

		- 父组件页面 包含 四个子组件子页面





		

3- 解读申请入住表单 - 父子组件通信

	1- 概念：当两个组件有 引入关系时，被引入组件成为子组件，另一方则为父组件，两个组件之间数据的传递称之为 父子组件通信

	2- 父向子传递数据：属性传递（props）

		----------------父------------------

		<template>

		  <div>

			<child :message="parentMessage"></child>

		  </div>

		</template>



		<script setup>

		import child from './child.vue';



		const parentMessage = '来自父组件的消息';

		</script>

		----------------子------------------

		<template>

		  <div>{{ message }}</div>

		</template>



		<script setup>

			defineProps({

			  message: String,

			});

		</script>

		----------------核心-------------------

		1- 父组件通过import引入子组件，并通过 标签导入子组件，标签中 通过 v-bind 绑定父组件数据 parentMessage 与 属性 message

		2- 子组件通过 defineProps 定义属性，并在组件中使用该属性

	

	3- 子向父传递数据：自定义事件传递（events）

		----------------子------------------

		<template>

		  <button @click="sendMessage">给父组件发消息</button>

		</template>



		<script setup>

			const emit = defineEmits(['message-sent']);

			function sendMessage() {

			  emit('message-sent', '来自子组件的消息');

			}

		</script>

		----------------父------------------

		<template>

		  <div>

			<child @message-sent="handleMessage"></child>

		  </div>

		</template>



		<script setup>

			import child from './child.vue';



			function handleMessage(message) {

			  console.log('接收到了子组件的消息:', message);

			}

		</script>

		----------------核心-------------------

		1- 子组件中 通过 defineEmits 函数声明自定义事件，并通过emit函数触发该自定义事件，向父组件发送数据

		2- 父组件 在子标签中 通过 v-on绑定自定义事件，事件触发自定义函数，自定义函数的形参就是 子向父传递的数据

	

	4- 新建文件和菜单进行测试

		1- 在views下新建test文件夹，新建 parent.vue 和 child.vue

		2- 新建【测试菜单】目录，路由地址：test

		3-【测试菜单】下新建菜单【父子组件】，路由地址：parent，组件路径：test/parent

		4- 刷新点击【父子组件】菜单进行测试		



4- 解读申请入住表单 - 入住管理页面中的父子组件

	1- 背景

		1- details 为父组件，JS中使用import引入了4个子组件

		2- <template> 中使用 标签导入了 4个子组件

		

	2- 父向子传递数据：属性传递（props） - 当在入住办理页面 点击右侧【查看】时

		1- 父组件- 执行 钩子函数 onMounted(), 将read赋值给了 type，接着执行 getCheckIn()

		2- 父组件- getCheckIn()中执行 getCheckInInfo() 访问后端 detail接口，查询入住详情，返回结果分别赋值给 4个模型数据对象，如 applyFormInfo

		3- 父组件- applyFormInfo 模型 通过 <ApplyForm>子组件标签中的 :applyFormInfo="applyFormInfo" v-bind 绑定到了 applyFormInfo 属性上

		

		4- 子组件- ApplyForm.vue的 JS中 通过 defineProps 函数定义了 applyFormInfo 属性 和 type 属性 并赋值给 props参数

		5- 子组件- 通过 watch 函数监听 props，当props有变化时会 将 props.applyFormInfo数据赋值给 表单：formData.value，子页面数据发生变化

		

	3- 子向父传递数据：自定义事件传递（events） - 当在子页面修改表单控件数据时

		1- 子组件- 如在 ApplyForm.vue 修改数据，watch 方法会监听表单数据的变化

		2- 子组件- 如果数据发生变化,会通过emit发送【通过defineEmits预先定义好的自定义事件 getFormData】，将表单数据 发送到 父组件

		

		3- 父组件 - <ApplyForm> 子组件标签中通过 @getFormData="getFormData" v-bind 绑定了getFormData事件

		4- 父组件 - 当子组件向父组件通过getFormData事件发送数据时，会触发=右边的 getFormData 函数，函数的形参 就是：表单数据

		5- 父组件 - getFormData函数逻辑就是 将来自于各个子组件的所有数据 【追加合并】至 父组件的 formData 中

		

		父组件 - 当最后在入住申请页面底部点击【提交】时  父组件 执行 submitForm()将formData所有数据进行校验 并 提交至后端



		

5- 若依表单构建功能

	1-表单构建

		1- 作用：通过拖拉拽的方式快速构建表单

		2- 位置：系统工具/表单构建

		3- 截图 - 演示构建【办理入住 - 基本信息】

		4- 点击行容器 -> 拖入各种组件（修改其中的 标题 和 字段名）

		5- 导出vue文件，命名为index.vue 

	2- 测试

		1- 放入 src/views/test目录

		2- 测试菜单下 新建菜单【表单构建】，路由地址：custom（不重要），组件路径：test/index 

		3- 刷新测试 - 发现 样式不对，借鉴 ApplyForm.vue, 使用 <el-col :span="11"></el-col> 包裹所有的 <el-form-item>

	

6- 智能健康评估 - 需求分析

	1- 健康评估意义：收不收？收的话评估护理等级 - 护理人员要看的

	2- 目标：

		1- 能说清楚 健康评估模块 在项目中的作用

		2- 掌握 千帆大模型 的开通和使用

		3- 掌握健康评估 中 prompt 提示词编写

		4- 自主完成 健康评估 模块的接口开发

	3- 业务需求分析

		1- 上传体检报告

			- 接口1- 填写老人姓名、身份证号、体检单位，上传体检报告（保存到Redis中）

			- 接口2- 提交信息：后端调用大模型，进行智能的体检报告评估，将评估的结果各项信息保存至 数据库

			

		2- 接口3- 分页列表右侧查询 评估详情

			1- 基本信息 

				- 老人姓名：填的   				 - 老人身份证号：填的

				- 出生日期：身份证计算   		 - 年龄：身份证计算

				- 性别：身份证计算（倒数第二位，奇数为男，偶数为女）  - 体检机构：填的

				- 总检日期：AI 从体检报告中提取  - 体检报告：上传的

			2- 体检总结

				- 健康评分：AI评估		风险等级：AI评估

				- 建议入住：AI计算		推荐等级：AI计算

				- 入住情况：未入住		评估时间：当前时间

				- 分析报告：报告名称	报告总结：AI总结

			3- 疾病风险

				- 不同年龄人群健康指数分布图：AI	- 不同系统健康指数分布图：AI

			4- 异常分析：AI

				结论  项目名称  价差结果  参考值  单位 

	

7- 智能健康评估- 表结构设计 & 接口设计

	1- 表结构- health_assessment 健康评估表

		- 老人姓名：填的

		- 身份证号：填的

		- 出生日期：身份证计算

		- 年龄：身份证计算

		- 性别：身份证计算

		- 健康评分：AI

		- 风险等级：AI

		- 是否建议入住：AI

		- 推荐护理等级：AI

		- 入住情况：未入住

		- 总检日期：AI提取

		- 体检机构：填的

		- 体检报告URL链接：OSS链接

		- 评估时间：当前时间

		- 报告总结：AI（text）

		

		- 疾病风险：AI（text-json）

		- 异常分析：AI（text-json）

		- 健康系统分值：AI（json）

	2- 在线讲义复制表结构，执行

		CREATE TABLE `health_assessment` (

		  `id` bigint NOT NULL AUTO_INCREMENT COMMENT '主键',

		  `elder_name` varchar(255) DEFAULT NULL COMMENT '老人姓名',

		  `id_card` varchar(255) DEFAULT NULL COMMENT '身份证号',

		  `birth_date` datetime DEFAULT NULL COMMENT '出生日期',

		  `age` int DEFAULT NULL COMMENT '年龄',

		  `gender` int DEFAULT NULL COMMENT '性别(0:男，1:女)',

		  `health_score` varchar(255) DEFAULT NULL COMMENT '健康评分',

		  `risk_level` varchar(255) DEFAULT NULL COMMENT '危险等级(健康, 提示, 风险, 危险, 严重危险)',

		  `suggestion_for_admission` int DEFAULT NULL COMMENT '是否建议入住(0:建议，1:不建议)',

		  `nursing_level_name` varchar(255) DEFAULT NULL COMMENT '推荐护理等级',

		  `admission_status` int DEFAULT NULL COMMENT '入住情况(0:已入住，1:未入住)',

		  `total_check_date` varchar(64) DEFAULT NULL COMMENT '总检日期',

		  `physical_exam_institution` varchar(255) DEFAULT NULL COMMENT '体检机构',

		  `physical_report_url` varchar(255) DEFAULT NULL COMMENT '体检报告URL链接',

		  `assessment_time` datetime DEFAULT NULL COMMENT '评估时间',

		  `report_summary` text COMMENT '报告总结',

		  `disease_risk` text COMMENT '疾病风险',

		  `abnormal_analysis` text COMMENT '异常分析',

		  `system_score` varchar(255) DEFAULT NULL COMMENT '健康系统分值',

		  `create_by` varchar(255) DEFAULT NULL COMMENT '创建者',

		  `create_time` datetime DEFAULT NULL COMMENT '创建时间',

		  `update_by` varchar(255) DEFAULT NULL COMMENT '更新者',

		  `update_time` datetime DEFAULT NULL COMMENT '更新时间',

		  `remark` text COMMENT '备注',

		  PRIMARY KEY (`id`)

		) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='健康评估表';



	3- 接口统计

		- 分页列表查询：代码生成

		- 上传体检报告：待完成

			填写身份证号 -> 上传体检报告 -> 后端存储到OSS -> 工具类读取PDF内容 -> 以身份证为key，以PDF为内容存储到Redis 供后续使用

		- 智能评测：待完成

			编写提示词 -> 根据身份证从redis读取PDF体检报告内容 -> 组装完整提示词丢给百度千帆 -> 解析结果，保存至数据库 ->

			返回数据库健康评估表主键ID -> 自动跳转至 详情页

		- 查看详情：代码生成

	 

8- PDF内容读取

	1- 导依赖 （父工程管理版本、zzyl-common导依赖）

		<dependency>

            <groupId>org.apache.pdfbox</groupId>

            <artifactId>pdfbox</artifactId>

        </dependency>

	2- 拷贝 PDFUtil 至 zzyl-common utils包

	3- zzyl-admin 编写单元测试 PDFTest

	 

9- 百度智能云 - 注册和介绍

	1- 介绍

	2- 注册&实名

	3- 模型广场介绍 - 文本生成模型 - 第二页 ERNIE 4.0

	4- 费用说明 - 右上角财务 - 代金券（新账号有一张为期一个月20元的代金券）

	

10- 百度智能云 - 大模型API说明 & 集成大模型

	1- 低版本模型的都不具备使用大量token的能力，所以我们本次采用的：ERNIE-4.0-8K-Preview

	2- 官方地址：https://cloud.baidu.com/doc/WENXINWORKSHOP/s/nluv1jxlp

	3- 关键API参数介绍：messages、model、temperature、max_output_tokens、response_format

	3- SDK&API介绍（集成 V1）

		- 推理服务API V1：https://cloud.baidu.com/doc/WENXINWORKSHOP/s/xlmokikxe（百度智能云特有）

			1- 导依赖 （父工程管理版本、zzyl-common导依赖）

				<dependency>

					<groupId>com.baidubce</groupId>

					<artifactId>qianfan</artifactId>

				</dependency>

			2- 拷贝 非流式、流式多轮对话 测试代码至 zzyl-admin test目录 - BaiduQianfanAIModelTest

			3- 个人中心 - 安全认证 - 创建 AccessKey 和 SecuretKey

		- 推理服务API V2：https://cloud.baidu.com/doc/WENXINWORKSHOP/s/2m3fihw8s（OpenAI 兼容）

		

11- 智能健康评估 - 代码生成

	1- int 改为 integer，日期改为LocalDateTime

	2- 包路径：com.zzyl.nursing，模块名：nursing，业务名：healthAssessment

	3- 后端代码放入项目中，重启测试，分页列表查询为空，从在线讲义粘贴SQL插入一条数据，再测试分页查询和查询详情



	

12- 智能健康评估 - prompt提示词

	1- 提示词 编写的6大 注意事项

	2- 编写智能健康评估 提示词

	

13- 智能健康评估 - 上传体检报告

	1- 定义接口（身份证 和 上传体检报告 都是必填） - HealthAssessmentController.upload()

		1- 调用 zzyl-oss模块的 工具 AliyunOSSOperator 将 体检报告 上传至 阿里云OSS

		2- 调用工具 PDFUtil 读取体检报告内容，将内容存储至 Redis

	4- 测试：上传 资料 中的一份PDF体检报告

	

14- 智能健康评估 - 抽取百度千帆大模型调用工具

	1- 将 accessKey、secretKey、qianfanModel 配置到 application.yml

	2- zzyl-common utils.ai 包下 新建 BaiduProperties 读取配置

	3- 同包下 新建 BaiduQianfanAIModelUtil 工具类

	

15- 智能健康评估 - 新增健康评估

	【改造】 HealthAssessmentController.add()

	1- 形参接受 HealthAssessmentDto（老人姓名、身份证号、体检机构、体检报告URL链接），返回 健康评估记录 ID，用于跳转详情页反显

	2- 组装prompt提示词

	3- 调用AI大模型分析体检报告，返回分析结果（JSON格式数据）

	4- 解析JSON格式的数据，将结果保存到数据库，返回ID

	5- 测试（有可能 疾病风险 小点不显示 - 原因：身份证年龄太小，不属于监控50岁以上老人）

## 相关笔记

- [[📖 中州养老课程文档/中州养老课程总览|中州养老课程总览]]
