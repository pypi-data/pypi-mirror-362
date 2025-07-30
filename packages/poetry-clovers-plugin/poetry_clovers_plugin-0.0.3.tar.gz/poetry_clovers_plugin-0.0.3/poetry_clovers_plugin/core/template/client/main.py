import asyncio
import json
import httpx
import websockets
from clovers import Leaf, Client
from clovers.logger import logger
from .config import Config

__config__ = Config.sync_config()


class MyClient(Leaf, Client):
    def __init__(self):
        super().__init__("SAMPLE")
        # 下面是获取配置
        self.url = __config__.url
        self.ws_url = __config__.ws_url
        self.load_adapters_from_list(__config__.adapters)
        self.load_adapters_from_dirs(__config__.adapter_dirs)
        self.load_plugins_from_list(__config__.plugins)
        self.load_plugins_from_dirs(__config__.plugin_dirs)

    def extract_message(self, recv: dict, **ignore) -> str | None:
        raise NotImplementedError

    def startup(self):
        self.client = httpx.AsyncClient(timeout=30)
        return super().startup()

    async def shutdown(self):
        await self.client.aclose()
        return await super().shutdown()

    async def run(self):
        async with self:
            while self.running:
                try:
                    ws_connect = await websockets.connect(self.ws_url)
                    logger.info("websockets connected")
                    async for recv_data in ws_connect:
                        asyncio.create_task(self.response(url=self.url, client=self.client, recv=json.loads(recv_data)))
                    logger.info("client closed")
                    return
                except (websockets.exceptions.ConnectionClosedError, TimeoutError):
                    logger.error("websockets reconnecting...")
                    await asyncio.sleep(5)
                except ConnectionRefusedError as e:
                    logger.error(f"ConnectionRefusedError:{e}")
                    logger.error(f"Please check service on {self.ws_url}")
                    return
                except Exception:
                    logger.exception("something error")
                    return


client = MyClient()
