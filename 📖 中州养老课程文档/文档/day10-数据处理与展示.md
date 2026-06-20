---
tags: [中州养老, 项目]
date: 2026-06-07
---
Day12 - IOT消息采集和处理



1- 设备模块接口实现-查询设备详细信息

	1- 需求分析

		1- 直接F12，点击 【编辑】 或者 【查看详情】 的时候，都会调用该接口，查询设备详细信息

		2- 其中

			编辑调用是为了 反显

		    查询详情调用 是为了 反显页面上半部分设备基本信息，当该接口开发完，页面下半部分还会发起另外一个请求：【查询设备最新上报数据】

	

	2- 代码实现 - DeviceController 定义接口 queryDeviceDetailInfo  - 参照接口文档

		1- 接收 IOT设备ID

		2- 根据设备ID查询 数据库 设备数据，但是缺少 设备状态 和 激活时间

		3- 根据设备ID调用华为云工具 查询设备信息（设备状态、激活时间）

		4- 将 数据库 信息拷贝至VO，封装设备状态、激活时间，VO返回前端

	3- 测试

		1- 发现激活时间 比当前时间晚 8个小时，需要特殊处理，处理方式两种

			1- 时区转换，将东十六区时间 转换为 东八区

			2- 加8个小时



2- 设备模块接口实现-查询设备最新上报数据

	1- 需求分析

		1- 当 编写好【查询设备详细信息】接口后，点击查询详情，会请求该接口，查询设备最近一次上报数据

	2- 代码实现 - DeviceController 定义接口 queryServiceProperties  - 参照接口文档

		1- 接收 IOT设备ID

		2- 根据设备ID 调用华为云工具 查询该设备最近一次上报数据（设备影子数据）

		3- 解析华为返回数据，包括最近上报时间，最终组装成List<Map>结构返回前端，Map中存  属性名、上报值、上报时间

	3- 测试

		1- 选一个使用中州养老新建的设备，使用 huaweicloud-iot-device-sdk-java-master 为其上报数据

		2- 查看页面数据 是否 和IOT平台一致



3- 设备模块接口实现-修改设备名称

	1- 需求分析

		1- 只能修改 【设备名称】和 【接入位置】（数据库）

		2- 设备标识码 不可修改 - 华为IOT平台 决定

		3- 所属产品 不可修改 - 华为IOT平台 决定

		4- 由于 所属产品不可修改，所以 设备类型 也不能修改，否则 产品类型 和 设备类型 有可能冲突（前端已实现编辑不能修改，新增可以）

			/views/nursing/device/index.vue：设备类型 el-radio 添加 :disabled="formData.id && formData.id !== undefined && formData.id !== ''

	2- 代码实现 - DeviceController 定义接口 edit  - 参照接口文档

		1- 根据主键查询 设备，判断是否存在

		2- 调用华为云工具，修改设备名称

		3- 拷贝前端 DTO 数据至 Device PO，发起更新（只是修改了 设备名称） 

	3- 测试



4- 设备模块接口实现-删除设备

	1- 需求分析

		删除数据库设备数据的 同时 删除华为IOT设备数据

	2- 代码实现 - DeviceController 定义接口 delete  - 参照接口文档

		1- 接收 华为云IOT 设备ID

		2- 根据 设备ID 删除 华为IOT设备

		2- 根据 设备ID 删除 数据库设备

	3- 测试



5- 设备数据处理&展示-课程内容介绍	

	1- 演示问题 & 今日目标

		1- 删除所有历史设备的前提下（保持干净），新建一个设备，查看设备ID和密钥，开始上报数据

		2- 在设备详情页，不断刷新，可以看到实时上报数据，但是 如果后台或者家属希望查看历史上报数据，看不了

		3- 原因：由于IOT平台只会保存最新上报数据，历史的不保存。

		   虽然不保存，但是IOT可以主动推给你，所以要想查看历史上报数据，我们就要自己保存IOT推过来的历史上报数据

		4- 所以今天要研究的主题就是：设备历史上报数据处理 与 展示 问题：也就是如何抓取IOT平台数据，然后存起来，后续做展示

	2- IOT基本原理回顾

		1- 设备通过传感器产生数据（目前是模拟的） -> 通过 MQTT 协议传输数据 -> 华为云IOT物联网平台 

			- MQTT是大名鼎鼎的物联网专属协议，轻量级、精简，不像HTTP含有请求行、请求头、请求体，响应也是，还对低端硬件设备向下兼容

			  原因是：物联网一般设备海量、上报频率非常大、很多硬件设备配置也不是很好，比如电视、机顶盒、冰箱

		2- 华为IOT 基于DB存储数据 -> 基于AMQP协议 异步推送 给 业务应用（前提是业务应用订阅了），或业务应用基于 HTTP 协议同步拉取数据 

		    -> 业务应用 -> 存储在自己数据库 -> 后续 后台页面或者APP 查询即可

		3- 总结下来就是：设备通过MQTT上报数据 -> IOT -> 基于AMQP异步推送数据 -> 业务应用 存储、展示

		4- 拓展：反过来 业务应用也可以向 设备下发指令

			业务应用 -> 通知IOT ->  基于MQTT下发指令到设备

	3- 效果目标

		1- 在设备详情页 物模型数据，点击【查看数据】- 可以查看到当前属性上报的 历史数据

	4- 今日目标

		1- 熟悉AMQP协议特点

		2- 能够使用 AMQP 消费 IOT 推过来的 设备上报数据

		3- 清楚线程池使用方式 和 场景

	

