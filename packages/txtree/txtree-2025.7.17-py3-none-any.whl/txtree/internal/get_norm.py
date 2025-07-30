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

def get_norm(mat):
    """
    Calculates the Euclidean norm of each row in a matrix.

    This function computes the Euclidean norm (or L2 norm) of each row in the
    given matrix. The norm is calculated as the square root of the sum of
    squares of the elements in each row.

    Parameters:
        - mat (np.ndarray): A matrix (n_samples x n_features), where each row
          represents a sample.

    Returns:
        - np.ndarray: An array containing the Euclidean norm of each row in
          the matrix.
    """
    norm = np.sqrt(np.sum(mat**2, axis=1))
    return norm