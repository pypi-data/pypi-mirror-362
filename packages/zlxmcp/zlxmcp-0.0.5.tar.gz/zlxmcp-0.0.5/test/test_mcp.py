import asyncio
import unittest
from zlxmcp.mcp.server import *
from dotenv import load_dotenv
load_dotenv()


class TestSQLMCP(unittest.TestCase):
    """"""
    def test_now_date(self):
        """"""
        data = now_date()
        print(data)

    def test_company_business_info(self):
        """"""
        for _type in ["工商基本信息", "主要人员", "年报信息", "股东信息"]:
            data = company_business_info("91330100MA2H2BME1C", _type=_type)
            print(_type)
            print(data)

    def test_list_tables(self):
        """"""
        tables = list_tables()
        print(tables)

    def test_list_columns(self):
        """"""
        columns = list_columns("ads_ai_ent_label")
        print(columns)

    def test_search_columns(self):
        """"""
        columns = search_columns("行业")
        print(columns)

    def test_read_sql(self):
        """"""
        query = "select company_name,credit_no from ads_ai_ent_label where eco_type='港澳台投资' limit 10"
        query = "SELECT * FROM ads_ai_ent_label WHERE establish_date BETWEEN '2025-04-22' AND '2025-05-22' AND business_scope LIKE '%征信%'"
        data = read_sql(query)
        print(data)

