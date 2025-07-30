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

def estimate_scipy_linkage_mem(n, m=None):
    """
    Estimates the memory usage for the input to scipy's linkage function based
    on the number of rows.

    Parameters:
        - n (int): The number of observations (rows).

    Returns:
        - float: The estimated memory usage in gigabytes (GB) for the linkage
          computation.
    """
    # Size of one element in bytes
    element_size = np.dtype(np.float64).itemsize

    # Condensed distance matrix: n*(n-1)/2 elements
    total_elements = n * (n - 1) // 2

    # Total memory usage in bytes
    total_memory_bytes = total_elements * element_size

    # Convert bytes to gigabytes
    total_memory_gb = total_memory_bytes / (1024 ** 3)

    return total_memory_gb