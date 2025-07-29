"""pytest setup and fixtures for wms integration tests"""

import subprocess as sp

import pytest


@pytest.fixture(scope="session")
def _dirac_proxy():
    sp.run(["dirac-proxy-init", "-g", "dpps_group"], check=True)


@pytest.fixture(scope="session")
def _init_dirac(_dirac_proxy):
    """Import and init DIRAC, needs to be run first for anything using DIRAC"""
    import DIRAC

    DIRAC.initialize()