6- 基本概念介绍-同步&异步&消息队列

	1- 同步：任务在后台进行处理，需要等待任务完成后才能 继续执行其他操作

	         比如：任务1完成后才能执行任务2，任务2需要等待任务1完成。这种顺序执行的方式 称为同步

		示例

			- 程序例子：controller 同步调用 多个service

			- 生活例子：打电话			

		- 优点：时效性好，立马能拿到响应结果   

		- 缺点：效率差太慢了

			

	2- 异步：任务提交和执行是相互独立，任务的执行不会阻塞程序的继续执行

	         比如：任务1和任务2可以并行执行，彼此之间相互独立，不需要等待对方的完成。这种并行执行方式称为异步

		示例

			- 程序例子：controller 多线程调用 多个service

			- 生活例子：发微信			

		- 优点：效率好速度快、提高系统并发性、改善系统响应时间

		- 缺点：时效性差，不能立马拿到响应结果，甚至不一定拿得到、复杂性增加、资源消耗增加   

	3- 消息队列 - 结合邮局例子

		1- 生产者 -> Broker(队列) -> 消费者 模型角 色说明【对应 设备 -> 华为IOT(其中也有队列) -> 业务应用】

		2- 打开 rabbitmq 第一天 PPT 看一下这个结构，不关，下一小节还要用

		在线讲义的 topic 理解为 队列... 

		

7- AMQP协议介绍  

	1- AMQP：全称xxx，是一种用于在应用程序之间传递消息的 网络协议，是一种开放标准的消息传递协议，能实现可靠、安全、高效的消息传递

	2- AMQP只是一种规范，对这种协议规范进行实现的具体消息软件有很多，如：RabbitMQ、ApacheActiveMQ、ApacheQpid

	       类似接口 和 类，数据库驱动接口 和 具体数据库厂商数据库 驱动一样

	3- 我们本次使用 ApacheQpid 订阅华为IOT消息，是因为 华为云提供了 能直接下载使用的示例代码，但是代码又臭又长，不用我们自己写，不常用，后续学习RabbitMQ后，经常使用的是 RM 

 

8- 设备数据转发-流程分析

	1- 分析原理、流程

		- 【需要我们操作的】

		1- 在IOT平台创建数据转发规则：设置当有设备上报数据，就将物模型属性数据推送出去（需要在IOT平台配置）

		2- 用户端（应用侧）使用Qpid产品去 订阅IOT平台 推送过来的数据（需要写代码 - IOT平台有示例代码）

		

		- 【自动触发的】

		3- 当设备上报数据到 IOT 平台

		4- IOT 平台自动推送数据

		5- 用户端（应用侧）订阅收取消费数据



9- 设备数据转发-IOT平台创建数据转发规则

	1- 实例内部 点击左侧菜单 【规则】 -> 【创建规则】

		1- 【设置转发数据】 - 能够决定转发什么数据

			1- 规则名称：设备数据转发规则

			2- 数据来源：设备属性

			3- 触发事件：设备属性上报（自动填充）

		2- 【设置转发目标】 - 能够决定最终转发目标（我们这里是 AMQP类型的 DefaultQueue）

			1- 添加

				1- 转发目标：AMQP推送消息队列

				2- 消息队列：使用默认的 DefalutQueue

		3- 【启动规则】

			点击按钮【启动规则】

			

