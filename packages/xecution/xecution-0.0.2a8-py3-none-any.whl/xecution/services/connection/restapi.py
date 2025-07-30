import aiohttp
import logging

logger = logging.getLogger(__name__)

class RestAPIClient:
    """
    Generic REST API client skeleton.
    
    Subclasses can override `_handle_response` to implement service-specific
    error handling (e.g., Binance, Bybit, OKX).
    Shared error handling logic for all services can also be placed here.
    """
    def __init__(self):
        self.session = None

    async def init_session(self):
        """Initialize the aiohttp session if not already open."""
        if self.session is None or self.session.closed:
            self.session = aiohttp.ClientSession()

    async def _handle_response(self, response):
        """
        Basic response handler.
        
        Raises an exception if the HTTP status is not 200, including
        the response body for debugging. Otherwise, returns parsed JSON.
        """
        try:
            if response.status != 200:
                text = await response.text()
                raise Exception(f"[HTTP {response.status}] Error: {text}")
            return await response.json()
        except Exception as err:
            raise err

    async def request(self, method: str, url: str, params: dict = None, headers: dict = None, timeout: int = 10):
        """
        Send a generic HTTP request.
        
        - GET requests will include `params` in the query string.
        - POST requests will send `params` as JSON payload.
        """
        await self.init_session()
        params = params or {}
        headers = headers or {"Content-Type": "application/json"}

        try:
            async with self.session.request(
                method=method.upper(),
                url=url,
                params=params if method.upper() == "GET" else None,
                json=params if method.upper() == "POST" else None,
                headers=headers,
                timeout=aiohttp.ClientTimeout(total=timeout)
            ) as resp:
                return await self._handle_response(resp)
        except Exception as e:
            raise Exception(f"[{method}] request to {url} failed: {e!r}") from e

    async def signed_request(self, method: str, url: str, headers: dict, timeout: int = 10):
        """
        Send an authenticated HTTP request.
        
        Note: Do not include a JSON body (`json=params`) here to avoid
        request body conflicts; subclasses should build signed URLs or
        include parameters in the headers if needed.
        """
        await self.init_session()
        try:
            async with self.session.request(
                method=method.upper(),
                url=url,
                headers=headers,
                timeout=aiohttp.ClientTimeout(total=timeout)
            ) as resp:
                return await self._handle_response(resp)
        except Exception as e:
            raise Exception(f"[{method}] request to {url} failed: {e!r}") from e

    async def close(self):
        """Close the HTTP session if it's open."""
        if self.session and not self.session.closed:
            await self.session.close()
