---
tags: [中州养老, 项目]
date: 2026-06-06
---
Day3 - 前后端快速开发



1、mybatis-plus字段自动填充

	1- 为什么需要自动填充？

	2- mp实现步骤

		1- BaseEntity 标注注解

			- createBy、createTime 字段标注 -  @TableField(fill = FieldFill.INSERT)

			- updateBy、updateTime 字段标注 -  @TableField(fill = FieldFill.INSERT_UPDATE)

		2- zzyl-framework模块 interceptor 包 新增MyMetaObjectHandler 处理字段自动填充

		3- 测试

			- 注释掉 NursingProjectServiceImpl  新增时设置创建时间、修改时设置修改时间

			- 测试新增、修改是否填充对应字段

			- 发现问题：发现编辑时并没有自动更新数据库表中的updateTime和updateBy字段

			- 原因：MetaObjectHandler 提供的默认方法策略是：如果实体属性有值则不覆盖，如果填充值为 null 则不填充。（查看官网-自动填充字段-注意事项）

			- 解决：两种方式

				- 方式一：根据ID查询信息，返回给前端的数据中 updateTime和updateBy 属性不设置值，或者前端修改时把这两个置为null -> views/serve/project/index.vue handleUpdate()

				- 方式二：修改 MyMetaObjectHandler 的 insertFill 和 updateFill 方法（使用普通填充方式，不进行严格校验）

					this.setFieldValByName("createTime", new Date(), metaObject);

					this.setFieldValByName("updateTime", new Date(), metaObject);

					this.setFieldValByName("createBy", getLoginUserId(), metaObject);

					this.setFieldValByName("updateBy", getLoginUserId(), metaObject);

					

					this.setFieldValByName("updateTime", new Date(), metaObject);

					this.setFieldValByName("updateBy", getLoginUserId(), metaObject);

			- serviceImpl.java.vm模板改造

				- insert 方法 注释 setCreateTime 相关代码

				- update 方法 注释 setUpdateTime 相关代码



2- 代码模板改造 - swagger

	1- 改造 controller.java.vm

		1- 导包

			import io.swagger.annotations.Api;

			import io.swagger.annotations.ApiOperation;

			import io.swagger.annotations.ApiParam;

			import com.zzyl.common.core.domain.R;

		2- controller 上标注：@Api(tags = "${functionName}管理")

		3- list()上标注： @ApiOperation("查询${functionName}列表")，返回值改为：TableDataInfo<${ClassName}>

		4- export()上标注：@ApiOperation("导出${functionName}列表")

		5- getInfo()上标注：@ApiOperation("获取${functionName}详细信息")，返回值改为：R<${ClassName}>，参数上添加：@ApiParam("${functionName}ID")，方法体改为 R.ok方式

		6- add()上标注：@ApiOperation("新增${functionName}")

		7- edit()上标注： @ApiOperation("修改${functionName}")

		8- remove()上标注：@ApiOperation("删除${functionName}")，参数上添加：@ApiParam("${functionName}ID数组")

		

	2- 改造 domain.java.vm

		1- 导包

			import io.swagger.annotations.ApiModel;

			import io.swagger.annotations.ApiModelProperty;

		2- domain 上标注：@ApiModel("${functionName}实体")

		3- 字段上标注: @ApiModelProperty(value = "$column.columnComment")

		

	3- 改造 mapper.java.vm

		1- 去除 @Mapper 注解

	

	4- 重启项目，重新生成 plan、level、project三张表的后端代码并整个替换，重启项目测试，预览生成的代码

		

