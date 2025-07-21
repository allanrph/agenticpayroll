import httpx

class HttpClientBase:
    BASE_URL: str
    TIMEOUT = 30

    def __init__(self):
        self.client = httpx.AsyncClient(base_url=self.BASE_URL, timeout=self.TIMEOUT)

    async def request(self, method: str, url: str, **kwargs):
        try:
            response = await self.client.request(method, url, **kwargs)
            response.raise_for_status()
            return response
        except httpx.HTTPStatusError as exc:
            raise RuntimeError(f"HTTP error {exc.response.status_code}: {exc.response.text}") from exc
        except httpx.RequestError as exc:
            raise RuntimeError(f"Request error: {exc}") from exc

    async def close(self):
        await self.client.aclose()