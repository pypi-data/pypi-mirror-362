#  Copyright: Contributors to the sts project
#  GNU General Public License v3.0+ (see LICENSE or https://www.gnu.org/licenses/gpl-3.0.txt)

import logging
from time import sleep

import pytest

from sts.iscsi.iscsiadm import IscsiAdm


@pytest.mark.usefixtures('_iscsi_offload_setup')
def test_login_logout() -> None:
    iscsiadm = IscsiAdm()
    for i in range(1, 300):
        logging.info(f'Iteration {i}')
        assert iscsiadm.node_login().rc == 0
        sleep(0.1)
        assert iscsiadm.node_logoutall().rc == 0