10- 设备数据转发-Qpid消息订阅&测试

	1- 华为云官方提供了 amqp-demo 用于模拟 消费者拉取消费 华为IOT AMQP 队列中的消息

	2- 在线讲义点击链接 下载 官方示例代码（或从资料中拷贝） 解压 amqp-demo，IDEA打开

		1- pom文件设置JDK版本为11

		2- 设置IDEA JDK（11）

		3- 设置maven（默认的）

	3- amqp-demo代码 使用 & 解读

		1- 使用 - 在线讲义中有步骤说明

			1- 找到 AmqpConstants，修改其中的：

				- HOST（AMQP接入域） ：从 控制台右上方 【接入信息】中的 【应用接入-AMQPS】 处获取  【接入地址】

				- PORT（AMQP接入端口）：5671 不用改

				- ACCESS_KEY（接入凭证） ： 点击【接入地址】右侧的 【预置接入凭证】，下载文件获取，秘钥也一样

				- ACCESS_CODE（接入凭证秘钥）

				- DEFAULT_QUEUE（拉取哪个队列消息）：DefaultQueue 不用改

				这几个配置，通过IDEA能看到 很多地方用到了，比如：ReceiveMessageByListener，先不用管

				意义：指定 IOT平台 AMQP 队列的位置、接入凭证秘钥授权、具体拉取消息队列名

				

			2- 放开 AbstractAmqpExample 中 打印消息日志的 注释，并且改为 warn 级别日志

			

			3- 启动 AmqpClientTest main 方法即可测试

				1- 先解读代码

					1- 新建 Amqp 消费者的 List<AbstractAmqpExample> 集合

					2- 新建一个 消费者 : receiveMessageByListener - ReceiveMessageByListener类型

					3- 调用 其 start 方法开始监听消息 ，并将该消费者放入 消费者集合，其中start方法逻辑：

						1- 创建AmqpClient（其中用到了 之前 AmqpConstants中设置的各项配置）

						2- amqppClient 创建消费者，同时指定 消息队列的 名字：DefaultQueue

						3- 指定消费者的 消费逻辑 -> 接收到消息后，调用 processMessage：打印日志 并且 将接收消息树用原子类 自增 1，

						   并且后续会通过线程池执行的任务打印（warn级别）已接收的消息数，所以一旦后续开启消费者代码，会有两句warn级别日志

						

					4- 以每10秒一次的速率（改为5秒），向线程池提交一个任务，任务内容：

						循环 消费者集合，打印每个消费者 目前已经接收消息的条数 

					

				2- 开始测试

					1- 运行 main 方法开始测试 -> 每5秒输出 一句： total recevie count 0，因为目前还没消息从IOT推过来

					2- 运行 huaweicloud-iot-device-sdk-java-master 向 某1个设备推数据

					3- 查看 main 方法运行日志：除了 totoal recevie count发生变化的warn日志，还有一句 消息 warn日志

					4- 停止运行 huaweicloud-iot-device-sdk-java-master，拷贝其中一句消息日志到 1.json ctrl+alt+L，分析结构

			

11- 设备数据转发-Qpid消息订阅代码集成至项目改造

	1- zzyl-nursing-platform 模块 导依赖

		<dependency>

			<groupId>org.apache.qpid</groupId>

			<artifactId>qpid-jms-client</artifactId>

			<version>0.61.0</version>

		</dependency>

	2- 将IOT课程第一天在线讲义 3.4.2 有关第二天的配置 加入到配置文件 application-dev.yml，其中配置值修改为自己的

	3- 将在线讲义中的 AmqpClient 拷贝入到 zzyl-nursing-platform 模块 的 task包下

	4- 解读 AmqpClient 代码

		1- 由于 AmqpClient 实现了 ApplicationRunner 接口，实现了 run方法，所以run方法内容会在项目启动完成时执行，与此类型效果的还有

			- ApplicationContextAware.setApplicationContext()

			- @PostConstruct

			- InitializingBean.afterPropertiesSet()

		2- 开始执行 run 方法中的 start方法，逻辑

			- 通过 huaWeiIotConfigProperties.getConnectionCount() 指定循环次数 4，每次循环中逻辑：

			1- 建立amqp连接	- Connection，其中点进去会用到 host、port、accessKey、accessCode

			2- 为 connection 添加 监听器，连接的各个阶段都会执行对应回调逻辑（非必须）

			3- 创建会话 session，同时指定 ACK 为自动回执

			4- 通过 connection、session 为 DefaultQueue 创建一个消费者，同时设置改消费者的 监听器，逻辑：

				1- 接收到消息后将 处理消息的任务 提交至 一个 线程池，其中处理消息任务逻辑：

					1- 解析消息内容 和  ID

					2- 日志打印

			总结：

				- 项目启动，建立4个connection连接，每个连接创建1个消费者，一共4个消费者

			    - 将来消费者接到消息后，将消息处理任务丢给线程池，任务目前就是日志输出了 接到的消息（改为warn级别）			

				

