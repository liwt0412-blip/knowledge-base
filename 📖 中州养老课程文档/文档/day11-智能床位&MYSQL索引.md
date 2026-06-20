---
tags: [MySQL, 中州养老, 项目]
date: 2026-06-06
---
Day13 - IOT消息采集和处理



01- 智能床位课程介绍 & 需求&接口分析

02- 智能床位-开发前数据准备

03- 智能床位-查询所有具有智能设备的楼层信息SQL分析

04- 智能床位-查询所有具有智能设备的楼层接口开发



05- 智能床位-查询某楼层下所有房间&设备&床位&老人信息接口分析数据准备

06- 智能床位-查询某楼层下所有房间&设备&床位&老人信息SQL分析(上)

07- 智能床位-查询某楼层下所有房间&设备&床位&老人信息SQL分析(下)

08- 智能床位-查询某楼层下所有房间&设备&床位&老人接口定义

09- 智能床位-查询某楼层下所有房间&设备&床位&老人接口开发（上）

10- 智能床位-查询某楼层下所有房间&设备&床位&老人接口开发（下）

11- 智能床位-查询某楼层下所有房间&设备&床位&老人接口测试

12- Mysql索引-作用&优缺点

13- Mysql索引-数据结构





01- 智能床位课程介绍 & 需求&接口分析

	1- 目标

		1- 能够完成智能床位的功能开发（2个接口）

		2- MYSQL 索引（创建、底层原理、失效）

	2- 需求

		1- 需要在 智能床位一览 页面查询 所有具有 智能设备 的：

			1- 楼层信息：floor

			2- 房间信息：room

			3- 房间智能设备信息：device、device_data

            4- 床位信息：bed

			5- 床位设备信息：device、device_data

			6- 老人信息：elder

		2- 接口分析（2个）：

			1- 查询所有具备智能设备的 楼层

				解读：

					1- 如果该楼层下有任意房间绑定了智能设备 或者 任意房间有任意床位绑定了智能设备，那么所属楼层要被查询出来

					2- 换而言之，如果某个楼层下既没有 绑定智能设备的房间，也没有绑定智能设备的床位，该楼层不应该被查询出来

			

			2- 查询房间设备或床位设备的数据

				解读：

					1- 根据楼层ID查询其下具有智能设备的： 房间+设备、床位+设备、床位上老人的数据

					2- 如果 某个床位绑定智能设备，所属房间基本信息也要展示出来，如果床位上有老人，老人信息也要查出来

		

02- 智能床位-开发前数据准备

	1- IOT平台准备产品：烟雾报警器、睡眠检测带（IOT第一天已经准备好）

	2- 中州养老新建智能设备

		0- 由于关联的 房间 和 床位 都需要时有人住的，所以需要提前准备6名老人信息，分别入住：1楼、3楼、6楼不同的床位



		1- 烟雾报警器

			烟雾报警器1号  yw01  1楼,101  固定设备

			烟雾报警器2号  yw02  1楼,104  固定设备	  		

			烟雾报警器3号  yw03  3楼,301  固定设备



		2- 睡眠检测带

			睡眠监测带1号 sleep01 1楼,101,101-1 固定设备	

			睡眠监测带2号 sleep02 3楼,301,301-2 固定设备	

			睡眠监测带3号 sleep03 6楼,606,606-1 固定设备

			

	3- 入住情况  

		101-1  老李头儿（睡眠检测带）  101-2  老李      			  烟雾报警器

		104-1  张三		  			   104-2  李天龙     			  烟雾报警器

		301-1        				   301-2  冯祥清（睡眠监测带）    烟雾报警器

		606-1  刘爱国（睡眠检测带）

	

	3- 准备【智能床位】菜单

		1- 上级菜单：在住管理

		2- 路由地址：smartBed

		3- 组件路径：nursing/smartBed/index

		

    

