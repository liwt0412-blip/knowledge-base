---
tags: [中州养老, 项目]
date: 2026-06-06
---
1- 入住办理 - 接口开发 - 代码生成 & 分页查询入住列表

	1- 使用 若依代码生成，生成 elder、contract、check_in、check_in_config 四张表的代码（由于前端代码已写好，所以无需关心前端代码、只需关注类型即可）

		1- elder 老人表 

			- 字段信息：int对应的Java类型改为 Integer

			- 生成信息：包路径改为 com.zzyl.nursing，生成模块名改为：nursing

		2- contract 签约（合同）表

			- 字段信息：int对应的Java类型改为 Integer，createTime、updateTime以外日期 类型改为 LocalDateTime

			- 生成信息：包路径改为 com.zzyl.nursing，生成模块名改为：nursing，生成功能名改为：合同

		3- check_in 入住表

			- 字段信息：int对应的Java类型改为 Integer，createTime、updateTime以外日期 类型改为 LocalDateTime

			- 生成信息：包路径改为 com.zzyl.nursing，生成模块名改为：nursing，生成业务名改为：checkIn，生成功能名改为：入住

		4- check_in_config 入住配置表

			- 字段信息：int对应的Java类型改为 Integer，createTime、updateTime以外日期 类型改为 LocalDateTime

			- 生成信息：包路径改为 com.zzyl.nursing，生成模块名改为：nursing，生成业务名改为：checkInConfig ，生成功能名改为：入住配置

	2- 复制后端代码，放入项目，删除 CheckInConfigController(不需要)

	3- 复制在线讲义 插入check_in表的几条数据，做分页查询入住办理列表 基础测试



2- 入住办理 - 接口开发 - 查询所有护理等级列表

	1- NursingLevelController中开发 getAllLevels 接口

	2- 测试



3- 入住办理 - 接口开发 - 根据床位状态查询所有可用的 楼层房间床位信息

	1- 分析需求：根据床位状态查询 楼层-房间-床位 树形结构

	2- SQL

		select 

			f.id fid, f.name fname, 

			r.id rid, r.code rcode,

			b.id bid, b.bed_number bbed_number

		from floor f

			 left join room r on r.floor_id = f.id

			 left join bed b on b.room_id = r.id

		where b.bed_status = #{status}

		

		或

		

		select f.id fid,f.name fname,

               r.id rid,r.code rcode,

               b.id bid,b.bed_number bbed_number

        from bed b

                 inner join room r on b.room_id = r.id

                 inner join floor f on r.floor_id = f.id

        where b.bed_status = #{status}

			

	3- FloorController 中开发 getRoomAndBedByBedStatus 接口

	4- 测试

	

4- 入住办理 - 接口开发 - 根据房间ID查询房间数据

	1- 分析需求：根据房间ID 查询 楼层ID、楼层名、房间ID、房间code、房间价格

	2- SQL（对照 接口文档返回的JSON结构）

		select f.id floorId, f.name floorName, r.id roomId, r.code, rt.price

        from room r

                 inner join room_type rt on r.type_name = rt.name

                 inner join floor f on r.floor_id = f.id

        where r.id = 11;



	3- 测试（选择床位，反显床位费用）



5- 入住办理 - 接口开发 - 申请入住办理

	

6- 作业

	1- 删除护理计划 接口改造（删除护理计划同时 级联删除 关联的 护理项目）

	2- 护理等级列表 不显示 护理计划名称Bug

## 相关笔记

- [[📖 中州养老课程文档/中州养老课程总览|中州养老课程总览]]