12- 线程池工作原理

	1- AmqpClient - 192行 属性messageListener 中使用到了线程池 - ThreadPoolTaskExecutor

	2- ThreadPoolTaskExecutor：Spring 封装的 线程池，通过各种 set 方法能看到，其底层依然是 JUC 下的 线程池

	3- 我们 @Autowire 注入的 ThreadPoolTaskExecutor，是在 ThreadPoolConfig.threadPoolTaskExecutor() 配置的

	4- 7个核心参数 及 工作流程



13- 设备数据转发-Qpid消息订阅代码集成至项目测试

	1- 重启 zzyl，项目启动

		1- 验证 打印的 拓展初始化日志顺序

		2- AmqpClient 的 messageListener 开始监听 IOT 推送的消息

		3- 使用 huaweicloud-iot-device-sdk-java-master 向某一设备推消息 到 IOT 平台，IOT平台再自动推送出去

		4- 消费者接收到消息 以warn 级别日志 输出到 控制台

	

14- 设备数据转发-接受设备端数据思路分析

	1- 目前已有：设备上报数据 -> IOT平台 -> AMQP客户端 -> 订阅数据

	2- 接下来需要做的：解析上报数据（IOT设备ID、属性名、属性值、上报时间） -> 保存至数据库（device_data）

	3- device_data 表结构：除了 （IOT设备ID、属性名、属性值、上报时间），其他数据均来自于 主表 device，拷过来即可

	

15- 设备数据转发-保存上报数据 & Bug修复

	1- device_data 代码生成，拷贝至 zzyl

	2- 修改 AmqpClient processMessage 方法，订阅到IOT推送过来的数据之后，添加解析数据json代码

		1- 将json反序列化成 IotMsgNotifyData 对象

		2- 调用 IDeviceDataService.batchInsertDeviceData方法，保存上报数据（添加事务）

			1- 根据IOT设备ID查询设备信息

			2- 判断该设备是否存在

			3- 设备存在，组装设备上报数据（一部分上报的，一部分从主表Device拷贝），批量保存到数据库

		3- 重启 zzyl 测试数据上报 - 验证数据是否进到 device_data

		  保存上报数据【注意事项】Bug修复 - 如不修复，上报数据无法正常入表 - device_data：

			1- 主表 拷贝数据至 从表时，"id","createBy","createTime","updateBy","updateTime" 字段需要忽略（不忽略就是个BUG）

			   否则批量新增时由于从表主键ID都是拷贝的主表的，都是一样的ID，所以会报 Duplicate entry ID重复的错误

			

			2- 新增数据时，由于会经过 MP 的自动填充处理器 MyMetaObjectHandler，在 insertFill 方法中会使用 request.getRequestURI（使用了就是个BUG）

			   - 由于保存上报数据任务 是在线程池多线程环境执行，根本就没有request，不是请求响应环境，所以会报错：No thread-bound request found

			   - 解决：将request.getRequestURI()判断URL是否 以/member开头的判断 封装为一个方法，且将异常【try catch】起来即可，如果出现异常，直接返回false	   

			   

16- 设备数据转发-AmqpClient消息订阅代码解耦优化

	1- 需求：之后 如果有别的service也需要消费 IOT推过来的消息，需求有改动，不需要改动 AmqpClient一句代码，实现AmqpClient订阅 与 业务消费代码解耦

	2- 代码实现：

		1- 新增一个接口：AmqpConsumer，新增一个消费方法： void consumer(IotMsgNotifyData iotMsgNotifyData)

		2- 所有需要 消费消息的servcie 都实现 这个接口，重写 consumer 方法，编写自己的 消息消费逻辑，如：

			- DeviceDataServiceImpl 实现这个接口，重写consumer方法，逻辑为：调用 batchInsertDeviceData 方法，批量保存设备上报数据

			- DeviceDataServiceImpl2 实现这个接口，日志输出 消息即可（为了示范）

		3- 修改 AmqpClient.processMessage 中 消息订阅代码

			- 注释掉原有 具有侵入性的代码：deviceDataService.batchInsertDeviceData(iotMsgNotifyData);

			- 新增 通用订阅代码：

				Map<String, AmqpConsumer> consumerMap = SpringUtil.getBeansOfType(AmqpConsumer.class);

				consumerMap.values().forEach(c -> c.consumer(iotMsgNotifyData));

				

17- 作业

	1- 完成今日课堂代码

	2- 改造 DeviceDataController 中的分页查询 list 方法，支持 startTime 和 endTime 条件查询

## 相关笔记

- [[📖 中州养老课程文档/中州养老课程总览|中州养老课程总览]]
