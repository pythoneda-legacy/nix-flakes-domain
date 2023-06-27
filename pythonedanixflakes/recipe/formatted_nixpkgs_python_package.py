"""
pythonedanixflakes/recipe/formatted_nixpkgs_python_package.py

This file defines the FormattedNixpkgsPythonPackage class.

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
from pythonedasharedpythonpackages.python_package import PythonPackage
from pythonedanixflakes.recipe.formatted_python_package import FormattedPythonPackage


class FormattedNixpkgsPythonPackage(FormattedPythonPackage):
    """
    Augments PythonPackage class for nixpkgs packages to include formatting logic required by recipe templates.

    Class name: FormattedNixpkgsPythonPackage

    Responsibilities:
        - Augments PythonPackage class for nixpkgs packages to include formatting logic required by recipe templates.

    Collaborators:
        - PythonPackage
    """

    def __init__(self, pkg: PythonPackage):
        """
        Creates a new instance.
        :param pkg: The Python package.
        :type pkg: PythonPackage from pythonedasharedpythonpackages.python_package
        """
        super().__init__(pkg)

    def as_parameter_to_package_nix(self) -> str:
        """
        Builds the subtemplate to pass this Python package as parameter to package.nix.
        :return: Such subtemplate.
        :rtype: str
        """
        return self._formatted.name

    def overrides(self) -> str:
        """
        Builds the subtemplate to override this Python package.
        :return: Such subtemplate.
        :rtype: str
        """
        return "TODO: {self._formatted.name}"
