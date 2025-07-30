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
from math import sqrt

def estimate_scipy_linkage_n(memory_gb):
    """
    Estimates the number of observations (rows) needed to reach a given memory
    usage in gigabytes for scipy's linkage function.

    Parameters:
        - memory_gb (float): The target memory usage in gigabytes (GB).

    Returns:
        - int: The estimated number of observations (rows).
    """
    # Size of one element in bytes
    element_size = np.dtype(np.float64).itemsize

    # Convert memory from gigabytes to bytes
    total_memory_bytes = memory_gb * (1024 ** 3)
    
    # Solve for n in the equation:
    # total_memory_bytes = (n * (n - 1) / 2) * element_size
    # Using the quadratic formula:
    n = (1 + sqrt(1 + 8 * total_memory_bytes / element_size)) / 2
    
    return int(n)
