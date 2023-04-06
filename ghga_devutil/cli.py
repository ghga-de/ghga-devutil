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

"""Entrypoint of the package"""

from pathlib import Path
from typing import List

import typer

from ghga_devutil import core
from ghga_devutil.core import cli_message as msg
from ghga_devutil.core.exceptions import ServiceFileValidationError

cli = typer.Typer()


@cli.command(name="annotate")
def annotate(
    service_spec: List[Path] = typer.Argument(
        ..., help="A list of files to read service specifications from."
    ),
    out_dir: Path = typer.Argument(..., help="The output directory."),
    force: bool = typer.Option(default=False, help="Overwrite existing files."),
):
    """Annotate service specifications with consumer and producer references and
    configuration options."""
    try:
        core.annotate(service_file_paths=service_spec, outdir=out_dir, force=force)
    except (IOError, ServiceFileValidationError) as error:
        msg.err(error)


@cli.command(name="markdown")
def markdown(service_spec: List[Path], out_dir: Path, force: bool = False):
    """Annotates multiple services jointly and then creates individual markdown
    representations including inter-service references."""
    try:
        core.markdown(service_spec, out_dir, force)
    except (IOError, ServiceFileValidationError) as error:
        msg.err(error)


@cli.command(name="html")
def html(
    service_spec: List[Path],
    out_dir: Path = typer.Argument(..., help="The output directory. ex. html."),
    local: bool = typer.Option(
        default=False, help="Run local web server or build static files"
    ),
    update: bool = typer.Option(
        default=False,
        help="Skip directory, config and theme checks. Update content only.",
    ),
):
    """Annotate and generate markdowns for multiple services and save them into
    certain directory structure then run local web server or build static files
    for deployment. Connection is required to download the UI theme for
    the first time.
    """
    try:
        core.html(service_spec, out_dir, local, update)
    except (IOError, ServiceFileValidationError) as error:
        msg.err(error)
