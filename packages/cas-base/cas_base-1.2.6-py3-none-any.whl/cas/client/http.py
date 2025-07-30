import jwt
import aiohttp
from ..base import schemas


class ApiClient:

    def __init__(self, base_url: str):
        self.base_url: str = base_url
        self.token: schemas.LoginOut | None = None
        self.user: schemas.UserLoginOut | None = None
        self.ins: aiohttp.ClientSession | None = None

    async def raise_for_resp(self,resp):
        resp.raise_for_status()
        result = await resp.json()
        if result.get("code") != 200:
            raise Exception(result.get("message"))
        return result.get("data")

    async def init_session(self):
        if self.ins is None or self.ins.closed:
            self.ins = aiohttp.ClientSession()

    async def close(self):
        if self.ins and not self.ins.closed:
            await self.ins.close()

    async def __aenter__(self):
        await self.init_session()
        return self

    async def __aexit__(self, exc_type, exc, tb):
        await self.close()

    def make_headers(self, url: str, custom_headers: dict | None = None):
        headers = {}
        if self.token and not url.startswith("/open"):
            headers["Authorization"] = f"Bearer {self.token.access_token}"
        if custom_headers:
            headers.update(custom_headers)
        return headers

    async def login(self, username: str, password: str, client_id: str, grant_type: str):
        await self.init_session()
        data = {"username": username, "password": password, "client_id": client_id, "grant_type": grant_type}
        async with self.ins.post(f"{self.base_url}/open/login", data=data) as resp:
            resp_data = await self.raise_for_resp(resp)
        self.token = schemas.LoginOut.model_validate(resp_data)
        payload = jwt.decode(self.token.access_token, options={"verify_signature": False})
        self.user = schemas.UserLoginOut.model_validate_json(payload.get("signature_data"))
        return payload
    
    async def register(self, username: str, password: str, password_two: str):
        await self.init_session()
        data = {"username": username, "password": password, "password_two": password_two}
        async with self.ins.post(f"{self.base_url}/open/register", data=data) as resp:
            return await self.raise_for_resp(resp)
        
    async def recharge(self, username: str, password: str,card_number: str):
        await self.init_session()
        data = {"username": username, "password": password, "card_number": card_number}
        async with self.ins.post(f"{self.base_url}/biz/recharge/cards/recharge", data=data) as resp:
            return await self.raise_for_resp(resp)
        
    async def change_password(self, password_old: str, password: str, password_two: str):
        await self.init_session()
        data = {"password_old": password_old, "password": password, "password_two": password_two}
        async with self.ins.post(f"{self.base_url}/auth/user/change/password", data=data) as resp:
            return await self.raise_for_resp(resp)

    async def request(self, method: str, url: str, **kwargs):
        """
        统一请求方法，自动带上headers，Content-Type自适应，处理响应。
        """
        await self.init_session()
        full_url = url if url.startswith("http") else f"{self.base_url}{url}"
        headers = kwargs.pop("headers", {}) or {}
        # Content-Type自适应
        if "Content-Type" not in {k.title(): v for k, v in headers.items()}:
            if "json" in kwargs:
                headers["Content-Type"] = "application/json"
            elif "data" in kwargs and isinstance(kwargs["data"], dict):
                headers["Content-Type"] = "application/x-www-form-urlencoded"
        all_headers = self.make_headers(url, headers)
        async with self.ins.request(method, full_url, headers=all_headers, **kwargs) as resp:
            return await self.raise_for_resp(resp)

    async def get(self, url: str, **kwargs):
        """GET 请求封装"""
        return await self.request("GET", url, **kwargs)

    async def post(self, url: str, **kwargs):
        """POST 请求封装"""
        return await self.request("POST", url, **kwargs)

    async def put(self, url: str, **kwargs):
        """PUT 请求封装"""
        return await self.request("PUT", url, **kwargs)

    async def delete(self, url: str, **kwargs):
        """DELETE 请求封装"""
        return await self.request("DELETE", url, **kwargs)
    

