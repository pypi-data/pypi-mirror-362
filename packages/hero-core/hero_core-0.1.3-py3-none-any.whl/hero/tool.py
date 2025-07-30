from typing import Callable, Any, Dict, Optional, TypeVar, Type, cast, Generic

from hero.context import Context


T = TypeVar('T')

class CommonToolWrapper(Generic[T]):
    def __init__(self, name: str, custom_params: T | None, annotations: Dict[str, Any], func: Callable[..., Any], params_type: Optional[Type[T]] = None):
        self.name = name
        self.custom_params: T | None = custom_params
        self.annotations = annotations
        self.func = func
        self.params_type = params_type

    def get_name(self) -> str:
        return self.name

    def get_prompt(self) -> str:
        return f"""
<tool name="{self.name}">
{self.annotations}
</tool>
"""
    
    def custom(self, custom_params: Optional[T] = None) -> "CommonToolWrapper[T]":

        if custom_params is None:
            return self
        
        if isinstance(custom_params, dict):
            result: Dict[str, Any] = custom_params.copy()
        else:
            # 如果不是字典，使用cast进行类型转换
            result: Dict[str, Any] = cast(Dict[str, Any], custom_params)
        
        if self.custom_params is not None:
            if isinstance(self.custom_params, dict):
                self.custom_params.update(result)
            else:
                self.custom_params = cast(T, result)
        return self

    def invoke(self, call_params: Dict[str, Any], ctx: Optional[Context]) -> Any:
        if "params" in self.func.__annotations__:
            call_params["params"] = self.custom_params
        if "ctx" in self.func.__annotations__:
            call_params["ctx"] = ctx
        return self.func(**call_params)

class Tool:
    def __init__(self):
        pass

    def init(self, name: str, custom_params: T | None = None, params_type: Optional[Type[T]] = None):
        """
        工具装饰器
        
        Args:
            name: 工具名称
            custom_params: 自定义参数
            params_type: 参数类型，用于类型提示和验证
        """
        def decorator(func: Callable[..., Any]) -> CommonToolWrapper[T]:
            return CommonToolWrapper[T](name, custom_params, func.__annotations__, func, params_type)

        return decorator