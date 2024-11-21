import os
import importlib
from clutchtimebot.notifications.base import Notification


class NotificationCollector:
    def __init__(self):
        self.classname_dict = {}
        self.common_name_dict = {}

    def _folder_path_module_path(self, folder_path):
        """
        Convert a folder path to a module path relative to the 'clutchtimebot' package.

        This method takes a file system path to a folder and converts it into a
        module path that is relative to the 'clutchtimebot' package. This is
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
        root_path = "clutchtimebot" + folder_path.rsplit("clutchtimebot", 1)[1]
        module_path = root_path.replace("/", ".")
        return module_path

    def collect_notifications(self, folder_path):
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
                module = importlib.import_module(f"{module_path}.{module_name}")
                for name, obj in vars(module).items():
                    if (
                        isinstance(obj, type)
                        and issubclass(obj, Notification)
                        and obj != Notification
                    ):
                        self.classname_dict[name] = obj
                        self.common_name_dict[obj.COMMON_NAME] = obj


if __name__ == "__main__":
    dir = os.path.dirname(__file__) + "/notifications"
    collector = NotificationCollector()
    collector.collect_notifications(dir)