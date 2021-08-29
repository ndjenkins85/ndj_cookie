# Copyright © 2021 by Nick Jenkins. All rights reserved
#
# Permission is hereby granted, free of charge, to any person obtaining a
# copy of this software and associated documentation files (the "Software"),
# to deal in the Software without restriction, including without limitation
# the rights to use, copy, modify, merge, publish, distribute, sublicense,
# and/or sell copies of the Software, and to permit persons to whom the
# Software is furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS
# OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL
# THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
# FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
# DEALINGS IN THE SOFTWARE.

"""Utility functions for modeling, data processing and one time use def tools."""
import argparse
import logging
from pathlib import Path
from typing import Union


def update_environments(
    main_env: Union[Path, str] = "environment.yml", opt_env: Union[Path, str] = "environment2.yml"
) -> None:
    """Utility to assist updating the project environment.yml.

    If we simply do `conda env export > environment2.yml` we will obtain every
    library, not just the key ones we select for inclusion. This can make knowing
    the subset of key libraries difficult, and reduce chances of successful env
    replication.

    This util takes the current environment.yml (with current hashes
    and # commented libraries)* and an environment.yml which is generated
    by above command, and prints the minimal set of libraries needed.

    * While experimenting with new libraries, it can be useful to mark the new
    libraries as a comment in the file until ready to include.

    Args:
        main_env: path as string
        opt_env: path as string
    """
    input_path = Path(main_env)
    logging.debug(f"Loading main file from {input_path}")
    with open(input_path, "r") as f:
        env = f.readlines()

    # Get simple library names from normal environment.yml
    libraries = []
    for x in env:
        if ":" in x or "conda-forge" in x or "defaults" in x:
            continue
        if "- " in x:
            x = x.split("- ")[1]
        if "# " in x:
            x = x.split("# ")[1]
        if "=" in x:
            x = x.split("=")[0]
        if "\n" in x:
            x = x.split("\n")[0]
        libraries.append(x)

    # Loads the full export
    input_path = Path(opt_env)
    logging.debug(f"Loading second file from {input_path}")
    with open(input_path, "r") as f:
        env = f.readlines()

    # Parse the full export to look for exact matches
    keep_libraries = []
    for line in env:
        line_good = False
        for lib in libraries:
            if "- " in line and "=" in line:
                line_segment = line.split("- ")[1].split("=")[0]
                if lib == line_segment:
                    line_good = True

        if line_good:
            keep_libraries.append(line)

    # Print the subset of environment
    print("".join(keep_libraries))


def start():
    parser = argparse.ArgumentParser("Conda environment management util")
    parser.add_argument("-i1", help="Path to main environment.yml")
    parser.add_argument("-i2", help="Path to opt environment2.yml")
    parser.add_argument("-v", action="store_true", help="Debug mode")
    args = parser.parse_args()

    log_level = logging.DEBUG if args.v else logging.INFO
    log_path = Path("logs", "_log.txt")
    try:
        logging.basicConfig(
            level=log_level,
            format="%(asctime)s [%(levelname)s] %(message)s",
            handlers=[logging.FileHandler(log_path), logging.StreamHandler()],
        )
    except FileNotFoundError:
        raise FileNotFoundError("'/logs/' directory missing, cannot create log files.")

    main_env = Path(args.i1)
    opt_env = Path(args.i2)
    update_environments(main_env=main_env, opt_env=opt_env)


if __name__ == "__main__":
    start()
