from PythonEDA.event import Event
from PythonEDA.value_object import primary_key_attribute


class FlakeAvailable(Event):
    """
    Represents the event when a Nix flake for a Python package is already available
    """

    def __init__(
        self,
        packageName: str,
        packageVersion: str
    ):
        """Creates a new FlakeAvailable instance"""
        super().__init__()
        self._package_name = packageName
        self._package_version = packageVersion

    @property
    @primary_key_attribute
    def package_name(self):
        return self._package_name

    @property
    @primary_key_attribute
    def package_version(self):
        return self._package_version
