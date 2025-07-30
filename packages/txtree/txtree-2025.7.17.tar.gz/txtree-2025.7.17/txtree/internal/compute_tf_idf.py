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

import math
from collections import defaultdict
import numpy as np
from tqdm import tqdm

def compute_tf_idf(tokenized_docs, word_list=None, return_term_norms=False,
                   return_tf_idf=True, verbose=False):
    """
    Computes the TF-IDF values for each term across a collection of documents
    using float32 precision.

    Parameters:
        - tokenized_docs (list of list of str): A collection of documents
          where each document is represented as a list of tokenized terms.
          Example: [["hello", "world"], ["example", "document"]]
        - word_list (list of str, optional): Specifies which terms to include
          in the output and their order. If None, uses all unique terms from
          the corpus in alphabetical order. Defaults to None.
        - return_term_norms: Return term L2 norms as dict. Defaults to False.
        - return_tf_idf: Return TF-IDF values. Defaults to True.
        - verbose (bool, optional): If True, displays a progress bar during
          computation. Defaults to False.

    Returns:
        - If both return_tf_idf and return_term_norms are True:
            Returns a tuple (tf_idf_values, tf_idf_term_norms)
        - If only return_tf_idf is True:
            Returns tf_idf_values
        - If only return_term_norms is True:
            Returns tf_idf_term_norms
        - If both are False:
            Returns None

        Where:
        - tf_idf_values (dict): A dictionary mapping terms to their TF-IDF
          values:
          * Keys (str): Vocabulary terms
          * Values (list of float32): TF-IDF values for each document
          * Terms not present in a document receive 0.0 for that document
          Example: {"hello": [0.5, 0.0], "world": [0.5, 0.0]}
        - tf_idf_term_norms (dict): A dictionary mapping terms to their L2
          norms
          * Keys (str): Vocabulary terms
          * Values (float32): L2 norm of the TF-IDF vector for each term
          
    Note:
        - Uses smoothed IDF calculation: log((1 + N)/(1 + df)) + 1 where N is
          total documents and df is document frequency.
        - All numerical operations use float32 precision.
    """
    # Compute IDF
    idf = _compute_idf(tokenized_docs)
    
    total_docs = len(tokenized_docs)
    
    # Use `word_list` if provided; otherwise, corpus terms
    if word_list is None:
        word_list = sorted(idf.keys())
    
    tf_idf_values = defaultdict(list)
    tf_idf_term_norms = defaultdict(np.float32)
    
    # Compute TF-IDF per term
    for term in tqdm(word_list, desc="Computing TF-IDF", disable=not verbose):
        tf_idf_values_term = np.zeros(total_docs, dtype=np.float32)
        if term in idf:
            # For each document, compute TF-IDF if term is present
            for i, doc in enumerate(tokenized_docs):
                if term in doc:
                    tf = _compute_tf(doc)
                    tf_idf_values_term[i] = np.float32(tf[term] * idf[term])
        if return_tf_idf:
            tf_idf_values[term] = tf_idf_values_term.tolist()
        if return_term_norms:
            tf_idf_term_norms[term] = np.linalg.norm(
                tf_idf_values_term, ord=2).astype(np.float32)
    
    # Determine what to return based on the parameters
    if return_tf_idf and return_term_norms:
        return dict(tf_idf_values), dict(tf_idf_term_norms)
    elif return_tf_idf:
        return dict(tf_idf_values)
    elif return_term_norms:
        return dict(tf_idf_term_norms)
    else:
        return None

def _compute_tf(doc):
    """Calculates term frequency (TF) for a single document using float32."""
    total_terms = np.float32(len(doc))
    term_counts = defaultdict(int)
    for term in doc:
        term_counts[term] += 1
    return (
        {term: np.float32(count) / total_terms
         for term, count in term_counts.items()})

def _compute_idf(tokenized_docs):
    """Calculates smoothed IDF for all terms in the document collection using float32."""
    doc_freq = defaultdict(int)
    total_docs = np.float32(len(tokenized_docs))
    
    for doc in tokenized_docs:
        unique_terms = set(doc)
        for term in unique_terms:
            doc_freq[term] += 1
    
    # Smoothed IDF: log((1 + total_docs) / (1 + freq)) + 1
    return (
        {term: np.float32(
            math.log(
                (1.0 + total_docs) / (1.0 + np.float32(freq)))) +
            np.float32(1.0) for term, freq in doc_freq.items()})