import pytest

from gdaps.api import Interface


class IEmptyInterface(Interface):
    pass


class IEmptyInterface2(Interface):
    pass


class ICount3Interface(Interface):
    pass


class CountImpl1(ICount3Interface):
    pass


class CountImpl2(ICount3Interface):
    pass


class CountImpl3(ICount3Interface):
    pass


class ITestInterfacwWith2Methods(Interface):
    def required_method(self):
        pass

    def get_item(self):
        pass


# Test classes for interfaces and their implementations
class ITestInterface3(Interface):
    pass


class ITestInterface4(Interface):
    pass


class ITestInterface5(Interface):
    pass


class IAttribute1Interface(Interface):
    """Implementations should contain a 'foo' attribute: list of str"""

    foo = []


class TestMixin:
    pass


class Foo(ITestInterface3):
    pass


class Bar(ITestInterface4):
    pass


class Baz(ITestInterface4):
    pass


class Attribute2Class(IAttribute1Interface):
    foo = ["first", "second"]


class ChildClassPlugin1(TestMixin, IEmptyInterface):
    pass


class ChildClassPlugin2(TestMixin, IEmptyInterface2):
    pass


# def test_missing_attribute():
#    with pytest.raises(PluginError):
#
#        class MissingAttr(IAttribute1):
#            pass

# def test_missing_method():
#     with pytest.raises(PluginError):
#
#         class TestPlugin2(TestPlugin, ITestInterface2):
#             # does not implement required_method()
#             # this must raise an error at declaration time!
#             def get_item(self):
#                 return "something"


def test_dont_use_interface_decorator():
    """Try to use "Interface" as decorator. Is forbidden since v.0.9"""
    with pytest.raises(TypeError):

        @Interface
        class Dummy:
            pass


def test_class_implementing_2_interfaces():
    """Try to implement more than one interfaces in one implementation"""

    class Dummy(IEmptyInterface, ITestInterfacwWith2Methods):
        def required_method(self):
            pass

        def get_item(self):
            pass

    assert Dummy in IEmptyInterface
    assert Dummy in ITestInterfacwWith2Methods


def test_class_implementing_3_interfaces():
    """Try to implement more than one interfaces in one implementation"""

    class Dummy(IEmptyInterface, IEmptyInterface2, ITestInterfacwWith2Methods):
        def required_method(self):
            pass

        def get_item(self):
            pass

    assert Dummy in IEmptyInterface
    assert Dummy in IEmptyInterface2
    assert Dummy in ITestInterfacwWith2Methods


def test_class_inheriting_class_and_implementing_interface():
    """Try to implement more than one interfaces in one implementation"""

    class Dummy(ChildClassPlugin1, IEmptyInterface2):
        pass

    assert Dummy in IEmptyInterface
    assert Dummy in IEmptyInterface2


def test_interface_implementations_attr():
    """tests if _implementations attribute is existing and accessible"""
    # FIXME: protected members should not be accessed...
    assert hasattr(IEmptyInterface, "_implementations")
    assert hasattr(ITestInterfacwWith2Methods, "_implementations")


def test_iterable_interface():
    """Raises an Error if an extension point is not iterable"""
    iter(IEmptyInterface)


def test_iter_over_interface_directly():
    """Direct iteration over `Interface` must fail"""
    with pytest.raises(TypeError):
        for _plugin in Interface:
            pass


def test_call_method():
    """Raises an error if an implemented method is not callable"""

    for i in ITestInterfacwWith2Methods:
        _dummy = i.get_item()


def test_direct_interface_iter():
    """Tests if direct implementation of "Interface" fails"""

    with pytest.raises(TypeError):
        for _plugin in Interface:
            pass

    # This should pass
    for _plugin in ITestInterfacwWith2Methods:
        pass


def test_count_implementations():
    assert len(ICount3Interface) == 3


def test_ep_len():
    """tests countability of plugins via interface"""
    assert len(ITestInterface5) == 0

    assert len(ITestInterface3) == 1

    assert len(ITestInterface4) == 2


def test_attribute():
    # directly instantiate a class, which should contain an attribute.
    a = Attribute2Class()
    assert a.foo == ["first", "second"]


def test_interface_called():
    with pytest.raises(TypeError):

        # Interface must not be "called"
        class Foo(Interface()):
            pass


def test_interface_with_str_argument():
    with pytest.raises(TypeError):

        # Interface must not have an argument
        class Foo(Interface("baz")):
            pass


def test_interface_with_class_as_argument():
    with pytest.raises(TypeError):

        class IBaz:
            pass

        # Interface must not have an argument
        class Foo(Interface(IBaz)):
            pass


def test_No_I_Interface():
    with pytest.warns(UserWarning, match="Interface names should start with a capital"):

        class MyInterfaceStartingWithoutI(Interface):
            pass


def test_Interface_repr():
    assert str(ICount3Interface) == "<Interface 'ICount3Interface'>"


def test_Implementation_repr():
    assert (
        str(CountImpl1)
        == "<Implementation 'CountImpl1' of Interface 'ICount3Interface'>"
    )


def test_interface_repr():
    assert repr(ICount3Interface) == "<Interface 'ICount3Interface'>"


def test_implementation_repr():
    assert repr(Foo) == "<Implementation 'Foo' of Interface 'ITestInterface3'>"


def test_impl_interface_and_mixin_repr():
    assert (
        repr(ChildClassPlugin1)
        == "<Implementation 'ChildClassPlugin1' of Interface 'IEmptyInterface'>"
    )


def test_2_interfaces_repr():
    class Dummy(ITestInterface3, ITestInterface4):
        pass

    assert (
        repr(Dummy)
        == "<Implementation 'Dummy' of Interfaces 'ITestInterface3', 'ITestInterface4'>"
    )


def test_get_unknown_interface():
    with pytest.raises(KeyError):
        _interface = Interface["not_registered_interface_name"]
