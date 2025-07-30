import os
import unittest
from dotenv import load_dotenv
from zlxmcp.utils import *
from zlxmcp.api import *
from pprint import pprint
load_dotenv()


class TestFetchData(unittest.TestCase):
    """"""
    def setUp(self):
        """"""
        # self.api_key = os.getenv('ZLX_TEST_API_KEY')
        # self.base_url = os.getenv('ZLX_TEST_BASE_URL')
        # self.api_key = os.getenv('ZLX_UAT_API_KEY')
        # self.base_url = os.getenv('ZLX_UAT_BASE_URL')
        self.api_key = os.getenv('ZLX_API_KEY')
        self.base_url = os.getenv('ZLX_BASE_URL')
        self.fetch = FetchZLXData(api_key=self.api_key, base_url=self.base_url)

    def test_search_company(self):
        """"""
        params = {'keyword': '同盾'}
        fetch_data = FetchZLXData(api_key=self.api_key, base_url=self.base_url)
        data = fetch_data.fetch(path="chayicha/search", params=params)
        print(data.to_frame().to_markdown())

    def test_fetch_base_info(self):
        params = {'enterpriseNo': '91330100MA2H2BME1C', 'company_name': '天道金科股份有限公司'}
        params = {'enterpriseNo': '91330106MAEH06D07G'}
        fetch_data = FetchZLXData(api_key=self.api_key, base_url=self.base_url)
        data = fetch_data.fetch(path="chayichaNewApi/baseInfo", params=params)
        print(data.to_frame())

    def test_person(self):
        params = {'enterprise_no': '91330100MA2H2BME1C'}
        data = self.fetch.fetch(path="chayicha/person", params=params)
        print(data.to_frame())

    def test_company_base(self):
        params = {'enterpriseNo': '91330100MA2H2BME1C'}
        data = self.fetch.fetch(path="chayichaNewApi/baseInfo", params=params)
        print(data.to_markdown())

    def test_sql(self):
        params = {'sql': r'select count(company_name) as "cnt" from ads_ai_ent_label'}
        fetch_data = FetchZLXData(api_key=self.api_key, base_url=self.base_url,)
        data = fetch_data.fetch(path="agent/executeSql", params=params)
        print(data.to_markdown())


class TestCompanyBaseInfo(unittest.TestCase):
    """"""

    def setUp(self):
        """"""
        self.fetch = FetchZLXData(
            api_key=os.getenv('ZLX_UAT_API_KEY'),
            base_url=os.getenv('ZLX_UAT_BASE_URL'),
        )

    def test_company_base(self):
        """"""
        company = CompanyBase(fetch=self.fetch, enterprise_no="91330100MA2H2BME1C")
        company.base_info()
        pprint(company.data)

    def test_company_person(self):
        """"""
        company = CompanyBase(fetch=self.fetch, enterprise_no="91330100MA2H2BME1C")
        company.company_person()
        pprint(company.data)

    def test_company_report(self):
        """"""
        company = CompanyBase(fetch=self.fetch, enterprise_no="91330110053687061Y")
        company.company_report()
        pprint(company.data)

    # def

    # def test_company_report(self):
    #     """"""
    #     company = CompanyBase(fetch=self.fetch, enterprise_no="91330110053687061Y")
    #     company.company_report()
    #     pprint(company.data)

    def test_company_share_holder(self):
        """"""
        company = CompanyBase(fetch=self.fetch, enterprise_no="91330100MA2H2BME1C", _type="股东信息")
        data = company()
        pprint(data)

    def test_company_abnormal(self):
        """"""
        company = CompanyBase(fetch=self.fetch, enterprise_no="91330100MA2H2BME1C")
        company.company_abnormal()
        pprint(company.data)

    def test_company_branch(self):
        """"""
        company = CompanyBase(fetch=self.fetch, enterprise_no="91330110053687061Y")
        company.company_branch()
        pprint(company.data)








