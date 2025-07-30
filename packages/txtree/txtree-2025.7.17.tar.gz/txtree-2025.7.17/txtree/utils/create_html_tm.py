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
import os
import matplotlib
import matplotlib.pyplot as plt
from tqdm import tqdm
import shutil
import math
import sys
from joblib import Parallel, delayed
from ete3 import TreeStyle
import xml.etree.ElementTree as ET
from PyQt5.QtCore import qInstallMessageHandler
from ..internal import (load_pickle, fuzzy_moving_average)
from ..internal.htmltools import (HTMLTableCreator, HTMLSVGCreator)

def create_html_tm(xml, word_processor, temporal_correlation, output_dir,
                   html_tm_title='HTML-TM',
                   suppress_html_tm_words=False,
                   suppress_html_tm_texts=False,
                   del_exist_dir=False,
                   n_jobs=1, chunk_size=1000,
                   verbose=True, test_mode=False):
    """
    Generate an HTML-TM (Text Mining) for exploring relationships between
    terms and documents in a given corpus.
    
    This function processes the provided dataset, extracts top terms, computes
    correlations between terms and related documents, and calculates the year
    of usage for each term to provide temporal context. It generates two HTML
    files: WORDS.html, which displays related terms and documents, and
    TEXTS.html, which allows users to explore similar articles based on the
    relationships between terms and documents. The HTML-TM offers a useful
    interface for academic content retrieval via a web browser.

    Parameters:
        - xml (str): Path to the XML file containing the dataset of
          documents.
        - word_processor (object or str): A WordProcessor object containing a 
          tokenized corpus and word list, or a string path to a pickle file 
          containing the WordProcessor object.
        - temporal_correlation (tuple or str): The `temporal_correlation`
          tuple result or a string path to a pickle file containing the saved
          tuple.
        - output_dir (str): The directory path where the generated HTML files
          and assets will be saved.
        - html_tm_title (str): The title to be displayed in the generated HTML
          pages. Default to 'HTML-TM'.
        - suppress_html_tm_words (bool): If True, the creation of the
          WORDS.html file (part of HTML-TM) is suppressed. Default: False.
        - suppress_html_tm_texts (bool): If True, the creation of the
          TEXTS.html file (part of HTML-TM) is suppressed. Default: False.
        - del_exist_dir (bool, optional): If True, deletes the existing output
          directory before generating new files. Defaults to False.
        - n_jobs (int, optional): The number of parallel jobs for processing
          the dataset. Defaults to 1.
        - chunk_size (int, optional): The number of words processed in each
          chunk for efficient computation. Defaults to 1000.
        - verbose (bool, optional): If True, enables progress messages to
          inform the user about the process. Defaults to True.
        - test_mode (bool, optional): If True, processes only a sample of
          the dataset for testing purposes. Defaults to False.
    
    Returns:
        - None: This function generates HTML files and saves them to the
          specified output directory.    
    """
    
    # Configure font type for SVG rendering
    # Set the font type to 'none' for SVG outputs, which ensures that text is
    # rendered as paths instead of using fonts
    plt.rcParams['svg.fonttype'] = 'none'
    
    process_count_max = 4  # Set the maximum number of processes
    process_count = 0      # Initialize the process count
    
    if suppress_html_tm_words:
        process_count_max -= 1
    if suppress_html_tm_texts:
        process_count_max -= 1
    
    if del_exist_dir:
        # If 'del_exist_dir' is True, try to remove the existing output
        # directory
        try:
            shutil.rmtree(output_dir)
        except FileNotFoundError:
            pass  # If the directory is not found, do nothing
    
    # Normalize paths to use '/' as separator
    xml = str(xml).replace(os.sep, '/')
    if isinstance(word_processor, str):
        word_processor = str(word_processor).replace(os.sep, '/')
    if isinstance(temporal_correlation, str):
        temporal_correlation = str(temporal_correlation).replace(os.sep, '/')
    output_dir = str(output_dir).replace(os.sep, '/')
    
    # Define paths for various output directories
    output_dir_data = f"{output_dir}/DATA"
    output_dir_assets = f"{output_dir_data}/ASSETS"
    output_dir_assets_rel = "DATA/ASSETS"
    output_dir_assets_rel_2 = "ASSETS"
    output_dir_tree = f"{output_dir_data}/WORD_TREE"
    output_dir_year_plot = f"{output_dir_data}/YEAR_PLOT"
    output_dir_html_tree = f"{output_dir_data}/HTML_WORD_TREE"
    output_dir_html_years = f"{output_dir_data}/HTML_YEAR_PLOT"
    output_dir_html_word_docs = f"{output_dir_data}/HTML_WORD_DOCS"
    output_dir_html_doc_docs = f"{output_dir_data}/HTML_DOC_DOCS"
    
    # Create the necessary directories if they don't exist
    os.makedirs(output_dir, exist_ok=True)
    os.makedirs(output_dir_data, exist_ok=True)
    os.makedirs(output_dir_assets, exist_ok=True)
    os.makedirs(output_dir_tree, exist_ok=True)
    os.makedirs(output_dir_year_plot, exist_ok=True)
    os.makedirs(output_dir_html_tree, exist_ok=True)
    os.makedirs(output_dir_html_years, exist_ok=True)
    os.makedirs(output_dir_html_word_docs, exist_ok=True)
    os.makedirs(output_dir_html_doc_docs, exist_ok=True)
    
    ###########################################################################
    
    process_count += 1  # Increment the process count
    process_name = 'Preparing dataset...'  # Name of the current process
    if verbose:
        print(f'[{process_count}/{process_count_max}] {process_name}')
    
    # Initialize lists to store parsed data
    title_list = []
    abstract_list = []
    year_list = []
    pmid_list = []
    
    # Iterate through the XML file and parse relevant data
    for event, record in ET.iterparse(xml, events=("start", "end")):
        if event == "end" and record.tag == "entry":
            # Extract title, abstract, publication year, and pmid for each
            # entry
            title = record.find("title")
            abstract = record.find("abstract")
            publication_year = record.find("publication_year")
            pmid = record.find("pmid")
    
            # Append extracted data to the corresponding lists, use empty
            # string if the field is missing
            title_list.append(title.text if title is not None else '')
            abstract_list.append(abstract.text if abstract is not None else '')
            year_list.append(publication_year.text
                             if publication_year is not None
                             else '')
            pmid_list.append(pmid.text if pmid is not None else '')
    
            # Clear the record to free memory
            record.clear()
    
    # Create a corpus combining titles and abstracts
    corpus = [f"{ti} {ab}" for ti, ab in zip(title_list, abstract_list)]
    
    # Filter out entries where the abstract is empty
    corpus_len = np.array([len(i) for i in corpus])
    corpus_fil = corpus_len >= 5  # Filter for non-empty abstracts
    
    # Apply the filter to all lists
    title_list = np.array(title_list)[corpus_fil]
    abstract_list = np.array(abstract_list)[corpus_fil]
    year_list = np.array(year_list)[corpus_fil]
    pmid_list = np.array(pmid_list)[corpus_fil]
    corpus = np.array(corpus)[corpus_fil]
    
    # Extract the publication year as an integer array
    year_list = [int(i[0:4]) for i in year_list]
    year_list = np.array(year_list)
    
    # Create links to the PubMed page for each article using the pmid
    link_list = [HTMLTableCreator.add_site_link(i,
                                    f'https://pubmed.ncbi.nlm.nih.gov/{i}',
                                    open_in_new_tab=True) for i in pmid_list]
    link_list = np.array(link_list)
    
    # Bold the titles and combine them with their abstracts
    title_list_b = [f'<b>{title_list[i]}</b>' for i in range(len(title_list))]
    title_list_b = np.array(title_list_b)
    title_abstract_list = [f'{title_list_b[i]} {abstract_list[i]}'
                           for i in range(len(title_list))]
    title_abstract_list = np.array(title_abstract_list)
    
    # Create an array combining year and corresponding link
    year_link_list = [[year_list[i], link_list[i]]
                      for i in range(len(title_list))]
    year_link_list = np.array(year_link_list)
    
    ###########################################################################
    
    # Load the Temporal Correlation data from the specified file path
    if isinstance(temporal_correlation, str):
        if verbose:
            print('Loading Temporal Correlation from: '
                  f'"{temporal_correlation}".')
        temporal_correlation = load_pickle(temporal_correlation)
        if verbose:
            print("Word Processor loaded successfully.")
    
    # Load the Word Processor from the specified file path if necessary
    if isinstance(word_processor, str):
        if verbose:
            print(f'Loading Word Processor from: "{word_processor}".')
        word_processor = load_pickle(word_processor)
        if verbose:
            print("Word Processor loaded successfully.")
    
    ###########################################################################
    
    process_count += 1  # Increment the process count
    process_name = 'Apply dendrogrammatic ordination...'
    if verbose:
        print(f'[{process_count}/{process_count_max}] {process_name}')
    
    # Retrieve word and document dendrogram orders from the Word Processor
    word_dendro_ord = word_processor.word_dendro_ord
    doc_dendro_ord = word_processor.doc_dendro_ord
    
    # Filter and order the word list and word count based on the dendrogram
    # order
    word_list = word_processor.word_list_filt[word_dendro_ord]
    word_count = word_processor.word_count_filt[word_dendro_ord]
    
    # Process the corpus based on the document dendrogram order
    processed_corpus = np.array(word_processor.corpus)[doc_dendro_ord]
    
    # Reorder other data arrays based on the document dendrogram order
    title_list = title_list[doc_dendro_ord]
    abstract_list = abstract_list[doc_dendro_ord]
    year_list = year_list[doc_dendro_ord]
    pmid_list = pmid_list[doc_dendro_ord]
    corpus = corpus[doc_dendro_ord]
    link_list = link_list[doc_dendro_ord]
    title_list_b = title_list_b[doc_dendro_ord]
    title_abstract_list = title_abstract_list[doc_dendro_ord]
    year_link_list = year_link_list[doc_dendro_ord]
    
    # Convert the temporary correlation data to a list for easier manipulation
    temporal_correlation = list(temporal_correlation)
    # Reorder the correlation data according to the word dendrogram order
    temporal_correlation[2] = temporal_correlation[2][word_dendro_ord]
    temporal_correlation[3] = temporal_correlation[3][word_dendro_ord]
    
    ###########################################################################

    # Save the CSS, JS, and help files
    HTMLTableCreator.save_style(f'{output_dir_assets}')
    HTMLTableCreator.save_script(f'{output_dir_assets}')
    HTMLSVGCreator.generate_js(f'{output_dir_assets}/svg_page.js')
    
    # Get length of the processed corpus
    processed_corpus_len = len(processed_corpus)
    
    # Set the number of top related documents for each word
    k_top = 20
    
    # Create a dictionary to map the dendrogram order of documents
    doc_dendro_ord_dict = {doc_dendro_ord[i]: i
                           for i in range(0, processed_corpus_len)}
    
    # Set JavaScript file name
    script_file_name = 'table.js'
    
    ###########################################################################
    
    if not suppress_html_tm_words:
        # Increment process count and set the current process name
        process_count += 1
        process_name = 'Creating WORDS.html'
        if verbose:
            print(f'[{process_count}/{process_count_max}] {process_name}')
        
        # Define columns for the HTML table
        columns = [
            "#",
            "Word",
            "Occ.",
            "Related Words",
            "Related Doc.",
            "Word Tree",
            "Year Plot"
        ]
        columns = [f'<div class="no-wrap">{i}</div>' for i in columns]
        
        # Create an object to generate the HTML for words-related information
        chtml = HTMLTableCreator(
            title=f'{html_tm_title} - Words',
            style_dir_rel=f'{output_dir_assets_rel}',
            script_dir_rel=f'{output_dir_assets_rel}',
            help_search_bar_file_rel=(f'{output_dir_assets_rel}/'
                                      'help_search_bar_words.html'),
            about_file_rel=f'{output_dir_assets_rel}/about_words.html',
            columns=columns
        )
        
        # Define columns for the HTML that will list documents related to
        # words
        html_doc_columns = [
            "#",
            "Rank",
            "Similarity",
            "Title + Abs.",
            "Year",
            "PMID"
        ]
        html_doc_columns = [f'<div class="no-wrap">{i}</div>'
                            for i in html_doc_columns]
        
        # Prepare data for generating the WORDS.html file
        if test_mode:
            # Select the first 20 words from the word list
            max_i = 20
        else:
            # Get the total number of words in the list
            max_i = len(word_list)
        
        # Calculate the number of "chunks" the word list will be split into
        chunks = math.ceil(max_i / chunk_size)
        range_s = range(0, chunks)
        
        # Generate indexes for the "chunks", splitting the word list into
        # smaller pieces
        chunk_index = (np.tile(chunk_size, (chunks, 2)) *
                         np.array([list(range(0, chunks)),
                                   list(range(1, chunks + 1))]).T +
                         np.concatenate((np.ones((chunks, 1)),
                                         np.zeros((chunks, 1))), axis=1))
        
        # Adjust the last chunk's ending index to the maximum number of words
        chunk_index[-1, 1] = max_i
        
        # Adjust indexes to be zero-based (starting from 0)
        chunk_index = chunk_index - 1
    
        def run_word_html_chunk(i, progress_bar):
            chunk_result = []
            
            # Get the range of indexes for the current chunk
            index_range = range(int(chunk_index[i, 0]),
                                int(chunk_index[i, 1]) + 1)
            index_range = np.array(list(index_range))
            
            # Loop through each word in the chunk
            for i in range(len(index_range)):
                index = index_range[i]
                xword = word_list[index]
                
                # Search for related words and generate the word tree
                related_words, word_tree = word_processor.search_words(
                    xword, 30, return_dedro=True)
                related_words = related_words[0:10]
                
                # Search for documents related to the word
                search_results = word_processor.search_docs(
                    xword, k_top=k_top, n_components=50, use_pca=True)
                
                # Map document indexes to their corresponding dendrogram order
                search_results.loc[:, "doc_idx"] = [
                    doc_dendro_ord_dict[j] for j in search_results.doc_idx]
                
                # Lists to store additional data and titles/abstracts
                additional_data = []
                title_abstract = []
                
                # Get the indexes of the top k documents from the search
                # results
                result_idx = list(search_results.doc_idx[0:k_top])
                
                # Retrieve additional data (year and PMID) corresponding to
                # the document indexes
                additional_data = year_link_list[result_idx]
                
                # Convert the additional data into a DataFrame and merge it
                # with the search results
                additional_data = pd.DataFrame(additional_data,
                                               columns=['year', 'pmid'])
                search_results = pd.concat([search_results, additional_data],
                                           axis=1)
                
                # Remove the 'doc' column and replace it with titles and
                # abstracts
                search_results.drop('doc', axis=1, inplace=True)
                title_abstract = title_abstract_list[result_idx]
                search_results.insert(3, 'title_abstract', title_abstract)
                
                # Ensures the 'similarity' column is treated as a string type
                # before processing
                search_results = search_results.astype({'similarity': str})
                # Convert similarity values to strings with 4 decimal places
                search_results.loc[:, "similarity"] = (
                    search_results["similarity"]
                    .astype(float)
                    .round(4)
                    .apply(lambda x: f"{float(x):.4f}")
                )
            
                # Define paths for the figures and HTML files
                html_tree_fig_file = (f"{output_dir_html_tree}/"
                                      f"{xword}_word_tree.html")
                html_years_fig_file = (f"{output_dir_html_years}/"
                                       f"{xword}_year_plot.html")
                html_doc_file = (f"{output_dir_html_word_docs}/"
                                 f"{xword}_word_docs.html")
                
                xword_upper = xword.upper()
                
                # Create an HTML document for the word-related documents
                html_doc = HTMLTableCreator(
                    style_dir_rel=f'../{output_dir_assets_rel_2}',
                    script_dir_rel=f'../{output_dir_assets_rel_2}',
                    help_search_bar_file_rel=(f'../{output_dir_assets_rel_2}/'
                                              'help_search_bar_words.html'),
                    about_file_rel=(f'../{output_dir_assets_rel_2}/'
                                    'about_words.html'),
                    back_button_rel='../../WORDS.html',
                    title=f'{xword_upper} - Word Related Documents',
                    columns=html_doc_columns
                )
                
                # Add each search result as a row to the HTML document
                for _, row in search_results.iterrows():
                    html_doc.add_row(row)
                
                # Save the generated HTML document
                html_doc.save_html(html_doc_file)
                
                # Construct the line for the current word's data
                xword = f'<b>{xword_upper}</b>'
                line = [
                    index,
                    xword,
                    word_count[index],
                    ', '.join(related_words),
                    HTMLTableCreator.add_file_link(
                        '<div class="no-wrap">Related Doc.</div>',
                        _get_relative_path(html_doc_file, 3),
                        open_in_new_tab=True),
                    HTMLTableCreator.add_file_link(
                        '<div class="no-wrap">Word Tree</div>',
                        _get_relative_path(html_tree_fig_file, 3),
                        open_in_new_tab=True),
                    HTMLTableCreator.add_file_link(
                        '<div class="no-wrap">Year Plot</div>',
                        _get_relative_path(html_years_fig_file, 3),
                        open_in_new_tab=True),
                ]
                
                # Append the current line and word tree to the result
                chunk_result.append([line, word_tree])
                
                # Update progress bar
                progress_bar.update(1)
            
            return chunk_result
    
        # Initialize the progress bar
        with tqdm(
                total=max_i, desc='Creating word HTML (step 1/2)',
                file=sys.stdout, ncols=0, disable=not verbose) as progress_bar:
            
            # Run sweep on chunks in parallel
            chunk_result = Parallel(n_jobs=n_jobs, prefer='threads')(
                delayed(run_word_html_chunk)(i, progress_bar)
                for i in range_s
            )
        
        # Flatten the chunk result (list of lists)
        chunk_result = [j for i in chunk_result for j in i]
        
        # Install a message handler to suppress warnings and informational
        # messages from Qt. This is applied to handle unwanted Qt-related
        # alerts that may occur when using the ETE3 library.
        qInstallMessageHandler(lambda *args, **kwargs: None)
        
        # Set the Qt platform to 'offscreen' to avoid graphical interface
        # issues when running in environments without a display (headless).
        os.environ["QT_QPA_PLATFORM"] = "offscreen"
    
        # Step 2 for processes that may cause issues within parallelization
        matplotlib.use('Agg')
        for i in tqdm(
                range(max_i), desc="Creating word HTML (step 2/2)", ncols=0,
                disable=not verbose):
            line = chunk_result[i][0]
            word_tree = chunk_result[i][1]
            
            xword = word_list[i]
            xword_upper = xword.upper()
            
            # Define paths for figures and HTML files
            tree_fig_file = f"{output_dir_tree}/{xword}_word_tree.svg"
            html_tree_fig_file = (
                f"{output_dir_html_tree}/{xword}_word_tree.html")
            year_fig_file = f"{output_dir_year_plot}/{xword}_year_plot.svg"
            html_years_fig_file = (
                f"{output_dir_html_years}/{xword}_year_plot.html")
            
            # Add row to HTML table
            chtml.add_row(line)
            
            # Yearly Trend Plot: Visualizes the yearly trends for the full
            # corpus and the target word
            
            # Normalize the occurrences of the target word:
            # - tc[2][i]: vector containing the occurrences of the target word
            #   across years;
            # - max(tc[1]): maximum number of publications in a single year;
            # - Dividing the target word occurrences by max(tc[1]) normalizes
            #   the values, allowing comparisons across different time periods.
            ctword = temporal_correlation[2][i] / max(temporal_correlation[1])
            
            # Create the figure and axis for the plot
            fig = plt.figure()
            ax = fig.add_subplot(111)
            
            # Plotting the yearly trend for the full corpus:
            # - tc[1] / processed_corpus_len: relative frequency of
            #   publications per year;
            # - fuzzy_moving_average: applies smoothing to highlight long-term
            #   trends.
            ax.plot(temporal_correlation[0],
                    fuzzy_moving_average(
                        temporal_correlation[1] / processed_corpus_len,
                        3, 0.9, 2),
                    label="Full corpus")
            
            # Plotting the yearly trend for the target word:
            # - ctword / sum(ctword): normalizes the occurrences of the target
            #   word;
            # - fuzzy_moving_average: applies smoothing to the normalized
            #   occurrences.
            ax.plot(temporal_correlation[0],
                    fuzzy_moving_average(ctword / sum(ctword), 3, 0.9, 2),
                    'm', label="Target word")
            
            # Add legend with custom styling
            ax.legend(frameon=True, facecolor='none', edgecolor='lightgray',
                      fontsize=10, borderpad=0.5, framealpha=1)
            
            # Add grid with custom line style and opacity
            ax.grid(True, linestyle='--', linewidth=0.5, alpha=0.7)
            
            # Adjust layout to avoid clipping and save the plot
            fig.tight_layout()
            fig.savefig(year_fig_file, transparent=True)
            plt.close()
            
            # Generate an interactive HTML file for the yearly trend plot
            HTMLSVGCreator.generate_html(
                year_fig_file,
                f'../{output_dir_assets_rel_2}',
                f'../{output_dir_assets_rel_2}/svg_page.js',
                html_years_fig_file,
                page_title=f'{xword_upper} - Year Plot',
                back_button_rel='../../WORDS.html'
            )
            
            # Save the word tree figure
            ts = TreeStyle()
            ts.margin_left = 10
            ts.margin_right = 10
            ts.margin_top = 10
            ts.margin_bottom = 10
            ts.branch_vertical_margin = 1
            word_tree.render(tree_fig_file, dpi=300, tree_style=ts)
            
            # Generate an interactive HTML file for the word tree plot
            HTMLSVGCreator.generate_html(
                tree_fig_file,
                f'../{output_dir_assets_rel_2}',
                f'../{output_dir_assets_rel_2}/svg_page.js',
                html_tree_fig_file,
                page_title=f'{xword_upper} - Word Tree',
                back_button_rel='../../WORDS.html'
            )
           
        # Save the final TEXTS.html table and related help/about files
        chtml.save_html(f'{output_dir}/WORDS.html')  # Save the HTML table
        HTMLTableCreator.save_help_search_bar(
            f'{output_dir_assets}',
            style_dir_rel='.',
            script_dir_rel='.',
            file_name='help_search_bar_words.html',
            back_button_rel='../../WORDS.html'
        )
        _save_about_file(
            'about_words.html',
            output_dir_assets,
            '.',
            f'./{script_file_name}',
            '../../WORDS.html'
        )
    
        # Remove SVG directory, which are already inserted in HTML
        shutil.rmtree(output_dir_year_plot)
        shutil.rmtree(output_dir_tree)

    ###########################################################################
    
    if not suppress_html_tm_texts:
        process_count += 1
        process_name = 'Creating TEXTS.html'
        if verbose:
            print(f'[{process_count}/{process_count_max}] {process_name}')
        
        # Define the columns for the HTML table
        columns = [
            "#",
            "Title",
            "Year",
            "Related Doc.",
            "PMID"
        ]
        columns = [f'<div class="no-wrap">{i}</div>' for i in columns]
        
        chtml = HTMLTableCreator(
            title=f'{html_tm_title} - Texts',
            style_dir_rel=f'{output_dir_assets_rel}',
            script_dir_rel=f'{output_dir_assets_rel}',
            help_search_bar_file_rel=(f'{output_dir_assets_rel}/'
                                      'help_search_bar_texts.html'),
            about_file_rel=f'{output_dir_assets_rel}/about_texts.html',
            columns=columns
        )
        
        # Define the columns for the document HTML
        html_doc_columns = [
            "#",
            "Rank",
            "Similarity",
            "Title + Abs.",
            "Year",
            "PMID"
        ]
        html_doc_columns = [f'<div class="no-wrap">{i}</div>'
                            for i in html_doc_columns]
        
        max_i = processed_corpus_len
        if test_mode:
            # Loop over a subset (100 for this case) of the corpus
            max_i = 100
    
        for i in tqdm(range(max_i), desc="Creating document HTML", ncols=0,
                      disable=not verbose):
            # Get the title for the current document
            title_i = title_list[i]
            
            # Get related document search results
            i_dentro = doc_dendro_ord[i]
            search_results = word_processor.search_docs(i_dentro, k_top=k_top,
                                                        query_type='doc_idx')
            
            # Map document indexes to their corresponding dendrogram order
            search_results.loc[:, "doc_idx"] = [
                doc_dendro_ord_dict[j] for j in search_results.doc_idx]
            
            # Get the top k results and associated titles/abstracts
            result_idx = list(search_results.doc_idx[0:k_top])
            title_abstract_list_i = title_abstract_list[result_idx]
            
            # Remove the 'doc' column and replace it with titles and abstracts
            search_results.drop('doc', axis=1, inplace=True)
            search_results.insert(3, 'title_abstract', title_abstract_list_i)
        
            # Get the publication years and pmids for the search results
            year_link_i = year_link_list[result_idx]
            year_link_i = pd.DataFrame(year_link_i, columns=['year', 'pmid'])
            search_results = pd.concat([search_results, year_link_i], axis=1)
            
            # Ensures the 'similarity' column is treated as a string type
            # before processing
            search_results = search_results.astype({'similarity': str})
            # Convert similarity values to strings with 4 decimal places
            search_results.loc[:, "similarity"] = (
                search_results["similarity"]
                .astype(float)
                .round(4)
                .apply(lambda x: f"{float(x):.4f}")
            )
            
            # Write the document HTML file for the current document
            html_doc_file = f"{output_dir_html_doc_docs}/{i}_doc_docs.html"
            html_doc = HTMLTableCreator(
                style_dir_rel=f'../{output_dir_assets_rel_2}',
                script_dir_rel=f'../{output_dir_assets_rel_2}',
                help_search_bar_file_rel=(f'../{output_dir_assets_rel_2}/'
                                          'help_search_bar_texts.html'),
                about_file_rel=(
                    f'../{output_dir_assets_rel_2}/about_texts.html'),
                back_button_rel='../../TEXTS.html',
                title=f'{title_i} - Related Documents',
                columns=html_doc_columns
            )
            
            # Add each row of search results to the document HTML
            for _, row in search_results.iterrows():
                html_doc.add_row(row)
                
            # Save the document HTML
            html_doc.save_html(html_doc_file)
            
            # Create the row for the main TEXTS.html table
            line = [
                i,
                title_list[i],
                year_list[i],
                HTMLTableCreator.add_file_link(
                    '<div class="no-wrap">Related Doc.</div>',
                    _get_relative_path(html_doc_file, 3),
                    open_in_new_tab=True),
                    link_list[i],
            ]
            
            # Add the row to the main HTML table
            chtml.add_row(line)
        
        # Save the final TEXTS.html table and related help/about files
        chtml.save_html(f'{output_dir}/TEXTS.html')
        HTMLTableCreator.save_help_search_bar(
            f'{output_dir_assets}',
            style_dir_rel='.',
            script_dir_rel='.',
            file_name='help_search_bar_texts.html',
            back_button_rel='../../TEXTS.html'
        )
        _save_about_file(
            'about_texts.html',
            output_dir_assets,
            '.',
            f'./{script_file_name}',
            '../../TEXTS.html'
        )
    
