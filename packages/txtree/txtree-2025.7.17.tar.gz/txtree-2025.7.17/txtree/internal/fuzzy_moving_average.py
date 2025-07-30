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

from scipy.signal.windows import triang
from scipy.ndimage import convolve1d
import numpy as np

def fuzzy_moving_average(input_vector, window_half_size, hedge=1,
                          iterations=1):
    """
    Fuzzy Moving Average using convolution with a triangular window.

    Parameters:
        - input_vector: Input vector to be smoothed.
        - window_half_size: Half the size of the triangular window.
        - hedge: Hedge parameter for the triangular function (default is 1).
        - iterations: Number of smoothing iterations (default is 1).

    Returns:
        - smoothed_vector: Smoothed vector after applying the moving average.
    """
    # Create a triangular window and apply the hedge parameter
    window_size = 2 * window_half_size + 1
    window = np.power(triang(window_size), hedge)
    
    # Iteratively apply smoothing
    smoothed_vector = input_vector.copy()
    for _ in range(iterations):
        smoothed_vector = convolve1d(smoothed_vector, window / window.sum(),
                                     mode='reflect')
    
    return smoothed_vector