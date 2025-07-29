import os
import httpx


class BookClient:
    def __init__(self):
        base_url = os.environ.get("API_BASE_URL", "http://localhost:8000/api/v1")
        self.base_url = base_url
        self._client = httpx.AsyncClient()

    async def get_books(self):
        response = await self._client.get(f"{self.base_url}/book")
        response.raise_for_status()
        return response.json()

    async def get_book_by_id(self, book_id: int):
        response = await self._client.get(f"{self.base_url}/book/{book_id}")
        if response.status_code == 404:
            return None
        response.raise_for_status()
        return response.json()

    async def create_book(self, book_data: dict):
        response = await self._client.post(f"{self.base_url}/book", json=book_data)
        response.raise_for_status()
        return response.json()

    async def aclose(self):
        await self._client.aclose()
