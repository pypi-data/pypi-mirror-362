from typing import Dict
from zlxmcp.utils import FetchZLXData, snake_to_camel
from zlxmcp.api.base import APIBase
from pprint import pprint


__all__ = [
    "CompanyOperation"
]


class CompanyOperation(APIBase):
    """"""

    def __init__(
            self,
            enterprise_no: str,
            fetch: FetchZLXData,
    ):
        """"""
        self.fetch = fetch
        self.enterprise_no = enterprise_no
        self.fetch_params = {
            "enterpriseNo": self.enterprise_no,
        }
        self.data = {}

    def __call__(self, **kwargs) -> Dict:
        """"""

    def appbk_info(self):
        """"""
        path = "chayichaNewApi/appbkInfo"
        data = self.fetch.fetch(path, self.fetch_params)
        print(data.result)



