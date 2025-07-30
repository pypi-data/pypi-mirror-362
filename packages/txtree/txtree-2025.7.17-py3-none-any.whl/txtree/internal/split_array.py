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

def split_array(arr, chunk_size):
    """
    Splits an array into chunks of a specified size.

    This function divides the input array into smaller subarrays, each
    containing up to `chunk_size` elements. If the array size is not a
    multiple of `chunk_size`, the final chunk will contain the remaining
    elements.

    Parameters:
        - arr (list): The input array to be split.
        - chunk_size (int): The size of each chunk.

    Returns:
        - list of list: A list containing subarrays (chunks), where each chunk
          has a maximum of `chunk_size` elements.
    """
    chunks = []
    for i in range(0, len(arr), chunk_size):
        chunks.append(arr[i:i+chunk_size])
    return chunks