# 📦 `ErisPulse.Core.raiserr` 模块

*自动生成于 2025-07-17 16:57:03*

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


*文档最后更新于 2025-07-17 16:57:03*