# excution/service/exchange/api/okxapi.py

import hashlib
import hmac
import base64
import time
import logging
from urllib.parse import urlencode
from ...connection.restapi import RestAPIClient  # 注意引用路徑

logger = logging.getLogger(__name__)

class OkxAPIClient(RestAPIClient):
    """
    專門給 OKX 用的 API 客戶端。
    若需要簽名，將產生 OK-ACCESS-SIGN，並在 header 中加入 OKX 所需的認證資訊。
    """
    def __init__(self, api_key: str = None, api_secret: str = None, passphrase: str = None):
        super().__init__()
        self.api_key = api_key
        self.api_secret = api_secret
        self.passphrase = passphrase

    def _get_timestamp(self):
        # 取得 UTC 時間並轉成 ISO8601 格式
        return time.strftime("%Y-%m-%dT%H:%M:%S.000Z", time.gmtime())

    async def request(self, method: str, url: str, params: dict = {}, auth: bool = False):
        await self.init_session()
        try:
            if auth:
                params = params.copy()
                timestamp = self._get_timestamp()
                query_string = ""
                if method.upper() == "GET" and params:
                    # GET 請求將參數以 query string 傳遞
                    query_string = "?" + urlencode(sorted(params.items()))
                # 取得 URL 中的 request path（不含域名）
                request_path = url.split("://")[-1].split("/", 1)[-1]
                # OKX 簽名內容：timestamp + method + "/" + request_path + query_string
                prehash = timestamp + method.upper() + "/" + request_path + (query_string if query_string else "")
                signature = hmac.new(self.api_secret.encode(), prehash.encode(), hashlib.sha256).digest()
                signature_b64 = base64.b64encode(signature).decode()
                headers = {
                    "OK-ACCESS-KEY": self.api_key,
                    "OK-ACCESS-SIGN": signature_b64,
                    "OK-ACCESS-TIMESTAMP": timestamp,
                    "OK-ACCESS-PASSPHRASE": self.passphrase,
                    "Content-Type": "application/json"
                }
                full_url = url + query_string
                return await super().signed_request(method, full_url, headers)
            else:
                return await super().request(method, url, params=params)
        except Exception as e:
            raise Exception(f"\n[OkxAPIClient] request failed: {e}")

    async def close(self):
        await super().close()
