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

def load_h5(file_path):
    """
    Loads data from an HDF5 (.h5) file.

    This function reads data from an HDF5 file, handling both numerical arrays
    and strings encoded as bytes. Strings are automatically decoded to Unicode.

    Parameters:
        - file_path (str): The path to the .h5 file from which the data will
          be loaded.

    Returns:
        - dict or array: If the file contains multiple datasets, a dictionary
          with dataset names as keys is returned. If the file contains a
          single dataset, the corresponding array is returned.
    """
    with h5py.File(file_path, "r") as h5f:
        if len(h5f.keys()) == 1:
            # Single dataset
            dataset_name = list(h5f.keys())[0]
            data = h5f[dataset_name][()]
            # Check if the data is bytes and decode to string if necessary
            if isinstance(data, np.ndarray) and data.dtype.kind == 'S':
                data = np.array([v.decode('utf-8') for v in data])
            return data
        else:
            # Multiple datasets
            data_dict = {}
            for key in h5f.keys():
                dataset = h5f[key][()]
                # Check if the dataset is bytes and decode to string if
                # necessary
                if (isinstance(dataset, np.ndarray) and
                    dataset.dtype.kind == 'S'):
                    dataset = np.array([v.decode('utf-8') for v in dataset])
                data_dict[key] = dataset
            return data_dict