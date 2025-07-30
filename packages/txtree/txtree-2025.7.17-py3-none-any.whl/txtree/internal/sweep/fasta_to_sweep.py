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
from time import time
from tqdm import tqdm
import warnings
import math
from joblib import Parallel, delayed
import sys

from .utils import (fastaread, orthrand, create_sweep_masks)
from .internal import (transform_with_lambert_w, scan_mask, aa_to_num,
                       count_occ, load_matrix_from_path)

def fasta_to_sweep(fasta, proj=1369, mask=None, xbinary=False,
                   minus_one_mode=False, n_jobs=1, chunk_size=1000,
                   progress_bar=True, print_details=True):
    """
    Applies SWeeP to a FASTA input.

    Parameters:
        - fasta (str or list): 
            - The path to a FASTA file or a list of SeqRecord objects 
              (in Biopython format).
        
        - proj (int, numpy.ndarray, list of numpy.ndarray, list of int, list
          of str, or str): 
            - Defines the projection input method, which determines the way
              projections are handled:
                - **int**: The number of projections to generate. When `proj`
                  is an integer, the function generates random projections
                  with this number of dimensions.
                - **list of int**: A list of integers, where each integer
                  represents the number of dimensions for a different random
                  projection.
                - **numpy.ndarray**: A single precomputed projection matrix.
                - **list of numpy.ndarray**: A list of precomputed projection 
                  matrices.
                - **str**: The path to a file containing the projection matrix.
                  The file can be in one of the following formats: .txt, .npy,
                  .h5, .mat, or .pickle.
                - **list of str**: A list of paths to files, where each file
                  contains a precomputed projection matrix.
            -  Default is 1369.
        
        - mask (list or None): 
            - A list of masks to be applied to the sequences. If None, default 
              sweep masks are generated.
        
        - xbinary (bool): 
            - If True, applies a binary transformation to the projection
              counts.
            - Default is False.
        
        - minus_one_mode (bool): 
            - If True, sets HDV inactive positions to -1. This option has no
              effect when `proj` is of type int.
            - Default is False.
        
        - chunk_size (int): 
            - The number of sequences to process in each chunk for
              memory-efficient computation.
            - Default is 1000.
        
        - progress_bar (bool): 
            - If True, displays a progress bar showing the processing status.
            - Default is True.
        
        - print_details (bool): 
            - If True, prints detailed output during processing.
            - Default is True.

    Returns:
        - list: 
            - A list containing the transformed projection results, one for
              each mask.
    """

    start_t = time()
    
    # Extract sequences from the FASTA file
    if isinstance(fasta, str):
        fasta = fastaread(fasta)
    try:
        seq = [str(i.seq).upper() for i in fasta]
    except AttributeError:
        seq = [i.upper() for i in fasta]
    
    # Generate masks
    if mask is None or len(mask)==0:
        mask = create_sweep_masks(6, 4)
    elif type(mask[0]) == int:
        mask = [mask]
    
    nmask = len(mask)
    
    # Handling different types for proj
    R_idx = []
    ldv_len = None
    # If is single path to a matrix file
    if isinstance(proj, str):
        R = [load_matrix_from_path(proj)]
        R_idx = [0] * nmask
        ldv_len = [len(R[0])] * nmask
        proj_type = 'single_file'
    # If is list of paths/matrices
    elif isinstance(proj, (np.ndarray, list)):
        if isinstance(proj, list):
            # If is list of paths
            if all(isinstance(item, str) for item in proj):
                R = [load_matrix_from_path(path) for path in proj]
                proj_type = 'list_of_files'
            # If is list of matrices
            elif all(isinstance(item, np.ndarray) for item in proj):
                R = proj  # Just use the matrices as is
                proj_type = 'list_of_matrices'
            # If is list of projection sizes (list of integers)
            elif all(isinstance(item, int) for item in proj):
                R = []  # No matrices provided
                R_idx = [0] * nmask
                ldv_len = proj  # Directly assign the list of projection sizes
                proj_type = 'list_of_projection_sizes'
        # If is single matrix
        else:
            R = [np.array(proj)]
            proj_type = 'matrix'
        # Store size and indexing
        ldv_len = ([len(i[0]) for i in R] if not isinstance(ldv_len, list)
                   else ldv_len)
        if len(R) > 1:
            R_idx = list(range(0, nmask))
        else:
            # Single matrix
            R_idx = [0] * nmask
            if proj_type != 'list_of_projection_sizes':
                ldv_len = ldv_len * nmask
    # If is number of projections
    elif isinstance(proj, int):
        R = []  # No precomputed projections
        R_idx = [0] * nmask
        ldv_len = [proj] * nmask
        proj_type = 'projection_size'
        # Display a warning when a parameter with no effect is set
        if minus_one_mode:
            warnings.warn(
                ("Warning: 'minus_one_mode' has no effect when 'proj' is an "
                 "integer (projection size)."),
                UserWarning
            )
    else:
        raise ValueError(
            "proj must be an integer, numpy.ndarray, list of lists or numpy "
            "arrays, a single path (str), or a list of paths to matrix files."
        )
        
    # Check if the number of projections matches the number of masks
    if len(ldv_len) > nmask:
        warnings.warn(("Warning: There are more projection sizes "
                       f"({len(ldv_len)}) than masks ({nmask})."), UserWarning)
    elif len(ldv_len) < nmask:
        raise ValueError(("Error: There are fewer projection sizes "
                          f"({len(ldv_len)}) than masks ({nmask})."))
    
    # Check if random projection creation are required
    morthrand = len(R) == 0
    
    # Compute parameters for each mask
    ntake, nbits, hdv_len, Um, Un, xnorm = [], [], [], [], [], []
    for i in range(0, nmask):
        m = mask[i]
        ntake.append(sum(m))
        nbits.append(len(m))
        hdv_len.append(20**ntake[i])
        
        if morthrand:
            # Initialize sinusoidal components for projection
            Um.append(np.sin(range(1, ldv_len[i] + 1)))
            Un.append(np.sin(range(1, hdv_len[i] + 1)))
            xnorm.append(np.sqrt(hdv_len[i] / 3))
    
    # Validate projection matrix dimensions if applicable
    if proj_type not in ('projection_size', 'list_of_projection_sizes'):
        # If there are different intakes
        ntake_uni_len = len(set(ntake))
        if ntake_uni_len != 1 and len(R) == 1:
            raise ValueError(
                "When masks have values different from 'ntake', and a "
                "precomputed projection matrix is desired as input, 'proj' "
                "must be a list containing one matrix for each mask."
            )
        R_shape_error = []
        for i in range(nmask):
            R_shape = np.shape(R[R_idx[i]])
            if R_shape[0] != hdv_len[i]:
                R_shape_error.append(i)
        if R_shape_error:
            raise ValueError(
                "The masks at the following indices are incompatible with the "
                f"corresponding projection matrix: {R_shape_error}. "
                "The number of lines must be 20**ntake, where ntake is the "
                "number of take positions in the mask."
            )
    
    # Define the transformation function
    if xbinary:
        fx = lambda x: (x > 0) + 0
    else:
        fx = lambda x: transform_with_lambert_w(x)
    
    nfas = len(seq)
    
    if print_details:
        print(f"Number of sequences: {nfas}")
        print(f"Number of masks: {nmask}")
        print(f"nbits: {', '.join(map(str, nbits))}")
        print(f"ntake: {', '.join(map(str, ntake))}")
        print(f"Masks: {', '.join(f'{row}' for row in mask)}")
        print(f"HDV length: {', '.join(map(str, hdv_len))}")
        print(f"LDV length: {', '.join(map(str, ldv_len))}")
        print(f"Projection input type: {proj_type.replace('_' ,' ')}")
    
    # Calculate the number of chunks
    chunks = math.ceil(nfas / chunk_size)
    range_s = range(0, chunks)
    # Generate chunks
    chunk_indices = (np.tile(chunk_size, (chunks, 2)) *
                     np.array([list(range(0, chunks)),
                               list(range(1, chunks + 1))]).T +
                     np.concatenate((np.ones((chunks, 1)),
                                     np.zeros((chunks, 1))), axis=1))
    # Adjust the last chunk's ending index to nfas
    chunk_indices[-1, 1] = nfas
    # Adjust indices to be zero-based
    chunk_indices = chunk_indices - 1
    
    def sweep_chunk(i, progress_bar):
        CT_expanded_list = [[] for _ in range(nmask)]
        SWP_chunk = [[] for _ in range(nmask)]
        
        seq_chunk = seq[int(chunk_indices[i, 0]):int(chunk_indices[i, 1]) + 1]
        seq_chunk_len = len(seq_chunk)
        
        # Process sequences and apply masks/projections
        for k in range(seq_chunk_len):
            s = seq_chunk[k]
            
            for j in range(nmask):
                # Apply the mask to the sequence
                SSlist = scan_mask(s, mask[j])
                # Convert sequence to numerical representation
                HDV = aa_to_num(SSlist)
                HDV = [x for x in HDV if 0 <= x < hdv_len[j]]
                # Counting occurrences
                CT = list(count_occ(HDV))
                # Apply the transformation function (fx) to the count
                CT[1] = fx(np.array(CT[1]))
                            
                # Projection step
                if morthrand:
                    swp = (CT[1].reshape(1, -1) @
                           ((1 / xnorm[j]) * orthrand(CT[0], Um[j], Un[j])))
                    SWP_chunk[j].append(swp)
                    
                else:
                    CT_expanded = np.zeros((1, hdv_len[j]))
                    if minus_one_mode:
                        CT_expanded -= 1
                    CT_expanded[:, CT[0]] = CT[1]
                    CT_expanded_list[j].append(CT_expanded)
            
            # Update progress bar
            progress_bar.update(1)
                        
        for j in range(nmask):
            if not morthrand:  
                CT_expanded_list[j] = np.vstack(CT_expanded_list[j])
                swp = CT_expanded_list[j] @ R[R_idx[j]]
                SWP_chunk[j] = swp
            else:
                SWP_chunk[j] = np.vstack(SWP_chunk[j])
            
        return SWP_chunk
    
    # Initialize the progress bar
    total_sequences = len(seq)
    with tqdm(total=total_sequences, desc='Processing sequences',
              file=sys.stdout, ncols=0, disable=(not progress_bar)
              ) as progress_bar:
        # Run sweep on chunks in parallel
        SWP = Parallel(n_jobs=n_jobs, prefer='threads')(
            delayed(sweep_chunk)(i, progress_bar)
            for i in range_s
        )
    SWP = [np.vstack(i) for i in zip(*SWP)]
    
    end_t = time()
    if print_details:
        print("Elapsed time:", end_t - start_t)
    
    return SWP