03- 智能床位-查询所有具有智能设备的楼层信息SQL分析

    # 需求一：查询所有具有 智能设备 的楼层信息

	-- 方式一：分别查询 【具有智能设备的房间对应楼层信息】 和 【具有智能设备的床位对应楼层信息】

	-- 1、先查询具有智能设备的【房间】对应楼层信息 -- device、room、floor

	select f.id, f.name, f.code  from device d

		inner join room r on r.id = d.binding_location

		inner join floor f on f.id = r.floor_id

	where d.location_type = 1  -- 设备类型为：固定设备

	and   d.physical_location_type = 1  -- 绑定位置为：房间

	

	union

	

	-- 2、再查询具有智能设备的【床位】对应楼层信息  -- device、bed、room、floor

	select f.id, f.name, f.code  from device d

		inner join bed b on b.id = d.binding_location

		inner join room r on r.id = b.room_id

		inner join floor f on f.id = r.floor_id

	where d.location_type = 1  -- 设备类型为：固定设备

	and   d.physical_location_type = 2  -- 绑定位置为：床位



	或者



	-- 设备表与绑定位置对应表关联产生笛卡尔积时直接 加过滤条件

	-- 1、先查询具有智能设备的【房间】对应楼层信息 -- device、room、floor

	select f.id, f.name, f.code from device d

		inner join room r on r.id = d.binding_location and d.location_type = 1 and d.physical_location_type = 1

		inner join floor f on f.id = r.floor_id

	union

	-- 2、再查询具有智能设备的【床位】对应楼层信息  -- device、bed、room、floor

	select f.id, f.name, f.code from device d

		inner join bed b on b.id = d.binding_location and d.location_type = 1 and d.physical_location_type = 2

		inner join room r on r.id = b.room_id

		inner join floor f on f.id = r.floor_id



	-- 方式二：通过左关联查询

	-- 思路：左关联依次 查询 楼层、房间、房间智能设备、床位、床位智能设备，筛选 房间智能设备 和 床位智能设备不为空的记录

	select distinct f.id, f.name, f.code

	from floor f

			 left join room r on r.floor_id = f.id

			 left join bed b on b.room_id = r.id

			 left join device dr on dr.binding_location = r.id and dr.location_type = 1 and dr.physical_location_type = 1

			 left join device db on db.binding_location = b.id and db.location_type = 1 and db.physical_location_type = 2

	where (dr.id is not null or db.id is not null)

	

	楼层1

		房间1      智能设备

			床位1  智能设备

			床位2  智能设备

			床位3 

		房间2	   智能设备

			床位1

			床位2

			床位3

	楼层2

		房间1      

			床位1  

			床位2  

	楼层3

		房间1      

			床位1  智能设备

			床位2

			

	

	楼层1 房间1 智能设备  床位1  智能设备	

	楼层1 房间1 智能设备  床位2  智能设备	

	楼层1 房间1 智能设备  床位3  

	

	楼层1 房间2	智能设备  床位1

	楼层1 房间2	智能设备  床位2

	楼层1 房间2	智能设备  床位3	

	

	楼层2 房间1			  床位1	

	楼层2 房间1			  床位2

		

	楼层3 房间1           床位1  智能设备	

	楼层3 房间1           床位2  

			

04- 智能床位-查询所有具有智能设备的楼层接口开发

	1- 编写接口：FloorController.getAllFloorsWithDevice

	2- SQL使用 方式二 SQL

	3- 测试，菜单：在住管理 - 智能床位

 

05- 智能床位-查询某楼层下所有房间&设备&床位&老人信息接口分析数据准备

	1- 需求分析：选择楼层，根据楼层ID，查询该楼层下：

		1- 绑了智能设备（烟雾报警器）的房间信息

			- 房间基本信息 room + 房间设备信息 device、房间设备最近一次上报数据 device_data

		2- 绑了智能设备（睡眠监测带）的床位信息

			- 床位基本信息 bed + 床位设备信息 device、床位设备最近一次上报数据 device_data + 床位上的老人信息 elder

			说明：

				- 如果床位没绑定智能设备，那么该床位不展示

				- 如果床位绑定了智能设备，但是房间没绑定智能设备，那么房间的基本信息要展示出来

	2- 关于 设备最近一次上报数据 查询方案

		1- 如果关联表查询，其中房间、房间设备、床位、床位设备、老人表的数据量都不大，但是 设备数据表 数据量 是海量的，查询效率会比较低

		2- 所以可以考虑将每个设备的最近一次上报数据暂存至 redis，有新的数据上报直接覆盖，这里查询就可以直接查redis即可，代码改造：

			1- DeviceDataServiceImpl.batchInsertDeviceData 最后添加代码：

				// 将该设备最新上报数据 保存至 Redis（供后续查询使用）

				redisTemplate.opsForHash().put(IOT_DEVICE_LAST_DATA,deviceId,deviceDataList);

				

