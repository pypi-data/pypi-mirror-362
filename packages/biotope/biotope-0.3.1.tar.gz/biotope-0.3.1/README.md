# biotope

|            |                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                         |
| ---------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Package    | [![Latest PyPI Version](https://img.shields.io/pypi/v/biotope.svg)](https://pypi.org/project/biotope/) [![Supported Python Versions](https://img.shields.io/pypi/pyversions/biotope.svg)](https://pypi.org/project/biotope/) [![Documentation](https://readthedocs.org/projects/biotope/badge/?version=latest)](https://biotope.readthedocs.io/en/latest/?badge=latest)                                                                                                                                                                                                                 |
| Meta       | [![MIT](https://img.shields.io/pypi/l/biotope.svg)](LICENSE) [![Code of Conduct](https://img.shields.io/badge/Contributor%20Covenant-v2.0%20adopted-ff69b4.svg)](.github/CODE_OF_CONDUCT.md) [![Checked with mypy](https://www.mypy-lang.org/static/mypy_badge.svg)](https://mypy-lang.org/) [![Code Style Black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black) [![Linting: Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/charliermarsh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff) |
| Automation |                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                         |

_CLI integration for BioCypher ecosystem packages_

Status: early alpha, volatile, partly vibe-coded

Documentation [here](https://biocypher.github.io/biotope/latest/), may be incomplete.

Currently discussed [here](https://github.com/orgs/biocypher/discussions/9).

## Metadata Management — Main Usage

The `biotope` CLI provides a unified interface for managing scientific datasets and metadata in the BioCypher ecosystem. It supports project initialization, data staging, metadata annotation, version control, and more.
Here we describe the metadata management functionality, the most mature aspect of the package.
Most other functionality is in prototype stage.

### Typical Workflow

```bash
# 1. Initialize a new biotope project (with Git integration)
biotope init

# 2. Add local data files for annotation and tracking
biotope add data/raw/experiment.csv

#    Or download and stage remote files
biotope get https://example.com/data/experiment.csv

# 3. Check project status and staged files
biotope status

# 4. Create or complete metadata annotations
biotope annotate interactive --staged
#    Or complete incomplete annotations
biotope annotate interactive --incomplete

# 5. Commit metadata changes to version control
biotope commit -m "Add experiment dataset"

# 6. View project history
biotope log --oneline

# 7. Push or pull metadata to/from remote repositories
biotope push
biotope pull

# 8. Verify data integrity
biotope check-data
```

### Available Commands

- `biotope init` – Initialize a new project with Git integration.
- `biotope add` – Stage local data files for annotation and version control.
- `biotope get` – Download and stage remote files for annotation.
- `biotope status` – Show the current status of your project and staged files.
- `biotope annotate` – Create, complete, or validate metadata using the Croissant ML schema.
- `biotope commit` – Commit metadata changes using Git.
- `biotope log` – View the commit history of your project.
- `biotope push` / `biotope pull` – Share metadata with remote repositories.
- `biotope check-data` – Verify data integrity using checksums.
- `biotope build`, `biotope chat`, `biotope read`, `biotope view` – Additional tools for building knowledge representations, chatting with your project, extracting information, and visual analysis.

For more details and advanced usage, see the [full documentation](https://biocypher.github.io/biotope/latest/).

## Copyright

- Copyright © 2025 Sebastian Lobentanzer.
- Free software distributed under the [MIT License](./LICENSE).
