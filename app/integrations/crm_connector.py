import httpx
import structlog

logger = structlog.get_logger(__name__)

class CRMConnector:
    def __init__(self, base_url: str, api_key: str):
        self.base_url = base_url
        self.client = httpx.AsyncClient(headers={"Authorization": f"Bearer {api_key}"}, timeout=15.0)

    async def get_customer(self, email: str):
        resp = await self.client.get(f"/api/customers?email={email}")
        resp.raise_for_status()
        return resp.json()

    async def close(self):
        await self.client.aclose()