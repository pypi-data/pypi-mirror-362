from cleo.helpers import argument
from poetry.console.commands.command import Command


WELCOME_TO_CLOVERS_CLI = r"""
  ___  _      ___  __   __ ___  ___  ___         ___  _     ___ 
 / __|| |    / _ \ \ \ / /| __|| _ \/ __|       / __|| |   |_ _|
| (__ | |__ | (_) | \   / | _| |   /\__ \      | (__ | |__  | | 
 \___||____| \___/   \_/  |___||_|_\|___/       \___||____||___|
"""
WELCOME_TO_CLOVERS_CLI = WELCOME_TO_CLOVERS_CLI[1:]


class CloversMainCommand(Command):
    name = "clovers"
    description = "Manage your clovers project"
    arguments = [
        argument("cmd", optional=True, description="update/create/run"),
        argument("name", optional=True, description="name"),
    ]

    def handle(self) -> int:
        match self.argument("cmd"):
            case None:
                self.line(WELCOME_TO_CLOVERS_CLI)
                self.line("Welcome to Clovers CLI!", style="comment")
                return 0
            case "update":
                return self.call("update", "--only clovers-plugins")
            case "run":
                return self.call("run", "args bot.py")
            case _:
                self.line("Invalid command", style="error")
                return 1
