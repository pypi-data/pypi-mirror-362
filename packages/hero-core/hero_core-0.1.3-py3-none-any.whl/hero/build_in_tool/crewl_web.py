from typing import  List, TypedDict
import traceback
from hero.context import Context
from hero.util import log, function, stream, Crewler
import os
import asyncio
import random
from hero.tool import Tool
from hero.model import Model

SCRAPE_CONCURRENT_LIMIT = 5
REQUEST_TIMEOUT = 60000

class CrewlWebParams(TypedDict):
    model: Model
    scrape_concurrent_limit: int
    request_timeout: int

tool = Tool()

@tool.init("crewl_web", {
    "model": Model(),
    "scrape_concurrent_limit": 5,
    "request_timeout": 60000,
},params_type=CrewlWebParams)
async def crewl_web(url_list: List[str], write_file: str, query: str, params: CrewlWebParams, ctx: Context):
    """
    <desc>Scrape content from multiple web pages, analyze carefully, and extract key information related to the user's question. It will then write the information to the task history and an independent file.</desc>
    <params>
        <url_list type="list">Get from context, one or more links</url_list>
        <write_file type="string">Write the extracted key information to a .md file</write_file>
        <query type="string">Query related to the user's question and web page content</query>
    </params>
    <example>
        {
            "tool": "crewl_web",
            "params": {
                "url_list": ["https://example1.com", "https://example2.com"], "write_file": "example.md", "query": "Today's weather in Beijing"
            }
        }
    </example>
    """
    try:
        if not url_list:
            raise ValueError("url_list is required")

        if not write_file:
            raise ValueError("write_file is required")

        if not query:
            raise ValueError("query is required")

        dir = ctx.get("dir", "")

        # 创建一个简单的同步回调，将更新放入列表
        status_updates = []

        def status_callback(data):
            status_updates.append(data)

        # 记录成功抓取的页面索引
        successful_web = []
        successful_file = []
        error_url = []

        # 创建任务列表和信号量限制并发
        scrape_semaphore = asyncio.Semaphore(SCRAPE_CONCURRENT_LIMIT)

        async def process_url_with_semaphore(url, index):
            async with scrape_semaphore:
                # 延迟启动避免资源争用
                await asyncio.sleep((index % 5) * 1.0)

                # 创建一个专用于此URL的状态更新列表
                url_status_updates = []

                # 创建一个异步回调适配器
                async def status_update_callback(data):
                    # 保存状态更新
                    url_status_updates.append(data)
                    # 同时发送到总状态列表，方便后续处理
                    status_callback(data)

                    # 实时反馈到日志
                    if data.get("content", {}).get("progress"):
                        progress = data["content"]["progress"]
                        log_text = f"- URL {index} Progress: {progress}"
                        log.info(log_text)

                    # 立即返回以不阻塞process_url函数
                    return

                try:
                    # 直接调用异步函数
                    result = await process_url(
                        url, index, dir, write_file, status_update_callback
                    )

                    if result["status"] == "success" and result["type"] == "web":
                        successful_web.append(result)

                    if result["status"] == "success" and result["type"] == "file":
                        successful_file.append(result)

                    if result["status"] == "error":
                        error_url.append(result)

                    return result
                except Exception as e:
                    log.error(f"Error processing URL at index {index}: {e}")
                    error_data = {
                        "index": index,
                        "message": str(e),
                        "status": "error",
                    }
                    # 记录错误日志
                    log_text = f"- URL {index} failed: {str(e)}"
                    log.info(log_text)
                    return error_data

        # 创建所有任务
        tasks = []
        for i, url in enumerate(url_list):
            url = ensure_protocol(url)
            tasks.append(process_url_with_semaphore(url, i + 1))

        # 使用as_completed来实现并发处理，同时尽快处理完成的任务
        for task in asyncio.as_completed(tasks):
            try:
                result = await task

                # 发送积累的状态更新
                for update in status_updates:
                    stream.push(
                        component="message",
                        action="web_crewl_update",
                        timestamp=function.timestamp(),
                        payload=update,
                    )

                # 清空状态更新列表
                status_updates.clear()

                # 添加日志反馈
                if result.get("content", {}).get("progress"):
                    index = result["content"]["index"]
                    progress = result["content"]["progress"]
                    log_text = f"- URL {index} Progress: {progress}"
                    log.info(log_text)

            except Exception as e:
                log.error(f"Task execution error: {e}")
                log.error(traceback.format_exc())

        # 合并所有内容到一个文件
        if successful_web:
            combined_content = ""
            for result in successful_web:
                if not dir:
                    raise ValueError("dir is required")
                content_file_path = os.path.join(
                    dir, f"__{write_file}_{result['index']}.html"
                )
                try:
                    with open(content_file_path, "r", encoding="utf-8") as f:
                        content = f.read()
                    combined_content += f"{content}---"
                except Exception as e:
                    log.error(
                        f"Error reading content file {content_file_path}: {e}"
                    )

            # 写入合并后的内容
            with open(os.path.join(dir, write_file), "w", encoding="utf-8") as f:
                f.write(combined_content)

            # 发送日志
            log_text = f"- Saved combined content to: {write_file}"
            log.info(log_text)

        message = ""
        if successful_web:
            message += f"- Crawl success: {[result['url'] for result in successful_web]}, and save the content to {write_file}\n"
        if successful_file:
            for result in successful_file:
                message += f"- Download '{result['file_path']}' success from '{result['url']}'\n"
        if error_url:
            message += (
                f"- Crawl failed: '{[result['url'] for result in error_url]}'\n"
            )

        return {
            "status": "success",
            "message": message,
        }
    except Exception as e:
        log.error(f"Error: {str(e)}")
        log.error(traceback.format_exc())
        return {
            "status": "error",
            "message": f"Error: {str(e)}",
        }

