import pytest

from gdaps.api import Interface


def test_service_attr_deprecated():
    """Declaring an interface with "__service__" attribute is deprecated."""
    with pytest.deprecated_call():

        class IFoo(Interface):  # noqa
            __service__ = False


@pytest.mark.filterwarnings("ignore::DeprecationWarning")
def test_service_AND_instanciate_plugins_attr():
    """Declaring an interface with "__service__" attribute is deprecated."""
    with pytest.raises(AttributeError):

        class IFoo2(Interface):  # noqa
            __service__ = False
            __instantiate_plugins__ = False
