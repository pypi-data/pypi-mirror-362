from .clovers import Event, Rule, plugin
from .config import Config

__config__ = Config.sync_config()

to_me: Rule = lambda e: e.to_me


@plugin.handle(["测试", "test"], ["user_id", "group_id", "nickname", "to_me"], rule=to_me)
async def _(event: Event):
    return f"UID: {event.user_id}\nGID: {event.group_id}\n昵称: {event.nickname}"
