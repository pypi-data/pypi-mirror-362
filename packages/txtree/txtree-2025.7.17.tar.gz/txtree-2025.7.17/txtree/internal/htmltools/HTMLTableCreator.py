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

import os
import textwrap

class HTMLTableCreator:
    def __init__(self, style_dir_rel, script_dir_rel,
                 help_search_bar_file_rel, about_file_rel=None,
                 back_button_rel=None, title="HTML Table", columns=None,
                 ):
        # Set the title and columns
        self.title = title
        self.columns = columns if columns else []
        
        # Set directory-related attributes
        self.style_dir_rel = style_dir_rel
        self.script_dir_rel = script_dir_rel
        self.help_search_bar_file_rel = help_search_bar_file_rel
        self.about_file_rel = about_file_rel
        self.back_button_rel = back_button_rel
        
        # Initialize page
        self.rows = []
        self.main_page_content = self.initialize_page()

    def initialize_page(self):
        # Initialize an empty list to store each column header as a string
        columns_header = []

        back_button_html = ""
        if self.back_button_rel:
            back_button_html = f"""
            <!-- Back Button -->
            <a href="{self.back_button_rel}"><button id="backButton">Back</button></a>"""
        
        about_button = ""
        if self.about_file_rel:
            about_button = f"""
                <!-- About Button -->
                <a href="{self.about_file_rel}" target="_blank">
                    <button id="aboutButton">About HTML-TM</button>
                </a>"""

        for index, col in enumerate(self.columns):
            header = f'<th>{col}</th>'
            columns_header.append(header)

        columns_header = ''.join(columns_header)

        return f"""
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <title>{self.title}</title>
            <link class="theme-style-sheet" rel="stylesheet" type="text/css" href="{self.style_dir_rel}/table_dark.css" media="(prefers-color-scheme: dark)">
            <link class="theme-style-sheet" rel="stylesheet" type="text/css" href="{self.style_dir_rel}/table_light.css" media="(prefers-color-scheme: light)">
            <script src="{self.script_dir_rel}/table.js"></script>
        </head>
        <body>
            <!-- Overlay that appears during sorting -->
            <div id="blocking-overlay">
            </div>{back_button_html}
            <div id="top-right-corner-container">
                <button id="toggle-theme-button" onclick="toggleTheme()">Toggle Theme</button>{about_button}
            </div>
            <br>
            <h1>{self.title}</h1>
            <div id="input-container">
                <input
                    type="text" 
                    id="search-input" 
                    placeholder="Search query"
                >
                <input
                    type="text" 
                    id="neighbors-number-input" 
                    placeholder="Neighbors number"
                >
            </div>
            <br>
            <button id="search-button" onclick="searchTable()">Search</button>
            <!-- Button that redirects to the help page -->
            <a href="{self.help_search_bar_file_rel}" target="_blank">
                <button id="helpButton">Help</button>
            </a>
            <br><br>
            <div id="counting-container">
                <div id="text">
                    <span id="total-entries"></span>
                    <span id="filtered-entries"></span>
                </div>
                <div>
                    <!-- Button to export to CSV -->
                    <button id="export-csv-button">Export CSV</button>
                    <!-- Button to clear all filters -->
                    <button id="clearFiltersButton">Clear Filters</button>
                </div>
            </div>
            <table id="dataTable">
                <thead>
                    <tr>
                        {columns_header}
                    </tr>
                    <tr>
                        {''.join([f'<th>{i}</th>' for i in range(0,index+1)])}
                    </tr>
                </thead>
        """

    def add_row(self, row_data):
        if len(row_data) != len(self.columns):
            raise ValueError("Row data must match the number of columns")

        row = ''.join(f'<td>{data}</td>' for data in row_data)
        self.rows.append(f'<tr>{row}</tr>')

    def save_html(self, html_file):    
        # Generate the HTML with the added lines
        rows_html = ''.join(self.rows)
        finished_page = self.main_page_content + " "*8 + rows_html + """
                </tbody>
            </table>
        </body>
        </html>
        """

        # Save the HTML to the output directory
        finished_page = textwrap.dedent(finished_page).strip()
        os.makedirs(os.path.dirname(html_file), exist_ok=True)
        with open(html_file, 'w', encoding='utf-8') as f:
            f.write(finished_page)

    @staticmethod
    def save_style(style_dir):
        assets_dir = os.path.join(os.path.dirname(__file__),
                                  "htmltools_assets")
        css_files = ["table_light.css", "table_dark.css"]
        for f in css_files:
            css_source = os.path.join(assets_dir, f)
            with open(css_source, 'r', encoding='utf-8') as css_file:
                css_content = css_file.read()
        
            # Save the CSS content to the specified path
            css_content = textwrap.dedent(css_content).strip()
            os.makedirs(style_dir, exist_ok=True)
            css_file = os.path.join(style_dir, f)
            with open(css_file, 'w', encoding='utf-8') as f:
                f.write(css_content)

    @staticmethod
    def save_script(script_dir):
        assets_dir = os.path.join(os.path.dirname(__file__),
                                  "htmltools_assets")
        js_source = os.path.join(assets_dir, "table.js")
        with open(js_source, 'r', encoding='utf-8') as js_file:
            js_content = js_file.read()
            
        # Save the JS content to the specified path
        js_content = textwrap.dedent(js_content).strip()
        os.makedirs(script_dir, exist_ok=True)
        script_file = f'{script_dir}/table.js'
        with open(script_file, 'w', encoding='utf-8') as f:
            f.write(js_content)
    
    @staticmethod
    def save_help_search_bar(help_search_bar_dir, style_dir_rel,
                             script_dir_rel, file_name='help_search_bar.html',
                             back_button_rel=None):
        assets_dir = os.path.join(os.path.dirname(__file__),
                                  "htmltools_assets")
        help_html_source = os.path.join(assets_dir, "help_search_bar.html")
        
        script_file_rel = f'{script_dir_rel}/table.js'
        
        back_button_html = ""
        if back_button_rel:
            back_button_html = f"""
            <!-- Back Button -->
            {' '*4}<a href="{back_button_rel}"><button id="backButton">Back</button></a>"""
            back_button_html = textwrap.dedent(back_button_html).strip()
        
        with open(help_html_source, 'r', encoding='utf-8') as help_html_file:
            help_html_content = help_html_file.read()
        help_html_content = help_html_content.format(
            style_dir_rel=style_dir_rel,
            script_file_rel=script_file_rel,
            back_button_html=back_button_html)
        help_search_bar_file = (f'{help_search_bar_dir}/{file_name}')
        with open(help_search_bar_file, 'w', encoding='utf-8') as f:
            f.write(help_html_content)
    
    @staticmethod
    def add_file_link(text, file_path, popup=False, open_in_new_tab=False):
        """
        Wraps a string in a <a href="file:"> tag, with options to open it in a popup or in a new window/tab.

        Args:
            text (str): The clickable text for the link.
            file_path (str): The file path for the link.
            popup (bool): If True, opens the link in a popup window.
            open_in_new_tab (bool): If True, opens the link in a new tab or window (without a popup).

        Returns:
            str: An HTML-formatted string with the link.
        """
        if popup:
            # Escape backslashes for JavaScript string handling
            safe_file_path = file_path.replace('\\', '\\\\')
            return f'<a href="file:{file_path}" onclick="window.open(\'file:{safe_file_path}\', \'_blank\', \'width=800,height=600,scrollbars=yes,resizable=yes\'); return false;">{text}</a>'
        elif open_in_new_tab:
            return f'<a href="file:{file_path}" target="_blank">{text}</a>'
        else:
            return f'<a href="file:{file_path}">{text}</a>'
            
    @staticmethod
    def add_site_link(text, url, popup=False, open_in_new_tab=False):
        """
        Wraps a string in a <a href="URL"> tag, with options to open it in a popup or in a new window/tab.

        Args:
            text (str): The clickable text for the link.
            url (str): The URL for the link.
            popup (bool): If True, opens the link in a popup window.
            open_in_new_tab (bool): If True, opens the link in a new tab or window (without a popup).

        Returns:
            str: An HTML-formatted string with the link.
        """
        if popup:
            return f'<a href="{url}" onclick="window.open(\'{url}\', \'_blank\', \'width=800,height=600,scrollbars=yes,resizable=yes\'); return false;">{text}</a>'
        elif open_in_new_tab:
            return f'<a href="{url}" target="_blank">{text}</a>'
        else:
            return f'<a href="{url}">{text}</a>'
