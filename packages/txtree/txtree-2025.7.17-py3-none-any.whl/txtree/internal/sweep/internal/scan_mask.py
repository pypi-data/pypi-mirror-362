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

def scan_mask(xseq, xmask):
    """
    Performs a scan on the sequence `xseq` based on the mask `xmask`.
    Optimizes memory usage for masks with large `nbits`.

    Parameters:
        xseq (str): Amino acid sequence.
        xmask (list or array-like): Binary mask to apply to the sequence.

    Returns:
        list: Extracted columns based on the mask.
    """
    xseq_len = len(xseq)  # Length of the sequence
    
    # Ensure a minimum sequence length of 10
    min_len = 10
    if xseq_len < min_len:
        xseq = xseq + "K" * (min_len - xseq_len)
        xseq = xseq[:min_len]
        
        xseq_len = min_len

    # Indices where the mask is 1
    ids = (i for i, bit in enumerate(xmask) if bit)
    
    IDS = [
        range(idx, min(idx + xseq_len, xseq_len))
        for idx in ids
    ]

    # Find the minimum length across all IDS arrays
    lmx = min(map(len, IDS))

    # Extract columns based on the mask and ensure uniformity
    xcols = [xseq[idx] for ids_array in IDS for idx in ids_array[:lmx]]

    xcols = [xcols[i:i+lmx] for i in range(0, len(xcols), lmx)]
    
    xcols = list(zip(*xcols))
    
    return xcols