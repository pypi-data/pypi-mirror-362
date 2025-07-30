import json
import logging
import asyncio
import aiohttp
from datetime import datetime, timedelta, timezone
from xecution.common.datasource_constants import CryptoQuantConstants
from xecution.models.config import RuntimeConfig
from xecution.models.topic import DataTopic, DataProvider
from xecution.services.connection.restapi import RestAPIClient

class CryptoQuantClient:
    def __init__(self, config: RuntimeConfig, data_map: dict):
        self.config      = config
        self.rest_client = RestAPIClient()
        self.data_map    = data_map
        self.headers     = {
            'Authorization': f'Bearer {self.config.cryptoquant_api_key}',
        }

    async def fetch(self, data_topic: DataTopic, last_n: int = 3):
        """
        Fetch only the last `last_n` records for `data_topic` (no `to` param).
        """
        # parse path and base params
        if '?' in data_topic.url:
            path, qs = data_topic.url.split('?', 1)
            base_params = dict(part.split('=', 1) for part in qs.split('&'))
        else:
            path = data_topic.url
            base_params = {}

        url = CryptoQuantConstants.BASE_URL + path
        params = {**base_params, 'limit': last_n}

        try:
            raw = await self.rest_client.request(
                method='GET', url=url, params=params, headers=self.headers,timeout=50
            )
        except Exception as e:
            logging.error(f"[{datetime.now()}] Error fetching last {last_n} for {data_topic.url}: {e}")
            return []

        result = raw.get('result', raw)
        data   = result.get('data') if isinstance(result, dict) else result
        items  = data if isinstance(data, list) else [data]

        processed = []
        for item in items or []:
            dt_str = item.get('datetime') or item.get('date')
            if dt_str:
                try:
                    item['start_time'] = self.parse_datetime_to_timestamp(dt_str)
                except ValueError as ex:
                    logging.warning(f"Date parsing failed ({dt_str}): {ex}")
            processed.append(item)

        processed.sort(key=lambda x: x.get('start_time', 0))
        final = processed[-last_n:]

        self.data_map[data_topic] = final
        return final

    async def fetch_all_parallel(self, data_topic: DataTopic):
        """
        Fetch up to `config.data_count` hourly bars ending now.  
        Only the batch-fetch loop is used for the stablecoins-ratio endpoint;  
        all other topics use a single GET and then the same flatten/dedupe/fill logic.
        Ensures the aiohttp session is always closed to prevent warnings.
        """
        limit      = self.config.data_count
        base_limit = 1000
        windows    = -(-limit // base_limit)  # ceil division
        end        = datetime.now(timezone.utc)

        # parse URL and base params
        if '?' in data_topic.url:
            path, qs = data_topic.url.split('?', 1)
            base_params = dict(part.split('=') for part in qs.split('&'))
        else:
            path = data_topic.url
            base_params = {}
        url = CryptoQuantConstants.BASE_URL + path

        session = aiohttp.ClientSession()
        try:
            if not (
                data_topic.provider is DataProvider.CRYPTOQUANT and
                'stablecoins-ratio' in data_topic.url
            ):
                # single-fetch branch
                try:
                    async with session.get(url, params={**base_params, 'limit': limit, 'format': 'json'}, headers=self.headers) as resp:
                        resp.raise_for_status()
                        raw = await resp.json()
                except Exception as e:
                    logging.error(f"[{datetime.now()}] Error fetching data for {data_topic.url}: {e}")
                    batches = [[]]
                else:
                    result = raw.get('result', raw)
                    data   = result.get('data') if isinstance(result, dict) else result
                    items  = data if isinstance(data, list) else [data]
                    # attach timestamps
                    batch = []
                    for item in items or []:
                        dt_str = item.get('datetime') or item.get('date')
                        if dt_str:
                            try:
                                item['start_time'] = self.parse_datetime_to_timestamp(dt_str)
                            except ValueError as ex:
                                logging.warning(f"Date parsing failed ({dt_str}): {ex}")
                        batch.append(item)
                    batches = [batch]
            else:
                # batch-fetch branch for stablecoins-ratio
                async def fetch_batch(to_ts: datetime):
                    from_str = to_ts.strftime('%Y%m%dT%H%M%S')
                    params   = {**base_params, 'limit': base_limit, 'to': from_str, 'format': 'json'}
                    try:
                        async with session.get(url, params=params, headers=self.headers) as resp:
                            resp.raise_for_status()
                            raw = await resp.json()
                    except Exception as e:
                        logging.error(f"[{datetime.now()}] Parallel fetch error: {e}")
                        return []

                    result = raw.get('result', raw.get('data', raw))
                    if isinstance(result, dict) and 'data' in result:
                        result = result['data']
                        if isinstance(result, str):
                            result = json.loads(result)
                    if isinstance(result, dict):
                        result = [result]

                    recs = []
                    for item in result or []:
                        dt_str = item.get('datetime')
                        if dt_str:
                            try:
                                item['start_time'] = self.parse_datetime_to_timestamp(dt_str)
                            except ValueError as ex:
                                logging.warning(f"Date parsing failed ({dt_str}): {ex}")
                                continue
                        recs.append(item)
                    return recs

                tasks   = [fetch_batch(end - timedelta(hours=i * base_limit)) for i in range(windows)]
                batches = await asyncio.gather(*tasks)
        finally:
            await session.close()

        # === common post-processing: flatten, sort, dedupe, forward-fill ===
        flat    = [rec for batch in batches for rec in batch if isinstance(rec, dict)]
        flat.sort(key=lambda x: x.get('start_time', 0))
        deduped = {x['start_time']: x for x in flat if 'start_time' in x}

        buffer    = 5
        effective = max(0, limit - buffer)
        final     = list(deduped.values())[-effective:]

        # forward-fill missing values
        filled = []
        prev   = None
        for rec in final:
            if prev is not None:
                for k, v in rec.items():
                    if v is None:
                        logging.warning(
                            f"Missing value for '{k}' at start_time: {rec['start_time']}, datetime: {rec.get('datetime')} - forward-filled"
                        )
                        rec[k] = prev.get(k)
            else:
                for k, v in rec.items():
                    if v is None:
                        logging.error(f"Missing value for '{k}' at start_time {rec['start_time']}")
            filled.append(rec)
            prev = rec

        self.data_map[data_topic] = filled
        return filled

    def parse_datetime_to_timestamp(self, dt_str: str) -> int:
        for fmt in (
            '%Y-%m-%dT%H:%M:%S.%fZ',
            '%Y-%m-%dT%H:%M:%SZ',
            '%Y-%m-%d %H:%M:%S',
        ):
            try:
                dt = datetime.strptime(dt_str, fmt).replace(tzinfo=timezone.utc)
                return int(dt.timestamp() * 1000)
            except ValueError:
                continue
        try:
            clean = dt_str.rstrip('Z')
            dt    = datetime.fromisoformat(clean)
            if dt.tzinfo is None:
                dt = dt.replace(tzinfo=timezone.utc)
            return int(dt.timestamp() * 1000)
        except Exception:
            raise ValueError(f"Unrecognized date format: {dt_str}")
