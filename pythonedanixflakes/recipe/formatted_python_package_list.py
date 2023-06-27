"""
pythonedanixflakes/recipe/formatted_python_package_list.py

This file defines the FormattedPythonPackageList class.

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
from pythonedanixflakes.recipe.formatted_python_package import FormattedPythonPackage

from typing import Callable, List

class FormattedPythonPackageList(Formatting):
    """
    Augments a list of PythonPackages to include formatting logic required by recipe templates.

    Class name: FormattedPythonPackageList

    Responsibilities:
        - Augment a list of PythonPackages to include formatting logic required by recipe templates.

    Collaborators:
        - FormattedPythonPackage
    """

    def __init__(self, lst: List[FormattedPythonPackage], f: str = "__str__", indent: str = "", separator: str = "", initialPrefix: str = "", finalSuffix: str = ""):
        """
        Creates a new instance.
        :param lst: The list of Python packages.
        :type lst: List[FormattedPythonPackage from pythonedanixflakes.recipe.formatted_python_package]
        :param f: The function name.
        :type f: str
        :param indent: The indentation text.
        :type indent: str
        :param separator: The separator.
        :type separator: str
        :param initialPrefix: The initial prefix.
        :type initialPrefix: str
        :param finalSuffix: The final suffix.
        :type finalSuffix: str
        """
        super().__init__(lst)
        self._func_name = f
        self._indent = indent
        self._separator = separator
        self._initial_prefix = initialPrefix
        self._final_suffix = finalSuffix

    @property
    def list(self) -> List[FormattedPythonPackage]:
        """
        Retrieves the list of Python packages.
        :return: Such list.
        :rtype: List[FormattedPythonPackage from pythonedanixflakes.recipe.formatted_python_package]
        """
        return self._fmt

    @property
    def func_name(self) -> str:
        """
        Retrieves the function name.
        :return: Such name.
        :rtype: str
        """
        return self._func_name

    @property
    def indent(self) -> str:
        """
        Retrieves the indentation text.
        :return: Such text.
        :rtype: str
        """
        return self._indent

    @property
    def separator(self) -> str:
        """
        Retrieves the separator.
        :return: Such text.
        :rtype: str
        """
        return self._separator

    @property
    def initial_prefix(self) -> str:
        """
        Retrieves the initial prefix.
        :return: Such prefix.
        :rtype: str
        """
        return self._initial_prefix

    @property
    def final_suffix(self) -> str:
        """
        Retrieves the final suffix.
        :return: Such text.
        :rtype: str
        """
        return self._final_suffix

    def with_function(self, value: str) :#-> FormattedPythonPackageList:
        """
        Builds another list with a different function name.
        :param value: The function name.
        :type value: str
        :return: The new list.
        :rtype: FormattedPythonPackageList from pythonedanixflakes.recipe.formatted_python_package_list
        """
        return FormattedPythonPackageList(self.list, value, self._indent, self._separator, self._initial_prefix, self._final_suffix)

    def with_indentation(self, value: str) :#-> FormattedPythonPackageList:
        """
        Builds another list with a different indentation.
        :param value: The indentation.
        :type value: str
        :return: The new list.
        :rtype: FormattedPythonPackageList from pythonedanixflakes.recipe.formatted_python_package_list
        """
        return FormattedPythonPackageList(self.list, self._func_name, value, self._separator, self._initial_prefix, self._final_suffix)

    def with_separator(self, value: str) :#-> FormattedPythonPackageList:
        """
        Builds another list with a different separator.
        :param value: The separator.
        :type value: str
        :return: The new list.
        :rtype: FormattedPythonPackageList from pythonedanixflakes.recipe.formatted_python_package_list
        """
        return FormattedPythonPackageList(self.list, self._func_name, self._indent, value, self._initial_prefix, self._final_suffix)

    def with_initial_prefix(self, value: str) :#-> FormattedPythonPackageList:
        """
        Builds another list with a different initial prefix.
        :param value: The prefix.
        :type value: str
        :return: The new list.
        :rtype: FormattedPythonPackageList from pythonedanixflakes.recipe.formatted_python_package_list
        """
        return FormattedPythonPackageList(self.list, self._func_name, self._indent, self._separator, value, self._final_suffix)

    def with_final_suffix(self, value: str) :#-> FormattedPythonPackageList:
        """
        Builds another list with a different final suffix.
        :param value: The suffix.
        :type value: str
        :return: The new list.
        :rtype: FormattedPythonPackageList from pythonedanixflakes.recipe.formatted_python_package_list
        """
        return FormattedPythonPackageList(self.list, self._func_name, self._indent, self._separator, self._initial_prefix, value)

    def _invoke_func(self, dep: FormattedPythonPackage) -> str:
        """
        Invokes the function.
        :param dep: The Python package.
        :type dep: FormattedPythonPackage from pythonedanixflakes.recipe.formatted_python_package
        :return: The function output.
        :rtype: str
        """
        result = ""

        func = getattr(dep, self.func_name)

        if callable(func):
            result = func()
        else:
            result = func

        return result

    def __str__(self) -> str:
        """
        Provides a string representation of the list.
        :return: Such text.
        :rtype: str
        """
        result = ""
        if len(self.list) > 0:
            result = f'{self.initial_prefix}{self.separator.join([f"{self.indent}{self._invoke_func(dep)}" for dep in self.list])}{self.final_suffix}'

        return result

    def __getattr__(self, attr):
        """
        Delegates any method call to the wrapped instance.
        :param attr: The attribute.
        :type attr: Any
        :return: The attribute value.
        :rtype: Any
        """
        return getattr(self.list, attr)
