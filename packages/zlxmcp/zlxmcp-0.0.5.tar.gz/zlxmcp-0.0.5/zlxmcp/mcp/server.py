import os
import re
import time
import click
import os.path
import webbrowser
import pandas as pd
from dotenv import load_dotenv
from pydantic import Field
from fastmcp import FastMCP
from typing import Any, List, Dict, Union, Annotated, Literal, Optional
from mcp.server.session import ServerSession
from zlxmcp.utils import FetchZLXData, validate_response_data, project_cache_dir
from zlxmcp.types import *
from zlxmcp.api import CompanyBase
from zlxmcp.charts import *


####################################################################################
# Temporary monkeypatch which avoids crashing when a POST message is received
# before a connection has been initialized, e.g: after a deployment.
# pylint: disable-next=protected-access
old__received_request = ServerSession._received_request


async def _received_request(self, *args, **kwargs):
    try:
        return await old__received_request(self, *args, **kwargs)
    except RuntimeError:
        pass


# pylint: disable-next=protected-access
ServerSession._received_request = _received_request
####################################################################################


load_dotenv()
mcp = FastMCP("ZLX-MCP")
fetch_data = FetchZLXData(
    api_key=os.getenv('ZLX_API_KEY'),
    base_url=os.getenv('ZLX_BASE_URL'),
)


@mcp.tool()
def get_tool_version() -> str:
    """获取当前工具的版本号"""
    from zlxmcp import __version__
    return __version__


@mcp.tool()
def now_date():
    """获取当前日期"""
    return time.strftime("%Y-%m-%d", time.localtime())


# @mcp.tool()
# def search_company(
#         keyword: Annotated[str, Field(description="company keyword")],
# ) -> str:
#     """ 根据企业关键词搜索企业企业编号（统一社会信用代码）
#     return:
#         - enterprise_no: 企业编号（统一社会信用代码）
#         - name: 企业名称
#         - base: 企业地址
#         - legal_person_name: 法人名称
#         - reg_statu: 企业状态
#     """
#     data = fetch_data.fetch(path="chayicha/search", params={"keyword": keyword})
#     df = data.to_frame()
#     columns = ["credit_code", "name", "base", "legal_person_name", "reg_status"]
#     df = df[columns]
#     df = df.rename(columns={"credit_code": "enterprise_no"})
#     return validate_response_data(df)


@mcp.tool()
def company_business_info(
        credit_no: Annotated[str, Field(description="企业编号（统一社会信用代码）")],
        _type: Annotated[Literal["工商基本信息", "主要人员", "年报信息", "股东信息"], Field(description="查询类型")],
) -> Union[Dict, str]:
    """根据企业编号查询工商信息

    Args:
        credit_no: 企业编号（统一社会信用代码）
        _type: 查询类型, 可选值: 工商基本信息, 主要人员, 年报信息, 股东信息
    """
    try:
        company = CompanyBase(fetch=fetch_data, enterprise_no=credit_no, _type=_type)
        data = company()
        return data
    except Exception as e:
        return f"Fetch Data Error: {str(e)}"


@mcp.tool()
def list_tables():
    """ List all tables in the database. """
    data = {
        "ads_ai_ent_label": "企业标签大宽表，包含诸多企业基本信息。"
    }
    return validate_response_data(data)


@mcp.tool()
def list_columns(
        table_name: Annotated[str, Field(description="table name", examples=["ads_ai_ent_label"])],
):
    """ Given a table name, list all columns in the table."""
    return TABLE_SCHEMA.get(table_name.lower(), [])


@mcp.tool()
def search_columns(
        pattern: Annotated[str, Field(description="Pattern to search for in column names")],
):
    """Find columns by name or columns comment, return table name"""
    df_columns = pd.DataFrame(TABLE_SCHEMA.get("ads_ai_ent_label", []))
    data = df_columns.loc[
        df_columns["column_name"].str.contains(pattern) | df_columns["column_comment"].str.contains(pattern),
        ["column_name", "column_comment"]
    ]
    if len(data) > 0:
        return validate_response_data(data)
    else:
        return f"not found columns about {pattern}"


@mcp.tool()
def read_sql(
        query: Annotated[str, Field(description="SQL查询语句")],
) -> str:
    """执行SQL查询语句"""
    try:
        data = fetch_data.fetch(path="agent/executeSql", params={'sql': query})
    except Exception as e:
        return str(e)
    if len(data.result) > 0:
        return validate_response_data(data.to_frame())
    else:
        return f"not found data about {query}"


@mcp.tool()
def base_charts(
        chart_type: Annotated[Literal["Line", "Bar", "Pie", "Radar"], Field(description="图表类型")],
        ticks: Annotated[List, Field(description="X轴刻度名称，或饼图、雷达图标签")],
        data: Annotated[Dict, Field(description="数据")],
        title: Annotated[str, Field(description="标题")],
        sub_title: Annotated[Optional[str], Field(description="副标题")] = None,
) -> str:
    """

    Args:
        chart_type: 图表类型
        ticks:
            Line/Bar: X轴刻度名称
            Pie/Radar: 饼图、雷达图标签
        data: 基础图表数据格式：{"最高气温": [10, 15, 30], "最低气温": [4, 5, 6], ...}
        title: 标题
        sub_title: 副标题

    Returns:

    """
    try:
        base_path = project_cache_dir()
        chart_path = os.path.join(base_path, "charts")
        chart_file = os.path.join(chart_path, f"{title}.html")
        if not os.path.exists(chart_path):
            os.makedirs(chart_path)
        c = base_chart(
            chart_type=chart_type,
            x_ticks=ticks, data=data,
            title=title, sub_title=sub_title,
            width=1200, height=600,
        )
        c.render(path=chart_file)
        webbrowser.open(chart_file)
        return chart_file
    except Exception as e:
        return f"Error: {e}"

@mcp.tool()
def map_charts(
        data: Annotated[List, Field(description="数据")],
        title: Annotated[str, Field(description="标题")],
        map_type: Annotated[str, Field(description="地图地区")] = "china",
        sub_title: Annotated[Optional[str], Field(description="副标题")] = None,
) -> str:
    """

    Args:
        data: 地图数据格式：[["河北省", 1.2], ["河南省": 1.3], ["浙江省": 2.5], ["广东省": 4.5], ...]
        title: 标题
        map_type: 地图地区，如，["china", "浙江", "北京", ...]
        sub_title: 副标题

    Returns:

    """
    map_type = re.sub(r"省|市", "", map_type)

    try:
        base_path = project_cache_dir()
        chart_path = os.path.join(base_path, "charts")
        chart_file = os.path.join(chart_path, f"{title}.html")
        if not os.path.exists(chart_path):
            os.makedirs(chart_path)
        c = map_chart(
            data=data,
            title=title,
            map_type=map_type,
            sub_title=sub_title,
            width=1200,
            height=600,
        )
        c.render(path=chart_file)
        webbrowser.open(chart_file)
        return chart_file
    except Exception as e:
        return f"Error: {e}"


@click.command()
@click.option("--host", "-h", default="127.0.0.1", type=str, required=False, help="host")
@click.option("--port", "-p", default=8000, type=int, required=False, help="port")
@click.option("--transport", "-t", default="stdio", type=str, required=False, help="transport")
def zlx_mcp_server(
        host: str = None,
        port: Union[int, str] = None,
        transport: Literal["stdio", "sse"] = "stdio",
) -> None:
    """"""
    if transport == "sse":
        mcp.run(transport=transport, port=port, host=host)
    else:
        mcp.run(transport=transport)


if __name__ == "__main__":
    mcp.run(transport="sse", port=9003)
