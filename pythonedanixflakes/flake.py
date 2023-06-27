"""
pythonedanixflakes/flake.py

This file defines the Flake class.

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
from pythoneda.event import Event
from pythoneda.event_emitter import EventEmitter
from pythoneda.event_listener import EventListener
from pythoneda.ports import Ports
from pythoneda.value_object import attribute, primary_key_attribute
from pythonedasharedgit.git_repo import GitRepo
from pythonedasharedgit.git_repo_repo import GitRepoRepo
from pythonedanixflakes.build.build_flake_requested import BuildFlakeRequested
from pythonedaeventnixflakes.flake_available import FlakeAvailable
from pythonedanixflakes.flake_in_progress import FlakeInProgress
from pythonedaeventnixflakes.flake_requested import FlakeRequested
from pythonedasharednix.nix_template import NixTemplate
from pythonedasharednix.python.nix_python_package_in_nixpkgs import NixPythonPackageInNixpkgs
from pythonedasharednix.python.nix_python_package_repo import NixPythonPackageRepo
from pythonedapythonpackages.python_package import PythonPackage
from pythonedaeventpythonpackages.python_package_created import PythonPackageCreated
from pythonedaeventpythonpackages.python_package_requested import PythonPackageRequested
from pythonedaeventpythonpackages.python_package_resolved import PythonPackageResolved

from typing import Dict, List, Type
import logging

class Flake(Entity, EventListener, EventEmitter):

    """
    Represents a nix flake.

    Class name: Flake

    Responsibilities:
        - Represent a Nix flake.
        - React upon receiving FlakeRequested events.

    Collaborators:
        - FlakeRequested: The event when a flake is requested.
    """
    def __init__(self, name: str, version: str, pythonPackage: PythonPackage, nativeBuildInputs: List, propagatedBuildInputs: List, buildInputs: List, checkInputs: List, optionalBuildInputs: List):
        """
        Creates a new flake instance.
        :param name: The flake name.
        :type name: str
        :param version: The flake version.
        :type version: str
        :param pythonPackage: The Python package.
        :type pythonPackage: PythonPackage from pythonedasharedpython.python_package
        :param nativeBuildInputs: The list of native build inputs.
        :type nativeBuildInputs: List
        :param propagatedBuildInputs: The list of propagated build inputs.
        :type propagatedBuildInputs: List
        :param buildInputs: The list of build inputs.
        :type buildInputs: List
        :param checkInputs: The list of check inputs.
        :type checkInputs: List
        :param optionalBuildInputs: The list of optional build inputs.
        :type optionalBuildInputs: List
        """
        super().__init__()
        self._name = name
        self._version = version
        self._python_package = pythonPackage
        self._native_build_inputs = nativeBuildInputs
        self._propagated_build_inputs = propagatedBuildInputs
        self._build_inputs = buildInputs
        self._check_inputs = checkInputs
        self._optional_build_inputs = optionalBuildInputs

    @property
    @primary_key_attribute
    def name(self) -> str:
        """
        Retrieves the name of the flake.
        :return: The flake name.
        :rtype: str
        """
        return self._name

    @property
    @primary_key_attribute
    def version(self) -> str:
        """
        Retrieves the version of the flake.
        :return: The flake version.
        :rtype: str
        """
        return self._version

    @property
    @attribute
    def python_package(self) -> PythonPackage:
        """
        Retrieves the Python package.
        :return: The package.
        :rtype: PythonPackage from pythonedasharedpython.python_package
        """
        return self._python_package

    @property
    @attribute
    def native_build_inputs(self) -> List:
        """
        Retrieves the native build inputs.
        :return: Such list.
        :rtype: List
        """
        return self._native_build_inputs

    @property
    @attribute
    def propagated_build_inputs(self) -> List:
        """
        Retrieves the propagated build inputs.
        :return: Such list.
        :rtype: List
        """
        return self._propagated_build_inputs

    @property
    @attribute
    def build_inputs(self) -> List:
        """
        Retrieves the build inputs.
        :return: Such list.
        :rtype: List
        """
        return self._build_inputs

    @property
    @attribute
    def check_inputs(self) -> List:
        """
        Retrieves the check inputs.
        :return: Such list.
        :rtype: List
        """
        return self._check_inputs

    @property
    @attribute
    def optional_build_inputs(self) -> List:
        """
        Retrieves the optional build inputs.
        :return: Such list.
        :rtype: List
        """
        return self._optional_build_inputs

    @classmethod
    def supported_events(cls) -> List[Type[Event]]:
        """
        Retrieves the list of supported event classes.
        :return: Such list
        :rtype: List
        """
        return [ FlakeRequested, PythonPackageResolved ]

    @classmethod
    async def listenFlakeRequested(cls, event: FlakeRequested): # -> FlakeCreated:
        """
        Receives a FlakeRequested event.
        :param event: Such event.
        :type event: FlakeRequested from pythonedaeventnixflakes.flake_requested
        """
        result = None
        logger = logging.getLogger(__name__)
        logger.info(f'Received "flake requested for {event.package_name}-{event.package_version}"')

        # 1, check if there's already a flake.
        logging.getLogger('step-by-step').info(f'Checking if there is a flake for {event.package_name}-{event.package_version}')
        flakeRepo = Ports.instance().resolveFlakeRepo()
        existingFlake = flakeRepo.find_by_name_and_version(event.package_name, event.package_version)
        if existingFlake:
            # 1a: emit FlakeAvailable
            logger.info(f'Flake for {event.package_name}-{event.package_version} already exists')
            self.__class__.emit(FlakeAvailable(event.package_name, event.package_version))
        else:
            # annotate the flake as in-progress
            FlakeInProgress(event.package_name, event.package_version, event.flakes_folder)
            logging.getLogger('step-by-step').info(f'Retrieving the Python package for {event.package_name}-{event.package_version}')
            # 1b.1: check if the python package is already in nixpkgs.
            nixPythonPackageRepo = Ports.instance().resolve(NixPythonPackageRepo)
            nixPythonPackage = await nixPythonPackageRepo.find_by_name_and_version(event.package_name, event.package_version)
            if nixPythonPackage:
                if pythonPackage:
                    # 1b.1a: emit NixPythonPackageInNixpkgs
                    logger.info(f'Python package {pythonPackage.nixpkgs_package_name()} compatible with version {event.package_version} already exists in nixpkgs.')
                    await self.__class__.emit(NixPythonPackageInNixpkgs(pythonPackage))
                else:
                    # 1b.1b.1: annotate the flake as "in progress"
                    FlakeInProgress(event.package_name, event.package_version)
                    # 1b.1b.2: emit PythonPackageRequested
                    self.__class__.emit(PythonPackageRequested(event.package_name, event.package_version))

    @classmethod
    async def listenPythonPackageResolved(cls, event: PythonPackageResolved):
        """
        Receives a PythonPackageResolved event.
        :param event: Such event.
        :type event: PythonPackageResolved from pythonedaeventpythonpackages.python_package_resolved
        """
        flakeInProgress = FlakeInProgress.matching(name=event.package_name, version=event.package_version)
        flakeInProgress.set_python_package(event.python_package)
        self.__class__.emit(BuildFlakeRequested(event.package_name, event.package_version, flakeInProgress.flakes_folder, event.python_package))

    @classmethod
    async def oldListenFlakeRequested(cls, event: FlakeRequested): # -> FlakeCreated:
        """
        Old version of the method to process an incoming FlakeRequested event.
        :param event: Such event.
        :type event: FlakeRequested from pythonedaeventnixflakes.flake_requested
        """
        result = None
        logger = logging.getLogger(__name__)
        logger.info(f'Received "flake requested for {event.package_name}-{event.package_version}"')
        flakeRepo = Ports.instance().resolveFlakeRepo()

        logging.getLogger('step-by-step').info(f'Checking if there is a flake for {event.package_name}-{event.package_version}')
        existingFlake = flakeRepo.find_by_name_and_version(event.package_name, event.package_version)
        if existingFlake:
            logger.info(f'Flake for {event.package_name}-{event.package_version} already exists')
        else:
            logging.getLogger('step-by-step').info(f'Retrieving the Python package for {event.package_name}-{event.package_version}')
            pythonPackageRepo = Ports.instance().resolve(PythonPackageRepo)
            pythonPackage = await pythonPackageRepo.find_by_name_and_version(event.package_name, event.package_version)

            if pythonPackage:
                if pythonPackage.in_nixpkgs():
                    logger.info(f'Python package {pythonPackage.nixpkgs_package_name()} compatible with version {event.package_version} already exists in nixpkgs.')
                else:
                    nixPythonPackageRepo = Ports.instance().resolve(NixPythonPackageRepo)
                    logging.getLogger('step-by-step').info(f'Retrieving the dependencies of {event.package_name}-{event.package_version}')
                    nativeBuildInputs = pythonPackage.get_native_build_inputs()
                    propagatedBuildInputs = pythonPackage.get_propagated_build_inputs()
                    buildInputs = pythonPackage.get_build_inputs()
                    checkInputs = pythonPackage.get_check_inputs()
                    optionalBuildInputs = pythonPackage.get_optional_build_inputs()
                    dependenciesInNixpkgs = []
                    for dep in list(set(nativeBuildInputs) | set(propagatedBuildInputs) | set(buildInputs) | set(checkInputs) | set(optionalBuildInputs)):
                        logging.getLogger('step-by-step').info(f'Processing dependency {dep.name}-{dep.version} of {event.package_name}-{event.package_version}')
                        # check if it's in nixpkgs already
                        if dep.in_nixpkgs():
                            logging.getLogger('step-by-step').info(f'Dependency {dep.name}-{dep.version} of {event.package_name}-{event.package_version} already in nixpkgs')
                            dependenciesInNixpkgs.append(dep)
                        else:
                            depName = dep.name
                            depVersion = dep.version
                            nixPythonPackages = nixPythonPackageRepo.find_by_name(dep.name)
                            nixPythonPackage = next((pkg for pkg in nixPythonPackages if dep.satisfies_spec(pkg.version)), None)
                            if nixPythonPackage:
                                pkg = pythonPackageRepo.find_by_name_and_version(nixPythonPackage.name, nixPythonPackage.version)
                                logging.getLogger('step-by-step').info(f'Found a compatible Python package in Nix for {dep.name}-{dep.version}: {pkg.name}-{pkg.version}')
                                dependenciesInNixpkgs.append(pkg)
                            else:
                                # check if there's a flake for the dependency
                                depFlake = flakeRepo.find_by_name_and_version(depName, depVersion)
                                if depFlake:
                                    logger.debug(f'Flake found for {depName}-{depVersion}')
                                else:
                                    flakeCreated = cls.emit(FlakeRequested(depName, depVersion))
                                    logger.info(f'Flake {dep.name}-{dep.version} created (triggered by "flake {event.package_name}-{event.package_version} requested")')

                    flake = Flake(
                        event.package_name,
                        event.package_version,
                        pythonPackage,
                        cls.cleanup_nixpkgs_dependencies(nativeBuildInputs, dependenciesInNixpkgs),
                        cls.cleanup_nixpkgs_dependencies(propagatedBuildInputs, dependenciesInNixpkgs),
                        cls.cleanup_nixpkgs_dependencies(buildInputs, dependenciesInNixpkgs),
                        cls.cleanup_nixpkgs_dependencies(checkInputs, dependenciesInNixpkgs),
                        cls.cleanup_nixpkgs_dependencies(optionalBuildInputs, dependenciesInNixpkgs))
                    logging.getLogger('step-by-step').info(f'Retrieving recipe for flake {flake.name}-{flake.version}')
                    flakeRecipe = cls.find_recipe_by_flake(flake)
                    if flakeRecipe:
                        logging.getLogger('step-by-step').info(f'Recipe processing')
                        result = flakeRecipe.process()
                    else:
                        logger.critical(f'No recipe available for {event.package_name}-{event.package_version}')

                    if result:
                        logger.info(f'Flake {event.package_name}-{event.package_version} created')
                    else:
                        logger.info(f'Flake {event.package_name}-{event.package_version} could not be created')
            else:
                logger.info(f'Unknown Python package {event.package_name}-{event.package_version}')

        return result

    @classmethod
    async def listenPythonPackageCreated(cls, event: PythonPackageCreated): # -> FlakeCreated:
        """
        Receives a PythonPackageCreated event.
        :param event: Such event.
        :type event: PythonPackageCreated from pythonedaeventpythonpackages.python_package_created
        """
        logger = logging.getLogger(__name__)
        logger.debug(f'Received PythonPackageCreated')

    @classmethod
    def find_recipe_by_flake(cls, flake):
        """
        Retrieves the best recipe for given Flake.
        :param flake: The flake.
        :type flake: Flake from pythonedanixflakes.flake
        """
        result = None
        flakeRecipeClasses = Ports.instance().resolveFlakeRecipeRepo().find_recipe_classes_by_flake(flake)
        similarities = {}
        for recipeClass in flakeRecipeClasses:
            similarities[recipeClass] = recipeClass.similarity(flake)
        matches = sorted([aux for aux in similarities.keys() if similarities[aux] != 0.0], key=lambda recipeClass: similarities[recipeClass], reverse=True)
        if matches and len(matches) > 0:
            result = matches[0](flake)
        return result

    @classmethod
    def cleanup_nixpkgs_dependencies(cls, inputs: List[PythonPackage], inNixpkgs: List[PythonPackage]) -> List[PythonPackage]:
        """
        Cleans up nixpkgs dependencies.
        :param inputs: The inputs.
        :type inputs: List
        :param inNixpkgs: The dependencies in nixpkgs.
        :type inNixpkgs: List
        :return: A cleaned-up list.
        :rtype: List
        """
        curatedInputs = list([input for input in inputs if not any((input.name == nixpkg.name) for nixpkg in inNixpkgs)])
        curatedNixpkgs = list([nixpkg for nixpkg in inNixpkgs if any((input.name == nixpkg.name) for input in inputs)])
        return curatedInputs + curatedNixpkgs

    def dependency_in_nixpkgs(self, dep) -> bool:
        """
        Checks if given dependency is in nixpkgs.
        :param dep: The dependency to check.
        :type dep: object
        :return: True in such case.
        :rtype: bool
        """
        return dep.in_nixpkgs() or dep in self.dependencies_in_nixpkgs

    def __str__(self):
        """
        Provides a string representation of the flake.
        :return: Such representation.
        :rtype: str
        """
        return super(Entity, self).__str__()

    def __eq__(self, other) -> bool:
        """
        Check if this flake is equivalent to given object.
        :param other: The other object.
        :type other: object
        :return: True in such case.
        :rtype: bool
        """
        return super(Entity, self).__eq__(other)

    def __hash__(self):
        """
        Retrieves the hash of this flake.
        :return: Such value.
        :rtype: int
        """
        return super(Entity, self).__hash__()
