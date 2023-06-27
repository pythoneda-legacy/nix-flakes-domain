"""
pythonedanixflakes/recipe/flake_recipe_repo.py

This file defines the FlakeRecipeRepo class.

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
from pythoneda.repo import Repo
from pythonedanixflakes.flake import Flake
from pythonedanixflakes.recipe.flake_recipe import FlakeRecipe

import abc
from typing import List

class FlakeRecipeRepo(Repo, abc.ABC):
    """
    A subclass of Repo that manages Flake recipes.

    Class name: FlakeRecipeRepo

    Responsibilities:
        - Repository of FlakeRecipe instances.

    Collaborators:
        - None
    """

    def __init__(self):
        """
        Creates a new FlakeRecipeRepo instance.
        """
        super().__init__(FlakeRecipe)

    @abc.abstractmethod
    def find_recipe_classes_by_flake(self, flake: Flake) -> List[FlakeRecipe]:
        """
        Retrieves the recipe classes matching given flake, if any.
        :param flake: The flake.
        :type flake: Flake from pythonedanixflakes.flake
        :return: The recipe classes.
        :rtype: List[FlakeRecipe from pythonedanixflakes.recipe.flake_recipe]
        """
        raise NotImplementedError(
            "find_recipe_classes_by_flake() must be implemented by subclasses"
        )
