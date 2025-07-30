# diffify-lib

## For Developers

### Environment set up

From this directory (`./diffify-lib/` in the repository), to load the developer
environment for this package:

- Install `poetry`: `pip install poetry`
- Install the 'dev' dependencies: `poetry install`

Then activate the environment:

```bash
# poetry >= 2
source .venv/bin/activate
# poetry < 2
poetry shell
```

From here you can open VS code, and have the environment preloaded.

### Continuous Integration

We use the JR
[Common CI](https://gitlab.com/jumpingrivers/lib/templates/common-ci) routines
in GitLab CI runs. To update the template, use

```
copier copy https://gitlab.com/jumpingrivers/lib/templates/common-ci .
```

Note that we have additional routines beyond the Common CI core, for running
pytest, mypy and for deploying the package to PyPI.

## Tests

Unit tests can be ran without further set up:

```bash
pytest tests/unit
```

To run the integration tests, you'll need some environment variables defined:

- `S3_KEY_DEV`
- `S3_SECRET_DEV`
- `S3_BUCKET_DEV`
- `S3_URL_DEV`

Contact the diffify devs if you need these secrets. The simplest way to use
these secrets locally is to store them in a file `.dev.env` (do not add this
file to version control) and load that file into your working environment before
running the tests:

```bash
env $(cat .dev.env) pytest tests/unit tests/integration
```

Note that the integration tests will be run in GitLab's CI runners, so you may
not need to have access to these secrets.

### Version numbers

Any pull request that modifies the source code should have an associated version bump to the
package. When this happens you should change the version in two places:

- `[tool.poetry]` section of `pyproject.toml`
- `__version__` declaration in `diffify_lib/__init__.py`

A simple way to keep the version numbers in sync is to use:

```
poetry version patch|minor|major
```

This requires that `poetry-bumpversion` is installed alongside `poetry`.

### Pre-commit hooks

A pre-commit suite is defined in the root of this repository. You are strongly
advised to use these hooks during development. To register the hooks with your
local copy of the repository, run the following (from the repo-root):

```bash
# Install pre-commit itself
pip install pre-commit
# Install the hooks that pre-commit runs
pre-commit install
```

Now, `pre-commit` will run on your code at every commit, maintaining the style
and quality of the code.
