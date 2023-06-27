"""
pythonedanixflakes/flake_in_progress.py

This file defines the FlakeInProgress class.

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
from pythoneda.entity_in_progress import EntityInProgress
from pythoneda.value_object import attribute, primary_key_attribute
from pythonedasharedpythonpackages.python_package import PythonPackage


class FlakeInProgress(EntityInProgress):
    """
    Represents a flake which doesn't have all information yet.

    Class name: FlakeInProgress

    Responsibilities:
        - Represent a not-fully-complete Flake.

    Collaborators:
        - None
    """
    def __init__(self, name: str, version: str, flakeFolder: str):
        """
        Creates a new FlakeInProgress instance.
        :param name: The name of the flake.
        :type name: str
        :param version: The version of the flake.
        :type version: str
        :param flakeFolder: The flake folder.
        :type flakeFolder: str
        :param pythonPackage: The Python package.
        :type pythonPackage: PythonPackage from pythonedasharedpythonpackages.python_package
        """
        super().__init__()
        self._name = name
        self._version = version
        self._flake_folder = flakesFolder
        self._python_package = None

    @property
    @primary_key_attribute
    def name(self) -> str:
        """
        Retrieves the name of the flake.
        :return: The name.
        :rtype: str
        """
        return self._name

    @property
    @primary_key_attribute
    def version(self) -> str:
        """
        Retrieves the version of the flake.
        :return: The version.
        :rtype: str
        """
        return self._version

    @property
    @attribute
    def flake_folder(self) -> str:
        """
        Retrieves the flake folder.
        :return: The folder.
        :rtype: str
        """
        return self._flake_folder

    @property
    @attribute
    def python_package(self) -> PythonPackage:
        """
        Retrieves the Python package.
        :return: Such package.
        :rtype: PythonPackage from pythonedasharedpythonpackages.python_package
        """
        return self._python_package

    def set_python_package(self, pythonPackage: PythonPackage):
        """
        Specifies the Python package.
        :param pythonPackage: Such package.
        :type pythonPackage: PythonPackage from pythonedasharedpythonpackages.python_package
        """
        self._python_package = pythonPackage
