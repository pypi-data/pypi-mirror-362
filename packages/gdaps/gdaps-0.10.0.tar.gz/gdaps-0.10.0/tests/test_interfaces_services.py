import pytest

from gdaps.api import InterfaceMeta, Interface


class IInstantiate(Interface):
    __instantiate_plugins__ = True

    def foo(self):
        pass


class INonInstanciate(Interface):
    __instantiate_plugins__ = False

    def foo(self):
        pass


class INonService2(Interface):
    __instantiate_plugins__ = False


# Classes/Plugins


class Service(IInstantiate):
    pass


class ClassPlugin1(INonInstanciate):
    def foo(self):
        pass


class ClassPlugin2(INonInstanciate):
    def foo(self):
        pass


class NonServicePlugin1(INonService2):
    pass


# Tests


def test_nonservice_is_not_instantiated():
    for i in INonService2:
        assert i is NonServicePlugin1


def test_service_is_instantiated():
    assert len(IInstantiate) > 0
    for i in IInstantiate:
        assert isinstance(i, IInstantiate)


def test_service_has_attr_or_method():
    for i in IInstantiate:
        assert hasattr(i, "foo")


def test_service_method_callable():
    for i in IInstantiate:
        assert callable(i.foo)


def test_service_method_call():
    for i in IInstantiate:
        i.foo()


def test_nonservice_plugins():
    assert len(IInstantiate) > 0
    for i in INonInstanciate:
        # compare classes, not instances
        assert ClassPlugin1 in INonInstanciate
        assert ClassPlugin2 in INonInstanciate

        # make sure that there is no instance in the list of plugins, just classes
        for cls in INonInstanciate:
            assert type(cls) is InterfaceMeta
            assert not isinstance(cls, INonInstanciate)

        # methods cannot be called, as there is no instance yet
        with pytest.raises(TypeError):
            i.foo()

        i().foo()


def test_instantiate_plugins():
    assert len(IInstantiate) > 0

    # make sure that there is no instance in the list of plugins, just classes
    for plugin in IInstantiate:
        assert isinstance(plugin, IInstantiate)

        plugin.foo()
