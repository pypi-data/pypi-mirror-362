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

import psutil

def get_available_mem():
    """
    Retrieves the amount of available memory in the system.

    Returns:
        - float: The amount of available memory in gigabytes (GB).

    Notes:
        - This function uses the `psutil` library to access system memory
          information.
        - The available memory is calculated as the sum of free memory and
          memory that can be quickly made available (e.g., cached or buffers).
    """
    # Get system memory information
    memory_info = psutil.virtual_memory()

    # Available memory in bytes
    available_memory_bytes = memory_info.available

    # Convert bytes to gigabytes
    available_memory_gb = available_memory_bytes / (1024 ** 3)

    return available_memory_gb