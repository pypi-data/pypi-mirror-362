import os
from typing import Any, Dict, List, TypedDict
import traceback
from hero.context import Context
from hero.util import log, function
from hero.tool import Tool

tool = Tool()

class ReadFileParams(TypedDict):
    split_file_limit: int

@tool.init("read_file", {
    "split_file_limit": 50000,
}, ReadFileParams)
async def read_file(read_file_list: List[str], params: ReadFileParams, ctx: Context):
    """
    <desc>Read a file</desc>
    <params>
        <read_file_list type="list">The file list to read, you should read multiple files to get the complete context and increase the efficiency, only support **TEXT and IMAGE FILES** like: txt, json, csv, md, py, js, html, png, jpg, jpeg, gif, etc.</read_file_list>
    </params>
    <example>
        {
            "tool": "read_file",
            "params": {
                "read_file_list": ["example.txt", "example.jpg", "example.py"]
            }
        }
    </example>
    """
    try:
        if not read_file_list:
            raise ValueError("Missing required parameter: read_file_list")

        # 拼接成绝对路径
        dir = ctx.get("dir")
        name = ctx.get("name")
        index = ctx.get("index")

        context = ""

        images = []
        # 验证文件列表
        for file in read_file_list:
            file_path = os.path.join(dir or "", file)
            if not os.path.exists(file_path):
                raise FileNotFoundError(f"File not found: {file}")

            if file.endswith((".png", ".jpg", ".jpeg", ".gif")):
                images.append(function.image_to_base64_url(file_path))
            else:
                context += f'<read_file name="{file}">\n'
                # 读取文件内容
                with open(file_path, "r", encoding="utf-8") as file:
                    context += file.read() + "\n"
                    if len(context) > params["split_file_limit"]:
                        raise Exception(
                            "The file content is too long, please use `extract_key_info_from_file` tool to extract the key information."
                        )
                context += f"</read_file>\n\n"

        return {
            "status": "success",
            "message": "Add files content to the **context**",
            "additional_context": context,
            "additional_images": images,
        }
    except Exception as e:
        log.error(f"Read file error: {e}")
        log.error(traceback.format_exc())
        return {"status": "error", "message": str(e)}