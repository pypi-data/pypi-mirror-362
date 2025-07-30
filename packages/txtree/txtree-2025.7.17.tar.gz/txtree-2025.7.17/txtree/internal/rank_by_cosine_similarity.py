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

from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

def rank_by_cosine_similarity(query_vector, subject_vectors):
    """
    Rank subjects based on their cosine similarity to a query vector.

    Parameters:
        - query_vector (np.ndarray): Vector representing the query.
        - subject_vectors (np.ndarray): Matrix where each row is a vector
          representing a subject.

    Returns:
        tuple: A tuple containing:
            - ranked_indices (list): Indices of subjects ranked by similarity
              in descending order.
            - cosine_similarities (np.ndarray): Cosine similarity scores
              corresponding to the ranked indices.
    """
    # Reshape the query vector for compatibility with cosine_similarity
    query_vector = query_vector.reshape(1, -1)

    # Calculate cosine similarities
    cosine_similarities = cosine_similarity(query_vector, subject_vectors)

    # Rank the subjects based on their similarity to the query
    ranked_indices = np.argsort(cosine_similarities[0], stable=True)[::-1]
    cosine_similarities = cosine_similarities[0][ranked_indices]

    return ranked_indices, cosine_similarities