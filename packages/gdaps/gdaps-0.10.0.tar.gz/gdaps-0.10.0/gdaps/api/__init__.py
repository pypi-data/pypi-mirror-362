# this is the API of GDAPS itself.
import typing
import warnings
from typing import Sized

from django.apps import AppConfig

from gdaps.api.interfaces import InterfaceNotFound


class PluginMeta:
    """Inner class of GDAPS plugins.

    All GDAPS plugin AppConfig classes need to have an inner class named ``PluginMeta``. This
    PluginMeta provides some basic attributes and  methods that are needed when interacting with a
    plugin during its life cycle.

    .. code-block:: python

        from django.utils.translation import gettext_lazy as _
        from gdaps import api

        class FooPluginConfig(api.PluginConfig):

            class PluginMeta:
                # the plugin machine "name" is taken from the Appconfig, so no name here
                verbose_name = _('Foo Plugin')
                author = 'Me Personally'
                description = _('A foo plugin')
                hidden = False
                version = '1.0.0'
                compatibility = "myproject.core>=2.3.0"

    .. note::
        If ``PluginMeta`` is missing, the plugin is not recognized by GDAPS.
    """

    #: The version of the plugin, following `Semantic Versioning <https://semver.org/>`_. This is
    #: used for dependency checking as well, see ``compatibility``.
    version = "1.0.0"

    #: The verbose name, as shown to the user
    verbose_name = "My special plugin"

    #: The author of the plugin. Not translatable.
    author = "Me, myself and Irene"

    #: The email address of the author
    author_email = "me@example.com"

    #: A longer text to describe the plugin.
    description = ""

    #: A free-text category where your plugin belongs to.
    #: This can be used in your application to group plugins.
    category = "GDAPS"

    #:A boolean value whether the plugin should be hidden. False by default.
    hidden = False

    #: A string containing one or more other plugins that this plugin is known being compatible with, e.g.
    #: "myproject.core>=1.0.0<2.0.0" - meaning: This plugin is compatible with ``myplugin.core`` from version
    #: 1.0.0 to 1.x - v2.0 and above is incompatible.
    #:
    #:         .. note:: Work In Progress.
    compatibility = "gdaps>=1.0.0"

    def install(self):
        """
        Callback to setup the plugin for the first time.

        This method is optional. If your plugin needs to install some data into the database at the first run,
        you can provide this method to ``PluginMeta``. It will be called when ``manage.py syncplugins`` is called and
        the plugin is run, but only for the first time.

        An example would be installing some fixtures, or providing a message to the user.
        """

    def initialize(self):
        """
        Callback to initialize the plugin.

        This method is optional. It is called and run at Django start once.
        If your plugin needs to make some initial checks, do them here, but make them quick, as they slow down
        Django's start.
        """


class PluginConfig(AppConfig):
    """Convenience class for GDAPS plugins to inherit from.

    While it is not strictly necessary to inherit from this class - duck typing is ok -
    it simplifies the type suggestions and autocompletion of IDEs like PyCharm, as PluginMeta is already declared here.
    """

    PluginMeta: PluginMeta = None


def _get_sort_attr(mcs):
    return getattr(mcs, "__sort_attribute__", "weight")


def is_enabled(plugin_cls_or_instance):
    """Helper class to determine if a plugin is enabled or not.

    Returns True if plugin is enabled, False otherwise.
    It tries to get the `enabled` attribute, which must be a callable, but it can be
    defined in the implementation as instance method or in the interface as class
    method.
    """
    if not hasattr(plugin_cls_or_instance, "enabled"):
        return True
    enabled_method = getattr(plugin_cls_or_instance, "enabled")
    if not callable(enabled_method):
        # this is an error, as enabled must be a callable.
        raise TypeError(
            f"Expected '{enabled_method}.enabled()' to be a callable, got"
            f" {type(enabled_method).__name__}."
        )
    return plugin_cls_or_instance.enabled()


class InterfaceMeta(type):
    """Metaclass of Interfaces and Implementations

    This class follows Marty Alchin's principle of MountPoints.
    Thanks for his GREAT software pattern.
    """

    _interfaces = {}

    def __iter__(mcs) -> typing.Iterable:
        """Returns an object with all enabled plugins, where you can iterate over."""

        def _get_sort_attr_value(element):
            sort_attr = _get_sort_attr(mcs)
            return getattr(element, sort_attr, 0)

        if mcs is Interface:
            raise TypeError("The <Interface> class cannot be iterated over directly.")
        # return only enabled plugins
        plugin_list = [impl for impl in mcs._implementations if impl.enabled()]
        # if __sort_attribute__ attribute is available, sort list by given attribute
        # else use "weight" as default

        plugin_list.sort(key=_get_sort_attr_value)
        return iter(plugin_list)
        # return iter(sorted(plugin_list, key=get_sort_attr))

    def __lt__(mcs, other):
        """Allows plugins to be sorted by their weight attribute."""
        return getattr(mcs, _get_sort_attr(mcs), 0) < getattr(
            other, _get_sort_attr(other), 0
        )

    def __getitem__(mcs, item) -> typing.Self:
        """Allow the Interface class to be accessed like a dictionary, where the keys represent the names of the interfaces, and the values are the corresponding interfaces."""
        # FIXME: only respond if called from an interface, not from an implementation.
        if item not in mcs._interfaces:
            raise KeyError(f"Interface '{item}' not registered.")
        return mcs._interfaces[item]

    def __len__(mcs) -> int:
        """Return the number of plugins that implement this interface."""
        return len(mcs.enabled_plugins())

    def __contains__(mcs, cls: type) -> bool:
        """Returns True if there is a plugin implementing this interface."""
        # TODO: test
        if getattr(mcs, "__instantiate_plugins__", True):
            return cls in [type(impl) for impl in mcs._implementations]
        else:
            return cls in mcs._implementations

    def __repr__(mcs) -> str:
        """Returns a textual representation of the interface/implementation."""
        if Interface in mcs.__bases__:
            # if this class is a direct child of `Interface`, then it is an interface.
            return f"<Interface '{mcs.__name__}'>"
        else:
            interfaces = []
            # all descendants further down are implementations
            # traverse the MRO until an interface (or more) is/are found
            for base in mcs.__mro__:
                if Interface in base.__bases__:
                    interfaces.append(base)
            if len(interfaces) == 0:
                raise ValueError(f"No interface found for {mcs.__name__}")
            elif len(interfaces) == 1:
                return (
                    f"<Implementation '{mcs.__name__}' of Interface '"
                    f"{interfaces[0].__name__}'>"
                )
            else:
                return (
                    f"<Implementation '{mcs.__name__}' of Interfaces "
                    + ", ".join(f"'{i.__name__}'" for i in interfaces)
                    + ">"
                )


