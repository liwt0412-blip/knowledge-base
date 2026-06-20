

---
tags:
  - 工具
date: 2026-06-04
---
# 第一步

安装nodejs

虽然Opengl官方文档不要求提前安装nodejs

但先把这一步做完可以避开很多坑

首先来到nodejs的官方下载页面https://nodejs.org/en/download

点击Windows安装程序按钮

下载完成后打开安装包

如果出现弹窗问是否允许此应用对你的设备进行更改点击是

在安装窗口里首先勾选用户同意协议

.然后点next.

下一步.,

安装位置可以保持默认你也可以进行更改

接下来我们可以一路无脑点next

然后点击install开始安装

这里我们要稍微等待片刻

完成后点击finish按钮

nodejs就安装好了

# 第二步

安装Git

Git并不是必备安装项,但很多人后面遇到的一些报错,本质上都和Git配置有关,所以也可以提前避坑

来到Git的官方下载页面https://git-scm.com/install/windows,

根据你的电脑架构,选择对应的下载链接

比如我这台电脑是Windows X64  所以点这个

下载完成后点开安装包 点击next ,这里同样安装位置可以保持默认,你也可以进行更改

再往后,如果你不是专业开发者,不用纠结这些设置,我们可以一路无脑点next

终于到了最后一个选项,点击install开始安装,等待一小会,安装完成后

我们可以把这个view release notes取消勾选,它会打开git更新说明的网页

对安装没有影响,然后我们点击finish,git的安装就搞定了

# 第三步

安装openclaw

在菜单栏搜索Powershell，这里注意要选择以管理员身份运行，然后会打开一个大黑窗口

先输入：Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

我们要先输入一下这个命令 iwr -useb https://openclaw.ai/install.ps1 | iex

并回车执行，这个命令可能会运行一段时间，如果中途出现弹窗问是否允许

公共网络和专业网络访问此应用

点击允许

当你看到一句来自Opencore的欢迎信息

就说明Opencore已经安装成功了

不过这还没完

# 第四步 

配置openclaw

Openclaw会展示一段话提醒你使用它可能存在风险

问是否继续

这里可以按键盘上的左方向键选择yes

然后回车确认

接下来保持默认的quick start模式

继续回车

下一步需要选择Openclaw

背后的大模型服务商

比如Openai  Anthropic等等

在这里呢

可以根据个人偏好进行选择

用键盘的上下方向键进行切换

如果你已经创建过某个服务商的API密钥

可以直接使用

那我呢，会选择Kimi大模型，不是广告，主要是便宜

也教你如何创建大模型API密钥

以Kimi模型为例子

来到他们开放平台的控制台

左侧有个API key管理

我们点击新建API key按钮

给这个密钥取个名字

下面选择项目

然后点击确定

就可以看到啊创建出的密钥的值

密钥一定要进行保密，被别人拿去用的话，烧的就是你的额度了

然后先别着急点确定，先点旁边的复制按钮，然后回到power shell

然后回到power shell，因为我是在deepseek国内官网创建的密钥

所以这里选择点cn的API密钥类型

回车

接下来问，用什么方式提供密钥，选择现在复制密钥值

回车

接下来把之前复制的粘贴到这里来

回车后呢

要选择具体的模型

我就保持默认的Kimi K2.5

再接下来

我们要选择通讯渠道

我们目前可以一路点向下键

也就是先跳过

因为呢，涉及到一些准备步骤，后面我们再来进行配置

然后问要不要现在配置skills，也就是小龙虾掌握的技能

如果你有比较清晰的目的啊，这里可以看看有没有需要配置的

每个技能后面的括号里啊，都写出来应用的场景，那这个呢

也可以留到后面进行配置

我们按空格选择SKIP for now

然后回车

接下来会出现一系列问题

问我们要不要配置好

各种服务的API密钥

也可以先都选择no

回头有需要再进行填写

下一步问我们要不要启用hook

我们目前也可以先跳过

空格选择skip for now

然后回车

接下来程序会启用网关

我们会看到有个命令

窗口被自动打开了

这个窗口先不要去关它

等待一段时间回到之前的Powershell窗口

它问我们想用什么方式启动小龙虾

我们可以选用Web UI

网页图形界面会更加，直观和操作友好一些

回车后会出现提示说，有网页自动被打开，选择允许

