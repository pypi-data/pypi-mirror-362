"""Target test fixtures.

This module provides fixtures for testing storage targets:
- Target creation and configuration
- Backstore management (block, fileio, ramdisk)
- ACL and authentication setup
- LUN management

Fixture Dependencies:
1. _target_test (base fixture)
   - Installs target utilities
   - Manages target cleanup
   - Logs system information

2. backstore_*_setup (depends on _target_test)
   - block: Creates block backstore with loop device
   - fileio: Creates fileio backstore
   - ramdisk: Creates ramdisk backstore

3. iscsi_target_setup (depends on _target_test)
   - Creates iSCSI target
   - Configures ACLs and LUNs
   - Manages cleanup

4. configure_auth (depends on _target_test)
   - Sets up CHAP authentication
   - Configures mutual CHAP
   - Manages credentials

Common Usage:
1. Basic target testing:
   @pytest.mark.usefixtures('_target_test')
   def test_target():
       # Create and test targets
       # Targets are cleaned up after test

2. Backstore testing:
   @pytest.mark.parametrize('backstore_block_setup',
                           [{'name': 'test', 'size': 1024*1024}],
                           indirect=True)
   def test_backstore(backstore_block_setup):
       # Test backstore operations

3. iSCSI target testing:
   @pytest.mark.parametrize('iscsi_target_setup',
                           [{'t_iqn': 'iqn.test', 'n_luns': 2}],
                           indirect=True)
   def test_iscsi(iscsi_target_setup):
       # Test iSCSI target operations

4. Authentication testing:
   @pytest.mark.parametrize('configure_auth',
                           [{'t_iqn': 'iqn.test',
                             'chap_username': 'user',
                             'chap_password': 'pass'}],
                           indirect=True)
   def test_auth(configure_auth):
       # Test authentication

Error Handling:
- Package installation failures fail test
- Target creation failures are handled
- Resource cleanup runs on failure
- Authentication errors are logged
"""
#  Copyright: Contributors to the sts project
#  GNU General Public License v3.0+ (see LICENSE or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import annotations

import logging
from contextlib import contextmanager
from pathlib import Path
from typing import TYPE_CHECKING

import pytest

from sts.loop import LoopDevice
from sts.target import (
    ACL,
    BackstoreBlock,
    BackstoreFileio,
    BackstoreRamdisk,
    Iscsi,
    IscsiLUN,
    Targetcli,
)
from sts.utils.packages import ensure_installed
from sts.utils.system import SystemManager

if TYPE_CHECKING:
    from collections.abc import Generator

# Constants
DEFAULT_TARGET_IQN = 'iqn.2003-01.com.redhat:targetauthtest'


@pytest.fixture(scope='class')
def _target_test() -> Generator[None, None, None]:
    """Install target utils and clean up before/after test.

    This fixture provides the foundation for target testing:
    - Installs targetcli package
    - Logs system information
    - Cleans up target configuration
    - Ensures consistent environment

    Package Installation:
    - targetcli: Target configuration tool
    - Required kernel modules
    - System dependencies

    Target Cleanup:
    1. Removes test target before test
    2. Removes test target after test
    3. Handles force cleanup if needed

    Example:
        ```python
        @pytest.mark.usefixtures('_target_test')
        def test_target():
            # Create and test targets
            # Configuration is cleaned up after test
        ```
    """
    system = SystemManager()
    assert ensure_installed('targetcli')
    logging.info(f'Kernel version: {system.info.kernel}')
    targetcli = Targetcli(path='/')
    # Clear target config before the test
    targetcli.clearconfig()

    yield

    # Clear target config after the test
    targetcli.clearconfig()


