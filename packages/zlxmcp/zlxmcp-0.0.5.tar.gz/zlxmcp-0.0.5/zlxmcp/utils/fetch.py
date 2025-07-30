import os
import json
import time
import requests
import pandas as pd
from urllib.parse import urljoin
from typing import Optional, Dict
from zlxmcp.types import ResponseData
from .utils import snake_to_camel, camel_to_snake
from .encrypt import sm2_encrypt, sm4_encrypt


__all__ = [
    "FetchZLXData"
]


class FetchZLXData:
    """"""
    api_key: str
    base_url: str
    public_key: str
    key: str
    tenant_id: str

    def __init__(
            self,
            api_key: Optional[str] = None,
            base_url: Optional[str] = None,
            key_name: Optional[str] = "ZLX_API_KEY",
            url_name: Optional[str] = "ZLX_BASE_URL",
            timeout: Optional[int] = 300,
    ):
        """"""
        self.key_name = key_name
        self.url_name = url_name
        self.timeout = timeout
        self.header = {"content-type": "application/json;charset=UTF-8"}
        self.set_user_config(api_key, base_url)

    def set_user_config(self, api_key: Optional[str] = None, base_url: Optional[str] = None):
        """"""
        if api_key:
            self.api_key = api_key
        elif os.getenv(self.key_name):
            self.api_key = os.getenv(self.key_name)
        else:
            raise ValueError("API_KEY is not set")

        self.tenant_id, self.key, self.public_key = self.api_key.split("-")
        self.header.update({"tenant-id": self.tenant_id})

        if base_url:
            self.base_url = base_url
        elif os.getenv(self.url_name):
            self.base_url = os.getenv(self.url_name)
        else:
            raise ValueError("BASE_URL is not set")

        if not self.base_url:
            raise ValueError("BASE_URL is not set")

    def fetch(self, path: str, params: Dict) -> ResponseData:
        """"""
        params = {snake_to_camel(key): val for key, val in params.items()}
        params.update({"flowId": str(int(time.time() * 1000))})
        params = json.dumps(params, ensure_ascii=False)
        result = {
            'key': f'04{sm2_encrypt(message=self.key, public_key=self.public_key)}',
            'content': sm4_encrypt(key=self.key, message=params)
        }
        url = urljoin(self.base_url, path)
        response = requests.post(url, json=result, headers=self.header, verify=False, timeout=self.timeout)
        if response.status_code == 200:
            json_data = response.json()
            if json_data.get('code') == 200 and json_data.get('result') is not None:
                data = {camel_to_snake(key): val for key, val in json_data.items()}
                response_data = ResponseData.model_validate(data)
            else:
                raise ValueError(f"{json_data}")
            return response_data
        else:
            raise ValueError(f"HTTP Error: res.status_code={response.status_code}, res.text={response.text}")
