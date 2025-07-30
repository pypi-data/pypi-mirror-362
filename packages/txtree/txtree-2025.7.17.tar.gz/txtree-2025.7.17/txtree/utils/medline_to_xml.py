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
from xml.dom import minidom
from Bio import Medline
from tqdm import tqdm

def medline_to_xml(file_path, output_xml_path, verbose=True):
    """
    Converts a PubMed Medline file to an XML format progressively.

    This function reads a Medline file, counts the number of records, 
    and then processes each record one by one, extracting specific fields
    and converting them into an XML format.

    Parameters:
        - file_path (str): Path to the input Medline file
          (e.g., pubmed.txt).
        - output_xml_path (str): Path to the output XML file
          (e.g., pubmed.xml).
        - verbose (bool): If True, displays alert messages and progress bar.
          If False, disables them. Default is True.
    """

    total_records = None
    if verbose:
        print("Counting the records in the Medline file. This may take some "
              "time...")

        # Count the number of entries before processing
        with open(file_path, encoding='utf-8') as handle:
            # Count the records without loading everything into memory
            total_records = sum(1 for _ in Medline.parse(handle))

        print(f"Counting complete. Total number of records: {total_records}")

    # Open output file for writing XML progressively
    with open(output_xml_path, 'wb') as xml_file:
        xml_file.write(b'<?xml version="1.0" encoding="UTF-8"?>\n')
        xml_file.write(b'<root>\n')

        # Open and parse the Medline file progressively
        with open(file_path, encoding='utf-8') as handle:
            records = Medline.parse(handle)
            # Use tqdm to show progress while parsing the file
            for record in tqdm(records, total=total_records,
                               desc="Processing records", ncols=0,
                               disable=not verbose):
                # Extract required fields
                ti = record.get('TI', '')
                ab = record.get('AB', '')
                dp = record.get('DP', '')
                pmid = record.get('PMID', '')

                # Extract DOI from 'AID' field
                aid = record.get('AID', [])
                doi = ''
                for item in aid:
                    aid_s = item.split(' ')
                    if len(aid_s) > 1 and '[doi]' in aid_s[1].lower():
                        doi = aid_s[0]

                # Create an XML element for the record
                record_element = ET.Element("entry")

                # Add Title if not empty
                if ti:
                    title = ET.SubElement(record_element, "title")
                    title.text = ti
        
                # Add Abstract if not empty
                if ab:
                    abstract = ET.SubElement(record_element, "abstract")
                    abstract.text = ab
        
                # Add PublicationYear if not empty
                if dp:
                    year = ET.SubElement(record_element, "publication_year")
                    year.text = dp[:4]
        
                # Add DOI if available
                if doi:
                    doi_element = ET.SubElement(record_element, "doi")
                    doi_element.text = doi
        
                # Add PMID if not empty
                if pmid:
                    pmid_element = ET.SubElement(record_element, "pmid")
                    pmid_element.text = pmid

                # Write the record XML to the file
                record_str = ET.tostring(record_element, encoding='utf-8')
                pretty_record_str = minidom.parseString(
                    record_str).toprettyxml(indent="  ", newl="\n")
                # Remove header
                pretty_record_str = '\n'.join(pretty_record_str.split('\n')[1:])
                xml_file.write(pretty_record_str.encode('utf-8'))

        # Close the root element
        xml_file.write(b'</root>\n')