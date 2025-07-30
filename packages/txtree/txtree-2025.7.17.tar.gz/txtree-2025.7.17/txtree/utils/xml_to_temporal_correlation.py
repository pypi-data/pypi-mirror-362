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

import xml.etree.ElementTree as ET
import numpy as np
from ..internal import (compute_temporal_correlation, save_pickle, load_pickle)

def xml_to_temporal_correlation(xml, word_processor, output_path=None,
                                verbose=True):
    """
    Processes temporal correlation using a given XML file, a word processor,
    and a temporal correlation function to calculate the relationship between 
    the publication years of the entries and the term usage over time.

    Parameters:
        - xml (str): Path to the XML file containing bibliographic entries
          with publication years.
        - word_processor (object or str): A WordProcessor object containing a 
          tokenized corpus and word list, or a string path to a pickle file 
          containing the WordProcessor object.
        - output_path (str, optional): Path to save the temporal correlation
          results. If None, the results are not saved. Defaults to None.
        - verbose (bool, optional): Whether to print progress and information. 
          Defaults to True.
          
    Returns:
        - temporal_correlation: A temporal correlation object that contains
          the calculated relationship between terms and publication years.
    """
    # Handle the case where word_processor is a path to a pickle file
    if isinstance(word_processor, str):
        # Load the word processor
        if verbose:
            print(f'Loading word processor from: "{word_processor}".')
        word_processor = load_pickle(word_processor)
        if verbose:
            print("Word processor loaded successfully.")

    # Extract publication years from the XML file
    publication_year_list = []
    for event, record in ET.iterparse(xml, events=("start", "end")):
        if event == "end" and record.tag == "entry":
            publication_year = record.find("publication_year")
            publication_year_list.append(int(publication_year.text)
                                         if publication_year is not None
                                         else np.nan)
            record.clear()  # Clear the record to free memory

    # Access tokenized corpus and word list
    tokenized_text = word_processor.tokenized_corpus
    word_list = word_processor.word_list

    # Compute temporal correlation
    temporal_correlation = compute_temporal_correlation(
        publication_year_list,
        tokenized_text,
        word_list,
        verbose=verbose)

    # Save the result if output_path is specified
    if output_path:
        save_pickle(temporal_correlation, output_path)
    
    return temporal_correlation