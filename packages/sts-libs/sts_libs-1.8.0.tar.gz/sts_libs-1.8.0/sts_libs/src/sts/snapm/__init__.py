"""Snapm - Linux snapshot manager.

This package provides functionality for managing snapm.
"""
#  Copyright: Contributors to the sts project
#  GNU General Public License v3.0+ (see LICENSE or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import annotations

from sts.snapm.base import SnapmBase
from sts.snapm.plugin import Plugin, PluginManager
from sts.snapm.snapset import Snapset, SnapsetInfo
from sts.snapm.snapshot import Snapshot, SnapshotInfo

__all__ = [
    'Plugin',
    'PluginManager',
    'SnapmBase',
    'Snapset',
    'SnapsetInfo',
    'Snapshot',
    'SnapshotInfo',
]
