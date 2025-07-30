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

import numpy as np
import h5py
import pickle
from scipy.io import loadmat

def _load_matrix_from_path(path):
    """
    Loads a matrix from a file. Tries .txt, .npy, .h5, .mat, and .pickle formats in sequence.
    
    Parameters:
        path (str): Path to the file.
    
    Returns:
        np.ndarray: A numpy array loaded from the file.
    
    Raises:
        ValueError: If no valid method succeeds in loading the file.
    """
    errors = []
    
    # Try loading as .txt
    try:
        return np.loadtxt(path, encoding='utf-8')
    except FileNotFoundError as e:
        raise FileNotFoundError(e)
    except Exception as e:
        errors.append(f"TXT load error: {e}")
    
    # Try loading as .npy
    try:
        return np.load(path, allow_pickle=True)
    except Exception as e:
        errors.append(f"NPY load error: {e}")
    
    # Try loading as .h5
    try:
        with h5py.File(path, 'r') as file:
            first_key = list(file.keys())[0]
            return file[first_key][:]
    except Exception as e:
        errors.append(f"HDF5 load error: {e}")
    
    # Try loading as .mat
    try:
        # Attempt HDF5-based .mat format
        with h5py.File(path, 'r') as file:
            first_key = list(file.keys())[0]
            return file[first_key][:]
    except OSError:
        try:
            # Fallback to older .mat format
            mat_data = loadmat(path)
            keys = [key for key in mat_data.keys() if not key.startswith("__")]
            if len(keys) != 1:
                raise ValueError("The .mat file contains multiple datasets.")
            return mat_data[keys[0]]
        except Exception as e:
            errors.append(f"MAT load error: {e}")
    
    # Try loading as .pickle
    try:
        with open(path, 'rb') as file:
            return pickle.load(file)
    except Exception as e:
        errors.append(f"Pickle load error: {e}")
    
    # If all methods fail, raise a ValueError with detailed error messages
    raise ValueError(f"Failed to load matrix from {path}. Errors:\n" + "\n".join(errors))