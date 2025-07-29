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

    def make_headers(self):
        headers = {"Content-Type": "application/json"}
        if self.token:
            headers["Authorization"] = f"Bearer {self.token.access_token}"
        return headers

    def login(self, username: str, password: str, client_id: str, grant_type: str):
        data = {"username": username, "password": password, "client_id": client_id, "grant_type": grant_type}
        resp = self.ins.post(f"{self.base_url}/open/login", data=data)
        self.token = schemas.LoginOut.model_validate(raise_for_resp(resp))
        payload = jwt.decode(self.token.access_token, options={"verify_signature": False})
        self.user = schemas.UserLoginOut.model_validate_json(payload.get("signature_data"))
