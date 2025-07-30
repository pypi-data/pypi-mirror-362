# biotope

|            |                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                         |
| ---------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Package    | [![Latest PyPI Version](https://img.shields.io/pypi/v/biotope.svg)](https://pypi.org/project/biotope/) [![Supported Python Versions](https://img.shields.io/pypi/pyversions/biotope.svg)](https://pypi.org/project/biotope/) [![Documentation](https://readthedocs.org/projects/biotope/badge/?version=latest)](https://biotope.readthedocs.io/en/latest/?badge=latest)                                                                                                                                                                                                                 |
| Meta       | [![MIT](https://img.shields.io/pypi/l/biotope.svg)](LICENSE) [![Code of Conduct](https://img.shields.io/badge/Contributor%20Covenant-v2.0%20adopted-ff69b4.svg)](.github/CODE_OF_CONDUCT.md) [![Checked with mypy](https://www.mypy-lang.org/static/mypy_badge.svg)](https://mypy-lang.org/) [![Code Style Black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black) [![Linting: Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/charliermarsh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff) |
| Automation |                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                         |

_CLI integration for BioCypher ecosystem packages_

Status: early alpha, volatile

Currently discussed [here](https://github.com/orgs/biocypher/discussions/9)

## Metadata annotation using Croissant, short guide

The `biotope` package features a metadata annotation assistant using the recently introduced [Croissant](https://research.google/blog/croissant-a-metadata-format-for-ml-ready-datasets/) schema. It is available as the `biotope annotate` module. Usage:

```
pip install biotope
biotope annotate interactive
```

After creation, `biotope` can also be used to validate the JSON-LD (CAVE: being a prototype, biotope does not yet implement all croissant fields):

```
biotope annotate validate –jsonld <file_name.json>
```

`biotope` also has the method `biotope annotate create` to create metadata files from CLI parameters (no interactive mode) and `biotope annotate load` to load an existing record (the use of this is not well-defined yet). Obvious improvements would be to integrate file download (something like `biotope annotate get`) with automatic annotation functionalities, and the integration of LLMs for the further automation of metadata annotations from file contents (using the `biochatter` module of `biotope`).

Unit tests to inform about further functions and details can be found at https://github.com/biocypher/biotope/blob/main/tests/commands/test_annotate.py


## Copyright

- Copyright © 2025 Sebastian Lobentanzer.
- Free software distributed under the [MIT License](./LICENSE).
