import aiohttp
from typing import Dict
import traceback
from hero.util import log
from hero.tool import Tool
from hero.context import Context
from typing import TypedDict

tool = Tool()
class SearchParams(TypedDict):
    api_key: str

@tool.init("search", {
    "api_key": ""
}, params_type=SearchParams)
async def search(query: str, params: SearchParams, ctx: Context):
    """
    <desc>Search the web for information via search engine api</desc>
    <params>
        <query>The query to search for</query>
    </params>
    <example>
        {
            "tool": "search",
            "params": {
                "query": "What is the capital of France?"
            }
        }
    </example>
    """
    api_key = params["api_key"]
    base_url = "https://google.serper.dev/search"
    try:
        # 验证参数
        log.debug(f"params: {params.get('query')}")
        if not params or not params.get("query"):
            return {"status": "error", "message": "Missing required parameter: query"}

        headers = {
            "X-API-KEY": api_key,
            "Content-Type": "application/json",
        }


        data = {
            "q": query,
            "num": 10,
        }

        async with aiohttp.ClientSession() as session:
            async with session.post(
                base_url, headers=headers, json=data
            ) as response:
                if response.status != 200:
                    log.error(f"Search API error: {response.status}")
                    return {"status": "error", "message": "Search API error"}

                result = await response.json()

                message = "\n"
                count = 0
                for item in result["organic"]:
                    message += f"## {item['title']}\n"
                    message += f"- url: {item['link']}\n"
                    if item.get("snippet"):
                        message += f"- snippet: {item['snippet']}\n\n"
                    count += 1

                if count == 0:
                    return {"status": "error", "message": "No results found"}

                return {"status": "success", "message": message}

    except Exception as e:
        log.error(f"Error in search: {e}")
        log.error(traceback.format_exc())

        return {"status": "error", "message": str(e)}