__interfaces = []


class Interface(metaclass=InterfaceMeta):
    """The base class for plugin interfaces."""

    @classmethod
    def plugins(cls) -> typing.Iterable:
        warnings.warn(
            f"<Interface>.plugins() is deprecated and will be removed. "
            f"Please iterate directly over the '{cls.__name__}' class (= '{cls.__name__}.enabled_plugins()"
            f"'), '.all_plugins()' or '.disabled_plugins()'.",
            DeprecationWarning,
        )
        return cls._implementations

    def __init_subclass__(cls):
        if hasattr(cls, "_implementations"):
            # this is already a subclass of your interface, meaning it is an implementation
            cls.__interface__ = False
            # set `_implementations` instance attr to empty set, as it should not be
            # possible to iterate over plugins: the user must use the interface!
            cls._implementations = set()
            instanciate = getattr(cls, "__instantiate_plugins__", True)
            if instanciate:
                plugin = cls()
            else:
                plugin = cls

            for base in cls.__mro__[1:]:
                if hasattr(base, "_implementations"):
                    base._implementations.add(plugin)
        else:
            # this is a new interface
            cls._implementations = set()
            cls.__interface__ = True

            if cls.__name__ in cls._interfaces:
                raise ValueError(
                    f"Duplicate interface '{cls.__name__}'. Interfaces must have unique names."
                )
            cls._interfaces[cls.__name__] = cls
            if not cls.__name__.startswith("I"):
                warnings.warn(
                    f"WARNING: <{cls.__name__}>: Interface names should start with a "
                    f"capital 'I'."
                )
            if getattr(cls, "__service__", None) is not None:
                warnings.warn(
                    "WARNING: <{cls.__name__}>: __service__ attribute is "
                    "deprecated. ",
                    DeprecationWarning,
                    1,
                )
                if getattr(cls, "__instantiate_plugins__", None) is not None:
                    raise AttributeError(
                        "Both '__instantiate_plugins__' and '__service__' are mutually exclusive."
                    )
                cls.__instanciate_plugins__ = getattr(cls, "__service__", True)

    @classmethod
    def all_plugins(cls) -> list:
        """Returns all plugins, even if they are not enabled."""
        # return a list from _implementations, sorted by the plugin's weight.'
        return list(cls._implementations)

    @classmethod
    def enabled_plugins(mcs) -> list:
        """Returns a list of enabled plugins.

        Beware that this method is at the class level. Implementations' `enabled()`
        method must return a bool instead.
        """
        return [impl for impl in mcs if impl.enabled()]

    @classmethod
    def disabled_plugins(mcs) -> list:
        """Returns a list of disabled plugins.

        Beware that this method is at the class level. Implementations' `disabled()`
        method must return a bool instead.
        """
        return [impl for impl in mcs if not impl.enabled()]

    @classmethod
    def enabled(self):
        """Returns True if this plugin is enabled, else False.

        Beware that this is a class method, so if your plugins are classes
        (`__instantiate_plugins__= False`), you have to override the `@classmethod`.
        If your plugins are instances (=default), you have to implement the `enabled()`
        as a normal instance method.
        """
        return True

    @classmethod
    def first(cls) -> typing.Self | None:
        """Returns the first enabled plugin of this interface."""
        return cls.enabled_plugins()[0] if len(cls) > 0 else None

    @classmethod
    def last(cls) -> typing.Self | None:
        """Returns the last enabled plugin of this interface."""
        return cls.enabled_plugins()[-1] if len(cls) > 0 else None

    @classmethod
    def get(cls, name, default=None) -> typing.Self:
        """Returns the"""
        # TODO !!
        if name in cls._interfaces:
            return cls[name]
        return default


def require_app(app_config: AppConfig, required_app_name: str) -> None:
    """Helper function for AppConfig.ready() - checks if an app is installed.

    An ``ImproperlyConfigured`` Exception is raised if the required app is not present.

    :param app_config: the AppConfig which requires another app. usually use ``self`` here
            when called from AppConfig.ready()
    :param required_app_name: the required app name.
    """
    from django.apps import apps
    from django.core.exceptions import ImproperlyConfigured

    if app_config.name not in [app.name for app in apps.get_app_configs()]:
        raise ImproperlyConfigured(
            "The '{}' module relies on {}. Please add '{}' to your INSTALLED_APPS.".format(
                app_config.name, app_config.verbose_name, required_app_name
            )
        )
