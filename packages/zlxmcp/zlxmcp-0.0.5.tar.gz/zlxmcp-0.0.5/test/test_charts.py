import unittest
from zlxmcp.charts import map_chart


class TestCharts(unittest.TestCase):
    """"""
    def test_map(self):
        """"""
        params = {
            "data": [
                ["中泰街道", 142413],
                # [
                #     "东城区",
                #     142413
                # ],
                # [
                #     "西城区",
                #     130492
                # ],
            ],
            "title": "浙江省各市企业数据量分布",
            "map_type": "余杭"
        }
        c = map_chart(**params)
        c.render("test.html")