@pytest.fixture
def backstore_block_setup(_target_test: None, request: pytest.FixtureRequest) -> Generator[BackstoreBlock, None, None]:
    """Create block backstore with loop device.

    Creates block backstore using loop device:
    - Creates temporary loop device
    - Sets up block backstore
    - Manages cleanup
    - Supports custom size

    Args:
        request: Fixture request with parameters:
            - name: Backstore name
            - size: Loop device size in MB

    Example:
        ```python
        @pytest.mark.parametrize('backstore_block_setup', [{'name': 'test', 'size': 1024}], indirect=True)
        def test_backstore(backstore_block_setup):
            assert backstore_block_setup.exists
        ```
    """
    loop_dev = None
    backstore = None
    try:
        # Create loop device
        loop_dev = LoopDevice.create(
            name=request.param['name'],
            size_mb=request.param['size'] // (1024 * 1024),
        )
        if not loop_dev:
            pytest.skip('Failed to create loop device')

        # Create backstore
        backstore = BackstoreBlock(name=request.param['name'])
        backstore.create_backstore(dev=str(loop_dev.path))
        yield backstore

    except Exception:
        logging.exception('Failed to set up block backstore')
        raise

    finally:
        # Clean up
        if backstore:
            backstore.delete_backstore()
        if loop_dev:
            loop_dev.remove()


@pytest.fixture
def backstore_fileio_setup(
    _target_test: None, request: pytest.FixtureRequest
) -> Generator[BackstoreFileio, None, None]:
    """Create fileio backstore.

    Creates fileio backstore:
    - Creates backing file
    - Sets up fileio backstore
    - Manages cleanup
    - Supports custom size

    Args:
        request: Fixture request with parameters:
            - name: Backstore name
            - size: File size in bytes
            - file_or_dev: File path

    Example:
        ```python
        @pytest.mark.parametrize('backstore_fileio_setup', [{'name': 'test', 'size': 1024 * 1024}], indirect=True)
        def test_backstore(backstore_fileio_setup):
            assert backstore_fileio_setup.exists
        ```
    """
    backstore = None
    try:
        backstore = BackstoreFileio(name=request.param['name'])
        backstore.create_backstore(
            size=str(request.param['size']),
            file_or_dev=request.param.get('file_or_dev') or f'{request.param["name"]}_file',
        )
        yield backstore

    except Exception:
        logging.exception('Failed to set up fileio backstore')
        raise

    finally:
        if backstore:
            backstore.delete_backstore()


@pytest.fixture
def backstore_ramdisk_setup(
    _target_test: None, request: pytest.FixtureRequest
) -> Generator[BackstoreRamdisk, None, None]:
    """Create ramdisk backstore.

    Creates ramdisk backstore:
    - Allocates memory
    - Sets up ramdisk backstore
    - Manages cleanup
    - Supports custom size

    Args:
        request: Fixture request with parameters:
            - name: Backstore name
            - size: Size in bytes

    Example:
        ```python
        @pytest.mark.parametrize('backstore_ramdisk_setup', [{'name': 'test', 'size': 1024 * 1024}], indirect=True)
        def test_backstore(backstore_ramdisk_setup):
            assert backstore_ramdisk_setup.exists
        ```
    """
    backstore = None
    try:
        backstore = BackstoreRamdisk(name=request.param['name'])
        backstore.create_backstore(size=str(request.param['size']))
        yield backstore

    except Exception:
        logging.exception('Failed to set up ramdisk backstore')
        raise

    finally:
        if backstore:
            backstore.delete_backstore()


