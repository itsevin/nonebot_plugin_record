from nonebot import get_driver

from typing import Optional
from pydantic import (
    BaseModel,
    Extra
)


class Config(BaseModel, extra=Extra.ignore):
    nonebot_plugin_gocqhttp: Optional[bool] = False
    asr_api_provider: str = None
    asr_api_key: str = None
    asr_secret_key: str = None


plugin_config = Config.parse_obj(get_driver().config.dict())

assert(
    plugin_config.asr_api_provider is not None and plugin_config.asr_api_key is not None
    and plugin_config.asr_secret_key is not None
), "请填写完整配置！"
assert(
    plugin_config.asr_api_provider in ["baidu", "tencent"]
), "asr_api_provider配置项只能填写“baidu”或“tencent”"
