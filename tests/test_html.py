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

import shutil
import tempfile
from pathlib import Path

import pytest

from ghga_devutil.core.exceptions import ThemeDownloadError
from ghga_devutil.core.html import git_clone_theme, verify_site_directory
from ghga_devutil.core.models import Theme


def test_git_clone_theme():
    """Test whether theme cloned correctly"""

    theme = Theme()

    # Test Theme model default values
    assert theme.name == "hugo-book"
    assert theme.url == "https://github.com/alex-shpak/hugo-book"

    outdir = Path(tempfile.mkdtemp())

    git_clone_theme(theme, outdir)

    assert (outdir / f"themes/{theme.name}").exists() is True
    assert (outdir / f"themes/{theme.name}/README.md").exists() is True

    # Run again to test already exist theme, results must be same

    git_clone_theme(theme, outdir)

    assert (outdir / f"themes/{theme.name}").exists() is True
    assert (outdir / f"themes/{theme.name}/README.md").exists() is True

    # Remove temp dir
    shutil.rmtree(outdir)


def test_git_clone_theme_error():
    """Test cloning the theme raises error when URL is broken"""

    theme = Theme(name="dummy theme", url="https://broken-url")

    # Test Theme model default values
    assert theme.name == "dummy theme"
    assert theme.url == "https://broken-url"

    outdir = Path(tempfile.mkdtemp())

    # Test broken URL must give error
    with pytest.raises(ThemeDownloadError):
        git_clone_theme(theme, outdir)

    # Remove temp dir
    shutil.rmtree(outdir)


def test_verify_site_directory():
    """Test site directory verification"""

    # Call verify directory
    outdir = Path(tempfile.mkdtemp())
    verify_site_directory(outdir)

    assert outdir.exists() is True
    assert (outdir / "config.toml").exists() is True

    # Check verified directory contains config with default content
    with open(str(outdir / "config.toml"), "r") as file:
        assert file.read() == "title = 'GHGA Integration Documentation'\n"

    # Remove temp dir
    shutil.rmtree(outdir)
