# Docker-Wrap

A drop-in wrapper for `docker-compose` that runs pre/post up and pre/post build scripts.

I frequently have scripts I want to run before/after `docker-compose`
build/up.  This wrapper creates a standard way to run everything by
just wrapping `docker-compose` and passing through all arguments.  You
use it wherever you normally use `docker-compose`.  You could even
symlink it as docker-compose in your /usr/local/bin.

The wrapper is smart enough to run your pre-build, even when build is
triggered by an `up` command.

The pre-build script runs before `Dockerfile` is loaded, so you can
*generate* your `Dockerfile` from your pre-build script.

## Install

Just `git clone` and then symlink it in to your path:

    git clone https://github.com/jvasile/docker-wrap.git /path/to/wrap
    ln -sf /path/to/wrap/docker-wrap.py /usr/local/bin/docker-wrap

Eventually, we want to install like this:

    pip3 install docker-wrap

## Use

For any service, add a dict called "x-wrap" with one or more keys that
correspond to 'build' or 'use'.  Those command keys should indicate
dicts that contain `pre` or `post` keys whose values are paths to
scripts to run.  See the example below.

`docker-wrap` will run any `pre` script before it runs your command,
then run any `post` script.  A future feature will that be if a `pre`
script prints a valid yaml structure, `docker-wrap` will use that
script as the `docker-compose.yml` for running the command.

`docker-wrap` passes all arguments on to `docker-compose`.

Something like this would work:

    docker-wrap up foo

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

## Features Roadmap

    [X] Pre/post build scripts
    [X] Allow pre script to replace Dockerfile
    [ ] Allow pre script to replace docker-compose
    [X] Pre/post up scripts
    [ ] Use `wrap` instead of `x-wrap`

## Contributing

Activity is in the [GitHub
Repo](https://github.com/jvasile/docker-wrap.git) and you can always
pop in to [chat.opentechstrategies.com](chat.opentechstrategies.com)
as well.

Please run the [python qa
script](https://code.librehq.com/james/quest-for-awesome) on the code
before submitting a PR.  That script just runs black, isort, mypy, and
tests (tho we have no tests yet).

## License and Copyright

Copyright 2020 James Vasile, published under the terms of AGPLv3 or
later.
