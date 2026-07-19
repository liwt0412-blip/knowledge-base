---
tags:
  - spring
date: 2026-06-04
---
# SpringBoot原理

## 一、起步依赖原理

起步依赖的底层原理就是Maven中的依赖传递



## 二、自动配置原理

SpringBoot的自动配置就是当spring项目启动后，一些配置类、bean对象就自动存入到了IOC容器中，不需要我们手动去声明，从而简化了开发，省去了繁琐的配置操作。

示例：使用Gson对象将一个对象或集合转化为JSON格式的数据

1. 引入依赖

   ```xml
   <dependency>
   	<groupId>com.google</groupId>
       <artifactId>......</artifactId>
       <version>0.0.1-SNAPSHOT</version>
   </dependency>
   ```

2. 直接注入对象，使用里面的方法

   ```java
   public class GsonTest{
   	@Autowired
   	private Gson gson;
       @Test
       public void TestJson(){
           System.out.println(gson.toJson(Result.success("Hello Gson")));
       }
   }
   ```



### 方案一：手动指定扫描范围

**`@Component` + `@ComponentScan`**

`@SpringBootApplication` 这个注解具备组件扫描功能，但是默认扫描的是启动类所在包及其子包

可以通过添加`@ComponentScan`这个注解来声明要扫描的包，如果添加了要扫描的包，那么默认的扫描范围就会失效，示例：

```java
@ComponentScan(basePackages = {"com.example","com.itheima"})
@SpringBootApplication
public class SpringbootWebConfigApplication{
	public static void main(String[] args){
        SpringApplication.run(SpringbootWebConfigApplication.class, args);
    }
}
```



### 方案二：@Import注解导入

@Import导入的类会被Spring加载到IOC容器中，导入形式主要有以下几种：

1. 导入普通类

   ```java
   @Import(TokenParser.class)  //直接导入普通类，普通类上不需要声明@Component注解
   @SpringBootApplication
   ```

2. 导入配置类

   ```java
   @Import(HeaderConfig.class)  //导入配置类
   @SpringBootApplication
   ```

3. 导入ImportSelector接口实现类

   ```java
   public class MyimportSelector implements ImportSelector{
       public String[] selectImports(AnnotationMetadata importingClassMetadata){
           return new String[]{"com.example.HeaderConfig","com.example.TokenParser"};
       }
   }
   ```

   ```java
   @Import(MyImportSelector.class)  //ImportSelector实现类 - 批量导入
   @SpringBootApplication
   ```

4. 第三方开发者把需要注入的类写入ImportSelector实现类，然后将这个@import注解交给@EnableHeaderConfig注解

   ```java
   @Retention(RetentionPolicy.RUNTIME)
   @Target(ElementType.TYPE)
   @Import(MyImportSelector.class)
   public @interface EnableHeaderConfig{}
   ```

   ```java
   @EnableHeaderConfig
   @SpringBootApplication
   ```

   

## 三、源码跟踪

@SpringBootApplication注解底层封装了三个重要的注解

1. @SpringBootConfiguration注解。它的底层又封装了Configuration注解，说明SpringBootApplication启动类本身也是一个配置类，因此将配置信息写在启动类里面也是可以生效的。
2. @ComponentScan注解。说明项目在启动时会自动扫描当前包及其子包
3. @EnableBootConfiguration注解：SpringBoot实现自动化配置的核心注解
   1. @Import(AutoConfigurationImportSelector.class)
   2. 参数里的AutoConfigurationImportSelector间接实现了ImportSelector接口

⚪快速聚焦当前类所在的jar包

项目一启动，就会自动加载配置文件，然后加载配置文件里面的配置类，然后将配置类中所有的bean加载到IOC容器中。

注意：在低版本（2.7.0以前）的springboot中，自动配置类（XxxAutoConfiguration）是定义在spring.factories文件中



@ConditionOnMissingBean：会根据当前的环境信息决定是否有必要将当前的bean注册到IOC容器中，成为IOC容器的bean对象，只有符合对应的条件才会将bean注册到IOC容器中



## 四、自定义starter

场景：在实际开发中，经常会定义一些公共组件，提供给各个项目团队使用。而在SpringBoot的项目中，一般会将这些公共组件封装为SpringBoot的starter(包含了起步依赖和自动配置功能)。



### 1. 命名规范

- 如果是官方定义的starter，那么spring-boot在前，功能模块名称在后；
- 如果是第三方技术提供的，那么功能模块名称在前，spring-boot在后；



### 2. 操作步骤

需求：自定义aliyun-oss-spring-boot-starter，完成阿里云OSS操作工具类AliyunOSSOperator的自动配置。

目标：引入起步依赖之后，要想使用阿里云OSS，注入AliyunOSSOperator直接使用即可

步骤：

1. 创建aliyun-oss-spring-boot-starter模块
   1. aliyun-oss-spring-boot-starter模块创建好之后只需要保留pom.xml文件
2. 创建aliyun-oss-spring-boot-autoconfigure模块，在starter中引入该模块
   1. aliyun-oss-spring-boot-autoconfigure模块创建好之后只需要保留pom.xml和src文件
   2. src里面的启动类也可以删掉，因为这么模块创建出来是为了给其它模块使用的
3. 在aliyun-oss-spring-boot-autoconfigure模块中定义自动配置功能，并定义自动配置文件META-INF/spring/xxx.imports

## 相关笔记

- [[☕ Java笔记/Java笔记总览|Java笔记总览]]

- [[☕ Java笔记/Bean管理|Bean 管理]]
- [[💼 面试/本人面试准备/本人面试准备|面试准备]]
- [[💼 面试/框架面试题|框架面试]]











