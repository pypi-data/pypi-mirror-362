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

def count_occurrences(input_list):
    """
    Counts the occurrences of each item in the input list and returns the
    unique items along with their counts in descending order.

    This function calculates the frequency of each unique item in the provided
    list, sorts the items by their occurrence count in descending order, and
    returns two lists: one with the unique items and one with their
    corresponding counts.

    Parameters:
        - input_list (list): A list of items to count occurrences of.

    Returns:
        - unique_items (list): A list of unique items sorted by occurrence
          count.
        - counts (list): A list of counts corresponding to the unique items,
          sorted in descending order.
    """
    
    # Count the occurrences of each item in the list
    counts = Counter(input_list)
    
    # Extract the unique items and their counts
    unique_items = list(counts.keys())
    counts = list(counts.values())
    
    # Combine items and counts into a list of tuples and sort by count in
    # descending order
    sorted_items_counts = sorted(zip(unique_items, counts), key=lambda x: x[1],
                                 reverse=True)
    
    # Separate the unique items and counts, now sorted
    unique_items, counts = zip(*sorted_items_counts)
    
    return (unique_items, counts)