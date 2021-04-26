# Docker-Wrap

A drop-in wrapper for docker-compose that runs pre/post up and pre/post build scripts.

I frequently have scripts I want to run before/after docker-compose
build/up.  This wrapper creates a standard way to run everything by
just wrapping docker-compose and passing through all arguments.  You
use it wherever you normally use docker-compose.  You could even
symlink it as docker-compose in your /usr/local/bin.

Note: we currently support pre/post build, but not pre/post use yet.

## Install

Just `git clone` and then symlink it in to your path:

    git clone https://github.com/jvasile/docker-wrap.git /path/to/wrap
    ln -sf /path/to/wrap/docker-wrap.py /usr/local/bin/docker-wrap

Eventually, we want to install like this:

    pip3 install docker-wrap

## Use

For any service, add a dict called "x-wrap" with one or more keys that
correspond to a docker-compose command (see `docker-compose --help` for
the list).  Those command keys should indicate dicts that contain
`pre` or `post` keys whose values are paths to scripts to run.

`docker-wrap` will run any `pre` script before it runs your command,
then run any `post` script.  If a `pre` script prints a valid yaml
structure, `docker-wrap` will use that script as the
`docker-compose.yml` for running the command.

`docker-wrap` passes all arguments on to `docker-compose`.

## Sample docker-compose.yml

    version: "3.9"
    services:
      foo:
        x-wrap:
            build:
              pre: pre-build.sh bar baz
        build: bar


The default directory for running `pre-build.sh` will be the `foo`
directory.  If you set context, it will be the context.

## License and Copyright

Copyright 2020 James Vasile, published under the terms of AGPLv3 or
later.
