# # from letterboxdpy.review import Review

import re


data = "/ajax/film:51610/report-form"

match = re.search(r'/film:(\d+)/', data)
print(int(match.group(1)))


def set_property(self, value, property_name: str) -> None:
    """Sets the specified property to the given value."""
    if hasattr(self, property_name):
        setattr(self, property_name, value)
    else:
        raise AttributeError(f"{property_name} is not a valid attribute of {self.__class__.__name__}")


