import logging
import os
import re
import subprocess as sp
from datetime import datetime
from pathlib import Path
from secrets import token_hex

import pytest
from rucio.client.scopeclient import ScopeClient


def pytest_configure():
    # gfal is overly verbose on info (global default), reduce a bit
    logging.getLogger("gfal2").setLevel(logging.WARNING)


@pytest.fixture(scope="session")
def test_user():
    return "root"


@pytest.fixture(scope="session")
def user_cert():
    return os.getenv("RUCIO_CFG_CLIENT_CERT", "/opt/rucio/etc/usercert.pem")


@pytest.fixture(scope="session")
def user_key():
    return os.getenv("RUCIO_CFG_CLIENT_KEY", "/opt/rucio/etc/userkey.pem")


@pytest.fixture(scope="session")
def auth_proxy(user_key, user_cert):
    """Auth proxy needed for accessing RSEs"""
    ret = sp.run(
        [
            "voms-proxy-init",
            "-valid",
            "9999:00",
            "-cert",
            user_cert,
            "-key",
            user_key,
        ],
        check=True,
        capture_output=True,
        encoding="utf-8",
    )
    m = re.match(r"Created proxy in (.*)\.", ret.stdout.strip())
    if m is None:
        raise ValueError(f"Failed to parse output of voms-proxy-init: {ret.stdout!r}")
    return Path(m.group(1))


@pytest.fixture(scope="session")
def test_scope(test_user):
    """To avoid name conflicts and old state, use a unique scope for the tests"""
    # length of scope is limited to 25 characters
    random_hash = token_hex(2)
    date_str = f"{datetime.now():%Y%m%d_%H%M%S}"
    scope = f"t_{date_str}_{random_hash}"

    sc = ScopeClient()
    sc.add_scope(test_user, scope)
    return scope


USER_CERT = os.getenv("RUCIO_CFG_CLIENT_CERT", "/tmp/usercert.pem")
USER_KEY = os.getenv("RUCIO_CFG_CLIENT_KEY", "/tmp/userkey.pem")


@pytest.fixture(scope="session")
def _dirac_proxy():
    sp.run(["dirac-proxy-init", "-g", "dpps_group"], check=True)


@pytest.fixture(scope="session")
def _init_dirac(_dirac_proxy):
    """Import and init DIRAC, needs to be run first for anything using DIRAC"""
    import DIRAC

    DIRAC.initialize()
