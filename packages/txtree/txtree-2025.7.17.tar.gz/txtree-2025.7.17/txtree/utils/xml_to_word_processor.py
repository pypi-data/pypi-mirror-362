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
import xml.etree.ElementTree as ET
import os
import sys
from ..WordProcessor import WordProcessor
from ..internal import (save_pickle, estimate_scipy_linkage_mem,
                        estimate_scipy_linkage_n,
                        get_available_mem)

def xml_to_word_processor(xml="dataset.xml",
                          output_path=None,
                          tf_idf_threshold=0.1,
                          word_ord_max_clus=None,
                          doc_ord_max_clus=None,
                          ignore_memory_check=False,
                          n_jobs=1, chunk_size=1000,
                          verbose=True):
    """
    Generates a WordProcessor object from an XML file and optionally saves it
    to a file.

    Parameters:
        - xml (str): Path to the dataset XML file.
        - output_path (str or None): Path to the file where the WordProcessor
          will be saved. If None, the file will not be saved. Defaults to None.
        - tf_idf_threshold (float): The threshold for filtering words based on
          their TF-IDF scores. Words with TF-IDF scores below this threshold
          will be filtered out. Default is 0.1.
        - word_ord_max_clus (int or None, optional): The maximum number of
          clusters to allow during word ordination. If None, no limit is
          applied. Default is None.
        - doc_ord_max_clus (int or None, optional): The maximum number of
          clusters to allow during document ordination. If None, no limit is
          applied. Default is None.
        - ignore_memory_check (bool): If False, checks available memory before
          processing and raises an error if insufficient. If True, skips this
          check. Default is False.
        - n_jobs (int): Number of jobs to use for processing. Defaults to 1.
        - chunk_size (int): The size of chunks to process at a time.
          Defaults to 1000.
        - verbose (bool): Whether to print progress messages. Defaults to True.

    Returns:
        - WordProcessor: The created WordProcessor object.
    """
    process_count_max = 7
    process_count = 0
    
    # Defines the length of the dividers used to segment verbose outputs
    # The subtraction ensures there's space for a line break
    # min() is used to prevent exceeding 80 columns in wide terminals
    divider_len = min(os.get_terminal_size().columns - 1, 80)
    
    # Prepare dataset iteratively
    if verbose:
        process_count += 1
        process_name = 'Prepare dataset'
        print(f'[{process_count}/{process_count_max}] {process_name}')
        print('-' * divider_len)
    
    title_list = []
    abstract_list = []
    publication_year_list = []
    pmid_list = []
    
    for event, record in ET.iterparse(xml, events=("start", "end")):
        if event == "end" and record.tag == "entry":
            title = record.find("title")
            abstract = record.find("abstract")
            publication_year = record.find("publication_year")
            pmid = record.find("pmid")
    
            title_list.append(title.text if title is not None else '')
            abstract_list.append(abstract.text if abstract is not None else '')
            publication_year_list.append(publication_year.text
                                         if publication_year is not None
                                         else '')
            pmid_list.append(pmid.text if pmid is not None else '')
    
            record.clear()  # Clear the record to free memory
    
    corpus = [f"{ti} {ab}" for ti, ab in zip(title_list, abstract_list)]
    corpus = np.array(corpus)
    
    corpus_len = np.array([len(i) for i in corpus])
    corpus_fil = corpus_len >= 5
    
    corpus = corpus[corpus_fil]
    title_list = np.array(title_list)[corpus_fil]
    abstract_list = np.array(abstract_list)[corpus_fil]
    publication_year_list = np.array(publication_year_list)[corpus_fil]
    pmid_list = np.array(pmid_list)[corpus_fil]
    
    corpus_len = len(corpus)
    
    # Check if doc_ord_max_clus is greater than the total number of documents
    # in the corpus
    if doc_ord_max_clus and doc_ord_max_clus > corpus_len:
        sys.tracebacklimit = -1
        raise ValueError(f"doc_ord_max_clus ({doc_ord_max_clus}) cannot be "
                         "greater than the total number of documents in "
                         f"corpus ({corpus_len}).")
    
    if not ignore_memory_check:
        # Estimate the memory required for document ordination by hierarchical
        # clustering and compare it with the available system memory.
        # If the available memory is insufficient, calculate the maximum
        # recommended value for 'doc_ord_max_clus' based on the available
        # memory and raise a MemoryError with a detailed message suggesting
        # how to adjust the parameter to avoid memory overload.
        #
        # Memory required for hierarchical clustering
        linkage_mem = estimate_scipy_linkage_mem(corpus_len * 0.95)
        # Available system memory
        available_mem = get_available_mem()
        esti_n = estimate_scipy_linkage_n(available_mem)
        if (available_mem < linkage_mem and
            (not doc_ord_max_clus  or doc_ord_max_clus > esti_n)):
            sys.tracebacklimit = -1
            raise MemoryError(
                "Insufficient memory to process the input corpus due to its "
                "size, preventing document ordination by hierarchical "
                "clustering.\n"
                f"Required: {linkage_mem:.2f} GB | "
                f"Available: {available_mem:.2f} GB.\n\n"
                "Possible solution:\n"
                "Set a value for 'doc_ord_max_clus'. Given the available "
                f"memory, it should be at most {esti_n} (preferably lower to "
                "avoid full memory usage).\n\n"
                "Note: It may also be necessary to define a value for "
                "'word_ord_max_clus'. However, an estimate for this "
                "parameter is not possible at this stage."
            )
    
    # Initialize WordProcessor
    if verbose:
        process_count += 1
        process_name = 'Initialize Word Processor'
        print(f'[{process_count}/{process_count_max}] {process_name}')
        print('-' * divider_len)
    word_processor = WordProcessor()
    word_processor.corpus = corpus
    word_processor.corpus_ids = pmid_list
    word_processor.verbose_start = '\t' if verbose else None
    
    # Prepare WordProcessor
    if verbose:
        process_count += 1
        process_name = 'Prepare Word Processor'
        print(f'[{process_count}/{process_count_max}] {process_name}')
        print('-' * divider_len)
    
    # Part 1: Initialization
    if verbose:
        print("Initial preparation")
        print('-' * divider_len)
    word_processor.process_corpus(init_prep=True, vectorize=False,
                                  tf_idf_threshold=tf_idf_threshold,
                                  n_jobs=n_jobs, chunk_size=chunk_size,
                                  verbose=verbose)
    
    word_list_len = len(word_processor.word_list_filt)
    
    # Check if word_ord_max_clus is greater than the word_list_len
    if word_ord_max_clus and word_ord_max_clus > word_list_len:
        sys.tracebacklimit = -1
        raise ValueError(f"word_ord_max_clus ({word_ord_max_clus}) cannot be "
                         "greater than the word list length "
                         f"({word_list_len}). The word list length can be "
                         "reduced by increasing the 'tf_idf_threshold', which "
                         "filters out words with lower TF-IDF scores.")
        
    if verbose:
        print("Initial preparation completed. Word list length: "
              f"{word_list_len}.")
    
    # Part 2: Vectorization
    if verbose:
        print('-' * divider_len)
        print("Vectorization")
        print('-' * divider_len)
    word_processor.process_corpus(init_prep=False, vectorize=True,
                                  n_jobs=n_jobs, chunk_size=chunk_size,
                                  verbose=verbose)
    
    if not ignore_memory_check:
        # Estimate the memory required for word ordination by hierarchical
        # clustering and compare it with the available system memory.
        # If the available memory is insufficient, calculate the maximum
        # recommended value for 'word_ord_max_clus' based on the available
        # memory and raise a MemoryError with a detailed message suggesting
        # how to adjust the parameter to avoid memory overload.
        #
        # Memory required for hierarchical clustering
        linkage_mem = estimate_scipy_linkage_mem(word_list_len)
        # Available system memory
        available_mem = get_available_mem()
        esti_n = estimate_scipy_linkage_n(available_mem)
        if (available_mem < linkage_mem and
            (not word_ord_max_clus  or word_ord_max_clus > esti_n)):
            sys.tracebacklimit = -1
            raise MemoryError(
                "Insufficient memory to process the word list due to its "
                "size, preventing word ordination by hierarchical clustering."
                "\n"
                f"Required: {linkage_mem:.2f} GB | "
                f"Available: {available_mem:.2f} GB.\n\n"
                "Possible solutions:\n"
                "1. Set a value for 'word_ord_max_clus'. Given the available "
                f"memory, it should be at most {esti_n} (preferably lower to "
                "avoid full memory usage).\n"
                "2. Increase 'tf_idf_threshold' to reduce the word list size "
                "by filtering with a higher TF-IDF value."
            )
    
    # Run embedding
    if verbose:
        process_count += 1
        process_name = 'Run embedding'
        print('-' * divider_len)
        print(f'[{process_count}/{process_count_max}] {process_name}')
        print('-' * divider_len)
    word_processor.create_word_emb(n_jobs=n_jobs, chunk_size=chunk_size,
                                  verbose=verbose)
    word_processor.create_doc_emb(n_jobs=n_jobs, chunk_size=chunk_size,
                                  verbose=verbose)
    
    # Apply PCA
    if verbose:
        process_count += 1
        process_name = 'Apply PCA'
        print('-' * divider_len)
        print(f'[{process_count}/{process_count_max}] {process_name}')
        print('-' * divider_len)
    word_processor.run_pca(verbose=verbose)
    
    # Compute word dendrogrammatic ordination
    if verbose:
        process_count += 1
        process_name = 'Compute word dendrogrammatic ordination'
        print('-' * divider_len)
        print(f'[{process_count}/{process_count_max}] {process_name}')
        print('-' * divider_len)
    word_processor.compute_word_dendro_ord(max_clus_size=word_ord_max_clus,
                                           verbose=verbose)
    
    # Compute document dendrogrammatic ordination
    if verbose:
        process_count += 1
        process_name = 'Compute document dendrogrammatic ordination'
        print('-' * divider_len)
        print(f'[{process_count}/{process_count_max}] {process_name}')
        print('-' * divider_len)
    word_processor.compute_doc_dendro_ord(max_clus_size=doc_ord_max_clus,
                                          verbose=verbose)
    
    # Save the word_processor if output_path is not None
    if output_path:
        save_pickle(word_processor, output_path)
        
    return word_processor