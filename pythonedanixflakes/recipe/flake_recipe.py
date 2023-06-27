"""
pythonedanixflakes/recipe/flake_recipe.py

This file defines the FlakeRecipe class.

Copyright (C) 2023-today rydnr's pythoneda/nix-flakes

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""
from pythoneda.entity import Entity
from pythoneda.value_object import primary_key_attribute
from pythonedanixflakes.flake import Flake
from pythonedanixflakes.recipe.empty_flake_metadata_section_in_recipe_toml import EmptyFlakeMetadataSectionInRecipeToml
from pythonedanixflakes.recipe.empty_flake_section_in_recipe_toml import EmptyFlakeSectionInRecipeToml
from pythonedanixflakes.recipe.missing_flake_section_in_recipe_toml import MissingFlakeSectionInRecipeToml
from pythonedanixflakes.recipe.missing_flake_version_spec_in_recipe_toml import MissingFlakeVersionSpecInRecipeToml
from pythonedanixflakes.recipe.missing_recipe_toml import MissingRecipeToml
from pythonedanixflakes.recipe.missing_type_in_flake_metadata_section_in_recipe_toml import MissingTypeInFlakeMetadataSectionInRecipeToml
from pythonedanixflakes.recipe.more_than_one_flake_in_recipe_toml import MoreThanOneFlakeInRecipeToml

import abc
import inspect
import logging
import os
from pathlib import Path
import toml
from typing import Dict, List

class FlakeRecipe(Entity, abc.ABC):
    """
    Represents a nix flake recipe.

    Class name: FlakeRecipe

    Responsibilities:
        - Represent recipes of how to build Nix flakes.

    Collaborators:
        - Flakes: To build them.
    """

    _flakes = []

    def __init__(self, flake: Flake):
        """
        Creates a new flake recipe instance.
        :param flake: The flake.
        :type flake: Flake from pythonedanixflakes.flake
        """
        super().__init__()
        self._flake = flake

    @property
    @primary_key_attribute
    def flake(self) -> Flake:
        """
        Retrieves the flake.
        :return: The flake.
        :rtype flake: Flake from pythonedanixflakes.flake
        """
        return self._flake

    @classmethod
    def initialize(cls):
        """
        Initializes the class.
        """
        if cls.should_initialize():
            cls._flakes = cls.supported_flakes()
            cls._type = cls.flake_type()

    @classmethod
    def should_initialize(cls) -> bool:
        """
        Checks if this class needs initalization.
        :return: True in such case.
        :rtype: bool
        """
        return cls != FlakeRecipe

    @classmethod
    def recipe_toml_file(cls) -> str:
        """
        Retrieves the recipe.toml file.
        :return: Such path.
        :rtype: str
        """
        recipe_folder = Path(inspect.getsourcefile(cls)).parent
        return os.path.join(recipe_folder, "recipe.toml")

    @classmethod
    def read_recipe_toml(cls):
        """
        Reads the recipe.toml file.
        """
        result = ""
        recipe_toml_file = cls.recipe_toml_file()
        if not os.path.exists(recipe_toml_file):
            raise MissingRecipeToml(recipe_toml_file)
        recipe_toml_contents = ""
        with open(recipe_toml_file, "r") as file:
            recipe_toml_contents = file.read()
        result = toml.loads(recipe_toml_contents)
        return result

    @classmethod
    def supported_flakes(cls) -> List[Dict[str, str]]:
        """
        Retrieves the list of supported flakes.
        :return: Such list.
        :rtype: List[Dict[str, str]]
        """
        result = []
        recipe_toml = cls.read_recipe_toml()
        flake_specs = recipe_toml.get("flake", {})
        if not flake_specs:
            raise MissingFlakeSectionInRecipeToml(cls.recipe_toml_file())
        entries = list(flake_specs.keys())
        if not entries or len(entries) == 0:
            raise EmptyFlakeSectionInRecipeToml(cls.recipe_toml_file())
        for flake in entries:
            version_spec = flake_specs.get(flake, "")
            if not version_spec:
                raise MissingFlakeVersionSpecInRecipeToml(flake, cls.recipe_toml_file())
            aux = {}
            aux[flake] = version_spec
            result.append(aux)
        return result

    @classmethod
    def flake_type(cls) -> str:
        """
        Retrieves the type of flake.
        :return: The type.
        :rtype: str
        """
        result = None
        recipe_toml = cls.read_recipe_toml()
        flake_metadata = recipe_toml.get("flake").get("metadata", {})
        if flake_metadata:
            result = flake_metadata.get("type", None)
            if not result:
                raise MissingTypeInFlakeMetadataSectionInRecipeToml(cls.recipe_toml_file())
        return result

    @abstractmethod
    def process(self): # -> FlakeCreated:
        """
        Performs the recipe tasks.
        :return: A FlakeCreated event.
        :rtype: FlakeCreated from pythonedaeventnixflakes.flake_created
        """
        raise NotImplementedError()

    @classmethod
    def compatible_versions(cls, v1: str, v2: str) -> bool:
        """
        Checks if given versions are compatible.
        :param v1: One version.
        :type v1: str
        :param v2: The other version.
        :type v2: str
        :return: True if they are compatible.
        :rtype: bool
        """
        raise NotImplementedError()

    @classmethod
    def supports(cls, flake: flake) -> bool:
        """
        Checks if the recipe class supports given flake.
        :param flake: The flake.
        :type flake: Flake from pythonedanixflakes.flake
        :return: True if the flake is supported.
        :rtype: bool
        """
        raise NotImplementedError()

    @classmethod
    def type_matches(cls, flake: Flake) -> bool:
        """
        Checks if the type matches.
        :param flake: The flake.
        :type flake: Flake from pythonedanixflakes.flake
        :return: True if the type matches.
        :rtype: bool
        """
        return cls._type == flake.python_package.get_type()

    @classmethod
    def similarity(cls, flake: Flake) -> float:
        """
        Figures out the similarity of this recipe to given flake.
        :param flake: The flake.
        :type flake: Flake from pythonedanixflakes.flake
        :return: A similarity value between 0.0 and 1.0
        :rtype: float
        """
        result = 0.0
        partialResults = []
        if cls.supports(flake):
            return 1.0
        if cls.type_matches(flake):
            partialResults.append(0.5)
        for entry in cls._flakes:
            partialResult = 0.0
            name = list(entry.keys())[0]
            version = entry[name]
            if name == flake.name:
                if version == flake.version:
                    return 1.0
                elif cls.compatible_versions(version, flake.version):
                    partialResult = 0.9
                else:
                    partialResult = 0.7
            partialResults.append(partialResult)
        result = max(partialResults)
        logging.getLogger(cls.__name__).debug(f'Similarity between recipe {cls.__name__} and flake {flake.name}-{flake.version}: {result}')
        return result

    def uses_git_repo_sha256(self) -> bool:
        """
        Checks if the recipe uses the SHA-256 hash of the git repository.
        :return: True in such case.
        :rtype: bool
        """
        return False

    def uses_pip_sha256(self):
        """
        Checks if the recipe uses the SHA-256 hash of the pip package.
        :return: True in such case.
        :rtype: bool
        """
        return False

    def remove_duplicates(self, *lists) -> List:
        """
        Removes duplicates in given list.
        :param list: The list.
        :type list: List
        :return: The trimmed list.
        :rtype: List
        """
        result = []
        for lst in lists:
            for item in lst:
                if item not in result:
                    result.append(item)
        return result
