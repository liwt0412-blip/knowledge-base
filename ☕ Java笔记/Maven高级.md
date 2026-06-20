---
tags:
  - maven
date: 2026-06-04
---
# Maven高级

## 分模块设计

将一个大项目拆分成若干个子模块，方便项目的管理维护、扩展，也方便模块间的相互引用，资源共享。



## 拆分策略

**策略一**：按照功能模块拆分，比如：公共组件、商品模块、搜索模块、购物车模块、订单模块等

**策略二**：按层拆分，比如：公共组件、实体类、控制层、业务层、数据访问层

**策略三**：按照功能模块 + 层拆分

**注意：分模块设计需要先针对模块功能进行设计，再进行编码。不会先将工程开发完毕，然后进行拆分。**



## Maven继承

**概念**：继承描述的是两个工程间的关系，与java中的继承相似，子工程可以继承父工程中的**配置信息**，常见于依赖关系的继承。

**作用**：简化依赖配置、统一管理依赖

**实现**：<parent>...</parent>

1. 创建maven模块tlias-parent，该工程为父工程，设置打包方式pom（默认为jar）。
2. 在子工程的pom.xml文件中，配置继承关系
3. 在父工程中配置各个工程共有的依赖（子工程会自动继承父工程的依赖）



#### 设置打包方式：packaging标签

| 打包方式 | 说明                                                        |
| -------- | ----------------------------------------------------------- |
| jar      | 普通模块打包，springboot项目基本都是jar包（内嵌tomcat运行） |
| war      | 普通web程序打包，需要部署在外部的tomcat服务器中运行         |
| pom      | 父工程或聚合工程，该模块不写代码，仅进行依赖管理            |



#### 配置父工程的pom.xml的相对路径：relativePath标签

自闭合表示默认，从本地仓库中查找依赖，如果本地仓库中没有依赖，则会从中央仓库下载依赖。示例：

```xml
<relativePath>../tlias-parent/pom.xml</relativePath>
```



#### 注意事项：

- 在子工程中，配置了继承关系之后，坐标中的groupId是可以省略的，因为会自动继承父工程的
- relativePath指定父工程的pom文件的相对位置（如果不指定，将从本地仓库/远程仓库查找）
- 若父子工程都配置了同一个版本的不同依赖，以子工程的为准



#### 以下两种形式运行的效果是一样的，实际结构关系只跟pom文件的设置有关

![image-20260529165830238](D:\softwares\Typora\TyporaImages\image-20260529165830238.png)



### 版本锁定

在maven中，可以在父工程的pom文件中通过<dependencyManagement>来统一管理版本



### 自定义属性

使用properties标签指定

```xml
<properties>
	<lombok.version>1.18.30</lombok.version>
</properties>

<dependencies>
	<dependency>
    	<groupId>org.projectlombok</groupId>
        <artifactId>lombok</artifactId>
        <version>${lombok.version}</version>
    </dependency>
</dependencies>
```



## Maven聚合

**解决的痛点**：分模块拆分后，模块与模块之间是有依赖关系的，在打包时十分繁琐

**聚合**：将多个模块组织成一个整体，同时进行项目的构建

**聚合工程**：一个不具有业务功能的“空”工程（有且仅有一个pom文件）

**作用**：快速构建项目（无需根据依赖关系手动构建，直接在聚合工程上构建即可）

**实现**：maven中可以通过`<modules>`设置当前聚合工程所包含的子模块名称

```xml
<modules>
	<module>../tlias-pojo</module>
    <module>../tlias-utils</module>
    <module>../tlias-web-management</module>
</modules>
```

**注意**：聚合工程中所包含的模块，在构建时，会自动根据模块间的依赖关系设置构建顺序，与聚合工程中模块的配置书写位置无关



#### 父工程和聚合工程虽然常常是同一个工程，但是表示的含义不同：

- 父工程的目的是依赖版本管理，解决依赖继承问题，相关标签是parent、packageing、properties、dependencies、dependencymanagement。
- 聚合工程的目的是打包时一键打包，打包时让maven自动地处理模块间的依赖关系，相关标签是modules。



#### maven中继承和聚合的联系与区别：

maven中的继承和聚合是相互独立的，我们可以只用继承不用聚合，也可以只用聚合不用继承。

**联系**：继承和聚合都属于设计型模块，打包方式都为pom，常将两种关系制作到同一个pom文件中

**区别**：

1. 继承用于简化依赖配置、统一管理依赖版本，是在子工程中配置继承关系
2. 聚合用于快速构建项目，是在聚合工程中配置聚合的模块



## 私服

私服是一种特殊的远程仓库，它是架设在局域网内的仓库服务，用来代理位于外部的中央仓库，用于解决团队内部的资源共享与资源同步问题。

依赖查找顺序：本地仓库——>私服——>中央仓库



### 资源上传与下载

| 私服仓库     | 说明                                                         |
| ------------ | ------------------------------------------------------------ |
| central仓库  | 中中央仓库下载的依赖                                         |
| release仓库  | 发行版本，功能趋于稳定、当前更新停止，可以用于发行的版本，存储在私服中的release仓库中 |
| snapshot仓库 | 快照版本，功能不稳定、尚处于开发中的版本，即快照版本，存储在私服的snapshot仓库中 |

- Install：安装到本地仓库
- deploy：上传到私服中



### 实现步骤

#### 步骤一：设置私服的访问用户名/密码（settings.xml中的servers中配置）

```xml
<server>
	<id>maven-releases</id>
    <username>admin</username>
    <password>admin</password>
</server>
<server>
	<id>maven-snapshots</id>
    <username>admin</username>
    <password>admin</password>
</server>
```



#### 步骤二：设置私服依赖下载的仓库组地址（在自己maven安装目录下的conf/settings.xml中的mirror中配置）（注意要将原来的阿里云私服注释掉）

```xml
<mirror>
	<id>maven-public</id>
    <mirrorOf>*</mirrorOf>
    <url>http://192.168.150.101.8081/repository/maven-public</url>
</mirror>
```



#### 步骤三：设置私服依赖下载的仓库组地址（在自己maven安装目录下的conf/settings.xml中的profiles中配置）

```xml
<profile>
	<id>allow-snapshots</id>
    <activation>
    	<activeByDefault>true</activeByDefault>
    </activation>
    <repository>
    	<id>maven-public</id>
        <url>http://localhost:8081/repository/maven-public/</url>
        <releases>
        	<enabled>true</enabled>
        </releases>
        <!--因为私服默认情况下只允许访问release版本的依赖，如果需要访问snapshot版本的依赖，那么需要加入这样一段配置-->
        <snapshots>
        	<enabled>true</enabled>
        </snapshots>
    </repository>
</profile>
```



#### 步骤四：IDEA的maven工程的pom文件中配置上传（发布）地址

```xml
<distributionManagement>
    <!--配置release版本的发布地址-->
	<repository>
    	<id>maven-releases</id>
        <url>http://192.168.150.101:8081/repository/maven-releases</url>
    </repository>
    <!--配置release版本的发布地址-->
    <snapshotRepository>
    	<id>maven-snapshots</id>
        <url>http://192.168.150.101:8081/repository/maven-snapshots</url>
    </snapshotRepository>
</distributionManagement>
```



#### 将本地依赖上传到私服：

双击deploy。maven会自动根据pom文件中是版本 release/snapshot上传到对应的仓库。



#### 将私服依赖引入到本地

直接在pom文件中引入依赖。

## 相关笔记

- [[☕ Java笔记/Java笔记总览|Java笔记总览]]


- [[MOC-Spring框架]]
