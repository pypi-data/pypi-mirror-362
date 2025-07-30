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

def create_sweep_masks(nbits, ntake):
    """
    Generate all binary vector combinations of length `nbits` with exactly
    `ntake` ones.

    This function recursively creates all possible binary vectors of length
    `nbits` where exactly `ntake` elements are set to 1, and the remaining
    elements are set to 0.
    
    Parameters:
    - nbits (int): The total number of elements in the binary vector.
    - ntake (int): The number of elements in the binary vector to be set to 1.

    Returns:
    - list of lists: A list containing all possible binary vectors of length
      `nbits` with exactly `ntake` ones. Each binary vector is represented as
      a list of 0s and 1s.
    """
    
    # Recursive helper function to generate combinations of binary vectors
    # with exactly `ntake` ones
    def generate_combination(position, nbits, ntake, vector):
        if ntake == 0:
            combinations.append(vector[:])
            return
        if position == nbits:
            return
        
        # Place a 1 at the current position and recursively generate the next
        # vector
        vector[position] = 1
        generate_combination(position + 1, nbits, ntake - 1, vector)
        
        # Place a 0 at the current position and recursively generate the next
        # vector
        vector[position] = 0
        generate_combination(position + 1, nbits, ntake, vector)
    
    combinations = []
    initial_vector = [0] * nbits
    generate_combination(0, nbits, ntake, initial_vector)
    
    return combinations