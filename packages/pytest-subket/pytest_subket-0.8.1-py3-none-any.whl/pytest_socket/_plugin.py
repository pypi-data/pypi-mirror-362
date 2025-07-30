import typing
from dataclasses import dataclass, field

import pytest

from ._core import (
    _remove_restrictions,
    disable_socket,
    enable_socket,
    socket_allow_hosts,
)


def pytest_addoption(parser):
    group = parser.getgroup("socket")
    group.addoption(
        "--disable-socket",
        action="store_true",
        dest="disable_socket",
        help="Disable socket.socket by default to block network calls.",
    )
    group.addoption(
        "--force-enable-socket",
        action="store_true",
        dest="force_enable_socket",
        help="Force enable socket.socket network calls (override --disable-socket).",
    )
    group.addoption(
        "--allow-hosts",
        dest="allow_hosts",
        metavar="ALLOWED_HOSTS_CSV",
        help="Only allow specified hosts through socket.socket.connect((host, port)).",
    )
    group.addoption(
        "--allow-unix-socket",
        action="store_true",
        dest="allow_unix_socket",
        help="Allow calls if they are to Unix domain sockets",
    )


@pytest.fixture
def socket_disabled(pytestconfig):
    """disable socket.socket for duration of this test function"""
    socket_config = pytestconfig.stash[_STASH_KEY]
    disable_socket(allow_unix_socket=socket_config.allow_unix_socket)
    yield


@pytest.fixture
def socket_enabled(pytestconfig):
    """enable socket.socket for duration of this test function"""
    enable_socket()
    yield


@dataclass
class _PytestSocketConfig:
    socket_disabled: bool
    socket_force_enabled: bool
    allow_unix_socket: bool
    allow_hosts: typing.Union[str, typing.List[str], None]
    resolution_cache: typing.Dict[str, typing.Set[str]] = field(default_factory=dict)


_STASH_KEY = pytest.StashKey[_PytestSocketConfig]()


def pytest_configure(config):
    config.addinivalue_line(
        "markers", "disable_socket(): Disable socket connections for a specific test"
    )
    config.addinivalue_line(
        "markers", "enable_socket(): Enable socket connections for a specific test"
    )
    config.addinivalue_line(
        "markers",
        "allow_hosts([hosts]): Restrict socket connection to defined list of hosts",
    )

    # Store the global configs in the `pytest.Config` object.
    config.stash[_STASH_KEY] = _PytestSocketConfig(
        socket_force_enabled=config.getoption("--force-enable-socket"),
        socket_disabled=config.getoption("--disable-socket"),
        allow_unix_socket=config.getoption("--allow-unix-socket"),
        allow_hosts=config.getoption("--allow-hosts"),
    )


def pytest_runtest_setup(item) -> None:
    """During each test item's setup phase,
    choose the behavior based on the configurations supplied.

    This is the bulk of the logic for the plugin.
    As the logic can be extensive, this method is allowed complexity.
    It may be refactored in the future to be more readable.

    If the given item is not a function test (i.e a DoctestItem)
    or otherwise has no support for fixtures, skip it.
    """
    if not hasattr(item, "fixturenames"):
        return

    socket_config = item.config.stash[_STASH_KEY]

    # If test has the `enable_socket` marker, fixture or
    # it's forced from the CLI, we accept this as most explicit.
    if (
        "socket_enabled" in item.fixturenames
        or item.get_closest_marker("enable_socket")
        or socket_config.socket_force_enabled
    ):
        enable_socket()
        return

    # If the test has the `disable_socket` marker, it's explicitly disabled.
    if "socket_disabled" in item.fixturenames or item.get_closest_marker(
        "disable_socket"
    ):
        disable_socket(socket_config.allow_unix_socket)
        return

    # Resolve `allow_hosts` behaviors.
    hosts = _resolve_allow_hosts(item)

    # Finally, check the global config and disable socket if needed.
    if socket_config.socket_disabled and not hosts:
        disable_socket(socket_config.allow_unix_socket)


def _resolve_allow_hosts(item):
    """Resolve `allow_hosts` behaviors."""
    socket_config = item.config.stash[_STASH_KEY]

    mark_restrictions = item.get_closest_marker("allow_hosts")
    cli_restrictions = socket_config.allow_hosts
    hosts = None
    if mark_restrictions:
        hosts = mark_restrictions.args[0]
    elif cli_restrictions:
        hosts = cli_restrictions

    socket_allow_hosts(
        hosts,
        allow_unix_socket=socket_config.allow_unix_socket,
        resolution_cache=socket_config.resolution_cache,
    )
    return hosts


def pytest_runtest_teardown():
    _remove_restrictions()
