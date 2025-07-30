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

import numpy as np

def pca(data_matrix):
    """
    Perform Principal Component Analysis (PCA) on the given data matrix using
    Singular Value Decomposition (SVD).

    This function computes the principal components of the input data matrix,
    including:
        - Principal component coefficients (eigenvectors)
        - Scores (projections of the data onto the principal components)
        - Eigenvalues (variances of the principal components)
        - Hotelling's T-squared statistic (a measure of the "outlierness" of
          each observation)

    The data matrix is first centered by subtracting the mean of each feature
    (column) before applying SVD.

    Parameters:
        - data_matrix (array-like): A 2D array where each row represents an
          observation and each column represents a variable.

    Returns:
        - coeff (array): Principal component coefficients (eigenvectors), with
          each column corresponding to a principal component.
        - score (array): Scores (projections) of the observations onto the
          principal components.
        - latent (array): Eigenvalues (variances) corresponding to the
          principal components, indicating the amount of variance explained by
          each component.
        - t_square (array): Hotelling's T-squared statistic for each
          observation, indicating its distance from the center in the principal
          component space.

    Notes:
        - The function centers the input data matrix by subtracting the mean
          of each feature.
        - The number of significant principal components is determined based on
          the singular values.
        - A sign convention is enforced on the coefficients to ensure
          consistency.
    """
    # Get the number of samples (rows) and features (columns) in the data
    # matrix
    num_samples, num_features = data_matrix.shape

    # Center the data matrix by subtracting the mean of each column (feature)
    centered_matrix = data_matrix - np.mean(data_matrix, axis=0)

    # Perform Singular Value Decomposition (SVD) on the centered data matrix
    u_matrix, singular_values, v_transpose = np.linalg.svd(centered_matrix,
                                                           full_matrices=True)

    # The principal component coefficients are the transpose of 'v' from SVD
    coeff = v_transpose.T

    # Calculate the eigenvalues (latent), which are the squared singular values
    # normalized by (num_samples - 1)
    latent = (singular_values ** 2) / (num_samples - 1)
    
    # Calculate the scores, which are the projections of the centered data on
    # the principal components
    score = np.dot(centered_matrix, coeff)

    # Compute Hotelling's T-squared statistic, which measures the "outlierness"
    # of each observation
    if num_samples > 1:
        # Determine the number of significant components based on the singular
        # values
        num_significant = np.sum(
            singular_values > max(num_samples, num_features) *
            np.finfo(singular_values.dtype).eps)
        
        # Calculate the T-squared statistic for each observation based on the
        # first 'num_significant' components
        t_square = ((num_samples - 1) *
                    np.sum(u_matrix[:, :num_significant] ** 2, axis=1))
    else:
        # If there is only one sample, T-squared is just a zero vector
        t_square = np.zeros(num_samples)

    # Adjust the signs of the coefficients and scores for consistency
    max_indices = np.argmax(np.abs(coeff), axis=0)
    col_signs = np.sign(coeff[max_indices, range(coeff.shape[1])])
    
    # Apply the sign convention to the coefficients and scores
    coeff *= col_signs
    score *= col_signs

    return coeff, score, latent, t_square