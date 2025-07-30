from zlxmcp.utils import FetchZLXData
from typing import Dict, List, Optional
from pprint import pprint


__all__ = [
    "APIBase",
]


class APIBase:
    """"""
    fetch: FetchZLXData
    data: Dict
    fetch_params: Dict

    def filter_list_api(self, path: str, columns: List[str], data_name: Optional[str] = None):
        """"""
        if data_name is None:
            data_name = path.split("/")[-1]

        data = self.fetch.fetch(path, self.fetch_params)
        list_data = data.result.get("list", [])
        data = []
        for item in list_data:
            data.append({k: item.get(k) for k in columns})
        self.data.update({data_name: data})
