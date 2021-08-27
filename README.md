# ndj_cookie

This repo is my personal python project cookie-cutter.
It contains my favourite tools and options for creating python projects for data science, web development, and adhoc projects.
While this is intended to be a personal resource, this is open to public users.

The cookie-cutter includes the following tools:

- Handy git files i.e. gitignore, codeowners, templates, github actions
- Initial documentation README, standard git docs, sphinx documentation
- Automations including pre-commit, nox
- Dependency and virtual environment management with poetry, (conda) or (docker-compose)
- Warmed up project example with logging, imports, and argparse

# Getting started

## 1. Use (cookie-cutter) or github to copy repo.

## 2. Instantiate pre-commit, add log directory, create git repo

```bash
pre-commit install
git init
git add .
git add logs/.gitkeep --force
git commit -m "initial commit"
git tag 0.1.0
```

Create a repo in github and follow instructions to push (including tags)

## 3. Choose any of poetry, conda or docker-compose for project. (NOTE: only poetry available at this stage)

### Poetry

Make sure you deactivate any existing virtual environments (i.e. conda).

```bash
poetry install
```

You may need to point poetry to the correct python interpreter using the following command.
In another terminal and in conda, run `which python`.
```bash
poetry env use /path/to/python3
```

Remove conda based material such as
- setup.py
- `my_project.__init__.py:VERSION`


### Conda

```bash
conda create --name my_project
...
conda env export > environment.yml
```

Setup project details in `setup.py`.


### Docker-compose

```bash
docker-compose up
```

## 4. Setup online resources for Github actions

Check python version in noxfile and  Github actions

- Codecov
- pypi and test-pypi
- Readthedocs

## 5. Other cleanup

Change name from my_project to new name in:

- project folder name
- README
- .flake8
- mypy.ini
- pyproject.toml


==================

# my_project

What is it, at a high high level?
Who is the audience or end users? Any requirements?
What are the feature and benefits?

# Instructions for users

The following are the quick start instructions for using/consuming assets such as the library or project cookiecutter.
Instructions for developers follows this section.

# Instructions for developers

### Dependencies and virtual env (conda)

```bash
conda env create -f environment.yml
conda activate my_project
```

Packaging and publishing (conda, setup.py), details to be added TODO.

### Dependencies and virtual env (poetry)

`poetry install`

### Pre-commit

On first time use of the repository, pre-commit will need to be installed locally. You can use the following command to run pre-commit over all files and install.

``` bash
pre-commit run --all-files
```

### Install library for adhoc development testing

setup.py can be used to generate a python wheel, or install the library for local usage.
It is useful to run this step before working on project code.

```bash
python setup.py bdist_wheel
```

```bash
python setup.py develop
```

## Manage sphinx documentation

`poetry run nox -s docs`

## Nox for task

Following can be used to run mypy, lint, and tests.
Recommended to use pre-commit for black.

```bash
poetry run nox
poetry run nox -s black safety pytype typeguard coverage xdoctest docs autoflake
```

# Contributors

Copyright © 2021 by Nick Jenkins. All rights reserved

See [CONTRIBUTING.md](CONTRIBUTING.md) and [LICENSE](LICENSE) for more info.
