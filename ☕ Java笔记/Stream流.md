---
tags:
  - java进阶
date: 2026-06-04
---
list.of ()批量添加数据到集合,但是不能操作集合数据

I

# Stream流

配合lambda表达式,简化集合和数组操作

startWith() 判断 以什么开头

endWith()判断 以什么结尾

注意思想：

1 每条流只能使用一次

2 流中的数据，不影响源集合中的数据（需要调用方法手机流中的数据）

### Stream流思想

#### 1 将数据到流中---获取流对象

单列集合 

直接lest/set .stream()

map 双列集合

map.keySet().stream 

map.valuesSet().stream 

map.entrySet().stream

数组

Stream.of(数据)

Arrays.stream(数组)

#### 2 中间方法--可以继续调用流中的其他方法

##### filter() 过滤---括号里面需要返回布尔类型

##### limit()截取前面多少个元素

##### skip()跳过前多少个元素

##### distinct()去重  通过equals方法实现

##### concat拼接两个流 

##### map(new Function) 映射 将流中数据转成其他类型的数据





#### 3 终结方法

foreach（）遍历

conut（）流中元素个数

collector+下面的+（）：

​			toList（）收集成list集合

​			toSet()
​			toMap(Function keyMapper , Function valueMapper) 把			元素收集到Map集合中

joinning（”分隔符”）收集成字符串  必须保证流中元素为String类型

## 相关笔记

- [[☕ Java笔记/Java笔记总览|Java笔记总览]]

- [[☕ Java笔记/函数式编程|函数式编程]]

