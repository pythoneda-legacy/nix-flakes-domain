from PythonEDA.event import Event
from PythonEDA.value_object import attribute, primary_key_attribute

class FlakeBuilt(Event):
    """
    Represents the event when a Nix flake for a Python package has been built successfully.
    """

    def __init__(self, packageName: str, packageVersion: str, flakeFolder: str):
        """Creates a new FlakeBuilt instance"""
        super().__init__()
        self._package_name = packageName
        self._package_version = packageVersion
        self._flake_folder = flakeFolder

    @property
    @primary_key_attribute
    def package_name(self):
        return self._package_name

    @property
    @primary_key_attribute
    def package_version(self):
        return self._package_version

    @property
    @attribute
    def flake_folder(self):
        return self._flake_folder
