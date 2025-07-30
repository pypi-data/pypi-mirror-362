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
from scipy.stats import pearsonr
from tqdm import tqdm
from .fuzzy_moving_average import fuzzy_moving_average

def compute_temporal_correlation(publication_year_list, tokenized_corpus,
                                 word_list, verbose=True):
    """
    Analyzes the temporal correlation of word occurrences in PubMed data.

    This function calculates the temporal correlation of word occurrences in
    PubMed articles over time. It provides insights into how the frequency of
    specific words correlates with the passage of time. The analysis includes
    calculating correlation coefficients, p-values, and storing results for
    further exploration.

    Parameters:
        - publication_year_list (list): A list of publication years for each
          article.
        - tokenized_corpus (list of list): A list of tokenized text from
          PubMed articles.
        - word_list (list): A list of words to analyze.
        - verbose (bool, optional): Whether to display progress information.
          Defaults to True.

    Returns:
        - count_by_year (numpy array): Array of publication years and their
          corresponding article counts.
        - word_occ_by_year (numpy array): A 2D array of word occurrences by
          year.
        - word_temp_corr (numpy array): An array of temporal correlation
          coefficients and p-values for each word.
    """
    year_start = np.min(publication_year_list)
    year_end = np.max(publication_year_list)

    count_by_year = {year: 0 for year in range(year_start, year_end + 1)}
    for year in publication_year_list:
        count_by_year[year] += 1

    num_years = len(count_by_year)
    num_words = len(word_list)

    word_list_idx = {word: idx for idx, word in enumerate(word_list)}
    years_idx = {year: idx for idx, year in enumerate(count_by_year)}

    word_occ_by_year = np.zeros((num_words, num_years), dtype=int)
    word_temp_corr = []

    tokenized_corpus_len = len(tokenized_corpus)
    with tqdm(total=tokenized_corpus_len,
              desc='Count occurrences by year', ncols=0,
              disable=not verbose) as pbar:
        for i, text in enumerate(tokenized_corpus):
            for word in text:
                try:
                    word_idx = word_list_idx[word]
                except KeyError:
                    continue
                year_idx = years_idx[publication_year_list[i]]
                word_occ_by_year[word_idx, year_idx] += 1
            pbar.update(1)

    max_count_by_year = max(count_by_year.values())

    with tqdm(total=num_words, desc='Calculate correlation', ncols=0,
              disable=not verbose) as pbar:
        for i in range(num_words):
            normalized_occurrences = word_occ_by_year[i, :] / max_count_by_year
            normalized_occurrences = fuzzy_moving_average(
                normalized_occurrences, 1, 0.9, 2)
            correlation, p_value = pearsonr(normalized_occurrences,
                                            range(num_years))
            word_temp_corr.append([correlation, p_value])
            pbar.update(1)

    word_temp_corr = np.array(word_temp_corr)

    return (np.array(list(count_by_year.keys())),
            np.array(list(count_by_year.values())),
            word_occ_by_year, word_temp_corr)