3- 代码模板改造 - 支持LocalDateTime

	1- 修改前端 - src\views\tool\gen\editTable.vue 

		36行添加：<el-option label="LocalDateTime" value="LocalDateTime" />

	2- 修改后端

		1- VelocityUtils - getImportList()方法，添加

			// 如果字段类型在前端选择的是LocalDateTime，则导入对应的包

            else if (!column.isSuperColumn() && GenConstants.TYPE_LOCAL_DATE_TYPE.equals(column.getJavaType()))

            {

                importList.add("java.time.LocalDateTime");

                // 导入这个是为了格式化日期

                importList.add("com.fasterxml.jackson.annotation.JsonFormat");

            }

		2- 改造 domain.java.vm - 51行 添加  || $column.javaType == 'LocalDateTime'，格式也要改为时分秒

		3- 给 project 表添加一个 insert_time 字段，重启项目测试，页面表结构刷新重新reload，预览生成的代码，而后删除这个字段

	

4- 护理项目前端页面改造 - 问题分析&前端代码阅读

	1- 现有问题

		1- 搜索栏缺少状态条件

		2- 状态展示为数字，应该展示禁用或启用

		3- 缺少禁用按钮和功能，多了几个不需要的按钮

		4- 没有序号，多了一列编号，显示的是数据库表中的ID

		5- 创建时间没有展示 时分秒

		

5- 护理项目前端页面改造 -  序号和时间处理

	1- 序号

		1- 注释表格第一行复选框代码

		2- 编号：

			方式一：<el-table-column label="编号" align="center" type="index" width="55"/>  <!-- 注意事项：type="index" 需要刷新页面 -->

			方式二：通过插槽 <template #default="scope"> <span>{{ scope.$index + 1 }}</span> </template>

	2- 时间，需要带有时分秒：{y}-{m}-{d} {h}:{i}:{s}

	

6- 护理项目前端页面改造 - 表格 状态栏 调整（查看官方网站 Data数据展示区 - Tag标签）

	 <el-table-column label="状态" align="center" prop="status">

		 <template #default="scope">

		  <el-tag effect="dark" :type="scope.row.status == 1 ? 'success' : 'danger'" > 

			{{scope.row.status == 1 ? '启用' : '禁用'}}

		  </el-tag>

		</template>

	 </el-table-column>

		 

7- 护理项目前端页面改造 - 添加 状态 搜索栏（查看官方网站 Form表单组件 - Select选择器 - 可清空单选）

	<el-form-item label="状态" prop="status">

		<el-select v-model="queryParams.status" clearable placeholder="请选择" style="width: 240px">

		  <el-option v-for="item in options" :key="item.value" :label="item.label" :value="item.value" />

		</el-select>

	</el-form-item>

		

8- 护理项目前端页面改造- 启用禁用功能开发 （图标 查看官方网站 Basic基础组件  Icon图标）

	<el-button link :type="scope.row.status == 1 ? 'warning' : 'success'"

		:icon="scope.row.status == 1 ? 'Lock' : 'Unlock'" @click="handleEnable(scope.row)"

		v-hasPermi="['serve:project:enable']">{{ scope.row.status == 1 ? '禁用' : '启用' }}</el-button>

	

	function handleEnable(row) {

	  const id = row.id;

	  const msg = row.status == 1 ? '禁用' : '启用';

	  const data = {

		id: id,

		status: row.status == 1 ? 0 : 1

	  }

	  proxy.$modal.confirm(`是否确认${msg}护理项目ID为${id}的数据项？`).then(function () {

		updateProject(data).then(response => {

		  proxy.$modal.msgSuccess(`${msg}成功`);

		  getList();

		});

	  })

	}	

		

9- 护理项目前端页面改造 - 其他改造

	1- 删除 无关紧要 按钮（注释 新增 以外的按钮）

	2- 调整表格每一列 宽度

	3- 固定 最后一列

	

10- 数据字典

	1- 介绍：数字字典概念

	2- 若依 - 数字字典模块介绍

		1- 外层为：数据字典类型，主要存储字典名称、字典类型和状态（sys_dict_type）

		2- 内层为：数据字典数据，主要存储字典类型、字典标签、字典健值（sys_dict_data）

	3- 实现

		1- 新建 护理项目状态 字典：nursing_project_status，点击去添加 启用|禁用 字典值

		2- 修改前端页面 project/index.vue

			1- JS 区域 添加 护理项目状态 字典加载代码：const { nursing_project_status } = proxy.useDict(["nursing_project_status"])

			2- 修改搜索栏中 状态的 字典加载 来源，由 options 修改为 nursing_project_status

	

