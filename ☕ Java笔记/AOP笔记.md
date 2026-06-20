---
tags:
  - spring
  - java进阶
date: 2026-06-04
---
# AOP笔记

## 一、AOP切面方法是使用步骤

### 1. 添加AOP起步依赖

```
<dependency>
	<groupId>org.springframework.boot</groupId>
	<artifactId>spring-boot-starter-aop</artifactId>
</dependency>
```



### 2. 定义一个切面类，添加两个注解：

- ​	@Component：将这个类交给IOC容器管理
- ​	@Aspect：声明这个类为切面类



### 3. 切面方法，添加通知类型

```java
// 代码示例
@Component  //将这个类交给IOC容器管理
@Aspect     //声明这个类为切面类
public class RecordTimeAspect {
    @Around("execution(* com.carrotking.service.impl.DeptServiceImpl.*(..))")
    public Object recordTime(ProceedingJoinPoint pjp) throws Throwable {
        //1. 获取开始时间
        long start = System.currentTimeMillis();

        //2. 运行原始业务方法
        Object result = pjp.proceed(); // result 原始方法运行的返回值

        //3. 获取结束时间
        long end = System.currentTimeMillis();
        System.Out.println(" {} 方法执行耗时: {}", pjp.getSignature() ,end - start);
        return result;
    }
}
```



## 二、通知类型

| 通知类型        | 说明                                                         |
| --------------- | ------------------------------------------------------------ |
| @Around         | 环绕通知，此注解标注的通知方法在目标方法前、后都被执行       |
| @Before         | 前置通知，此注解标注的通知方法在目标方法前被执行             |
| @After          | 后置通知，此注解标注的通知方法在目标方法后被执行，无论是否有异常都会执行 |
| @AfterReturning | 返回后通知，此注解标注的通知方法在目标方法后被执行，有异常不会执行 |
| @AfterThrowing  | 异常后通知，此注解标注的通知方法发生异常后执行               |



### @Pointcut注解

**将公共的切入点表达式进行统一的抽取，示例：**

```java
// 语法：@Pointcut(切入点表达式)		----  也可以使用注解的切入点表达式
@Pointcut("execution(* com.itheima.service.impl.DeptServiceImpl.*(..))")
public void pt(){}

@Around("pt()")
public Object recordTime(ProceedingJoinPoint joinPoint) throws Throwable{}
```

**切入点表达式的修饰符：**

- private：仅能在当前切面类中引用该表达式
- public：在其它外部的切面类中也可以引用该表达式



## 三、通知顺序

- 不同切面类中，默认按照切面类的类名字母排序：
  - 目标方法前的通知方法：字母排名靠前的先执行
  - 目标方法后的通知方法：字母排名靠前的后执行
- 用 @Order(数字) 加载切面类上来控制顺序
  - 目标方法前的通知方法：数字小的先执行
  - 目标方法后的通知方法：数字小的后执行
- 同一个类中不同通知的执行顺序
  - 正常：Around——>Before——>AfterReturning——>After——>Around
  - 异常：Around——>Before——>AfterThrowing——>After

​	

## 四、切入点表达式

### （一）方法签名

- execution(访问修饰符? 返回值 包名.类名.?方法名(方法参数) throws 异常?)

- 其中带 ? 的表示可以省略的部分

  1. 访问修饰符：可省略（比如：public、protected）
  2. 包名.类名：可省略
  3. throws 异常：可省略（注意是方法上声明抛出的异常，不是实际抛出的异常）

- 星号(*)表示单个任意符号，点点(..)表示多个连续的任意符号

- 注意星号还可以用于方法名的拼接，例如“search*(..)”表示搜索以"search"开头的方法名

- 示例

  ```java
  @Before("execution(* com.itheima..DeptService.*(..))")
  ```



**书写建议：**

1. 所有的业务方法名在命名时尽量规范，方便切入点表达式快速匹配，如：findXxx, updateXxx。

2. 描述切入点方法通常基于接口描述，而不是直接描述实现类，增强拓展性。

3. 在满足业务需要的前提下，尽量缩小切入点的匹配范围。

   

### （二）注解

- 步骤1：定义一个注解

  ```java
  @Target(ElementType.METHOD)				//元注解，标识该注解只能定义在方法上
  @Retention(RetentionPolicy.RUNTIME)		//元注解，标识该注解保留到运行阶段
  public @interface LogOperation{}		//注意注解的关键字是 @interface
  ```

- 步骤2：使用@annotation切入点表达式

  ```java
  // 方式一：参数写切面注解的全类名
  @Before("@annotation(com.itheima.anno.LogOperation)")
  public void doBefore(JoinPoint joinPoint){方法体}
  
  // 方式二：参数写一个注解形参，通知方法里加上这个形参
  @Before("@annotation(anno)")
  public void doBefore(JoinPoint joinPoint, LogOperation anno){方法体}
  ```

  

## 五、连接点

### （一）JoinPoint 核心接口通用方法

| 方法名              | 功能说明                                                     |
| :------------------ | :----------------------------------------------------------- |
| **getArgs()**       | 返回被拦截方法的入参数组（`Object[]`类型），可用于获取、读取方法的入参值 |
| **getTarget()**     | 返回被代理的**原始目标对象**，即业务逻辑的真实实现类实例     |
| getThis()           | 返回 AOP 框架生成的**代理对象本身**，即当前执行的代理实例    |
| **getSignature()**  | 返回连接点的**方法签名对象（Signature）**，包含方法名、返回类型、所属类等核心元数据 |
| getKind()           | 返回连接点的类型，Spring AOP 中固定为`method-execution`（方法执行），AspectJ 中可返回方法调用、构造器执行等更多类型 |
| getStaticPart()     | 返回连接点的静态部分信息，包含连接点的固定元数据，与执行状态无关 |
| getSourceLocation() | 返回连接点的源代码位置信息，包含被拦截方法所在的文件名、行号等 |
| toShortString()     | 返回连接点的简短字符串描述，用于快速识别连接点               |
| toLongString()      | 返回连接点的完整字符串描述，包含全限定类名、方法名、参数类型等完整信息 |
| toString()          | 返回连接点的默认字符串描述，格式介于简短与完整描述之间       |