@contextmanager
def target_setup(
    *,
    t_iqn: str | None = None,
    i_iqn: str | None = None,
    n_luns: int = 0,
    back_size: int | None = None,
) -> Generator[Iscsi, None, None]:
    """Set up iSCSI target.

    Creates and manages iSCSI target:
    - Creates target with IQN
    - Sets up ACLs if needed
    - Creates LUNs if needed
    - Manages cleanup

    Args:
        t_iqn: Target IQN
        i_iqn: Initiator IQN
        n_luns: Number of LUNs
        back_size: Backstore size in bytes

    Yields:
        iSCSI target instance

    Example:
        ```python
        with target_setup(t_iqn='iqn.test', n_luns=2) as target:
            # Use target
            assert target.exists
        ```
    """
    target_wwn = t_iqn or DEFAULT_TARGET_IQN
    target = Iscsi(target_wwn=target_wwn)

    try:
        # Create target
        target.create_target()

        # Add ACL if needed
        if i_iqn:
            acl = ACL(target_wwn=target_wwn, initiator_wwn=i_iqn)
            acl.create_acl()

        # Add LUNs if needed
        if back_size and n_luns > 0:
            luns = IscsiLUN(target_wwn)
            for n in range(n_luns):
                name = f'backstore{n}'
                backstore = BackstoreFileio(name=name)
                backstore.create_backstore(size=str(back_size), file_or_dev=f'{name}_file')
                luns.create_lun(storage_object=backstore.path)

        yield target

    finally:
        target.delete_target()
        # Clean up backstore files
        for n in range(n_luns):
            Path(f'backstore{n}_file').unlink(missing_ok=True)


@pytest.fixture(scope='class')
def iscsi_target_setup(_target_test: None, request: pytest.FixtureRequest) -> Generator[Iscsi, None, None]:
    """Create iSCSI target with ACLs and LUNs.

    Creates complete iSCSI target:
    - Creates target with IQN
    - Sets up ACLs
    - Creates LUNs
    - Manages cleanup

    Args:
        request: Fixture request with parameters:
            - t_iqn: Target IQN (optional)
            - i_iqn: Initiator IQN (optional)
            - n_luns: Number of LUNs (optional)
            - back_size: Backstore size in bytes (optional)

    Example:
        ```python
        @pytest.mark.parametrize('iscsi_target_setup', [{'t_iqn': 'iqn.test', 'n_luns': 2}], indirect=True)
        def test_target(iscsi_target_setup):
            assert iscsi_target_setup.exists
        ```
    """
    params = request.param
    with target_setup(
        t_iqn=params.get('t_iqn'),
        i_iqn=params.get('i_iqn'),
        n_luns=params.get('n_luns', 0),
        back_size=params.get('back_size'),
    ) as target:
        yield target


@pytest.fixture
def configure_auth(request: pytest.FixtureRequest) -> Generator[Iscsi, None, None]:
    """Configure CHAP authentication.

    Sets up CHAP authentication:
    - Creates target with auth
    - Configures CHAP credentials
    - Supports mutual CHAP
    - Manages cleanup

    Args:
        request: Fixture request with parameters:
            - t_iqn: Target IQN
            - i_iqn: Initiator IQN
            - chap_username: CHAP username
            - chap_password: CHAP password
            - chap_target_username: Mutual CHAP username (optional)
            - chap_target_password: Mutual CHAP password (optional)
            - tpg_or_acl: Configure TPG or ACL auth

    Example:
        ```python
        @pytest.mark.parametrize(
            'configure_auth', [{'t_iqn': 'iqn.test', 'chap_username': 'user', 'chap_password': 'pass'}], indirect=True
        )
        def test_auth(configure_auth):
            assert configure_auth.exists
        ```
    """
    target_wwn = request.param['t_iqn']
    target = Iscsi(target_wwn=target_wwn)

    try:
        # Create target
        target.create_target()

        # Add backstore
        backstore = BackstoreFileio(name='auth_test')
        backstore.create_backstore(size='1M', file_or_dev='auth_test_file')
        luns = IscsiLUN(target_wwn=target_wwn)
        luns.create_lun(storage_object=backstore.path)

        # Configure auth
        if request.param['tpg_or_acl'] == 'acl':
            acl = ACL(target_wwn=target_wwn, initiator_wwn=request.param['i_iqn'])
            acl.create_acl()
            acl.set_auth(
                userid=request.param['chap_username'],
                password=request.param['chap_password'],
                mutual_userid=request.param.get('chap_target_username', ''),
                mutual_password=request.param.get('chap_target_password', ''),
            )

        yield target

    finally:
        target.delete_target()
