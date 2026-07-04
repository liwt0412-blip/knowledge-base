---
tags: [MQ, RabbitMQ, 消息队列, 课堂总结]
date: 2026-07-01
sources:
  - 东哥随堂: 微服务阶段/day5-MQ基础/课堂总结
---

# 微服务 Day4 随堂总结 — MQ 基础

## 1. 同步 vs 异步

### 同步通讯

就像**打电话**，需要实时响应。

| 优点 | 缺点 |
|---|---|
| 时效性强，立即得到结果 | 耦合度高 |
| 调用有顺序性 | 性能和吞吐能力下降 |
| | 有额外资源消耗 |
| | 有级联失败问题 |

### 异步通讯

就像**发邮件**，不需要马上回复。

| 优点 | 缺点 |
|---|---|
| 吞吐量提升：无需等待订阅者处理 | 时效性差 |
| 故障隔离：无直接调用，不存在级联失败 | 架构复杂，业务没有明显流程线 |
| 调用间无阻塞，无无效资源占用 | 依赖 Broker 的可靠、安全、性能 |
| 耦合度极低，服务灵活插拔可替换 | |
| **流量削峰**：无论流量多大都由 Broker 接收，订阅者按自己速度处理 | |

## 2. 主流 MQ 产品对比

| 产品 | 语言 | AMQP | 可用性 | 延迟 | 可靠性 | 吞吐量 |
|---|---|---|---|---|---|---|
| **RabbitMQ** | Erlang | ✅ | 高 | 微秒级 | 高 | 一般 |
| **RocketMQ** | Java | ❌ | 高 | 毫秒级 | 高 | 高 |
| **ActiveMQ** | Java | ✅ | 一般 | 毫秒级 | 一般 | 差 |
| **Kafka** | Scala & Java | ❌ | 高 | 毫秒级 | 一般 | 非常高 |

## 3. SpringAMQP

基于 AMQP 协议定义的一套 API 规范，SpringBoot 对其实现自动装配，底层默认实现为 `spring-rabbit`，使用非常方便。

## 4. RabbitMQ 核心概念

```
消息生产者 ──msg(routingKey)──→ 交换机(Exchange) ──路由──→ 队列(Queue) ──消费──→ 消费者
```

| 概念 | 说明 |
|---|---|
| **Connection**（连接） | RabbitMQ 的 socket 连接，封装 socket 协议逻辑 |
| **Channel**（通道） | 最重要的操作接口，定义 Queue/Exchange、绑定、发布消息。类比 Hibernate 的 Session |
| **Exchange**（交换机） | 从生产者接收消息，路由转发至队列 |
| **Queue**（队列） | 从交换机接收消息并存储 |
| **Virtual Host**（虚拟主机） | 多租户概念，做数据隔离 |
| **RoutingKey** | 生产者投递消息时携带的路由标识 |
| **BindingKey** | 队列与交换机绑定的标识，匹配的 RoutingKey 消息会被路由到该队列 |

## 5. 五种消息模式

### 5.1 Simple Queue（简单队列）

```
生产者(routingKey=队列名) → 默认交换机("") --bindingKey=队列名--→ 队列 → 消费者
```

- 生产者携带 routingKey（队列名）→ 默认交换机 `""`
- 声明队列，以队列名作为 bindingKey 绑定至默认交换机
- 默认交换机根据 routingKey 路由到对应队列

### 5.2 Work Queue（工作队列）

```
生产者 → 队列 → 多个消费者（同一条消息只被一个消费者消费）
```

- 与简单队列一致，但多个消费者竞争消费，效率大增
- **问题**：默认预取消息平均分配，未最大化利用资源
- **优化**：修改消费端参数 `spring.rabbitmq.listener.simple.prefetch = 1`，消费者处理完 + ack 后再分配，**能者多劳**

### 5.3 Fanout（发布订阅 / 广播）

```
生产者(routingKey="") → Fanout交换机 --bindingKey=""--→ 所有绑定队列 → 消费者
```

- Fanout 交换机将消息**广播**到所有绑定的队列
- routingKey 和 bindingKey 都为空即可

### 5.4 Direct（路由模式）

```
生产者(routingKey="red") → Direct交换机 --bindingKey="red"/"blue"--→ 匹配的队列 → 消费者
```

- Direct 交换机根据**精确匹配**的 bindingKey 路由
- 消息 routingKey 和队列 bindingKey 一致才转发