### （二）环绕通知专属 ProceedingJoinPoint 方法

| 方法名                 | 功能说明                                                     |
| :--------------------- | :----------------------------------------------------------- |
| **proceed()**          | 执行 AOP 切面链的下一个通知逻辑，若已到链尾则执行**原始目标方法**，返回目标方法的执行结果 |
| proceed(Object[] args) | 使用指定的入参数组，执行切面链的下一个通知逻辑或原始目标方法，可用于动态修改方法的入参值 |



### （三）方法签名 Signature 常用辅助方法

| 方法名                     | 功能说明                                                     |
| :------------------------- | :----------------------------------------------------------- |
| **getName()**              | 返回被拦截方法的**方法名**（如`saveUser`）                   |
| **getModifiers()**         | 返回方法的访问权限修饰符（int 类型），可通过`java.lang.reflect.Modifier`类解析为`public`/`private`等可读文本 |
| **getDeclaringType()**     | 返回方法所属类的**Class 对象**，可用于获取类的注解、泛型等更多信息 |
| **getDeclaringTypeName()** | 返回方法所属类的**全限定类名**（如`com.example.service.UserService`） |
| **toShortString()**        | 返回方法签名的简短字符串，仅包含类名、方法名                 |
| **toLongString()**         | 返回方法签名的完整字符串，包含全限定类名、方法名、参数类型、返回类型等完整信息 |



### （四）补充：AOP 连接点核心类型（getKind () 返回值）

| 类型常量              | 说明                                     | 支持框架            |
| :-------------------- | :--------------------------------------- | :------------------ |
| method-execution      | 方法执行连接点，拦截方法的执行过程       | Spring AOP、AspectJ |
| method-call           | 方法调用连接点，拦截方法的调用过程       | AspectJ             |
| constructor-execution | 构造器执行连接点，拦截对象构造器的执行   | AspectJ             |
| constructor-call      | 构造器调用连接点，拦截对象构造器的调用   | AspectJ             |
| field-get             | 字段读取连接点，拦截对象字段的读取操作   | AspectJ             |
| field-set             | 字段写入连接点，拦截对象字段的赋值操作   | AspectJ             |
| staticinitialization  | 静态初始化连接点，拦截类的静态代码块执行 | AspectJ             |
| exception-handler     | 异常处理连接点，拦截异常的捕获处理过程   | AspectJ             |



## 六、注意事项

- 自定义注解的关键字是@interface，上面要加上@Target和@Retention两个元注解。
- 自定义切面类需要加上@Component和@Aspect两个注解，前者让切面类被IOC容器管理，后者声明它是一个切面类。
- @Around环绕通知需要自己调用ProceedingJoinPoint.proceed()来让原始方法执行，其它通知不需要考虑目标方法执行。

- @Around环绕通知方法的返回值，**必须**指定为Object，来接收原始方法的返回值。

- 使用@Pointcut注解将公共的切入点表达式进行统一的抽取之后，在使用它时记得加上小括号“()”。 

- 对于@Around通知，获取连接点信息只能使用ProceedingJoinPoint。

- 对于其它四种通知，获取连接点信息只能使用JointPoint，它是ProceedingJoinPoint的父类型。

- 注意获取切入点的方法名不是靠getTarget().getClass().getMethod()，而是靠getSignature.getName，因为getTarget方法获得的字节码对象的方法，是需要往里面传参去执行的，而获取方法签名的方式可以直接获取切入点方法名。

- 注意如果要获取连接点的返回值，由于有些切入点的返回值是null，有的不是null，因此如果要返回存储，需要做一个判断：

  ```java
  String res = result == null ? "void" : result.toString();
  ```

## 相关笔记

- [[☕ Java笔记/Java笔记总览|Java笔记总览]]

- [[☕ Java笔记/日志笔记|日志配置]]
- [[☕ Java笔记/枚举反射注解|枚举反射注解]]

  

## 七、高级用法

### （一）切入点方法执行结束后，可以把方法的返回值放进注解里的jsonResult里面

```java
// 定义后置返回通知，在带有@Log注解的方法成功返回后触发
@AfterReturning(pointcut = "@annotation(controllerLog)", returning = "jsonResult")
// 定义后置返回处理方法，接收切点、日志注解和返回结果作为参数
public void doAfterReturning(JoinPoint joinPoint, Log controllerLog, Object jsonResult)
{
    // 调用统一的日志处理方法，传入切点、日志注解、空异常和返回结果
    handleLog(joinPoint, controllerLog, null, jsonResult);
}
```


### （二）定义异常后置通知，在带有@Log注解的方法抛出异常后触发

```java
@AfterThrowing(value = "@annotation(controllerLog)", throwing = "e")
// 定义异常处理方法，接收切点、日志注解和异常对象作为参数
public void doAfterThrowing(JoinPoint joinPoint, Log controllerLog, Exception e){
	// 调用统一的日志处理方法，传入切点、日志注解、异常对象和空返回结果
    handleLog(joinPoint, controllerLog, e, null);
}
```


   















