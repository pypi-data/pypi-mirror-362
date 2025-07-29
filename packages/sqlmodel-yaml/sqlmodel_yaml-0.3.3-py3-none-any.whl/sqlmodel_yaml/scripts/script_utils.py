import subprocess
import site
from pathlib import Path
from sys import exit

this_directory = Path(__file__).parent
project_root = this_directory.parent.parent


def run(cmd):
    print(f"Running: {cmd}")
    return subprocess.run(
        cmd,
        shell=True,
        text=True,
        cwd=project_root,
        stderr=subprocess.STDOUT,
        stdout=subprocess.PIPE,
        check=False,
    )


def package_installed_as_editable(package_name: str = "sqlmodel-yaml") -> bool:
    for path in site.getsitepackages() + [site.getusersitepackages()]:
        egg_link = Path(path) / f"{package_name}.egg-link"
        if egg_link.exists():
            return True
    return False


class ScriptEnvironmentError(Exception):

    def __init__(self, package, name):
        message = (
            f"PyPi package '{package}' is not installed with '-e' option."
            f"This is required to give relative paths to {name}."
            ""
        )
        print(message)
        super().__init__(message)
        exit(1)


class ScripCLIError(Exception):

    def __init__(self, *args):
        super().__init__(*args)
        exit(1)
