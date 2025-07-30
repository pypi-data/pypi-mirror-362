from typing import TypedDict


class Context(TypedDict):
    name: str
    dir: str
    log_dir: str
    index: int