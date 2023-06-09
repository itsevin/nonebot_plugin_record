from nonebot import get_driver

from typing import Optional
from pydantic import (
    BaseModel,
    Extra
)


class Config(BaseModel, extra=Extra.ignore):
    nonebot_plugin_gocqhttp: Optional[bool] = False
    gocqhttp_address: Optional[str] = './'
    asr_api_provider: str = None
    asr_api_key: str = None
    asr_secret_key: str = None


plugin_config = Config.parse_obj(get_driver().config.dict())
