---
tags:
  - java基础
date: 2026-06-04
---
# 一、Object 类核心方法

`Object` 是所有 Java 类的**父类**，任何对象都能调用这些方法。

| 方法签名                     | 作用                                                     | 常用场景                         |
| :--------------------------- | :------------------------------------------------------- | :------------------------------- |
| `boolean equals(Object obj)` | 判断两个对象**内容是否相等**（默认比较地址，子类可重写） | 字符串、自定义对象比较           |
| `int hashCode()`             | 返回对象的哈希码值                                       | 哈希集合（HashMap、HashSet）去重 |
| `String toString()`          | 返回对象的字符串表示形式                                 | 打印对象、日志输出               |
| `Class<?> getClass()`        | 返回对象的运行时类                                       | 反射、获取对象类型               |
| `protected Object clone()`   | 创建并返回对象的副本                                     | 对象浅拷贝                       |
| obj.notify(线程)             | 唤醒某个线程                                             |                                  |
| obj.notifyAll()              | 唤醒所有线程                                             |                                  |
| obj.wait()                   | 等待唤醒                                                 |                                  |



# 二、String 类常用 API

`String` 是不可变字符串，是 Java 最常用的类，表格按**功能分类**。

### 1. 基础获取 / 判断

| 方法                               | 作用                             |
| :--------------------------------- | :------------------------------- |
| `int length()`                     | 获取字符串长度                   |
| `char charAt(int index)`           | 获取指定索引位置的字符           |
| `boolean isEmpty()`                | 判断字符串是否为空（长度 = 0）   |
| `boolean equals(Object obj)`       | 严格比较字符串内容（区分大小写） |
| `boolean equalsIgnoreCase(String)` | 忽略大小写比较内容               |
| `boolean contains(CharSequence)`   | 判断是否包含指定子串             |



### 2. 查找与索引

| 方法                                | 作用                                   |
| :---------------------------------- | :------------------------------------- |
| `int indexOf(String str)`           | 返回子串第一次出现的索引，无则返回 - 1 |
| `int lastIndexOf(String str)`       | 返回子串最后一次出现的索引             |
| `boolean startsWith(String prefix)` | 判断是否以指定前缀开头                 |
| `boolean endsWith(String suffix)`   | 判断是否以指定后缀结尾                 |



### 3. 截取、替换、分割

| 方法                                                 | 作用                             |
| :--------------------------------------------------- | :------------------------------- |
| `String substring(int beginIndex)`                   | 从指定索引截取到字符串末尾       |
| `String substring(int begin, int end)`               | 截取 [begin, end) 区间的字符串   |
| `String replace(CharSequence old, CharSequence new)` | 替换所有指定字符 / 字符串        |
| `String[] split(String regex)`                       | 按规则分割字符串，返回字符串数组 |
| `String trim()`                                      | 去除字符串**首尾**空格           |



### 4. 转换相关

| 方法                              | 作用                               |
| :-------------------------------- | :--------------------------------- |
| `String toLowerCase()`            | 转小写                             |
| `String toUpperCase()`            | 转大写                             |
| `char[] toCharArray()`            | 字符串转字符数组                   |
| `static String valueOf(任意类型)` | 基本类型 / 对象 转字符串（最安全） |



# 三、Java 时间类常用 API

Java 8 推出 `LocalDateTime`、`LocalDate`、`LocalTime`，**替代旧的 Date、Calendar**，线程安全、易用。

### 1. 日期时间创建 / 获取

| 类              | 常用方法                           | 作用                           |
| :-------------- | :--------------------------------- | :----------------------------- |
| `LocalDate`     | `LocalDate.now()`                  | 获取当前**日期**（yyyy-MM-dd） |
| `LocalDate`     | `LocalDate.of(年,月,日)`           | 指定日期创建对象               |
| `LocalTime`     | `LocalTime.now()`                  | 获取当前**时间**（HH:mm:ss）   |
| `LocalDateTime` | `LocalDateTime.now()`              | 获取当前**日期 + 时间**        |
| `LocalDateTime` | `LocalDateTime.of(年,月,日,时,分)` | 指定日期时间创建               |



