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

def explode_list(lists_of_lists, return_indices=False):
    """
    Flattens a list of lists into a single list and optionally returns the
    indices.

    This function takes a list of lists and flattens it into a single list.
    Each item from the sublists is added to the flattened list, and the
    function can optionally return the indices of the items in the original
    structure.

    Parameters:
        - lists_of_lists (list of lists): A list where each element is a
          sublist that needs to be flattened.
        - return_indices (bool, optional): If True, returns the indices of the
          original items. Defaults to False.

    Returns:
        - list: The flattened list containing all the elements from the
          sublists.
        - list of tuples (optional): If return_indices is True, a list of
          tuples where each tuple represents the indices of the items in the
          original sublists.
    """
    flattened_list = []
    indices = []
    
    for sublist_idx, sublist in enumerate(lists_of_lists):
        for item_idx, item in enumerate(sublist):
            flattened_list.append(item)
            indices.append((sublist_idx, item_idx))
    
    if return_indices:
        return flattened_list, indices
    else:
        return flattened_list