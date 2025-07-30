import inspect
import logging
from contextlib import ContextDecorator
from operator import itemgetter
from typing import Callable, TypeVar
from gdaps.pluginmanager import PluginManager

# Credits: this is basically copied and modified from wagtail.hooks

logger = logging.getLogger(__name__)

# The function and it's weight:
HookImplementation: type = tuple[Callable, int]

_hooks: dict[str, list[HookImplementation]] = {}
_hook_signature: dict[str, tuple[type, ...]] = {}
_hook_return_types: dict[str, type] = {}


def define(
    name: str, signature: tuple[type, ...] | None, return_type: type | None = None
):
    """Defines a new hook.

    ```python
    hooks.define("my_app.hook_name", (int, str), bool)
    ```
    Parameters:
        name (str): Name of the hook.
        signature (tuple[type]): Types for the hook call parameters signature,
        e.g.: (int, str)
        return_type (type | None): Type of the hook's return value, or None if it doesn't return anything.

    """
    if signature is None:
        signature = ()
    if name in _hooks:
        logger.warning(f"Hook '{name}' is already defined.")
    if not isinstance(signature, tuple) and signature is not None:
        raise TypeError(
            f"hooks.define() args must be a tuple, not <{signature.__class__.__name__}>."
        )
    if signature:
        for i, arg in enumerate(signature):
            if not isinstance(arg, type):
                raise TypeError(
                    f"Hook arg[{i}] ({arg}) must be a type, not {i.__name__}"
                )
        _hook_signature[name] = signature
    else:
        _hook_signature[name] = tuple()
    _hook_return_types[name] = return_type
    _hooks[name] = []


def check_signature(fn: Callable, hook_name: str) -> None:
    """Checks a callable's signature against the expected signature of a hook name.'"""
    expected_signature = _hook_signature[hook_name]
    expected_return_type = _hook_return_types[hook_name]

    # Get the signature of the function
    func_signature = inspect.signature(fn)
    func_params = func_signature.parameters.values()

    # Check if the number of parameters matches
    if len(func_params) != len(expected_signature):
        raise ValueError(
            f"Function '{fn.__name__}' has {len(func_params)} parameters, but expected {len(expected_signature)}."
        )

    # Check each parameter's type annotation
    for param, expected_type in zip(func_params, expected_signature):
        if param.annotation == inspect._empty:
            raise TypeError(
                f"Parameter '{param.name}' of function '{fn.__name__}' has no type annotation."
            )
        if param.annotation != expected_type:
            raise TypeError(
                f"Parameter '{param.name}' of function '{fn.__name__}' is expected to be of type '{expected_type}', but got '{param.annotation}'."
            )

    # Check the return type annotation
    if expected_return_type is not None:
        return_annotation = func_signature.return_annotation
        if return_annotation != expected_return_type:
            raise TypeError(
                f"Return type of function '{fn.__name__}' is expected to be "
                f"'{expected_return_type.__name__}', but got '{return_annotation.__name__}'."
            )


def register(hook_name: str, fn: Callable = None, weight: int = 0) -> Callable | None:
    """
    Register hook for `hook_name`. Can be used as a decorator:
    ```python
    @hooks.register('app.hook_name')
    def my_hook(...):
        pass
    ```
    or as a function call:
    ```python
    def my_hook(...):
        pass
    hooks.register('app.hook_name', my_hook)
    ```
    """
    if hook_name not in _hooks:
        raise ValueError(f"Hook '{hook_name}' is not defined.")
    if fn in [f for f, _ in _hooks[hook_name]]:
        logger.warning(f"Function {fn} is already registered with kook '{hook_name}'.")

    # Pretend to be a decorator if fn is not supplied
    if fn is None:

        def decorator(fn):
            check_signature(fn, hook_name)

            logger.debug(
                f"Function '{fn.__name__}' successfully registered for hook '{hook_name}'."
            )
            register(hook_name, fn, weight=weight)
            return fn

        return decorator

    check_signature(fn, hook_name)
    _hooks[hook_name].append((fn, weight))
    return None


def unregister(hook_name, fn) -> None:
    if hook_name not in _hooks:
        raise ValueError(f"Hook '{hook_name}' is not defined.")

    for func, _order in _hooks[hook_name]:
        if fn == func:
            _hooks[hook_name].remove((fn, _order))
            return
    else:
        raise ValueError(
            f"Function '{hook_name}' is not registered at hook [{hook_name}]."
        )


def unregister_all(hook_name) -> None:
    """
    Unregister all functions from a defined hook.
    """
    if hook_name not in _hooks:
        raise ValueError(f"Hook '{hook_name}' is not defined.")
    del _hooks[hook_name]
    del _hook_signature[hook_name]
    del _hook_return_types[hook_name]


