import os
from typing import Any, Coroutine
import asyncio
import httpx
from mcp.server.models import InitializationOptions
import mcp.types as types
from mcp.server import NotificationOptions, Server
import mcp.server.stdio
import logging
logging.basicConfig(level=logging.INFO)

# Create an MCP server
server = Server("mcp-jamie-test2")

# api_key = os.getenv("API_KEY")
# if not api_key:
#     raise ValueError("API_KEY environment variable is not set")
api_key = "Basic NThxZnY1cXFRaHc2ZDhQQ0RabENDU0d6Y044amR2d1Y="

@server.list_tools()
async def handle_list_tools() -> list[types.Tool]:
    """
    列出可用的工具。
    每个工具使用 JSON Schema 验证来指定其参数。
    """
    return [
        types.Tool(
            name="add",
            description="Add two numbers together123",
            inputSchema={
                "type": "object",
                "properties": {
                    "a": {"type": "number", "description": "The first number"},
                    "b": {"type": "number", "description": "The second number"}
                },
                "required": ["a"]
            }
        ),
        types.Tool(
            name="text_processing",
            description="- 支持转化英文单词的大小写 \n - 支持统计英文单词的数量",
            inputSchema={
                "type": "object",
                "properties": {
                    "text": {"type": "string", "description": "等待转化的英文单词"},
                    "operation": {"type": "string", "description": "转换类型，可选upper/lower/count"}
                },
                "required": ["text"]
            }
        ),
        types.Tool(
            name="img_processing",
            description="处理图片请求",
            inputSchema={
                "type": "object",
                "properties": {
                    "source": {
                        "type": "object",
                        "properties": {
                            "url": {
                                "type": "string",
                                "description": "图片地址"
                            }
                        },
                        "description": "图片参数，object类型",
                        "required": ["url"]
                    }
                },
                "required": ["source"]
            }
        ),
        types.Tool(
            name="params_test",
            description="保存用户的个人信息",
            inputSchema={
                "type": "object",
                "properties": {
                    "name": {"type": "string", "description": "用户名"},
                    "age": {"type": "int", "description": "年龄"},
                    "is_married": {"type": "bool", "description": "是否已婚"},
                    "score": {"type": "float", "description": "成绩"},
                    "interests": {"type": "array", "items": {"type": "string"}, "description": "兴趣爱好"},
                    "remarks": {"type": "object", "description": "备注"}
                },
                "required": ["name", "age"]
            }
        )
    ]

async def add(a: int, b: int = 0) -> dict:
    logging.info(f"------Adding {a} and {b}")
    """Add two numbers together."""

    return {"result": a + b }


async def text_processing(text: str, operation: str = "count") ->  str | None:
    """文本处理工具，支持英文文本的大小写转换和单词统计"""
    # 输入验证
    if not isinstance(text, str):
        raise TypeError("Input text must be a string")
    if not text.strip():
        raise ValueError("Input text cannot be empty")

    # 操作验证
    operation = operation.lower().strip()
    valid_operations = {"upper", "lower", "count"}
    if operation not in valid_operations:
        raise ValueError(f"Invalid operation. Must be one of: {valid_operations}")

    # 执行操作
    if operation == "upper":
        return text.upper()
    elif operation == "lower":
        return text.lower()
    elif operation == "count":
        # 按空格分割并过滤空字符串
        words = [word for word in text.split() if word]
        return str(len(words))


async def img_processing(source: dict) -> str:
    """图片压缩工具"""
    if not source or not isinstance(source, dict):
        raise ValueError("Invalid source parameter, expected non-empty dict")

    url = "https://api.tinify.com/shrink"
    headers = {
        "Authorization": api_key,
        "Content-Type": "application/json",
    }
    data = {"source": source}

    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.post(url, headers=headers, json=data)
            response.raise_for_status()  # 自动检查HTTP错误状态码
            return response.json()

    except httpx.HTTPStatusError as e:
        error_msg = f"API request failed with status {e.response.status_code} | error message:{e.response.json()}"
        raise httpx.HTTPStatusError(error_msg, request=e.request, response=e.response) from e
    except httpx.RequestError as e:
        raise Exception(f"Request failed: {str(e)}") from e
    except ValueError as e:
        raise ValueError(f"Invalid JSON response: {str(e)}") from e


async def params_test(name: str, age: int, is_married: bool = False, score: float = 0, interests=None, remarks=None) -> dict:
    """保存用户的个人信息"""
    if remarks is None:
        remarks = {}
    if interests is None:
        interests = []
    return {
        "message": "个人信息保存成功",
        "name": {
            "value": name,
            "type": type(name).__name__
        },
        "age": {
            "value": age,
            "type": type(age).__name__,
        },
        "is_married": {
            "value": is_married,
            "type": type(is_married).__name__
        },
        "score": {
            "value": score,
            "type": type(score).__name__,
        },
        "interests": {
            "value": interests,
            "type": type(interests).__name__,
        },
        "remarks": {
            "value": remarks,
            "type": type(remarks).__name__,
        }
    }


@server.call_tool()
async def handle_call_tool(
    name: str, arguments: dict | None
) -> list[types.TextContent | types.ImageContent | types.EmbeddedResource]:
    """
    处理工具执行请求。
    """
    if not arguments:
        raise ValueError("缺少参数")
    if name == "add":
        result = await add(**arguments)
        return [types.TextContent(type="text", text=f"{result}")]
    if name == "text_processing":
        result = await text_processing(**arguments)
        return [types.TextContent(type="text", text=f"{result}")]
    if name == "img_processing":
        result = await img_processing(**arguments)
        return [types.TextContent(type="text", text=f"{result}")]
    if name == "params_test":
        result = await params_test(**arguments)
        return [types.TextContent(type="text", text=f"{result}")]
    else:
        raise NotImplementedError(f"工具 {name} 不支持")



async def main():
    # Run the server using stdin/stdout streams
    async with mcp.server.stdio.stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            InitializationOptions(
                server_name="mcp-jamie-test3",
                server_version="2.0.1",
                capabilities=server.get_capabilities(
                    notification_options=NotificationOptions(),
                    experimental_capabilities={},
                ),
            ),
        )


if __name__ == "__main__":
    asyncio.run(main())