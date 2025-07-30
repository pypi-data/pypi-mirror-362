from contextlib import contextmanager
from typing import Callable

import pytest
from django.test import TestCase

from gdaps import hooks

hooks.define("test_hook_name", (), None)
hooks.define("test_hook_name_str", (str,), str)
hooks.define("test_hook_name_str_int", (str, int), str)
hooks.define("test_hook_name_bool", (bool,), int)
hooks.define("test_hook_name_ret_bool", (), bool)
hooks.define("test_hook_name_ret_none", ())
hooks.define("test_hook_name_ret_none2", (), None)


def empty_func():
    """Test hook. Does nothing."""


def empty_str_func(s: str) -> str:
    """Test hook. Does nothing."""
    return ""


@pytest.fixture
def register_test_hooks():
    hooks.register("test_hook_name", empty_func)
    hooks.register("test_hook_name_str", empty_str_func)
    yield
    hooks.unregister("test_hook_name", empty_func)
    hooks.unregister("test_hook_name_str", empty_str_func)


@contextmanager
def temp_register_hook(hook_name: str, fn: Callable, order: int = 0):
    """Registers a hook with the given name and order, and then yields it.

    You can use that for registering temporary hooks:
    ```python
    with temp_register_hook("test_hook_name", before_hook, order=-1):
        #...do something...
    ```
    The hook will be removed afterwords.

    """
    hooks.register(hook_name, fn, order)
    yield
    hooks.unregister(hook_name, fn)


def test_hook_order_before(register_test_hooks):
    def before_hook():
        pass

    with temp_register_hook("test_hook_name", before_hook, order=-1):
        hook_fns = hooks.get_hooks("test_hook_name")
        assert hook_fns, [before_hook, empty_func]


def test_hook_order_after(register_test_hooks):
    def after_hook():
        pass

    with temp_register_hook("test_hook_name", after_hook, order=-1):
        hook_fns = hooks.get_hooks("test_hook_name")
        assert hook_fns, [empty_func, after_hook]


def test_call_hooks_before_after(register_test_hooks):
    def before_hook():
        pass

    def after_hook():
        pass

    with temp_register_hook("test_hook_name", before_hook, order=-1):
        with temp_register_hook("test_hook_name", after_hook, order=1):
            hook_fns = hooks.get_hooks("test_hook_name")
            assert hook_fns, [before_hook, after_hook, empty_func]


def test_register_simple_hook(register_test_hooks):
    """Tests registering a simple hook."""

    # this may not throw an exception
    @hooks.register("test_hook_name")
    def my_implementation() -> None: ...


def test_register_hook_with_types(register_test_hooks):
    """Tests registering a normal hook with correct, explicit types."""

    @hooks.register("test_hook_name_str")
    def my_implementation(a: str) -> str: ...

    # we have to clean up manually, as the hook is not removed by pytest
    hooks.unregister("test_hook_name_str", my_implementation)


def test_register_wrong_types(register_test_hooks):
    with pytest.raises(TypeError):

        @hooks.register("test_hook_name_str")
        def my_implementation(a: int) -> str: ...

    with pytest.raises(TypeError):

        @hooks.register("test_hook_name_str")
        def my_implementation(a: bool) -> str: ...


def test_register_wrong_type_count(register_test_hooks):

    with pytest.raises(ValueError):

        @hooks.register("test_hook_name")  # expects 0 args
        def my_implementation(a: int) -> int: ...

    with pytest.raises(ValueError):

        @hooks.register("test_hook_name")  # expects 0 args
        def my_implementation(a: int, b: str, c: bool) -> int: ...

    with pytest.raises(ValueError):

        @hooks.register("test_hook_name_str")  # expects 1 arg
        def my_implementation() -> str: ...

    with pytest.raises(ValueError):

        @hooks.register("test_hook_name_str")  # expects 1 arg
        def my_implementation(a: int, b: str, c: bool) -> str: ...


def test_register_missing_type_annotation(register_test_hooks):

    with pytest.raises(TypeError):

        @hooks.register("test_hook_name_str")
        def my_implementation(a_str) -> str: ...


def test_register_missing_return_type(register_test_hooks):

    with pytest.raises(TypeError):

        @hooks.register("test_hook_name_str")
        def my_implementation(a: str): ...


def test_register_missing_none_return_type(register_test_hooks):
    # registration of missing return type means return type == None
    # and should be ok
    @hooks.register("test_hook_name")
    def my_implementation(): ...


# a test to call a hook


def test_call_hook(register_test_hooks):
    def hook():
        pass

    with temp_register_hook("test_hook_name", hook):
        for fn in hooks.get_hooks("test_hook_name"):
            fn()


def test_call_hook_with_args(register_test_hooks):
    def hook(a: str) -> str:
        pass

    with temp_register_hook("test_hook_name_str", hook):
        for fn in hooks.get_hooks("test_hook_name_str"):
            fn("foo")


def test_call_hook_with_return_value(register_test_hooks):
    def hook(a: str) -> str:
        return "foo"

    with temp_register_hook("test_hook_name_str", hook):
        for fn in hooks.get_hooks("test_hook_name_str"):
            assert isinstance(fn("foo"), str)


def test_hooks_with_2_params():
    def hook(a: str, b: int) -> str:
        return f"{a} {b}"

    with temp_register_hook("test_hook_name_str_int", hook):
        for fn in hooks.get_hooks("test_hook_name_str_int"):
            assert isinstance(fn("foo", 123), str)


def test_bool_param_hook():
    def hook(a: bool) -> int:
        return 1 if a else 0

    with temp_register_hook("test_hook_name_bool", hook):
        for fn in hooks.get_hooks("test_hook_name_bool"):
            assert isinstance(fn(True), int)
            assert fn(True) == 1
            assert isinstance(fn(False), int)
            assert fn(False) == 0


def test_hook_return_bool():
    def hook() -> bool:
        return True

    with temp_register_hook("test_hook_name_ret_bool", hook):
        for fn in hooks.get_hooks("test_hook_name_ret_bool"):
            assert isinstance(fn(), bool)
            assert fn() == True


def test_return_none_hook():
    """Tests if a hook impl that has None as return value matches a hook with
    implicit or explicit None return type."""

    def hook() -> None:
        return None

    with temp_register_hook("test_hook_name_ret_none", hook):
        for fn in hooks.get_hooks("test_hook_name_ret_none"):
            assert fn() is None
    with temp_register_hook("test_hook_name_ret_none2", hook):
        for fn in hooks.get_hooks("test_hook_name_ret_none2"):
            assert fn() is None


def test_return_implicit_none_hook():
    """Tests if a hook impl that has no return value matches a hook with implicit or
    explicit None return type."""

    def hook():
        return None

    with temp_register_hook("test_hook_name_ret_none", hook):
        for fn in hooks.get_hooks("test_hook_name_ret_none"):
            assert fn() is None
    with temp_register_hook("test_hook_name_ret_none2", hook):
        for fn in hooks.get_hooks("test_hook_name_ret_none2"):
            assert fn() is None
