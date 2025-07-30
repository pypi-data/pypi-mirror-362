from typing import Dict, Literal, Callable
from zlxmcp.utils import FetchZLXData, snake_to_camel
from zlxmcp.api.base import APIBase
from pprint import pprint


__all__ = [
    "CompanyBase"
]


class CompanyBase(APIBase):
    """"""

    def __init__(
            self,
            enterprise_no: str,
            fetch: FetchZLXData,
            _type: Literal["工商基本信息", "主要人员", "年报信息", "股东信息"],
    ):
        """"""
        self.fetch = fetch
        self.enterprise_no = enterprise_no
        self.fetch_params = {
            "enterpriseNo": self.enterprise_no,
        }
        self.data = {}
        self._type = _type

    def __call__(self, **kwargs) -> Dict:
        """"""
        self.data_mapping()()
        return self.data

    def data_mapping(self) -> Callable:
        """"""
        mapping = {
            "工商基本信息": self.base_info,
            "主要人员": self.company_person,
            "年报信息": self.company_report,
            "股东信息": self.company_share_holder,
        }
        return mapping.get(self._type)

    def base_info(self, ):
        """"""
        columns = [
            'actual_capital', 'approved_time', 'base', 'business_scope',
            'company_org_type', 'credit_code', 'en_name', 'from_time',
            'legal_person_caption', 'legal_person_name', 'name', 'reg_capital',
            'reg_institute', 'reg_location', 'reg_status',]

        path = "chayichaNewApi/baseInfo"
        data = self.fetch.fetch(path, self.fetch_params)
        _data = {key: data.result[snake_to_camel(key)] for key in columns}
        self.data.update(_data)

    def company_person(self, ):
        """"""
        path = "chayichaNewApi/person"
        columns = ["name", "typeJoin", "isHistory"]
        self.filter_list_api(columns=columns, path=path, data_name="persons")

    def company_report(self):
        """"""
        path = "chayichaNewApi/report"
        columns = [
            "businessScope", "companyHolding", "email", "employeeNum",
            "manageState", "postalAddress", "stockSell", "postcode",
        ]
        self.filter_list_api(columns=columns, path=path, data_name="reports")

    def company_share_holder(self):
        """"""
        path = "chayichaNewApi/shareHolder"
        columns = [
            "stockName", "stockType", "stockCapital", "isHistory",
        ]
        self.filter_list_api(columns=columns, path=path, data_name="shareHolder")

    def company_branch(self):
        """todo: 待完善"""
        path = "chayichaNewApi/branch"
        data = self.fetch.fetch(path, self.fetch_params)

    def company_abnormal(self):
        """todo: 待完善"""
        path = "chayichaNewApi/abnormal"
        data = self.fetch.fetch(path, self.fetch_params)
