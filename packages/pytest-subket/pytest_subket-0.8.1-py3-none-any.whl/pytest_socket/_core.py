import ipaddress
import itertools
import json
import os
import socket
import typing
from collections import defaultdict

_SUBPROCESS_ENVVAR = "_PYTEST_SOCKET_SUBPROCESS"
_true_socket = socket.socket
_true_connect = socket.socket.connect


def update_subprocess_config(config: typing.Dict[str, object]) -> None:
    """Enable pytest-socket in Python subprocesses.

    The configuration will be read by the .pth file to mirror the
    restrictions in the main process.
    """
    os.environ[_SUBPROCESS_ENVVAR] = json.dumps(config)


def delete_subprocess_config() -> None:
    """Disable pytest-socket in Python subprocesses."""
    if _SUBPROCESS_ENVVAR in os.environ:
        del os.environ[_SUBPROCESS_ENVVAR]


class SocketBlockedError(RuntimeError):
    def __init__(self, *_args, **_kwargs):
        super().__init__("A test tried to use socket.socket.")


class SocketConnectBlockedError(RuntimeError):
    def __init__(self, allowed, host, *_args, **_kwargs):
        if allowed:
            allowed = ",".join(allowed)
        super().__init__(
            "A test tried to use socket.socket.connect() "
            f'with host "{host}" (allowed: "{allowed}").'
        )


def _is_unix_socket(family) -> bool:
    try:
        is_unix_socket = family == socket.AF_UNIX
    except AttributeError:
        # AF_UNIX not supported on Windows https://bugs.python.org/issue33408
        is_unix_socket = False
    return is_unix_socket


def disable_socket(allow_unix_socket=False):
    """disable socket.socket to disable the Internet. useful in testing."""

    class GuardedSocket(socket.socket):
        """socket guard to disable socket creation (from pytest-socket)"""

        def __new__(cls, family=-1, type=-1, proto=-1, fileno=None):
            if _is_unix_socket(family) and allow_unix_socket:
                return super().__new__(cls, family, type, proto, fileno)

            raise SocketBlockedError()

    socket.socket = GuardedSocket
    update_subprocess_config(
        {"mode": "disable", "allow_unix_socket": allow_unix_socket}
    )


def enable_socket():
    """re-enable socket.socket to enable the Internet. useful in testing."""
    socket.socket = _true_socket
    delete_subprocess_config()


def host_from_address(address):
    host = address[0]
    if isinstance(host, str):
        return host


def host_from_connect_args(args):
    address = args[0]

    if isinstance(address, tuple):
        return host_from_address(address)


def is_ipaddress(address: str) -> bool:
    """
    Determine if the address is a valid IPv4 or IPv6 address.
    """
    try:
        ipaddress.ip_address(address)
        return True
    except ValueError:
        return False


def resolve_hostnames(hostname: str) -> typing.Set[str]:
    try:
        return {
            addr_struct[0] for *_, addr_struct in socket.getaddrinfo(hostname, None)
        }
    except socket.gaierror:
        return set()


def normalize_allowed_hosts(
    allowed_hosts: typing.List[str],
    resolution_cache: typing.Optional[typing.Dict[str, typing.List[str]]] = None,
) -> typing.Dict[str, typing.Set[str]]:
    """Map all items in `allowed_hosts` to IP addresses."""
    if resolution_cache is None:
        resolution_cache = {}
    ip_hosts = defaultdict(set)
    for host in allowed_hosts:
        host = host.strip()
        if is_ipaddress(host):
            ip_hosts[host].add(host)
            continue
        if host not in resolution_cache:
            resolution_cache[host] = resolve_hostnames(host)
        ip_hosts[host].update(resolution_cache[host])

    return ip_hosts


def _create_guarded_connect(
    allowed_hosts: typing.Sequence[str],
    allow_unix_socket: bool,
    _pretty_allowed_list: typing.Sequence[str],
) -> typing.Callable:
    """Create a function to replace socket.connect."""

    def guarded_connect(inst, *args):
        host = host_from_connect_args(args)
        if host in allowed_hosts or (
            _is_unix_socket(inst.family) and allow_unix_socket
        ):
            return _true_connect(inst, *args)

        raise SocketConnectBlockedError(_pretty_allowed_list, host)

    return guarded_connect


def socket_allow_hosts(
    allowed: typing.Union[str, typing.List[str], None] = None,
    allow_unix_socket: bool = False,
    resolution_cache: typing.Optional[typing.Dict[str, typing.List[str]]] = None,
) -> None:
    """disable socket.socket.connect() to disable the Internet. useful in testing."""
    if isinstance(allowed, str):
        allowed = allowed.split(",")

    if not isinstance(allowed, list):
        return

    allowed_ip_hosts_by_host = normalize_allowed_hosts(allowed, resolution_cache)
    allowed_ip_hosts_and_hostnames = set(
        itertools.chain(*allowed_ip_hosts_by_host.values())
    ) | set(allowed_ip_hosts_by_host.keys())
    allowed_list = sorted(
        [
            (
                host
                if len(normalized) == 1 and next(iter(normalized)) == host
                else f"{host} ({','.join(sorted(normalized))})"
            )
            for host, normalized in allowed_ip_hosts_by_host.items()
        ]
    )

    socket.socket.connect = _create_guarded_connect(
        allowed_ip_hosts_and_hostnames, allow_unix_socket, allowed_list
    )
    update_subprocess_config(
        {
            "mode": "allow-hosts",
            "allowed_hosts": list(allowed_ip_hosts_and_hostnames),
            "allow_unix_socket": allow_unix_socket,
            "_pretty_allowed_list": allowed_list,
        }
    )


def _remove_restrictions():
    """restore socket.socket.* to allow access to the Internet. useful in testing."""
    socket.socket = _true_socket
    socket.socket.connect = _true_connect
    delete_subprocess_config()
