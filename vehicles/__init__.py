import os, sys, inspect
from importlib import import_module

def getAllVehicleClasses() -> list[str]:
    classes: list[str] = []
    directory = os.path.dirname(__file__)

    for file in os.listdir(directory):
        if file.endswith(".py") and file != "__init__.py":
            classes.append(file[:-3])

            import_module("." + file[:-3], "QgisSweptPath.vehicles")
            module = import_module("." + file[:-3], "QgisSweptPath.vehicles")

            for name, obj in inspect.getmembers(module):
                if inspect.isclass(obj):
                    pass

    print(classes)
    return classes


__all__ = getAllVehicleClasses()