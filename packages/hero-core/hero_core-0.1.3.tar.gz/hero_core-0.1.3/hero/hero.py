from hero.model import Model
from hero.context import Context
from hero.tool import CommonToolWrapper
from hero.util import (log, function, stream, Storage, Memory)
from hero.agent import Agent
from typing import Any, Callable, Coroutine, List
import os
import traceback
from datetime import datetime
from hero.build_in_tool import final_answer, crewl_web, write_a_note, read_file, download_files, execute_shell, extract_key_info_from_file, reflect_and_brainstorm, program, search
import re
import json


class Hero:
    def __init__(self,  model: Model, search_api: str = "", manual_list: List[str] = [], workspace_root="_workspace"):
        """
        初始化 Hero
        """
        self.default_model = model
        self.workspace_root = workspace_root
        self._initialized = False
        self.run_count = 0
        self.manual_list = manual_list
        self.wait_for_confirmation: None | Callable[[
            Context], Coroutine[Any, Any, str]] = None
        self.planner = Agent(
            name="Hero",
            model=model,
            prompt=function.read_default_tool_prompt("planner.md"),
        )
        self.compressor = Agent(
            name="compressor",
            model=model,
            prompt=function.read_default_tool_prompt("compressor.md"),
        )
        self._initialized = True
        self.basic_info = f"current time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} weekday: {datetime.now().weekday()}"

        # default tools
        self.final_answer = final_answer.custom({
            "model": model
        })
        self.write_a_note = write_a_note
        self.read_file = read_file
        self.download_files = download_files
        self.execute_shell = execute_shell
        self.extract_key_info_from_file = extract_key_info_from_file.custom({
            'model': model
        })
        self.reflect_and_brainstorm = reflect_and_brainstorm.custom({
            "model": model
        })
        self.program = program.custom({
            "coder": model,
            "patcher": model
        })
        # 后期分离
        self.search = search.custom({
            "api_key": search_api
        })
        self.crewl_web = crewl_web.custom({
            "model": model
        })

        self.tools: List[CommonToolWrapper] = [
            self.final_answer, self.write_a_note, self.read_file,
            self.download_files, self.execute_shell, self.extract_key_info_from_file,
            self.reflect_and_brainstorm, self.program, self.search,
            self.crewl_web,
        ]  # TODO: 优化类型

    def get_tool(self, tool_name: str) -> CommonToolWrapper | None:
        """
        获取工具
        """
        for tool in self.tools:
            if tool.get_name() == tool_name:
                return tool

    def add_tool(self, *tools: CommonToolWrapper):
        """
        添加工具
        """
        # 如果工具已经存在，则替换
        for tool in tools:
            if tool.get_name() in self.tools:
                old = self.get_tool(tool.get_name())
                if old:
                    self.tools.remove(old)
        self.tools.extend(tools)

    def get_tools(self):
        """
        获取工具
        """
        return self.tools

    def get_tools_prompt(self):
        """
        获取工具提示
        """
        prompt = ""
        for tool in self.tools:
            prompt += tool.get_prompt()
        return prompt

    async def cleanup(self):
        """
        清理 Hero
        """
        self._initialized = False

    def new_workspace(self):
        """
        创建新的 workspace
        """
        self.workspace_id = function.ulid()
        workspace_path = self.workspace_dir()
        os.makedirs(workspace_path, exist_ok=True)
        log_dir = self.log_dir()
        os.makedirs(log_dir, exist_ok=True)
        return self.workspace_id

    def log_dir(self):
        """
        获取 log 目录
        """
        workspace_root = os.path.abspath(self.workspace_root)
        return os.path.join(workspace_root, self.workspace_id, 'log')

    def workspace_dir(self):
        """
        获取 workspace 目录
        """
        workspace_root = os.path.abspath(self.workspace_root)
        return os.path.join(workspace_root, self.workspace_id, 'working')

    async def run(
        self,
        question: str,
        workspace_id: str = "",
        ref_info: str = "",
        max_turn: int = 20,
    ):
        """
        开始对话
        """
        if workspace_id == "":
            workspace_id = self.new_workspace()
        self.workspace_id = workspace_id

        if ref_info:
            self.basic_info += f"\nreference info:\n {ref_info}"

        ctx: Context = {
            "name": self.planner.get_name(),
            "index": self.run_count,
            "dir": self.workspace_dir(),
            "log_dir": self.log_dir(),
        }

        try:
            self.storage = Storage(self.log_dir())
            self.memory = Memory(self.log_dir(), self.compressor, ctx)

            if not question:
                meta = json.loads(function.read_file(
                    self.log_dir(), "__meta.json") or "{}")
                user_message = meta.get("user_message")
                if user_message:
                    question = user_message
                else:
                    raise Exception("message is empty")
            else:
                # 记录用户消息
                function.write_user_message(
                    {
                        "log_dir": self.log_dir(),
                        "dir": self.workspace_dir(),
                        "name": self.planner.get_name(),
                    }, question)

            # 运行 chat
            stream.push(
                component="message",
                action="chat_start",
                timestamp=function.timestamp(),
                payload={},
            )

            result = await self.task_run(message=question, ctx=ctx, max_turn=max_turn)

            stream.push(
                component="message",
                action="chat_end",
                timestamp=function.timestamp(),
                payload=result or {},
            )

            return result
        except Exception as e:
            log.error(f"chat error: {e}")
            log.error(traceback.format_exc())
            return {
                "status": "error",
                "message": str(e),
            }
        finally:
            log.debug(f"chat end")
            await self.cleanup()

    async def task_run(self, message: str, ctx: Context, images: List[str] = [], context: str = "", max_turn: int | None = None):
        """
        运行对话

        TODO: 支持读取
        """
        if max_turn is not None and self.run_count >= max_turn:
            self.basic_info += f"\nhave reached the maximum number of turns: {max_turn}, please call the `final_answer` tool to answer the question right now."

        if self.planner is None:
            log.error("Hero is not initialized")
            return

        # 追加context，比如读取文件、读取图片，一次性使用
        additional_context = ""
        additional_images = []

        try:
            content = ""
            self.run_count += 1

            # 如果是继续执行历史对话，则需要更新 task_index
            task_history = await self.memory.read_task_history()

            # 如果是继续执行历史对话，则需要更新 task_index
            task_history_tail = int(self.storage.read("task_history_tail"))
            if task_history_tail > self.run_count:
                ctx["index"] = task_history_tail + 1
                self.run_count = task_history_tail + 1

            # 读取 __brainstorm.md 文件
            if os.path.exists(os.path.join(ctx["dir"], "__brainstorm.md")):
                brainstorm = function.read_file(
                    ctx["dir"], "__brainstorm.md")
            else:
                brainstorm = ""

            # 获取流式响应的返回
            json_content = ""
            json_processing = False

            content = ""
            # 获取 workspace 目录下的文件列表
            workspace_file_list = function.list_files_recursive(
                self.workspace_dir()
            )
            log.debug(f"workspace_file_list: {workspace_file_list}")

            if context:
                read_file_content = (
                    f"<read_file_content>\n{context}\n</read_file_content>"
                )
            else:
                read_file_content = ""

            stream.push(
                component="message",
                action="thinking",
                timestamp=function.timestamp(),
                payload={},
            )

            # 获取流式响应的返回
            async for token in self.planner.chat(
                message=message
                + "\n\n"
                + "Please give me the next task in `json` following the `return_format`.",
                params={
                    "tools": self.get_tools_prompt(),
                    "task_history": task_history,
                    "workspace_file_list": workspace_file_list,
                    "basic_info": self.basic_info,
                    "read_file_content": read_file_content,
                    "brainstorm": brainstorm,
                },
                images=images,
            ):
                # 获取json内容
                if token.get("action") == "content_line":
                    # 获取完整的大模型响应内容
                    line = token.get("payload", {}).get("content", "")

                    content += line
                    # 处理json内容
                    if re.search(r"^```json$", line):
                        json_processing = True
                        line = None
                        stream.push(
                            component="message",
                            action="json_start",
                            timestamp=function.timestamp(),
                            payload=token.get("payload", {}),
                        )
                    elif re.search(r"^```$", line):
                        json_processing = False
                        line = None
                        stream.push(
                            component="message",
                            action="json_end",
                            timestamp=function.timestamp(),
                            payload=token.get("payload", {}),
                        )

                    if line is not None:
                        if json_processing:
                            json_content += line
                            stream.push(
                                component="message",
                                action="json_line",
                                timestamp=function.timestamp(),
                                payload=token.get("payload", {}),
                            )
                        else:
                            # 处理非json内容
                            stream.push(
                                component="message",
                                action="content_line",
                                timestamp=function.timestamp(),
                                payload=token.get("payload", {}),
                            )
                else:
                    # 其他消息直接广播
                    stream.push(
                        component="message",
                        action=token.get("action", ""),
                        timestamp=function.timestamp(),
                        payload=token.get("payload", {}),
                    )

            # 从json中提取工具名称和参数
            if json_content:
                tool_dict = json.loads(json_content)
            else:
                tool_dict = function.extract_tool_response(content) or json.loads(
                    content.strip()
                )

            if tool_dict:
                tool_name = tool_dict.get("tool")
                tool_params = tool_dict.get("params")
                log.debug(f"execute tool: {tool_name}, {tool_params}")

                # 开始执行工具
                stream.push(
                    component="message",
                    action="execute_tool_start",
                    timestamp=function.timestamp(),
                    payload={
                        "tool_name": tool_name,
                        "params": tool_params,
                    },
                )

                tool_call = self.get_tool(tool_name)
                if tool_call is None:
                    log.error(f"Tool {tool_name} not found")
                    return

                result = await tool_call.invoke(tool_params, ctx)

                # 写入 task_execute_history
                self.memory.append_task_history(
                    tool=tool_name,
                    params=tool_params,
                    status=result.get("status"),
                    message=result.get("message"),
                    index=ctx["index"],
                )

                # 如果工具返回了 content，则添加到一次性使用的 context 中
                if result.get("additional_context"):
                    additional_context += result.get("additional_context")

                if result.get("additional_images"):
                    additional_images.extend(result.get("additional_images"))

                result["tool_name"] = tool_name
                # 返回结果
                stream.push(
                    component="message",
                    action="execute_tool_end",
                    timestamp=function.timestamp(),
                    payload=result,
                )

                if tool_name == "final_answer" and result.get("status") == "success":
                    # 如果工具是 final_answer，则直接返回结果
                    return result
                if self.wait_for_confirmation and tool_name and tool_name in self.manual_list:
                    stream.push(
                        component="message",
                        action="wait_for_confirmation",
                        timestamp=function.timestamp(),
                        payload={},
                    )
                    await self.wait_for_confirmation(ctx)
            else:
                log.error(f"execute tool failed: {json_content}")

            # 重复执行 chat_run
            return await self.task_run(
                "Next task, Please.", ctx, additional_images, additional_context
            )
        except Exception as e:
            log.error(str(e))
            log.error(traceback.format_exc())

            function.write_task_execute_history(
                tool="",
                params={},
                status="error",
                message=str(e),
                ctx=ctx,
            )

            # 重复执行 chat_run
            return await self.task_run(
                "Next task, Please.", ctx, additional_images, additional_context
            )
