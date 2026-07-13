---
tags:
  - Java
  - 面向对象
  - 编码规范
  - 封装
status: active
created: 2026-07-12
---

# Java 编码规范与面向对象封装

## 核心原则

> 封装不是“字段全部 private 再生成全部 getter/setter”，而是保护对象的不变量和可变状态，只通过有约束、有业务含义的接口改变对象。

默认编码取向：

- 实例字段默认 `private`，不直接暴露可变状态。
- 对象创建后不应改变的字段优先 `final`。
- 不机械生成全部 setter，只开放业务真正需要的修改能力。
- 对象自身不变量在构造器、静态工厂或领域方法中校验。
- DTO 的格式与必填校验使用 Jakarta Validation。
- 跨对象、跨资源、需要查询外部状态的规则放在 Service 或领域服务中。
- 复杂逻辑按业务语义抽取私有方法或独立协作类。
- 对外只暴露完成用例所需的最小接口，内部实现默认不公开。
- 集合字段不直接返回可变引用，使用不可变副本或受控修改方法。
- 根据项目复杂度选择富领域模型或普通 CRUD 模型，避免为了形式过度设计。

## 为什么不能机械生成 getter/setter

下面的对象虽然字段是 `private`，但外部可以把订单随意改成任何状态，实际上没有保护业务规则：

```java
public class Order {
    private BigDecimal amount;
    private String status;

    public void setAmount(BigDecimal amount) {
        this.amount = amount;
    }

    public void setStatus(String status) {
        this.status = status;
    }
}
```

更合理的做法是让方法表达业务意图，并在状态变化入口维护不变量：

```java
public class Order {

    private final Long id;
    private BigDecimal amount;
    private OrderStatus status;

    public Order(Long id, BigDecimal amount) {
        this.id = Objects.requireNonNull(id, "订单ID不能为空");
        this.amount = requirePositiveAmount(amount);
        this.status = OrderStatus.CREATED;
    }

    public void changeAmount(BigDecimal newAmount) {
        ensureEditable();
        this.amount = requirePositiveAmount(newAmount);
    }

    public void pay() {
        if (status != OrderStatus.CREATED) {
            throw new IllegalStateException("只有待支付订单可以支付");
        }
        this.status = OrderStatus.PAID;
    }

    private void ensureEditable() {
        if (status != OrderStatus.CREATED) {
            throw new IllegalStateException("当前状态不能修改金额");
        }
    }

    private BigDecimal requirePositiveAmount(BigDecimal value) {
        if (value == null || value.signum() <= 0) {
            throw new IllegalArgumentException("订单金额必须大于0");
        }
        return value;
    }

    public Long getId() {
        return id;
    }

    public BigDecimal getAmount() {
        return amount;
    }

    public OrderStatus getStatus() {
        return status;
    }
}
```

## 校验应该放在哪里

| 校验类型 | 推荐位置 | 示例 |
|---|---|---|
| 请求格式、必填、长度 | DTO + Jakarta Validation | `@NotBlank`、`@Size` |
| 对象始终必须满足的不变量 | 构造器、静态工厂、领域方法 | 金额必须大于零 |
| 状态迁移规则 | 有业务含义的领域方法 | 只有待支付订单能支付 |
| 跨对象或需要查询数据库的规则 | Service / 领域服务 | 库存是否足够、账号是否存在 |
| 权限和安全边界 | 应用服务或统一权限层 | 当前用户能否操作目标油站 |

不要把所有校验都塞进 setter。setter 不知道完整业务上下文，也不适合查询数据库或调用外部服务。

## 对外接口与内部实现

### 对外暴露

- 用例需要的 public 方法。
- 稳定、可解释的返回模型。
- 明确的异常和失败语义。
- 必要的接口或端口抽象。

### 内部实现

- 只服务当前类的细节使用 `private` 方法。
- 只服务当前包的实现类优先包级可见，不必全部 `public`。
- 不把 Mapper、内部实体或可变集合直接暴露给 Controller 和外部模块。
- 接口用于隔离真实变化点，不要给每个类机械创建接口。

## DTO、Entity 与领域对象的边界

- DTO：负责传输和输入格式校验，可以为框架绑定保留 getter/setter。
- 数据库 Entity：负责持久化映射，不等于完整领域模型。
- 领域对象：保护业务状态和不变量，通过业务方法改变状态。
- 简单 CRUD 场景可以保持轻量；规则复杂、状态迁移明显时再引入富领域模型。

## 集合与可变状态

不直接暴露内部集合：

```java
public List<OrderItem> getItems() {
    return List.copyOf(items);
}

public void addItem(Product product, int quantity) {
    validateQuantity(quantity);
    items.add(OrderItem.create(product, quantity));
    recalculateTotalAmount();
}
```

这样外部不能绕过校验直接执行 `order.getItems().clear()`。

## Codex 编写 Java 项目时的默认检查清单

- [ ] 字段是否默认 `private`，不可变字段是否可以 `final`？
- [ ] 是否存在无约束、会破坏对象状态的 setter？
- [ ] 必填项和对象不变量是否在创建或状态变化入口校验？
- [ ] 方法名称是否表达业务意图，而不是只有 `setXxx`？
- [ ] 复杂逻辑是否按业务语义拆分，而不是简单切碎代码？
- [ ] Controller、Service、领域对象和持久化层职责是否清晰？
- [ ] 对外接口是否最小化，内部实现是否避免无意义公开？
- [ ] 集合和可变对象是否避免直接暴露引用？
- [ ] 是否存在为了“面向对象”而过度抽象、过度创建接口的问题？
- [ ] 框架要求与封装规则冲突时，是否记录了取舍原因？

## 适用边界

以下情况可以合理放宽，但应明确原因：

- Spring MVC、MyBatis、Jackson 等框架绑定需要无参构造器或 setter。
- DTO 主要承担数据传输，不必强行设计成富领域对象。
- JPA 实体可能需要受保护的无参构造器和特定代理约束。
- 简单后台 CRUD 不需要完整 DDD 分层。
- Lombok 可以减少样板代码，但 `@Data` 不应成为所有领域对象的默认选择。

## 相关笔记

- [[MOC-Java基础]]
- [[☕ Java笔记/Java全套代码质量与优化规范]]
- [[☕ Java笔记/Java笔记总览]]
- [[☕ Java笔记/枚举反射注解]]
- [[☕ Java笔记/接参笔记]]
- [[00-我的长期上下文]]
