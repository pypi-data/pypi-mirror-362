import re
import json
from pydantic import BaseModel, Field
from typing import Dict, List, Optional


__all__ = [
    "StructuredSQL"
]


class SelectSchema(BaseModel):
    """"""
    expression: str
    alias: Optional[str] = None


class StructuredSQLSchema(BaseModel):
    """"""
    select: List[SelectSchema]
    database: Optional[str]
    table: Optional[str]
    where: List[str]
    order: Optional[List]
    limit: Optional[int]


class StructuredSQL:
    """"""
    select: List[SelectSchema]
    database: Optional[str]
    table: Optional[str]
    where: List[str]
    order: Optional[List]
    limit: Optional[int]

    def __init__(self, query, query_schema: Optional[Dict] = None,):
        """"""
        self.query = query.strip().lower()
        self.parse_select()
        self.parse_db_table()
        self.parse_where()
        self.parse_order()
        self.parse_limit()

    def parse_select(self, ):
        """"""
        # 提取 SELECT 字段（包含 AS 别名 和 聚合函数）
        select_match = re.search(r"select\s+(.*?)\s+from", self.query, re.DOTALL)
        self.select = []
        if select_match:
            columns = select_match.group(1).strip().split(',')
            for col in columns:
                col = col.strip()
                as_match = re.search(r"(.+)\s+as\s+(\w+)", col, re.IGNORECASE)
                if as_match:
                    expr = as_match.group(1).strip()
                    alias = as_match.group(2).strip()
                    self.select.append(SelectSchema(expression=expr, alias=alias))
                else:
                    self.select.append(SelectSchema(expression=col))

    def parse_db_table(self):
        """"""
        from_match = re.search(r"from\s+(`?[\w\d_]+`?(?:\.`?[\w\d_]+`?)?)", self.query, re.IGNORECASE)
        self.database = None
        self.table = None
        if from_match:
            full_table = from_match.group(1).replace('`', '')
            if '.' in full_table:
                parts = full_table.split('.')
                self.database = parts[0]
                self.table = parts[1]
            else:
                self.table = full_table

    def parse_where(self):
        """"""
        where_match = re.search(r"where\s+(.*?)(?:group by|order by|limit|$)", self.query, re.DOTALL)
        self.where = []
        if where_match:
            where_str = where_match.group(1).strip()
            self.where = [
                cond.strip() for cond in re.split(r"\s+and\s+|\s+or\s+", where_str)
                if cond.strip()
            ]

    def parse_order(self):
        """"""
        order_match = re.search(r"group by\s+.*$|order by\s+(.*?)(?:limit|$)", self.query, re.DOTALL)
        self.order = []
        if order_match:
            ob_str = order_match.group(1).strip()
            for part in ob_str.split(','):
                part = part.strip()
                if not part:
                    continue
                dir_match = re.search(r"(\S+)\s+(asc|desc)", part, re.IGNORECASE)
                if dir_match:
                    self.order.append({
                        "column": dir_match.group(1),
                        "direction": dir_match.group(2).upper()
                    })
                else:
                    self.order.append({
                        "column": part,
                        "direction": "ASC"
                    })

    def parse_limit(self):
        """"""
        limit_match = re.search(r"limit\s+(\d+)", self.query)
        self.limit = int(limit_match.group(1)) if limit_match else None

    def to_structured(self) -> StructuredSQLSchema:
        """"""
        return StructuredSQLSchema(
            select=self.select,
            database=self.database,
            table=self.table,
            where=self.where,
            order=self.order,
            limit=self.limit
        )
