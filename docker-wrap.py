#!/usr/bin/env python3

"""
Monkeypatch docker-compose to call pre/post build scripts.
"""

import os
import subprocess
import sys
from contextlib import contextmanager
from pathlib import Path
from typing import Any, Dict, Generator

import compose  # type: ignore
from packaging import version

# Import compose and make sure our docker-compose is the correct version for monkeypatching
min_version = version.parse("1.28.6")
if version.parse(compose.__version__) < min_version:
    sys.exit(
        f"Underlying docker-compose must be version {min_version}+ not {compose.__version__}"
    )

# Import after validating version because older ones have different submodules
import compose.cli  # type: ignore
import compose.cli.main  # type: ignore
from compose.cli.log_printer import LogPrinter #type: ignore
from compose.service import Service  # type: ignore
from compose.project import Project  # type: ignore

@contextmanager
def cd(path: Path) -> Generator[None, None, None]:
    """Sets the cwd within the context

    Args: path (Path): The path to the cwd
    Yields: None

    Thanks to https://dev.to/teckert/changing-directory-with-a-python-context-manager-2bj8
    """

    origin = Path().absolute()
    try:
        os.chdir(path)
        yield
    finally:
        os.chdir(origin)


def do_wrap_cmd(opts: Dict[str, Any], stage: str, cmd: str) -> None:
    """Execute a pre- or post- command

    This function checks the docker-compose options for a pre- or
    post- command and execute it if found.

    """

    # Exit if docker-compose file doesn't have a wrap command
    if not "x-wrap" in opts or not cmd in opts["x-wrap"]:
        return

    # Run any indicated script
    if stage in opts["x-wrap"][cmd]:
        script_dir = opts['build']['context']
        with cd(script_dir):
            script = opts["x-wrap"][cmd][stage]
            if script_dir.startswith("/"):
                script = os.path.join(script_dir, script)
                print(f"Running {stage}-{cmd} {script}")
                cp = subprocess.run(script, shell=True)
            else:
                print(f"Running {stage}-{cmd} {script}")
                cp = subprocess.run("./" + script, shell=True)
            if cp.returncode != 0:
                sys.exit(f"x-wrap {stage}-{cmd} failed")


def advise_build() -> None:
    """Advise the build method of the Service class"""

    def build_replacement(self: Service, *args: Any, **kwargs: Any) -> None:
        do_wrap_cmd(self.options, "pre", "build")
        build_orig(self, *args, **kwargs)
        do_wrap_cmd(self.options, "post", "build")

    build_orig = Service.build
    Service.build = build_replacement


def advise_log_printer_from_project() -> None:
    """Advise the log_printer_from_project function in main.py

    When docker-compose creates the LogPrinter, add a list of Service
    objects, because those have the docker-compose options in them.
    That will make that info available to LogPrinter.run.

    """

    def wrap_run(self:LogPrinter):
        if not self.containers:
            return


        for c in self.containers:
            service = [s for s in self.services if s.name == c.service][0]
            do_wrap_cmd(service.options, "pre", "up")

        orig_run(self)

        for c in self.containers:
            service = [s for s in self.services if s.name == c.service][0]
            do_wrap_cmd(service.options, "post", "up")

    def replacement(project: Project, *args: Any, **kwargs: Any) -> None:
        log_printer = orig(project, *args, **kwargs)
        log_printer.services = project.services
        return log_printer

    orig_run = LogPrinter.run
    LogPrinter.run = wrap_run

    orig = compose.cli.main.log_printer_from_project
    compose.cli.main.log_printer_from_project = replacement


if __name__ == "__main__":
    advise_build()
    advise_log_printer_from_project()

    compose.cli.main.main()
