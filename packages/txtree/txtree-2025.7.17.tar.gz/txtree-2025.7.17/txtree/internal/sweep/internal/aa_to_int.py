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

def aa_to_int(aa_list):
    """
    Converts a list of amino acids (or characters) to their corresponding
    integer values. The input list must be in uppercase for the conversion to
    be correct.
    
    Parameters:
    - aa_list (list): List of characters (amino acids) to be converted to
      integers.
    
    Returns:
    - list: List of integers corresponding to the characters in the input list.
    """
    # Mapping dictionary
    aa_map = { 
        "A": 1, "B": 21, "C": 5, "D": 4, "E": 7, "F": 14,
        "G": 8, "H": 9, "I": 10, "J": 0, "K": 12, "L": 11,
        "M": 13, "N": 3, "O": 0, "P": 15, "Q": 6, "R": 2,
        "S": 16, "T": 17, "U": 0, "V": 20, "W": 18, "X": 23,
        "Y": 19, "Z": 22, "*": 24, "-": 25, "?": 0
    }
    
    # Mapping the elements of the list to their integer values
    aa_list = [aa_map[aa] for aa in aa_list]
    
    return aa_list