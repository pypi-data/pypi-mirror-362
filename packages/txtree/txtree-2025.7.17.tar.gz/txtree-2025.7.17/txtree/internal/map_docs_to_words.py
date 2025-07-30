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

from tqdm import tqdm

def map_docs_to_words(tokenized_docs, word_list, verbose=True):
    """
    Maps each document to the words (tokens) it contains from a given list.

    This function creates an index that associates each document (by its index)
    with the words from `word_list` that appear in it.
    
    Parameters:
        - tokenized_docs (list): A list of documents, where each document is
          represented as a list of tokens (words).
        - word_list (list): A list of target tokens to search for in the
          documents.
        - verbose (bool): Boolean flag to enable/disable progress tracking
          (default is True).
    
    Returns:
        - list of lists: A list where each element is a sublist containing the
          indices of tokens (from `word_list`) found in the corresponding
          document. The order of the sublists matches the order of documents
          in `tokenized_docs`.
    """
    # Create a dictionary mapping tokens to their indices in `word_list`
    word_dict = {token: i for i, token in enumerate(word_list)}
    
    # Create a set of tokens for faster membership testing
    word_keys = set(word_dict.keys())

    # Initialize the result list
    doc_word_idx = []

    # Iterate over the tokenized documents
    for doc in tqdm(tokenized_docs, desc='Searching', ncols=0,
                    disable=not verbose):
        # Get the indices of tokens present in the current document
        doc_word_idx.append([word_dict[token] for token in doc if token in
                             word_keys])

    return doc_word_idx