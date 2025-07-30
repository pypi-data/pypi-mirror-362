from cleo.helpers import argument
from poetry.console.commands.command import Command

WELCOME_TO_CLOVERS_CLI = r"""Welcome to Clovers CLI!
  ___  __    _____  _  _  ____  ____  ___       ___  __    ____ 
 / __)(  )  (  _  )( \/ )( ___)(  _ \/ __)     / __)(  )  (_  _)
( (__  )(__  )(_)(  \  /  )__)  )   /\__ \    ( (__  )(__  _)(_ 
 \___)(____)(_____)  \/  (____)(_)\_)(___/     \___)(____)(____)"""


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
                return 0
            case "update":
                return self.call("update", "--only clovers-plugins")
            case "run":
                return self.call("run", "args python bot.py")
            case _:
                self.line("Invalid command", style="error")
                return 1
