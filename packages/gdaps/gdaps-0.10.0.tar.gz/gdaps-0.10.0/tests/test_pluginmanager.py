import pytest

from gdaps.exceptions import PluginError
from gdaps.pluginmanager import PluginManager


def test_pluginmanager_alter_installed_apps_with_wrong_entrypoint():
    # try to find plugins from a nonexisting entry point

    INSTALLED_APPS = ["blah_app", "foo_app"]
    PluginManager.alter_installed_apps(
        installed_apps=INSTALLED_APPS, group="gdapstest_foo321.plugins"
    )
    assert INSTALLED_APPS == ["blah_app", "foo_app"]


def test_instantiate_pluginmanager():
    with pytest.raises(PluginError):
        PluginManager()
