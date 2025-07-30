# pytest-socket

[![PyPI current version](https://img.shields.io/pypi/v/pytest-subket.svg)](https://pypi.python.org/pypi/pytest-subket)
[![Python Support](https://img.shields.io/pypi/pyversions/pytest-subket.svg)](https://pypi.python.org/pypi/pytest-subket)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

A plugin to use with Pytest to disable or restrict `socket` calls during
tests to ensure network calls are prevented.

> [!important]
> This is a fork of [pytest-socket] by [@miketheman]. Unless you are the pip
> project, you probably shouldn't use this. This fork was created to include
> subprocess support (that can even be injected into nested environments).

---

## Features

- Disables all network calls flowing through Python\'s `socket` interface.
- Python subprocesses are supported

## Requirements

- [Pytest](https://github.com/pytest-dev/pytest) 7.0 or greater

## Installation

You can install `pytest-subket` via [pip](https://pypi.python.org/pypi/pip/)
from [PyPI](https://pypi.python.org/pypi):

```console
pip install pytest-subket
```

or add to your `pyproject.toml` for [uv](https://docs.astral.sh/uv/):

```toml
[project.optional-dependencies]
dev = [
    "pytest-subket",
]
```

## Usage

Run `pytest --disable-socket`, tests should fail on any access to `socket` or
libraries using socket with a `SocketBlockedError`.

To add this flag as the default behavior, add this section to your
[`pytest.ini`](https://docs.pytest.org/en/stable/reference/customize.html#pytest-ini):

```ini
[pytest]
addopts = --disable-socket
```

or add this to your [`setup.cfg`](https://docs.pytest.org/en/stable/reference/customize.html#setup-cfg):

```ini
[tool:pytest]
addopts = --disable-socket
```

or update your [`conftest.py`](https://docs.pytest.org/en/stable/how-to/writing_plugins.html#conftest-py-local-per-directory-plugins) to include:

```python
from pytest_socket import disable_socket

def pytest_runtest_setup():
    disable_socket()
```

If you exceptionally want to enable socket for one particular execution
pass `--force-enable-socket`. It takes precedence over `--disable-socket`.

To enable Unix sockets during the test run (e.g. for async), add this option:

```ini
[pytest]
addopts = --disable-socket --allow-unix-socket
```

To enable specific tests use of `socket`, pass in the fixture to the test or
use a marker:

```python
def test_explicitly_enable_socket(socket_enabled):
    assert socket.socket(socket.AF_INET, socket.SOCK_STREAM)


@pytest.mark.enable_socket
def test_explicitly_enable_socket_with_mark():
    assert socket.socket(socket.AF_INET, socket.SOCK_STREAM)
```

To allow only specific hosts per-test:

```python
@pytest.mark.allow_hosts(['127.0.0.1'])
def test_explicitly_enable_socket_with_mark():
    assert socket.socket.connect(('127.0.0.1', 80))
```

or for whole test run

```ini
[pytest]
addopts = --allow-hosts=127.0.0.1,127.0.1.1
```

### Frequently Asked Questions

Q: Why is network access disabled in some of my tests but not others?

A: pytest's default fixture scope is "function", which `socket_enabled` uses.
If you create another fixture that creates a socket usage that has a "higher"
instantiation order, such as at the module/class/session, then the higher order
fixture will be resolved first, and won't be disabled during the tests.
Read more in [this excellent example](https://github.com/miketheman/pytest-socket/issues/45#issue-679835420)
and more about [pytest fixture order here](https://docs.pytest.org/en/stable/fixture.html#fixture-instantiation-order).

This behavior may change in the future, as we learn more about pytest
fixture order, and what users expect to happen.

## Contributing

Contributions are very welcome. Tests can be run with
[pytest](https://github.com/pytest-dev/pytest), please ensure the
coverage at least stays the same before you submit a pull request.

## License

Distributed under the terms of the
[MIT](http://opensource.org/licenses/MIT) license, "pytest-subket" is
free and open source software

## Issues

If you encounter any problems, please [file an issue](https://github.com/miketheman/pytest-socket/issues)
along with a detailed description.

## Acknowledgements

This is a fork of [@miketheman]'s [pytest-socket] project. A fork was created to
support the unique requirements of the pip project.

This plugin came about due to the efforts by
[\@hangtwenty](https://github.com/hangtwenty) solving a [StackOverflow
question](https://stackoverflow.com/a/30064664), then converted into a
pytest plugin by [\@miketheman](https://github.com/miketheman).

[@miketheman]: https://github.com/miketheman
[pytest-socket]: https://github.com/miketheman/pytest-socket
