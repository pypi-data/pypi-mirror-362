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
from .lambert_w import lambert_w

def transform_with_lambert_w(kmer_counts):
    """
    Apply a transformation to input values using the Lambert W function.

    This function transforms the input values using a custom transformation
    involving the Lambert W function. Specifically, it computes:
        fx(x) = (-W₀(-exp(-x) * x))^0.1,
    where W₀ is the upper branch of the Lambert W function. After the
    transformation, any zeros in the result are replaced with -1.

    Parameters:
        - values (array-like): Array of values to be transformed.
          Expected to be non-negative values.

    Returns:
        - numpy.ndarray: The transformed values, with zeros replaced by -1.
    """
    # Define the function fx using Lambert W
    fx = lambda x: (-lambert_w(0, -np.exp(-x) * x)) ** 0.1
    
    # Apply the transformation
    u = fx(kmer_counts)
    
    # Replace zeros with -1
    u[u == 0] = -1
    
    return u