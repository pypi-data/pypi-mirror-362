from pathlib import Path

TEMPLATE_DIR = Path(__file__).parent
TEMPLATE_PLUGIN_DIR = TEMPLATE_DIR / "plugin"
TEMPLATE_ADAPTER_DIR = TEMPLATE_DIR / "adapter"
TEMPLATE_CLIENT_DIR = TEMPLATE_DIR / "client"
TEMPLATE_BOT_DIR = TEMPLATE_DIR / "bot"


DEPENDENCIES = {
    "plugin": ["pydantic>=2.0"],
    "client": ["pydantic>=2.0", "httpx>=0.23,<1.0.0", "websockets>=15.0,<16.0"],
}
