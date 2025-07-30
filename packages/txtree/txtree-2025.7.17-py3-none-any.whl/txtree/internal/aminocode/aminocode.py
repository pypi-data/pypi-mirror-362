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

import re
import unicodedata

# AMINOcode encoding table for letters and symbols
aminocode_table = {
    "a": "YA",
    "b": "E",
    "c": "C",
    "d": "D",
    "e": "YE",
    "f": "F",
    "g": "G",
    "h": "H",
    "i": "YI",
    "j": "I",
    "k": "K",
    "l": "L",
    "m": "M",
    "n": "N",
    "o": "YQ",
    "p": "P",
    "q": "Q",
    "r": "R",
    "s": "S",
    "t": "T",
    "u": "YV",
    "v": "V",
    "x": "W",
    "z": "A",
    "w": "YW",
    "y": "YY",
    ".": "YP",
    "9": "YD",
    " ": "YS",
}

# AMINOcode encoding table for digits
aminocode_table_d = {
    "0": "YDA",
    "1": "YDQ",
    "2": "YDT",
    "3": "YDH",
    "4": "YDF",
    "5": "YDI",
    "6": "YDS",
    "7": "YDE",
    "8": "YDG",
    "9": "YDN",
}

# AMINOcode encoding table for punctuation
aminocode_table_p = {
    ".": "YPE",
    ",": "YPC",
    ";": "YPS",
    "!": "YPW",
    "?": "YPQ",
    ":": "YPT",
}  

def encode_string(input_string, detail='dp'):
    """
    Encodes a string with AMINOcode.

    This function encodes a given string by translating its characters into
    AMINOcode using predefined encoding tables for letters, digits, and
    punctuation. The function also handles unaccented characters and spaces.

    Parameters:
        - input_string (str): The natural language text string to be encoded.
        - detail (str): Set details in coding. 'd' for details in digits; 'p'
          for details on punctuation; 'dp' or 'pd' for both. Default is 'dp'.

    Returns:
        - str: The encoded text string.

    Example:
        >>> encoded_string = encode_string("Hello world!", 'dp')
        >>> print(encoded_string)
        'HYELLYQYSYWYQRLDYPW'
    """
    
    # Decode the input string if it's in bytes format
    try:
        input_string = input_string.decode('utf-8')
    except (AttributeError, UnicodeDecodeError):
        # If the input is already a string or decoding fails, continue without
        # changes
        pass
    
    # Remove accents and special characters
    # Normalize the string to its decomposed form (NFKD) to separate base
    # characters from diacritics
    input_string = unicodedata.normalize('NFKD', input_string)
    # Remove combining characters (like accents) to get the base characters
    # only
    input_string = "".join(
        [c for c in input_string if not unicodedata.combining(c)])
    
    # Convert the string to lowercase to ensure consistent encoding
    input_string = input_string.lower()
    
    # Normalize all whitespace characters (e.g., tabs, newlines) to a single
    # space
    input_string = re.sub(r'\s', ' ', input_string)
    
    # Start with the base encoding table
    c_dict = aminocode_table.copy()
    
    # Add detailed digit encoding if 'd' is specified in the detail parameter
    if 'd' in detail:
        c_dict.update(aminocode_table_d)
    else:
        # If detailed digit encoding is not requested, replace all digits with
        # '9'
        input_string = re.sub(r'\d', '9', input_string)
    
    # Add detailed punctuation encoding if 'p' is specified in the detail
    # parameter
    if 'p' in detail:
        c_dict.update(aminocode_table_p)
    else:
        # If detailed punctuation encoding is not requested, replace specific
        # punctuation marks with '.'
        input_string = re.sub('[,;!?:]', '.', input_string)
    
    # Ensure all characters in the input string are in the encoding dictionary
    # If a character is not found, assign it a default encoding of 'YK'
    for i in ''.join(set(input_string)):
        if i not in c_dict:
            c_dict[i] = 'YK'
    
    # Replace each character in the input string with its corresponding value
    # from the dictionary
    for k, v in c_dict.items():
        input_string = input_string.replace(k, v)
    
    return input_string
    
