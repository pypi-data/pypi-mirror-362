from typing import Any, AsyncGenerator, Dict, List
import aiohttp
import json

from hero.util import log

from hero.model import Model


class Usage:
    """
    使用情况
    """
    def __init__(
        self,
        prompt_tokens: int = 0,
        completion_tokens: int = 0,
        total_tokens: int = 0,
        reasoning_tokens: int = 0,
        content_tokens: int = 0,
        prompt_cache_hit_tokens: int = 0,
        prompt_cache_miss_tokens: int = 0,
    ):
        self.prompt_tokens = prompt_tokens
        self.completion_tokens = completion_tokens
        self.total_tokens = total_tokens
        self.reasoning_tokens = reasoning_tokens
        self.content_tokens = content_tokens
        self.prompt_cache_hit_tokens = prompt_cache_hit_tokens
        self.prompt_cache_miss_tokens = prompt_cache_miss_tokens

    def to_dict(self) -> Dict[str, int]:
        return {
            "prompt_tokens": self.prompt_tokens,
            "completion_tokens": self.completion_tokens,
            "total_tokens": self.total_tokens,
            "reasoning_tokens": self.reasoning_tokens,
            "content_tokens": self.content_tokens,
            "prompt_cache_hit_tokens": self.prompt_cache_hit_tokens,
            "prompt_cache_miss_tokens": self.prompt_cache_miss_tokens,
        }


