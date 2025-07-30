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

from .aa_to_int import aa_to_int

def aa_to_num(xseq):
    """
    Converts amino acid sequences to numerical representations.

    Parameters:
        xseq (list of strings): Amino acid sequence(s).

    Returns:
        list: Numerical representation of the amino acid sequences.
    """
    n = len(xseq)  # Number of sequences
    m = len(xseq[0]) if n > 0 else 0  # Length of the first sequence

    # Initialize result list
    mret = []

    for seq in xseq:
        # Convert the amino acid sequence to integers (map from 1 to 20,
        # subtract 1 for 0-indexing)
        vls = aa_to_int(seq)
        vls = [i - 1 for i in vls]  # Subtract 1 to adjust to 0-indexed values
        if -1 in vls:  # Check if any invalid amino acid is encountered
            mret.append(-1)
            continue
        
        # Create the positional powers
        pot = list(range(m))

        # Compute the numerical representation using a loop and sum
        total = 0
        for i, p in enumerate(pot):
            total += (20 ** p) * vls[i]

        mret.append(total)

    return mret