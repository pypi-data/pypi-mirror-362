import os
from typing import Dict, List, TypedDict
import traceback
from hero.model import Model
from hero.context import Context
from hero.util import log, function, stream
from hero.agent import Agent
from hero.tool import Tool

class ExtractKeyInfoFromFileParams(TypedDict):
    model: Model

tool = Tool()

@tool.init("extract_key_info_from_file", {
    "model": Model(),
}, params_type=ExtractKeyInfoFromFileParams)
async def extract_key_info_from_file(read_file_list: List[str], write_file: str, query: str, params: ExtractKeyInfoFromFileParams, ctx: Context):
    """
    <desc>Read context from file, carefully analyze, and extract key information related to the user's question. It will then write the information to the task history and an independent file.</desc>
    <params>
        <read_file_list type="list">Get the file name from context, can be one or more files. Do not generate filenames yourself, do not read non-text files (e.g., .pdf/.docx/.pptx/.xlsx/.csv/.json/.yaml/.py/.js/.ts/.html/.css/.ipynb), do not read images.</read_file_list>
        <write_file type="string">Write the extracted key information to a .md file</write_file>
        <query type="string">Query related to the user's question and file content</query>
    </params>
    <example>
        {
            "tool": "extract_key_info_from_file",
            "params": {
                "read_file_list": ["example1.md", "example2.txt"], 
                "write_file": "example.md", 
                "query": "What is the main idea of the document?"
            }
        }
    </example>
    """
    try:
        if not read_file_list or not write_file or not query:
            raise ValueError("Missing required parameters")

        # 读取文件内容
        for file_name in read_file_list:
            file_path = os.path.join(ctx.get("dir", ""), file_name)
            content = ""

            if os.path.exists(file_path):
                with open(file_path, "r", encoding="utf-8") as f:
                    content = f.read()

            parts = function.split_markdown(content)
            part_length = len(parts)
            log.info(f"Read {part_length} parts from {file_name}")

            # 使用模型提取关键信息
            extractor = Agent(name="extractor", model=params["model"], prompt=function.read_default_tool_prompt("extractor.md"))

            key_info = ""

            for index, part in enumerate(parts):
                log.info(
                    f"Processing part {index + 1} of {part_length} from {file_name}"
                )
                log.info(f"length: {len(part)}")
                
                # 使用模型提取关键信息
                user_message = str(function.read_user_message(ctx))
                log.info(f"user_message: {user_message}")

                message = f"File: {file_name} Total: {part_length}(Parts) Current: {index + 1}(Part)\n"
                message += f"Content of Part {index + 1} has been printed below, between <content> and </content>.\n"
                message += f"Please extract the key information from the **content** strictly following the **protocal**.\n"

                key_info += (
                    f'<key_info file_name="{file_name}" part="{index + 1}">\n\n'
                )

                # 使用模型提取关键信息
                async for token in extractor.chat(
                    message=message,
                    params={
                        "content": part,
                        "user_message": user_message,
                        "query": query,
                    },
                ):
                    stream.push(
                        component="message",
                        action=token.get("action", ""),
                        timestamp=function.timestamp(),
                        payload=token.get("payload", {}),
                    )

                    if token.get("action") == "content_line":
                        key_info += token.get("payload", {}).get("content")

                key_info += f"\n</key_info>\n"

            function.write_file(ctx.get("dir"), write_file, key_info)

        return {
            "status": "success",
            "message": f"Extract key information from {read_file_list} successfully. The key information has been written to {write_file}.",
        }
    
    except Exception as e:
        log.error(f"Error in extract_key_info_from_file: {e}")
        log.error(traceback.format_exc())
        return {"status": "error", "message": str(e)}