class Agent:
    def __init__(self, name: str, model: Model, prompt: str, timeout: int = 60):
        self.name = name
        self.model = model
        self.prompt = prompt
        self.timeout = timeout

    def get_name(self):
        return self.name

    def _replace_prompt_params(self, prompt: str, params: dict):
        for key, value in params.items():
            prompt = prompt.replace(f"{{{{{key}}}}}", value)
        return prompt
    
    def change_prompt(self, prompt: str):
        self.prompt = prompt
    
    def change_model(self, model: Model):
        self.model = model

    async def chat(
        self,
        message: str,
        params: Dict[str, Any] = {},
        images: List[str] = [],
    ) -> AsyncGenerator[Dict[str, Any], None]:
        """
        聊天
        """
        try:

            system_prompt = self.prompt
            system_prompt = self._replace_prompt_params(system_prompt, params)

            images_str_length = len(json.dumps(
                images or [], ensure_ascii=False))

            if images and len(images) > 0:
                user_message = {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": message},
                        *[
                            {
                                "type": "image_url",
                                "image_url": {"url": image},
                            }
                            for image in images
                        ],
                    ],
                }
                log.debug(
                    f"{self.name} | Images Str Length: {images_str_length}")
            else:
                user_message = {
                    "role": "user",
                    "content": message,
                }

            messages: List[Dict[str, Any]] = [
                {"role": "user", "content": system_prompt},
                user_message,
            ]

            messages_length = len(json.dumps(messages, ensure_ascii=False))

            log.debug(f"{self.name} | Messages Bytes: {messages_length}")
            log.debug(
                f"{self.name} | Messages without images: {messages_length - images_str_length}"
            )

            # 把 messages 写入文件，用于 debug
            messages_content = ""
            for message_item in messages:
                messages_content += f"# {message_item['role']}: \n{message_item['content']}\n\n"

            # MODEL_CONTEXT_LIMIT 默认值为 60000
            if messages_length - images_str_length > int(self.model.model_context_limit or 60000):
                log.error("messages length is too long")
                raise Exception("messages length is too long")

            max_tokens = self.model.max_tokens

            # 构建请求体
            request_body = {
                "model": self.model.model_name,
                "messages": messages,
                "stream": True,
                "max_tokens": max_tokens,
                "stream_options": {
                    "include_reasoning": True,
                    "include_usage": True,
                },
            }

            if self.model.options:
                request_body.update(self.model.options)

            headers = {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self.model.api_key}",
            }

            yield {
                "action": "message_start",
                "payload": {
                    "name": self.name,
                },
            }

            async with aiohttp.ClientSession(
                timeout=aiohttp.ClientTimeout(total=self.timeout)
            ) as session:
                async with session.post(
                    self.model.api_base + "/chat/completions",
                    headers=headers,
                    json=request_body,
                ) as response:
                    if not response.ok:
                        error_text = await response.text()
                        log.error(f"API Error Response: {error_text}")
                        raise Exception(
                            f"API request failed with status {response.status}: {error_text}"
                        )

                    content_cache = ""
                    reasoning_content_cache = ""
                    reasoning_content_progressing = False
                    content_progressing = False
                    line_index = 0

                    async for line in response.content:
                        if line:
                            line = line.decode("utf-8").strip()
                            # print(line)
                            if line.startswith("data: "):
                                data = line[6:]
                                # 如果 data 为 "[DONE]"，则说明流式响应结束
                                if data == "[DONE]":
                                    break

                                try:
                                    parsed = json.loads(data)
                                    content = ""
                                    reasoning_content = ""

                                    if parsed.get("choices") and parsed["choices"][0]:
                                        delta = parsed["choices"][0].get(
                                            "delta", {})
                                        content = delta.get("content", "")
                                        reasoning_content = delta.get(
                                            "reasoning_content", ""
                                        )
                                        finish_reason = parsed["choices"][0].get(
                                            "finish_reason", ""
                                        )

                                        # 按行输出content，只有content按行输出，reasoning_content内没有需要格式化的内容，所以不需要按行输出
                                        content_list = content_cache.split(
                                            "\n")
                                        content_list_len = len(content_list)

                                        # 至少要有两行，第一行内容才是完整的
                                        if content_list_len > 1:

                                            while line_index < content_list_len - 1:

                                                # 消息结束时，再处理最后一行，确保最后一行的内容是完整的
                                                if line_index == content_list_len - 1:
                                                    break

                                                # split时会移除换行符，所以这里要加回去
                                                line = content_list[line_index] + "\n"

                                                yield {
                                                    "action": "content_line",
                                                    "payload": {
                                                        "name": self.name,
                                                        "content": line,
                                                    },
                                                }

                                                line_index += 1

                                        # 如果发现 finish_reason 为 stop，则说明 content 已经结束
                                        if finish_reason == "stop":

                                            # 发出 content_end 事件
                                            if content_progressing:
                                                content_progressing = False

                                                # 输出最后一行
                                                yield {
                                                    "action": "content_line",
                                                    "payload": {
                                                        "name": self.name,
                                                        "content": content_list[
                                                            line_index
                                                        ]
                                                        + "\n",
                                                    },
                                                }

                                                yield {
                                                    "action": "progress_update",
                                                    "payload": {
                                                        "name": self.name,
                                                        "content": "content_end",
                                                    },
                                                }

                                        # 如果 content 不为空，则记录 content 完整文本
                                        if content:
                                            # 记录 content 完整文本
                                            content_cache += content
                                            # 发出 content_start 事件
                                            if not content_progressing:
                                                content_progressing = True
                                                yield {
                                                    "action": "progress_update",
                                                    "payload": {
                                                        "name": self.name,
                                                        "content": "content_start",
                                                    },
                                                }
                                            # 发出 think_end 事件
                                            if reasoning_content_progressing:
                                                reasoning_content_progressing = False
                                                yield {
                                                    "action": "progress_update",
                                                    "payload": {
                                                        "name": self.name,
                                                        "content": "think_end",
                                                    },
                                                }

                                        # 如果 reasoning_content 不为空，则记录 reasoning_content 完整文本
                                        if reasoning_content:
                                            # 记录 reasoning_content 完整文本
                                            reasoning_content_cache += reasoning_content
                                            # 发出 think_start 事件
                                            if not reasoning_content_progressing:
                                                reasoning_content_progressing = True
                                                yield {
                                                    "action": "progress_update",
                                                    "payload": {
                                                        "name": self.name,
                                                        "content": "think_start",
                                                    },
                                                }

                                            yield {
                                                "action": "reasoning_content_token",
                                                "payload": {
                                                    "name": self.name,
                                                    "reasoning_content": reasoning_content,
                                                },
                                            }

                                    # 如果 parsed 中包含 usage 字段，则计算 usage
                                    if parsed.get("usage"):

                                        usage = Usage()
                                        usage_data = parsed["usage"]

                                        if "prompt_tokens" in usage_data:
                                            usage.prompt_tokens = usage_data[
                                                "prompt_tokens"
                                            ]
                                        if "completion_tokens" in usage_data:
                                            usage.completion_tokens = usage_data[
                                                "completion_tokens"
                                            ]
                                        if "total_tokens" in usage_data:
                                            usage.total_tokens = usage_data[
                                                "total_tokens"
                                            ]

                                        if "completion_tokens_details" in usage_data:
                                            details = usage_data[
                                                "completion_tokens_details"
                                            ]
                                            if "reasoning_tokens" in details:
                                                usage.reasoning_tokens = details[
                                                    "reasoning_tokens"
                                                ]
                                            if "content_tokens" in details:
                                                usage.content_tokens = details[
                                                    "content_tokens"
                                                ]

                                        if "prompt_cache_hit_tokens" in usage_data:
                                            usage.prompt_cache_hit_tokens = usage_data[
                                                "prompt_cache_hit_tokens"
                                            ]
                                        if "prompt_cache_miss_tokens" in usage_data:
                                            usage.prompt_cache_miss_tokens = usage_data[
                                                "prompt_cache_miss_tokens"
                                            ]

                                        yield {
                                            "action": "usage",
                                            "payload": {
                                                "name": self.name,
                                                "usage": usage.to_dict(),
                                            },
                                        }

                                except json.JSONDecodeError as e:
                                    log.error(f"Error parsing chunk: {e}")
                                    log.error(f"Raw chunk: {line}")

                    yield {
                        "action": "message_completed",
                        "payload": {
                            "name": self.name,
                            "content": content_cache,
                            "reasoning_content": reasoning_content_cache,
                        },
                    }

            # 接收完流式响应后，结束
            yield {
                "action": "message_end",
                "payload": {
                    "name": self.name,
                },
            }

        except Exception as e:
            log.error(f"Error in chat: {e}")
            raise e
