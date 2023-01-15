from nonebot import on_message
from nonebot.matcher import Matcher
from nonebot.rule import Rule
from nonebot.typing import T_RuleChecker
from nonebot.adapters.onebot.v11 import (
    Message,
    Event,
    Bot
)

import base64
import pilk
import os
from typing import (
    Type,
    Union,
    Optional
)

from .config import plugin_config
from .baidu import baidu_get_text
from .tencent import tencent_get_text


async def type_checker(event: Event) -> bool:
    """判断消息类型为语音的规则。

    依赖参数:

    - event: Event 对象
    """
    return event.get_message()[0].type == "record"


def on_record(
    rule: Optional[Union[Rule, T_RuleChecker]] = None,
    **kwargs,
) -> Type[Matcher]:
    """注册一个语音事件响应器。

    参数:
        rule: 事件响应规则
        permission: 事件响应权限
        handlers: 事件处理函数列表
        temp: 是否为临时事件响应器（仅执行一次）
        expire_time: 事件响应器最终有效时间点，过时即被删除
        priority: 事件响应器优先级
        block: 是否阻止事件向更低优先级传递
        state: 默认 state
    """
    return on_message(rule=Rule(type_checker) & rule, **kwargs)


async def get_text(bot: Bot, event: Event):
    """通过语音识别获取语音中的文本，仅支持普通话。

    依赖参数:

    - bot: Bot 对象
    - event: Event 对象
    """
    if plugin_config.nonebot_plugin_gocqhttp is True:
        path_amr = "./accounts/" + bot.self_id + "/data/voices/" + event.get_message()[0].data["file"]
    else:
        path_amr = "./data/voices" + event.get_message()[0].data["file"]
    path_pcm = path_amr[0:-4] + ".pcm"
    pilk.decode(path_amr, path_pcm)
    with open(path_pcm, 'rb') as f:
        speech = base64.b64encode(f.read()).decode('utf-8')
    length = os.path.getsize(path_pcm)
    os.remove(path_pcm)
    if plugin_config.asr_api_provider == "baidu":
        text = await baidu_get_text(speech, length)
    elif plugin_config.asr_api_provider == "tencent":
        text = await tencent_get_text(speech, length)
    else:
        return None
    return text


def record_tts(pattern: str):
    """获取字符串转换的语音的Message对象。
    调用的TX的接口，采用的音源与登录账号的性别有关

    参数:
        pattern: 要进行转换的字符串
    """
    return Message("[CQ:tts,text=" + pattern + "]")
