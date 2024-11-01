# Contributing to CompactRag

Welcome to clutchtimebot. These are the instructions for setting up
development environment for contributing to the project

**Table of Contents**
- [Setting Up Dev Environment](#setting-up-dev-environment)
  - [Installing PDM](#installing-pdm)
  - [Using Precommit Hooks](#using-precommit-hooks)

## Setting Up Dev Environment

In order to set up the development environment

### Installing PDM

In order to manage the python project dependencies we are using pdm.
So first you want to install pdm. This can be done using the install
documentation found on their website: [**PDM Documentation**](https://pdm-project.org/latest/#installation)

For linux:
```bash
# Install pdm
curl -sSL https://pdm-project.org/install-pdm.py | python3 -

# Check installation
pdm --version
```

Once you have pdm installed you will want to install all the necessary dependencies.

```bash
pdm install
```

### Using Precommit Hooks

In order to ensure that all our files are properly formatted we use ruff. These are installed as dev dependencies within your pdm
environment.

For convenience, the project uses pre-commit hooks to ensure that all the files
are properly formatted and linted before being committed to the codebase. Any PR that fail
the precommit hooks will be rejected. To install precommit configurations run the following
command.

```bash
# Install Hooks
pdm run pre-commit install

# Test installation
pdm run pre-commit run --all-files
```
