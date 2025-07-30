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

def lambert_w(branch, x, dtype=np.float64):
    """
    Lambert W function: Functional inverse of x = w * exp(w).
    
    Parameters:
        - branch (int): Branch to compute (-1 for lower branch, 0 for upper
          branch).
        - x (array-like): Input value(s).

    Returns:
        - numpy.ndarray: Computed Lambert W values for the given input.
    """
    # Convert x to a numpy array for vectorized operations
    x = np.asarray(x, dtype=np.float64)
    
    # Initial guess
    if branch == -1:
        w = -2 * np.ones_like(x)  # Start below -1 for the lower branch
    else:
        w = np.ones_like(x)  # Start above -1 for the upper branch
    
    v = np.inf * w  # Initialize previous value for iteration comparison
    
    # Halley's method
    with np.errstate(divide='ignore', invalid='ignore'):
        while np.any(np.abs(w - v) / np.abs(w) > 1e-8):
            v = w
            e = np.exp(w)
            f = w * e - x  # Function to zero
            w = w - f / (e * (w + 1) - (w + 2) * f / (2 * w + 2))
        
    return w