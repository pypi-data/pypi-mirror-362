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
from .orthrand import orthrand

def create_proj_mat(rows, cols):
    """
    Generate a pseudo-random projection matrix designed for use in the SWeeP
    method.

    Parameters:
        rows (int): Number of rows in the projection matrix.
        cols (int): Number of columns in the projection matrix.

    Returns:
        np.ndarray: The computed pseudo-random projection matrix R.
    """
    Um = np.sin(range(1, cols + 1))
    Un = np.sin(range(1, rows + 1))
    xnorm = np.sqrt(rows / 3)
    idx = list(range(0, rows))
    R = (1 / xnorm) * orthrand(idx, Um, Un)
    return R