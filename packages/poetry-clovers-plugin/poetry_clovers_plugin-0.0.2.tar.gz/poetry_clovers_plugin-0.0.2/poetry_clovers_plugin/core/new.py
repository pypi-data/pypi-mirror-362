import sys
import subprocess
from pathlib import Path
from cleo.helpers import argument, option
from poetry.console.commands.command import Command
from poetry.pyproject.toml import PyProjectTOML
from .template import TEMPLATE_PLUGIN_DIR, TEMPLATE_ADAPTER_DIR, TEMPLATE_CLIENT_DIR, DEPENDENCIES


class CloversNewCommand(Command):
    name = "clovers new"
    description = "Create a clovers project"
    arguments = [
        argument("type", optional=False, description="Type of template, can be one of [plugin,adapter,client,bot] or not"),
        argument("name", optional=False, description="Your project name"),
    ]
    options = [
        option("namespace", None, "create a namespace package project", flag=False),
        option("flat", None, "use flat layout"),
        option("add-depend", "d", "Add template's dependencies"),
    ]

    def arg_name(self) -> str:
        name: str = self.argument("name")
        name = name.replace("_", "-")
        if not name.startswith("clovers-"):
            name = f"clovers-{name}"
        return name

    def new_project(self, path: str, dependencies: list[str] | None) -> int:
        args = f"args {path} --python >=3.12,<4.0.0"
        if namespace := self.option("namespace"):
            args += f" --name {namespace}"
        if self.option("flat"):
            args = "--flat " + args
        return_code = self.call(f"new", args)
        if return_code != 0:
            return return_code
        pyproject = PyProjectTOML(Path.cwd() / path / "pyproject.toml")
        pyproject.data.setdefault("project", {})["name"] = path
        pyproject.save()
        self.line(f"Adding dependencies to the {path}...", style="info")
        command = [sys.executable, "-m", "poetry", "add", "clovers>=0.4.6,<1.0.0"]
        if self.option("add-depend"):
            if dependencies:
                command.extend(dependencies)
        else:
            self.line("If you don't need the template's dependencies, please modify this project", style="comment")
        try:
            subprocess.run(command, cwd=path, check=True)
        except subprocess.CalledProcessError as e:
            self.line(f"Return code: {e.returncode}", "error")
            self.line(f"Error Output:\n{e.stderr}", "error")
            return e.returncode
        return 0

    def copy_template(self, path: str, template_path: Path) -> int:
        src_path = Path(path)
        if (check_src_path := src_path.joinpath("src")).exists():
            src_path = check_src_path
        src_path = src_path / path.replace("-", "_")
        import shutil

        try:
            shutil.copytree(template_path, src_path, dirs_exist_ok=True)
        except Exception as e:
            self.line(f"copy template failed: {e}", "error")
            return 1
        return 0

    template_dirs = {
        "plugin": TEMPLATE_PLUGIN_DIR,
        "adapter": TEMPLATE_ADAPTER_DIR,
        "client": TEMPLATE_CLIENT_DIR,
    }

    def handle(self) -> int:
        template_type: str = self.argument("type")
        if template_type == "bot":
            name = self.argument("name")
            return self.call("clovers create", f"args {name}")
        elif template_type in self.template_dirs:
            name = self.arg_name()
            return_code = self.new_project(name, DEPENDENCIES.get(template_type))
            if return_code != 0:
                return return_code
            self.copy_template(name, self.template_dirs[template_type])
            return 0
        else:
            self.line(f"Invalid template: {template_type}", "error")
            return -1
