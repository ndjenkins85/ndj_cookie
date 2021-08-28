# ndj_cookie

This repo is my personal python project quick starter.
It contains my favourite tools and options for creating python projects for data science, web development, and adhoc projects.
While this is intended to be a personal resource, this is open to public users.

The quick-start includes the following features:

- Handy git files i.e. gitignore, codeowners, templates
- Initial documentation README, standard git project docs, sphinx documentation for static and API reference
- Automations including pre-commit, nox, github actions
- Dependency and virtual environment management with poetry or conda (or docker-compose TBC)
- Warmed up project example with logging, imports, pytest, and argparse CLI

This README contains three major sections:

* [About this repo](#ndj_cookie). General info about this repo.
* [Setup new repo](#Instructions-for-copying-to-set-up-new-project). Instructions for copying this repo to create a new project.
* [README Template](#my_project). Warmed up README template for new projects with writing prompts, instructions for usage and development.

The following sources have been inspiration for creating my own project quick starter.

* [Hypermodern python](https://cjolowicz.github.io/posts/hypermodern-python-01-setup/)
* [SQLmodel](https://github.com/tiangolo/sqlmodel)
* [Project blueprint](https://github.com/johnthagen/python-blueprint)

# Instructions for copying to set up new project

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

Ensure you have Poetry 1.2.0a1 or above, along with poetry-version-plugin.

Make sure you deactivate any existing virtual environments (i.e. conda).

```bash
poetry install
```

You may need to point poetry to the correct python interpreter using the following command.
In another terminal and in conda, run `which python`.
```bash
poetry env use /path/to/python3
```

Remove tools not required by poetry, but required for conda
- setup.py
- `docs/requirements.txt`

### Conda

```bash
conda create --name my_project
...
conda env export > environment.yml
```

* Setup project details in `setup.py`.
* Nox functions need to be changed to Conda (`noxfile.py:black_conda_example`)
* Create new Github Actions (currently using poetry)

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

* [Instructions for users](#instructions-for-users)
* [Instructions for developers](#instructions-for-developers)
* [Contributors](#contributors)

# Instructions for users

The following are the quick start instructions for using the library as an end-user.
[Instructions for developers](#instructions-for-developers) follows this section.

# Instructions for developers

The following are the setup instructions for developers looking to improve this project.
For information on current contributors and guidelines see the [contributors](#contributors) section.

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
