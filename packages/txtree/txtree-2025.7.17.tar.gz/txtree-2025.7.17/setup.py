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

from setuptools import setup, find_packages
from datetime import datetime

# Get current date in YYYY.MM.DD format
current_date = datetime.now().strftime("%Y.%m.%d")

setup(
    name='txtree',
    version=current_date,  # Uses automatically generated date version
    author='Diogo de Jesus Soares Machado, Roberto Tadeu Raittz',
    description=(
        'TXTree: A Visual Tool for PubMed Literature Exploration by Text Mining'
    ),
    packages=find_packages(),
    long_description_content_type='text/markdown',
    long_description=open('README.md').read(),
    zip_safe=False,
    install_requires=[
        'biopython==1.85',
        'ete3==3.1.3',
        'h5py==3.12.1',
        'matplotlib==3.10.0',
        'nuitka==2.6',
        'numpy==2.2.2',
        'pandas==2.2.3',
        'pip-licenses==5.0.0',
        'psutil==7.0.0',
        'PyQt5==5.15.11',
        'scikit-learn==1.6.1',
        'scipy==1.15.1',
        'tqdm==4.67.1',
    ],
    license='AGPL-3.0-or-later',
    license_files=['LICENSE.txt']
)