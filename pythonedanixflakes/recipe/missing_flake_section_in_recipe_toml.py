"""
pythonedanixflakes/recipe/missing_flake_section_in_recipe_toml.py

This file defines the MissingFlakeSectionInRecipeToml class.

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

class MissingFlakeSectionInRecipeToml(Exception):
    """
    A recipe.toml does not include a [flake] section.

    Class name: MissingFlakeSectionInRecipeToml

    Responsibilities:
        - Represent the error when a recipe.toml does not include a [flake] section.

    Collaborators:
        - None
    """
    def __init__(self, message:str=None, extraInfo:Dict=None):
        """
        Creates a new MissingFlakeSectionInRecipeToml instance.
        :param message: The error message.
        :type message: str
        :param extraInfo: Additional information.
        :type extraInfo: Dict
        """
        super().__init__(message)
        self._extra_info = extra_info

    @property
    def extra_info(self) -> Dict:
        """
        Retrieves the additional information.
        :return: Such information.
        :rtype: Dict
        """
        return self._extra_info