### 2. 获取时间分量

| 方法              | 作用             |
| :---------------- | :--------------- |
| `getYear()`       | 获取年           |
| `getMonthValue()` | 获取月份（1-12） |
| `getDayOfMonth()` | 获取日           |
| `getHour()`       | 获取小时         |
| `getMinute()`     | 获取分钟         |
| `getSecond()`     | 获取秒           |



### 3. 时间计算（加减）

| 方法                                         | 作用         |
| :------------------------------------------- | :----------- |
| `plusYears(long n)` / `minusYears(long n)`   | 加 / 减 年   |
| `plusMonths(long n)` / `minusMonths(long n)` | 加 / 减 月   |
| `plusDays(long n)` / `minusDays(long n)`     | 加 / 减 天   |
| `plusHours(long n)` / `minusHours(long n)`   | 加 / 减 小时 |



### 4. 时间比较 / 判断

| 方法                          | 作用                             |
| :---------------------------- | :------------------------------- |
| `boolean isBefore(时间对象)`  | 判断是否在指定时间**之前**       |
| `boolean isAfter(时间对象)`   | 判断是否在指定时间**之后**       |
| `boolean isEqual(时间对象)`   | 判断时间是否相等                 |
| `Duration.between(开始,结束)` | 计算两个**时间**的间隔（时分秒） |
| `Period.between(开始,结束)`   | 计算两个**日期**的间隔（年月日） |



### 5. 格式化与解析（DateTimeFormatter）

| 方法                               | 作用              |
| :--------------------------------- | :---------------- |
| `format(DateTimeFormatter)`        | 时间对象 → 字符串 |
| `parse(字符串, DateTimeFormatter)` | 字符串 → 时间对象 |



# 四、Java 集合常用 API 总结

## 1. Collection 接口

**所有单列集合的父接口**

| 方法                           | 作用                     |
| :----------------------------- | :----------------------- |
| `boolean add(E e)`             | 添加元素                 |
| `boolean remove(Object o)`     | 删除指定元素             |
| `boolean contains(Object o)`   | 判断是否包含指定元素     |
| `int size()`                   | 获取集合元素个数         |
| `boolean isEmpty()`            | 判断集合是否为空         |
| `void clear()`                 | 清空集合                 |
| `Object[] toArray()`           | 集合转数组               |
| `boolean addAll(Collection c)` | 批量添加另一个集合的元素 |



## 2. List 接口

**有序、可重复、有索引。继承 Collection，额外拥有索引相关方法**

| 方法                       | 作用                     |
| :------------------------- | :----------------------- |
| `E get(int index)`         | 根据索引获取元素         |
| `E set(int index, E e)`    | 修改指定索引位置的元素   |
| `void add(int index, E e)` | 在指定索引插入元素       |
| `E remove(int index)`      | 根据索引删除元素         |
| `int indexOf(Object o)`    | 获取元素第一次出现的索引 |



## 3. ArrayList

数组实现，查询快、增删慢

完全使用 List / Collection 方法，**无特有常用方法**

常用方法同上，**高频：add、get、remove、size、contains**



## 4. LinkedList

**链表实现，增删快、查询慢。继承 List，额外拥有队列 / 栈方法**

| 方法                 | 作用             |
| :------------------- | :--------------- |
| `void addFirst(E e)` | 添加到头部       |
| `void addLast(E e)`  | 添加到尾部       |
| `E getFirst()`       | 获取第一个元素   |
| `E getLast()`        | 获取最后一个元素 |
| `E removeFirst()`    | 删除第一个元素   |
| `E removeLast()`     | 删除最后一个元素 |



## 5. Set 接口

无序、无索引、不可重复

方法全部来自 Collection，无特有方法

常用：`add、remove、contains、size、isEmpty、clear`



## 6. HashSet

