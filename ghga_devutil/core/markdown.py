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

"""Markdown representation of annotated services."""

from datetime import datetime, timezone
from typing import Mapping

from jinja2 import Environment, PackageLoader, select_autoescape

from ghga_devutil.core.models import AnnotatedService


def generate_markdown(
    services: Mapping[str, AnnotatedService], service_key: str
) -> str:
    """Generates markdown from service"""
    # Load jinja2 template
    env = Environment(
        loader=PackageLoader("ghga_devutil"), autoescape=select_autoescape()
    )
    template = env.get_template("service_page.md.jinja2")
    template.globals["cur_time"] = lambda: datetime.now(tz=timezone.utc)
    template.globals["service_title"] = lambda service: service.name.replace(
        "-", " "
    ).title()

    # Render markdown
    return template.render(services=services, service_key=service_key)
