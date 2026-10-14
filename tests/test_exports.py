import importlib
import pkgutil

import pytest

import shekar

MODULES = ["shekar"] + [
    module.name
    for module in pkgutil.walk_packages(shekar.__path__, "shekar.")
    if module.ispkg
]


@pytest.mark.parametrize("name", MODULES)
def test_all_exports_exist(name):
    module = importlib.import_module(name)
    missing = [n for n in getattr(module, "__all__", []) if not hasattr(module, n)]
    assert missing == []