哈希表实现，无序、去重最快

完全使用 Set 方法，无特有常用 API

特点：无序、无索引、不重复、查询极快



## 7. TreeSet

红黑树，自动排序、去重

**Set + 排序功能**

| 方法            | 作用               |
| :-------------- | :----------------- |
| `E first()`     | 获取最小元素       |
| `E last()`      | 获取最大元素       |
| `E pollFirst()` | 删除并返回最小元素 |
| `E pollLast()`  | 删除并返回最大元素 |



## 8. Map 接口

双列集合：key-value，key 唯一

| 方法                                  | 作用                         |
| :------------------------------------ | :--------------------------- |
| `V put(K key, V value)`               | 添加 / 修改键值对            |
| `V get(Object key)`                   | 根据 key 获取 value          |
| `V remove(Object key)`                | 根据 key 删除键值对          |
| `boolean containsKey(Object key)`     | 判断是否包含指定 key         |
| `boolean containsValue(Object value)` | 判断是否包含指定 value       |
| `int size()`                          | 获取键值对个数               |
| `void clear()`                        | 清空集合                     |
| `Set<K> keySet()`                     | 获取所有 key 的集合          |
| `Collection<V> values()`              | 获取所有 value 的集合        |
| `Set<Map.Entry<K,V>> entrySet()`      | 获取所有键值对对象（遍历用） |



## 9. HashMap

哈希表，无序、key 唯一、线程不安全

完全使用 Map 方法，无特有常用 API

最常用 Map，查询极快、无序



## 10. TreeMap

红黑树，key 自动排序

**Map + 按键排序**

| 方法                     | 作用           |
| :----------------------- | :------------- |
| `K firstKey()`           | 获取最小 key   |
| `K lastKey()`            | 获取最大 key   |
| `Map.Entry firstEntry()` | 获取最小键值对 |
| `Map.Entry lastEntry()`  | 获取最大键值对 |



## 11. LinkedHashMap

哈希表 + 链表，保证存入顺序

完全使用 Map 方法

特点：**有序（存入顺序）、key 唯一、比 HashMap 稍慢**



# 五、Queue 接口常用 API 总结

Queue：**队列，先进先出 FIFO**，继承 Collection 接口。

## 1. Queue 核心常用方法表

| 方法                 | 作用                     | 异常情况                   |
| :------------------- | :----------------------- | :------------------------- |
| `boolean offer(E e)` | 向队列**尾部添加**元素   | 队列满不抛异常，返回 false |
| `E poll()`           | 获取并**删除队首**元素   | 队列为空返回 null          |
| `E peek()`           | **获取但不删除**队首元素 | 队列为空返回 null          |
| `boolean add(E e)`   | 向队列尾部添加元素       | 队列满**抛出异常**         |
| `E remove()`         | 获取并删除队首元素       | 队列为空**抛出异常**       |
| `E element()`        | 获取但不删除队首元素     | 队列为空**抛出异常**       |



## 2. 常见 Queue 实现类

1. **LinkedList**：既实现 List 也实现 Queue，日常最常用队列
2. **ArrayDeque**：数组双端队列，效率高于 LinkedList
3. **PriorityQueue**：优先级队列，自带自然排序



## 3. 补充：Deque 双端队列（Queue 子接口）

可当**队列 / 栈**使用，常用：

- `push(E e)`：入栈
- `E pop()`：出栈
- `isEmpty()`：判断队列 / 栈是否为空



# 六、Java Stack 常用 API 总结



## 1. 传统 Stack 类（java.util.Stack，继承 Vector）

**特点：后进先出 LIFO**

| 方法                   | 作用                                          |
| :--------------------- | :-------------------------------------------- |
| `E push(E item)`       | **入栈**：把元素压入栈顶                      |
| `E pop()`              | **出栈**：移除并返回栈顶元素，栈空抛异常      |
| `E peek()`             | **取栈顶**：只查看不删除，栈空抛异常          |
| `boolean empty()`      | 判断栈是否为空                                |
| `int search(Object o)` | 查找元素位置，返回距栈顶偏移量；找不到返回 -1 |



