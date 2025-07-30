from gdaps.exceptions import PluginError
from gdaps.api import Interface


class ITestInterface(Interface):
    pass


class EnabledPlugin(ITestInterface):
    def enabled(self):
        return True


class AutoEnabledPlugin(ITestInterface):
    pass


class DisabledPlugin(ITestInterface):
    def enabled(self):
        return False


def test_enabled_implementations():

    assert len(ITestInterface) == 2
    for i in ITestInterface:
        # either plugins have a .enabled() method which returns True, or (per default) are enabled by
        # not having this method.
        # There may not be any disabled plugin in the list!
        assert i.enabled()


def test_all_implementations():

    assert len(ITestInterface.all_plugins()) == 3
    for i in ITestInterface.all_plugins():
        # There may not be any disabled plugin in the list!
        assert i.__class__ in [EnabledPlugin, DisabledPlugin, AutoEnabledPlugin]


def test_disabled_implementations():

    # assert len(ITestInterface.disabled()) == 1
    for i in ITestInterface.disabled_plugins():
        # There may not be any enabled plugin in the list!
        assert i.enabled is False


# ------------------------------------------------------------


class INoop2(Interface):
    pass


class Baz2(INoop2):
    def enabled(self):
        return False


def test_disabled_implementations2():

    for i in INoop2:
        raise PluginError("Disabled extension was returned in Interface!")