会进入到这个127.0.0.1这个网页，在聊天界面我们就可以开始和自己的小龙虾对话了

如果你能收到来自小龙虾的回复

撒花

但小龙虾之所以出圈，其中一个原因是它，可以接入各种通讯软件，接入后

我们只需要在手机上发一条消息，它就能在电脑上自动开始干活，

所以我们接下来要做的是，把Openclaw和飞书连接起来

# 第五步

创建飞书机器人

来到飞书开放平台

点击右上角登录

如果没有账号，可以注册一个个人账号，需要加入任何企业

登录完成后，点击开发者后台，然后点击创建企业自建应用

给应用起一个名字，填写对应的描述，图标也可以自定义，然后点右下角的创建按钮

接下来我们点击添加机器人能力，然后通过左侧菜单栏来到权限管理



点开通权限,把里面代码删除，输入神秘代码：

{  "scopes": {    "tenant": [      "aily:file:read",      "aily:file:write",      "application:application.app_message_stats.overview:readonly",      "application:application:self_manage",      "application:bot.menu:write",      "cardkit:card:write",      "contact:contact.base:readonly",      "contact:user.employee_id:readonly",      "corehr:file:download",      "docs:document.content:read",      "event:ip_list",      "im:chat",      "im:chat.access_event.bot_p2p_chat:read",      "im:chat.members:bot_access",      "im:message",      "im:message.group_at_msg:readonly",      "im:message.group_msg",      "im:message.p2p_msg:readonly",      "im:message:readonly",      "im:message:send_as_bot",      "im:resource",      "sheets:spreadsheet",      "wiki:wiki:readonly"    ],    "user": ["aily:file:read", "aily:file:write", "im:chat.access_event.bot_p2p_chat:read"]  } }，点击确认开通权限，

上面有提醒我们，应用发布后，当前的修改才会生效

所以我们可以先点创建版本，然后在这个界面输入版本号

比如1.0.0  以及对应的更新说明    接下来点击保存并确认发布

现在我们的飞书机器人就创建好了

但还需要把它和Openclaw接通

# 第六步

连接Openclaw和飞书

回到Powershell

我们输入一个命令  Openclaw config

再次进行配置 

第一个问题选择第一个

也就是在本机运行

然后我们要选择配置channels，也就是通讯渠道

接下来回车选择configure link 用来添加新的消息渠道

这里一路向下 找到飞书后回车

要在飞书上运行   需要先安装飞书渠道插件

所以这里回车选择通过NPM安装 

等待一会  安装完成后 我们要输入飞书应用的APP secret

这个在飞书的开发者后台啊   就能获取 我们先按回车

然后来到飞书开发者  后台的凭证与基础信息 

复制这个APP secret

然后把值粘贴到power shell

接下来还要输入APP ID

也是一样的流程

复制然后粘贴进来

再然后我们要选择飞书

和open call的通信方式  默认的Websocket是实时通信模式

配置起来简单

所以回车选择

我们的机器人应用啊

是在国内版飞书

也就是飞书点cn这个域名创建的

所以选China这个

接下来问我们是否允许，在群聊里使用机器人

这里可以选择open，也就是在所有群里都可以用机器人

但必须@机器人

下一步我们选择finished

表示完成配置

然后这一步问要不要

现在配置私聊访问策略

我们选择yes

然后如果只是自己测试用啊

策略可以先选open

如果是正式环境

建议选择paran

然后回车

选择最后的continue

这样我们就完成了，飞书通讯渠道的配置

接下来在Powershell输入 openclaw- Gateway启用网关

然后在飞书的自建应用界面

点击左侧菜单的事件与回调

编辑订阅方式，选择为长链接，保存

然后添加事件 ，输入神秘代码---im.message.receive_v

要让这些保存生效

我们要再次发布版本

点击创建版本

输入新的版本号以及对应的更新说明

这次啊

我们是在给机器人添加消息接收能力

其余保持默认

点击保存并确认发布

# 第七步

测试对话

飞书机器人的配置啊

到目前就完成了

虽然过程很漫长和琐碎

但现在我们就可以尝试在，飞书上和小龙虾对话了，

如果想让它变得更强，也可以给它配置更多的skills，扩展它能完成的任务

但建议啊，只安装官方或可信来源的skills，避免带来安全风险

## 相关笔记

- [[MOC-工具运维]]