## 2. 开发推荐：用 Deque 代替 Stack

> 官方不推荐用老旧 `Stack` 类，推荐 **`Deque<E>` 当栈用**，性能更好、线程设计更合理。

**Deque 模拟栈常用 API**

| 方法        | 等价栈操作 | 作用           |
| :---------- | :--------- | :------------- |
| `push(E e)` | 入栈       | 头部压入元素   |
| `E pop()`   | 出栈       | 弹出头部元素   |
| `E peek()`  | 查栈顶     | 获取头部不删除 |

**常用实现类**：`ArrayDeque`、`LinkedList`

```
Deque<String> stack = new ArrayDeque<>();
stack.push("A");  // 入栈
stack.pop();      // 出栈
stack.peek();     // 看栈顶
```



## 3. Stack & Queue 口诀

- **Queue 队列**：先进先出，offer/poll/peek
- **Stack 栈**：后进先出，push/pop/peek
- 业务开发统一用 **Deque 代替老式 Stack**



# 七、Math 类常用 API

`java.lang.Math` 静态工具类，**所有方法都是静态**，直接 `Math.xxx()` 调用。

## 1. 常用常量

| 常量      | 作用                      |
| :-------- | :------------------------ |
| `Math.PI` | 圆周率 π 约 3.14159       |
| `Math.E`  | 自然对数底数 e 约 2.71828 |



## 2. 取整相关

| 方法                   | 作用                | 示例           |
| :--------------------- | :------------------ | :------------- |
| `Math.round(double d)` | 四舍五入，返回 long | round(3.6)=4   |
| `Math.ceil(double d)`  | 向上取整（进一）    | ceil(3.1)=4.0  |
| `Math.floor(double d)` | 向下取整（舍小数）  | floor(3.9)=3.0 |



## 3. 最值、绝对值

| 方法                   | 作用             |
| :--------------------- | :--------------- |
| `Math.abs(int/double)` | 求绝对值         |
| `Math.max(a,b)`        | 返回两个数最大值 |
| `Math.min(a,b)`        | 返回两个数最小值 |



## 4. 幂运算、开方

| 方法                          | 作用           |
| :---------------------------- | :------------- |
| `Math.sqrt(double a)`         | 平方根         |
| `Math.pow(double a,double b)` | 求 a 的 b 次幂 |
| `Math.cbrt(double a)`         | 立方根         |



## 5. 随机数

| 方法            | 作用                      |
| :-------------- | :------------------------ |
| `Math.random()` | 返回 `[0.0,1.0)` 随机小数 |



## 6. 三角函数（弧度制）

| 方法                         | 作用       |
| :--------------------------- | :--------- |
| `Math.sin(double a)`         | 正弦       |
| `Math.cos(double a)`         | 余弦       |
| `Math.tan(double a)`         | 正切       |
| `Math.toRadians(double ang)` | 角度转弧度 |
| `Math.toDegrees(double rad)` | 弧度转角度 |



## 7. 符号、取舍辅助

| 方法                    | 作用                                 |
| :---------------------- | :----------------------------------- |
| `Math.signum(double d)` | 返回符号：正数 1、负数 - 1、0 返回 0 |
| `Math.exp(double a)`    | 返回 e 的 a 次方                     |
| `Math.log(double a)`    | 自然对数 ln                          |
| `Math.log10(double a)`  | 以 10 为底对数                       |



# 八、Number 抽象类 常用 API

`java.lang.Number` 是**所有包装类的父类**：

`Integer、Long、Byte、Short、Float、Double` 都直接继承 Number。

作用：提供**基本类型互相转换**的通用方法。

## 1. Number 核心常用 API 表

