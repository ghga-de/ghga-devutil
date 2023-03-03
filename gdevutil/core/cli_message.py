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

"""Command line message functionality."""

from typing import Union

from rich.console import Console

console = Console(stderr=False)
err_console = Console(stderr=True)


def err(message: Union[str, BaseException]) -> None:
    """Print an error message."""
    err_console.print(message, style="red")


def info(message: str) -> None:
    """Print an info message."""
    console.print(message, style="white")


def warn(message: str) -> None:
    """Print a warning message"""
    err_console.print(message, style="yellow")
