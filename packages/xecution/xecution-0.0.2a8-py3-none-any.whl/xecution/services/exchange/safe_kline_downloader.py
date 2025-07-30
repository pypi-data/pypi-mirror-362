import asyncio
import logging

class SafeKlineDownloader:
    def __init__(
        self,
        session,
        fetch_func,
        endpoint,
        symbol,
        interval,
        max_limit=1000,
        time_increment_ms=60_000,
        max_concurrent_requests=5,
        chunk_sleep=1.2
    ):
        self.session = session
        self.fetch_func = fetch_func
        self.endpoint = endpoint
        self.symbol = symbol
        self.interval = interval
        self.max_limit = max_limit
        self.time_increment = time_increment_ms
        self.max_concurrent_requests = max_concurrent_requests
        self.chunk_sleep = chunk_sleep

    async def fetch_with_retry(self, params, retries=3):
        for attempt in range(retries):
            try:
                data = await self.fetch_func(self.session, self.endpoint, params)
                if isinstance(data, dict) and data.get("code") == -1003:
                    logging.warning(f"❌ Rate limited: {data.get('msg')}")
                    await asyncio.sleep(60 + attempt * 10)
                    continue
                return data
            except Exception as e:
                logging.warning(f"⚠️ Fetch attempt {attempt + 1} failed: {e}")
                await asyncio.sleep(2 ** attempt)
        raise Exception("Exceeded retry limit")

    async def download(self, start_time: int, total_needed: int = 1000):
        # 預先建立所有請求參數
        num_batches = -(-total_needed // self.max_limit)  # ceiling division
        requests = []
        for i in range(num_batches):
            params = {
                "symbol": self.symbol,
                "interval": self.interval,
                "limit": min(self.max_limit, total_needed - i * self.max_limit),
                "startTime": start_time + i * self.max_limit * self.time_increment
            }
            requests.append(params)

        total_data = []
        semaphore = asyncio.Semaphore(self.max_concurrent_requests)

        async def safe_fetch(p):
            async with semaphore:
                return await self.fetch_with_retry(p)

        for i in range(0, len(requests), self.max_concurrent_requests):
            chunk = requests[i:i + self.max_concurrent_requests]
            tasks = [safe_fetch(p) for p in chunk]
            results = await asyncio.gather(*tasks)
            for batch in results:
                if batch:
                    total_data.extend(batch)
            logging.debug(f"已完成第 {i // self.max_concurrent_requests + 1} 輪，共累積 {len(total_data)} 筆")
            await asyncio.sleep(self.chunk_sleep)

        return total_data
    
    async def download_reverse(self,end_time: int,total_needed: int = 1000):
        """
        從最新時間開始，向過去拉 total_needed 筆資料
        使用 endTime 向前翻頁
        """
        total_data = []

        # 第一次請求：不帶 startTime / endTime
        params = {
            "symbol": self.symbol,
            "interval": self.interval,
            "limit": min(self.max_limit, total_needed),
            "endTime": end_time
        }

        batch = await self.fetch_with_retry(params)
        if not batch:
            return total_data

        total_data.extend(batch)

        # 設定下一批的 endTime（往前翻頁）
        earliest_open_time = batch[0][0]  # 最早一根的 openTime（毫秒）

        while len(total_data) < total_needed:
            remaining = total_needed - len(total_data)
            limit = min(self.max_limit, remaining)
            params = {
                "symbol": self.symbol,
                "interval": self.interval,
                "limit": limit,
                "endTime": earliest_open_time - 1  # 注意：不包含 endTime 當天
            }

            batch = await self.fetch_with_retry(params)
            if not batch:
                break

            total_data = batch + total_data  # 往前疊加資料
            earliest_open_time = batch[0][0]  # 更新下一輪 endTime
            await asyncio.sleep(self.chunk_sleep)
            
        logging.debug(f"Retrieved {len(total_data)} {self.symbol} historical data")
        return total_data

