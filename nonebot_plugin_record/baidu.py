from nonebot import logger
import httpx
import json

from .config import plugin_config


API_KEY = plugin_config.asr_api_key
SECRET_KEY = plugin_config.asr_secret_key


async def _get_token():
    url = f'https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id={API_KEY}&client_secret=' \
          f'{SECRET_KEY}'
    async with httpx.AsyncClient() as client:
        resp = await client.get(url)
        token = json.loads(resp.text)["access_token"]
    logger.debug("get_token Succeeded")
    return token


async def baidu_get_text(speech, length):
    url = "https://vop.baidu.com/server_api"
    data = {
        "format": "pcm",
        "rate": 16000,
        "channel": 1,
        "cuid": "nonebot_plugin_record",
        "speech": speech,
        "len": length,
        "token": await _get_token()
    }
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }
    async with httpx.AsyncClient() as client:
        try:
            resp = await client.post(url, headers=headers, json=data)
            if json.loads(resp.text)["err_msg"] == "success.":
                text = json.loads(resp.text)["result"][0]
                logger.debug("baidu_get_text Succeeded")
                return text
            else:
                logger.error(f"语音识别接口报错，返回内容：{resp.text}")
                return None
        except:
            logger.error("请求语音识别接口失败，请检查网络环境或重试")
            return None
