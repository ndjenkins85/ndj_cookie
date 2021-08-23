"""Nox for python task automation.

nox.option.sessions is default run for 'nox' on command line inc:
    * lint: python linting
    * mypy^: strict variable type checking
    * pytype:
    * tests (pytest^): runs our test suite

Additional options:
    * black^: codestyle alignment
    * safety^: security checks
    * typeguard: strict type checking of functions
    * coverage: in addition to tests, tells us how much code coverage
    * xdoctest^: any code snippets in docstrings are run for correctness
    * docs: (re)-build documentation

^ can also be run directly from CLI without nox
"""
import tempfile
from typing import Any

import nox
from nox.sessions import Session

locations = "my_project", "tests", "noxfile.py", "docs/conf.py"
nox.options.sessions = "mypy", "lint", "tests"
package = "my_project"


def install_with_constraints(session: Session, *args: str, **kwargs: Any) -> None:
    """Install packages constrained by Poetry's lock file."""
    with tempfile.NamedTemporaryFile() as requirements:
        session.run(
            "poetry", "export", "--dev", "--format=requirements.txt", f"--output={requirements.name}", external=True
        )
        session.install(f"--constraint={requirements.name}", *args, **kwargs)


def install_with_constraints_nohash(session: Session, *args: str, **kwargs: Any) -> None:
    """Install packages constrained by Poetry's lock file."""
    with tempfile.NamedTemporaryFile() as requirements:
        session.run(
            "poetry",
            "export",
            "--dev",
            "--format=requirements.txt",
            "--without-hashes",
            f"--output={requirements.name}",
            external=True,
        )
        session.install(f"--constraint={requirements.name}", *args, **kwargs)


@nox.session(python="3.8")
def black(session: Session) -> None:
    """Run black code formatter."""
    args = session.posargs or locations
    install_with_constraints_nohash(session, "black")
    session.run("black", *args)


@nox.session(python=["3.8"])
def lint(session: Session) -> None:
    """Lint using flake8."""
    args = session.posargs or locations
    install_with_constraints_nohash(
        session,
        "flake8",
        "flake8-annotations",
        "flake8-bandit",
        "flake8-black",
        "flake8-bugbear",
        "flake8-docstrings",
        "flake8-import-order",
        "darglint",
    )
    session.run("flake8", *args)


@nox.session(python="3.8")
def safety(session: Session) -> None:
    """Scan dependencies for insecure packages."""
    with tempfile.NamedTemporaryFile() as requirements:
        session.run(
            "poetry",
            "export",
            "--dev",
            "--format=requirements.txt",
            "--without-hashes",
            f"--output={requirements.name}",
            external=True,
        )
        install_with_constraints_nohash(session, "safety")
        session.run("safety", "check", f"--file={requirements.name}", "--full-report")


@nox.session(python=["3.8"])
def mypy(session: Session) -> None:
    """Type-check using mypy."""
    args = session.posargs or locations

    install_with_constraints_nohash(session, "mypy")
    session.run("mypy", *args)


@nox.session(python="3.8")
def pytype(session: Session) -> None:
    """Type-check using pytype."""
    args = session.posargs or ["--disable=import-error", *locations]
    install_with_constraints_nohash(session, "pytype")
    session.run("pytype", *args)


@nox.session(python=["3.8"])
def tests(session: Session) -> None:
    """Run the test suite."""
    # Updated with fix from:
    # https://stackoverflow.com/questions/59768651/how-to-use-nox-with-poetry
    args = session.posargs or ["--cov", "-m", "not e2e"]
    session.install(".")
    install_with_constraints_nohash(session, "coverage[toml]", "pytest", "pytest-cov", "pytest-mock")
    session.run("pytest", *args)


@nox.session(python=["3.8"])
def typeguard(session: Session) -> None:
    """Runtime type checking using Typeguard."""
    args = session.posargs or ["-m", "not e2e"]
    session.install(".")
    install_with_constraints_nohash(session, "pytest", "pytest-mock", "typeguard")
    session.run("pytest", f"--typeguard-packages={package}", *args)


@nox.session(python="3.8")
def coverage(session: Session) -> None:
    """Upload coverage data."""
    install_with_constraints_nohash(session, "coverage[toml]", "codecov")
    session.run("coverage", "xml", "-i", "--fail-under=0")
    session.run("codecov", *session.posargs)


@nox.session(python=["3.8"])
def xdoctest(session: Session) -> None:
    """Run examples with xdoctest."""
    args = session.posargs or ["all"]
    session.install(".")
    # session.run("poetry", "install", "--no-dev", external=True)
    install_with_constraints_nohash(session, "xdoctest")
    session.run("python", "-m", "xdoctest", package, *args)


@nox.session(python="3.8")
def docs(session: Session) -> None:
    """Build the documentation."""
    session.install(".")
    # session.run("poetry", "install", "--no-dev", external=True)
    install_with_constraints_nohash(session, "sphinx", "sphinx-autodoc-typehints", "m2r2", "sphinx_rtd_theme")
    session.run("rm", "-rf", "docs/_build")
    session.run("sphinx-build", "docs", "docs/_build", *session.posargs)
