# This file is part of craft-platforms.
#
# Copyright 2025 Canonical Ltd.
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
"""Unit tests for build functions."""

from unittest.mock import Mock, call

from craft_platforms import _build


def test_get_snapcraft_build_plan(monkeypatch):
    fake_build_plan = Mock()
    monkeypatch.setitem(_build._APP_SPECIFIC_PLANNERS, "snapcraft", fake_build_plan)

    project_data = {
        "base": "core22",
        "build-base": "core24",
        "platforms": {},
        "type": "base",
    }
    _build.get_build_plan("snapcraft", project_data=project_data)

    assert fake_build_plan.mock_calls == [
        call(base="core22", build_base="core24", platforms={}, snap_type="base")
    ]