# def register(hook: str, fn=None, weight=0) -> Callable | bool:
#     """
#     Register hook for a defined HookInterface. Can be used as a decorator:
#
#     ```python
#     class MyInterface(HookInterface):
#         def __call__(a:int, b:str) -> bool: ...
#
#     @hooks.implement(MyInterface)
#     def my_hook(a:int, b:str):
#         ...
#     ```
#
#     or as a function call:
#
#     ```python
#     def my_hook(a:int, b:str, c:Callable):
#         pass
#     hooks.implement(MyInterface, my_hook)
#     ```
#     """
#     if not isinstance(hook, str):
#         raise TypeError(f"Expected <str>, got <{type(hook).__name__}>")
#
#     if fn is None:
#
#         def decorator(f: FunctionType):
#             iface_sig = inspect.signature(hook.__call__)
#             func_sig = inspect.signature(f)
#
#             # Check: Parameter count
#             if len(func_sig.parameters) != len(iface_sig.parameters) - 1:
#                 # -1 wegen self bei Protocol-Methoden
#                 raise TypeError(
#                     f"<{f.__name__}> has wrong parameter count for hook <"
#                     f"{hook.__name__}>."
#                 )
#
#             # Check: Parameter-Types
#             for (name_f, param_f), (name_i, param_i) in zip(
#                 func_sig.parameters.items(), list(iface_sig.parameters.items())[1:]
#             ):
#                 anno_f = param_f.annotation
#                 anno_i = param_i.annotation
#                 if anno_i is inspect._empty:
#                     continue
#                 if anno_f is inspect._empty:
#                     raise TypeError(
#                         f"Parameter {name_f} in <{f.__name__}> has missing type annotation."
#                     )
#                 if anno_f != anno_i:
#                     raise TypeError(
#                         f"Hook <{hook.__name__}>: implementation "
#                         f"<{f.__module__}.{f.__name__}>: "
#                         f"param  '{name_f}:{anno_f.__name__}' "
#                         f"does not match expected interface type '{anno_i.__name__}'"
#                     )
#
#             # Check Rückgabetyp
#             ret_f = func_sig.return_annotation
#             ret_i = iface_sig.return_annotation
#             if ret_i is not inspect._empty and ret_f != ret_i:
#                 raise TypeError(
#                     f"Hook <{hook.__name__}>: implementation "
#                     f"<{f.__module__}.{f.__name__}> "
#                     f"return type '{ret_f.__name__}' does not match interface return type "
#                     f"'{ret_i.__name__}'"
#                 )
#
#             register(hook, f, weight=weight)
#
#             return f
#
#         return decorator
#
#     # check if fn not already exists, no matter which weight
#     if not hook in _hooks:
#         _hooks[hook] = []
#     if fn not in [f for f, _ in _hooks[hook]]:
#         _hooks.setdefault(hook, []).append((fn, weight))
#         return True
#
#     return False


class TemporaryHook(ContextDecorator):
    def __init__(self, hooks: list[str], order):
        self.hooks = hooks
        self.order = order

    def __enter__(self):
        for hook_name, fn in self.hooks:
            if hook_name not in _hooks:
                _hooks[hook_name] = []
            _hooks[hook_name].append((fn, self.order))

    def __exit__(self, exc_type, exc_value, traceback):
        for hook_name, fn in self.hooks:
            _hooks[hook_name].remove((fn, self.order))


def register_temporarily(
    hook_name_or_hooks: str | list[str],
    fn: Callable = None,
    *,
    order: int = 0,
):
    """
    Implementation hook for `hook_name` temporarily. This is useful for testing hooks.

    Can be used as a decorator::

        def my_hook(...):
            pass

        def test_my_hook():
            @hooks.implement_temporarily("app.hook_name", my_hook)
            def test_my_hook(self):
                pass

    or as a context manager::

        def my_hook(...):
            pass

        with hooks.implement_temporarily("app.hook_name", my_hook):
            # Hook is registered here

        # Hook is unregistered here

    To register multiple hooks at the same time, pass in a list of 2-tuples:

        def my_hook(...):
            pass

        def my_other_hook(...):
            pass

        with hooks.register_temporarily([
                ("app.hook_name", my_hook),
                ("app.hook_name", my_other_hook),
            ]):
            # Hooks are registered here
    """
    if not isinstance(hook_name_or_hooks, list) and fn is not None:
        hooks = [(hook_name_or_hooks, fn)]
    else:
        hooks = hook_name_or_hooks

    return TemporaryHook(hooks, order)


def get_hooks(hook_name: str):
    """Return the hooks function sorted by their order."""
    if not hook_name:
        return []
    PluginManager.find_hooks()
    hooks = _hooks.get(hook_name, [])
    hooks = sorted(hooks, key=itemgetter(1))
    return [hook[0] for hook in hooks]
