---
tags: [MQ, RabbitMQ, 面试问答]
date: 2026-07-03
sources:
  - 黑马微服务: day04-MQ基础
  - Hermes拷问: 8道题逐层深入
---

> 📂 [[微服务框架-黑马新版|课程索引]] | 课程笔记: [[day04-MQ基础]]

# day04 MQ基础 — 面试问答

> 从第一性原理出发，8 道题逐层深入。用自己的话复述，不要死记。

---

## 第一题：同步调用三大问题

**问**：同步调用（OpenFeign）存在哪三个问题？分别解释本质。

**答**：

1. **性能下降**：不是单个调用慢，是**串行阻塞**——每个调用必须等上一个完成才能继续，总耗时 = 所有调用耗时之和。
2. **级联失败**：链式阻塞依赖，一个服务挂了 → 调用方超时抛异常 → **事务回滚**。钱扣了、通知调不通、整个交易失败。
3. **拓展性差**：每次加需求（短信/积分/推送）都要改支付代码，违反开闭原则。

---

## 第二题：MQ 的四个角色

**问**：MQ 有哪些角色？消息从生产者到消费者的完整链路怎么走？

**答**：

```
Producer → Broker(Exchange → Queue) → Consumer
              ↑
         Virtual Host（数据隔离层）
```

- **Producer**（生产者）：发送消息
- **Broker**（消息代理）：RabbitMQ 服务本身，不是泛称"中间件"
- **Exchange**（交换机）：只负责**路由**，**不存消息**
- **Queue**（队列）：**存储消息**，等待消费者处理
- **Consumer**（消费者）：监听队列，消费消息
- **Virtual Host**：数据隔离层（类比数据库的不同 database），不同 vhost 的 exchange/queue 互不可见

> **第一性原理**：Exchange 为什么不能省？直接发队列 = 生产者必须知道队列名 = 紧耦合。Exchange 是路由抽象层——生产者只认消息类型（routingKey），不认队列。

---

## 第三题：Exchange 存不存消息？

**问**：Exchange 存不存消息？不存的话消息在哪儿？

**答**：Exchange **不存消息**，只做路由转发。消息存在 **Queue** 里。

验证方法：往没绑定队列的 Exchange 发消息 → 消息直接丢失。

---

## 第四题：三种交换机

**问**：三种交换机叫什么？路由规则各是什么？一句话区分。

**答**：

| 类型 | 路由规则 | 记忆口诀 |
|---|---|---|
| **Fanout** | 广播，**复制**给所有绑定的队列 | 一呼百应 |
| **Direct** | 精确匹配 RoutingKey | 对号入座 |
| **Topic** | 通配符匹配（`#` 零或多词，`*` 单词） | 模式匹配 |

**常见混淆纠正**：
- Fanout 是**复制**给所有队列，不是轮询
- 轮询是 Work Queue 里**多个消费者抢同一个队列**，是消费者侧的事，跟交换机无关

**场景选择速查**：
- 一条消息所有服务都要 → **Fanout**
- 不同消息类型路由到不同队列 → **Direct**
- 需要按模式批量匹配（如 `order.#` 匹配所有订单消息）→ **Topic**

---

## 第五题：Work Queue 的问题

**问**：Work Queue 默认分配策略有什么问题？为什么？怎么修正？

**答**：

**默认问题**：RabbitMQ 按 **round-robin 平均分配**，不考虑消费者处理速度。快的干完了等着，慢的越堆越多。

**本质原因**：RabbitMQ 在消息到达时立刻分派（push），不等消费者 ack 完。这是"分发"不是"负载均衡"。

**修正**：`spring.rabbitmq.listener.simple.prefetch=1`

意思是消费者告诉 Broker："一次只给我一条，ack 了再给下一条。"实现**能者多劳**——谁处理快谁拿更多。

---

## 第六题：消息序列化的坑

**问**：SpringAMQP 默认用什么序列化？有什么问题？怎么改？

**答**：

**默认**：JDK 自带序列化（`ObjectOutputStream`），不是 Spring 的。

**三个问题**：
1. 数据体积大
2. RabbitMQ 控制台显示二进制乱码，排错没法看
3. 不跨语言——Python/Go 消费者无法反序列化 `application/x-java-serialized-object`

**修正**：改为 **Jackson JSON 序列化**

```java
@Bean
public MessageConverter messageConverter() {
    Jackson2JsonMessageConverter converter = new Jackson2JsonMessageConverter();
    converter.setCreateMessageIds(true);  // 自动生成 messageId，用于幂等性
    return converter;
}
```

> publisher 和 consumer 两端都要配，否则一端 JSON 一端 JDK 反序列化会报错。

---

## 第七题：综合设计

**问**：用户注册后，发短信 + 发邮件 + 加积分。用 MQ 怎么设计？用什么交换机？几个队列？为什么？

**答**：

- **交换机**：**Fanout**
- **队列**：3 个（sms.queue、email.queue、score.queue）
- **为什么 Fanout 不是 Topic**：一条消息三个服务全要 = 广播语义。Fanout 天生干这个——一份消息复制给所有绑定队列。Topic 绑 `#` 也能实现广播，但那是拿 Topic 当 Fanout 用，设计意图不清晰。

**变体**：如果后期要分流——注册消息只发邮件+积分，支付消息只发短信+积分——这时才该上 **Topic**，按 `user.register` / `order.pay` 区分 routingKey。

---

## 第八题：异步调用的心智模型转变

**问**：同步调用和异步调用最本质的区别是什么？

**答**：

| | 同步（Feign） | 异步（MQ） |
|---|---|---|
| 等待 | 阻塞等结果 | 发完就走 |
| 返回值 | 有 | **没有** |
| 失败感知 | 立即知道 | **不知道对方收没收到** |

> 异步调用的核心代价：**消息发出去后，没有"成功/失败"反馈，没有"返回数据"。**
> 这引出 day05 的两大主题——**可靠性**（怎么保证消息不丢）和**幂等性**（同一条消息被重复消费怎么办）。

---

## 踩坑清单（自检用）

- [ ] Exchange 没绑定 Queue → 发消息丢了（控制台验证过）
- [ ] Work Queue 没设 prefetch → 慢消费者堆积，快消费者闲着
- [ ] 没换 JSON 转换器 → 控制台看消息是乱码，跨语言无法消费
- [ ] Fanout 说成"轮询" → 轮询是 Work Queue 消费者侧的事
- [ ] JDK 序列化说成"Spring 底层序列化" → 是 JDK 的 `ObjectOutputStream`
- [ ] "中间件" → 精确说 "Broker"
