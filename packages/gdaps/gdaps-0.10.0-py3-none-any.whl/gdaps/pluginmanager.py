import importlib
import logging
import os
import warnings
from typing import List, Union

from django.apps import apps
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.db.models import QuerySet
from django.urls import include, path
import importlib.metadata

from gdaps.api import PluginConfig
from gdaps.exceptions import PluginError

__all__ = ["PluginManager"]

logger = logging.getLogger(__name__)


# with Python 3.7 we could use this instead of a plugin_spec dict:
#
# @dataclass
# class PluginSpec:
#     name: str
#     app_name: str
#     verbose_name: str
#     description: str
#     vendor: str
#     version: semver.VersionInfo
#     core_compat_version: semver.VersionInfo
#     author: str
#     author_email: str
#     category: str = "Misc"
#     enabled: bool = True
#     dependencies: list = ['core']


# class Singleton(type):
#     """A Metaclass implementing the Singleton pattern.
#
#     This class is for internal use only
#     """
#
#     _instances = {}
#
#     def __call__(cls, *args, **kwargs):
#         if cls not in cls._instances:
#             cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
#         return cls._instances[cls]


class PluginManager:
    """A Generic Django Plugin Manager that finds Django app plugins in a
    plugins folder or setuptools entry points and loads them dynamically.
    It provides a couple of methods to interact with plugins, load submodules of all available plugins
    dynamically, or get a list of enabled plugins.
    Don't instantiate a ``PluginManager`` directly, just use its static and class methods directly.
    """

    group: str = ""
    _default_router = None
    _searched_for_hooks: bool = False

    def __init__(self):
        raise PluginError("PluginManager is not meant to be instantiated.")

    @classmethod
    def plugin_path(cls) -> str:
        """Returns the absolute path where application plugins live.

        This is basically the Django root + the dotted entry point.
        CAVE: this is not callable from within the settings.py file.
        """
        if not cls.group:
            raise ImproperlyConfigured(
                "Plugin path could not be determined. Please run PluginManager.alter_installed_plugins() in your settings.py first."
            )
        # TODO: use pathlib here
        return os.path.join(settings.BASE_DIR, *cls.group.split("."))

    @classmethod
    def find_plugins(cls, group: str) -> List[str]:
        """Finds plugins from entry points.
        This function is supposed to be called in settings.py after the
        INSTALLED_APPS variable. Therefore, it can not use global variables from
        settings, to prevent circle imports.

        :param group: a dotted path where to find plugin apps. This is used as
            'group' for entry points.
        :returns: A list of dotted app_names, which can be appended to
            INSTALLED_APPS.
        """

        warnings.warn(
            "The find_plugins() method is deprecated. Use alter_installed_apps() instead.",
            DeprecationWarning,
        )
        if not group:
            raise PluginError(
                "You have to specify an entry points group "
                "where GDAPS can look for plugins."
            )

        cls.group = group

        installed_plugin_apps = []
        entry_points = importlib.metadata.entry_points(group=group)
        for entry_point in entry_points:
            appname = entry_point.value
            if entry_point.attr:
                appname += "." + entry_point.attr
            installed_plugin_apps.append(appname)
            logger.info("Found plugin '{}'.".format(appname))

        return installed_plugin_apps

    @classmethod
    def alter_installed_apps(cls, installed_apps: list[str], group: str) -> None:
        """Lets plugins update INSTALLED_APPS and add their own apps to it, in arbitrary order.

        Call this method directly after your settings.INSTALLED_APPS declaration.
        """
        if not group:
            raise PluginError(
                "You have to specify an entry points group "
                "where GDAPS can look for plugins."
            )

        cls.group = group
        entry_points = importlib.metadata.entry_points(group=group)
        for entry_point in entry_points:
            appname = entry_point.module
            if entry_point.attr:
                module = importlib.import_module(appname)

                # if there is a function, call it
                if hasattr(module, "alter_installed_apps") and callable(
                    module.alter_installed_apps
                ):
                    module.alter_installed_apps(installed_apps)

                # if there is only a variable, append it
                elif hasattr(module, "INSTALLED_APPS"):
                    installed_apps += module.INSTALLED_APPS
                    appname += "." + entry_point.attr
                    installed_apps.append(appname)
                    logger.info(
                        f"Found plugin '{appname}': {', '.join([app for app in module.INSTALLED_APPS])}"
                    )

                # legacy: if there is nothing, append the module name.
                else:
                    appname += "." + entry_point.attr
                    if appname not in installed_apps:
                        installed_apps.append(appname)
                    logger.info(f"Found plugin '{appname}'.")
        cls.find_hooks()

    @staticmethod
    def plugins(skip_disabled: bool = False) -> List[PluginConfig]:
        """Returns a list of AppConfig classes that are GDAPS plugins.

        This method basically checks for the presence of a ``PluginMeta`` attribute
        within the AppConfig of all apps and returns a list of apps containing it.
        :param skip_disabled: If True, skips disabled plugins and only returns enabled ones. Defaults to ``False``.
        """

        # TODO: test plugins() method
        list = []
        for app in apps.get_app_configs():
            if not hasattr(app, "PluginMeta"):
                continue
            if app.PluginMeta is None:
                continue
            if skip_disabled:
                # skip disabled plugins per default
                if not getattr(app.PluginMeta, "enabled", "True"):
                    continue
            list.append(app)

        return list

    @classmethod
    def load_plugin_submodule(cls, submodule: str, mandatory=False) -> list:
        """
        Search plugin apps for specific submodules and load them.

        :param submodule: the dotted name of the Django app's submodule to
            import. This package must be a submodule of the
            plugin's namespace, e.g. "schema" - then
            ["<main>.core.schema", "<main>.laboratory.schema"] etc. will be
            found and imported.
        :param mandatory: If set to True, each found plugin _must_ contain the given
            submodule. If any installed plugin doesn't have it, a PluginError is raised.
        :return: a list of module objects that have been successfully imported.
        """
        modules = []
        importlib.invalidate_caches()
        for app in PluginManager.plugins():

            # import all the submodules from all plugin apps

            dotted_name = f"{app.name}.{submodule}"
            try:
                module = importlib.import_module(dotted_name)
                modules.append(module)
                logger.info(f" ✓ Successfully loaded plugin submodule {dotted_name}")
            except ImportError as e:
                if mandatory:
                    raise PluginError(
                        f"The '{app.name}' app does not contain a (mandatory) '{submodule}' module"
                    )

                # if THIS module is not present, just ignore it
                if str(e) == f"No module named '{dotted_name}'":
                    logger.info(f" i Ignoring missing submodule '{dotted_name}'. {e}")
                else:
                    # else the importing has another reason, like syntax errors in that module, etc.
                    logger.error(f" ✘ Error importing submodule '{dotted_name}': {e}")
        return modules

    @classmethod
    def find_hooks(cls):
        if not cls._searched_for_hooks:
            cls.load_plugin_submodule("gdaps_hooks")
            cls._searched_for_hooks = True

    @classmethod
    def router(cls) -> Union["SimpleRouter", "DefaultRouter"]:
        """Loads all plugins' urls.py and collects their routers into one.

        :returns: a list of routers that can be merged with the global router."""

        try:
            from rest_framework.routers import DefaultRouter, SimpleRouter
        except ImportError:
            return []

        module_list = PluginManager.load_plugin_submodule("urls")

        if not cls._default_router:
            if settings.DEBUG:
                cls._default_router = DefaultRouter()
            else:
                cls._default_router = SimpleRouter()

            for module in module_list:
                router = getattr(module, "router", None)  # type: SimpleRouter
                if router:
                    logger.info(
                        f" ✓ Extended global router table with router from module '{module.__name__}'."
                    )
                    cls._default_router.registry.extend(router.registry)

        return cls._default_router

    @staticmethod
    def urlpatterns() -> list:
        """Loads all plugins' urls.py and collects their urlpatterns.

        This is maybe not the best approach, but it allows plugins to
        have "global" URLs, and not only namespaced, and it is flexible

        :returns: a list of urlpatterns that can be merged with the global
                  urls.urlpattern."""

        # FIXME: the order the plugins are loaded is not deterministic. This can lead to serious problems,
        # as apps could use the same URL namespace, and depending on which one was loaded first, it may mask the other
        # URL. This has to be fixed.
        #
        # Another unmanaged problem is 'dependencies':
        # FIXME: a dependency manager must be implemented into the PluginManager

        module_list = PluginManager.load_plugin_submodule("urls")

        urlpatterns = []
        for module in module_list:
            if module.__name__.startswith("gdaps"):
                continue

            root_urlpatterns = getattr(module, "root_urlpatterns", None)
            if root_urlpatterns:
                logger.info(
                    f" ✓ Added urlpatterns from module '{module.__name__}' to global list."
                )
                urlpatterns += root_urlpatterns
            try:
                namespace = getattr(module, "app_name")
            except AttributeError:
                raise ImproperlyConfigured(
                    "A GDAPS plugin's urls.py must define an 'app_name'. "
                    f"Please do that for '{module.__name__}'"
                )
            if getattr(module, "urlpatterns", None):
                urlpatterns += [path(namespace + "/", include(module))]

        return urlpatterns

    ###############################################################
    #  The following methods require Django's ORM already setup.  #
    #  Don't call them during the setup process                   #
    ###############################################################

    @staticmethod
    def orphaned_plugins() -> QuerySet:
        """Returns a list of GdapsPlugin models that have no disk representance any more.

        .. note:: This method needs Django's ORM to be running.
        """

        from gdaps.models import GdapsPlugin

        return GdapsPlugin.objects.exclude(
            name__in=[app.name for app in PluginManager.plugins()]
        )
