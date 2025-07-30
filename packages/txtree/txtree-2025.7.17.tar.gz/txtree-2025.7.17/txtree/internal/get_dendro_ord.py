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

import os
import sys
import numpy as np
from sklearn.cluster import KMeans
from scipy.cluster.hierarchy import linkage, dendrogram
from scipy.spatial.distance import pdist
from tqdm import tqdm

def get_dendro_ord(data, method='ward', metric='euclidean',
                   max_clus_size=None, verbose=True):
    """
    Generates an ordination of data points based on hierarchical clustering.

    By default, this function performs hierarchical clustering directly on the
    entire dataset. If `max_clus_size` is specified, it first applies KMeans
    clustering to divide the data into clusters, ensuring that no cluster
    exceeds the size `max_clus_size`. It then performs hierarchical clustering
    within each cluster and orders the clusters based on hierarchical
    clustering of their centroids. The final ordination is a concatenation of
    the ordered clusters.

    Using KMeans before hierarchical clustering (when `max_clus_size` is
    specified) allows this approach to handle very large matrices efficiently.
    By breaking the data into smaller clusters, the hierarchical clustering
    step is applied only within each cluster, reducing computational
    complexity and memory usage.

    Parameters:
        - data (np.ndarray): A data matrix (n_samples x n_features) to be
          clustered and ordered.
        - method (str, optional): The linkage method for hierarchical
          clustering. Options include 'ward', 'single', 'complete', 'average',
          etc. Defaults to 'ward'.
        - metric (str, optional): The distance metric for hierarchical
          clustering. Options include 'euclidean', 'cosine', 'cityblock', etc.
          Defaults to 'euclidean'.
        - max_clus_size (int, optional): The maximum number of items allowed in
          each KMeans cluster. If None, hierarchical clustering is performed
          directly on the entire dataset without KMeans preprocessing.
          Defaults to None.
        - verbose (bool, optional): If True, enables progress tracking.
          Defaults to True.

    Returns:
        - list: A list of indices representing the final ordination of the data
          points.
    """
    # Set OMP_NUM_THREADS to '1' to avoid [WinError 2] in
    # sklearn.cluster.KMeans
    os.environ['OMP_NUM_THREADS'] = '1'

    n_samples = data.shape[0]

    # Check if max_clus_size is greater than the total number of entries in
    # data
    if max_clus_size is not None and max_clus_size > n_samples:
        raise ValueError(f"max_clus_size ({max_clus_size}) cannot be greater "
                         "than the total number of entries in data "
                         f"({n_samples}).")

    if max_clus_size is None:
        if verbose:
            print(("Running hierarchical clustering..."))
        
        # Perform hierarchical clustering on the entire dataset
        linkage_matrix = linkage(data, method=method, metric=metric)
        dendrogram_result = dendrogram(linkage_matrix, no_plot=True)
        final_ordination = dendrogram_result['leaves']
        
        if verbose:
            print("Hierarchical clustering completed.")
            print("Final ordination generated successfully.")
        
        return [int(i) for i in final_ordination]
    
    else:
        if verbose:
            print("Running KMeans clustering to divide data into clusters...")
        
        # Divide the number of entries by max_clus_size to get the initial k
        k = int(np.ceil(n_samples / max_clus_size))
        
        # Run KMeans with the initial k
        max_attempts = 100  # Set a maximum number of attempts
        attempts = 0
        while attempts < max_attempts:
            attempts += 1
            # Print the number of clusters being tested
            if verbose:
                print(f"Attempt {attempts}: Testing with {k} clusters...",
                      end='\r')
            
            kmeans = KMeans(n_clusters=k, random_state=0)
            labels = kmeans.fit_predict(data)
            centroids = kmeans.cluster_centers_
            
            # Check if any cluster has more than m items
            cluster_sizes = np.bincount(labels)
            if np.all(cluster_sizes <= max_clus_size):
                # Print success message
                if verbose:
                    print()
                    print(f"Found suitable clusters with k = {k}.")
                break
            else:
                # Increment k and retry if any cluster exceeds max_clus_size
                k += 1
        else:
            print()
            sys.tracebacklimit = -1
            raise ValueError(
                "Failed to find a suitable number of clusters after "
                f"{max_attempts} attempts. "
                "This is likely because the maximum cluster size defined is "
                "too small for the number of entries in the dataset. "
                "Consider increasing the maximum cluster size or "
                "re-evaluating the dataset."
            )
        
        if verbose:
            print(f"KMeans clustering completed with {k} clusters.")
            print("Running hierarchical clustering within each cluster...")
        
        # Perform hierarchical clustering for each KMeans cluster
        cluster_ordinations = []
        for cluster_id in tqdm(range(k), desc="Clustering progress", ncols=0,
                               disable=not verbose):
            # Original indices of points in the cluster
            cluster_indices = np.where(labels == cluster_id)[0]
            cluster_data = data[cluster_indices]
            
            if len(cluster_data) > 1:
                # Perform hierarchical clustering within the cluster
                cluster_linkage = linkage(cluster_data, method=method,
                                          metric=metric)
                # Create a dendrogram with the original indices
                cluster_dendrogram = dendrogram(cluster_linkage, no_plot=True,
                                                labels=cluster_indices)
                cluster_ordination = cluster_dendrogram['leaves']
                cluster_ordinations.append(
                    [cluster_indices[i] for i in cluster_ordination])
            else:
                # If the cluster has only one point, add the original index
                cluster_ordinations.append(cluster_indices)
        
        if verbose:
            print("Hierarchical clustering within clusters completed.")
            print("Running hierarchical clustering of centroids...")
        
        # Perform hierarchical clustering on the centroids to define
        # the ordination
        centroid_distances = pdist(centroids, metric=metric)
        centroid_linkage = linkage(centroid_distances, method=method)
        centroid_dendrogram = dendrogram(centroid_linkage, no_plot=True)
        
        # Order the clusters based on the hierarchical clustering of
        # centroids
        ordered_clusters = centroid_dendrogram['leaves']
        
        if verbose:
            print("Hierarchical clustering of centroids completed.")
            print("Generating final ordination...")
        
        # Concatenate the cluster ordinations in the defined order
        final_ordination = []
        for cluster_id in ordered_clusters:
            final_ordination.extend(cluster_ordinations[cluster_id])
        
        # Convert indices to integers
        final_ordination = [int(i) for i in final_ordination]
        
        if verbose:
            print("Final ordination generated successfully.")
        
        return final_ordination