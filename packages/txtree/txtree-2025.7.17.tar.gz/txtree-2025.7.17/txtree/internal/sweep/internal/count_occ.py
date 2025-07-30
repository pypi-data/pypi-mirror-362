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

from collections import Counter

def count_occ(input_list):
    """
    Count occurrences of each item in the input list, returning two separate
    lists: one with items and one with their corresponding counts, ordered by
    the items in ascending order.

    Parameters:
        input_list (list): The list of items to count.

    Returns:
        tuple: A tuple containing two lists:
               - A list of items, ordered in ascending order.
               - A list of counts corresponding to each item.
    """
    # Count occurrences using Counter
    count_dict = Counter(input_list)
    
    # Sort items by key and separate into two lists
    items, counts = zip(*sorted(count_dict.items()))
    
    return list(items), list(counts)