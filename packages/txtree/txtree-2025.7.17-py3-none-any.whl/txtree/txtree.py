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

import argparse
from .utils import medline_to_html_tm

def txtree():    
    # Create the parser
    parser = argparse.ArgumentParser(
        description=(
            'Description: '
            'TXTree is a vector-based analysis tool designed to transform a '
            'MEDLINE file (a PubMed search result) into an HTML-TM '
            '(Hypertext Markup Language for Text Mining), a portable HTML '
            'platform for exploring texts.'
        ),
        add_help=False # Disable the default help argument
    )
    
    # Add the help argument manually
    help_group = parser.add_argument_group('Help Argument')
    help_group.add_argument(
        '-h', '--help', action='help', default=argparse.SUPPRESS,
        help=('Show this help message and exit.')
    )
    
    # Required Argument
    required_group = parser.add_argument_group('Required Argument')
    required_group.add_argument(
        'input_path', type=str,
        help=('Path to the Medline dataset file or a preprocessed directory.')
    )
    
    # Output Argument
    output_group = parser.add_argument_group('Output Argument')
    output_group.add_argument(
        '--output_dir', type=str, default='txtree_result',
        help=('Directory to store output. Default: "txtree_result".')
    )

    # HTML-TM Interface Argument
    title_theme_group = parser.add_argument_group(
        'HTML-TM Interface Argument'
    )
    title_theme_group.add_argument(
        '--html_tm_title', type=str, default='HTML-TM',
        help=('Title for the HTML-TM. Default: "HTML-TM".')
    )
    
    # Filtering Argument
    filtering_group = parser.add_argument_group('Filtering Argument')
    filtering_group.add_argument(
        '--tf_idf_threshold', type=float, default=0.1,
        help=(
            'Threshold for filtering words based on their TF-IDF scores. '
            'Words with TF-IDF scores below this threshold are filtered out. '
            'Default: 0.1.'
        )
    )
    
    # Dendrogrammatic Ordination Arguments
    dendro_ord_group = parser.add_argument_group(
        'Dendrogrammatic Ordination Arguments'
    )
    dendro_ord_group.add_argument(
        '--word_ord_max_clus', type=int, default=None,
        help=(
            'Maximum number of clusters for word ordination. This parameter '
            'controls the maximum number of clusters allowed during '
            'hierarchical clustering of words. If not set, no limit is '
            'applied. Default: None.'
        )
    )
    dendro_ord_group.add_argument(
        '--doc_ord_max_clus', type=int, default=None,
        help=(
            'Maximum number of clusters for document ordination. This '
            'parameter controls the maximum number of clusters allowed '
            'during hierarchical clustering of documents. If not set, no '
            'limit is applied. Default: None.'
        )
    )
    
    # Optional Output Argument
    optional_output_group = parser.add_argument_group(
        'Optional Output Argument'
    )
    optional_output_group.add_argument(
        '--save_emb', action='store_true',
        help=(
            'Save embedding vectors in an HDF5 file in the output directory.'
        )
    )
    
    # File Recreation Arguments
    file_recreation_group = parser.add_argument_group(
        'File Recreation Arguments'
    )
    file_recreation_group.add_argument(
        '--force_xml', action='store_true',
        help=('Force recreate XML file.')
    )
    file_recreation_group.add_argument(
        '--force_word_processor', action='store_true',
        help=('Force recreate Word Processor file.')
    )
    file_recreation_group.add_argument(
        '--force_temporal_correlation', action='store_true',
        help=('Force recreate Temporal Correlation file.')
    )
    file_recreation_group.add_argument(
        '--force_html_tm', action='store_true',
        help=('Force recreate HTML-TM files.')
    )
    
    # Directory Management Argument
    dir_group = parser.add_argument_group('Directory Management Argument')
    dir_group.add_argument(
        '--del_exist_dir', action='store_true',
        help=('Delete existing output directory if it exists.')
    )
    
    # Suppression Arguments
    suppression_group = parser.add_argument_group('Suppression Arguments')
    suppression_group.add_argument(
        '--suppress_temporal_correlation', action='store_true',
        help=(
            'Suppresses the Temporal Correlation process. If this flag is '
            'set, the Temporal Correlation file is not generated, regardless '
            'of other settings.'
        )
    )
    suppression_group.add_argument(
        '--suppress_html_tm', action='store_true',
        help=(
            'Suppresses the creation of HTML-TM files. If this flag is set, '
            'HTML-TM is not generated, regardless of other settings.'
        )
    )
    suppression_group.add_argument(
        '--suppress_html_tm_words', action='store_true',
        help=(
            'Suppresses the creation of the WORDS.html file (part of '
            'HTML-TM). If this flag is set, WORDS.html is not generated, '
            'regardless of other settings.'
        )
    )
    suppression_group.add_argument(
        '--suppress_html_tm_texts', action='store_true',
        help=(
            'Suppresses the creation of the TEXTS.html file (part of '
            'HTML-TM). If this flag is set, TEXTS.html is not generated, '
            'regardless of other settings.'
        )
    )
    
    # Special mode Argument
    special_group = parser.add_argument_group('Special Mode Argument')
    special_group.add_argument(
        '--only_emb', action='store_true',
        help=(
            'If enabled, only the embedding vectors are generated and saved, '
            'skipping the Temporal Correlation and HTML-TM creation '
            'processes. This option automatically sets `save_emb`, '
            '`suppress_temporal_correlation`, and `suppress_html_tm` to True. '
            'When `only_emb` is used, it overrides any direct definitions of '
            '`save_emb`, `suppress_temporal_correlation`, and '
            '`suppress_html_tm`, regardless of their individual settings.'
        )
    )
    
    # Memory Management Argument
    memory_group = parser.add_argument_group('Memory Management Argument')
    memory_group.add_argument(
        '--ignore_memory_check', action='store_true',
        help=(
            'Ignore memory checks before processing. If enabled, skips memory '
            'validation, which could lead to crashes if the system lacks '
            'sufficient RAM for large datasets. Use with caution. '
            'Default: False (checks memory).')
        )
    
    # Parallelization Arguments
    parallel_group = parser.add_argument_group('Parallelization Arguments')
    parallel_group.add_argument(
        '--n_jobs', type=int, default=1,
        help=(
            'Number of parallel jobs for specific tasks. This parameter '
            'controls how many processes are used for parallel execution in '
            'applicable cases. Not all processes are parallelized. Default: 1 '
            '(no parallelization).'
        )
    )
    parallel_group.add_argument(
        '--chunk_size', type=int, default=1000,
        help=(
            'Chunk size for tasks that support parallel execution. This '
            'parameter controls the number of items processed in each batch '
            'during parallel execution. A larger chunk size reduces '
            'communication overhead but may increase memory usage. Default: '
            '1000.'
        )
    )
    
    # Testing Argument
    testing_group = parser.add_argument_group('Testing Argument')
    testing_group.add_argument(
        '--test_html_tm', action='store_true',
        help=(
            'Activates test mode for HTML-TM generation. Use this mode to '
            'validate the output structure and debug the process without '
            'requiring the full processing.'
        )
    )
    
    # Verbosity Argument
    verbosity_group = parser.add_argument_group('Verbosity Argument')
    verbosity_group.add_argument(
        '--quiet', action='store_false',
        help=('Disable verbose output.')
    )
    
    # Parse the arguments
    args = parser.parse_args()

    medline_to_html_tm(
        input_path=args.input_path,
        output_dir=args.output_dir,
        html_tm_title=args.html_tm_title,
        tf_idf_threshold=args.tf_idf_threshold,
        word_ord_max_clus=args.word_ord_max_clus,
        doc_ord_max_clus=args.doc_ord_max_clus,
        save_emb=args.save_emb,
        force_xml=args.force_xml,
        force_word_processor=args.force_word_processor,
        force_temporal_correlation=args.force_temporal_correlation,
        force_html_tm=args.force_html_tm,
        del_exist_dir=args.del_exist_dir,
        suppress_temporal_correlation=args.suppress_temporal_correlation,
        suppress_html_tm=args.suppress_html_tm,
        suppress_html_tm_words=args.suppress_html_tm_words,
        suppress_html_tm_texts=args.suppress_html_tm_texts,
        only_emb=args.only_emb,
        ignore_memory_check=args.ignore_memory_check,
        n_jobs=args.n_jobs,
        chunk_size=args.chunk_size,
        test_html_tm=args.test_html_tm,
        verbose=args.quiet)
        
if __name__ == "__main__":
    txtree()