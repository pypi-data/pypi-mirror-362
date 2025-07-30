from typing import AbstractSet, Any
from collections.abc import Iterable
from cleo.helpers import argument
from poetry.console.commands.command import Command


def get_keys(resorce_dict: dict, key_path: Iterable[str]):
    target_dict: dict[str, Any] = resorce_dict
    for key in key_path:
        if key in target_dict:
            target_dict = target_dict[key]
        else:
            return
    return target_dict


class CloversPluginCommand(Command):
    name = "clovers plugin"
    description = "Add/Remove clovers-plugins using poetry add/remove."
    arguments = [
        argument("do", optional=False, description="add/remove"),
        argument("name", optional=False, multiple=True, description="package name"),
    ]
    key_path = ("tool", "poetry", "group", "clovers-plugins", "dependencies")

    def handle(self) -> int:
        do = self.argument("do")
        match do:
            case "add":
                return self.add_handle()
            case "remove":
                return self.remove_handle()
            case _:
                self.line(f'Invalid command "{do}" please use [add,remove]', style="error")
                return -1

    def clovers_plugins(self) -> AbstractSet[str]:
        dependencies = get_keys(self.poetry.pyproject.data, self.key_path)
        return dependencies.keys() if dependencies else set[str]()

    def add_handle(self) -> int:
        name = " ".join(self.argument("name"))
        old_plugins = self.clovers_plugins()
        return_code = self.call(f"add", f"args {name} --group clovers-plugins")
        if return_code != 0:
            return return_code
        self.poetry.pyproject.reload()
        new_plugins = self.clovers_plugins()
        added_plugins = new_plugins - old_plugins
        if not added_plugins:
            self.line("No new plugins added.", style="error")
            return -1
        from clovers.config import Config as CloversConfig

        clovers_config = CloversConfig.environ()
        plugins: list[str] = clovers_config.setdefault("clovers", {}).setdefault("plugins", [])
        plugins.extend(plugin for plugin in added_plugins if plugin not in plugins)
        clovers_config.save()
        return 0

    def remove_handle(self) -> int:
        name = " ".join(self.argument("name"))
        old_plugins = self.clovers_plugins()
        return_code = self.call(f"remove", f"args {name}")
        if return_code != 0:
            return return_code
        self.poetry.pyproject.reload()
        new_plugins = self.clovers_plugins()
        removed_plugins = old_plugins - new_plugins
        from clovers.config import Config as CloversConfig

        clovers_config = CloversConfig.environ()
        plugins: list[str] = clovers_config.setdefault("clovers", {}).get("plugins", [])
        clovers_config["clovers"]["plugins"] = [plugin for plugin in plugins if plugin not in removed_plugins]
        clovers_config.save()
        return 0
