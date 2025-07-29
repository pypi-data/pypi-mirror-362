<!-- start docs-include-index -->

# Cookiecutter Python CLI App Demo

[![PyPI](https://img.shields.io/pypi/v/cookiecutter-python-cli-app-demo)](https://img.shields.io/pypi/v/cookiecutter-python-cli-app-demo)
[![Supported Python Versions](https://img.shields.io/pypi/pyversions/cookiecutter-python-cli-app-demo)](https://pypi.org/project/cookiecutter-python-cli-app-demo/)
[![pre-commit.ci status](https://results.pre-commit.ci/badge/github/sgraaf/cookiecutter-python-cli-app-demo/main.svg)](https://results.pre-commit.ci/latest/github/sgraaf/cookiecutter-python-cli-app-demo/main)
[![Test](https://github.com/sgraaf/cookiecutter-python-cli-app-demo/actions/workflows/test.yml/badge.svg)](https://github.com/sgraaf/cookiecutter-python-cli-app-demo/actions/workflows/test.yml)
[![Documentation Status](https://readthedocs.org/projects/cookiecutter-python-cli-app-demo/badge/?version=latest)](https://cookiecutter-python-cli-app-demo.readthedocs.io/en/latest/?badge=latest)
[![PyPI - License](https://img.shields.io/pypi/l/cookiecutter-python-cli-app-demo)](https://img.shields.io/pypi/l/cookiecutter-python-cli-app-demo)

Demo of https://github.com/sgraaf/cookiecutter-python-cli-app.

<!-- end docs-include-index -->

## Installation

<!-- start docs-include-installation -->

Cookiecutter Python CLI App Demo is available on [PyPI](https://pypi.org/project/cookiecutter-python-cli-app-demo/). Install with [uv](https://docs.astral.sh/uv/) or your package manager of choice:

```sh
uv tool install cookiecutter-python-cli-app-demo
```

<!-- end docs-include-installation -->

## Documentation

Check out the [Cookiecutter Python CLI App Demo documentation](https://cookiecutter-python-cli-app-demo.readthedocs.io/en/stable/) for the [User's Guide](https://cookiecutter-python-cli-app-demo.readthedocs.io/en/stable/usage.html) and [CLI Reference](https://cookiecutter-python-cli-app-demo.readthedocs.io/en/stable/cli.html).

## Usage

<!-- start docs-include-usage -->

Running `cookiecutter-python-cli-app-demo --help` or `python -m cookiecutter_python_cli_app_demo --help` shows a list of all of the available options and arguments:

<!-- [[[cog
import cog
from cookiecutter_python_cli_app_demo import cli
from click.testing import CliRunner
runner = CliRunner()
result = runner.invoke(cli.cli, ["--help"], terminal_width=88)
help = result.output.replace("Usage: cli", "Usage: cookiecutter-python-cli-app-demo")
cog.outl(f"\n```sh\ncookiecutter-python-cli-app-demo --help\n{help.rstrip()}\n```\n")
]]] -->
<!-- [[[end]]] -->

<!-- end docs-include-usage -->
