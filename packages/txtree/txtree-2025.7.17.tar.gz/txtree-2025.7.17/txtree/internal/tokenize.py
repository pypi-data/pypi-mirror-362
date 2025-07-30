"""
TXTree: A Visual Tool for PubMed Literature Exploration by Text Mining
Copyright (C) 2025 Diogo de Jesus Soares Machado, Roberto Tadeu Raittz

This file is part of TXTree.

TXTree is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as
published by the Free Software Foundation, either version 3 of the
License, or (at your option) any later version.

TXTree is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with TXTree. If not, see <https://www.gnu.org/licenses/>.
"""

import re

def tokenize(text_list):
    """
    Tokenizes a list of text strings into words.

    This function splits each string in the input list into individual words
    based on word boundaries using regular expressions.

    Parameters:
        - text_list (list of str): A list of text strings to be tokenized.

    Returns:
        - list of list of str: A list where each element is a list of words
          corresponding to a string in the input text list.
    """
    # Split phrases into words
    return [re.findall(r'\b\w+\b', text) for text in text_list]