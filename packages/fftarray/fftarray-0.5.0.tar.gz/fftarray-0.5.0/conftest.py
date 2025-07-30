# from https://docs.pytest.org/en/6.2.x/example/simple.html
import pytest


def pytest_addoption(parser):
    parser.addoption(
        "--include-slow", action="store_true", default=False, help="run slow tests"
    )


def pytest_configure(config):
    config.addinivalue_line("markers", "slow: mark test as slow to run")


def pytest_collection_modifyitems(config, items):
    if config.getoption("--include-slow"):
        # --include-slow given in cli: do not skip slow tests
        return
    skip_slow = pytest.mark.skip(reason="need --include-slow option to run")
    for item in items:
        if "slow" in item.keywords:
            item.add_marker(skip_slow)