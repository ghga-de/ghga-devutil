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

"""File IO for service descriptions"""


from pathlib import Path
from typing import Union

import yaml
import yaml.parser
from pydantic import ValidationError

from ghga_devutil.core.exceptions import (
    OutputFileExistsError,
    ServiceFileValidationError,
)
from ghga_devutil.core.models import AnnotatedService, Service


def load_service(path: Path) -> Service:
    """Loads a service from a file"""
    try:
        obj = yaml.safe_load(path.read_bytes())
        return Service.parse_obj(obj)
    except (yaml.parser.ParserError, ValidationError) as error:
        raise ServiceFileValidationError(path, error) from None


def write_service(
    service: Union[Service, AnnotatedService], out_path: Path, force: bool = False
) -> None:
    """Write a service to file"""
    if out_path.exists() and not force:
        raise OutputFileExistsError(out_path)
    out_path.write_text(yaml.dump(service.dict()))
