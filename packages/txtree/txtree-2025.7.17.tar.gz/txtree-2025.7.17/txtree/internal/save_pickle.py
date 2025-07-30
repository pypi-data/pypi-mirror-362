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

import pickle

def save_pickle(data, file_path):
    """
    Saves data to a pickle file.

    This function serializes the input data and writes it to a file in pickle
    format, allowing the data to be saved and later deserialized.

    Parameters:
        - data (object): The data to be serialized and saved to the file.
        - file_path (str): The path to the file where the data will be saved.

    Returns:
        - None: The function does not return any value; it only saves the data
          to the file.
    """
    with open(file_path, 'wb') as handle:
        pickle.dump(data, handle, protocol=pickle.HIGHEST_PROTOCOL)