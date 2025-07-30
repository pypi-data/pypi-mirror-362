from typing import List
import traceback
from hero.context import Context
from hero.util import log, function
from hero.tool import Tool

DOWNLOAD_TIMEOUT = 60000

tool = Tool()

@tool.init("download_files")
async def download_files(url_list: List[str], ctx: Context):
    """
    <desc>Download files from the internet</desc>
    <params>
        <url_list type="list">The url list to download, don't generate the url by yourself, just select from the **context**</url_list>
    </params>
    <example>
        {
            "tool": "download_files",
            "params": {
                "url_list":  ["https://example1.com/file1.pdf", "https://example2.com/file2.txt"]
            }
        }
    </example>
    """
    try:

        if not url_list:
            raise ValueError("url_list is required")

        message = ""

        for index, url in enumerate(url_list):
            file_path = function.download_file(url, ctx["dir"])

            if file_path:
                message += f"- download {url} success, save to {file_path}\n\n"
            else:
                message += f"- download {url} failed, content is empty\n\n"

        return {
            "status": "success",
            "message": message
        }
    except Exception as e:
        log.error(f"下载文件失败: {str(e)}")
        log.error(traceback.format_exc())
        return {
            "status": "error",
            "message": str(e)
        }
