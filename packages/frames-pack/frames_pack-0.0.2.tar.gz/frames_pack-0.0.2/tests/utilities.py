from __future__ import annotations

import contextlib
import os
import sys
from pathlib import Path

import pytest

# https://loguru.readthedocs.io/en/stable/resources/migration.html#making-things-work-with-pytest-and-caplog
from _pytest.logging import LogCaptureFixture
from loguru import logger

__pwd = Path(__file__).parent.absolute()
__project_source_dir = __pwd.parent
sys.path.insert(0, str((__project_source_dir / "src").absolute()))


# https://loguru.readthedocs.io/en/stable/resources/migration.html?highlight=pytest#making-things-work-with-pytest-and-caplog
@pytest.fixture
def caplog(caplog: LogCaptureFixture):
    # https://loguru.readthedocs.io/en/stable/api/logger.html#loguru._logger.Logger.add
    """
    with dynamic logging level configuration
    """
    caplog.handler_id = None

    def update_loguru(
        format: str = "{message}",
        level: str = "DEBUG",
        **kwargs,
    ):
        logger.remove(caplog.handler_id)
        caplog.handler_id = logger.add(
            caplog.handler,
            format=format,
            level=level,
            **kwargs,
        )
        return caplog.handler_id

    caplog.update_loguru = update_loguru
    handler_id = caplog.update_loguru()
    yield caplog
    if caplog.handler_id == handler_id:
        with contextlib.suppress(ValueError):
            logger.remove(handler_id)


def setup_loguru_to_stdout(format: str = "{message}", level: str = "DEBUG"):
    logger.remove()
    logger.add(sys.stdout, format=format, level=level)
    # we need this:
    # capture: combine or line-order intersparse stdout and stderr #5449
    # https://github.com/pytest-dev/pytest/issues/5449


"""
Tips:

https://docs.pytest.org/en/latest/how-to/skipping.html#skipif
@pytest.mark.skip
"""


def pytest_main(dir: str, *, test_file: str | None = None):
    # pytest test_cli.py
    # pytest --capture=tee-sys test_cli.py
    os.chdir(dir)
    # https://docs.pytest.org/en/6.2.x/usage.html#calling-pytest-from-python-code
    sys.exit(
        pytest.main(
            [
                dir,
                *(["-k", test_file] if test_file else []),
                "--capture",
                "tee-sys",
                "-vv",
                "-x",
            ]
        )
    )
