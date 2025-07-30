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

from Bio.Seq import Seq
from Bio.SeqRecord import SeqRecord
import re

def create_seqrecord_list(seq_list, header_list=None):
    """
    Creates a list of SeqRecord (Biopython object) from a list of sequences.

    This function takes a list of biological sequences and, optionally, a list
    of headers, and creates a list of SeqRecord objects with corresponding
    headers.

    Parameters:
        - seq_list (list of str): List of biological sequences in string
          format.
        - header_list (list of str or None): List of headers in string format.
          If None, the headers will be automatically assigned as numbers in
          increasing order.

    Returns:
        - list of SeqRecord: List of SeqRecord objects created from the input
          sequences and headers.
    """
    if header_list is None:
        header_list = list(range(1, len(seq_list) + 1))
    
    seqrecord_list = []
    for i in range(len(seq_list)):
        description = str(header_list[i])
        ident = re.split('\s+', description)[0]
        record = SeqRecord(Seq(seq_list[i]), description=description, id=ident)
        seqrecord_list.append(record)
    
    return seqrecord_list