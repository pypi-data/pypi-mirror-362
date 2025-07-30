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

import h5py
import numpy as np

def save_h5(data, file_path, dataset_name="data"):
    """
    Saves data to an HDF5 (.h5) file.

    This function stores the input data in an HDF5 file, allowing efficient
    storage and retrieval of numerical arrays.

    Parameters:
        - data (array-like or dict): The data to be saved. If it's a
          dictionary, each key-value pair is stored as a separate dataset.
        - file_path (str): The path to the .h5 file where the data will be
          saved.
        - dataset_name (str, optional): The name of the dataset when saving a
          single array. Ignored if data is a dictionary. Default is "data".

    Returns:
        - None: The function does not return any value; it only saves the data
          to the file.
    """
    with h5py.File(file_path, "w") as h5f:
        if isinstance(data, dict):
            for key, value in data.items():
                # Convert strings to bytes if necessary
                if (isinstance(value, (list, np.ndarray))
                    and len(value) > 0 and isinstance(value[0], str)):
                    # Convert strings to bytes
                    value = np.array([v.encode('utf-8') for v in value])
                h5f.create_dataset(key, data=np.array(value))
        else:
            # Convert strings to bytes if necessary
            if (isinstance(data, (list, np.ndarray))
                and len(data) > 0 and isinstance(data[0], str)):
                # Convert strings to bytes
                data = np.array([v.encode('utf-8') for v in data])
            h5f.create_dataset(dataset_name, data=np.array(data))