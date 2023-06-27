"""
pythonedanixflakes/flake_repo.py

This file defines the FlakeRepo class.

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
from PythonEDA.repo import Repo
from PythonEDANixFlakes.flake import Flake
from PythonEDANixFlakes.flake_created import FlakeCreated
from PythonEDANixFlakes.recipe.flake_recipe import FlakeRecipe

import abc

from typing import Dict, List

class FlakeRepo(Repo, abc.ABC):
    """
    A subclass of Repo that manages Flakes.

    Class name: FlakeRepo

    Responsibilities:
        - Define the way Flakes are persisted and retrieved.

    Collaborators:
        - None
    """

    def __init__(self):
        """
        Creates a new FlakeRepo instance.
        """
        super().__init__(Flake)

    @abc.abstractmethod
    def find_by_name_and_version(self, name: str, version: str) -> Flake:
        """
        Retrieves a flake matching given name and version.
        :param name: The flake name.
        :type name: str
        :param version: The flake version.
        :type version: str
        :return: The matching flake.
        :rtype: Flake from pythonedanixflakes.flake
        """
        raise NotImplementedError("find_by_name_and_version() must be implemented by subclasses")

    @abc.abstractmethod
    def create(self, flake: Flake, content: List[Dict[str, str]], recipe: FlakeRecipe) -> FlakeCreated:
        """
        Creates the flake.
        :param flake: The flake.
        :type: Flake from pythonedanixflakes.flake
        :param content: The flake content.
        :type content: List[Dict[str, str]]
        :param recipe: The flake recipe.
        :type recipe: FlakeRecipe from pythonedanixflakes.recipe.flake_recipe
        :return: A FlakeCreated event.
        :rtype: FlakeCreated from pythonedaeventnixflakes.flake_created
        """
        raise NotImplementedError("create() must be implemented by subclasses")

    @abc.abstractmethod
    def url_for_flake(self, name: str, version: str) -> str:
        """
        Retrieves the url of given flake.
        :param name: The flake name.
        :type name: str
        :param version: The flake version.
        :type version: str
        :return: The url of the flake.
        :rtype: str
        """
        raise NotImplementedError("url_for_flake() must be implemented by subclasses")
