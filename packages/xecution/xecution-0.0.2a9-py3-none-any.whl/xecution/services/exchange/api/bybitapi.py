# excution/service/exchange/api/bybitapi.py

import hashlib
import hmac
import logging
import time
from urllib.parse import urlencode
from ...connection.restapi import RestAPIClient  # 注意引用路徑

logger = logging.getLogger(__name__)

class BybitAPIClient(RestAPIClient):
    """
    專門給 Bybit 用的 API 客戶端。
    若需要簽名，會在請求參數中加入 api_key、timestamp 與 recv_window，
    並根據排序後的 query string 產生簽名，最後將簽名附加在 URL 中。
    """
    def __init__(self, api_key: str = None, api_secret: str = None):
        super().__init__()
        self.api_key = api_key
        self.api_secret = api_secret

    async def request(self, method: str, url: str, params: dict = {}, auth: bool = False):
        await self.init_session()
        try:
            if auth:
                params = params.copy()
                # Bybit 需要在參數中帶入 api_key 與 timestamp
                params["api_key"] = self.api_key
                params["timestamp"] = int(time.time() * 1000)
                params["recv_window"] = 5000  # Bybit 的接收窗口參數
                # 排序參數並產生 query string
                query_string = urlencode(sorted(params.items()))
                # 產生簽名（使用 HMAC-SHA256）
                signature = hmac.new(self.api_secret.encode(), query_string.encode(), hashlib.sha256).hexdigest()
                # 將簽名參數加到 URL 中，參數名稱為 sign
                url = f"{url}?{query_string}&sign={signature}"
                headers = {"Content-Type": "application/json"}
                return await super().signed_request(method, url, headers)
            else:
                return await super().request(method, url, params=params)
        except Exception as e:
            raise Exception(f"\n[BybitAPIClient] request failed: {e}")

    async def close(self):
        await super().close()
