import re
import os
import pandas as pd
from typing import Union


__all__ = [
    "project_cache_dir",
    "camel_to_snake",
    "snake_to_camel",
    "validate_response_data"
]


def project_cache_dir():
    """"""
    if os.getenv("ZLXMCP_CACHE_DIR"):
        path = os.getenv("ZLXMCP_CACHE_DIR")
    else:
        user_home = os.path.expanduser('~')
        path = os.path.join(user_home, "zlxmcp")
    return path


def camel_to_snake(string: str) -> str:
    """"""
    return re.sub(r'(?<!^)(?=[A-Z])', '_', string).lower()


def snake_to_camel(name):
    parts = name.split('_')
    return parts[0] + ''.join(word.capitalize() for word in parts[1:])


def validate_response_data(data: Union[dict, list, pd.DataFrame]) -> str:
    """"""
    if len(data) == 0:
        return "No data found."
    prefix = ""
    if len(data) > 50:
        prefix = f"Data too large with {len(data)} items, showing first 50 items:\n\n"

    if isinstance(data, list):
        data = str(data[:50])
    elif isinstance(data, pd.DataFrame):
        data = data.head(50).to_markdown(index=False)
    elif isinstance(data, dict):
        data = dict(list(data.items())[:50])

    data = f"{prefix}{data}"
    return data
