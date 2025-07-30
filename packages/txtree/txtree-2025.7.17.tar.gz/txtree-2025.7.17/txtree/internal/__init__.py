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

from .aminocode import aminocode
from .compute_tf_idf import compute_tf_idf
from .count_occurrences import count_occurrences
from .create_seqrecord_list import create_seqrecord_list
from .estimate_scipy_linkage_mem import estimate_scipy_linkage_mem
from .estimate_scipy_linkage_n import estimate_scipy_linkage_n
from .explode_list import explode_list
from .fuzzy_moving_average import fuzzy_moving_average
from .get_available_mem import get_available_mem
from .get_dendro_ord import get_dendro_ord
from .get_norm import get_norm
from .htmltools import HTMLTableCreator, HTMLSVGCreator
from .load_h5 import load_h5
from .load_pickle import load_pickle
from .map_docs_to_words import map_docs_to_words
from .map_words_to_docs import map_words_to_docs
from .mat_to_ete_tree import mat_to_ete_tree
from .parallelization import parallelization
from .pca import pca
from .rank_by_cosine_similarity import rank_by_cosine_similarity
from .save_h5 import save_h5
from .save_pickle import save_pickle
from .sweep import fasta_to_sweep, create_proj_mat
from .compute_temporal_correlation import compute_temporal_correlation
from .tokenize import tokenize

__all__ = [
    'aminocode',
    'compute_tf_idf',
    'count_occurrences',
    'create_seqrecord_list',
    'estimate_scipy_linkage_mem',
    'estimate_scipy_linkage_n',
    'explode_list',
    'fuzzy_moving_average',
    'get_available_mem',
    'get_dendro_ord',
    'get_doc_word_idx',
    'get_norm',
    'get_word_doc_idx',
    'HTMLTableCreator',
    'HTMLSVGCreator',
    'load_h5',
    'load_pickle',
    'map_docs_to_words',
    'map_words_to_docs',
    'mat_to_ete_tree',
    'parallelization',
    'pca',
    'rank_by_cosine_similarity',
    'save_h5',
    'save_pickle',
    'fasta_to_sweep',
    'create_proj_mat',
    'compute_temporal_correlation',
    'tokenize'
]