06- 智能床位-查询某楼层下所有房间&设备&床位&老人信息SQL分析(上)

	1、左关联查询 房间、床位、老人、房间设备、床位设备

	-- 需求二：根据楼层ID 查询该楼层下所有 具有智能设备的房间、床位  所对应的房间、床位、床位上老人、设备 数据

	select * from room r

			 left join bed b on b.room_id = r.id

			 left join elder e on e.bed_id = b.id

			 left join device dr on dr.binding_location = r.id and dr.location_type = 1 and dr.physical_location_type = 1

			 left join device db on db.binding_location = b.id and db.location_type = 1 and db.physical_location_type = 2

	where (dr.id is not null or db.id is not null)

	  and r.floor_id = 1 

    

07- 智能床位-查询某楼层下所有房间&设备&床位&老人信息SQL分析(下)

	1、为上一小节SQL填充查询字段

		1- 参考在线讲义 中接口返回的JSON，放入IDEA序列化后参考使用

			- 房间

				- 房间基本信息

				- 房间下床位集合

					- 床位基本信息

					- 老人基本信息

					- 床位下智能设备集合

						- 设备基本信息

						- 设备 上报数据集合

				- 房间下智能设备集合

					- 设备基本信息

					- 设备 上报数据集合

		2- 最终SQL

		select 

		   r.id r_id,

		   r.code r_code,



		   b.id b_id,

		   b.bed_number,

		   b.bed_status,



		   e.id e_id,

		   e.name e_name,



		   dr.id dr_id ,

		   dr.iot_id dr_iot_id,

		   dr.device_name dr_device_name,

		   dr.product_key dr_product_key,

		   dr.product_name dr_product_name,



		   db.id db_id,

		   db.iot_id  db_iot_id,

		   db.device_name db_device_name,

		   db.product_key db_product_key,

		   db.product_name db_product_name

	from room r

			 left join bed b on b.room_id = r.id

			 left join elder e on e.bed_id = b.id

			 left join device dr on dr.binding_location = r.id and dr.location_type = 1 and dr.physical_location_type = 1

			 left join device db on db.binding_location = b.id and db.location_type = 1 and db.physical_location_type = 2

	where (dr.id is not null or db.id is not null)

	  and r.floor_id = 6

	

08- 智能床位-查询某楼层下所有房间&设备&床位&老人接口定义

	1- 根据接口文档，定义接口 RoomController.getRoomsWithDeviceByFloorId

	2- 其中 出参严格按照 接口文档返回JSON对照定义 -> R<List<RoomVo>>

		1- RoomVo 项目中已经有了，但是缺少一个属性 -> 房间设备信息：

			@ApiModelProperty(value = "房间设备信息", required = true)

			private List<DeviceInfo> deviceVos; 

		2- RoomVo 中的 BedVo 下，也缺少 床位设备信息: 

			@ApiModelProperty(value = "床位设备信息", required = true)

			private List<DeviceInfo> deviceVos;

    

09- 智能床位-查询某楼层下所有房间&设备&床位&老人接口开发（上）

	1- 一对多查询 从数据库查询数据

    

10- 智能床位-查询某楼层下所有房间&设备&床位&老人接口开发（下）

	1- 给房间 和 床位 的智能设备 填充最近一次上报数据 

    

11- 智能床位-查询某楼层下所有房间&设备&床位&老人接口测试

	1- 使用 huaweicloud-iot-device-sdk-java-master 给 三台烟雾报警器 和 三个睡眠监测带 上报数据，最近一次上报数据最终会进入redis中

	2- 刷新智能床位页面 - 测试 烟雾报警器 和 睡眠监测带 是否都有数据

	

	3- 前端 不显示 图片bug修复

		- views/nursing/smartBed/constants.js  

			- 离床时间 的 value 改为：BedTime

			- 离床次数 的 value 改为：BedExiitCount

			- 睡眠状态 的 value 改为：SleepPhaseState

	4- 前端 睡眠状态为 离床时，离床时间显示格式问题

		- 297 行 timestampToTime(arr[0]?.dataValue) 改为 -> arr[0]?.dataValue   不适用时间戳转换了，后端上报数据用 时分秒即可

    

12- Mysql索引-作用&优缺点

    

13- Mysql索引-数据结构

## 相关笔记

- [[📖 中州养老课程文档/中州养老课程总览|中州养老课程总览]]
