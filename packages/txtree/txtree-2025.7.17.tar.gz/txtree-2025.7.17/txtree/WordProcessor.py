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
import pandas as pd
from .internal import (aminocode, compute_tf_idf, count_occurrences,
                       create_seqrecord_list, explode_list, get_dendro_ord,
                       map_docs_to_words, map_words_to_docs, mat_to_ete_tree,
                       parallelization, pca, rank_by_cosine_similarity, sweep,
                       tokenize)

class WordProcessor:
    def __init__(self, corpus=None, corpus_ids=None, emb_size=1200):
        """
        Initializes the WordProcessor instance.
    
        Parameters:
            - corpus (list, optional): A list of documents to be processed.
              Defaults to None.
            - corpus_ids (list, optional): A list of IDs corresponding
              to the documents. If None, a list of IDs in string format is
              created with a range based on the length of the corpus. Defaults
              to None.
            - emb_size (int, optional): The size of the word embedding.
              Defaults to 1200.
    
        Raises:
            - ValueError: If `emb_size` is not divisible by 4.
        """
        if emb_size % 4 != 0:
            raise ValueError(f"proj_size ({emb_size}) must be divisible by 4.")
    
        self.corpus = corpus
        self.emb_size = emb_size
    
        # If corpus_label is None, create a list of labels in string format
        # with a range
        if corpus_ids is None and corpus is not None:
            self.corpus_labels = [str(i) for i in range(len(corpus))]
        else:
            self.corpus_ids = corpus_ids
    
        # Initialize attribute generators dictionary
        self._init_attribute_generators()

    def _init_attribute_generators(self):
        """
        Initializes the mapping of attributes to their respective generator
        methods. This avoids duplication and ensures a consistent setup.
        """
        self._attribute_generators = {
            "tokenized_corpus": "tokenize_corpus",
            "word_list": "create_word_list",
            "word_doc_idx": "create_word_doc_idx",
            "doc_idx": "create_doc_word_idx",
            "encoded_corpus": "encode_corpus",
            "sweeped_corpus": "run_sweep",

            "word_emb": "create_word_emb",

            "tf_idf_score": "compute_tf_idf",
            "word_list_filt": "create_word_list_filt",
            "filt_idx": "create_word_list_filt",
            "word_count_filt": "create_word_list_filt",
            "word_to_idx_fil": "create_word_list_filt",

            "word_emb_filt": "create_word_emb_filt",
            "pca_coeff": "create_pca_coeff",
            "word_emb_filt_pca": "create_word_emb_pca",
            "word_emb_pca": "create_word_emb_pca",
            "doc_emb_pca": "create_doc_emb_pca",

            "word_dendro_ord": "compute_word_dendro_ord",
            "doc_dendro_ord": "compute_doc_dendro_ord",
        }

    def __getattr__(self, name):
        """
        Handles access to uninitialized attributes.

        Parameters:
            - name (str): The name of the attribute being accessed.

        Raises:
            - AttributeError: If the attribute has not been initialized
              yet and cannot be accessed.
        """
        if name in self._attribute_generators:
            generator_method = self._attribute_generators[name]
            raise AttributeError(
                f"The attribute '{name}' has not been initialized. It can be "
                f"initialized by calling the method: '{generator_method}()'."
            )
        else:
            raise AttributeError(
                f"'{type(self).__name__}' object has no attribute '{name}'."
            )

    def __getstate__(self):
        """
        Returns the state of the object for serialization.
        """
        # Create a copy of the object's attribute dictionary
        state = self.__dict__.copy()
    
        return state
    
    def __setstate__(self, state):
        """
        Restores the state of the object during deserialization.
        """
        # Update the object's attribute dictionary with the saved state
        self.__dict__.update(state)
    
        # Check if `_attribute_generators` exists and initialize it if
        # necessary
        if "_attribute_generators" not in self.__dict__:
            self._init_attribute_generators()

    def process_corpus(self, init_prep=True, vectorize=True, lower=True,
                       filt=True, tf_idf_threshold=0.1,
                       n_jobs=1, chunk_size=1000, verbose=True):
        """
        Prepares the corpus by processing the documents, tokenizing, 
        creating necessary indices, and performing filtering based on 
        TF-IDF scores. Allows for controlling which parts of the process 
        to execute: initial preparation and vectorization.
    
        Parameters:
            - init_prep (bool, optional): If True, executes the initial
              preparation phase. Default is True.
            - vectorize (bool, optional): If True, executes the vectorization
              phase. Default is True.
            - lower (bool, optional): If True, converts all text to lowercase.
              Only has an effect if `init_prep` is True. Default is True.
            - filt (bool, optional): If True, performs additional filtering of
              the word list based on TF-IDF. Only has an effect if `init_prep` 
              is True. Default is True.
            - tf_idf_threshold (float, optional): The threshold for filtering
              words based on their TF-IDF scores. Only has an effect if
              `init_prep` and `filt` is True. Default is 0.1.
            - n_jobs (int, optional): Number of parallel jobs. Default is 1.
            - chunk_size (int, optional): Size of chunks to process in
              parallel. Default is 1000.
            - verbose (bool, optional): If True, prints progress. Default is
              True.
              
        Executed Phases:
            - **Initial Preparation**: 
                - If `initial_prep` is True, the method will execute the
                  initial preparation phase, which includes:
                  - Lowercasing the corpus (if `lower` is True).
                  - Tokenizing the corpus.
                  - Creating word lists and word indices (word-doc and
                    doc-word indices).
                  - Filtering words based on TF-IDF (if `filt` is True).
                  
            - **Vectorization**: 
                - If `vectorize` is True, the method will execute the
                  vectorization phase, which includes:
                  - Encoding the texts into a suitable format for analysis.
                  - Running the SWeeP process for further processing.
        """
        # Initial setup for total_steps
        total_steps = 0
        if init_prep:
            total_steps += 4
            if lower:
                total_steps += 1
            if filt:
                total_steps += 1

        if vectorize:
            total_steps += 2
        
        current_step = 1
    
        # Initial Preparation Phase
        if init_prep:
            if lower:
                corpus = self.corpus
                corpus_len = len(corpus)
    
                # Convert all text to lowercase for uniformity
                if verbose:
                    print(f"[{current_step}/{total_steps}] Converting "
                          "corpus to lowercase...")
                for i in range(corpus_len):
                    corpus[i] = corpus[i].lower()
                if verbose:
                    print("Corpus converted to lowercase.")
                current_step += 1
    
            # Tokenizing the corpus (splitting text into individual words)
            if verbose:
                print(f"[{current_step}/{total_steps}] Tokenizing corpus...")
            self.tokenize_corpus(n_jobs=n_jobs, chunk_size=chunk_size,
                                 verbose=verbose)
            current_step += 1
    
            # Creating word list and word indices
            if verbose:
                print(f"[{current_step}/{total_steps}] Creating word list...")
            self.create_word_list(verbose=verbose)
            current_step += 1
            
            if verbose:
                print(f"[{current_step}/{total_steps}] Creating word-doc "
                      "index...")
            self.create_word_doc_idx(verbose=verbose)
            current_step += 1
            
            if verbose:
                print(f"[{current_step}/{total_steps}] Creating doc-word "
                      "index...")
            self.create_doc_word_idx(verbose=verbose)
            current_step += 1
    
            if filt:
                # Perform additional filtering of the word list if `filt` is
                # True
                if verbose:
                    print(f"[{current_step}/{total_steps}] Filtering word "
                          "list...")
                self.compute_tf_idf(verbose=verbose)
                self.create_word_list_filt(tf_idf_threshold=tf_idf_threshold)
                if verbose:
                    print("Word filtering completed.")
                current_step += 1
    
        # Vectorization Phase
        if vectorize:    
            # Encoding the texts
            if verbose:
                print(f"[{current_step}/{total_steps}] Encoding texts...")
            self.encode_corpus(n_jobs=n_jobs, chunk_size=chunk_size,
                                verbose=verbose)
            current_step += 1
    
            # Run SWeeP
            if verbose:
                print(f"[{current_step}/{total_steps}] Running SWeeP...")
            self.run_sweep(n_jobs=n_jobs, chunk_size=chunk_size,
                           verbose=verbose)

    def create_word_emb(self, filt=True, n_jobs=1, chunk_size=1000,
                        verbose=True):
        """
        Creates word embeddings by calculating the mean of text vectors 
        that contain each word.
    
        The method splits the word index into chunks, processes each chunk 
        to calculate the mean of the text vectors for each word, and then 
        flattens the result into a single array.
    
        Parameters:
            - filt (bool, optional): If True, creates an embedding matrix 
              for the filtered words using the `create_word_emb_filt` method. 
              Default is True.
            - n_jobs (int, optional): The number of jobs to run in parallel.
              Default is 1.
            - chunk_size (int, optional): The size of chunks to split the 
              word index for parallel processing. Default is 1000.
            - verbose (bool, optional): If True, prints progress during the
              process. Default is True.
    
        Attributes:
            - word_emb (numpy.ndarray): The resulting array of word embeddings.
        """
        # Check for required attribute if filt is True
        if filt and not hasattr(self, "filt_idx"):
            raise AttributeError(
                "The attribute 'filt_idx' is required when 'filt' is True, "
                "but it does not exist. Run 'create_word_list_filt' to "
                "generate it."
                )
        
        word_doc_idx = self.word_doc_idx
        sweeped_corpus = self.sweeped_corpus
        
        par_function = lambda x: [np.mean(j, axis=0, where=~np.isnan(j))
                                  for j in [sweeped_corpus[i] for i in x]]
        word_emb = parallelization(word_doc_idx, par_function,
                                   n_jobs=n_jobs, chunk_size=chunk_size,
                                   desc="Creating word embedding",
                                   verbose=verbose)
        word_emb = np.array(word_emb, dtype=np.float32)
        
        self.word_emb = word_emb
        
        if filt:
            self.create_word_emb_filt()
        
    def create_doc_emb(self, n_jobs=1, chunk_size=1000, verbose=True):
        doc_word_idx = self.doc_word_idx
        word_emb = self.word_emb

        par_function = lambda x: [np.mean(j, axis=0, where=~np.isnan(j))
                                  for j in [word_emb[i] for i in x]]
        doc_emb = parallelization(doc_word_idx, par_function,
                                  n_jobs=n_jobs, chunk_size=chunk_size,
                                  desc="Creating document embedding",
                                  verbose=verbose)
        doc_emb = np.array(doc_emb, dtype=np.float32)
    
        self.doc_emb = doc_emb
        
    def run_pca(self, word_pca=True, doc_pca=True, verbose=True):
        """
        Runs Principal Component Analysis (PCA) on the word and document
        embeddings.
    
        Parameters:
            - word_pca (bool, optional): If True, performs PCA on word
              embeddings. Default is True.
            - doc_pca (bool, optional): If True, performs PCA on document
              embeddings. Default is True.
            - verbose (bool, optional): If True, prints progress during PCA
              computation. Default is True.
        """
        total_steps = 1
        current_step = 0
        
        if word_pca:
            total_steps += 1
        if doc_pca:
            total_steps += 1
    
        if verbose:
            print("Starting PCA computation...")
    
        # Creating PCA coefficients
        if verbose:
            current_step += 1
            print(f"[{current_step}/{total_steps}] Creating PCA "
                  "coefficients...")
        self.create_pca_coeff(verbose=verbose)
    
        # Performing PCA on word embeddings
        if word_pca:
            if verbose:
                current_step += 1
                print(f"[{current_step}/{total_steps}] Performing PCA on "
                      "word embeddings...")
            self.create_word_emb_pca(verbose=verbose)
    
        # Performing PCA on document embeddings
        if doc_pca:
            if verbose:
                current_step += 1
                print(f"[{current_step}/{total_steps}] Performing PCA on "
                      "document embeddings...")
            self.create_doc_emb_pca(verbose=verbose)
        
    def search_words(self, query, k_top=30, cut_min=2, use_pca=True,
                     n_components=50, return_dedro=False, 
                     clus_method='complete', clus_metric='cosine'):
        """
        Finds related words to the given query based on word embeddings and
        PCA. If `return_dedro=True`, performs clustering to generate a
        dendrogram representing the relationships between the related words.
        
        Parameters:
            - query (str or array-like): The word(s) to find related terms for.
              If a single word, it's converted to an array.
            - k_top (int, optional): The number of related words to return.
              Defaults to 30.
            - cut_min (int, optional): Minimum count threshold for words to be
              included in the result. Defaults to 2.
            - use_pca (bool, optional): Whether to use PCA for dimensionality
              reduction. Defaults to True.
            - n_components (int, optional): The number of PCA components to
              use. Defaults to 50.
            - return_dedro (bool, optional): Whether to return the dendrogram
              along with the related words. If True, clustering is performed
              to generate the dendrogram. Defaults to False.
            - clus_method (str, optional): The clustering method to use.
              Options include methods supported by
              `scipy.cluster.hierarchy.linkage` (e.g., 'ward', 'complete',
              'single', etc.). Defaults to 'complete'.
            - clus_metric (str, optional): The distance metric to use for
              clustering. Options include 'euclidean', 'cosine', etc.
              Defaults to 'cosine'.
        
        Returns:
            - list or tuple: 
                - If `return_dedro` is False, returns a list of related words.
                - If `return_dedro` is True, returns a tuple containing:
                    - A list of related words.
                    - A dendrogram (tree structure) representing the
                      relationships between the related words.
        """
        if use_pca:
            we = self.word_emb_pca[:, 0:n_components]
        else:
            we = self.word_emb
        
        word_list = self.word_list
        
        # Convert query to a numpy array if it's a string (single word query)
        if isinstance(query, str):
            query_list = [query]
        else:
            query_list = query
            
            
        # Get word indices for the query_list
        word_indices = [
            self.word_to_idx[word]
            for word in query_list if word in self.word_to_idx
        ]
        we_x = np.mean(we[word_indices], axis=0)
        
        ranked_indices, _ = rank_by_cosine_similarity(we_x, we)
        
        # Select the top k_top from the filtered list of related words
        related_words = word_list[ranked_indices][0:k_top]
        we_sel = we[ranked_indices][0:k_top]
        
        # Generate a dendrogram based on the related words
        if return_dedro:
            if query in related_words:
                reroot = query
            else:
                reroot = None
            tree = mat_to_ete_tree(
                we_sel, related_words,
                method=clus_method,
                metric=clus_metric,
                reroot=reroot
            )
            return related_words, tree
        else:
            return related_words
        
    def search_docs(self, query, k_top=20, query_type="word", use_pca=True,
                    n_components=50):
        """
        Searches for the most relevant documents in the corpus based on a
        query.
    
        Parameters:
        - query: The query for searching. It can be either:
            - A list of words or a single word (if query_type is "word").
            - An integer representing the index of a document in the corpus
              (if query_type is "doc_idx").
        - k_top: The number of top documents to return (default is 20).
        - n_components: The number of components to use for PCA (default is
          50).
        - use_pca: Boolean flag to determine whether to use PCA for
          dimensionality reduction (default is True).
        - query_type: Specifies the type of the query. Can be either "word" or
          "doc_idx". Default is "word".
    
        Returns:
        - A DataFrame containing the top k documents ranked by similarity to
          the query, with the following columns:
            - "doc_idx": The index of the document in the corpus.
            - "rank": The rank of the document.
            - "similarity": The cosine similarity between the query and the
              subject.
            - "doc": The full text of the document.
        """
        # Retrieve word and document embeddings and the tokenized corpus
        corpus = self.corpus
        if use_pca:
            we = self.word_emb_pca[:, 0:n_components]
            de = self.doc_emb_pca[:, 0:n_components]
        else:
            we = self.word_emb
            de = self.doc_emb
    
        # Check the query type and process accordingly
        if query_type == "word":
            # Convert query to a list if it's a string (single word query)
            if isinstance(query, str):
                query = [query]
                
            # Get word indices for the query
            word_indices = [self.word_to_idx[word]
                            for word in query if word in self.word_to_idx]
            we_x = np.mean(we[word_indices], axis=0)
            
        elif query_type == "doc_idx":
            # Treat the query as a document index (find the closest document to
            # the query document)
            if isinstance(query, int) and 0 <= query < len(corpus):
                # Retrieve the document embedding for the query document
                we_x = de[query]
            else:
                raise ValueError("Invalid document index provided for query.")
    
        else:
            raise ValueError("Invalid query type. Use 'word' or 'doc_idx'.")
        
        ranked_indices, similarity = rank_by_cosine_similarity(we_x, de)

        similarity = similarity[0:k_top]
        
        # Generate a range for top ranks (0 to k_top)
        top_rank_range = list(range(0, k_top))
        
        # Get the indices of the top ranked documents
        top_ranked_indices = ranked_indices[0:k_top]
        
        # Get the full documents corresponding to the top ranked indices
        top_docs = [corpus[i] for i in ranked_indices[0:k_top]]
        
        # Prepare a DataFrame with the rank, document index, overlap count with
        # top document, and document text
        search_results = pd.DataFrame({
            "doc_idx": top_ranked_indices,
            "rank": top_rank_range,
            "similarity": similarity,
            "doc": top_docs,
        })
        
        # Return the DataFrame containing the search results
        return search_results
        
    def compute_word_dendro_ord(self, use_pca=True, n_components=50,
                                clus_method='complete', clus_metric='cosine',
                                max_clus_size=None, verbose=True):
        """
        Computes the dendrogram ordination of words based on their embeddings.
    
        This method creates a hierarchical clustering (dendrogram) of word
        embeddings, optionally reducing the dimensionality of the embeddings
        using PCA. The resulting dendrogram ordination can be used to
        visualize or analyze the relationships between words.
    
        Parameters:
            - use_pca (bool, optional): If True, applies PCA to reduce the
              dimensionality of the word embeddings before clustering. Default
              is True.
            - n_components (int, optional): The number of principal components
              to retain when using PCA. Default is 50.
            - clus_method (str, optional): The clustering method to use for
              hierarchical clustering. Supported methods include those
              available in `scipy.cluster.hierarchy.linkage` (e.g., 'ward',
              'complete', 'single', etc.). Default is 'complete'.
            - clus_metric (str, optional): The distance metric to use for
              clustering. Supported metrics include 'euclidean', 'cosine',
              'cityblock', etc. Default is 'cosine'.
            - max_clus_size (int, optional): The maximum size of clusters to
              allow during clustering. If None, no limit is applied. Default
              is None.
            - verbose (bool, optional): If True, prints progress and
              intermediate information during the computation. Default is True.
        """
        if verbose:
            print("Starting word ordination...")
        
        if use_pca:
            we = self.word_emb_filt_pca[:, 0:n_components]
        else:
            we = self.word_emb_filt
    
        word_dendro_ord = get_dendro_ord(
            we,
            method=clus_method,
            metric=clus_metric,
            max_clus_size=max_clus_size,
            verbose=verbose
        )
    
        self.word_dendro_ord = word_dendro_ord
        self.word_ord_max_clus = max_clus_size
    
    def compute_doc_dendro_ord(self, use_pca=True, n_components=50,
                               clus_method='complete', clus_metric='cosine',
                               max_clus_size=None, verbose=True):
        """
        Computes the dendrogram ordination of documents based on their
        embeddings.
    
        This method creates a hierarchical clustering (dendrogram) of document
        embeddings, optionally reducing the dimensionality of the embeddings
        using PCA. The resulting dendrogram ordination can be used to
        visualize or analyze the relationships between documents.
    
        Parameters:
            - use_pca (bool, optional): If True, applies PCA to reduce the
              dimensionality of the document embeddings before clustering.
              Default is True.
            - n_components (int, optional): The number of principal components
              to retain when using PCA. Default is 50.
            - clus_method (str, optional): The clustering method to use for
              hierarchical clustering. Supported methods include those
              available in `scipy.cluster.hierarchy.linkage` (e.g., 'ward',
              'complete', 'single', etc.). Default is 'complete'.
            - clus_metric (str, optional): The distance metric to use for
              clustering. Supported metrics include 'euclidean', 'cosine',
              'cityblock', etc. Default is 'cosine'.
            - max_clus_size (int, optional): The maximum size of clusters to
              allow during clustering. If None, no limit is applied. Default
              is None.
            - verbose (bool, optional): If True, prints progress and
              intermediate information during the computation. Default is True.
        """
        if verbose:
            print("Starting document ordination...")
        
        if use_pca:
            de = self.doc_emb_pca[:, 0:n_components]
        else:
            de = self.doc_emb
    
        doc_dendro_ord = get_dendro_ord(
            de,
            method=clus_method,
            metric=clus_metric,
            max_clus_size=max_clus_size,
            verbose=verbose
        )

        self.doc_dendro_ord = doc_dendro_ord
        self.doc_ord_max_clus = max_clus_size

    def create_word_dict(self):
        """
        Creates a dictionary mapping words to their indices for the complete
        word list.
        """
        word_list = self.word_list
        word_dict = {word_list[i]: i for i in range(0, len(word_list))}

        self.word_dict = word_dict

    def create_filt_map_dict(self):
        """
        Creates a dictionary mapping words to their indices for the filtered
        word list.
        """
        word_list_filt = self.word_list_filt
        filt_map_dict = {word_list_filt[i]: i
                         for i in range(0, len(word_list_filt))}

        self.filt_map_dict = filt_map_dict
        
    def tokenize_corpus(self, n_jobs=1, chunk_size=1000, verbose=True):
        """
        Tokenizes the processed corpus using parallelization.
    
        Parameters:
            - n_jobs (int, optional): Number of parallel jobs to use. Default
              is 1.
            - chunk_size (int, optional): Number of texts to process in each
              parallel chunk. Default is 1000.
            - verbose (bool, optional): If True, prints progress during
              tokenization. Default is True.
        """    
        corpus = self.corpus
        
        # Define the function for tokenization
        par_function = lambda x: tokenize(x)
        
        # Perform parallel tokenization
        tokenized_corpus = parallelization(corpus, par_function,
                                           n_jobs=n_jobs,
                                           chunk_size=chunk_size,
                                           desc="Tokenizing texts",
                                           verbose=verbose)
    
        # Strip unwanted characters from tokens
        tokenized_corpus = [[word.strip("!@#$%^&*()[]{};:\"',<>?.")
                             for word in sublist]
                            for sublist in tokenized_corpus]
    
        self.tokenized_corpus = tokenized_corpus
    
        if verbose:
            print("Tokenization completed.")

    def create_word_list(self, verbose=True):
        """
        Creates a word list from the tokenized corpus.

        Removes repetitions within documents, counts word occurrences, sorts
        the words by frequency, and creates a mapping from words to indices.

        Parameters:
            - verbose (bool, optional): If True, prints progress during
              processing. Default is True.
        """
        if verbose:
            print("Starting the word list creation.")
        tokenized_corpus = self.tokenized_corpus

        if verbose:
            print("Removing repetitions within documents...")
        # Remove repetitions within documents
        tokenized_corpus_set = [sorted(set(i)) for i in tokenized_corpus]

        if verbose:
            print("Exploding lists and counting occurrences...")
        tokenized_corpus_exp = explode_list(tokenized_corpus_set,
                                            return_indices=False)
        word_list, word_count = count_occurrences(tokenized_corpus_exp)
        word_list = np.array(word_list)
        word_count = np.array(word_count)

        if verbose:
            print("Sorting the list by word frequency...")
        # Sort the list by word frequency
        sorted_indices = word_count.argsort(stable=True)[::-1]
        word_list = word_list[sorted_indices]
        word_count = word_count[sorted_indices]

        if verbose:
            print("Creating word-to-index mapping...")
        word_to_idx = {item: index for index, item in
                       enumerate(word_list)}

        self.word_list = word_list
        self.word_count = word_count
        self.word_to_idx = word_to_idx
        
        if verbose:
            print("Word list creation completed.")

    def compute_tf_idf(self, verbose=True):
        """
        Computes the TF-IDF matrix for the corpus.

        Calculates the term frequency-inverse document frequency (TF-IDF)
        values for words in the corpus.

        Parameters:
            - verbose (bool, optional): If True, prints progress during
              computation. Default is True.
        """
        if verbose:
            print("Starting the TF-IDF computation.")
        tokenized_corpus = self.tokenized_corpus
        word_list = self.word_list

        tf_idf_score = compute_tf_idf(
            tokenized_corpus, word_list, verbose=verbose,
            return_term_norms=True, return_tf_idf=False)
        tf_idf_score = np.array([tf_idf_score[word] for word in word_list])

        self.tf_idf_score = tf_idf_score

        if verbose:
            print("TF-IDF computation completed.")
        
    def create_word_list_filt(self, tf_idf_threshold=0.1):
        """
        Filters the word list based on TF-IDF scores.
        
        Parameters:
            - tf_idf_threshold (float): The threshold for filtering words
              based on their TF-IDF scores. Words with TF-IDF scores below
              this threshold will be filtered out. Default is 0.1.
        """
        word_list = self.word_list
        word_count = self.word_count
        tf_idf_score = self.tf_idf_score
    
        # Filtering words based on the TF-IDF threshold
        filt_idx = tf_idf_score >= tf_idf_threshold
    
        word_list_filt = word_list[filt_idx]
        word_count_filt = word_count[filt_idx]
    
        word_to_idx_fil = {item: index for index, item in
                           enumerate(word_list_filt)}
    
        # Saving results to the object
        self.word_list_filt = word_list_filt
        self.filt_idx = np.where(filt_idx)[0]
        self.word_count_filt = word_count_filt
        self.word_to_idx_fil = word_to_idx_fil
        self.tf_idf_score = tf_idf_score
        self.tf_idf_threshold = tf_idf_threshold

    def create_word_doc_idx(self, verbose=True):
        """
        Creates an index mapping words to the documents they appear in.
    
        This method processes the tokenized corpus and word list to generate
        an index of words to the documents that contain them.
        
        Parameters:
            - verbose (bool, optional): If True, prints progress during the
              encoding process. Default is True.
        """
        if verbose:
            print("Starting creation of word-to-document index...")
        
        # Searching for documents for each token
        tokenized_corpus = self.tokenized_corpus  # Tokenized corpus data
        word_list = self.word_list  # List of words to be indexed
    
        # Call function to search for token occurrences in documents
        word_doc_idx = map_words_to_docs(word_list, tokenized_corpus,
                                         verbose=verbose)
    
        self.word_doc_idx = word_doc_idx
        
        if verbose:
            print("Word-to-document index completed.")

    def create_doc_word_idx(self, verbose=True):
        """
        Creates an index mapping documents to the tokens they contain.
    
        Processes the tokenized corpus and word list to generate an index of
        documents to the tokens present within them.
        
        Parameters:
            - verbose (bool, optional): If True, prints progress during the
              encoding process. Default is True.
        """
        if verbose:
            print("Starting creation of document-to-word index...")
        
        # Searching for tokens for each text
        tokenized_corpus = self.tokenized_corpus  # Tokenized corpus data
        word_list = self.word_list  # List of words to be indexed
    
        # Call function to search for documents that contain each token
        doc_word_idx = map_docs_to_words(tokenized_corpus, word_list,
                                         verbose=verbose)
    
        self.doc_word_idx = doc_word_idx
        
        if verbose:
            print("Document-to-word index completed.")
            
    def encode_corpus(self, n_jobs=1, chunk_size=1000, verbose=True):
        """
        Encodes the processed corpus using biological-like encoding.

        Parameters:
            - n_jobs (int, optional): Number of parallel jobs to use. Default
              is 1.
            - chunk_size (int, optional): Number of texts to process in each
              parallel chunk. Default is 1000.
            - verbose (bool, optional): If True, prints progress during the
              encoding process. Default is True.
        """
        corpus = self.corpus

        par_function = lambda x: aminocode.encode_list(x)
        encoded_corpus = parallelization(corpus, par_function,
                                         n_jobs=n_jobs, chunk_size=chunk_size,
                                         desc="Encoding",
                                         verbose=verbose)

        self.encoded_corpus = np.array(encoded_corpus)

        if verbose:
            print("Encoding process completed.")

        
    def run_sweep(self, n_jobs=1, chunk_size=1000, verbose=True):
        """
        Runs SWeeP on the encoded text.

        Parameters:
            - verbose (bool, optional): If True, prints progress during the
              process. Default is True.
        """
        if verbose:
            print("Starting SWeeP...")
        
        encoded_corpus = self.encoded_corpus
        emb_size = self.emb_size

        mask = [[1,1,0,0,1], [1,1,1,0,0], [1,0,1,0,1], [1,1,0,1,0]]
        proj_size = int(emb_size / 4)

        ntake = sum(mask[0])
        proj = sweep.create_proj_mat(20**ntake, proj_size)

        encoded_corpus_fasta = create_seqrecord_list(encoded_corpus)
        sweeped_corpus = sweep.fasta_to_sweep(
            encoded_corpus_fasta, proj=proj,
            mask=mask,
            n_jobs=n_jobs, chunk_size=chunk_size,
            print_details=False,
            progress_bar=verbose
        )
        sweeped_corpus = np.hstack(sweeped_corpus)

        self.sweeped_corpus = sweeped_corpus
        
        if verbose:
            print("SWeeP completed.")
    
    def create_word_emb_filt(self):
        """
        Filters the word embedding matrix based on the provided indices.
        """
        word_emb = self.word_emb
        filt_idx = self.filt_idx

        word_emb_filt = word_emb[filt_idx]

        self.word_emb_filt = word_emb_filt
       
    def create_pca_coeff(self, verbose=True):
        """
        Creates PCA coefficients from the filtered word embeddings.

        Parameters:
            - verbose (bool, optional): If True, prints progress during the
            process. Default is True.
        """
        if verbose:
            print("Starting PCA...")
        
        word_emb_filt = self.word_emb_filt

        pca_coeff = pca(word_emb_filt)[0]

        self.pca_coeff = pca_coeff
        
        if verbose:
            print("PCA completed.")
         
    def create_word_emb_pca(self, verbose=True):
        """
        Projects word embeddings and filtered word embeddings to PCA space.

        Parameters:
            - verbose (bool, optional): If True, prints progress during the
            process. Default is True.
        """
        if verbose:
            print("Starting PCA projection of word embeddings...")
        
        word_emb = self.word_emb
        pca_coeff = self.pca_coeff
        word_emb_filt = self.word_emb_filt

        word_emb_filt_pca = word_emb_filt @ pca_coeff
        word_emb_pca = word_emb @ pca_coeff

        self.word_emb_filt_pca = word_emb_filt_pca
        self.word_emb_pca = word_emb_pca
        
        if verbose:
            print("PCA projection of word embeddings completed successfully.")

    def create_doc_emb_pca(self, verbose=True):
        """
        Projects document embeddings to PCA space.

        Parameters:
            - verbose (bool, optional): If True, prints progress during the
            process. Default is True.
        """
        if verbose:
            print("Starting PCA projection of document embeddings...")
        
        doc_emb = self.doc_emb
        pca_coeff = self.pca_coeff

        doc_emb_pca = doc_emb @ pca_coeff

        self.doc_emb_pca = doc_emb_pca
        
        if verbose:
            print(("PCA projection of document embeddings completed "
                   "successfully."))