import pkgutil, inspect
from importlib import import_module
from os.path import dirname, join


class VehicleFactory:
    @staticmethod
    def get_classes() -> dict[str, tuple[str, str]]:
        """
        Get a dictionary of all main vehicle classes
        The structure is as follows:
            {vehicle name:
                {class name: module name}
            }
        @return dictionary with infos for dynamic vehicle class import
        """

        class_dict: dict[str, tuple[str, str]] = {}
        # path to the vehicle subpackage
        pkgpath = join(dirname(__file__), "vehicles")

        # Loop over all modules in vehicle package
        for i, n, pkg in pkgutil.iter_modules([pkgpath]):
            # n is the name of the module
            # Import all the modules
            module = import_module(".{}".format(n), "QgisSweptPath.vehicles")
            # Loop over all members of each module
            for name, cls in inspect.getmembers(module):
                # Get only the classes with the class attribute is_main_vehicle set to True
                if inspect.isclass(cls) and cls.is_main_vehicle:
                    # Add the infos to the dict
                    class_dict[cls.vehicle_name] = (cls.__name__, n)

        return class_dict
