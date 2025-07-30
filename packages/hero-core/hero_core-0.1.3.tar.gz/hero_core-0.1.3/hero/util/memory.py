import os
from typing import List
import traceback
from hero.context import Context
from hero.util import log, function, stream
from hero.agent import Agent
from hero.util.storage import Storage
import re
import json


class Memory:
    def __init__(self, dir: str, compressor: Agent, ctx: Context):
        self.dir = dir
        self.ctx = ctx
        self.full_task_history = f"__Hero_tasks.md"
        self.compressed_task_history = "__Hero_tasks_compressed.md"
        self.storage = Storage(self.dir)
        self.compressor = compressor
        self.split_file_limit = 50000
        self.compressed_word_limit = 1000
        self.compressed_task_file_word_limit = 50000
        self.max_history_count = 20
        self.max_history_limit = 40000

    def custom(self, split_file_limit: int | None = None,
               compressed_word_limit: int | None = None,
               compressed_task_history_word_limit: int | None = None,
               max_history_count: int | None = None,
               max_history_limit: int | None = None):
        if split_file_limit is not None:
            self.split_file_limit = split_file_limit
        if compressed_task_history_word_limit is not None:
            self.compressed_word_limit = compressed_task_history_word_limit
        if max_history_count is not None:
            self.max_history_count = max_history_count
        if max_history_limit is not None:
            self.max_history_limit = max_history_limit
        if compressed_word_limit is not None:
            self.compressed_task_file_word_limit = compressed_word_limit

    def _read_full_task_history(self) -> str:
        if not os.path.exists(os.path.join(self.dir, self.full_task_history)):
            with open(
                os.path.join(self.dir, self.full_task_history),
                "w",
                encoding="utf-8",
            ) as f:
                f.write("")
        return function.read_file(self.dir, self.full_task_history)

    def _append_compressed_task_history(self, content: str):
        function.append_file(self.dir, self.compressed_task_history, content)

    def _read_compressed_task_history(self) -> str:
        return function.read_file(self.dir, self.compressed_task_history)

    def _read_short_task_history(self) -> tuple[str, int]:
        # 如果文件不存在，则创建
        file_path = os.path.join(self.dir, self.full_task_history)
        if not os.path.exists(file_path):
            with open(file_path, "w", encoding="utf-8") as f:
                f.write("")

        start_index = 1
        task_history_tail = int(self.storage.read("task_history_tail"))
        history = self._read_full_task_history()

        history_list = history.split("</task>")
        log.debug(f"len(history_list): {len(history_list)}")
        log.debug(f"len(history): {len(history)}")

        if task_history_tail > self.max_history_count:
            # 计算 start_index，是整体任务列表的索引
            start_index = task_history_tail - self.max_history_count + 1
            history_list = history_list[-self.max_history_count:]

        # 把 history_list 拼接成字符串，如果 history_list 的字符串长度大于 MAX_HISTORY_LIMIT，则从后往前截取，直到小于 MAX_HISTORY_LIMIT
        history = "</task>".join(history_list)
        while len(history) > self.max_history_limit:
            history_list.pop(0)
            start_index += 1
            history = "</task>".join(history_list)

        history = "</task>".join(history_list)
        log.debug(f"After len(history_list): {len(history_list)}")
        log.debug(f"After len(history): {len(history)}")
        log.debug(f"start_index: {start_index}")

        return history, start_index

    def append_task_history(
        self, tool: str, params: dict, status: str, message: str, index: int
    ):
        print(f"append_task_history: {tool} {params} {status} {message} {index}")
        with open(
            os.path.join(self.dir, self.full_task_history),
            "a",
            encoding="utf-8",
        ) as f:
            content = ""
            content += f"<task tool={tool} index={index} finished_at={function.timestamp_to_str(function.timestamp())}>\n"
            content += f"<params>{json.dumps(params, ensure_ascii=False)}</params>\n"
            content += f"<result status={status}>\n"
            content += message
            content += f"\n</result>\n"
            content += f"</task>\n\n"
            f.write(content)
        self.storage.write("task_history_tail", str(index))

    async def read_task_history(self) -> str:
        short_task_history_content, start_index = self._read_short_task_history()
        compressed_task_history_tail = int(
            self.storage.read("compressed_task_history_tail")
        )
        task_history_tail = int(self.storage.read("task_history_tail"))

        long_task_history_content = ""

        if start_index > 1:
            # -1 是避免交界处重复
            # 需要压缩任务历史
            if compressed_task_history_tail < start_index - 1:
                # 从之前压缩任务历史的地方开始压缩，直到当前任务历史
                log.info(
                    f"compressing task history from {compressed_task_history_tail + 1} to {task_history_tail}"
                )
                await self._compress_task_history(
                    compressed_task_history_tail + 1, task_history_tail
                )

            # 读取压缩任务历史
            long_task_history_content = self._read_compressed_task_history()
            # 打印最新的压缩任务历史尾指针
            log.info(
                f"compressed_task_history_tail: {self.storage.read('compressed_task_history_tail')}"
            )
            if len(long_task_history_content) > self.compressed_task_file_word_limit:
                log.info(
                    f"long_task_history_content is too long: {len(long_task_history_content)}, compressing it"
                )
                await self._compress_task_history_file_twice()
                # 重新读取压缩任务历史
                long_task_history_content = self._read_compressed_task_history()

        # 拼接压缩任务历史和短任务历史
        task_history = long_task_history_content + short_task_history_content

        log.info(f"task_history_length: {len(task_history)}")

        return task_history

    async def _compress_task_history_file_twice(self) -> dict[str, str]:
        try:
            # 读取压缩任务历史
            long_task_history_content = self._read_compressed_task_history()

            # 使用模型提取关键信息
            compressed_task_history_tail = int(
                self.storage.read("compressed_task_history_tail")
            )

            log.info(
                f"long_task_history_content_length: {len(long_task_history_content)}"
            )
            log.info(f"compressed_task_history_tail: {compressed_task_history_tail}")

            key_info = ""

            # 使用模型提取关键信息
            user_message = str(function.read_user_message(self.ctx))

            message = f"Task 1 to Task {compressed_task_history_tail} history has been printed above, between <content> and </content>.\n"
            message += f"Please summarize the key information from the **content** strictly based on **user_message** and following the **protocal**.\n"
            message += (
                f"The summary should be less than {self.compressed_word_limit} words.\n"
            )

            key_info += f'<compressed_task_history start_index="1" end_index="{compressed_task_history_tail}">\n\n'

            # 使用模型提取关键信息
            async for token in self.compressor.chat(
                message=message,
                params={
                    "content": long_task_history_content,
                    "user_message": user_message,
                },
            ):
                stream.push(
                    component="message",
                    action=token.get("action", ""),
                    timestamp=function.timestamp(),
                    payload=token.get("payload", {}),
                )

                if token.get("action") == "content_line":
                    key_info += token.get("payload", {}).get("content", "")

            key_info += f"\n</compressed_task_history>\n"

            # 已有文件改名
            # 获取当前时间
            timestamp = function.timestamp()
            # 改名
            os.rename(
                os.path.join(self.dir, self.compressed_task_history),
                os.path.join(self.dir, f"__Hero_tasks_compressed_{timestamp}.md"),
            )

            # 写入新文件
            function.append_file(self.dir, self.compressed_task_history, key_info)

            return {
                "status": "success",
                "message": f"Compress the task history successfully. The compressed task history has been written to {self.compressed_task_history}.",
            }

        except Exception as e:
            log.error(f"Error in compress_task_history_file_twice: {e}")
            log.error(traceback.format_exc())
            return {"status": "error", "message": str(e)}

    async def _compress_task_history(self, start_index: int, end_index: int) -> dict[str, str]:
        try:

            if not os.path.exists(os.path.join(self.dir, self.compressed_task_history)):
                with open(
                    os.path.join(self.dir, self.compressed_task_history),
                    "w",
                    encoding="utf-8",
                ) as f:
                    f.write("")

            history = self._get_task_history_index(start_index, end_index)

            log.info(f"history_length: {len(history)}")
            log.info(f"start_index: {start_index}")
            log.info(f"end_index: {end_index}")

            key_info = ""

            # 使用模型提取关键信息
            user_message = str(
                function.read_user_message(self.ctx))

            message = f"Task {start_index} to Task {end_index} history has been printed above, between <content> and </content>.\n"
            message += f"Please summarize the key information from the **content** strictly based on **user_message** and following the **protocal**.\n"
            message += f"The summary should be less than {self.compressed_word_limit} words.\n"

            key_info += f'<compressed_task_history start_index="{start_index}" end_index="{end_index}">\n\n'

            # 使用模型提取关键信息
            async for token in self.compressor.chat(
                message=message,
                params={
                    "content": history,
                    "user_message": user_message,
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

            key_info += f"\n</compressed_task_history>\n"

            function.append_file(
                self.dir, self.compressed_task_history, key_info)

            # 更新压缩任务历史尾指针
            self.storage.write("compressed_task_history_tail", str(end_index))

            return {
                "status": "success",
                "message": f"Compress the task history successfully. The compressed task history has been written to {self.compressed_task_history}.",
            }

        except Exception as e:
            log.error(f"Error in compress_task_history: {e}")
            log.error(traceback.format_exc())
            return {"status": "error", "message": str(e)}

    def _split_task_history(self, content: str) -> List[str]:
        """
        将 Markdown 内容按照标题分割，并确保每部分不超过指定长度
        """
        blocks = content.split("</task>")
        temp_str = ""
        split_array = []
        result_array = []

        for i in range(len(blocks)):
            if len(temp_str + blocks[i]) > self.split_file_limit:
                split_array.append(temp_str)
                temp_str = ""
            temp_str += blocks[i] + "</task>"

        split_array.append(temp_str)

        for i in range(len(split_array)):
            # 获取所有task标签的index
            task_matches = re.findall(
                r"<task tool=\"(.*?)\" index=\"(.*?)\"", split_array[i]
            )
            if task_matches:
                first_index = task_matches[0][1]  # 第一个index
                last_index = task_matches[-1][1]  # 最后一个index
                log.info(
                    f"First index: {first_index}, Last index: {last_index}")
                result_array.append(
                    {
                        "start": first_index,
                        "end": last_index,
                        "content": split_array[i],
                    }
                )

        return result_array

    def _get_task_history_index(self, start: int, end: int) -> str:
        full_content = self._read_full_task_history()
        blocks = full_content.split("</task>")
        result = ""
        for i in range(len(blocks)):
            if i + 1 >= start and i + 1 <= end:
                result += blocks[i] + "</task>"
        return result
