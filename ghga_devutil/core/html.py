# Copyright 2021 - 2023 Universität Tübingen, DKFZ, EMBL, and Universität zu Köln
# for the German Human Genome-Phenome Archive (GHGA)
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

"""Web interface build for annotated services."""
import os
import shlex
import shutil
from pathlib import Path
from subprocess import PIPE, CalledProcessError, run  # nosec

import git

from ghga_devutil.core import cli_message as msg
from ghga_devutil.core.exceptions import ThemeDownloadError


def git_clone_theme(theme, outdir: Path):
    """Clone theme from Repo and overwrite theme directory"""
    name, theme_url = theme.name, theme.url
    theme_dir = outdir / f"themes/{name}"

    # Remove previous to start anew
    shutil.rmtree(theme_dir, ignore_errors=True)

    try:
        git.Repo.clone_from(theme_url, str(theme_dir))
    except git.GitCommandError as error:
        msg.err(error)
        raise ThemeDownloadError(error) from error


def verify_site_directory(outdir, file_name: str = "config.toml"):
    """Check outdir exist and contains Hugo config. Otherwise create."""
    outdir.mkdir(parents=True, exist_ok=True)

    config_path = Path(outdir / file_name)
    if not config_path.exists():
        msg.warn(f"Unable to locate config file in {outdir}.")

        with open(config_path, "w", encoding="utf-8") as file:
            file.write("title = 'GHGA Integration Documentation'\n")
            msg.info(f"{config_path} created.")


def run_web_server(outdir, theme: str, local: bool = False):
    """Start web server or build static files for deployment"""

    if local:
        cmd = f"hugo server --theme {shlex.quote(theme)} --port 1313"
    else:
        cmd = f"hugo --theme {shlex.quote(theme)}"

    try:
        msg.info(f"Running... `{cmd}`")
        result = run(
            shlex.split(cmd),
            cwd=os.path.abspath(outdir),
            check=True,
            shell=False,
            stdout=PIPE,
        )
    except CalledProcessError as error:
        msg.err(f"Unable to build: {error}")
    else:
        msg.info(result.stdout.decode("utf-8").strip("\n"))
