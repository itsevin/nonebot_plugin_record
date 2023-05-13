<div align="center">
  <a href="https://v2.nonebot.dev/store"><img src="https://s2.loli.net/2022/06/16/opBDE8Swad5rU3n.png" width="180" height="180" alt="NoneBotPluginLogo"></a>
  <br>
  <p><img src="https://s2.loli.net/2022/06/16/xsVUGRrkbn1ljTD.png" width="240" alt="NoneBotPluginText"></p>
</div>

<div align="center">

# Nonebot-Plugin-Record

_✨ 基于 [NoneBot2](https://v2.nonebot.dev/) 的语音功能适配插件 ✨_

<p align="center">
  <img src="https://img.shields.io/github/license/itsevin/nonebot_plugin_record" alt="license">
  <img src="https://img.shields.io/badge/python-3.8+-blue.svg" alt="Python">
  <img src="https://img.shields.io/badge/nonebot-2.0.0b4+-red.svg" alt="NoneBot">
  <a href="https://pypi.org/project/nonebot-plugin-record">
    <img src="https://badgen.net/pypi/v/nonebot-plugin-record" alt="pypi">
  </a>
</p>

</div>

## 功能

- 语音事件响应器（仅限私聊）
- 语音识别（仅限私聊，支持百度智能云、腾讯云接口）
- 语音合成（利用TX的tts接口）

## 安装

- 使用 nb-cli

```
nb plugin install nonebot-plugin-record
```

- 使用 pip

```
pip install nonebot_plugin_record
```

## 配置项

```
asr_api_provider="" #必填，API提供商，填写“baidu”或“tencent”
asr_api_key="" #必填，百度智能云的API_KRY或腾讯云的SECRET_ID
asr_secret_key="" #必填，百度智能云的SECRET_KRY或腾讯云的SECRET_KEY
nonebot_plugin_gocqhttp=False #选填，是否使用nonebot2插件版本的go-cqhttp，默认为False
```

## API选择与配置

### 选什么API?

- 百度智能云-短语音识别标准版：5并发，15万次免费调用量，期限180天
- 腾讯云-一句话识别：每月5000次免费调用量（推荐）

### 获取密钥

- 百度智能云：https://ai.baidu.com/tech/speech
- 腾讯云：https://cloud.tencent.com/document/product/1093

## 如何使用？

### 语音事件响应器的使用

语音事件响应器：```on_record()```

说明：语音事件响应器继承自```on_message```，在其上增加了自定义的相应事件响应规则

选填参数：

```
rule: 事件响应规则
permission: 事件响应权限
handlers: 事件处理函数列表
temp: 是否为临时事件响应器（仅执行一次）
expire_time: 事件响应器最终有效时间点，过时即被删除
priority: 事件响应器优先级
block: 是否阻止事件向更低优先级传递
state: 默认 state
```

代码示例：

```python
# 导入依赖包
from nonebot import require
require('nonebot_plugin_record')
from nonebot_plugin_record import on_record

# 注册语音事件响应器
matcher = on_record()
```

### 获取语音中的文本

获取文本的异步函数：```get_text```()

必填参数：

```
bot: Bot 对象
event: Event 对象
```

代码示例：

```python
# 导入依赖包
from nonebot import require
require('nonebot_plugin_record')
from nonebot_plugin_record import get_text
from nonebot.adapters.onebot.v11 import Event, Bot

# 事件处理中获取文本
text = await get_text(bot=bot, event=event)
```

> 当函数出错时会返回None，具体报错信息请前往Nonebot2进程日志查看

### 获取文本转换的语音的```Message```对象

获取文本转换的语音的Message对象的异步函数：```record_tts```()

必填参数：
```
patter: 要进行转换的字符串
```

代码示例：

```python
# 导入依赖包
from nonebot import require
require('nonebot_plugin_record')
from nonebot_plugin_record import record_tts

# 事件处理中获取文本转换的语音的Message对象
record_tts(pattern=pattern)
```

### 插件示例

私聊语音聊天插件：

```python
from nonebot.adapters.onebot.v11 import (
    Event,
    Bot
)
from nonebot import require
require('nonebot_plugin_record')
from nonebot_plugin_record import (
    on_record,
    get_text,
    record_tts
)

import httpx
import json


chat = on_record()


@chat.handle()
async def main(bot: Bot, event: Event):
    text = await get_text(bot, event)
    msg = await get_data(text)
    await chat.finish(record_tts(msg))


async def get_data(msg):
    url = f'http://api.qingyunke.com/api.php?key=free&appid=0&msg={msg}'
    async with httpx.AsyncClient() as client:
        resp = await client.get(url)
        get_dic = json.loads(resp.text)
    data = get_dic['content']
    return data

```

## 有问题怎么办？

1. 确认是不是你自己的插件的问题
2. 确认是否正确按照本插件使用说明使用
3. 排查日志，通过日志内容尝试找出问题并自行解决
4. 在配置文件中配置```LOG_LEVEL=DEBUG```，然后在日志中查看debug日志，并同时根据本插件源码尝试找出问题并自行解决（确认是本插件的问题可以提issue或者pr）
5. 问题仍未解决可以提issue，要求提供详细问题描述和较为完整的debug级别的相关日志

## 更新日志

### 2023/5/13 \[v1.0.4]

- 重构代码，舍弃CQ码过时写法
- 增加dubug和info级别的日志输出

### 2023/1/27 \[v1.0.3]

- 修复错误

### 2023/1/15 \[v1.0.2]

- 修复错误

### 2023/1/15 \[v1.0.1]

- 适配Nonebot2商店插件自动检测，删除配置文件报错提醒

### 2023/1/15 \[v1.0.0]

- 发布插件
