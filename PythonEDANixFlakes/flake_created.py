from PythonEDA.event import Event
from PythonEDA.value_object import primary_key_attribute, attribute
from PythonEDANixFlakes.recipe.flake_recipe import FlakeRecipe

class FlakeCreated(Event):
    """
    Represents the event when a Nix flake for a Python package has been created
    """
    def __init__(self, packageName: str, packageVersion: str, flakeFolder: str, flakeRecipe: FlakeRecipe):
        """Creates a new FlakeCreated instance"""
        super().__init__()
        self._package_name = packageName
        self._package_version = packageVersion
        self._flake_folder = flakeFolder
        self._flake_recipe = flakeRecipe

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

    @property
    @attribute
    def flake_recipe(self):
        return self._flake_recipe
