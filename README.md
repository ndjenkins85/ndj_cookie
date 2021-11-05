# Python project quick start

This repo is my personal python project quick starter.
It contains my favourite tools and options for creating python projects for data science, web development, and adhoc projects.
While this is intended to be a personal resource, this is open to public users.

The quick-start includes the following features:

- Full set-up guide and checklist - *so you can quickly set up tooling and get into coding*
- Choice of dependency and virtual environment management with full-featured poetry workflow or partial conda workflow - *so you can ensure code runs on different environments*
- Pre-populated Git and Github assets including gitignore, codeowners, templates, issue labels - *to make your Github experience more enjoyable*
- Documentation including README with prompts, opinionated CONTRIBUTORS guide, LICENSE, sphinx docs generation with markdown and API reference support, and actions to automatically generate Github pages - *to easily expose project documentation*
- CI/CD framework including pre-commit for quick formatting, task automation with Nox, and Github Actions - *to ensure high quality releases*
- Linting, type checking, and tests with minimum of tool config files and close nox and pyproject.toml integration - *to standardize code and minimize clutter*
- Tools for release management including tagging and versioning process, Github actions for release notes, test-pypi and release actions - *to simplify the code release process*
- 'my_project' dummy project example with logging, imports, pytest, argparse CLI, poetry scripts, docstrings - *for a minimal non-tool codeset with warmed up examples*

This guide contains three major sections:

