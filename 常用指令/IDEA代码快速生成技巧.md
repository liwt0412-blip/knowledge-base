---
tags:
  - 工具
  - idea
date: 2026-06-04
---
# IDEA Java 代码快速生成技巧

利用IDEA 自带的**代码模板（Live Templates）**，输入缩写 + `Tab` 即可一键生成代码，高效实用。

## 一、打印输出（最常用）

| 缩写    | 生成代码                               | 作用                |
| :------ | :------------------------------------- | :------------------ |
| `sout`  | `System.out.println();`                | 普通换行打印        |
| `souf`  | `System.out.printf();`                 | 格式化打印          |
| `soutm` | `System.out.println("类名.方法名");`   | 打印当前类 + 方法名 |
| `soutp` | `System.out.println("参数名=参数值");` | 打印方法参数        |
| `soutv` | `System.out.println("变量名=变量值");` | 打印最近变量        |

## 二、定义变量 / 常量

表格

| 缩写   | 生成代码                      | 作用         |
| :----- | :---------------------------- | :----------- |
| `var`  | `类型 变量名 = 新值;`         | 快速定义变量 |
| `psf`  | `public static final `        | 公共静态常量 |
| `psfi` | `public static final int `    | 整型常量     |
| `psfs` | `public static final String ` | 字符串常量   |
| `arr`  | `类型[] 数组名 = new 类型[];` | 快速定义数组 |

## 三、方法 / 循环

表格

| 缩写            | 生成代码                                    | 作用          |
| :-------------- | :------------------------------------------ | :------------ |
| `main` / `psvm` | `public static void main(String[] args) {}` | 主方法入口    |
| `fori`          | `for (int i = 0; i < ; i++) {}`             | 普通 for 循环 |
| `iter`          | `for (类型 变量 : 集合) {}`                 | 增强 for 循环 |
| `ret`           | `return ;`                                  | 快速返回值    |

## 四、条件判断 / 异常

表格

| 缩写  | 生成代码                        | 作用             |
| :---- | :------------------------------ | :--------------- |
| `ifn` | `if (变量 == null) {}`          | 判断对象为空     |
| `inn` | `if (变量 != null) {}`          | 判断对象非空     |
| `try` | `try {} catch (Exception e) {}` | 异常捕获         |
| `twr` | `try (资源) {} catch () {}`     | 自动关闭资源 try |

## 五、常用一键生成快捷键

- 生成 

  ```
  getter/setter/构造方法/toString
  ```

  - Windows：`Alt + Insert`
  - Mac：`Cmd + N`

  

- 快速包裹代码（if、for、try 等）

  - Windows：`Ctrl + Alt + T`
  - Mac：`Cmd + Alt + T`

  

- 格式化代码

  - Windows：`Ctrl + Alt + L`
  - Mac：`Cmd + Opt + L`

  

## 六、自定义模板

路径：`File → Settings → Editor → Live Templates`

可自定义专属代码缩写模板。

## 相关笔记

- [[MOC-工具运维]]
