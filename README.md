# Python project quick start

This repo is my personal python project quick starter.
It contains my favourite tools and options for creating python projects for data science, web development, and adhoc projects.
While this is intended to be a personal resource, this is open to public users.

The quick-start includes the following features:

- Full set-up guide and checklist - *so you can quickly set up tooling and get into coding*
- Choice of dependency and virtual environment management with full-featured poetry workflow, partial conda workflow, and docker with poetry - *so you can ensure code runs on different environments*
- Pre-populated Git and Github assets including gitignore, codeowners, templates, issue labels - *to make your Github experience more enjoyable*
- Documentation including README with prompts, opinionated CONTRIBUTORS guide, LICENSE, sphinx docs generation with markdown and API reference support, and actions to automatically generate Github pages - *to easily expose project documentation*
- CI/CD framework including pre-commit for quick formatting, task automation with Nox, and Github Actions - *to ensure high quality releases*
- Linting, type checking, and tests with minimum of tool config files and close nox and pyproject.toml integration - *to standardize code and minimize clutter*
- Tools for release management including tagging and versioning process, Github actions for release notes, test-pypi and release actions - *to simplify the code release process*
- `my_project` dummy project example with logging, imports, pytest, argparse CLI, poetry scripts, docstrings - *for a minimal non-tool codeset with warmed up examples*
- `ndj_pipeline` machine learning pipeline and framework - *to separate data engineering concerns and build repeatable experiments*

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

See the [Environment 1: Poetry](#environment-1-poetry) in the Developer Guide to set up your own environment first.

Remove tools not required by poetry, but required for conda
- Delete `setup.py`
- Delete `docs/requirements.txt`
- Edit Conda references in `README.md`
- Dockerfile and docker-compose.yml

### Conda

See the [Environment 2: Conda](#environment-2-conda) in the Developer Guide to set up your own environment first.

*Note*: using conda will mean incompatability with some Nox, Github actions, and library publish functionality. Only the default Nox sessions are included (with light flake8 checks), plus black and docs.

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

See the [Environment 3: Docker](#environment-3-docker) in the Developer Guide to set up your own environment first.

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
  * [Installation](#installation)
  * [Usage documentation](#usage-documentation)
  * [Bug reports](#bug-reports)
* [Instructions for developers](#instructions-for-developers)
  * [Environment 1: Poetry](#environment-1-poetry)
  * [Environment 2: Conda](#environment-2-conda)
  * [Environment 3: Docker](#environment-3-docker)
  * [Testing with Nox](#testing-with-nox)
  * [Code formatting with Pre-commit](#code-formatting-with-pre-commit)
* [Contributors](#contributors)

## Instructions for users

The following are the quick start instructions for using the project as an end-user.

Follow the [Instructions for developers](#instructions-for-developers) to set up the virtual environment and dependency management.
We recommend `poetry`, but an alternative `conda` environment has been prepared (will not work with `nox`).

### Installation

Note: Instructions marked with %% are not functioning and are for demo purposes only.

Install the project using pip %%:

```bash
pip install my_project
```

Include an example of running the program with expected outputs.

To replicate the data transformations and model results, run the following commands from the project root.
These should be run from the `poetry shell`, or `conda` environment, or with the `poetry run` prefix.
```bash
python -m ndj_pipeline.transform
python -m ndj_pipeline.model -p data/doordash_pred.yaml
python -m ndj_pipeline.final_prediction_clean

```

This will produce a feature rich dataset in `data/processed`, model results and metrics under `data/doordash_pred`, and the formatted predictions file under `data_to_predict.csv`.

Example of using poetry to create scripts.

```bash
my_project -i1 environment.yml -i2 environment.yml -v
```

Alternatively run from Dockerfile or docker-compose.
See [Docker environment instructions](#environment-3-docker) for more details.

### Usage documentation

The user guides can be found on [github pages](https://ndjenkins85.github.io/ndj_cookie).
This includes overview of features, discussion of `ndj_pipeline` framework, and API reference.

### Bug reports

Please raise an [issue](https://github.com/ndjenkins85/ndj_cookie/issues) with `bug` label and I will look into it!

## Instructions for developers

The following are the setup instructions for developers looking to improve this project.
For information on current contributors and guidelines see the [contributors](#contributors) section.
Follow each step here and ensure tests are working.

### Environment 1: Poetry

[Poetry](https://python-poetry.org/docs/) handles virtual environment management, dev and optional extra libraries, library development, builds and publishing.

Ensure you have and installation of Poetry 1.1 or above.
Make sure you deactivate any existing virtual environments (i.e. conda).

```bash
poetry install
```

Troubleshooting: You may need to point poetry to the correct python interpreter using the following command.
In another terminal and in conda, run `which python`.
```bash
poetry env use /path/to/python3
```

When the environment is correctly installed, you can enter the virtual environment using `poetry shell`. Library can be built using `poetry build`.

### Environment 2: Conda

[Conda](https://docs.conda.io/projects/conda/en/latest/user-guide/getting-started.html) is a lightweight solution for Anaconda python users to handle virtual environment management and basic library specification.

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

### Environment 3: Docker

[Docker](https://www.docker.com/) goes beyond virtual environment management to virtualize the operating system itself. The docker container is specified through a Dockerfile and can be run with docker commands or docker-compose. Dependeny management is handled through poetry.

Use either of the following commands to setup and run the docker environment.

``` bash
docker build -t ndj_cookie/my_project .
docker run --rm ndj_cookie/my_project
docker stop $(docker ps -a -q)
```

Example docker-compose also included.

``` bash
docker-compose build
docker-compose up
docker-compose down
```

### Testing with Nox

[Nox](https://nox.thea.codes/en/stable/index.html) is a command-line tool that automates testing in multiple Python environments, similar to tox, Makefiles or scripts. Unlike tox, Nox uses a standard Python file for configuration.

Here it is used for code quality, testing, and generating documentation.

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

[Pre-commit](https://pre-commit.com/) is a framework for managing and maintaining multi-language pre-commit hooks.

It intercepts the `git commit` command to run checks of staged code before the commit is finalized.
The checks are specified in `.pre-commit-config.yaml`.
Checks in use are quick, pragmatic, and apply automatic formatting checks.
If checks fail, it is usually only a matter of re-staging the files (`git add`) and attempting to commit again.

The aim is to provide a lightweight way to keep some code standards automatically in line with standards.
This does not replace the need to run nox tests, although pre-commits will satisfy some of the nox test checks.

On first time use of the repository, pre-commit will need to be installed locally.
You will need to be in the `poetry shell` or `conda` environment.
Run the following command to perform a first time install.

```bash
pre-commit install
```

This will cache several code assets used in the checks.

When you have new code to commit, pre-commit will kick in and check the code.
Alternatively, you can run the following command to run for all files in repo.

``` bash
pre-commit run --all-files
```

## Contributors

* [Nick Jenkins](https://www.nickjenkins.com.au) - Data Scientist, API & Web dev, Team lead, Writer

See [CONTRIBUTING.md](CONTRIBUTING.md) in Github repo for specific instructions on contributing to project.

Usage rights governed by [LICENSE](LICENSE)  in Github repo or page footer.