* [About this repo](#python-project-quick-start). General info about this repo.
* [Setup new repo](#instructions-for-copying-to-set-up-new-project). Instructions for copying this repo to create a new project.
* [README Template](#my-project). Warmed up README template for new projects with writing prompts, instructions for usage and development.

The following sources have been inspiration for creating my own project quick starter.

* [Hypermodern python](https://cjolowicz.github.io/posts/hypermodern-python-01-setup/)
* [SQLmodel](https://github.com/tiangolo/sqlmodel)
* [Project blueprint](https://github.com/johnthagen/python-blueprint)

# Instructions for copying to set up new project

## 1. Clone repo

Clone repo locally and delete the `.git` directory to start fresh.

## 2. Pre-use editing

- Edit the `my_project.__init__.py` to revert to version `0.1.0`.
- Rename `my_project` package name and imports
- Edit the `README.md` to include [my project](#my-project) onwards.
- Check python and library versions in noxfile
- Check python and library versions, and branch name in Github actions
- Change [LICENSE](LICENSE) as required. Use [this guide](https://github.com/Lucas-C/pre-commit-hooks#removing-old-license-and-replacing-it-with-a-new-one) to redo licenses across project

Change name from my_project to new name in:

- `README.md`
- `CONTRIBUTING.md`
- `.flake8`
- `pyproject.toml`
- `docs/conf.py`
- `setup.py`
- `tests/test_utils.py`
- `Dockerfile`
- `docker-compose.yml`

## 3. Choose any of poetry, conda (or docker-compose) for project.

### Poetry

Ensure you have and installation of Poetry 1.2.0a1 or above, along with poetry-version-plugin.

Make sure you deactivate any existing virtual environments (i.e. conda).

```bash
poetry install
```

You may need to point poetry to the correct python interpreter using the following command.
In another terminal and in conda, run `which python`.
```bash
poetry env use /path/to/python3
```

Enter the poetry shell.

```bash
poetry shell
```

Remove tools not required by poetry, but required for conda
- Delete `setup.py`
- Delete `docs/requirements.txt`
- Edit Conda references in `README.md`
- Dockerfile and docker-compose.yml

### Conda

*Note*: using conda will mean incompatability with some Nox, Github actions, and library publish functionality. Only the default Nox sessions are included (with light flake8 checks), plus black and docs.

```bash
conda env create -f environment.yml
conda activate my_project
```

Additional conda related setup:

* Setup project details in `setup.py`.
* Remove or update the following Github Actions:
  * coverage
  * release
  * test-pypi
  * tests
* Update project README specify conda instructions

### Docker-compose

`Dockerfile` and `docker-compose` are supported using poetry for dependencies.
See above instructions for conda cleanup.

```bash
docker-compose build
docker-compose up
docker-compose down
```

## 4. Instantiate pre-commit, add log directory, create new git repo

```bash
pre-commit install
git init
git add .
git add logs/.gitkeep --force
git commit -m "initial commit"
git tag 0.1.0
```

Create a repo in github and follow instructions to push (including tags).

Check if the branch name is `main` or `master` - Github Actions are set to use `main`.

## 5. Post push cleanup

- Setup Codecov connection
- Setup pypi and test-pypi secrets, uncomment test-pypi github action
- In Github repo set up dependabot and Github pages

# My Project

What is it, at a high high level?
Who is the audience or end users? Any requirements?
What are the feature and benefits?

* [Instructions for users](#instructions-for-users)
* [Instructions for developers](#instructions-for-developers)
  * [Dependency and virtual environment management, library development and build with poetry](#dependency-and-virtual-environment-management-library-development-and-build-with-poetry)
  * [Dependency and virtual environment management, library development and build with conda](#dependency-and-virtual-environment-management-library-development-and-build-with-conda)
  * [Code quality, testing, and generating documentation with Nox](#code-quality-testing-and-generating-documentation-with-nox)
  * [Code formatting with Pre-commit](#code-formatting-with-pre-commit)
* [Contributors](#contributors)

## Instructions for users

The following are the quick start instructions for using the project as an end-user.
[Instructions for developers](#instructions-for-developers) follows this section.

Note: Instructions marked with %% are not functioning and are for demo purposes only.

Install the project using pip %%:

```bash
pip install my_project
```

Include an example of running the program with expected outputs.

```bash
python -m my_project.utils -i1 environment.yml -i2 environment.yml -v
...
2021-08-29 14:59:09,489 [DEBUG] Loading main file from environment.yml
2021-08-29 14:59:09,489 [DEBUG] Loading second file from environment.yml
...
  - pytest-cov=2.10.1
  - python=^3.8
  - sphinx=3.2.1
  - sphinx-autodoc-typehints=1.12.0
  - sphinx_rtd_theme=0.4.3
```

Can also be run as a script.

```bash
my_project -i1 environment.yml -i2 environment.yml -v
```

### Using Dockerfile

Alternatively run from Dockerfile:

``` bash
docker build -t ndj_cookie/my_project .
docker run --rm ndj_cookie/my_project
docker stop $(docker ps -a -q)
```

### Using docker-compose

Example docker-compose also included.

``` bash
docker-compose build
docker-compose up
docker-compose down
```

## Instructions for developers

The following are the setup instructions for developers looking to improve this project.
For information on current contributors and guidelines see the [contributors](#contributors) section.
Follow each step here and ensure tests are working.

### Dependency and virtual environment management, library development and build with poetry

Ensure you have and installation of Poetry 1.2.0a1 or above, along with poetry-version-plugin.

Make sure you deactivate any existing virtual environments (i.e. conda).

```bash
poetry install
```

You may need to point poetry to the correct python interpreter using the following command.
In another terminal and in conda, run `which python`.
```bash
poetry env use /path/to/python3
```

Library can be built using

```bash
poetry build
```

### Dependency and virtual environment management, library development and build with conda

Following commands will create the conda environment and setup the library in interactive development mode using setup.py.

```bash
conda env create -f environment.yml
conda activate my_project
pip install -e .
```

Library can be built using

```bash
python setup.py bdist_wheel
```

### Code quality, testing, and generating documentation with Nox

Nox is a python task automation tool similar to Tox, Makefiles or scripts.

The following command can be used to run mypy, lint, and tests.
It is recommended to run these before pushing code, as this is run with Github Actions.
Some checks such as black are run more frequently with [pre-commit](#code-formatting-with-pre-commit).

```bash
poetry run nox
```

Local Sphinx documentation can be generated with the following command.
Documentation publishing using Github Actions to Github pages is enabled by default.

```bash
poetry run nox -s docs
```

Other available commands include:

```bash
poetry run nox -rs coverage
```

### Code formatting with Pre-commit

On first time use of the repository, pre-commit will need to be installed locally.
You can use the following command to install and run pre-commit over all files.
See .pre-commit-config.yaml for checks in use.
Intention is to have lightweight checks that automatically make code changes.

``` bash
pre-commit run --all-files
```

## Contributors

* [Nick Jenkins](https://www.nickjenkins.com.au) - Data Scientist, API & Web dev, Team lead, Writer

See [CONTRIBUTING.md](CONTRIBUTING.md) in Github repo for specific instructions on contributing to project.

Usage rights governed by [LICENSE](LICENSE)  in Github repo or page footer.
