"""
pythonedanixflakes/recipe/recipe_does_not_support_placeholder.py

This file defines the RecipeDoesNotSupportPlaceholder error class.

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
from typing import Dict

class RecipeDoesNotSupportPlaceholder(Exception):
    """
    A recipe does not include a required placeholder.

    Class name: RecipeDoesNotSupportPlaceholder

    Responsibilities:
        - Represent the error when a recipe does not include a required placeholder.

    Collaborators:
        - None
    """
    def __init__(self, placeholder: str, functionName: str, recipeClass: str):
        """
        Creates a new RecipeDoesNotSupportPlaceholder instance.
        :param message: The error message.
        :type message: str
        :param extraInfo: Additional information.
        :type extraInfo: Dict
        """
        super().__init__(f'Function {functionName} not implemented for placeholder {placeholder} in recipe class {recipeClass}')
        self._placeholder = placeholder
        self._function_name = functionName
        self._recipe_class = recipeClass

    @property
    def placeholder(self) -> str:
        """
        Retrieves the placeholder.
        :return: Such information.
        :rtype: str
        """
        return self._placeholder

    @property
    def function_name(self) -> str:
        """
        Retrieves the function name.
        :return: Such information.
        :rtype: str
        """
        return self._function_name


    @property
    def recipe_class(self) -> str:
        """
        Retrieves the recipe class.
        :return: Such information.
        :rtype: str
        """
        return self._recipe_class
