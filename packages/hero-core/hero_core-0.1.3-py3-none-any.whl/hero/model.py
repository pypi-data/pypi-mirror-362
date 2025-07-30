from typing import Any, Dict


class Model:
    def __init__(self,
                 model_name: str = "",
                 api_base: str = "",
                 api_key: str = "",
                 model_context_limit: int = 60000,
                 max_tokens: int = 60000,
                 is_multimodal: bool = False,
                 options: Dict[str, Any] = {},
                 ):
        self.model_name = model_name
        self.api_base = api_base
        self.api_key = api_key
        self.model_context_limit = model_context_limit
        self.max_tokens = max_tokens
        self.is_multimodal = is_multimodal
        self.options = options