def _save_about_file(output_file_name, output_dir, style_dir_rel,
                     script_file_rel, back_button_rel):
    """
    Save a formatted "About" HTML file with a back button and CSS styling.

    This function reads an input HTML file containing "About" content, inserts
    a CSS file path, a JavaScript file path, and a back button HTML, and
    writes the formatted content to an output HTML file in the specified
    directory.

    Parameters:
        - output_file_name (str): The name of the output HTML file to be
          saved in the `output_dir` directory.
        - output_dir (str): The directory where the output HTML file is
          saved.
        - style_dir_rel (str): The relative path to the directory containing
          the CSS files that style the "About" HTML content.
        - script_file_rel (str): The relative path to the JavaScript file that
          provides functionality for the "About" HTML content.
        - back_button_rel (str): The relative path to the file where the
          back button links to (e.g., '../../TEXTS.html').

    Returns:
        - None: The function writes the formatted HTML content to the output
          file but does not return any value.
    """
    # Construct the path to the input HTML file containing the "About"
    # content.
    about_file_input = os.path.join(
        os.path.dirname(os.path.dirname(__file__)),
        "txtree_assets",
        "html_tm_pubmed_about.html")
    # Define the output path for the processed "About" HTML file.
    about_file_output = f'{output_dir}/{output_file_name}'
    # Create the HTML code for the "Back" button, linking it to the
    # "TEXTS.html" file.
    back_button_html = (f'<a href="{back_button_rel}">'
                          '<button id="backButton">Back</button></a>')
    # Open and read the input HTML file containing the "About" content.
    with open(about_file_input, 'r', encoding='utf-8') as help_html_file:
        about_html_content = help_html_file.read()
    # Format the HTML content by inserting the CSS file path and the "Back"
    # button HTML.
    about_html_content = about_html_content.format(
        style_dir_rel=style_dir_rel,
        script_file_rel=script_file_rel,
        back_button_html=back_button_html)
    # Write the formatted HTML content to the output file.
    with open(about_file_output, 'w', encoding='utf-8') as f:
        f.write(about_html_content)
        
def _get_relative_path(path, num_parts):
    """
    Function to extracts the last `num_parts` parts of a file path to form a
    relative path.
    """
    return '/'.join(path.split('/')[-num_parts:])