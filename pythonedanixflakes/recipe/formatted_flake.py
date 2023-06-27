"""
pythonedanixflakes/recipe/formatted_flake.py

This file defines the FormattedFlake class.

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
from pythoneda.formatting import Formatting
from pythonedanixflakes.flake import Flake
from pythonedanixflakes.flake.license import License

class FormattedFlake(Formatting):
    """
    Augments Flake class to include formatting logic required by recipe templates.

    Class name: FormattedFlake

    Responsibilities:
        - Augment Flake class to include formatting logic required by recipe templates.

    Collaborators:
        - Flake
    """

    def __init__(self, flk: Flake):
        """
        Creates a new instance.
        :param flake: The flake to augment.
        :type flake: Flake from pythonedanixflakes.flake
        """
        super().__init__(flk)

    @property
    def flake(self) -> Flake:
        """
        Retrieves the flake.
        :return: Such flake.
        :rtype: Flake from pythonedanixflakes.flake
        """
        return self._fmt

    def version_with_underscores(self) -> str:
        """
        Retrieves the version, with underscores.
        :return: Such variant of the version.
        :rtype: str
        """
        return self.flake.version.replace(".", "_")

    def description(self) -> str:
        """
        Retrieves the description of the Python package.
        :return: The description.
        :rtype: str
        """
        return self.flake.python_package.info["description"]

    def license(self) -> str:
        """
        Retrieves the license of the Python package.
        :return: Such information.
        :rtype str:
        """
        return License.from_pypi(self.flake.python_package.info.get("license", "")).nix

    def sha256(self) -> str:
        """
        Retrieves the SHA-256 hash of the Python package.
        :return: Such information.
        :rtype: str
        """
        return self.flake.python_package.release.get("hash", "")

    def repo_url(self) -> str:
        """
        Retrieves the url of the repository.
        :return: Such url.
        :rtype: str
        """
        result = ""
        if self.flake.python_package.git_repo:
            result = self.flake.python_package.git_repo.url
        return result

    def repo_rev(self) -> str:
        """
        Retrieves the revision of the repository.
        :return: Such revision.
        :rtype: str
        """
        result = ""
        if self.flake.python_package.git_repo:
            result = self.flake.python_package.git_repo.rev
        return result

    def repo_owner(self) -> str:
        """
        Retrieves the owner of the repository.
        :return: Such information.
        :rtype: str
        """
        result = ""
        if self.flake.python_package.git_repo:
            result, _ = self.flake.python_package.git_repo.repo_owner_and_repo_name()
        return result

    def repo_name(self):
        """
        Retrieves the name of the repository.
        :return: Such information.
        :rtype: str
        """
        result = ""
        if self.flake.python_package.git_repo:
            _, result = self.flake.python_package.git_repo.repo_owner_and_repo_name()
        return result
