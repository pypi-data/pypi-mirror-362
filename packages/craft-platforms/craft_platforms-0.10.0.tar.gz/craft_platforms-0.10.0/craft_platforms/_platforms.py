# This file is part of craft-platforms.
#
# Copyright 2024 Canonical Ltd.
#
# This program is free software: you can redistribute it and/or modify it
# under the terms of the GNU Lesser General Public License version 3, as
# published by the Free Software Foundation.
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranties of MERCHANTABILITY,
# SATISFACTORY QUALITY, or FITNESS FOR A PARTICULAR PURPOSE.
# See the GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License along
# with this program.  If not, see <http://www.gnu.org/licenses/>.
"""Platform related models."""

import itertools
import typing
from typing import Dict, List, Optional, Sequence, Tuple, Union

import annotated_types
from typing_extensions import Annotated

from craft_platforms import _architectures, _buildinfo, _distro, _errors, _utils

PlatformDict = typing.TypedDict(
    "PlatformDict",
    {
        "build-on": Union[Sequence[str], str],
        "build-for": Union[Annotated[Sequence[str], annotated_types.Len(1)], str],
    },
)
"""The platforms where an artifact is built and where the resulting artifact runs."""


Platforms = Dict[Union[_architectures.DebianArchitecture, str], Optional[PlatformDict]]
"""A mapping of platforms names to ``PlatformDicts``.

A ``PlatformDict`` is not required if the platform name is a supported Debian architecture.
"""


def get_platforms_build_plan(
    base: Union[str, _distro.DistroBase],
    platforms: Platforms,
    build_base: Optional[str] = None,
) -> Sequence[_buildinfo.BuildInfo]:
    """Generate the build plan for a platforms-based artefact."""
    if isinstance(base, _distro.DistroBase):
        distro_base = base
    else:
        distro_base = _distro.DistroBase.from_str(build_base or base)
    build_plan: List[_buildinfo.BuildInfo] = []

    for platform_name, platform in platforms.items():
        if platform is None:
            # This is a workaround for Python 3.10.
            # In python 3.12+ we can just check:
            # `if platform_name not in _architectures.DebianArchitecture`
            try:
                architecture = _architectures.DebianArchitecture(platform_name)
            except ValueError:
                raise _errors.InvalidPlatformNameError(
                    f"Platform name {platform_name!r} is not a valid Debian architecture. "
                    "Specify a build-on and build-for.",
                ) from None
            build_plan.append(
                _buildinfo.BuildInfo(
                    platform=platform_name,
                    build_on=architecture,
                    build_for=architecture,
                    build_base=distro_base,
                ),
            )
        else:
            for build_on, build_for in itertools.product(
                _utils.vectorize(platform["build-on"]),
                _utils.vectorize(platform.get("build-for", [platform_name])),
            ):
                build_plan.append(
                    _buildinfo.BuildInfo(
                        platform=platform_name,
                        build_on=_architectures.DebianArchitecture(build_on),
                        build_for=(
                            "all"
                            if build_for == "all"
                            else _architectures.DebianArchitecture(build_for)
                        ),
                        build_base=distro_base,
                    ),
                )

    build_for_archs = {info.build_for for info in build_plan}
    if "all" in build_for_archs:
        platforms_with_all = {
            info.platform for info in build_plan if info.build_for == "all"
        }
        if len(platforms_with_all) > 1:
            raise _errors.AllSinglePlatformError(platforms_with_all)
        if len(build_for_archs) > 1:
            raise _errors.AllOnlyBuildError(platforms_with_all)

    return build_plan


def parse_base_and_name(platform_name: str) -> Tuple[Optional[_distro.DistroBase], str]:
    """Get the platform name and optional base from a platform name.

    The platform name may have an optional base prefix as '[<base>:]<platform>'.

    :param platform_name: The name of the platform.

    :returns: A tuple of the DistroBase and the platform name.

    :raises ValueError: If the base is invalid.
    """
    if ":" in platform_name:
        base_str, _, name = platform_name.partition(":")
        base = _distro.DistroBase.from_str(base_str)
    else:
        base = None
        name = platform_name

    return base, name
