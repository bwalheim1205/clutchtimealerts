import os
import importlib
from importlib.metadata import entry_points
import logging
from clutchtimealerts.notifications.base import Notification

logger = logging.getLogger("clutchtimealerts")


class NotificationCollector:
    def __init__(self):
        self.classname_dict = {}
        self.common_name_dict = {}

    def _folder_path_module_path(self, folder_path):
        """
        Convert a folder path to a module path relative to the 'clutchtimealerts' package.

        This method takes a file system path to a folder and converts it into a
        module path that is relative to the 'clutchtimealerts' package. This is
        useful for dynamically importing modules based on their file location.

        Parameters
        ----------
        folder_path : str
            The file system path to the folder.

        Returns
        -------
        str
            The module path corresponding to the folder path.
        """
        root_path = "clutchtimealerts" + folder_path.rsplit("clutchtimealerts", 1)[1]
        module_path = root_path.replace("/", ".")
        return module_path

    def _iter_plugin_entrypoints(self):
        return entry_points(group="clutchtimealerts.notification_plugins")

    def _add_notification_class(self, cls):
        """Registers a discovered Notification subclass."""
        if not issubclass(cls, Notification) or cls is Notification:
            return

        self.classname_dict[cls.__name__] = cls
        self.common_name_dict[getattr(cls, "COMMON_NAME", cls.__name__)] = cls
        logger.debug(f"Registered: {cls.__name__}")

    def _collect_package_notifications(self, folder_path):
        """
        Collect notification classes from Python files in the specified folder.

        This method iterates through all Python files in the given folder, imports
        them as modules and gets all subclasses of Notification base class.
        It populates two dictionaries: one mapping class names to class objects
        and another mapping common names to class objects.

        Parameters
        ----------
        folder_path : str
            The path to the folder containing the Python files to be scanned for
            notification classes.

        Returns
        -------
        None
        """
        module_path = self._folder_path_module_path(folder_path)
        for file in os.listdir(folder_path):
            if file.endswith(".py"):
                module_name = file[:-3]
                try:
                    module = importlib.import_module(f"{module_path}.{module_name}")
                    logger.debug(f"Imported module: {module_path}.{module_name}")
                except ImportError:
                    logger.warning(
                        f"Error importing module: {module_path}.{module_name} ... skipping"
                    )
                    continue
                # Loads classes from module
                for obj in module.__dict__.values():
                    if isinstance(obj, type):
                        self._add_notification_class(obj)

    def _collect_plugin_notifications(self):
        """
        Collect notifications from any plugins that are loaded. Collects
        from the entrypoint clutchtimealerts.notifaction_plugins. It
        populates two dictionaries: one mapping class names to class objects
        and another mapping common names to class objects.

        Returns
        -------
        None
        """
        eps = self._iter_plugin_entrypoints()

        for ep in eps:
            try:
                cls = ep.load()
                logger.debug(f"Loaded plugin entry point: {ep.name}")
                self._add_notification_class(cls)
            except Exception as e:
                logger.warning(f"Failed loading plugin '{ep.name}': {e}")

    def collect_notifications(self, folder_path):
        """
        Collect notifications from both specified folder and from any plugins
        that are loaded. It populates two dictionaries: one mapping
        class names to class objects and another mapping common names to class objects.

        Returns
        -------
        None
        """
        self._collect_package_notifications(folder_path)
        self._collect_plugin_notifications()


if __name__ == "__main__":
    dir = os.path.dirname(__file__) + "/notifications"
    collector = NotificationCollector()
    collector.collect_notifications(dir)
