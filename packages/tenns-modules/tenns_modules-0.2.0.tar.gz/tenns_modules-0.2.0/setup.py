#!/usr/bin/env python
# ******************************************************************************
# Copyright 2025 Brainchip Holdings Ltd.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ******************************************************************************
from setuptools import setup
from setuptools_scm import get_version
from packaging.version import Version

VERSION = "0.2.0"


def get_custom_version():
    current_version = get_version(version_scheme="no-guess-dev", local_scheme="no-local-version")
    if ".dev" in current_version:
        # Extract number of commits as the number after '.dev'.
        dev_part = current_version.split(".dev")[-1].split("+")[0]
        # Format build version.
        # Note we remove rc0 (current commit has a tag).
        build_version = f"{VERSION}rc{dev_part}" if dev_part != '0' else VERSION
        # Format release version
        release_version = current_version.split(".post")[0]
        # Check build version.
        if Version(build_version) < Version(release_version):
            raise RuntimeError("Fix-versions (with `post` suffix) are not allowed: "
                               "increase VERSION to define a new release candidate. "
                               f"Fix version: {build_version}. "
                               f"Release candidate: {release_version}.")
        # Convert post version into rc{num_commits}
        return build_version
    else:
        return current_version


setup(version=get_custom_version())
