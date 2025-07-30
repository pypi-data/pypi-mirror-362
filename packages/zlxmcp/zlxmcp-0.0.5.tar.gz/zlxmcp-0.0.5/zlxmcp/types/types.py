import pandas as pd
from pydantic import BaseModel
from typing import List, Dict, Union


__all__ = [
    "ResponseData",
]


class ResponseData(BaseModel):
    """"""
    code: Union[int, str]
    message: str
    result: Union[Dict, List[Dict]]
    trace_id: str

    def to_frame(self) -> pd.DataFrame:
        if isinstance(self.result, dict):
            return pd.DataFrame([self.result])
        elif isinstance(self.result, list) and isinstance(self.result[0], dict):
            return pd.DataFrame(self.result)
        else:
            raise TypeError("result must be dict or list of dict")

    def to_markdown(self) -> str:
        return self.to_frame().to_markdown(index=False)

    def to_data(self) -> List[Dict]:
        return self.result
