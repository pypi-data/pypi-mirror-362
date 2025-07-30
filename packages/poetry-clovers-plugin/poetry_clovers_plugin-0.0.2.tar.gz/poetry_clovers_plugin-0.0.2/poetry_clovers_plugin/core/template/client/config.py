from pydantic import BaseModel
from clovers.config import Config as CloversConfig
from functools import cache


class Config(BaseModel):
    url: str = "http://127.0.0.1:3000"
    ws_url: str = "ws://127.0.0.1:3001"
    adapters: list[str] = []
    adapter_dirs: list[str] = []
    plugins: list[str] = []
    plugin_dirs: list[str] = []

    @classmethod
    @cache
    def sync_config(cls):
        """获取 `CloversConfig.environ()['clovers']` 配置并将默认配置同步到全局配置中。"""
        __config_dict__: dict = CloversConfig.environ().setdefault("clovers", {})
        __config_dict__.update((__config__ := cls.model_validate(__config_dict__)).model_dump())
        return __config__
