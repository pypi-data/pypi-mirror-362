import re
import unittest
from zlxmcp.utils import *
from zlxmcp.utils.parse_sql import *


class TestUtils(unittest.TestCase):
    def test_utils(self):
        """"""
        print(camel_to_snake("legalPersonName"))


class TestStructSQL(unittest.TestCase):

    def test_parse_sql_1(self):
        """"""
        query = """
        SELECT id, name, COUNT(email) AS total_emails, MAX(age) AS max_age 
        FROM mydb.user 
        WHERE age > 25 AND status = 'active' 
        ORDER BY name DESC, created_at ASC
        LIMIT 10;
        """
        # select_match = re.search(r"select\s+(.*?)\s+from", query, re.DOTALL)
        # print(select_match)
        data = StructuredSQL(query).to_structured()
        print(data.model_dump_json(indent=4))

    def test_parse_sql_2(self):
        """"""
        query = """
        SELECT id, name, COUNT(email) AS total_emails, MAX(age) AS max_age 
        FROM mydb.user 
        WHERE age > 25 AND status = 'active' 
        ORDER BY name Desc
        """
        # select_match = re.search(r"select\s+(.*?)\s+from", query, re.DOTALL)
        # print(select_match)
        data = StructuredSQL(query).to_structured()
        print(data.model_dump_json(indent=4))

    def test_parse_sql_3(self):
        """"""
        query = """
        SELECT id, name, COUNT(email) AS total_emails, MAX(age) AS max_age 
        FROM user 
        WHERE age > 25 AND status = 'active' AND name = 'json' AND scope LIKE '%test%'
        ORDER BY name Desc
        """
        # select_match = re.search(r"select\s+(.*?)\s+from", query, re.DOTALL)
        # print(select_match)
        data = StructuredSQL(query).to_structured()
        print(data.model_dump_json(indent=4))
