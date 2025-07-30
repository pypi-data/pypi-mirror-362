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
import shutil
import numpy as np
from .. import utils
from ..internal import (load_pickle, save_h5)

def medline_to_html_tm(input_path, output_dir='HTML-TM',
                       html_tm_title='HTML-TM',
                       tf_idf_threshold=0.1,
                       word_ord_max_clus=None,
                       doc_ord_max_clus=None,
                       save_emb=False,
                       force_xml=False,
                       force_word_processor=False,
                       force_temporal_correlation=False,
                       force_html_tm=False,
                       suppress_temporal_correlation=False,
                       suppress_html_tm=False,
                       suppress_html_tm_words=False,
                       suppress_html_tm_texts=False,
                       del_exist_dir=False,
                       only_emb=False,
                       ignore_memory_check=False,
                       n_jobs=1,
                       chunk_size=1000,
                       test_html_tm=False,
                       verbose=True
                       ):
    """
    Converts a PubMed file (Medline) to HTML-TM visualization.

    HTML-TM is created from a corpus – a collection of texts – and is designed
    to assist in exploring the relationships between terms and documents within
    a given dataset. The process begins by selecting a set of top terms and
    finding the nearest 30 correlated terms for each word, sourced from a
    larger list of words and documents. Additionally, an index of the year of
    usage for each word is calculated to provide temporal context. The HTML-TM
    can be accessed through any web browser, facilitating the quick retrieval
    and exploration of related academic content.

    Features:
        - WORDS.html: This file presents a concise list of the top seven
          related terms for each word, along with a hierarchical tree
          displaying the 30 most closely related terms and a corresponding
          list of 20 relevant documents. The structure allows for easy
          exploration of the term-document relationships.
        - TEXTS.html: This second file enables users to search for similar
          articles, making it easier to connect relevant research. The
          numbering system for the papers remains consistent across both files,
          which enhances navigation and allows users to efficiently explore
          the literature.

    Parameters:
        - input_path (str): Path to the Medline dataset file or a directory
          preprocessed by this program.
        - output_dir (str): Directory to store the output. Default:
          'pubmed_processor_result'.
        - html_tm_title (str): Title for the HTML-TM. Default: 'HTML-TM'.
        - tf_idf_threshold (float): The threshold for filtering words based on
          their TF-IDF scores. Words with TF-IDF scores below this threshold
          are filtered out. Default: 0.1.
        - word_ord_max_clus (int or None, optional): The maximum number of
          clusters to allow during word ordering. If None, no limit is applied.
          Default: None.
        - doc_ord_max_clus (int or None, optional): The maximum number of
          clusters to allow during document ordering. If None, no limit is
          applied. Default: None.
        - save_emb (bool): Save embedding vectors in an HDF5 file in the output
          directory. Default: False.
        - force_xml (bool): Force recreating the XML file even if it already
          exists. Default: False.
        - force_word_processor (bool): Force recreating the Word Processor
          file. Default: False.
        - force_temporal_correlation (bool): Force recreating the Temporal
          Correlation file. Default: False.
        - force_html_tm (bool): Force recreating the HTML-TM files.
          Default: False.
        - del_exist_dir (bool): Whether to delete the existing output
          directory if it exists. Default: False.
        - suppress_temporal_correlation (bool): If True, the Temporal
          Correlation process is suppressed, regardless of other settings.
          Default: False.
        - suppress_html_tm (bool): If True, the creation of the HTML-TM file
          is suppressed, regardless of other settings. Default: False.
        - suppress_html_tm_words (bool): If True, the creation of the
          WORDS.html file (part of HTML-TM) is suppressed, regardless of other
          settings. Default: False.
        - suppress_html_tm_texts (bool): If True, the creation of the
          TEXTS.html file (part of HTML-TM) is suppressed, regardless of other
          settings. Default: False.
        - only_emb (bool): If True, only the embedding vectors are generated
          and saved, skipping the Temporal Correlation and HTML-TM creation
          processes. This option automatically sets `save_emb`,
          `suppress_temporal_correlation`, and `suppress_html_tm` to True.
          When `only_emb` is True, it overrides any direct definitions of
          `save_emb`, `suppress_temporal_correlation`, and `suppress_html_tm`,
          regardless of their individual settings. Default: False.
        - ignore_memory_check (bool): If False, checks available memory before
          processing and raises an error if insufficient. If True, skips this
          check. Default is False.
        - n_jobs (int): Number of parallel jobs for processing. Default: 1.
        - chunk_size (int): Chunk size for processing. Default: 1000.
        - test_html_tm (bool): Activates test mode for HTML-TM generation. Use
          this mode to validate the output structure and debug the process
          without requiring the complete dataset or full processing. Default:
          False.
        - verbose (bool): Whether to display verbose output. Default: True.

    Returns:
    - None: The function generates HTML-TM files in the specified output
      directory.
    """
    
    process_count_max = 6
    process_count = 0
    
    if only_emb:
        save_emb = True
        suppress_temporal_correlation = True
        suppress_html_tm = True
    
    if save_emb:
        process_count_max += 1
    if suppress_temporal_correlation:
        process_count_max -= 1
    if suppress_html_tm:
        process_count_max -= 1

    # Defines the length of the dividers used to segment verbose outputs
    # The subtraction ensures there's space for a line break
    # min() is used to prevent exceeding 80 columns in wide terminals
    divider_len = min(os.get_terminal_size().columns - 1, 80)

    ###########################################################################
    # PREPARE
    if verbose:
        print('=' * divider_len)
        process_count += 1
        print(f'[{process_count}/{process_count_max}] PREPARE')
        print('=' * divider_len)
        
    # Check if input_path is a file or directory
    if os.path.isfile(input_path):
        # If it's a file, treat it as a raw Medline dataset
        medline_path = input_path
        is_input_dir = False
    elif os.path.isdir(input_path):
        # If it's a directory, assume it contains preprocessed files
        medline_path = None
        is_input_dir = True
    else:
        sys.tracebacklimit = -1
        raise ValueError("The provided path is not a valid file or directory.")
        
    # Initialize objects
    word_processor = None
    temporal_correlation = None
        
    # Set output names
    xml_file = 'dataset.xml'
    word_processor_file = 'word_processor.pkl'
    temporal_correlation_file = 'temporal_correlation.pkl'
    html_tm_dir = 'html_tm'
    words_txt_file = 'words.txt'
    doc_ids_txt_file = 'doc_ids.txt'
    params_txt_file = 'parameters.txt'
    
    xml_path_out = f'{output_dir}/{xml_file}'
    word_processor_path_out = f'{output_dir}/{word_processor_file}'
    temporal_correlation_path_out = f'{output_dir}/{temporal_correlation_file}'
    html_tm_path_out = f'{output_dir}/{html_tm_dir}'
    if is_input_dir:
        xml_path_in = f'{input_path}/{xml_file}'
        word_processor_path_in = f'{input_path}/{word_processor_file}'
        temporal_correlation_path_in = (
            f'{input_path}/{temporal_correlation_file}')
    else:
        xml_path_in = xml_path_out
        word_processor_path_in = word_processor_path_out
        temporal_correlation_path_in = temporal_correlation_path_out
    
            
    #--------------------------------------------------------------------------
    # Check if the existing output directory should be deleted
    if del_exist_dir:
        if os.path.exists(output_dir):
            shutil.rmtree(output_dir) # Delete the existing directory

    # Create the output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    
    #--------------------------------------------------------------------------
    # Checks if the Word Processor's parameters match expected values.
    # Raises an error if any parameter mismatches; otherwise, confirms success.
    if (os.path.exists(word_processor_path_in) and
        not force_word_processor and not del_exist_dir):
        # Load the Word Processor
        if verbose:
            print('Starting parameter checking...')
            print(('Loading Word Processor from: '
                   f'"{word_processor_path_in}".'))
        word_processor = load_pickle(word_processor_path_in)
        if verbose:
            print("Word Processor loaded successfully.")
            
        # Extract the parameters from the Word Processor
        word_ord_max_clus_wp = word_processor.word_ord_max_clus
        doc_ord_max_clus_wp = word_processor.doc_ord_max_clus
        tf_idf_threshold_wp = word_processor.tf_idf_threshold
        
        # Check if the parameters match the expected values
        if word_ord_max_clus_wp != word_ord_max_clus:
            sys.tracebacklimit = -1
            raise ValueError("The input Word Processor is configured "
                             "with a different value for 'word_ord_max_clus'. "
                             "To run with a new value, the parameter "
                             "'force_word_processor' can be used.")
        if doc_ord_max_clus_wp != doc_ord_max_clus:
            sys.tracebacklimit = -1
            raise ValueError("The input Word Processor is configured "
                             "with a different value for 'doc_ord_max_clus'. "
                             "To run with a new value, the parameter "
                             "'force_word_processor' can be used.")
        if tf_idf_threshold_wp != tf_idf_threshold:
            sys.tracebacklimit = -1
            raise ValueError("The input Word Processor is configured "
                             "with a different value for 'tf_idf_threshold'. "
                             "To run with a new value, the parameter "
                             "'force_word_processor' can be used.")
        
        # If no issues are found
        if verbose:
            print("No issues found. All parameters match the expected values.")
    
    #--------------------------------------------------------------------------
    if verbose:
        print("Everything is ready to continue.")
    
    ###########################################################################
    # CONVERT MEDLINE TO XML
    if verbose:
        print('=' * divider_len)
        process_count += 1
        print(f'[{process_count}/{process_count_max}] CONVERT MEDLINE TO XML')
        print('=' * divider_len)
        
    if is_input_dir and not os.path.exists(xml_path_out) and not force_xml:
        # Copy the XML file from the input path to the output path
        if verbose:
            print(f'Copying XML file from "{xml_path_in}" to '
                  f'"{xml_path_out}".')
        shutil.copy(xml_path_in, xml_path_out)
        # Update the input path to point to the copied file
        xml_path_in = xml_path_out
        if verbose:
            print("XML file copied successfully.")
    elif not os.path.exists(xml_path_out) or force_xml:
        utils.medline_to_xml(medline_path, xml_path_out, verbose=verbose)
        xml_path_in = xml_path_out
        if verbose:
            print(f'XML saved at {xml_path_out}.')
    else:
        if verbose:
            print(f'The file "{xml_file}" already exists at "{xml_path_out}".')

    ###########################################################################
    # CREATE WORD PROCESSOR
    if verbose:
        print('=' * divider_len)
        process_count += 1
        print(f'[{process_count}/{process_count_max}] CREATE WORD PROCESSOR')
        print('=' * divider_len)
    
    if (is_input_dir and not os.path.exists(word_processor_path_out) and not
        force_word_processor):
        # Copy the Word Processor file from the input path to the output path
        if verbose:
            print('Copying Word Processor file from '
                  f'"{word_processor_path_in}" to '
                  f'"{word_processor_path_out}".')
        shutil.copy(word_processor_path_in, word_processor_path_out)
        # Update the input path to point to the copied file
        word_processor_path_in = word_processor_path_out
        if verbose:
            print("Word Processor file copied successfully.")
    elif (not os.path.exists(word_processor_path_out) or
        force_word_processor):
        word_processor = utils.xml_to_word_processor(
            xml_path_in,
            word_processor_path_out,
            tf_idf_threshold=tf_idf_threshold,
            word_ord_max_clus=word_ord_max_clus,
            doc_ord_max_clus=doc_ord_max_clus,
            ignore_memory_check=ignore_memory_check,
            n_jobs=n_jobs,
            chunk_size=chunk_size,
            verbose=verbose
        )
        word_processor_path_in = word_processor_path_out
        if verbose:
            print(f'Word Processor saved at "{word_processor_path_out}".')
    else:
        if verbose:
            print(f'The file "{word_processor_file}" already exists at '
                  f'"{word_processor_path_out}".')
    
    ###########################################################################
    # SAVE TXT FILES
    if verbose:
        print('=' * divider_len)
        process_count += 1
        print(f'[{process_count}/{process_count_max}] SAVE TXT FILES')
        print('=' * divider_len)
    
    params_path = f'{output_dir}/{params_txt_file}'    
    if (not os.path.exists(params_path) or force_word_processor):
        if verbose:
            print('Starting process to save parameters file...')
            print('Extracting parameters from the Word Processor...')
        
        if not word_processor:
            # Load the Word Processor
            if verbose:
                print(('Loading Word Processor from: '
                       f'"{word_processor_path_in}".'))
            word_processor = load_pickle(word_processor_path_in)
            if verbose:
                print("Word Processor loaded successfully.")
        
        # Extract the parameters from the Word Processor
        word_ord_max_clus_wp = word_processor.word_ord_max_clus
        doc_ord_max_clus_wp = word_processor.doc_ord_max_clus
        tf_idf_threshold_wp = word_processor.tf_idf_threshold
    
        if verbose:
            print('Saving parameters...')
        
        with open(params_path, 'w') as f:
            f.write(f"word_ord_max_clus: {word_ord_max_clus_wp}\n")
            f.write(f"doc_ord_max_clus: {doc_ord_max_clus_wp}\n")
            f.write(f"tf_idf_threshold: {tf_idf_threshold_wp}\n")
        
        if verbose:
            print(f'Parameters saved successfully at: "{params_path}".')
    else:
        if verbose:
            print((f'The file "{params_txt_file}" already exists at '
                   f'"{params_path}".'))
    
    if verbose:
        print('-' * divider_len)
    
    # Define word list path
    words_path = f'{output_dir}/{words_txt_file}'
    if (not os.path.exists(words_path) or force_word_processor):
        if verbose:
            print('Starting process to save word list file...')
            print('Extracting words from the Word Processor...')
        
        if not word_processor:
            # Load the Word Processor
            if verbose:
                print(('Loading Word Processor from: '
                       f'"{word_processor_path_in}".'))
            word_processor = load_pickle(word_processor_path_in)
            if verbose:
                print("Word Processor loaded successfully.")
                
        words = word_processor.word_list_filt[word_processor.word_dendro_ord]
        
        if verbose:
            print(f'Words extracted successfully. Total words: {len(words)}.')
            print('Saving words to file...')
        
        with open(words_path, 'w', encoding='utf-8') as f:
            np.savetxt(f, words, fmt='%s')
    
        if verbose:
            print(f'Word list saved successfully at: "{words_path}".')
    else:
        if verbose:
            print((f'The file "{words_txt_file}" already exists at '
                   f'"{words_path}".'))
    
    if verbose:
        print('-' * divider_len)
    
    # Define document ID list path
    doc_ids_path = f'{output_dir}/{doc_ids_txt_file}'
    if (not os.path.exists(doc_ids_path) or force_word_processor):
        if verbose:
            print('Starting process to save document identifier file...')
            print('Extracting document IDs from the Word Processor...')
        
        if not word_processor:
            # Load the Word Processor
            if verbose:
                print(('Loading Word Processor from: '
                       f'"{word_processor_path_in}".'))
            word_processor = load_pickle(word_processor_path_in)
            if verbose:
                print("Word Processor loaded successfully.")
        
        doc_ids = word_processor.corpus_ids[word_processor.doc_dendro_ord]
        
        if verbose:
            print(('Document IDs extracted successfully. Total document IDs: '
                   f'{len(doc_ids)}.'))
            print('Saving document IDs to file...')
        
        with open(doc_ids_path, 'w', encoding='utf-8') as f:
            np.savetxt(f, doc_ids, fmt='%s')
        
        if verbose:
            print(('List of document IDs saved successfully at: '
                   f'"{doc_ids_path}".'))
    else:
        if verbose:
            print((f'The file "{doc_ids_txt_file}" already exists at '
                   f'"{doc_ids_path}".'))

    ###########################################################################
    # RUN TEMPORAL CORRELATION
    if (is_input_dir and not os.path.exists(temporal_correlation_path_out) and
        not force_temporal_correlation):
        # Copy the Temporal Correlation file from the input path to the output
        # path
        if verbose:
            print('Copying Temporal Correlation file from '
                  f'"{temporal_correlation_path_in}" to '
                  f'"{temporal_correlation_path_out}".')
        shutil.copy(temporal_correlation_path_in,
                    temporal_correlation_path_out)
        # Update the input path to point to the copied file
        temporal_correlation_path_in = temporal_correlation_path_out
        if verbose:
            print("Temporal Correlation file copied successfully.")
    elif not suppress_temporal_correlation:
        if verbose:
            print('=' * divider_len)
            process_count += 1
            print((f'[{process_count}/{process_count_max}] RUN TEMPORAL '
                   'CORRELATION'))
            print('=' * divider_len)
        if (not os.path.exists(temporal_correlation_path_out) or
            force_temporal_correlation):
            temporal_correlation = utils.xml_to_temporal_correlation(
                xml_path_in,
                word_processor or word_processor_path_in,
                temporal_correlation_path_out,
                verbose=verbose
            )
            temporal_correlation_path_in = temporal_correlation_path_out
            if verbose:
                print('Temporal Correlation saved at '
                      f'"{temporal_correlation_path_out}".')
        else:
            if verbose:
                print(f'The file "{temporal_correlation_file}" already '
                      f'exists at "{temporal_correlation_path_out}".')
            
    ###########################################################################
    # CREATE HTML-TM
    if not suppress_html_tm:
        if verbose:
            print('=' * divider_len)
            process_count += 1
            print(f'[{process_count}/{process_count_max}] CREATE HTML-TM')
            print('=' * divider_len)
            
        if not os.path.exists(html_tm_path_out) or force_html_tm:
            # Create HTML-TM
            utils.create_html_tm(
                xml_path_in,
                word_processor or word_processor_path_in,
                temporal_correlation or temporal_correlation_path_in,
                html_tm_path_out, html_tm_title=html_tm_title,
                suppress_html_tm_words=suppress_html_tm_words,
                suppress_html_tm_texts=suppress_html_tm_texts,
                del_exist_dir=True,
                n_jobs=n_jobs, chunk_size=chunk_size,
                verbose=verbose,
                test_mode=test_html_tm
            )
            if verbose:
                print(f'HTML-TM saved at {html_tm_path_out}.')
        else:
            if verbose:
                print(f'The HTML-TM directory "{html_tm_dir}" already exists '
                      f'at "{html_tm_path_out}".')
    
    ###########################################################################
    # SAVE EMBEDDINGS
    if save_emb:
        if verbose:
            print('=' * divider_len)
            process_count += 1
            print(f'[{process_count}/{process_count_max}] SAVE EMBEDDINGS')
            print('=' * divider_len)
        
        if not word_processor:
            # Load the Word Processor
            if verbose:
                print(('Loading Word Processor from: '
                       f'"{word_processor_path_in}".'))
            word_processor = load_pickle(word_processor_path_in)
            if verbose:
                print("Word Processor loaded successfully.")
        
        # Save the embeddings into an HDF5 file
        if verbose:
            print("Saving embeddings in HDF5 format...")
        # Define the path to the file where word embeddings will be saved
        word_emb_file = f'{output_dir}/embeddings.h5'
        # Retrieve the dendrogram order for words and documents  
        word_dendro_ord = word_processor.word_dendro_ord
        doc_dendro_ord = word_processor.doc_dendro_ord
        save_h5({
            'words': word_processor.word_list,
            'doc_ids': word_processor.corpus_ids[doc_dendro_ord],
            'word_emb': word_processor.word_emb,
            'doc_emb': word_processor.doc_emb[doc_dendro_ord],
            'pca_coeff': word_processor.pca_coeff,
            'word_filt_idx': word_processor.filt_idx[word_dendro_ord]
        }, word_emb_file)
        if verbose:
            print(f'Embeddings saved successfully to: "{word_emb_file}".')