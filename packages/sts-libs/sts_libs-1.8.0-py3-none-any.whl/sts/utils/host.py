"""Host management utilities.

This module provides functionality for managing the test host:
- Host initialization
- Package installation
- Command execution
"""
#  Copyright: Contributors to the sts project
#  GNU General Public License v3.0+ (see LICENSE or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import annotations

from testinfra.host import Host

from sts import get_sts_host


def host_init() -> Host:
    """Initialize testinfra host with local backend.

    Returns:
        Host instance configured for local backend

    Example:
        ```python
        host = host_init()
        host.exists('rpm')
        True
        ```
    """
    return Host.get_host('local://')


# Initialize global host instance
host: Host = get_sts_host()

# Ensure iproute is installed for network operations
if not host.exists('ip'):
    host.run('dnf install -y iproute')
