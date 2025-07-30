import hashlib
import hmac
import logging
import time
from urllib.parse import urlencode
from ...connection.restapi import RestAPIClient  # Note import path

logger = logging.getLogger(__name__)

class BinanceAPIClient(RestAPIClient):
    """
    API client specifically for Binance.
    - Override `request` with auth=True to add signing.
    - Override `_handle_response` for Binance-specific error handling.
    """
    def __init__(self, api_key: str = None, api_secret: str = None):
        super().__init__()
        self.api_key = api_key
        self.api_secret = api_secret

    async def request(self, method: str, url: str, params: dict = {}, auth: bool = False):
        """
        Override request() to include Binance-specific headers and signature when `auth=True`.
        """
        await self.init_session()
        try:
            if auth:
                # 1. Prepare a copy of the parameters
                params = params.copy()
                params["timestamp"] = int(time.time() * 1000)
                params["recvWindow"] = 5000
                # 2. Build sorted query string
                query_string = urlencode(sorted(params.items()))
                # 3. Generate signature
                signature = hmac.new(
                    self.api_secret.encode(),
                    query_string.encode(),
                    hashlib.sha256
                ).hexdigest()
                url = f"{url}?{query_string}&signature={signature}"
                # 4. Set headers for authenticated request
                headers = {
                    "X-MBX-APIKEY": self.api_key,
                    "Content-Type": "application/json"
                }
                return await super().signed_request(method, url, headers)
            else:
                # Non-authenticated request
                return await super().request(method, url, params=params)
        except Exception as e:
            # Call parent class (RestAPIClient) request error
            raise Exception(f"[BinanceAPIClient] request failed: {e}")

    async def close(self):
        """Close the underlying HTTP session."""
        await super().close()
