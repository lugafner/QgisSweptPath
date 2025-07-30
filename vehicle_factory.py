import pkgutil, inspect
from importlib import import_module
from os.path import dirname, join, normpath, basename
import sys


class VehicleFactory:
    @staticmethod
    def get_classes(pkg_list: list[str] = []) -> dict[str, tuple[str, str]]:
        """
        Get a dictionary of all main vehicle classes
        The structure is as follows:
            {vehicle name:
                (class name, module name)
            }

        The parameter pkg_list is for user defined folder with additional vehicles. The default package .vehicles will
        always be imported. This directory must not be set in pkg_list.

        @param pkg_list: List of strings with absolute path to user defined package directories with additional vehicles
        @return dictionary with infos for dynamic vehicle class import
        """

        class_dict: dict[str, tuple[str, str]] = {}

        # path to the vehicle subpackage (default vehicle package)
        # Remove from package list if present to avoid double import
        default_vehicles = join(dirname(__file__), "vehicles")
        if default_vehicles in pkg_list:
            pkg_list.remove(default_vehicles)

        # List of all vehicle modules
        modules = []
        # Get all default vehicle modules from the vehicles folder in plugin directory
        try:
            for _, n, _ in pkgutil.iter_modules([default_vehicles]):
                modules.append(import_module(".{}".format(n), "QgisSweptPath.vehicles"))
        except ImportError as e:
            raise ImportError("Default vehicle package not available or damaged. Try to reinstall the plugin") from e

        # Loop over each location in package list
        for pkg in pkg_list:
            sys.path.append(pkg)  # Add directory to sys path
            package_name = basename(normpath(pkg))  # Get basename as package name
            try:
                    # Get all vehicle modules in specified package directories with basename as package name
                    for _, name, _ in pkgutil.iter_modules([pkg]):
                        modules.append(import_module(".{}".format(name), package_name))
            except ImportError as e:
                # TODO: Print warning message
                pass

        # Loop over all modules in module list
        for module in modules:
            # Loop over all members of each module
            for name, cls in inspect.getmembers(module):
                # Get only the classes with the class attribute is_main_vehicle set to True
                if inspect.isclass(cls) and cls.is_main_vehicle:
                    # Add the infos to the dict
                    class_dict[cls.vehicle_name] = (cls.__name__, module.__name__)

        return class_dict
