---
tags:
  - java进阶
date: 2026-06-04
---
# IO流

i： iput 输入（读取）

0：outpu输出 （写出）

介绍： 文件传输

读写配置文件 日志文件

​			客户端与服务端的通玄

​			文件上传下载

## IO流体系结构

### 字节流--万能流

#### FileInputStream

### 字节输出流

new FileInputStream（）创建对象 在这里加ture

.write 写入:

输出流写出数据之前，它会清空文件内容，重新写入

如果不想情况  后面要加ture

如果文件存在，则创建该文件，再写入

fos.close  释放资源

### 字节输入流

rend（）方法 读取文件里面的内容 一次返回一个字节

rend（数组）一次读一个字节数组数据，返回读到字节数组中的有效的字节个数

close（）释放资源



![image-20260410175200584](C:\Users\ALIENWARE\AppData\Roaming\Typora\typora-user-images\image-20260410175200584.png)

#### 异常处理

finally---只能与try。。。catch一同使用 一定会被执行的代码块

return 在finally里面就一定是返回 finally 的返回值,只有eixt

通常用于释放资源



### 字符流--只能操作纯文本文件

字符流=字节流+默认编码表（unicode码表）

字符流需要关流才能把数据写进文件，只有关流的时候才会把数据写进去

flush（）刷新，及时将缓存中发的数据写入文件，刷新之后，还能继续写出

flush（）释放资源 但是不能继续写出了

FileReader在

FileWriter

操作纯文本文件不会乱码

## Properties 集合

其实就是一个Map集合

内部存在两个方法,可以很方便的将集合中的键值对写入文件,也可以方便的从文件中读取

​			将来加载配置文件的时候很方便

### 构造器

Properties 集合()  创建一个没有默认值的空属性列表

### 方法

| Object setProperty(String  key, String value) | 添加(修改)一个键值对 |
| --------------------------------------------- | -------------------- |
| String getProperty(String  key)               | 根据键获取值         |
| Set<String> stringPropertyNames()             | 获取集合中所有的键   |

| Object setProperty(String  key, String value) | 添加(修改)一个键值对 |
| --------------------------------------------- | -------------------- |
|                                               |                      |

### **Properties** **和** **IO** **有关的方法**

| 方法                                           | 说明                                                         |
| ---------------------------------------------- | ------------------------------------------------------------ |
| void load(InputStream inStream)                | 从输入字节流读取属性列表（键和元素对）                       |
| void  load(Reader reader)                      | 从输入字符流读取属性列表（键和元素对）                       |
| void store(OutputStream out,  String comments) | 将此属性列表（键和元素对）写入此 Properties表中，以适合于使用 load(InputStream)方法的格式写入输出字节流 |
| void  store(Writer writer, String  comments)   | 将此属性列表（键和元素对）写入此 Properties表中，以适合使用 load(Reader)方法的格式写入输出字符流 |

## HuTool 

Hutool 是一个小而全的 Java 工具类库，通过静态方法封装，降低相关API的学习成本，提高工作效率

### 常用API

| IOUtil 类提供的部分方法展示                             | 说明               |
| ------------------------------------------------------- | ------------------ |
| copy(InputStream in, OutputStream out, int bufferSize)  | 字节流拷贝         |
| copy(Reader reader, Writer writer)                      | 字符流拷贝         |
| readLines(Reader reader, Collection<String> collection) | 按行读取内容到集合 |
| close(Closeable closeables)                             | 安全关闭流         |

| FileUtil 类提供的部分方法展示       | 说明                       |
| ----------------------------------- | -------------------------- |
| touch(filePath)                     | 创建文件（自动创建父目录） |
| mkdir(dirPath)                      | 创建目录（支持多级目录）   |
| copy(srcPath, destPath, isOverride) | 复制文件或目录（可选覆盖） |
| move(srcFile, destDir, isOverride)  | 移动文件或目录             |

## 正则表达式

就是一串用来校验字符串是否符合要求的规则

## 相关笔记

- [[☕ Java笔记/Java笔记总览|Java笔记总览]]


- [[MOC-Java基础]]