### 5.5 Topic（主题模式）

```
生产者(routingKey="china.news") → Topic交换机 --bindingKey="china.#"--→ 匹配的队列 → 消费者
```

- Topic 交换机根据**通配符匹配**路由

| 通配符 | 含义 |
|---|---|
| `*` | 匹配**一个**单词 |
| `#` | 匹配**0 个或多个**单词 |

> **技巧**：Topic 可以模拟 Fanout 和 Direct：
> - 模拟 Fanout：bindingKey 设为 `#`
> - 模拟 Direct：bindingKey 设为精确的 routingKey

## 6. 消息转换器

- **默认**：`SimpleMessageConverter`，基于 JDK `ObjectOutputStream` 序列化。缺点：**可读性差、传输效率低**
- **优化**：替换为 `Jackson2JsonMessageConverter`（生产者+消费者都要配）

```java
// 1. 引依赖
// jackson-databind

// 2. 定义 Bean
@Bean
public MessageConverter jsonMessageConverter() {
    return new Jackson2JsonMessageConverter();
}
```

## 7. 编码方式

### 7.1 SpringBoot 方式

**准备工作：**
- 依赖：`spring-boot-starter-amqp`
- 配置：host / port / username / password / virtual-host

**生产者：**

```java
rabbitTemplate.convertAndSend("exchange.log", "simple.queue", "消息内容");
```

**消费者：**

```java
@RabbitListener(queues = {"simple.queue"})
public void listenWorkQueue1(String msg) throws InterruptedException {
    System.out.println("消费者接收到消息：【" + msg + "】" + LocalTime.now());
    Thread.sleep(20);
}
```

**声明交换机/队列 — 两种方式：**

方式一：配置类 `@Bean`

```java
@Bean
public FanoutExchange fanoutExchange() {
    return new FanoutExchange("itcast.fanout");
}
@Bean
public Queue fanoutQueue1() {
    return new Queue("fanout.queue1");
}
@Bean
public Binding fanoutBinding1(Queue fanoutQueue1, FanoutExchange fanoutExchange) {
    return BindingBuilder.bind(fanoutQueue1).to(fanoutExchange);
}
```

方式二：消费者方法上 `@RabbitListener` 注解声明

```java
@RabbitListener(bindings = @QueueBinding(
    value = @Queue(name = "direct.queue1"),
    exchange = @Exchange(name = "itcast.direct", type = ExchangeTypes.DIRECT),
    key = {"red", "blue"}
))
public void listenDirectQueue1(String msg) {
    System.out.println("消费者接收到direct.queue1的消息：【" + msg + "】");
}
```

### 7.2 原生方式

```java
// 1. 创建工厂
ConnectionFactory factory = new ConnectionFactory();
factory.setHost("127.0.0.1");
factory.setPort(5672);
factory.setVirtualHost("/");
factory.setUsername("guest");
factory.setPassword("guest");

// 2. 创建连接
Connection connection = factory.newConnection();

// 3. 创建 Channel
Channel channel = connection.createChannel();

// 4. 声明交换机
channel.exchangeDeclare("my_exchange", BuiltinExchangeType.DIRECT, true, false, false, null);
//   参数: 名称, 类型(DIRECT/FANOUT/TOPIC/HEADERS), 持久化, 自动删除, 内部使用, 参数

// 5. 声明队列
channel.queueDeclare("my_queue", true, false, false, null);
//   参数: 名称, 持久化, 独占, 自动删除, 参数

// 6. 绑定队列和交换机
channel.queueBind("my_queue", "my_exchange", "error");
//   Fanout 类型时 routingKey 设为 ""

// 7. 发送消息
channel.basicPublish(exchangeName, "error", null, body.getBytes());

// 8. 接收消息
Consumer consumer = new DefaultConsumer(channel) {
    @Override
    public void handleDelivery(String consumerTag, Envelope envelope,
                               AMQP.BasicProperties properties, byte[] body) throws IOException {
        System.out.println("body：" + new String(body));
    }
};
channel.basicConsume(queueName, true, consumer);
```

> ⚠️ **注意**：无论生产者的异步代码是否已自己捕获异常，还是消费者代码内部，**一定要打日志**，防止后续排错困难。

## 相关笔记

- [[day04-MQ基础|day04 正课笔记]]
- [[day05-MQ高级|day05 MQ 高级]]
- [[微服务框架-黑马新版|课程总索引]]
- [[MOC-Spring框架]]
