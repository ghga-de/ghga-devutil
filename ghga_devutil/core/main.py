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

"""Main program entrypoints used by the user interface"""

from pathlib import Path
from typing import List

from ghga_devutil.core.annotate import annotate_services
from ghga_devutil.core.io import load_service, write_service
from ghga_devutil.core.markdown import generate_complete_diagram, generate_markdown


def markdown(service_file_paths: List[Path], outdir: Path, force: bool):
    """Reads services from disk, annotates them jointly and generates individual
    markdown files representing their annotated state."""
    # Read services
    services = [load_service(in_path) for in_path in service_file_paths]

    # Annotate services
    ann_services = annotate_services(services)
    ann_services_map = {
        ann_service.shortname: ann_service for ann_service in ann_services
    }

    # Generate and write markdown representation
    for in_path, ann_service in zip(service_file_paths, ann_services):
        out_path = (outdir / in_path.name).with_suffix(".md")
        if not out_path.exists() or force:
            out_path.write_text(
                generate_markdown(
                    services=ann_services_map, service_key=ann_service.shortname
                )
            )

    diagram_out_path = (outdir / "service_communications").with_suffix(".md")
    if not diagram_out_path.exists() or force:
        diagram_out_path.write_text(
            generate_complete_diagram(services=ann_services_map)
        )


def annotate(service_file_paths: List[Path], outdir: Path, force: bool):
    """Reads services from disk and writes their annotated counterpart to a
    specified output directory. The output filenames are suffixed with
    '.annotated.yaml' and outputfile are overwritten if the force option is
    set."""
    # Read services
    services = [load_service(in_path) for in_path in service_file_paths]

    # Annotate services
    ann_services = annotate_services(services)

    # Write annotated services
    for in_path, ann_service in zip(service_file_paths, ann_services):
        write_service(
            service=ann_service,
            out_path=(outdir / in_path.name).with_suffix(".annotated.yaml"),
            force=force,
        )
