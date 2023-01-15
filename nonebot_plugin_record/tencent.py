from datetime import datetime
import httpx
import hashlib
import hmac
import json
import time

from .config import plugin_config


secret_id = plugin_config.asr_api_key
secret_key = plugin_config.asr_secret_key


async def _get_authorization(params):
    service = "asr"
    host = "asr.tencentcloudapi.com"
    algorithm = "TC3-HMAC-SHA256"
    timestamp = int(time.time())
    date = datetime.utcfromtimestamp(timestamp).strftime("%Y-%m-%d")

    # ************* 步骤 1：拼接规范请求串 *************
    http_request_method = "POST"
    canonical_uri = "/"
    canonical_querystring = ""
    ct = "application/json; charset=utf-8"
    payload = json.dumps(params)
    canonical_headers = "content-type:%s\nhost:%s\n" % (ct, host)
    signed_headers = "content-type;host"
    hashed_request_payload = hashlib.sha256(payload.encode("utf-8")).hexdigest()
    canonical_request = (http_request_method + "\n" +
                         canonical_uri + "\n" +
                         canonical_querystring + "\n" +
                         canonical_headers + "\n" +
                         signed_headers + "\n" +
                         hashed_request_payload)

    # ************* 步骤 2：拼接待签名字符串 *************
    credential_scope = date + "/" + service + "/" + "tc3_request"
    hashed_canonical_request = hashlib.sha256(canonical_request.encode("utf-8")).hexdigest()
    string_to_sign = (algorithm + "\n" +
                      str(timestamp) + "\n" +
                      credential_scope + "\n" +
                      hashed_canonical_request)

    # ************* 步骤 3：计算签名 *************
    # 计算签名摘要函数
    async def _sign(key, msg):
        return hmac.new(key, msg.encode("utf-8"), hashlib.sha256).digest()
    secret_date = await _sign(("TC3" + secret_key).encode("utf-8"), date)
    secret_service = await _sign(secret_date, service)
    secret_signing = await _sign(secret_service, "tc3_request")
    signature = hmac.new(secret_signing, string_to_sign.encode("utf-8"), hashlib.sha256).hexdigest()

    # ************* 步骤 4：拼接 Authorization *************
    authorization = (algorithm + " " +
                     "Credential=" + secret_id + "/" + credential_scope + ", " +
                     "SignedHeaders=" + signed_headers + ", " +
                     "Signature=" + signature)
    return authorization


async def tencent_get_text(speech, length):
    timestamp = int(time.time())
    url = "https://asr.tencentcloudapi.com"
    data = {
        "ProjectId": 0,
        "SubServiceType": 2,
        "EngSerViceType": "16k_zh",
        "SourceType": 1,
        "VoiceFormat": "pcm",
        "UsrAudioKey": "github.com/itsevin",
        "Data": speech,
        "DataLen": length
    }
    headers = {
        "Authorization": await _get_authorization(data),
        "Content-Type": "application/json; charset=utf-8",
        "Host": "asr.tencentcloudapi.com",
        "X-TC-Action": "SentenceRecognition",
        "X-TC-Version": "2019-06-14",
        "X-TC-Timestamp": str(timestamp),
    }
    async with httpx.AsyncClient() as client:
        resp = await client.post(url, headers=headers, json=data)
        text = json.loads(resp.text)["Response"]["Result"]
    return text
