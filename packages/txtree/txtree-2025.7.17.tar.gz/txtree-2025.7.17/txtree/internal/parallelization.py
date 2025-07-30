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

from joblib import Parallel, delayed
from tqdm import tqdm
from .split_array import split_array

def parallelization(data_list, func, chunk_size=1000, n_jobs=1, desc=None,
                    verbose=True):
    """
    Perform parallel processing on a list of data by splitting it into chunks
    and applying a function.

    Parameters:
    - data_list: List of data to be processed.
    - func: Function to apply to each chunk of data.
    - chunk_size: Size of each chunk (default is 1000).
    - n_jobs: Number of parallel jobs to run (default is 1).
    - desc: Description to display alongside the progress tracking (default is
      None).
    - verbose: Boolean flag to enable/disable progress tracking (default is
      True).

    Returns:
    - A flattened list of results from the function applied to each chunk.
    """
    
    # Split the data list into smaller chunks of the specified size
    chunks = split_array(data_list, chunk_size)
    
    # Initialize the progress bar for monitoring progress
    with tqdm(total=len(chunks), desc=desc, ncols=0,
              disable=not verbose) as progress_bar:
        # Use Parallel to apply the function to each chunk of data
        result = Parallel(n_jobs=n_jobs, prefer="threads")(
            delayed(lambda chunk: (func(chunk), progress_bar.update()))(chunk)
            for chunk in chunks
        )
    
    # Extract the results from the tuples returned by Parallel
    result = [i[0] for i in result]
    
    # Flatten the list of results
    result = [item for sublist in result for item in sublist]
    
    return result