import jwt
import requests
from ..base import schemas
from ..utils import raise_for_resp


class ApiClient:

    def __init__(self, base_url: str):
        self.base_url: str = base_url
        self.token: schemas.LoginOut | None = None
        self.user: schemas.UserLoginOut | None = None
        self.ins = requests

    def make_headers(self, url: str, custom_headers: dict | None = None):
        headers = {}
        if self.token and not url.startswith("/open"):
            headers["Authorization"] = f"Bearer {self.token.access_token}"
        if custom_headers:
            headers.update(custom_headers)
        return headers

    def login(self, username: str, password: str, client_id: str, grant_type: str):
        data = {"username": username, "password": password, "client_id": client_id, "grant_type": grant_type}
        resp = self.ins.post(f"{self.base_url}/open/login", data=data)
        self.token = schemas.LoginOut.model_validate(raise_for_resp(resp))
        payload = jwt.decode(self.token.access_token, options={"verify_signature": False})
        self.user = schemas.UserLoginOut.model_validate_json(payload.get("signature_data"))
        return payload
    
    def register(self, username: str, password: str, password_two: str):
        data = {"username": username, "password": password, "password_two": password_two}
        resp = self.ins.post(f"{self.base_url}/open/register", data=data)
        return raise_for_resp(resp)

    def request(self, method: str, url: str, **kwargs):
        """
        统一请求方法，自动带上headers，Content-Type自适应，处理响应。
        """
        full_url = url if url.startswith("http") else f"{self.base_url}{url}"
        headers = kwargs.pop("headers", {}) or {}
        # Content-Type自适应
        if "Content-Type" not in {k.title(): v for k, v in headers.items()}:
            if "json" in kwargs:
                headers["Content-Type"] = "application/json"
            elif "data" in kwargs and isinstance(kwargs["data"], dict):
                headers["Content-Type"] = "application/x-www-form-urlencoded"
        all_headers = self.make_headers(url,headers)
        resp = self.ins.request(method, full_url, headers=all_headers, **kwargs)
        return raise_for_resp(resp)

    def get(self, url: str, **kwargs):
        """GET 请求封装"""
        return self.request("GET", url, **kwargs)

    def post(self, url: str, **kwargs):
        """POST 请求封装"""
        return self.request("POST", url, **kwargs)

    def put(self, url: str, **kwargs):
        """PUT 请求封装"""
        return self.request("PUT", url, **kwargs)

    def delete(self, url: str, **kwargs):
        """DELETE 请求封装"""
        return self.request("DELETE", url, **kwargs)
