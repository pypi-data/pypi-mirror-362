from gdaps.api import Interface
import pytest


class IEnabledNonServiceInterface(Interface):
    """plugins are classes"""


class DynamicNonServiceEnabled(IEnabledNonServiceInterface):
    @classmethod
    def enabled(cls):
        return True


class DynamicNonServiceDisabled(IEnabledNonServiceInterface):
    @classmethod
    def enabled(cls):
        return False


def test_enabled_nonservice_interface_count():
    assert len(IEnabledNonServiceInterface) == 1


def test_enabled_nonservice_interface():
    # make sure all returned plugins are enabled
    for plugin in IEnabledNonServiceInterface:
        assert plugin.enabled()


class IEnabledServiceInterface(Interface):
    """plugins are instances"""

    __instantiate_plugins__ = True


class DynamicServiceEnabled(IEnabledServiceInterface):
    def enabled(self):
        return True


class DynamicServiceDisabled(IEnabledServiceInterface):
    def enabled(self):
        return False


def test_enabled_service_interface_count():
    assert len(IEnabledServiceInterface) == 1


def test_enabled_service_interface():
    # make sure all returned plugins classes are enabled
    for plugin in IEnabledServiceInterface:
        assert plugin.enabled()
