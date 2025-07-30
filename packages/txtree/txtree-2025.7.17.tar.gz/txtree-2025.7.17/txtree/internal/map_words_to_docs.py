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
from collections import defaultdict

def map_words_to_docs(word_list, tokenized_docs, verbose=True):
    """
    Maps each word in a given list to the documents where it appears.

    This function creates an index that associates each word from `word_list`
    with the documents (by their indices) in which the word is found.

    Parameters:
        - word_list (list): A list of tokens to search for in the documents.
        - tokenized_docs (list): A list of documents, where each document is
          represented as a list of tokens (words).
        - verbose (bool): Boolean flag to enable/disable progress tracking
          (default is True).

    Returns:
        - list of lists: A list containing sublists, where each sublist
          contains the indices of the documents that contain the corresponding
          token in `word_list`. The order of the sublists matches the order of
          tokens in `word_list`.
    """
    # Convert `word_list` to a set for faster lookups
    word_set = set(word_list)

    # Preprocess `tokenized_docs` into a list of sets for efficient membership
    # testing
    tokenized_docs = [set(doc) for doc in tokenized_docs]

    # Initialize the dictionary to hold indices of documents for each token
    token_idx = defaultdict(list)

    # Iterate over each document with its index
    for index, doc in enumerate(tqdm(tokenized_docs, desc='Searching',
                                     ncols=0, disable=not verbose)):
        # Find intersection of tokens in the document with `word_set`
        for token in doc:
            if token in word_set:
                token_idx[token].append(index)

    # Convert `defaultdict` to a list of lists in the order of `word_list`
    return [token_idx[token] for token in word_list]