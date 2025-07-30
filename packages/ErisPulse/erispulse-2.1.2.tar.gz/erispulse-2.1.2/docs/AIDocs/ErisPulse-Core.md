# ErisPulse 核心功能文档

本文件由多个开发文档合并而成，用于辅助 AI 理解 ErisPulse 的相关功能。

## 各文件对应内容说明

| 文件名 | 作用 |
|--------|------|
| quick-start.md | 快速开始指南 |
| UseCore.md | 核心功能使用说明 |
| PlatformFeatures.md | 平台功能说明 |

## 合并内容开始

<!-- quick-start.md -->

# 快速开始

## 安装ErisPulse

### 使用 pip 安装
```bash
pip install ErisPulse
```

### 更先进的安装方法
> 我们全面采用 [`uv`](https://github.com/astral-sh/uv) 作为 Python 工具链, 所以需要先安装 uv。

### 1. 安装 uv

#### 通用方法 (pip):
```bash
pip install uv
```

#### macOS/Linux:
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

#### Windows (PowerShell):
```powershell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

验证安装:
```bash
uv --version
```

### 2. 创建虚拟环境,并安装 ErisPulse

```bash
uv python install 3.12              # 安装 Python 3.12
uv venv                             # 创建虚拟环境
source .venv/bin/activate           # 激活环境 (Windows: .venv\Scripts\activate)
uv pip install ErisPulse --upgrade  # 安装框架
```

---

## 初始化项目

1. 创建项目目录并进入：

```bash
mkdir my_bot && cd my_bot
```

2. 初始化 SDK 并生成配置文件：

```bsah
epsdk init
# 或 ep-init
```

这将在当前目录下自动生成 `env.py` 配置模板文件, 以及最简程序入口 `main.py`。

---

## 安装模块

你可以通过 CLI 安装所需模块：

```bash
epsdk install Yunhu OneBot AIChat
```

你也可以手动编写模块逻辑，参考开发者文档进行模块开发。

---

## 运行你的机器人
运行我们自动生成的程序入口：
```bash
epsdk run main.py
```

或者使用热重载模式（开发时推荐）：

```bash
epsdk run main.py --reload
```


<!--- End of quick-start.md -->

<!-- UseCore.md -->

# ErisPulse 核心模块使用指南

## 核心模块
| 名称 | 用途 |
|------|------|
| `sdk` | SDK对象 |
| `env`/`sdk.env` | 获取/设置全局配置 |
| `mods`/`sdk.mods` | 模块管理器 |
| `adapter`/`sdk.adapter` | 适配器管理/获取实例 |
| `logger`/`sdk.logger` | 日志记录器 |
| `raiserr`/`sdk.raiserr` | 错误管理器 |
| `util`/`sdk.util` | 工具函数（缓存、重试等） |
| `BaseAdapter`/`sdk.BaseAdapter` | 适配器基类 |

```python
# 直接导入方式
from ErisPulse.Core import env, mods, logger, raiserr, util, adapter, BaseAdapter

# 通过SDK对象方式
from ErisPulse import sdk
sdk.env  # 等同于直接导入的env
```

## 模块系统架构
- 所有模块通过`sdk`对象统一管理
- 模块间可通过`sdk.<ModuleName>`互相调用
- 模块基础结构示例：
```python
from ErisPulse import sdk

class MyModule:
    def __init__(self):
        self.sdk = sdk
        self.logger = sdk.logger
        
    def hello(self):
        self.logger.info("hello world")
        return "hello world"
```

## 适配器使用
- 适配器是ErisPulse的核心，负责与平台进行交互

适配器事件分为两类：
- 标准事件：平台转换为的标准事件，其格式为标准的 OneBot12 事件格式 | 需要判断接收到的消息的 `platform` 字段，来确定消息来自哪个平台
- 原生事件：平台原生事件 通过 sdk.adapter.<Adapter>.on() 监听对应平台的原生事件
适配器标准事件的拓展以及支持的消息发送类型，请参考 [PlatformFeatures.md](docs/PlatformFeatures.md)

建议使用标准事件进行事件的处理，适配器会自动将原生事件转换为标准事件

```python
# 启动适配器
await sdk.adapter.startup("MyAdapter")  # 不指定名称则启动所有适配器

# 监听底层的标准事件
@adapter.on("message")
async def on_message(data):
    platform = data.get("platform")
    detail_type = "user" if data.get("detail_type") == "private" else "group"
    detail_id = data.get("user_id") if detail_type == "user" else data.get("group_id")
    
    if hasattr(adapter, platform):
        await getattr(adapter, platform).To(detail_type, detail_id).Text(data.get("alt_message"))
```

## 核心模块功能详解

### 1. 日志模块(logger)
```python
logger.set_module_level("MyModule", "DEBUG")  # 设置模块日志级别
logger.save_logs("log.txt")  # 保存日志到文件

# 日志级别
logger.debug("调试信息")
logger.info("运行状态")
logger.warning("警告信息")
logger.error("错误信息")
logger.critical("致命错误")  # 会触发程序崩溃
```

### 2. 环境配置(env)
```python
# 数据库配置操作
env.set("key", "value")  # 设置配置项
value = env.get("key", "default")  # 获取配置项
env.delete("key")  # 删除配置项

# 事务操作
with env.transaction():
    env.set('important_key', 'value')
    env.delete('temp_key')  # 异常时自动回滚

# 模块配置操作（读写config.toml）
module_config = env.getConfig("MyModule")  # 获取模块配置
if module_config is None:
    env.setConfig("MyModule", {"MyKey": "MyValue"})  # 设置默认配置
```

### 3. 错误管理(raiserr)
```python
# 注册自定义错误
raiserr.register("MyCustomError", doc="自定义错误说明")

# 获取错误信息
error_info = raiserr.info("MyCustomError")

# 抛出错误
raiserr.MyCustomError("错误描述")
```

### 4. 工具函数(util)
```python
# 自动重试
@util.retry(max_attempts=3, delay=1)
async def unreliable_function():
    ...

# 结果缓存
@util.cache
def expensive_operation(param):
    ...

# 异步执行
@util.run_in_executor
def sync_task():
    ...

# 同步调用异步
util.ExecAsync(sync_task)
```

## 建议
1. 模块配置应使用`getConfig/setConfig`操作config.toml
2. 持久信息存储使用`get/set`操作数据库
3. 关键操作使用事务保证原子性
> 其中，1-2 步骤可以实现配合，比如硬配置让用户设置后，和数据库中的配置进行合并，实现配置的动态更新

更多详细信息请参考[API文档](docs/api/)

<!--- End of UseCore.md -->

<!-- PlatformFeatures.md -->

# ErisPulse PlatformFeatures 文档
> 基线协议：(OneBot12)[https://12.onebot.dev/] 
> 
> 本文档为**快速使用指南**，包含：
> - 各适配器支持的Send方法链式调用示例
> - 平台特有的事件/消息格式说明
> 
> 正式适配器开发请参考：
> - [适配器开发指南](docs/Development/Adapter.md)
> - [事件转换标准](docs/AdapterStandards/event-conversion.md)  
> - [API响应规范](docs/AdapterStandards/api-response.md)

---

## 标准格式
为方便参考，这里给出了简单的事件格式，如果需要详细信息，请参考上方的链接。

### 标准事件格式
所有适配器必须实现的事件转换格式：
```json
{
  "id": "event_123",
  "time": 1752241220,
  "type": "message",
  "detail_type": "group",
  "platform": "yunhu",
  "self": {"platform": "yunhu", "user_id": "bot_123"},
  "message_id": "msg_abc",
  "message": [
    {"type": "text", "data": {"text": "你好"}}
  ],
  "alt_message": "你好",
  "user_id": "user_456",
  "user_nickname": "YingXinche",
  "group_id": "group_789"
}
```

### 标准响应格式
#### 消息发送成功
```json
{
  "status": "ok",
  "retcode": 0,
  "data": {
    "message_id": "1234",
    "time": 1632847927.599013
  },
  "message_id": "1234",
  "message": "",
  "echo": "1234",
  "{platform}_raw": {...}
}
```

#### 消息发送失败
```json
{
  "status": "failed",
  "retcode": 10003,
  "data": null,
  "message_id": "",
  "message": "缺少必要参数",
  "echo": "1234",
  "{platform}_raw": {...}
}
```

---

### 1. YunhuAdapter
YunhuAdapter 是基于云湖协议构建的适配器，整合了所有云湖功能模块，提供统一的事件处理和消息操作接口。

#### 支持的消息发送类型
所有发送方法均通过链式语法实现，例如：
```python
from ErisPulse.Core import adapter
yunhu = adapter.get("yunhu")

await yunhu.Send.To("user", user_id).Text("Hello World!")
```

支持的发送类型包括：
- `.Text(text: str, buttons: List = None)`：发送纯文本消息，可选添加按钮。
- `.Html(html: str, buttons: List = None)`：发送HTML格式消息。
- `.Markdown(markdown: str, buttons: List = None)`：发送Markdown格式消息。
- `.Image(file: bytes, buttons: List = None)`：发送图片消息。
- `.Video(file: bytes, buttons: List = None)`：发送视频消息。
- `.File(file: bytes, buttons: List = None)`：发送文件消息。
- `.Batch(target_ids: List[str], message: str)`：批量发送消息。
- `.Edit(msg_id: str, text: str)`：编辑已有消息。
- `.Recall(msg_id: str)`：撤回消息。
- `.Board(board_type: str, content: str, **kwargs)`：发布公告看板。
- `.Stream(content_type: str, generator: AsyncGenerator)`：发送流式消息。

Borard board_type 支持以下类型：
- `local`：指定用户看板
- `global`：全局看板

##### 按钮参数说明
`buttons` 参数是一个嵌套列表，表示按钮的布局和功能。每个按钮对象包含以下字段：

| 字段         | 类型   | 是否必填 | 说明                                                                 |
|--------------|--------|----------|----------------------------------------------------------------------|
| `text`       | string | 是       | 按钮上的文字                                                         |
| `actionType` | int    | 是       | 动作类型：<br>`1`: 跳转 URL<br>`2`: 复制<br>`3`: 点击汇报            |
| `url`        | string | 否       | 当 `actionType=1` 时使用，表示跳转的目标 URL                         |
| `value`      | string | 否       | 当 `actionType=2` 时，该值会复制到剪贴板<br>当 `actionType=3` 时，该值会发送给订阅端 |

示例：
```python
buttons = [
    [
        {"text": "复制", "actionType": 2, "value": "xxxx"},
        {"text": "点击跳转", "actionType": 1, "url": "http://www.baidu.com"},
        {"text": "汇报事件", "actionType": 3, "value", "xxxxx"}
    ]
]
await yunhu.Send.To("user", user_id).Text("带按钮的消息", buttons=buttons)
```
> **注意：**
> - 只有用户点击了**按钮汇报事件**的按钮才会收到推送，**复制***和**跳转URL**均无法收到推送。

#### OneBot12协议转换说明
云湖事件转换到OneBot12协议，其中标准字段完全遵守OneBot12协议，但存在一些差异，你需要阅读以下内容：
需要 platform=="yunhu" 检测再使用本平台特性

##### 核心差异点
1. 特有事件类型：
    - 表单（如表单指令）：yunhu_form
    - 按钮点击：yunhu_button_click
    - 机器人设置：yunhu_bot_setting
    - 快捷菜单：yunhu_shortcut_menu
2. 扩展字段：
    - 所有特有字段均以yunhu_前缀标识
    - 保留原始数据在yunhu_raw字段
    - 私聊中self.user_id表示机器人ID

3. 特殊字段示例：
```python
# 表单命令
{
  "type": "yunhu_form",
  "data": {
    "id": "1766",
    "name": "123123",
    "fields": [
      {
        "id": "abgapt",
        "type": "textarea",
        "value": ""
      },
      {
        "id": "mnabyo", 
        "type": "select",
        "value": ""
      }
    ]
  },
  "yunhu_command": {
    "name": "123123",
    "id": "1766",
    "form": {
      "abgapt": {
        "id": "abgapt",
        "type": "textarea",
        "value": ""
      },
      "mnabyo": {
        "id": "mnabyo",
        "type": "select",
        "value": ""
      }
    }
  }
}

# 按钮事件
{
  "detail_type": "yunhu_button_click",
  "yunhu_button": {
    "id": "",
    "value": "test_button_value"
  }
}

# 机器人设置
{
  "detail_type": "yunhu_bot_setting",
  "yunhu_setting": {
    "lokola": {
      "id": "lokola",
      "type": "radio",
      "value": ""
    },
    "ngcezg": {
      "id": "ngcezg",
      "type": "input",
      "value": null
    }
  }
}

# 快捷菜单
{
  "detail_type": "yunhu_shortcut_menu", 
  "yunhu_menu": {
    "id": "B4X00M5B",
    "type": 1,
    "action": 1
  }
}
```

---

### 2. TelegramAdapter
TelegramAdapter 是基于 Telegram Bot API 构建的适配器，支持多种消息类型和事件处理。

#### 支持的消息发送类型
所有发送方法均通过链式语法实现，例如：
```python
from ErisPulse.Core import adapter
telegram = adapter.get("telegram")

await telegram.Send.To("user", user_id).Text("Hello World!")
```

支持的发送类型包括：
- `.Text(text: str)`：发送纯文本消息。
- `.Image(file: bytes, caption: str = "")`：发送图片消息。
- `.Video(file: bytes, caption: str = "")`：发送视频消息。
- `.Audio(file: bytes, caption: str = "")`：发送音频消息。
- `.Document(file: bytes, caption: str = "")`：发送文件消息。
- `.EditMessageText(message_id: int, text: str)`：编辑已有消息。
- `.DeleteMessage(message_id: int)`：删除指定消息。
- `.GetChat()`：获取聊天信息。

#### env.py 配置示例
```python
sdk.env.set("TelegramAdapter", {
    # 必填：Telegram Bot Token
    "token": "YOUR_BOT_TOKEN",

    # Webhook 模式下的服务配置（如使用 webhook）
    "server": {
        "host": "127.0.0.1",            # 推荐监听本地，防止外网直连
        "port": 8443,                   # 监听端口
        "path": "/telegram/webhook"     # Webhook 路径
    },
    "webhook": {
        "host": "example.com",          # Telegram API 监听地址（外部地址）
        "port": 8443,                   # 监听端口
        "path": "/telegram/webhook"     # Webhook 路径
    }

    # 启动模式: webhook 或 polling
    "mode": "webhook",

    # 可选：代理配置（用于连接 Telegram API）
    "proxy": {
        "host": "127.0.0.1",
        "port": 1080,
        "type": "socks5"  # 支持 socks4 / socks5
    }
})
```

#### 数据格式示例
> 略: 使用你了解的 TG 事件数据格式即可,这里不进行演示

#### OneBot12协议转换说明
Telegram事件转换到OneBot12协议，其中标准字段完全遵守OneBot12协议，但存在以下差异：

##### 核心差异点
1. 特有事件类型：
   - 内联查询：telegram_inline_query
   - 回调查询：telegram_callback_query
   - 投票事件：telegram_poll
   - 投票答案：telegram_poll_answer

2. 扩展字段：
   - 所有特有字段均以telegram_前缀标识
   - 保留原始数据在telegram_raw字段
   - 频道消息使用detail_type="channel"

3. 特殊字段示例：
```python
# 回调查询事件
{
  "type": "notice",
  "detail_type": "telegram_callback_query",
  "user_id": "123456",
  "user_nickname": "YingXinche",
  "telegram_callback": {
    "id": "cb_123",
    "data": "callback_data",
    "message_id": "msg_456"
  }
}

# 内联查询事件
{
  "type": "notice",
  "detail_type": "telegram_inline_query",
  "user_id": "789012",
  "user_nickname": "YingXinche",
  "telegram_inline": {
    "id": "iq_789",
    "query": "search_text",
    "offset": "0"
  }
}

# 频道消息
{
  "type": "message",
  "detail_type": "channel",
  "message_id": "msg_345",
  "channel_id": "channel_123",
  "telegram_channel": {
    "title": "News Channel",
    "username": "news_official"
  }
}
```

---

### 3. OneBot11Adapter
OneBot11Adapter 是基于 OneBot V11 协议构建的适配器。

#### 支持的消息发送类型
所有发送方法均通过链式语法实现，例如：
```python
from ErisPulse.Core import adapter
onebot = adapter.get("onebot11")

await onebot.Send.To("group", group_id).Text("Hello World!")
```

支持的发送类型包括：
- `.Text(text: str)`：发送纯文本消息。
- `.Image(file: str)`：发送图片消息（支持 URL 或 Base64）。
- `.Voice(file: str)`：发送语音消息。
- `.Video(file: str)`：发送视频消息。
- `.Raw(message_list: List[Dict])`：发送原生 OneBot 消息结构。
- `.Recall(message_id: int)`：撤回消息。
- `.Edit(message_id: int, new_text: str)`：编辑消息。
- `.Batch(target_ids: List[str], text: str)`：批量发送消息。


#### 数据格式示例
> 略: 使用你了解的 OneBot v11 事件数据格式即可,这里不进行演示
#### OneBot12协议转换说明
OneBot11事件转换到OneBot12协议，其中标准字段完全遵守OneBot12协议，但存在以下差异：

##### 核心差异点
1. 特有事件类型：
   - CQ码扩展事件：onebot11_cq_{type}
   - 荣誉变更事件：onebot11_honor
   - 戳一戳事件：onebot11_poke

2. 扩展字段：
   - 所有特有字段均以onebot11_前缀标识
   - 保留原始CQ码消息在onebot11_raw_message字段
   - 保留原始事件数据在onebot11_raw字段

3. 特殊字段示例：
```python
# 荣誉变更事件
{
  "type": "notice",
  "detail_type": "onebot11_honor",
  "group_id": "123456",
  "user_id": "789012",
  "onebot11_honor_type": "talkative",
  "onebot11_operation": "set"
}

# 戳一戳事件
{
  "type": "notice",
  "detail_type": "onebot11_poke",
  "group_id": "123456",
  "user_id": "789012",
  "target_id": "345678",
  "onebot11_poke_type": "normal"
}

# CQ码消息段
{
  "type": "message",
  "message": [
    {
      "type": "onebot11_face",
      "data": {"id": "123"}
    },
    {
      "type": "onebot11_shake",
      "data": {} 
    }
  ]
}
```

---

## 参考链接
ErisPulse 项目：
- [主库](https://github.com/ErisPulse/ErisPulse/)
- [ErisPulse Yunhu 适配器库](https://github.com/ErisPulse/ErisPulse-YunhuAdapter)
- [ErisPulse Telegram 适配器库](https://github.com/ErisPulse/ErisPulse-TelegramAdapter)
- [ErisPulse OneBot 适配器库](https://github.com/ErisPulse/ErisPulse-OneBotAdapter)

相关官方文档：
- [OneBot V11 协议文档](https://github.com/botuniverse/onebot-11)
- [Telegram Bot API 官方文档](https://core.telegram.org/bots/api)
- [云湖官方文档](https://www.yhchat.com/document/1-3)

---

## 参与贡献

我们欢迎更多开发者参与编写和维护适配器文档！请按照以下步骤提交贡献：
1. Fork [ErisPuls](https://github.com/ErisPulse/ErisPulse) 仓库。
2. 在 `docs/` 目录下找到 ADAPTER.md 适配器文档。
3. 提交 Pull Request，并附上详细的描述。

感谢您的支持！

<!--- End of PlatformFeatures.md -->

<!-- API文档 -->

# API参考

## adapter.md

# 📦 `ErisPulse.Core.adapter` 模块

*自动生成于 2025-07-17 16:39:14*

---

## 模块概述

ErisPulse 适配器系统

提供平台适配器基类、消息发送DSL和适配器管理功能。支持多平台消息处理、事件驱动和生命周期管理。

💡 **提示**：

1. 适配器必须继承BaseAdapter并实现必要方法
2. 使用SendDSL实现链式调用风格的消息发送接口
3. 适配器管理器支持多平台适配器的注册和生命周期管理
4. 支持OneBot12协议的事件处理

---

## 🏛️ 类

### `SendDSLBase`

消息发送DSL基类

用于实现 Send.To(...).Func(...) 风格的链式调用接口

💡 **提示**：

1. 子类应实现具体的消息发送方法(如Text, Image等)
2. 通过__getattr__实现动态方法调用


#### 🧰 方法

##### `__init__`

初始化DSL发送器

:param adapter: 所属适配器实例
:param target_type: 目标类型(可选)
:param target_id: 目标ID(可选)
:param _account_id: 发送账号(可选)

---

##### `To`

设置消息目标

:param target_type: 目标类型(可选)
:param target_id: 目标ID(可选)
:return: SendDSL实例

:example:
>>> adapter.Send.To("user", "123").Text("Hello")
>>> adapter.Send.To("123").Text("Hello")  # 简化形式

---

##### `Using`

设置发送账号

:param _account_id: 发送账号
:return: SendDSL实例

:example:
>>> adapter.Send.Using("bot1").To("123").Text("Hello")
>>> adapter.Send.To("123").Using("bot1").Text("Hello")  # 支持乱序

---

### `BaseAdapter`

适配器基类

提供与外部平台交互的标准接口，子类必须实现必要方法

💡 **提示**：

1. 必须实现call_api, start和shutdown方法
2. 可以自定义Send类实现平台特定的消息发送逻辑
3. 通过on装饰器注册事件处理器
4. 支持OneBot12协议的事件处理


#### 🧰 方法

##### `__init__`

初始化适配器

---

##### `on`

适配器事件监听装饰器

:param event_type: 事件类型
:return: 装饰器函数

---

##### `middleware`

添加中间件处理器

:param func: 中间件函数
:return: 中间件函数

:example:
>>> @adapter.middleware
>>> async def log_middleware(data):
>>>     print(f"处理数据: {data}")
>>>     return data

---

##### 🔹 `async` `call_api`

调用平台API的抽象方法

:param endpoint: API端点
:param params: API参数
:return: API调用结果
⚠️ **可能抛出**: `NotImplementedError` - 必须由子类实现

---

##### 🔹 `async` `start`

启动适配器的抽象方法

⚠️ **可能抛出**: `NotImplementedError` - 必须由子类实现

---

##### 🔹 `async` `shutdown`

关闭适配器的抽象方法

⚠️ **可能抛出**: `NotImplementedError` - 必须由子类实现

---

##### 🔹 `async` `emit`

触发原生协议事件

:param event_type: 事件类型
:param data: 事件数据

:example:
>>> await adapter.emit("message", {"text": "Hello"})

---

##### 🔹 `async` `send`

发送消息的便捷方法

:param target_type: 目标类型
:param target_id: 目标ID
:param message: 消息内容
:param kwargs: 其他参数
    - method: 发送方法名(默认为"Text")
:return: 发送结果

⚠️ **可能抛出**: `AttributeError` - 当发送方法不存在时抛出
    
:example:
>>> await adapter.send("user", "123", "Hello")
>>> await adapter.send("group", "456", "Hello", method="Markdown")

---

### `AdapterManager`

适配器管理器

管理多个平台适配器的注册、启动和关闭

💡 **提示**：

1. 通过register方法注册适配器
2. 通过startup方法启动适配器
3. 通过shutdown方法关闭所有适配器
4. 通过on装饰器注册OneBot12协议事件处理器


#### 🧰 方法

##### `Adapter`

获取BaseAdapter类，用于访问原始事件监听

:return: BaseAdapter类

:example:
>>> @sdk.adapter.Adapter.on("raw_event")
>>> async def handle_raw(data):
>>>     print("收到原始事件:", data)

---

##### `on`

OneBot12协议事件监听装饰器

:param event_type: OneBot12事件类型
:return: 装饰器函数

:example:
>>> @sdk.adapter.on("message")
>>> async def handle_message(data):
>>>     print(f"收到OneBot12消息: {data}")

---

##### `middleware`

添加OneBot12中间件处理器

:param func: 中间件函数
:return: 中间件函数

:example:
>>> @sdk.adapter.middleware
>>> async def onebot_middleware(data):
>>>     print("处理OneBot12数据:", data)
>>>     return data

---

##### 🔹 `async` `emit`

提交OneBot12协议事件到指定平台

:param platform: 平台名称
:param event_type: OneBot12事件类型
:param data: 符合OneBot12标准的事件数据

⚠️ **可能抛出**: `ValueError` - 当平台未注册时抛出
    
:example:
>>> await sdk.adapter.emit("MyPlatform", "message", {
>>>     "id": "123",
>>>     "time": 1620000000,
>>>     "type": "message",
>>>     "detail_type": "private",
>>>     "message": [{"type": "text", "data": {"text": "Hello"}}]
>>> })

---

##### `register`

注册新的适配器类

:param platform: 平台名称
:param adapter_class: 适配器类
:return: 注册是否成功

⚠️ **可能抛出**: `TypeError` - 当适配器类无效时抛出
    
:example:
>>> adapter.register("MyPlatform", MyPlatformAdapter)

---

##### 🔹 `async` `startup`

启动指定的适配器

:param platforms: 要启动的平台列表，None表示所有平台

⚠️ **可能抛出**: `ValueError` - 当平台未注册时抛出
    
:example:
>>> # 启动所有适配器
>>> await adapter.startup()
>>> # 启动指定适配器
>>> await adapter.startup(["Platform1", "Platform2"])

---

##### 🔹 `async` `_run_adapter`

⚠️ **内部方法**：

运行适配器实例

:param adapter: 适配器实例
:param platform: 平台名称

---

##### 🔹 `async` `shutdown`

关闭所有适配器

:example:
>>> await adapter.shutdown()

---

##### `get`

获取指定平台的适配器实例

:param platform: 平台名称
:return: 适配器实例或None
    
:example:
>>> adapter = adapter.get("MyPlatform")

---

##### `__getattr__`

通过属性访问获取适配器实例

:param platform: 平台名称
:return: 适配器实例

⚠️ **可能抛出**: `AttributeError` - 当平台未注册时抛出
    
:example:
>>> adapter = adapter.MyPlatform

---

##### `platforms`

获取所有已注册的平台列表

:return: 平台名称列表
    
:example:
>>> print("已注册平台:", adapter.platforms)

---


*文档最后更新于 2025-07-17 16:39:14*

## env.md

# 📦 `ErisPulse.Core.env` 模块

*自动生成于 2025-07-17 16:39:14*

---

## 模块概述

ErisPulse 环境配置模块

提供键值存储、事务支持、快照和恢复功能，用于管理框架配置数据。基于SQLite实现持久化存储，支持复杂数据类型和原子操作。

💡 **提示**：

1. 支持JSON序列化存储复杂数据类型
2. 提供事务支持确保数据一致性
3. 自动快照功能防止数据丢失

---

## 🏛️ 类

### `EnvManager`

环境配置管理器

单例模式实现，提供配置的增删改查、事务和快照管理

💡 **提示**：

1. 使用get/set方法操作配置项
2. 使用transaction上下文管理事务
3. 使用snapshot/restore管理数据快照


#### 🧰 方法

##### `_init_db`

⚠️ **内部方法**：

初始化数据库

---

##### `get`

获取配置项的值

:param key: 配置项键名
:param default: 默认值(当键不存在时返回)
:return: 配置项的值

:example:
>>> timeout = env.get("network.timeout", 30)
>>> user_settings = env.get("user.settings", {})

---

##### `get_all_keys`

获取所有配置项的键名

:return: 键名列表

:example:
>>> all_keys = env.get_all_keys()
>>> print(f"共有 {len(all_keys)} 个配置项")

---

##### `set`

设置配置项的值

:param key: 配置项键名
:param value: 配置项的值
:return: 操作是否成功

:example:
>>> env.set("app.name", "MyApp")
>>> env.set("user.settings", {"theme": "dark"})

---

##### `set_multi`

批量设置多个配置项

:param items: 键值对字典
:return: 操作是否成功

:example:
>>> env.set_multi({
>>>     "app.name": "MyApp",
>>>     "app.version": "1.0.0",
>>>     "app.debug": True
>>> })

---

##### `getConfig`

获取模块/适配器配置项
:param key: 配置项的键(支持点分隔符如"module.sub.key")
:param default: 默认值
:return: 配置项的值

---

##### `setConfig`

设置模块/适配器配置
:param key: 配置项键名(支持点分隔符如"module.sub.key")
:param value: 配置项值
:return: 操作是否成功

---

##### `delete`

删除配置项

:param key: 配置项键名
:return: 操作是否成功

:example:
>>> env.delete("temp.session")

---

##### `delete_multi`

批量删除多个配置项

:param keys: 键名列表
:return: 操作是否成功

:example:
>>> env.delete_multi(["temp.key1", "temp.key2"])

---

##### `get_multi`

批量获取多个配置项的值

:param keys: 键名列表
:return: 键值对字典

:example:
>>> settings = env.get_multi(["app.name", "app.version"])

---

##### `transaction`

创建事务上下文

:return: 事务上下文管理器

:example:
>>> with env.transaction():
>>>     env.set("key1", "value1")
>>>     env.set("key2", "value2")

---

##### `_check_auto_snapshot`

⚠️ **内部方法**：

检查并执行自动快照

---

##### `set_snapshot_interval`

设置自动快照间隔

:param seconds: 间隔秒数

:example:
>>> # 每30分钟自动快照
>>> env.set_snapshot_interval(1800)

---

##### `clear`

清空所有配置项

:return: 操作是否成功

:example:
>>> env.clear()  # 清空所有配置

---

##### `load_env_file`

加载env.py文件中的配置项

:return: 操作是否成功

:example:
>>> env.load_env_file()  # 加载env.py中的配置

---

##### `__getattr__`

通过属性访问配置项

:param key: 配置项键名
:return: 配置项的值

⚠️ **可能抛出**: `KeyError` - 当配置项不存在时抛出
    
:example:
>>> app_name = env.app_name

---

##### `__setattr__`

通过属性设置配置项

:param key: 配置项键名
:param value: 配置项的值
    
:example:
>>> env.app_name = "MyApp"

---

##### `snapshot`

创建数据库快照

:param name: 快照名称(可选)
:return: 快照文件路径

:example:
>>> # 创建命名快照
>>> snapshot_path = env.snapshot("before_update")
>>> # 创建时间戳快照
>>> snapshot_path = env.snapshot()

---

##### `restore`

从快照恢复数据库

:param snapshot_name: 快照名称或路径
:return: 恢复是否成功

:example:
>>> env.restore("before_update")

---

##### `list_snapshots`

列出所有可用的快照

:return: 快照信息列表(名称, 创建时间, 大小)

:example:
>>> for name, date, size in env.list_snapshots():
>>>     print(f"{name} - {date} ({size} bytes)")

---

##### `delete_snapshot`

删除指定的快照

:param snapshot_name: 快照名称
:return: 删除是否成功

:example:
>>> env.delete_snapshot("old_backup")

---


*文档最后更新于 2025-07-17 16:39:14*

## logger.md

# 📦 `ErisPulse.Core.logger` 模块

*自动生成于 2025-07-17 16:39:14*

---

## 模块概述

ErisPulse 日志系统

提供模块化日志记录功能，支持多级日志、模块过滤和内存存储。

💡 **提示**：

1. 支持按模块设置不同日志级别
2. 日志可存储在内存中供后续分析
3. 自动识别调用模块名称

---

## 🏛️ 类

### `Logger`

日志管理器

提供模块化日志记录和存储功能

💡 **提示**：

1. 使用set_module_level设置模块日志级别
2. 使用get_logs获取历史日志
3. 支持标准日志级别(DEBUG, INFO等)


#### 🧰 方法

##### `set_level`

设置全局日志级别

:param level: 日志级别(DEBUG/INFO/WARNING/ERROR/CRITICAL)
:return: bool 设置是否成功

---

##### `set_module_level`

设置指定模块日志级别

:param module_name: 模块名称
:param level: 日志级别(DEBUG/INFO/WARNING/ERROR/CRITICAL)
:return: bool 设置是否成功

---

##### `set_output_file`

设置日志输出

:param path: 日志文件路径 Str/List
:return: bool 设置是否成功

---

##### `save_logs`

保存所有在内存中记录的日志

:param path: 日志文件路径 Str/List
:return: bool 设置是否成功

---

##### `get_logs`

获取日志内容

:param module_name (可选): 模块名称
:return: dict 日志内容

---


*文档最后更新于 2025-07-17 16:39:14*

## mods.md

# 📦 `ErisPulse.Core.mods` 模块

*自动生成于 2025-07-17 16:39:14*

---

## 模块概述

ErisPulse 模块管理器

提供模块的注册、状态管理和依赖关系处理功能。支持模块的启用/禁用、版本控制和依赖解析。

💡 **提示**：

1. 使用模块前缀区分不同模块的配置
2. 支持模块状态持久化存储
3. 自动处理模块间的依赖关系

---

## 🏛️ 类

### `ModuleManager`

模块管理器

管理所有模块的注册、状态和依赖关系

💡 **提示**：

1. 通过set_module/get_module管理模块信息
2. 通过set_module_status/get_module_status控制模块状态
3. 通过set_all_modules/get_all_modules批量操作模块


#### 🧰 方法

##### `_ensure_prefixes`

⚠️ **内部方法**：

确保模块前缀配置存在

---

##### `module_prefix`

获取模块数据前缀

:return: 模块数据前缀字符串

---

##### `status_prefix`

获取模块状态前缀

:return: 模块状态前缀字符串

---

##### `set_module_status`

设置模块启用状态

:param module_name: 模块名称
:param status: 启用状态

:example:
>>> # 启用模块
>>> mods.set_module_status("MyModule", True)
>>> # 禁用模块
>>> mods.set_module_status("MyModule", False)

---

##### `get_module_status`

获取模块启用状态

:param module_name: 模块名称
:return: 模块是否启用

:example:
>>> if mods.get_module_status("MyModule"):
>>>     print("模块已启用")

---

##### `set_module`

设置模块信息

:param module_name: 模块名称
:param module_info: 模块信息字典

:example:
>>> mods.set_module("MyModule", {
>>>     "version": "1.0.0",
>>>     "description": "我的模块",
>>>     "status": True
>>> })

---

##### `get_module`

获取模块信息

:param module_name: 模块名称
:return: 模块信息字典或None

:example:
>>> module_info = mods.get_module("MyModule")
>>> if module_info:
>>>     print(f"模块版本: {module_info.get('version')}")

---

##### `set_all_modules`

批量设置多个模块信息

:param modules_info: 模块信息字典

:example:
>>> mods.set_all_modules({
>>>     "Module1": {"version": "1.0", "status": True},
>>>     "Module2": {"version": "2.0", "status": False}
>>> })

---

##### `get_all_modules`

获取所有模块信息

:return: 模块信息字典

:example:
>>> all_modules = mods.get_all_modules()
>>> for name, info in all_modules.items():
>>>     print(f"{name}: {info.get('status')}")

---

##### `update_module`

更新模块信息

:param module_name: 模块名称
:param module_info: 完整的模块信息字典

---

##### `remove_module`

移除模块

:param module_name: 模块名称
:return: 是否成功移除

:example:
>>> if mods.remove_module("OldModule"):
>>>     print("模块已移除")

---

##### `update_prefixes`

更新模块前缀配置

:param module_prefix: 新的模块数据前缀(可选)
:param status_prefix: 新的模块状态前缀(可选)

:example:
>>> # 更新模块前缀
>>> mods.update_prefixes(
>>>     module_prefix="custom.module.data:",
>>>     status_prefix="custom.module.status:"
>>> )

---


*文档最后更新于 2025-07-17 16:39:14*

## raiserr.md

# 📦 `ErisPulse.Core.raiserr` 模块

*自动生成于 2025-07-17 16:39:14*

---

## 模块概述

ErisPulse 错误管理系统

提供错误类型注册、抛出和管理功能，集成全局异常处理。支持自定义错误类型、错误链追踪和全局异常捕获。

💡 **提示**：

1. 使用register注册自定义错误类型
2. 通过info获取错误信息
3. 自动捕获未处理异常

---

## 🛠️ 函数

### `global_exception_handler`

⚠️ **内部方法**：

全局异常处理器

:param exc_type: 异常类型
:param exc_value: 异常值
:param exc_traceback: 追踪信息

---

### `async_exception_handler`

⚠️ **内部方法**：

异步异常处理器

:param loop: 事件循环
:param context: 上下文字典

---

## 🏛️ 类

### `Error`

错误管理器

提供错误类型注册和抛出功能

💡 **提示**：

1. 通过register方法注册自定义错误类型
2. 通过动态属性访问抛出错误
3. 通过info方法获取错误信息


#### 🧰 方法

##### `register`

注册新的错误类型

:param name: 错误类型名称
:param doc: 错误描述文档
:param base: 基础异常类
:return: 注册的错误类

:example:
>>> # 注册简单错误
>>> raiserr.register("SimpleError", "简单的错误类型")
>>> # 注册自定义基类的错误
>>> raiserr.register("AdvancedError", "高级错误", CustomBaseError)

---

##### `__getattr__`

动态获取错误抛出函数

:param name: 错误类型名称
:return: 错误抛出函数

⚠️ **可能抛出**: `AttributeError` - 当错误类型未注册时抛出

---

##### `info`

获取错误信息

:param name: 错误类型名称(可选)
:return: 错误信息字典

:example:
>>> # 获取特定错误信息
>>> error_info = raiserr.info("SimpleError")
>>> # 获取所有错误信息
>>> all_errors = raiserr.info()

---


*文档最后更新于 2025-07-17 16:39:14*

## server.md

# 📦 `ErisPulse.Core.server` 模块

*自动生成于 2025-07-17 16:39:14*

---

## 模块概述

ErisPulse Adapter Server
提供统一的适配器服务入口，支持HTTP和WebSocket路由

💡 **提示**：

1. 适配器只需注册路由，无需自行管理服务器
2. WebSocket支持自定义认证逻辑
3. 兼容FastAPI 0.68+ 版本

---

## 🏛️ 类

### `AdapterServer`

适配器服务器管理器

💡 **提示**：

核心功能：
- HTTP/WebSocket路由注册
- 生命周期管理
- 统一错误处理


#### 🧰 方法

##### `__init__`

初始化适配器服务器

💡 **提示**：

会自动创建FastAPI实例并设置核心路由

---

##### `_setup_core_routes`

设置系统核心路由

⚠️ **内部方法**：

此方法仅供内部使用
{!--< /internal-use >!--}

---

##### `register_webhook`

注册HTTP路由

:param adapter_name: str 适配器名称
:param path: str 路由路径(如"/message")
:param handler: Callable 处理函数
:param methods: List[str] HTTP方法列表(默认["POST"])

⚠️ **可能抛出**: `ValueError` - 当路径已注册时抛出

💡 **提示**：

路径会自动添加适配器前缀，如：/adapter_name/path

---

##### `register_websocket`

注册WebSocket路由

:param adapter_name: str 适配器名称
:param path: str WebSocket路径(如"/ws")
:param handler: Callable[[WebSocket], Awaitable[Any]] 主处理函数
:param auth_handler: Optional[Callable[[WebSocket], Awaitable[bool]]] 认证函数

⚠️ **可能抛出**: `ValueError` - 当路径已注册时抛出

💡 **提示**：

认证函数应返回布尔值，False将拒绝连接

---

##### `get_app`

获取FastAPI应用实例

:return: 
    FastAPI: FastAPI应用实例

---

##### 🔹 `async` `start`

启动适配器服务器

:param host: str 监听地址(默认"0.0.0.0")
:param port: int 监听端口(默认8000)
:param ssl_certfile: Optional[str] SSL证书路径
:param ssl_keyfile: Optional[str] SSL密钥路径

⚠️ **可能抛出**: `RuntimeError` - 当服务器已在运行时抛出

---

##### 🔹 `async` `stop`

停止服务器

💡 **提示**：

会等待所有连接正常关闭

---


*文档最后更新于 2025-07-17 16:39:14*

## util.md

# 📦 `ErisPulse.Core.util` 模块

*自动生成于 2025-07-17 16:39:14*

---

## 模块概述

ErisPulse 工具函数集合

提供常用工具函数，包括拓扑排序、缓存装饰器、异步执行等实用功能。

💡 **提示**：

1. 使用@cache装饰器缓存函数结果
2. 使用@run_in_executor在独立线程中运行同步函数
3. 使用@retry实现自动重试机制

---

## 🏛️ 类

### `Util`

工具函数集合

提供各种实用功能，简化开发流程

💡 **提示**：

1. 拓扑排序用于解决依赖关系
2. 装饰器简化常见模式实现
3. 异步执行提升性能


#### 🧰 方法

##### `ExecAsync`

异步执行函数

:param async_func: 异步函数
:param args: 位置参数
:param kwargs: 关键字参数
:return: 函数执行结果

:example:
>>> result = util.ExecAsync(my_async_func, arg1, arg2)

---

##### `cache`

缓存装饰器

:param func: 被装饰函数
:return: 装饰后的函数

:example:
>>> @util.cache
>>> def expensive_operation(param):
>>>     return heavy_computation(param)

---

##### `run_in_executor`

在独立线程中执行同步函数的装饰器

:param func: 被装饰的同步函数
:return: 可等待的协程函数

:example:
>>> @util.run_in_executor
>>> def blocking_io():
>>>     # 执行阻塞IO操作
>>>     return result

---

##### `retry`

自动重试装饰器

:param max_attempts: 最大重试次数 (默认: 3)
:param delay: 重试间隔(秒) (默认: 1)
:return: 装饰器函数

:example:
>>> @util.retry(max_attempts=5, delay=2)
>>> def unreliable_operation():
>>>     # 可能失败的操作

---


*文档最后更新于 2025-07-17 16:39:14*

<!--- End of API文档 -->
