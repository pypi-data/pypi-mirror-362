from clovers import Adapter


adapter = Adapter("SAMPLE")


@adapter.send_method("text")
async def _(message: str, /, data: dict): ...


@adapter.property_method("user_id")
async def _(data: dict) -> str: ...


@adapter.call_method("group_member_list")
async def _(group_id: str, user_id: str, /, data: dict) -> list[dict]: ...
