import re
import os
import click
import json
import markdown
import subprocess
from weasyprint import HTML
from openai import OpenAI
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import Any, Dict, Union, Literal, Annotated, Optional, Tuple, List
from pydantic import Field
from fastmcp import FastMCP
from zlxmcp.utils import validate_response_data, project_cache_dir


mcp = FastMCP("ZLX-MCP")
client = OpenAI(
    base_url=os.getenv("ZLXMCP_REPORT_LLM_URL"),
    api_key=os.getenv("ZLXMCP_REPORT_LLM_API_KEY"),
)


def completion(prompt: str) -> str:
    """"""
    model = 'Qwen/Qwen3-235B-A22B'
    extra_body = {"enable_thinking": False,}
    messages = [{'role': 'user', 'content': prompt}]
    response = client.chat.completions.create(
        model=model, messages=messages, extra_body=extra_body, stream=False,)
    return response.choices[0].message.content


@mcp.tool()
def generate_research_outline(
        name: Annotated[str, Field(description="研究报告的名称")],
        description: Annotated[str, Field(description="研究报告的描述")] = "",
) -> Tuple[str, Optional[dict]]:
    """生成研究报告的大纲

    Args:
        name: 研究报告的名称
        description: 研究报告的描述，可以是你对这篇文章的简要描述，也可以是文章的摘要

    Returns:
        研究报告的大纲
    """
    prompt = f"""你是一位专业的研究分析师，需要为《{name}》生成一份结构完整、逻辑严谨的研究报告大纲。\n\n{description}\n\n最终以json格式输出大纲内容，格式如下："""
    format = """
    ```json
    {
        'title': '报告标题',
        'sections': [
            {
                'title': '章节标题', 
                'outline': '章节内容概要',
            }, 
            ...
        ]
    }
    """
    prompt = prompt + format
    path = os.path.join(project_cache_dir(), "report")
    content = completion(prompt=prompt)
    try:
        # 从content中提取JSON部分
        json_start = content.find('```json') + 7
        json_end = content.find('```', json_start)
        json_str = content[json_start:json_end].strip()

        # 解析JSON
        outline_data = json.loads(json_str)

        # 将json存储至文件
        filename = f"{name}.json"
        file_path = os.path.join(path, filename)
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(outline_data, f, ensure_ascii=False, indent=4)

        message = f"大纲已生成并保存至: {filename}"
        return message, outline_data

    except Exception as e:
        message = f"解析大纲时出错: {str(e)}"
        return message, None


def gen_section(
        name: Annotated[str, Field(description="报告的名称")],
        section_name: Annotated[str, Field(description="报告章节的名称")],
        outline: Annotated[str, Field(description="章节纲要")],
        ret_type: Literal["dict", "str"] = "dict",
):
    """"""
    filename = f"{name}.json"
    path = os.path.join(project_cache_dir(), "report")
    file_path = os.path.join(path, filename)

    if not os.path.exists(file_path):
        return "报告文件Json不存在"

    with open(file_path, 'r', encoding='utf-8') as f:
        json_str = f.read()
    try:
        data = json.loads(json_str)
    except Exception as e:
        return f"报告文件Json解析失败: {str(e)}"

    sections = data.get("sections", [])
    sections_title = [f"章节：{s.get('title')}\n章节纲要: {s.get('outline')}" for s in sections]


    prompt = f"""你是一位专业的研究分析师，需要为《{name}》章节`{section_name}`生成章节正文。
    总体章节题目有：
    {"\n\n".join(sections_title)}
    
    你需要结合整体的大纲要求，撰写某一个章节的正文。
    
    现在，你需要写`{section_name}`章节的正文，内容要求如下：\n{outline}"""
    content = completion(prompt)
    if ret_type == "dict":
        return {section_name: content}
    else:
        return content


@mcp.tool()
def generate_section_content(
        name: Annotated[str, Field(description="报告的名称")],
        section_name: Annotated[str, Field(description="报告章节的名称")],
):
    """指定报告名称、章节名称，生成报告其中一个章节的内容

    Args:
        name: 报告的名称
        section_name: 报告章节的名称

    Returns:

    """
    filename = f"{name}.json"
    path = os.path.join(project_cache_dir(), "report")
    file_path = os.path.join(path, filename)

    if not os.path.exists(file_path):
        return "报告文件Json不存在"

    with open(file_path, 'r', encoding='utf-8') as f:
        json_str = f.read()
    try:
        data = json.loads(json_str)
    except Exception as e:
        return f"报告文件Json解析失败: {str(e)}"

    sections = data.get("sections", [])
    section = None
    for _section in sections:
        if _section["title"] == section_name:
            section = _section
            break
    if not section:
        return f"报告章节`{section_name}`不存在"
    section_content = gen_section(
        name=name,
        section_name=section.get("title"),
        outline=section.get("outline"),
        ret_type="str"
    )

    for _section in data.get("sections", []):
        if _section["title"] == section_name:
            _section["content"] = section_content
            break

    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(json.dumps(data, ensure_ascii=False, indent=4))

    return f"报告章节`{section_name}`生成成功", section_content


