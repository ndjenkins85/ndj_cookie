# Copyright © 2021 by Nick Jenkins. All rights reserved

"""Sphinx configuration."""
from pathlib import Path

import sphinx_rtd_theme  # noqa: F401

project = "{{project_name}}"
author = "Nick Jenkins"

copyright = open(Path("..", "LICENSE")).read()
extensions = ["sphinx.ext.autodoc", "sphinx.ext.napoleon", "sphinx_autodoc_typehints", "m2r2", "sphinx_rtd_theme"]
source_suffix = [".rst", ".md"]
html_theme = "sphinx_rtd_theme"
