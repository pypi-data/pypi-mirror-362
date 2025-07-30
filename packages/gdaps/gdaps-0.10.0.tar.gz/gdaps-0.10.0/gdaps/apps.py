import logging
import sys

import importlib.metadata

from django.conf import settings
from django.core.exceptions import ImproperlyConfigured

from gdaps import __version__
from gdaps import api
from gdaps.pluginmanager import PluginManager

logger = logging.getLogger(__name__)


class GdapsPluginMeta:
    """This is the PluginMeta class of GDAPS itself."""

    version = __version__
    verbose_name = "Generic Django Application Plugin System"
    author = "Christian Gonzalez"
    author_email = "christian.gonzalez@nerdocs.at"
    category = "GDAPS"
    # hidden = True


class GdapsConfig(api.PluginConfig):
    name = "gdaps"
    PluginMeta = GdapsPluginMeta

    def ready(self):
        # walk through all installed plugins and check some things
        for app in PluginManager.plugins():
            if hasattr(app.PluginMeta, "compatibility"):
                try:
                    importlib.metadata.version(app.PluginMeta.compatibility)
                except importlib.metadata.PackageNotFoundError as e:
                    logger.critical("Incompatible plugins found!")
                    logger.critical(
                        f"Plugin {app.name} requires {app.PluginMeta.compatibility}, "
                        f"but it is not installed."
                    )

                    sys.exit(1)

        try:
            settings.PROJECT_NAME
        except AttributeError:
            raise ImproperlyConfigured(
                "Please define a PROJECT_NAME in your settings.py"
            )

        # load all generic gdaps.plugins - they must be implementations of GDAPS Interfaces
        logger.info("Loading gdaps plugins...")
        for entry_point in importlib.metadata.entry_points(group="gdaps.plugins"):
            # it is enough to have them instantiated, as they are remembered internally in their interface.
            entry_point.load()
