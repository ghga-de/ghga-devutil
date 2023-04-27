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
import http.server
import os
import shlex
import shutil
import socketserver
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


def set_directory_navigation(content_outdir: Path):
    """
    |-- <content directory>
        |-- communications
            |-- _index.md
        |-- services
            |-- _index.md
    """

    # Prepare "communications" for all-in-one service pages
    communications_dir = content_outdir / "communications"
    shutil.rmtree(communications_dir, ignore_errors=True)
    communications_dir.mkdir(parents=True)
    (communications_dir / "_index.md").touch()  # empty _index.md for nav menu

    # Prepare "services" for individual service pages
    services_dir = content_outdir / "services"
    shutil.rmtree(services_dir, ignore_errors=True)
    services_dir.mkdir(parents=True)
    (services_dir / "_index.md").touch()  # empty _index.md for nav menu


def run_web_server(outdir, theme: str, local: bool = False):
    """Start web server or build static files for deployment"""

    cmd = f"hugo --theme {shlex.quote(theme)}"
    if local:
        cmd = cmd + " --baseURL /"

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

        if local:
            _port = 8000
            web_directory = str(Path(outdir / "public"))

            class Handler(http.server.SimpleHTTPRequestHandler):
                """Define a Handler that can accept a directory parameter."""

                def __init__(self, *args, **kwargs):
                    super().__init__(*args, directory=web_directory, **kwargs)

            try:
                with socketserver.TCPServer(("", _port), Handler) as httpd:
                    msg.info(
                        f"Documentation is being served on http://localhost:{_port}."
                    )
                    httpd.serve_forever()
            except KeyboardInterrupt:
                msg.info("\nShutting down the server...")
                httpd.shutdown()
                msg.info("Server shut down successfully.")
