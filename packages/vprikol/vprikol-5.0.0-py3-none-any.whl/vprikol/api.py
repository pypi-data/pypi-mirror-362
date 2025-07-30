from typing import Optional, Dict, Any
import aiohttp


class VprikolAPIError(Exception):
    def __init__(self, status_code: int, error_data: Dict[str, Any]):
        self.status_code = status_code
        self.detail = error_data.get("detail", error_data)
        self.error_data = error_data
        super().__init__(f"API веселого прикола вернуло ошибку {self.status_code}: {self.detail}")


async def _request(session: aiohttp.ClientSession, method: str, url: str, params: Optional[Dict] = None, json: Optional[Dict] = None) -> Any:
    async with session.request(method, url, params=params, json=json) as response:
        if response.ok:
            if response.content_type == "application/json":
                return await response.json()
            return await response.read()

        error_data = await response.json()
        raise VprikolAPIError(status_code=response.status, error_data=error_data)


async def get_json(base_url: str, path: str, headers: Dict, params: Optional[Dict] = None) -> Any:
    async with aiohttp.ClientSession(headers=headers) as session:
        return await _request(session, "GET", f"{base_url}{path}", params=params)


async def post_json(base_url: str, path: str, headers: Dict, params: Optional[Dict] = None, body: Optional[Dict] = None) -> Any:
    async with aiohttp.ClientSession(headers=headers) as session:
        return await _request(session, "POST", f"{base_url}{path}", params=params, json=body)


async def delete_json(base_url: str, path: str, headers: Dict, params: Optional[Dict] = None) -> Any:
    async with aiohttp.ClientSession(headers=headers) as session:
        return await _request(session, "DELETE", f"{base_url}{path}", params=params)
