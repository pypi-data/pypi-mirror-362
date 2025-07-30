import asyncio
from colorama import Fore, Style
from hero.util import function


class Stream:
    """
    流
    """
    def __init__(self):
        self.server_callback = None
        pass

    def set_server_callback(self, server_callback):
        """
        设置服务器回调
        """
        self.server_callback = server_callback

    def push(self, component: str, action: str, timestamp: str, payload: dict):
        """
        推送
        """
        self._print(component, action, timestamp, payload)
        if self.server_callback:
            asyncio.create_task(self.server_callback(component, action, timestamp, payload))

    def _print(self, component: str, action: str, timestamp: str, payload: dict):
        """
        打印
        """
        # 处理message消息
        if component == "message":
            if action == "reasoning_content_token":
                print(payload["reasoning_content"], end="", flush=True)
            elif action == "content_line":
                print(payload["content"], end="", flush=True)
            elif action == "usage":
                function.print_block(f"{action}", timestamp)
                for key, value in payload["usage"].items():
                    function.print_kv(key, value)
            elif action == "progress_update":
                function.print_progress(payload["content"], timestamp)
            elif action == "message_start" or action == "message_end":
                function.print_block(f"{action}", timestamp)
                for key, value in payload.items():
                    function.print_kv(key, value)
            elif action == "execute_tool_start":
                function.print_block(f"{action}", timestamp)
                for key, value in payload.items():
                    function.print_kv(key, value)
            elif action == "execute_tool_end":
                function.print_block(f"{action}", timestamp)
                for key, value in payload.items():
                    if not key == "additional_image":
                        function.print_kv(key, value)
            elif action == "json_start" or action == "json_end":
                function.print_block(f"{action}", timestamp)
            elif action == "json_line" or action == "shell_line":
                print(payload["content"], end="", flush=True)
            elif action == "chat_start":
                function.print_block(f"{action}", timestamp)
            elif action == "chat_end":
                function.print_block(f"{action}", timestamp)
                for key, value in payload.items():
                    function.print_kv(key, value)
            elif action == "web_crewl_update":
                function.print_block(f"{action}", timestamp)
                for key, value in payload.items():
                    function.print_kv(key, value)
            else:
                function.print_block(f"{action}", timestamp)

        # 处理editor消息
        elif component == "editor":
            if action == "open_file" or action == "close_file":
                function.print_block(f"{action}", timestamp)
                for key, value in payload.items():
                    function.print_kv(key, value)
            elif action == "append_file":
                print(payload["content"], end="", flush=True)

        # 处理terminal消息
        elif component == "terminal":
            if action == "stdout":
                if payload.get("update_last"):
                    print(f"\r{Fore.GREEN}{payload['content']}{Style.RESET_ALL}", end="", flush=True)
                else:
                    print(f"{Fore.GREEN}{payload['content']}{Style.RESET_ALL}")
            elif action == "stderr":
                if payload.get("update_last"):
                    print(f"\r{Fore.RED}{payload['content']}{Style.RESET_ALL}", end="", flush=True)
                else:
                    print(f"{Fore.RED}{payload['content']}{Style.RESET_ALL}")
        pass


stream = Stream()