| 方法返回值 | 方法名          | 作用说明         |
| :--------- | :-------------- | :--------------- |
| `byte`     | `byteValue()`   | 转为 byte 类型   |
| `short`    | `shortValue()`  | 转为 short 类型  |
| `int`      | `intValue()`    | 转为 int 类型    |
| `long`     | `longValue()`   | 转为 long 类型   |
| `float`    | `floatValue()`  | 转为 float 类型  |
| `double`   | `doubleValue()` | 转为 double 类型 |



## 2. 补充：六大包装类共性常用 API

### 2.1 字符串转基本类型（静态方法）

| 方法                           | 作用            |
| :----------------------------- | :-------------- |
| `Integer.parseInt(String s)`   | 字符串转 int    |
| `Double.parseDouble(String s)` | 字符串转 double |
| `Long.parseLong(String s)`     | 字符串转 long   |



### 2.2 基本类型 / 字符串 转包装类对象

| 方法                        | 作用                      |
| :-------------------------- | :------------------------ |
| `Integer.valueOf(int i)`    | int 转 Integer            |
| `Integer.valueOf(String s)` | 字符串转 Integer 包装对象 |



### 2.3 包装类转字符串

| 方法         | 作用             |
| :----------- | :--------------- |
| `toString()` | 包装对象转字符串 |



# 九、Java BigDecimal 常用 API 表格总结

## 1. 创建对象常用方式

| 方法                             | 作用                       | 备注                     |
| :------------------------------- | :------------------------- | :----------------------- |
| `new BigDecimal(String val)`     | 通过**字符串**构造精确小数 | **推荐**，无精度丢失     |
| `new BigDecimal(double val)`     | 通过 double 构造           | 不推荐，有精度丢失       |
| `BigDecimal.valueOf(double val)` | 静态方法创建               | 比直接 new double 更稳妥 |



## 2. 四则运算（返回新 BigDecimal，原对象不变）

| 方法                                           | 作用                          |
| :--------------------------------------------- | :---------------------------- |
| `add(BigDecimal b)`                            | 加法                          |
| `subtract(BigDecimal b)`                       | 减法                          |
| `multiply(BigDecimal b)`                       | 乘法                          |
| `divide(BigDecimal b)`                         | 除法（不指定保留位数会报错）  |
| `divide(BigDecimal b, int 保留位数, 舍入模式)` | 带保留小数位数 + 舍入模式除法 |



## 3. 舍入 / 保留小数

| 方法                                        | 作用                           |
| :------------------------------------------ | :----------------------------- |
| `setScale(int newScale, RoundingMode mode)` | 设置保留小数位数并指定舍入规则 |

### 常用舍入模式（背这几个）

| 舍入模式               | 含义               |
| :--------------------- | :----------------- |
| `RoundingMode.HALF_UP` | 四舍五入（最常用） |
| `RoundingMode.FLOOR`   | 直接向下取整       |
| `RoundingMode.CEILING` | 向上取整           |



## 4. 大小比较

| 方法                      | 作用                                           |
| :------------------------ | :--------------------------------------------- |
| `compareTo(BigDecimal b)` | 比较两个数值大小返回：1 大于 / 0 等于 /-1 小于 |

> 注意：**不要用 ==、equals 比较数值**，统一用 `compareTo`



## 5. 类型转换

| 方法            | 作用       |
| :-------------- | :--------- |
| `intValue()`    | 转 int     |
| `longValue()`   | 转 long    |
| `doubleValue()` | 转 double  |
| `toString()`    | 转为字符串 |



## 6. 正负绝对值

| 方法       | 作用     |
| :--------- | :------- |
| `abs()`    | 取绝对值 |
| `negate()` | 取相反数 |



## 7. 常用常量

| 常量              | 说明    |
| :---------------- | :------ |
| `BigDecimal.ZERO` | 常量 0  |
| `BigDecimal.ONE`  | 常量 1  |
| `BigDecimal.TEN`  | 常量 10 |

## 相关笔记

- [[☕ Java笔记/Java笔记总览|Java笔记总览]]

- [[💼 面试/Java集合面试题|集合面试]]


