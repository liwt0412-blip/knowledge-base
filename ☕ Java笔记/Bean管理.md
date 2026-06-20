---
tags:
  - spring
date: 2026-06-04
---
# Bean管理

## bean作用域

作用域使用`@Scope`注解指定，例如：`@Scope("prototype")`

| 作用域      | 说明                                           |
| ----------- | ---------------------------------------------- |
| singleton   | 容器内同名称的bean只有一个实例（单例）（默认） |
| prototype   | 每次使用该bean时会创建新的实例（非单例/多例）  |
| request     | 每次请求范围内会创建新的实例（web环境中）      |
| session     | 每次会话范围内会创建新的实例（web环境中）      |
| application | 每个应用范围内会创建新的实例（web环境中）      |



## bean的创建时机

- 默认bean是单例，在项目启动时创建
- `@Lazy`可以延迟初始化，延迟到第一次使用的时候创建bean
- `@prototype`是多例创建，每使用一次就创建一次新的bean



## 获取IOC容器对象

直接注入ApplicationContext对象

```java
@scope("prototype")
public class SpringbootWeb{
    // 注入IOC容器对象，注意导包是springframework提供的包
    @Autowaired
	private ApplicationContext applicationcontext;
    // 获取DeptController的对象，注入的对象名默认是首字母小写
    Object deptController =  application.getBean("deptController");
}
```



## 第三方Bean

如果要管理的bean对象来自于第三方（不是自定义的），是无法使用`@Component`及衍生注解声明bean的，就需要用到`@Bean`注解。

若要管理的第三方bean对象，建议对这些bean进行集中分类配置，可以通过@Configuration注解声明一个配置类。

```java
@Configuration  //标识这个类为配置类，项目启动时会自动扫描这个类并执行里面的方法
public class CommonConfig{
    @Bean //将方法返回值交给IOC容器管理，成为IOC容器的bean对象
    public AliyunOssOperator aliyunOSSOperator(AliyunOssProperties ossproperties){
        return new AliyunOSSOperator(ossProperties);
    }
}
```

- 如果第三方bean需要依赖其它bean对象，直接在bean定义方法中设置形参即可，容器会根据类型自动装配。
- 通过@Bean注解的name或value属性可以声明bean的名称，如果不指定，默认bean的名称就是方法名。



## 自动配置-@Conditional

- 作用：按照一定的条件进行判断，在满足给定条件后才会注册对应的bean对象到Spring IOC容器中。
- 位置：方法、类
- @Conditional本身是一个父注解，派生大量的子注解：
  - @ConditionalOnClass(name = "全类名")：判断环境中是否有对应的字节码文件，才注册bean到IOC容器
  - @ConditionalOnMissingBean：判断环境中没有对应的bean（类型或名称），才注册bean到IOC容器
  - @ConditionalOnProperty(name="",havingValue="")：判断配置文件中有对应属性和值，才注册bean到IOC容器

## 相关笔记

- [[☕ Java笔记/Java笔记总览|Java笔记总览]]

- [[☕ Java笔记/SpringBoot原理|Spring Boot 原理]]











