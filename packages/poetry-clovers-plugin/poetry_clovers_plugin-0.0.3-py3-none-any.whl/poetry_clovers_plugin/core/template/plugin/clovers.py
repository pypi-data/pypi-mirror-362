from typing import Protocol, overload, Literal
from clovers import EventProtocol, Plugin, Result


class Event(EventProtocol, Protocol):
    """插件事件协议"""

    user_id: str
    group_id: str | None
    nickname: str
    to_me: bool
    permission: int

    @overload
    async def call(self, key: Literal["user_id"]) -> str: ...

    @overload
    async def call(self, key: Literal["group_id"]) -> str | None: ...

    @overload
    async def call(self, key: Literal["nickname"]) -> str: ...

    @overload
    async def call(self, key: Literal["text"], message: str): ...


type Rule = Plugin.Rule.Checker[Event]
"""插件事件规则类型"""


def build_result(result):
    if isinstance(result, Result):
        return result
    if isinstance(result, str):
        return Result("text", result)
    if isinstance(result, bytes):
        return Result("image", result)
    if isinstance(result, list):
        return Result("list", [build_result(seg) for seg in result if seg])


plugin = Plugin(build_result=build_result)
"""插件实例"""

plugin.set_protocol("properties", Event)
