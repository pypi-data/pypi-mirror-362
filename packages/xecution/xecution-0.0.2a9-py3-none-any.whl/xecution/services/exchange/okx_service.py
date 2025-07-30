from xecution.models.config import RuntimeConfig
from xecution.services.connection.base_websockets import WebSocketService
from xecution.services.exchange.exchange_order_manager import OKXOrderManager  


class OkxService:
    
    def __init__(self, config: RuntimeConfig, data_map: dict):
        """
        Okx Service for managing WebSocket and API interactions.
        """
        self.config = config
        self.ws_service = WebSocketService()
        self.data_map = data_map  # External data map reference
        self.manager = OKXOrderManager(
            api_key=config.API_Key,
            api_secret=config.API_Secret,
            mode = config.mode
        )
        
    async def get_current_price(self,symbol: str):
        return await self.manager.get_current_price(symbol)
