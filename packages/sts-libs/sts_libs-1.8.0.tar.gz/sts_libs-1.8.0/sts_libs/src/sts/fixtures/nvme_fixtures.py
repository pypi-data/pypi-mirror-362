"""Fixtures for NVMe device testing.

This module provides fixtures for NVMe device detection and management.
"""
#  Copyright: Contributors to the sts project
#  GNU General Public License v3.0+ (see LICENSE or https://www.gnu.org/licenses/gpl-3.0.txt)

import pytest

from sts.nvme import NvmeDevice
from sts.utils.packages import ensure_installed


@pytest.fixture(scope='class')
def ensure_nvme_disks() -> None:
    """Ensure NVMe disks exist on the system.

    This fixture:
    - Ensures nvme-cli package is installed
    - Checks for NVMe device presence
    - Skips tests if requirements are not met
    """
    # Ensure nvme-cli package is installed
    if not ensure_installed('nvme-cli'):
        pytest.skip('Failed to install nvme-cli package')

    # Check if NVMe devices are available
    if not NvmeDevice.has_nvme():
        pytest.skip('No NVMe disks detected.')
