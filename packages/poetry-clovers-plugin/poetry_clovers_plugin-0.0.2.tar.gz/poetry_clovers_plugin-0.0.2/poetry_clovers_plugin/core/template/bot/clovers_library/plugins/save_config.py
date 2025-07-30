from clovers import Plugin
from clovers.logger import logger
from clovers.config import Config as CloversConfig

__plugin__ = plugin = Plugin()


@plugin.startup
async def _():
    logger.info(f'本插件位于 "{__file__}",请在首次运行后删除。')
    CloversConfig.environ().save()
