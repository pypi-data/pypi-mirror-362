# Python: Rako Controls API Client

[![GitHub Release][releases-shield]][releases]
![Project Stage][project-stage-shield]
![Project Maintenance][maintenance-shield]
[![License][license-shield]](LICENSE)

[![Build Status][build-shield]][build]
[![Code Coverage][codecov-shield]][codecov]
[![Code Quality][code-quality-shield]][code-quality]


Asynchronous Python client for Rako Controls.

**This is a modernized fork** that has been updated to Python 3.12+ best practices, includes async concurrency fixes for Home Assistant integration, and uses modern tooling (Ruff, Hatchling, etc.).

## About

This package allows you to control and monitor Rako Controls devices
programmatically. It is mainly created to allow third-party programs to automate
their behavior.

## Installation

```bash
pip install python-rako-2025
```

## Usage

```python
import asyncio
import aiohttp
from python_rako import discover_bridge, Bridge


async def main():
    # Discover bridge on network
    bridge_info = await discover_bridge()
    print(f"Found bridge: {bridge_info}")

    # Create bridge instance
    bridge = Bridge(
        host=bridge_info["host"],
        port=bridge_info["port"],
        name=bridge_info["name"],
        mac=bridge_info["mac"]
    )

    # Get bridge information and discover devices
    async with aiohttp.ClientSession() as session:
        info = await bridge.get_info(session)
        print(f"Bridge version: {info.version}")

        # Discover all lights
        async for light in bridge.discover_lights(session):
            print(f"Found light: {light.title} (Room {light.room_id})")


if __name__ == "__main__":
    asyncio.run(main())
```

## Changelog & Releases

This repository keeps a change log using [GitHub's releases][releases]
functionality. The format of the log is based on
[Keep a Changelog][keepchangelog].

Releases are based on [Semantic Versioning][semver], and use the format
of ``MAJOR.MINOR.PATCH``. In a nutshell, the version will be incremented
based on the following:

- ``MAJOR``: Incompatible or major changes.
- ``MINOR``: Backwards-compatible new features and enhancements.
- ``PATCH``: Backwards-compatible bugfixes and package updates.

## Contributing

This is an active open-source project. We are always open to people who want to
use the code or contribute to it.

We've set up a separate document for our
[contribution guidelines](CONTRIBUTING.md).

Thank you for being involved! :heart_eyes:

## Setting up development environment

In case you'd like to contribute, a `Makefile` has been included to ensure a
quick start.

```bash
make venv
source ./venv/bin/activate
make dev
```

Now you can start developing, run `make` without arguments to get an overview
of all make goals that are available (including description):

```bash
$ make
Asynchronous Python client for Rako Controls Lighting.

Usage:
  make help                            Shows this message.
  make dev                             Set up a development environment.
  make lint                            Run Ruff linting and formatting checks.
  make format                          Format code with Ruff.
  make typecheck                       Run type checking with MyPy.
  make check                           Run all checks (linting, formatting, and type checking).
  make test                            Run tests quickly with the default Python.
  make coverage                        Check code coverage quickly with the default Python.
  make install                         Install the package to the active Python's site-packages.
  make clean                           Removes build, test, coverage and Python artifacts.
  make clean-all                       Removes all venv, build, test, coverage and Python artifacts.
  make clean-build                     Removes build artifacts.
  make clean-pyc                       Removes Python file artifacts.
  make clean-test                      Removes test and coverage artifacts.
  make clean-venv                      Removes Python virtual environment artifacts.
  make dist                            Builds source and wheel package.
  make release                         Release build on PyPI.
  make venv                            Create Python venv environment.
  make bump-patch                      Bump patch version (x.y.Z) and commit.
  make bump-minor                      Bump minor version (x.Y.z) and commit.
  make bump-major                      Bump major version (X.y.z) and commit.
```

## Authors & contributors

The original setup of this repository is by [Ben Marengo][marengaz].
Currently maintained by [Simon Leigh][simonleigh].

For a full list of all authors and contributors,
check [the contributor's page][contributors].

## License

[License](LICENSE)

[build-shield]: https://github.com/simonleigh/python-rako/workflows/Continuous%20Integration/badge.svg
[build]: https://github.com/simonleigh/python-rako/actions
[code-quality-shield]: https://img.shields.io/lgtm/grade/python/g/simonleigh/python-rako.svg?logo=lgtm&logoWidth=18
[code-quality]: https://lgtm.com/projects/g/simonleigh/python-rako/context:python
[codecov-shield]: https://codecov.io/gh/simonleigh/python-rako/branch/master/graph/badge.svg
[codecov]: https://codecov.io/gh/simonleigh/python-rako
[contributors]: https://github.com/simonleigh/python-rako/graphs/contributors
[marengaz]: https://github.com/marengaz
[simonleigh]: https://github.com/simonleigh
[keepchangelog]: http://keepachangelog.com/en/1.0.0/
[license-shield]: https://img.shields.io/github/license/simonleigh/python-rako.svg
[maintenance-shield]: https://img.shields.io/maintenance/yes/2025.svg
[project-stage-shield]: https://img.shields.io/badge/project%20stage-stable-green.svg
[releases-shield]: https://img.shields.io/github/release/simonleigh/python-rako.svg
[releases]: https://github.com/simonleigh/python-rako/releases
[semver]: http://semver.org/spec/v2.0.0.html
