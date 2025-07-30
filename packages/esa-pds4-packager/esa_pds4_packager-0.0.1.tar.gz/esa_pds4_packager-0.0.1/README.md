# ESA PDS4 Packager

[![PyPI](https://img.shields.io/pypi/v/esa-pds4-packager?style=flat-square)](https://pypi.python.org/pypi/esa-pds4-packager/)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/esa-pds4-packager?style=flat-square)](https://pypi.python.org/pypi/esa-pds4-packager/)
[![PyPI - License](https://img.shields.io/pypi/l/esa-pds4-packager?style=flat-square)](https://pypi.python.org/pypi/esa-pds4-packager/)
[![Coookiecutter - Wolt](https://img.shields.io/badge/cookiecutter-Wolt-00c2e8?style=flat-square&logo=cookiecutter&logoColor=D4AA00&link=https://github.com/woltapp/wolt-python-package-cookiecutter)](https://github.com/woltapp/wolt-python-package-cookiecutter)


---

**Documentation**: [https://luca-penasa.github.io/esa-pds4-packager](https://luca-penasa.github.io/esa-pds4-packager)

**Source Code**: [https://github.com/luca-penasa/esa-pds4-packager](https://github.com/luca-penasa/esa-pds4-packager)

**PyPI**: [https://pypi.org/project/esa-pds4-packager/](https://pypi.org/project/esa-pds4-packager/)

---



## Installation

```sh
pip install esa-pds4-packager
```

## Development

* Clone this repository
* Requirements:
  * [uv](https://docs.astral.sh/uv/)
  * Python 3.10+
* Create a virtual environment and install the dependencies

```sh
uv sync
```


### Testing

```sh
uv run pytest
```

### Documentation

The documentation is automatically generated from the content of the [docs directory](https://github.com/luca-penasa/esa-pds4-packager/tree/master/docs) and from the docstrings
 of the public signatures of the source code. The documentation is updated and published as a [Github Pages page](https://pages.github.com/) automatically as part each release.



### Releasing

#### Manual release

Releases are done with the command, e.g. incrementing patch:

```bash
uv run just bump patch
# also push, of course:
git push origin main --tags
```

this will update the changelog, commit it, and make a corresponding tag.

as the CI is not yet configured for publish on pypi it can be done by hand:

```bash
uv build
uv publish --build path/to/wheel
```
#### Automatic release - to be fixed


Trigger the [Draft release workflow](https://github.com/luca-penasa/esa-pds4-packager/actions/workflows/draft_release.yml)
(press _Run workflow_). This will update the changelog & version and create a GitHub release which is in _Draft_ state.

Find the draft release from the
[GitHub releases](https://github.com/luca-penasa/esa-pds4-packager/releases) and publish it. When
 a release is published, it'll trigger [release](https://github.com/luca-penasa/esa-pds4-packager/blob/master/.github/workflows/release.yml) workflow which creates PyPI
 release and deploys updated documentation.

### Updating with copier

To update the skeleton of the project using copier:
```sh
uvx copier update --defaults
```

### Pre-commit

Pre-commit hooks run all the auto-formatting (`ruff format`), linters (e.g. `ruff` and `mypy`), and other quality
 checks to make sure the changeset is in good shape before a commit/push happens.

You can install the hooks with (runs for each commit):

```sh
pre-commit install
```

Or if you want them to run only for each push:

```sh
pre-commit install -t pre-push
```

Or if you want e.g. want to run all checks manually for all files:

```sh
pre-commit run --all-files
```

---

This project was generated using [a fork](https://github.com/luca-penasa/wolt-python-package-cookiecutter) of the [wolt-python-package-cookiecutter](https://github.com/woltapp/wolt-python-package-cookiecutter) template.