async def process_url(
        url: str,
        index: int,
        dir: str,
        write_file: str,
        status_callback=None,
    ):
    try:
        stream.push(
            component="message",
            action="web_crewl_update",
            timestamp=function.timestamp(),
            payload={
                "index": index,
                "url": url,
                "status": "running",
                "progress": "Start getting content",
            },
        )

        # 检查是否是可下载的链接
        if function.is_downloadable(url) and (
            file_path := function.download_file(url, dir)
        ):
            try:
                if file_path:
                    stream.push(
                        component="message",
                        action="web_crewl_update",
                        timestamp=function.timestamp(),
                        payload={
                            "index": index,
                            "url": url,
                            "status": "success",
                            "progress": "Download success",
                            "file_path": file_path,
                        },
                    )
                else:
                    raise Exception("下载失败")

                return {
                    "index": index,
                    "url": url,
                    "type": "file",
                    "status": "success",
                    "file_path": file_path,
                }

            except Exception as e:
                log.error(f"Download failed: {str(e)}")
                log.error(traceback.format_exc())

                # 发送错误状态
                stream.push(
                    component="message",
                    action="web_crewl_update",
                    timestamp=function.timestamp(),
                    payload={
                        "index": index,
                        "url": url,
                        "status": "error",
                        "progress": f"Download failed: {str(e)}",
                    },
                )
                raise Exception(f"Download failed: {str(e)}")
        else:
            # 处理普通网页
            try:
                # 尝试爬取内容，最多重试3次
                retry_count = 0
                max_retries = 3
                last_error = None

                # 为这个URL请求创建一个独立的WebScraper实例
                thread_scraper = Crewler(dir)

                while retry_count < max_retries:
                    try:
                        # 添加随机延时，避免多个协程同时请求
                        # 第一次尝试使用索引作为基础延时，确保请求错开启动
                        # 后续重试使用更长的随机延时
                        if retry_count == 0:
                            delay = (index % 5) * 1.5 + random.uniform(0.5, 1.5)
                            log.info(
                                f"URL {index}: {url} - First try, wait {delay:.2f} seconds"
                            )
                        else:
                            delay = retry_count * 2 + random.uniform(1.0, 3.0)
                            log.info(
                                f"URL {index}: {url} - The {retry_count+1}/{max_retries} retry, wait {delay:.2f} seconds"
                            )

                        await asyncio.sleep(delay)

                        stream.push(
                            component="message",
                            action="web_crewl_update",
                            timestamp=function.timestamp(),
                            payload={
                                "index": index,
                                "url": url,
                                "status": "running",
                                "progress": f"Getting content (try {retry_count+1}/{max_retries})",
                            },
                        )

                        # 获取内容 - 直接调用异步方法
                        content = await thread_scraper.scrape_url(
                            url, index, dir, REQUEST_TIMEOUT
                        )

                        # 爬取成功，保存内容
                        file_path = os.path.join(
                            dir, f"__{write_file}_{index}.html"
                        )

                        # 使用独立的文件写入器来避免资源竞争
                        with open(file_path, "w", encoding="utf-8") as f:
                            f.write(content)

                        # 清理资源
                        await thread_scraper.close()

                        stream.push(
                            component="message",
                            action="web_crewl_update",
                            timestamp=function.timestamp(),
                            payload={
                                "index": index,
                                "url": url,
                                "status": "success",
                                "progress": "Completed saving, processing success",
                                "screenshot": f"/screenshot_{index}.png",
                            },
                        )

                        # 返回成功结果
                        return {
                            "index": index,
                            "url": url,
                            "status": "success",
                            "screenshot": f"/screenshot_{index}.png",
                            "type": "web",
                        }

                    except Exception as e:
                        retry_count += 1
                        last_error = e
                        log.error(
                            f"Failed to crawl URL (try {retry_count}/{max_retries}): {url}, error: {str(e)}"
                        )

                        stream.push(
                            component="message",
                            action="web_crewl_update",
                            timestamp=function.timestamp(),
                            payload={
                                "index": index,
                                "url": url,
                                "status": "retrying",
                                "progress": f"Failed to crawl, waiting for retry ({retry_count}/{max_retries}): {str(e)[:50]}...",
                            },
                        )

                        # 尝试清理资源
                        try:
                            await thread_scraper.close()
                        except Exception as close_error:
                            log.error(
                                f"Error cleaning up resources: {str(close_error)}"
                            )

                        # 如果是最后一次尝试，不再继续
                        if retry_count >= max_retries:
                            break

                # 所有重试都失败
                if last_error:
                    error_msg = f"Failed to crawl URL after multiple attempts: {str(last_error)}"
                    log.error(f"URL {index} final failure: {error_msg}")
                    raise Exception(error_msg)
                else:
                    raise Exception("Failed to crawl URL, unknown reason")

            except Exception as e:
                log.error(f"Failed to process URL: {url}, error: {str(e)}")
                log.error(traceback.format_exc())

                stream.push(
                    component="message",
                    action="web_crewl_update",
                    timestamp=function.timestamp(),
                    payload={
                        "index": index,
                        "url": url,
                        "status": "error",
                        "progress": f"Failed to process: {str(e)}",
                    },
                )

                raise Exception(f"Failed to crawl URL: {str(e)}")

    except Exception as e:
        log.error(f"URL processing error: {str(e)}")
        log.error(traceback.format_exc())
        return {
            "index": index,
            "url": url,
            "message": f"{str(e)}",
            "status": "error",
        }


def ensure_protocol(url: str) -> str:
    if not url.startswith(("http://", "https://")):
        return f"https://{url}"
    return url
