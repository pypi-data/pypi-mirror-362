# Iker's Python Setup Module

[![codecov](https://codecov.io/gh/ruyangshou/iker-python-setup/graph/badge.svg?token=W4D8HOPVED)](
https://codecov.io/gh/ruyangshou/iker-python-setup)

SCM/CI environment settings aware setup tool for Iker's Python projects

The Python package naming and versioning should comply with the [PEP 440](https://peps.python.org/pep-0440) and
[PEP 517](https://peps.python.org/pep-0517/) standards to ensure compatibility with the Python Package Index, as well as
various build front-ends and back-ends. Additionally, we aim to manage version updates using both the SCM and CI
systems, enabling for example automatic patch increments based on SCM branch information, CI build numbers, or release
tags.

To achieve this, we can utilize SCM branch information alongside CI-generated data injected into the build environment.
This approach requires the build process to dynamically determine the version string, taking into account both the local
version configuration (e.g., major and minor version numbers) and the CI runtime environment.

This package offers the necessary build tools to fulfill these requirements.

## Usage

To use this tool for managing the versioning of your Python package, follow these steps:

1. **Create a `VERSION` file** that maintains the major and minor version numbers. For example:
    ```
    1.0
    ```
2. **Modify the `pyproject.toml` file** as follows:
    ```toml
    [build-system]
    requires = [
        "setuptools>=68.0",
        "setuptools-scm>=8.0",
        "iker-python-setup>=1.0"  # This is required
    ]

    [project]
    dynamic = ["version"]  # This is required
    ```
3. **Use this tool in your `setup.py` script**:
    ```python
    from iker.setup import setup

    setup()
    ```

### Behaviors

The major and minor version numbers are read from the `VERSION` file located in the project’s root directory, while the
patch version number is sourced from the `BUILD_NUMBER` environment variable. These can be configured via the
`version_file` and `patch_env_var` parameters of the `setup` function. In a CI environment, the `patch_env_var` can be
set by the CI system.

For SCM settings, if the code is on the specified "base" branch, no additional segments will be appended to the version
string. Otherwise, a 12-character digest of the current commit will be appended to the version string. Additionally, if
there are uncommitted changes in the workspace, a `dirty` label will also be added, resulting in a final version string
format like `{major}.{minor}.{patch}+{digest}.dirty`.

An alternative approach for detecting the "base" branch is to use an environment variable specified by
`scm_branch_env_var`, which defaults to `GIT_BRANCH`. The "base" branch name, defaulting to `master`, is also
configurable.

```python
from iker.setup import setup

setup(
    version_file="MY_VERSION",
    patch_env_var="MY_ENV_VAR",
    scm_branch_name="main",
    scm_branch_env_var="MY_SCM_BRANCH"
)
```

## Build and Deploy

### Using Conda

We recommend using Conda. You need to install Anaconda packages from
the [official site](https://www.anaconda.com/products/distribution)

Create a Conda environment and install the modules and their dependencies in it

```shell
conda create -n iker python=3.13
conda activate iker

pip install .

conda deactivate
```

To remove the existing Conda environment (and create a brand new one)

```shell
conda env remove -n iker
```
