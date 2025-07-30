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

def orthrand(xlines, Um, Un):
    """
    Generates orthonormal projection lines for use in the SweeP strategy 
    with a new pseudorandom generator approach.

    This function creates a pair of projections based on the input 
    vectors `Um` and `Un` using a mathematical transformation and returns 
    the result.

    Parameters:
        xlines (array-like): Indices of the lines to be used in the projection.
        Um (array-like): Array of values used to generate `Z1`.
        Un (array-like): Array of values used to generate `Z2`.

    Returns:
        np.ndarray: Array containing the orthonormal projections.
    """
    maxcol = len(Um)  # Get the number of columns in Um
    
    nlines = len(xlines)  # Get the number of lines
    Un = Un[xlines]  # Access Un at the positions defined by `xlines`

    # Partitioning process to generate Z1 and Z2:
    # - Generate Z1 based on Um
    Z1 = np.float32(10**8 * (10**4 * Um - np.trunc(10**4 * Um)))
    # - Generate Z2 based on Un
    Z2 = np.float32(10**8 * (10**4 * Un - np.trunc(10**4 * Un)))
    
    Z1 = np.repeat([Z1], nlines, axis=0)
    Z2 = np.repeat([Z2], maxcol, axis=0).T

    # Calculate the orthonormal projection result
    # Apply the sine function to the product of Z1 and Z2
    mret = np.sin(Z1 * Z2)
    
    # Return the resulting projections
    return mret

