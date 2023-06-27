"""
pythonedanixflakes/recipe/base_flake_recipe.py

This file defines the BaseFlakeRecipe class.

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
from pythoneda.ports import Ports
from pythonedaeventnixflakes.flake_created import FlakeCreated
from pythonedanixflakes.flake import Flake
from pythonedanixflakes.license import License
from pythonedanixflakes.recipe.flake_recipe import FlakeRecipe
from pythonedanixflakes.recipe.formatted_flake import FormattedFlake
from pythonedanixflakes.recipe.formatted_flake_python_package import FormattedFlakePythonPackage
from pythonedanixflakes.recipe.formatted_nixpkgs_python_package import FormattedNixpkgsPythonPackage
from pythonedanixflakes.recipe.formatted_python_package_list import FormattedPythonPackageList
from pythonedasharednix.nix_template import NixTemplate
from pythonedasharedpythonpackages.python_package import PythonPackage

from enum import Enum
import inspect
import logging
from pathlib import Path
from typing import Dict, List

class BaseFlakeRecipe(FlakeRecipe):
    """
    Represents a base nix flake recipe.

    Class name: BaseFlakeRecipe

    Responsibilities:
        - Common data and behavior to all flake recipes.

    Collaborators:
        - Subtemplates: To define the available subtemplates.
    """
    def __init__(self, flake: Flake):
        """
        Creates a new base nix flake recipe instance.
        :param flake: The flake.
        :type flake: Flake from pythonedanixflakes.flake
        """
        super().__init__(flake)
        self._native_build_inputs_subtemplates = self.extract_dep_templates(flake, flake.native_build_inputs)
        self._propagated_build_inputs_subtemplates = self.extract_dep_templates(flake, flake.propagated_build_inputs)
        self._build_inputs_subtemplates = self.extract_dep_templates(flake, flake.build_inputs)
        self._check_inputs_subtemplates = self.extract_dep_templates(flake, flake.check_inputs)
        self._optional_build_inputs_subtemplates = self.extract_dep_templates(flake, flake.optional_build_inputs)
        self._subtemplates = self.extract_dep_templates(flake, list(
                set(flake.native_build_inputs)
            | set(flake.propagated_build_inputs)
            | set(flake.build_inputs)
            | set(flake.check_inputs)
            | set(flake.optional_build_inputs)))
        all = list(
                set(flake.native_build_inputs)
            | set(flake.propagated_build_inputs)
            | set(flake.build_inputs)
            | set(flake.check_inputs)
            | set(flake.optional_build_inputs))

    class Subtemplates(Enum):
        """
        Enumerated values for available subtemplates.

        Class name: Subtemplates

        Responsibilities:
            - Define known subtemplates.

        Collaborators:
            - None
        """
        NIXPKGS_DEPS = "nixpkgs_deps"
        FLAKE_DEPS = "flake_deps"
        ALL_DEPS = "all_deps"
        NIXPKGS_DECLARATION = "nixpkgs_declaration"
        FLAKES_DECLARATION = "flakes_declaration"
        NIXPKGS_AS_PARAMETER_TO_PACKAGE_NIX = "nixpkgs_as_parameter_to_package_nix"
        FLAKES_AS_PARAMETER_TO_PACKAGE_NIX = "flakes_as_parameter_to_package_nix"
        DECLARATION = "declaration"
        NIXPKGS_OVERRIDES = "nixpkgs_overrides"

    @classmethod
    def should_initialize(cls) -> bool:
        """
        Checks if the recipe needs initialization.
        :return: True in such case.
        :rtype: bool
        """
        return cls != BaseFlakeRecipe and super().should_initialize()

    @classmethod
    def supports(cls, flake: Flake) -> bool:
        """
        Checks if the recipe class supports given flake.
        :param flake: The flake.
        :type flake: Flake from pythonedanixflakes.flake
        """
        return False

    def process(self) -> FlakeCreated:
        """
        Processes the recipe.
        :return: A FlakeCreated event.
        :rtype: FlakeCreated from pythonedaeventnixflakes.flake_created
        """
        result = None
        renderedTemplates = []
        templates = Ports.instance().resolveNixTemplateRepo().find_flake_templates_by_recipe(self)
        if templates:
            for template in [ NixTemplate(t["folder"], t["path"], t["contents"]) for t in templates ]:
                renderedTemplates.append({ "folder": template.folder, "path": template.path, "contents": template.render(self.flake, self) })
            result = Ports.instance().resolveFlakeRepo().create(self.flake, renderedTemplates, self)
        else:
            logging.getLogger(__name__).critical(f'No templates provided by recipe {Path(inspect.getsourcefile(self.__class__)).parent}')
        return result

    def extract_dep_templates(self, flake: Flake, inputs: List[PythonPackage]) -> Dict[str, str]:
        """
        Extracts the dependency templates.
        :param flake: The flake.
        :type flake: Flake from pythonedanixflakes.flake
        :param inputs: The python packages
        :type inputs: List[PythonPackage from pythonedanixsharedpythonpackages.python_package]
        :return: The dependency templates.
        :rtype: Dict[str, str]
        """
        if inputs:
            nixpkgs_deps = FormattedPythonPackageList(self.remove_duplicates([FormattedNixpkgsPythonPackage(dep) for dep in inputs if dep.in_nixpkgs()]))
            flake_deps = FormattedPythonPackageList(self.remove_duplicates([FormattedFlakePythonPackage(dep) for dep in inputs if not dep.in_nixpkgs()]))
            all_deps = FormattedPythonPackageList(flake_deps.list + nixpkgs_deps.list)

            nixpkgs_declaration = FormattedPythonPackageList(nixpkgs_deps.list, "nixpkgs_declaration")
            flakes_declaration = FormattedPythonPackageList(flake_deps.list, "flake_declaration")
            nixpkgs_as_parameter_to_package_nix = FormattedPythonPackageList(nixpkgs_deps.list, "as_parameter_to_package_nix")
            flakes_as_parameter_to_package_nix = FormattedPythonPackageList(flake_deps.list, "as_parameter_to_package_nix")
            declaration = FormattedPythonPackageList(all_deps.list, "name")
            nixpkgs_overrides = FormattedPythonPackageList(nixpkgs_deps.list, "overrides")
        else:
            nixpkgs_deps = FormattedPythonPackageList([])
            flake_deps = FormattedPythonPackageList([])
            all_deps = FormattedPythonPackageList([])
            nixpkgs_declaration = FormattedPythonPackageList([])
            flakes_declaration = FormattedPythonPackageList([])
            nixpkgs_as_parameter_to_package_nix = FormattedPythonPackageList([])
            flakes_as_parameter_to_package_nix = FormattedPythonPackageList([])
            declaration = FormattedPythonPackageList([])
            nixpkgs_overrides = FormattedPythonPackageList([])

        return {
            BaseFlakeRecipe.Subtemplates.NIXPKGS_DEPS: nixpkgs_deps,
            BaseFlakeRecipe.Subtemplates.FLAKE_DEPS: flake_deps,
            BaseFlakeRecipe.Subtemplates.ALL_DEPS: all_deps,
            BaseFlakeRecipe.Subtemplates.NIXPKGS_DECLARATION: nixpkgs_declaration,
            BaseFlakeRecipe.Subtemplates.FLAKES_DECLARATION: flakes_declaration,
            BaseFlakeRecipe.Subtemplates.NIXPKGS_AS_PARAMETER_TO_PACKAGE_NIX: nixpkgs_as_parameter_to_package_nix,
            BaseFlakeRecipe.Subtemplates.FLAKES_AS_PARAMETER_TO_PACKAGE_NIX: flakes_as_parameter_to_package_nix,
            BaseFlakeRecipe.Subtemplates.DECLARATION: declaration,
            BaseFlakeRecipe.Subtemplates.NIXPKGS_OVERRIDES: nixpkgs_overrides
            }

    @property
    def flake(self) -> FormattedFlake:
        """
        Retrieves the flake.
        :return: A FormattedFlake.
        :rtype: FormattedFlake from pythonedanixflakes.recipe.formatted_flake
        """
        return FormattedFlake(self._flake)

    def repo_sha256(self) -> str:
        """
        Retrieves the SHA-256 hash of the git repository.
        :return: Such hash.
        :rtype: str
        """
        result = ""
        if self.usesGitrepoSha256():
            result = self._flake.python_package.git_repo.sha256()
        return result

    def pypi_sha256(self) -> str:
        """
        Retrieves the SHA-256 hash of the pypi package.
        :return: Such hash.
        :rtype: str
        """
        result = ""
        if self.usesPipSha256():
            result = self._flake.python_package.pip_sha256()
        return result

    def native_build_inputs_flakes_declaration(self) -> FormattedPythonPackageList:
        """
        Retrieves the declaration of the native build inputs packaged as flakes.
        :return: A list of formatted Python packages.
        :rtype: FormattedPythonPackageList from pythonedanixflakes.recipe.formatted_python_package_list
        """
        return self._native_build_inputs_subtemplates.get(BaseFlakeRecipe.Subtemplates.FLAKES_DECLARATION, [])

    def native_build_inputs_nixpkgs_declaration(self) -> FormattedPythonPackageList:
        """
        Retrieves the declaration of the native build inputs already in nixpkgs.
        :return: A list of formatted Python packages.
        :rtype: FormattedPythonPackageList from pythonedanixflakes.recipe.formatted_python_package_list
        """
        return self._native_build_inputs_subtemplates.get(BaseFlakeRecipe.Subtemplates.NIXPKGS_DECLARATION, [])

    def native_build_inputs_flake_deps(self) -> FormattedPythonPackageList:
        """
        Retrieves the native build inputs packaged as flakes.
        :return: A list of formatted Python packages.
        :rtype: FormattedPythonPackageList from pythonedanixflakes.recipe.formatted_python_package_list
        """
        return self._native_build_inputs_subtemplates.get(BaseFlakeRecipe.Subtemplates.FLAKE_DEPS, [])

    def native_build_inputs_nixpkgs_deps(self) -> FormattedPythonPackageList:
        """
        Retrieves the native build inputs already in nixpkgs.
        :return: A list of formatted Python packages.
        :rtype: FormattedPythonPackageList from pythonedanixflakes.recipe.formatted_python_package_list
        """
        return self._native_build_inputs_subtemplates.get(BaseFlakeRecipe.Subtemplates.NIXPKGS_DEPS, [])

    def native_build_inputs_flakes_as_parameter_to_package_nix(self) -> FormattedPythonPackageList:
        """
        Retrieves the subtemplate to pass flake-formatted native build dependencies as parameter to the package nix template.
        :return: A list of formatted Python packages.
        :rtype: FormattedPythonPackageList from pythonedanixflakes.recipe.formatted_python_package_list
        """
        return self._native_build_inputs_subtemplates.get(BaseFlakeRecipe.Subtemplates.FLAKES_AS_PARAMETER_TO_PACKAGE_NIX, [])

    def native_build_inputs_nixpkgs_as_parameter_to_package_nix(self) -> FormattedPythonPackageList:
        """
        Retrieves the subtemplate to pass the native build dependencies in nixpkgs as parameters to the package nix template.
        :return: A list of formatted Python packages.
        :rtype: FormattedPythonPackageList from pythonedanixflakes.recipe.formatted_python_package_list
        """
        return self._native_build_inputs_subtemplates.get(BaseFlakeRecipe.Subtemplates.NIXPKGS_AS_PARAMETER_TO_PACKAGE_NIX, [])

    def native_build_inputs_declaration(self) -> FormattedPythonPackageList:
        """
        Retrieves the declaration of the native build inputs.
        :return: A list of formatted Python packages.
        :rtype: FormattedPythonPackageList from pythonedanixflakes.recipe.formatted_python_package_list
        """
        return self._native_build_inputs_subtemplates.get(BaseFlakeRecipe.Subtemplates.DECLARATION, [])

    def native_build_inputs_nixpkgs_overrides(self) -> FormattedPythonPackageList:
        """
        Retrieves the subtemplate to override native build inputs already in nixpkgs.
        :return: A list of formatted Python packages.
        :rtype: FormattedPythonPackageList from pythonedanixflakes.recipe.formatted_python_package_list
        """
        return self._native_build_inputs_subtemplates.get(BaseFlakeRecipe.Subtemplates.NIXPKGS_OVERRIDES, [])

    def propagated_build_inputs_flakes_declaration(self) -> FormattedPythonPackageList:
        """
        Retrieves the declaration of the propagated build inputs packaged as flakes.
        :return: A list of formatted Python packages.
        :rtype: FormattedPythonPackageList from pythonedanixflakes.recipe.formatted_python_package_list
        """
        return self._propagated_build_inputs_subtemplates.get(BaseFlakeRecipe.Subtemplates.FLAKES_DECLARATION, [])

    def propagated_build_inputs_nixpkgs_declaration(self) -> FormattedPythonPackageList:
        """
        Retrieves the declaration of the propagated build inputs already in nixpkgs.
        :return: A list of formatted Python packages.
        :rtype: FormattedPythonPackageList from pythonedanixflakes.recipe.formatted_python_package_list
        """
        return self._propagated_build_inputs_subtemplates.get(BaseFlakeRecipe.Subtemplates.NIXPKGS_DECLARATION, [])

    def propagated_build_inputs_flake_deps(self) -> FormattedPythonPackageList:
        """
        Retrieves the propagated build inputs packaged as flakes.
        :return: A list of formatted Python packages.
        :rtype: FormattedPythonPackageList from pythonedanixflakes.recipe.formatted_python_package_list
        """
        return self._propagated_build_inputs_subtemplates.get(BaseFlakeRecipe.Subtemplates.FLAKE_DEPS, [])

    def propagated_build_inputs_nixpkgs_deps(self) -> FormattedPythonPackageList:
        """
        Retrieves the propagated build inputs already in nixpkgs.
        :return: A list of formatted Python packages.
        :rtype: FormattedPythonPackageList from pythonedanixflakes.recipe.formatted_python_package_list
        """
        return self._propagated_build_inputs_subtemplates.get(BaseFlakeRecipe.Subtemplates.NIXPKGS_DEPS, [])

    def propagated_build_inputs_flakes_as_parameter_to_package_nix(self) -> FormattedPythonPackageList:
        """
        Retrieves the subtemplate to pass flake-formatted propagated build dependencies as parameter to the package nix template.
        :return: A list of formatted Python packages.
        :rtype: FormattedPythonPackageList from pythonedanixflakes.recipe.formatted_python_package_list
        """
        return self._propagated_build_inputs_subtemplates.get(BaseFlakeRecipe.Subtemplates.FLAKES_AS_PARAMETER_TO_PACKAGE_NIX, [])

    def propagated_build_inputs_nixpkgs_as_parameter_to_package_nix(self) -> FormattedPythonPackageList:
        """
        Retrieves the subtemplate to pass the propagated build dependencies in nixpkgs as parameters to the package nix template.
        :return: A list of formatted Python packages.
        :rtype: FormattedPythonPackageList from pythonedanixflakes.recipe.formatted_python_package_list
        """
        return self._propagated_build_inputs_subtemplates.get(BaseFlakeRecipe.Subtemplates.NIXPKGS_AS_PARAMETER_TO_PACKAGE_NIX, [])

    def propagated_build_inputs_declaration(self) -> FormattedPythonPackageList:
        """
        Retrieves the declaration of the native build inputs.
        :return: A list of formatted Python packages.
        :rtype: FormattedPythonPackageList from pythonedanixflakes.recipe.formatted_python_package_list
        """
        return self._propagated_build_inputs_subtemplates.get(BaseFlakeRecipe.Subtemplates.DECLARATION, [])

    def propagated_build_inputs_nixpkgs_overrides(self) -> FormattedPythonPackageList:
        """
        Retrieves the subtemplate to override propagated build inputs already in nixpkgs.
        :return: A list of formatted Python packages.
        :rtype: FormattedPythonPackageList from pythonedanixflakes.recipe.formatted_python_package_list
        """
        return self._propagated_build_inputs_subtemplates.get(BaseFlakeRecipe.Subtemplates.NIXPKGS_OVERRIDES, [])

    def build_inputs_flakes_declaration(self) -> FormattedPythonPackageList:
        """
        Retrieves the declaration of the build inputs packaged as flakes.
        :return: A list of formatted Python packages.
        :rtype: FormattedPythonPackageList from pythonedanixflakes.recipe.formatted_python_package_list
        """
        return self._build_inputs_subtemplates.get(BaseFlakeRecipe.Subtemplates.FLAKES_DECLARATION, [])

    def build_inputs_nixpkgs_declaration(self) -> FormattedPythonPackageList:
        """
        Retrieves the declaration of the build inputs already in nixpkgs.
        :return: A list of formatted Python packages.
        :rtype: FormattedPythonPackageList from pythonedanixflakes.recipe.formatted_python_package_list
        """
        return self._build_inputs_subtemplates.get(BaseFlakeRecipe.Subtemplates.NIXPKGS_DECLARATION, [])

    def build_inputs_flake_deps(self) -> FormattedPythonPackageList:
        """
        Retrieves the build inputs packaged as flakes.
        :return: A list of formatted Python packages.
        :rtype: FormattedPythonPackageList from pythonedanixflakes.recipe.formatted_python_package_list
        """
        return self._build_inputs_subtemplates.get(BaseFlakeRecipe.Subtemplates.FLAKE_DEPS, [])

    def build_inputs_nixpkgs_deps(self) -> FormattedPythonPackageList:
        """
        Retrieves the build inputs already in nixpkgs.
        :return: A list of formatted Python packages.
        :rtype: FormattedPythonPackageList from pythonedanixflakes.recipe.formatted_python_package_list
        """
        return self._build_inputs_subtemplates.get(BaseFlakeRecipe.Subtemplates.NIXPKGS_DEPS, [])

    def build_inputs_flakes_as_parameter_to_package_nix(self) -> FormattedPythonPackageList:
        """
        Retrieves the subtemplate to pass flake-formatted build dependencies as parameter to the package nix template.
        :return: A list of formatted Python packages.
        :rtype: FormattedPythonPackageList from pythonedanixflakes.recipe.formatted_python_package_list
        """
        return self._build_inputs_subtemplates.get(BaseFlakeRecipe.Subtemplates.FLAKES_AS_PARAMETER_TO_PACKAGE_NIX, [])

    def build_inputs_nixpkgs_as_parameter_to_package_nix(self) -> FormattedPythonPackageList:
        """
        Retrieves the subtemplate to pass the build dependencies in nixpkgs as parameters to the package nix template.
        :return: A list of formatted Python packages.
        :rtype: FormattedPythonPackageList from pythonedanixflakes.recipe.formatted_python_package_list
        """
        return self._build_inputs_subtemplates.get(BaseFlakeRecipe.Subtemplates.NIXPKGS_AS_PARAMETER_TO_PACKAGE_NIX, [])

    def build_inputs_declaration(self) -> FormattedPythonPackageList:
        """
        Retrieves the declaration of the native build inputs.
        :return: A list of formatted Python packages.
        :rtype: FormattedPythonPackageList from pythonedanixflakes.recipe.formatted_python_package_list
        """
        return self._build_inputs_subtemplates.get(BaseFlakeRecipe.Subtemplates.DECLARATION, [])

    def build_inputs_nixpkgs_overrides(self) -> FormattedPythonPackageList:
        """
        Retrieves the subtemplate to override build inputs already in nixpkgs.
        :return: A list of formatted Python packages.
        :rtype: FormattedPythonPackageList from pythonedanixflakes.recipe.formatted_python_package_list
        """
        return self._build_inputs_subtemplates.get(BaseFlakeRecipe.Subtemplates.NIXPKGS_OVERRIDES, [])

    def check_inputs_flakes_declaration(self) -> FormattedPythonPackageList:
        """
        Retrieves the declaration of the check inputs packaged as flakes.
        :return: A list of formatted Python packages.
        :rtype: FormattedPythonPackageList from pythonedanixflakes.recipe.formatted_python_package_list
        """
        return self._check_inputs_subtemplates.get(BaseFlakeRecipe.Subtemplates.FLAKES_DECLARATION, [])

    def check_inputs_nixpkgs_declaration(self) -> FormattedPythonPackageList:
        """
        Retrieves the declaration of the check inputs already in nixpkgs.
        :return: A list of formatted Python packages.
        :rtype: FormattedPythonPackageList from pythonedanixflakes.recipe.formatted_python_package_list
        """
        return self._check_inputs_subtemplates.get(BaseFlakeRecipe.Subtemplates.NIXPKGS_DECLARATION, [])

    def check_inputs_flake_deps(self) -> FormattedPythonPackageList:
        """
        Retrieves the check inputs packaged as flakes.
        :return: A list of formatted Python packages.
        :rtype: FormattedPythonPackageList from pythonedanixflakes.recipe.formatted_python_package_list
        """
        return self._check_inputs_subtemplates.get(BaseFlakeRecipe.Subtemplates.FLAKE_DEPS, [])

    def check_inputs_nixpkgs_deps(self) -> FormattedPythonPackageList:
        """
        Retrieves the check inputs already in nixpkgs.
        :return: A list of formatted Python packages.
        :rtype: FormattedPythonPackageList from pythonedanixflakes.recipe.formatted_python_package_list
        """
        return self._check_inputs_subtemplates.get(BaseFlakeRecipe.Subtemplates.NIXPKGS_DEPS, [])

    def check_inputs_flakes_as_parameter_to_package_nix(self) -> FormattedPythonPackageList:
        """
        Retrieves the subtemplate to pass flake-formatted check dependencies as parameter to the package nix template.
        :return: A list of formatted Python packages.
        :rtype: FormattedPythonPackageList from pythonedanixflakes.recipe.formatted_python_package_list
        """
        return self._check_inputs_subtemplates.get(BaseFlakeRecipe.Subtemplates.FLAKES_AS_PARAMETER_TO_PACKAGE_NIX, [])

    def check_inputs_nixpkgs_as_parameter_to_package_nix(self) -> FormattedPythonPackageList:
        """
        Retrieves the subtemplate to pass the check dependencies in nixpkgs as parameters to the package nix template.
        :return: A list of formatted Python packages.
        :rtype: FormattedPythonPackageList from pythonedanixflakes.recipe.formatted_python_package_list
        """
        return self._check_inputs_subtemplates.get(BaseFlakeRecipe.Subtemplates.NIXPKGS_AS_PARAMETER_TO_PACKAGE_NIX, [])

    def check_inputs_declaration(self) -> FormattedPythonPackageList:
        """
        Retrieves the declaration of the native build inputs.
        :return: A list of formatted Python packages.
        :rtype: FormattedPythonPackageList from pythonedanixflakes.recipe.formatted_python_package_list
        """
        return self._check_inputs_subtemplates.get(BaseFlakeRecipe.Subtemplates.DECLARATION, [])

    def check_inputs_nixpkgs_overrides(self) -> FormattedPythonPackageList:
        """
        Retrieves the subtemplate to override check inputs already in nixpkgs.
        :return: A list of formatted Python packages.
        :rtype: FormattedPythonPackageList from pythonedanixflakes.recipe.formatted_python_package_list
        """
        return self._check_inputs_subtemplates.get(BaseFlakeRecipe.Subtemplates.NIXPKGS_OVERRIDES, [])

    def optional_build_inputs_flakes_declaration(self) -> FormattedPythonPackageList:
        """
        Retrieves the declaration of the optional build inputs packaged as flakes.
        :return: A list of formatted Python packages.
        :rtype: FormattedPythonPackageList from pythonedanixflakes.recipe.formatted_python_package_list
        """
        return self._optional_build_inputs_subtemplates.get(BaseFlakeRecipe.Subtemplates.FLAKES_DECLARATION, [])

    def optional_build_inputs_nixpkgs_declaration(self) -> FormattedPythonPackageList:
        """
        Retrieves the declaration of the optional build inputs already in nixpkgs.
        :return: A list of formatted Python packages.
        :rtype: FormattedPythonPackageList from pythonedanixflakes.recipe.formatted_python_package_list
        """
        return self._optional_build_inputs_subtemplates.get(BaseFlakeRecipe.Subtemplates.NIXPKGS_DECLARATION, [])

    def optional_build_inputs_flake_deps(self) -> FormattedPythonPackageList:
        """
        Retrieves the declaration of the optional build inputs.
        :return: A list of formatted Python packages.
        :rtype: FormattedPythonPackageList from pythonedanixflakes.recipe.formatted_python_package_list
        """
        return self._optional_build_inputs_subtemplates.get(BaseFlakeRecipe.Subtemplates.FLAKE_DEPS, [])

    def optional_build_inputs_nixpkgs_deps(self) -> FormattedPythonPackageList:
        """
        Retrieves the optional build inputs already in nixpkgs.
        :return: A list of formatted Python packages.
        :rtype: FormattedPythonPackageList from pythonedanixflakes.recipe.formatted_python_package_list
        """
        return self._optional_build_inputs_subtemplates.get(BaseFlakeRecipe.Subtemplates.NIXPKGS_DEPS, [])

    def optional_build_inputs_flakes_as_parameter_to_package_nix(self) -> FormattedPythonPackageList:
        """
        Retrieves the subtemplate to pass flake-formatted optional build dependencies as parameter to the package nix template.
        :return: A list of formatted Python packages.
        :rtype: FormattedPythonPackageList from pythonedanixflakes.recipe.formatted_python_package_list
        """
        return self._optional_build_inputs_subtemplates.get(BaseFlakeRecipe.Subtemplates.FLAKES_AS_PARAMETER_TO_PACKAGE_NIX, [])

    def optional_build_inputs_nixpkgs_as_parameter_to_package_nix(self) -> FormattedPythonPackageList:
        """
        Retrieves the subtemplate to pass the optional build dependencies in nixpkgs as parameters to the package nix template.
        :return: A list of formatted Python packages.
        :rtype: FormattedPythonPackageList from pythonedanixflakes.recipe.formatted_python_package_list
        """
        return self._optional_build_inputs_subtemplates.get(BaseFlakeRecipe.Subtemplates.NIXPKGS_AS_PARAMETER_TO_PACKAGE_NIX, [])

    def optional_build_inputs_declaration(self) -> FormattedPythonPackageList:
        """
        Retrieves the declaration of the optional build inputs.
        :return: A list of formatted Python packages.
        :rtype: FormattedPythonPackageList from pythonedanixflakes.recipe.formatted_python_package_list
        """
        return self._optional_build_inputs_subtemplates.get(BaseFlakeRecipe.Subtemplates.DECLARATION, [])

    def optional_build_inputs_nixpkgs_overrides(self) -> FormattedPythonPackageList:
        """
        Retrieves the subtemplate to override optional build inputs already in nixpkgs.
        :return: A list of formatted Python packages.
        :rtype: FormattedPythonPackageList from pythonedanixflakes.recipe.formatted_python_package_list
        """
        return self._optional_build_inputs_subtemplates.get(BaseFlakeRecipe.Subtemplates.NIXPKGS_OVERRIDES, [])

    def flakes_as_parameter_to_package_nix(self) -> FormattedPythonPackageList:
        """
        Retrieves the subtemplate to pass flake-formatted dependencies as parameter to the package nix template.
        :return: A list of formatted Python packages.
        :rtype: FormattedPythonPackageList from pythonedanixflakes.recipe.formatted_python_package_list
        """
        return FormattedPythonPackageList(self.remove_duplicates(
            self.native_build_inputs_flakes_as_parameter_to_package_nix().list,
                self.propagated_build_inputs_flakes_as_parameter_to_package_nix().list,
                self.build_inputs_flakes_as_parameter_to_package_nix().list,
                self.check_inputs_flakes_as_parameter_to_package_nix().list,
                self.optional_build_inputs_flakes_as_parameter_to_package_nix().list), "as_parameter_to_package_nix")

    def nixpkgs_as_parameter_to_package_nix(self) -> FormattedPythonPackageList:
        """
        Retrieves the subtemplate to pass the dependency in nixpkgs as parameter to the package nix template.
        :return: A list of formatted Python packages.
        :rtype: FormattedPythonPackageList from pythonedanixflakes.recipe.formatted_python_package_list
        """
        return FormattedPythonPackageList(self.remove_duplicates(
            self.native_build_inputs_nixpkgs_as_parameter_to_package_nix().list,
            self.propagated_build_inputs_nixpkgs_as_parameter_to_package_nix().list,
            self.build_inputs_nixpkgs_as_parameter_to_package_nix().list,
            self.check_inputs_nixpkgs_as_parameter_to_package_nix().list,
            self.optional_build_inputs_nixpkgs_as_parameter_to_package_nix().list), "as_parameter_to_package_nix")

    def flakes_declaration(self) -> FormattedPythonPackageList:
        """
        Retrieves the declaration of all flakes-packaged dependencies.
        :return: A list of formatted Python packages.
        :rtype: FormattedPythonPackageList from pythonedanixflakes.recipe.formatted_python_package_list
        """
        return FormattedPythonPackageList(self.remove_duplicates(
            self.native_build_inputs_flakes_declaration().list,
            self.propagated_build_inputs_flakes_declaration().list,
            self.build_inputs_flakes_declaration().list,
            self.check_inputs_flakes_declaration().list,
            self.optional_build_inputs_flakes_declaration().list), "flake_declaration")

    def declaration(self) -> FormattedPythonPackageList:
        """
        Retrieves the declaration of all dependencies.
        :return: A list of formatted Python packages.
        :rtype: FormattedPythonPackageList from pythonedanixflakes.recipe.formatted_python_package_list
        """
        return FormattedPythonPackageList(self.remove_duplicates(
            self.native_build_inputs_declaration().list,
            self.propagated_build_inputs_declaration().list,
            self.build_inputs_declaration().list,
            self.check_inputs_declaration().list,
            self.optional_build_inputs_declaration().list), "name")