@mcp.tool()
def fix_section_content(
        name: Annotated[str, Field(description="报告的名称")],
        section_name: Annotated[str, Field(description="报告章节的名称")],
        description: Annotated[str, Field(description="修改要求")],
):
    """对指定的报告章节进行内容修改，指定报告名称、章节名称以及修改要求，生成修改后的报告章节内容

    Args:
        name: 报告的名称
        section_name: 报告章节的名称
        description: 修改要求

    Returns:

    """
    filename = f"{name}.json"
    path = os.path.join(project_cache_dir(), "report")
    file_path = os.path.join(path, filename)

    if not os.path.exists(file_path):
        return "报告文件Json不存在"

    with open(file_path, 'r', encoding='utf-8') as f:
        json_str = f.read()
    try:
        data = json.loads(json_str)
    except Exception as e:
        return f"报告文件Json解析失败: {str(e)}"

    sections = data.get("sections", [])
    section = None
    for _section in sections:
        if _section["title"] == section_name:
            section = _section
            break
    if not section:
        return f"报告章节`{section_name}`不存在"
    section_content = gen_section(
        name=name,
        section_name=section.get("title"),
        outline=description,
        ret_type="str",
    )

    for _section in data.get("sections", []):
        if _section["title"] == section_name:
            _section["content"] = section_content
            break

    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(json.dumps(data, ensure_ascii=False, indent=4))

    return f"报告章节`{section_name}`生成成功", section_content


@mcp.tool()
def generate_report(
        name: Annotated[str, Field(description="报告的名称")],
):
    """指定报告名称全部章节的内容

    Args:
        name: 报告的名称

    Returns:

    """
    filename = f"{name}.json"
    path = os.path.join(project_cache_dir(), "report")
    file_path = os.path.join(path, filename)

    if not os.path.exists(file_path):
        return "报告文件Json不存在"

    with open(file_path, 'r', encoding='utf-8') as f:
        json_str = f.read()
    try:
        data = json.loads(json_str)
    except Exception as e:
        return f"报告文件Json解析失败: {str(e)}"

    # 异步模式
    # sections = data.get("sections", [])
    # with ThreadPoolExecutor() as executor:
    #     futures = []
    #     for section in sections:
    #         section_name = section.get("section_name")
    #         outline = section.get("outline")
    #         futures.append(executor.submit(gen_section, name=name, section_name=section_name, outline=outline))
    #     contents = dict()
    #     for future in as_completed(futures):
    #         result = future.result()
    #         contents.update(result)
    # for section in data.get("sections", []):
    #     section["content"] = contents.get(section["section_name"], "")

    # 同步模式
    for section in data.get("sections", []):
        section["content"] = gen_section(
            name=name,
            section_name=section["title"],
            outline=section["outline"],
            ret_type="str",
        )
        print(section["title"], "生成成功")

        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)

    return "报告生成成功", data


def open_pdf(pdf_path):
    """使用系统默认应用打开 PDF 文件"""
    if not os.path.exists(pdf_path):
        raise FileNotFoundError(f"PDF 文件不存在: {pdf_path}")

    try:
        # Windows
        if os.name == 'nt':
            os.startfile(pdf_path)  # Windows 原生方法
        # macOS
        elif os.name == 'posix' and 'darwin' in os.uname().sysname.lower():
            subprocess.run(['open', pdf_path], check=True)
        # Linux/Unix
        else:
            subprocess.run(['xdg-open', pdf_path], check=True)
        print(f"已用默认应用打开: {pdf_path}")
    except Exception as e:
        print(f"打开 PDF 失败: {str(e)}")


@mcp.tool()
def render_pdf(
        name: str,
):
    """"""
    filename = f"{name}.json"
    path = os.path.join(project_cache_dir(), "report")
    file_path = os.path.join(path, filename)

    if not os.path.exists(file_path):
        return "报告文件Json不存在"

    with open(file_path, 'r', encoding='utf-8') as f:
        json_str = f.read()
    try:
        data = json.loads(json_str)
    except Exception as e:
        return f"报告文件Json解析失败: {str(e)}"

    content = [s["content"] for s in data.get("sections", [])]
    md_text = "\n\n".join(content)
    html = markdown.markdown(md_text)

    # 添加基本 CSS 样式（可选）
    full_html = f"""
        <html>
            <head>
                <style>
                    body {{ font-family: Arial, sans-serif; line-height: 1.6; }}
                    h1, h2, h3 {{ color: #333; }}
                    code {{ background: #f4f4f4; padding: 2px 5px; }}
                    pre {{ background: #f4f4f4; padding: 10px; overflow: auto; }}
                </style>
            </head>
            <body>{html}</body>
        </html>
        """

    # 渲染 HTML 为 PDF
    pdf_file_path = os.path.join(path, f"{name}.pdf")
    HTML(string=full_html).write_pdf(pdf_file_path)
    open_pdf(pdf_file_path)
    return pdf_file_path



@click.command()
@click.option("--host", "-h", default="127.0.0.1", type=str, required=False, help="host")
@click.option("--port", "-p", default=8000, type=int, required=False, help="port")
@click.option("--transport", "-t", default="stdio", type=str, required=False, help="transport")
def report_mcp_server(
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
    mcp.run(transport="streamable-http", port=9004)