11- 优化新增弹窗

	1- 排序号、价格 输入框改为 数字输入框

		<el-input-number v-model="form.orderNo" :min="1" :max="20" @change="handleChange" />

		<el-input-number v-model="form.price" :min="0" :max="1000" @change="handleChange" :step="5"/>

	2- 护理要求 输入框改为 文本输入框 

		<el-input type="textarea" v-model="form.nursingRequirement" placeholder="请输入护理要求" />

	3- 价格下面添加状态 单选框 

		<el-form-item label="状态" prop="status">

            <el-radio-group v-model="form.status">

              <el-radio v-for="item in nursing_project_status" :label="parseInt(item.value)">

                {{item.label}}

              </el-radio>

            </el-radio-group>

        </el-form-item>

		【注意事项】

		1- label 这个单词千万不要输错，否则单选效果会成为全选

		2- element plus 2.6.0以下存在bug，是使用 :label提交的item.value 而不是使用 :value提交的 item.value，2.6.0以上做了修复，3.0彻底废弃（官方网站 Radio 单选框开头 有说明）

		3- 修改数据弹框时，单选框不会反显，原因：nursing_project_status字典中是string，但是反显接口返回时form.status是integer，类型不匹配，解决

			1- 方式一：在label中使用 parseInt 对 string类型的 item.value 进行 int类型转换：:label="parseInt(item.value)

			2- 方式二：在handleUpdate中将 反显接口返回的数据 转为 string类型：form.value.status=String(form.value.status);

			

12- OSS集成

	1- 后端改造

		1- 新建 zzyl-oss 模块

		2- 父工程管理 aliyun-oss 和 zzyl-oss 依赖的版本

			<aliyun.sdk.oss>3.17.4</aliyun.sdk.oss>

			<!--阿里云OSS通用模块依赖-->

            <dependency>

                <groupId>com.zzyl</groupId>

                <artifactId>zzyl-oss</artifactId>

                <version>${zzyl.version}</version>

            </dependency>

			<!-- 阿里云OSS依赖... -->

            <dependency>

                <groupId>com.aliyun.oss</groupId>

                <artifactId>aliyun-sdk-oss</artifactId>

                <version>${aliyun.sdk.oss}</version>

            </dependency>

			

		3- zzyl-oss 模块添加 aliyun-oss依赖 和 工具类

			<dependency>

				<groupId>com.aliyun.oss</groupId>

				<artifactId>aliyun-sdk-oss</artifactId>

			</dependency>

			<dependency>

				<groupId>com.zzyl</groupId>

				<artifactId>zzyl-common</artifactId>

			</dependency>

		

		4- zzyl-admin 模块 application.yml 添加 阿里云OSS配置、pom.xml中添加 zzyl-oss依赖

			aliyun:

			  oss:

				endpoint: https://oss-cn-beijing.aliyuncs.com

				bucketName: cs-zzyl

				

			<dependency>

				<groupId>com.zzyl</groupId>

				<artifactId>zzyl-oss</artifactId>

			</dependency>

		

		5- 改造 CommonController upload 上传逻辑

		

	2- 前端改造

		1- 找到 src/components/ImageUpload/index.vue，修改代码，支持读取阿里云链接（F12-点击编辑-debugger查看后修改）

			注释掉之前的，改为：（同时支持本地文件读取 和 阿里云OSS文件上传和读取）

			debugger;

			if (item.indexOf("http") === -1) {

			  item = { name: baseUrl + item, url: baseUrl + item };

			} else {

			  item = { name: item, url: item };

			}

			

	3- 测试：分别测试本地文件上传 和 阿里云OSS上传，都是正常可用的

## 相关笔记

- [[📖 中州养老课程文档/中州养老课程总览|中州养老课程总览]]
