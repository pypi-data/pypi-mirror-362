import tqdm
import json
from pprint import pprint
import requests
import unittest
import pandas as pd
from sqlite3 import connect


def remove_mock(data):
    if isinstance(data, dict):
        keys_to_remove = []
        for key, value in data.items():
            remove_mock(value)
            if key == "mock":
                keys_to_remove.append(key)
        for key in keys_to_remove:
            del data[key]

    elif isinstance(data, list):
        for item in data:
            remove_mock(item)

    return data


class TestFetchSchema(unittest.TestCase):
    """"""
    def setUp(self) -> None:
        """"""
        self.headers = {
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36",
            "cookie": "cna=6i1rHT7DWjgCAXrq9gxbTdSE; Hm_lvt_45597bd006df64e6d360069f387e7872=1746191377; Hm_lpvt_45597bd006df64e6d360069f387e7872=1746191377; HMACCOUNT=331D29A569109DB5; _yapi_token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1aWQiOjQyOCwiaWF0IjoxNzQ2MjMyNzEzLCJleHAiOjE3NDY4Mzc1MTN9.isHykAv5Rpoe13nr-g0COx_m-zJ5vWzpUYwz43MRoe0; _yapi_uid=428",
        }
        self.conn = connect("schema.db")

    def test_fetch_domain(self):
        """"""
        base_url = "https://yapi.tdft.cn/api/project/get?id=618"
        response = requests.get(base_url, headers=self.headers)
        data = response.json().get("data").get("cat")
        df = pd.DataFrame(data)
        columns = ["_id", "name"]
        df = df[columns]
        df.columns = ["domain_id", "domain_name"]
        df.to_sql("domain", self.conn, if_exists="replace", index=False)

    def test_fetch_data(self):
        base_url = "https://yapi.tdft.cn/api/interface/list?page=1&limit=1000&project_id=618"
        response = requests.get(base_url, headers=self.headers)
        data = response.json().get("data").get("list")
        df_schema = pd.DataFrame(data)
        columns = ["_id", "title", "path", "catid"]
        df_schema = df_schema[columns]
        df_schema.path = df_schema.path.str[1:]
        df_schema = df_schema.rename(columns={"catid": "domain_id"})
        df_schema.to_sql("table_schema", index=False, con=self.conn, if_exists="replace")

    def test_fetch_schema(self):
        """"""
        df = pd.read_sql_query("SELECT * FROM table_schema", self.conn)
        data = []
        for _, row in tqdm.tqdm(df.iterrows(), total=df.shape[0]):
            try:
                _id = row["_id"]
                base_url = f"https://yapi.tdft.cn/api/interface/get?id={_id}"
                response = requests.get(base_url, headers=self.headers)
                req_body_other = json.loads(response.json().get("data").get("req_body_other"))
                res_body = json.loads(response.json().get("data").get("res_body"))
                request_properties = remove_mock(req_body_other.get("properties"))
                response_properties = remove_mock(res_body.get("properties").get("result").get("properties"))
                data.append({
                    "_id": _id,
                    "path": row["path"],
                    "title": row["title"],
                    "required": str(["enterpriseNo"]),
                    "request_properties": str(request_properties),
                    "response_properties": str(response_properties)
                })
            except Exception as e:
                print(row)
                print(f"Error: {e}")

        df = pd.DataFrame(data)
        df.to_sql("schema", self.conn, if_exists="replace", index=False)
        print()
