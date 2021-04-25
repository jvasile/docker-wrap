#!/usr/bin/env python3

import os
import pprint
import subprocess
import sys
from contextlib import contextmanager
from pathlib import Path

import compose
import compose.cli
import compose.cli.main
import compose.config
import compose.config.validation as validation
from compose.service import Service

pp = pprint.PrettyPrinter(indent=4).pprint


"""If we ever want to ditch the x- prefix to our wrap option, we
might want to adjust the schema.  This code is a start.

from compose.project import Project
# Adjust schema to accept our wrap option
def load_jsonschema_replace(version):
    schema = load_json_schema_orig(version)
    return schema
load_json_schema_orig = validation.load_jsonschema
validation.load_jsonschema = load_jsonschema_replace

"""


@contextmanager
def cd(path: Path):
    """Sets the cwd within the context

    Args:
        path (Path): The path to the cwd

    Yields:
        None

    Thanks to https://dev.to/teckert/changing-directory-with-a-python-context-manager-2bj8
    """

    origin = Path().absolute()
    try:
        os.chdir(path)
        yield
    finally:
        os.chdir(origin)


def do_wrap_cmd(opts, stage, cmd):
    """Execute a pre- or post- command

    This function checks the docker-compose options for a pre- or
    post- command and execute it if found.

    """

    # Exit if docker-compose file doesn't have a wrap command
    if not "x-wrap" in opts or not cmd in opts["x-wrap"]:
        return

    # Run any indicated script
    if stage in opts["x-wrap"][cmd]:
        script_dir = opts[cmd].get("context", ".")
        with cd(script_dir):
            if script_dir.startswith("/"):
                script = os.path.join(script_dir, opts["x-wrap"][cmd][stage])
                subprocess.run(script, shell=True)
            else:
                subprocess.run("./" + opts["x-wrap"][cmd][stage], shell=True)


# Advise the build method of the Service class
def build_replacement(self, *args, **kwargs):
    do_wrap_cmd(self.options, "pre", "build")
    build_orig(self, *args, **kwargs)
    do_wrap_cmd(self.options, "post", "build")


build_orig = Service.build
Service.build = build_replacement

compose.cli.main.main()
