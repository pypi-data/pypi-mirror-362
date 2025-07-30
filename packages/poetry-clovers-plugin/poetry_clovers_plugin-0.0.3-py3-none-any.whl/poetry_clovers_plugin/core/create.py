import sys
import subprocess
from pathlib import Path
from cleo.helpers import argument
from poetry.console.commands.command import Command
from poetry.pyproject.toml import PyProjectTOML
from .template import TEMPLATE_BOT_DIR


def client_code(client: str) -> str:
    if client == "onebot":
        code = "from clovers_client.onebot.v11.client import __client__ as client\n"
    else:
        code = f"from clovers_client.{client}.client import __client__ as client\n"
    code += "import asyncio\n\n"
    code += "asyncio.run(client.run())\n"
    return code


def create_client(name: str, client: str) -> int:
    command = (
        sys.executable,
        "-m",
        "poetry",
        "init",
        "--name",
        name,
        "--python",
        ">=3.12,<4.0.0",
        "--dependency",
        f"clovers_client[{client}]",
        "--no-interaction",
    )
    p = subprocess.run(command, cwd=name)
    if p.returncode != 0:
        return p.returncode
    pyproject = PyProjectTOML(Path.cwd() / name / "pyproject.toml")
    pyproject.data.setdefault("tool", {}).setdefault("poetry", {})["package-mode"] = False
    pyproject.save()
    return subprocess.run((sys.executable, "-m", "poetry", "install"), cwd=name).returncode


class CloversCreateCommand(Command):
    name = "clovers create"
    description = "Create a clovers bot based on `clovers_client`"
    arguments = [argument("name", optional=False, description="Your project name")]

    def handle(self) -> int:
        name: str = self.argument("name")
        path = Path(name)
        if path.exists():
            self.line(f'"{name}" already exists', style="error")
            return 1
        path.mkdir(parents=True)
        import shutil

        try:
            shutil.copytree(TEMPLATE_BOT_DIR, path, dirs_exist_ok=True)
        except Exception as e:
            self.line(f"copy template failed: {e}", "error")
            return 1
        client = self.ask(f"please choose a client [onebot,console,qq]:", default="onebot")
        return_code = create_client(name, client)
        if return_code != 0:
            self.line(f"Error: {return_code}", "error")
            return return_code
        bot = path / "bot.py"
        bot.write_text(client_code(client))
        bot.chmod(0o755)
        return 0