def decode_string(input_string, detail='dp'):
    """
    Decodes a string with AMINOcode reverse.

    This function decodes a given AMINOcode-encoded string back to its
    original text by reversing the encoding process using the predefined
    decoding tables for letters, digits, and punctuation.

    Parameters:
        - input_string (str): The AMINOcode-encoded text string.
        - detail (str): Set details in coding. 'd' for details in digits; 'p'
          for details on punctuation; 'dp' or 'pd' for both. Default is 'dp'.

    Returns:
        - str: The decoded text string.

    Example:
        >>> decoded_string = decode_string("HYELLYQYSYWYQRLDYPW", 'dp')
        >>> print(decoded_string)
        'hello world!'
    """
    
    c_dict = aminocode_table.copy()
    if 'd' in detail:
        c_dict.update(aminocode_table_d)
    if 'p' in detail:
        c_dict.update(aminocode_table_p)
        
    c_dict = dict(sorted(c_dict.items(), key=lambda x: (len(x[1]), x[0]),
                          reverse=True))
    input_string = input_string.replace('YK', '-')
    
    for k, v in c_dict.items():
        input_string = input_string.replace(v, k)
    
    decoded_string = input_string
    return decoded_string

def encode_list(string_list, detail='dp', verbose=False):
    """
    Encodes all strings in a list with AMINOcode.

    This function encodes each string in a given list of strings using
    AMINOcode encoding.

    Parameters:
        - string_list (list of str): The list of strings to be encoded.
        - detail (str): Set details in coding. 'd' for details in digits; 'p'
          for details on punctuation; 'dp' or 'pd' for both. Default is 'dp'.
        - verbose (bool): If True, displays progress during encoding.

    Returns:
        - list of str: List of encoded strings.

    Example:
        >>> encoded_list = encode_list(['Hello', 'world', '!'], 'dp')
        >>> print(encoded_list)
        ['HYELLYQ', 'YWYQRLD', 'YPW']
    """
    
    list_size = len(string_list)
    selectedEncoder = lambda x: encode_string(x, detail=detail)

    encoded_list = []
    if verbose:
        print('Encoding text...')
    for c, i in enumerate(string_list):
        seq = selectedEncoder(i)
        encoded_list.append(seq)
        if verbose and (c+1) % 10000 == 0:
            print(str(c+1)+'/'+str(list_size))
    if verbose:
        print(str(list_size)+'/'+str(list_size))
    return encoded_list

def decode_list(input_list, detail='dp', verbose=False):
    """
    Decodes all strings in a list with reverse AMINOcode.

    This function decodes each AMINOcode-encoded string in a given list of
    encoded strings back to their original text using the reverse decoding
    process.

    Parameters:
        - input_list (list of str): The list of AMINOcode-encoded strings.
        - detail (str): Set details in coding. 'd' for details in digits; 'p'
          for details on punctuation; 'dp' or 'pd' for both. Default is 'dp'.
        - verbose (bool): If True, displays progress during decoding.

    Returns:
        - list of str: List of decoded strings.

    Example:
        >>> decoded_list = decode_list(['HYELLYQ', 'YWYQRLD', 'YPW'], 'dp')
        >>> print(decoded_list)
        ['hello', 'world', '!']
    """

    list_size = len(input_list)
    selectedEncoder = lambda x: decode_string(x, detail=detail)
    
    decoded_list = []
    if verbose:
        print('Decoding text...')
    for c, i in enumerate(input_list):
        c += 1
        if verbose and (c+1) % 10000 == 0:
            print(str(c+1)+'/'+str(list_size))
        decoded_list.append(selectedEncoder(str(i)))
    if verbose:
        print(str(list_size)+'/'+str(list_size))
    
    return decoded_list