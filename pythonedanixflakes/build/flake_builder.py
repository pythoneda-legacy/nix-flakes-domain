"""
pythonedanixflakes/build/flake_builder.py

This file defines the FlakeBuilder class.

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
from pythoneda.event import Event
from pythoneda.event_listener import EventListener
from pythonedaeventgit.git_add_failed import GitAddFailed
from pythonedaeventgit.git_init_failed import GitInitFailed
from pythonedaeventnixflakes.build.build_flake_requested import BuildFlakeRequested
from pythonedaeventnixflakes.build.flake_built import FlakeBuilt
from pythonedaeventnixflakes.flake_created import FlakeCreated
from pythonedaeventnixflakes.recipe.flake_recipe import FlakeRecipe
from pythonedaeventnix.nix_build_failed import NixBuildFailed
from pythonedasharednix.sha256_mismatch_error import Sha256MismatchError

import logging
import os
import re
import shutil
import subprocess
import tempfile
from typing import List, Type

class FlakeBuilder(EventListener):
    """
    Class capable of building flakes.

    Class name: FlakeBuilder

    Responsibilities:
        - Building Flakes.

    Collaborators:
        - Flakes: The entities to build.
    """
    _forensic_folder = None

    @classmethod
    def forensic_folder(cls, folder: str):
        """
        Specifies the forensic folder.
        :param folder: The folder.
        :type folder: str
        """
        cls._forensic_folder = folder

    @classmethod
    def supported_events(cls) -> List[Type[Event]]:
        """
        Retrieves the list of supported event classes.
        :return: The list of event classes.
        :rtype: List[Type[Event]]
        """
        return [ BuildFlakeRequested ]

    @classmethod
    def listenBuildFlakeRequested(cls, event: BuildFlakeRequested) -> FlakeBuilt:
        """
        Receives BuildFlakeRequested events.
        :param event: The event.
        :type event: BuildFlakeRequested from pythonedaeventnixflakes.build.build_flake_requested
        """
        return cls.build_flake(event, os.path.join(event.flakes_folder, f'{event.package_name}-{event.package_version}'))

    @classmethod
    def build_flake(cls, event: BuildFlakeRequested, flakeFolder: str) -> FlakeBuilt:
        """
        Builds a flake.
        :param event: The event with the flake information.
        :type event: BuildFlakeRequested from pythonedaeventnixflakes.build.build_flake_requested
        :param flakeFolder: The flake folder.
        :type flakeFolder: str
        :return: A FlakeBuilt event.
        :rtype: FlakeBuilt from pythonedaeventnixflakes.build.flake_built
        """
        result = None

        with tempfile.TemporaryDirectory() as temp_dir:
            cls.copy_folder_contents(flakeFolder, temp_dir)
            cls.git_init(temp_dir)
            for file in os.listdir(temp_dir):
                cls.git_add(temp_dir, file)
            try:
                logging.getLogger(__name__).debug(f'Building the flake in {temp_dir}')
                cls.nix_build(temp_dir, firstAttempt=True)
            except Sha256MismatchError as mismatch:
                cls.replace_sha256_in_files(temp_dir, mismatch.sha256)
                cls.nix_build(temp_dir, firstAttempt=False)
                if os.path.exists(os.path.join(temp_dir, '.git')):
                    shutil.rmtree(os.path.join(temp_dir, '.git'))
                cls.copy_folder_contents(temp_dir, flakeFolder)

        return FlakeBuilt(event.package_name, event.package_version, flakeFolder)

    @classmethod
    def copy_folder_contents(cls, source: str, destination: str):
        """
        Copies the contents of a folder into a destination folder.
        :param source: The source folder.
        :type source: str
        :param destination: The destination folder.
        :type destination: str
        """
        logging.getLogger(__name__).debug(f'Copying {source} contents to {destination}')
        if os.path.exists(destination):
            shutil.rmtree(destination)
        shutil.copytree(source, destination)

    @classmethod
    def git_init(cls, folder: str):
        """
        Performs a "git init" on given folder.
        :param folder: The folder.
        :type folder: str
        """
        output = None
        try:
            logging.getLogger(__name__).debug(f'Initializing a git repository in {folder}')
            output = subprocess.check_output(['git', 'init'], stderr=subprocess.STDOUT, cwd=folder)
        except subprocess.CalledProcessError:
            raise GitInitFailed(folder, output.stdout)

    @classmethod
    def git_add(cls, folder: str, file: str):
        """
        Performs a "git add [file]" on given folder.
        :param folder: The folder.
        :type folder: str
        :param file: The file to add.
        :type file: str
        """
        logging.getLogger(__name__).debug(f'Adding {file} to the git repository in {folder}')
        output = None
        try:
            output = subprocess.check_output(['git', 'add', file], stderr=subprocess.STDOUT, cwd=folder)
        except subprocess.CalledProcessError:
            raise GitAddFailed(file, output.stdout)

    @classmethod
    def nix_build(cls, folder: str, firstAttempt = True):
        """
        Performs a "nix build" on given folder.
        :param folder: The folder.
        :type folder: str
        :param firstAttempt: Whether it's the first attempt or not.
        :type firstAttempt: bool
        """
        try:
            subprocess.run(['nix', 'build', '.'], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, cwd=folder)
        except subprocess.CalledProcessError as err:
            sha256 = cls.extract_sha256_from_output(err.stderr)
            if sha256:
                raise Sha256MismatchError(sha256)
            else:
                logging.getLogger(__name__).error(err.stdout)
                logging.getLogger(__name__).error(err.stderr)
                cls.copy_folder_contents(folder, cls._forensic_folder)
                raise NixBuildFailed(cls._forensic_folder, err.stdout)

    @classmethod
    def extract_sha256_from_output(cls, output: str) -> str:
        """
        Extracts the SHA-256 hash from given output.
        :param output: The output to parse.
        :type output: str
        :return: The SHA-256 hash.
        :rtype: str
        """
        result = None
        match = re.search(r'got:\s+(sha256-\S+)', output)
        if match:
            result = match.group(1)
        return result

    @classmethod
    def replace_sha256_in_files(cls, directory: str, newSha256: str):
        """
        Replaces the SHA-256 hash in all files on given folder.
        :param directory: The folder.
        :type directory: str
        :param newSha256: The new hash.
        :type newSha256: str
        """
        # Define a pattern for a line containing 'sha256 = "[whatever]"'
        pattern = re.compile(r'(sha256\s*=\s*)"([^"]*)"')

        # Walk through the directory, including all subdirectories
        for root, _, files in os.walk(directory):
            for file in files:
                # Only process .nix files
                if file.endswith('.nix'):
                    file_path = os.path.join(root, file)
                    with open(file_path, 'r+') as f:
                        content = f.read()
                        # Replace all occurrences of the pattern with 'sha256 = "[newSha256]"'
                        new_content = pattern.sub(fr'\1"{newSha256}"', content)
                        if new_content != content:
                            # If any replacements were made, overwrite the file with the new content
                            f.seek(0)
                            f.write(new_content)
                            f.truncate()
