from . import server
import asyncio

def main():
    """包的主入口点。"""
    asyncio.run(server.main())