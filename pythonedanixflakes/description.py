"""
pythonedanixflakes/description.py

This file defines the Description class.

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
from bs4 import BeautifulSoup
import mistune

class Description():
    """
    Class name: Description

    Responsibilities:
        - Provide descriptions for Nix flakes

    Collaborators:
        - None
    """
    def extract_html_description(description: str) -> str:
        """
        Extracts the description from given HTML-formatted text.
        :param description: The text.
        :type description: str
        :return: The description.
        :rtype: str
        """
        if description:
            soup = BeautifulSoup(description, "html.parser")
            first_paragraph = soup.find("p")
            if first_paragraph is not None:
                plain_text_description = first_paragraph.get_text()
            else:
                plain_text_description = ""
        else:
            plain_text_description = ""

            return plain_text_description.strip(" \n\t")

    def extract_markdown_description(description: str) -> str:
        """
        Extracts the description from given markdown-formatted text.
        :param description: The text.
        :type description: str
        :return: The description.
        :rtype: str
        """
        if description:
            renderer = mistune.HTMLRenderer()
            parser = mistune.BlockParser(renderer)
            raw_description = extract_html_description(parser.parse(description))
        else:
            raw_description = ""

        return raw_description

    def extract_description(description: str, type: str) -> str:
        """
        Extracts the description from given formatted text.
        :param description: The text.
        :type description: str
        :param type: The format type.
        :type type: str
        :return: The description.
        :rtype: str
        """
        if (str == 'text/html'):
            return extract_html_description(str)
        elif (str == 'text/markdown'):
            return extract_markdown_description(str)

        return description
