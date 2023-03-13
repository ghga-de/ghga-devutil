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

"""GHGA Dev Util Exceptions"""

from pathlib import Path
from typing import Union

import yaml.parser
from pydantic import ValidationError


class OutputFileExistsError(RuntimeError):
    """Raised when an output file exists and force was not specified."""

    def __init__(self, path: Path):
        super().__init__(f"The output path '{path}' already exists.")


class ServiceFileValidationError(RuntimeError):
    """Raised when a service specification file could not be parsed."""

    def __init__(
        self, path: Path, val_error: Union[ValidationError, yaml.parser.ParserError]
    ):
        super().__init__(
            f"The service file '{path}' could not be read. "
            f"Not a valid service specification: {val_error}"
        )
