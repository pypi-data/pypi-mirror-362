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
import re

class HTMLSVGCreator:

    @staticmethod
    def generate_css(css_path):
        css_content = """
        body, html {
            font-family: 'Arial', sans-serif;
            margin: 0;
            padding: 0;
            height: 100%;
            width: 100%;
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            background-color: #f4f6f9; /* Updated background color */
        }

        h1 {
            text-align: center;
            color: #333; /* Text color */
        }

        .svg-container {
            align-items: center; /* Centers items horizontally in the flex container */
            display: flex; /* Enables flexbox layout */
            flex-direction: column; /* Arranges items in a vertical column */
            width: 100%; /* Sets the container width to 100% of the parent element */
            height: 90vh; /* Adjusts the height to occupy 90% of the viewport height */
            justify-content: center; /* Vertically centers the content within the container */
        }

        svg {
            margin: 0px;
        }

        #button-container {
            display: flex;
            gap: 10px;
            margin-top: 20px; /* Added margin-top for spacing */
        }

        button {
            padding: 8px 15px;
            font-size: 16px;
            cursor: pointer;
            background-color: #59759A; /* Primary color */
            color: white; /* Button text color */
            border: none;
            border-radius: 4px;
            transition: background-color 0.3s ease;
        }

        /* Button hover effect */
        button:hover {
            background-color: #475e75; /* Darker shade for hover effect */
        }

        /* Button focus effect */
        button:focus {
            outline: 2px solid #59759A; /* Primary color for focus outline */
            outline-offset: 2px;
        }
        """
        
        css_content = textwrap.dedent(css_content).strip()
        with open(css_path, 'w', encoding='utf-8') as css_file:
            css_file.write(css_content)

    @staticmethod
    def generate_js(js_path, svg_download='image.svg',
                    png_download='image.png'):
        js_content = f"""
        function saveAsSVG() {{
            const svgContent = document.querySelector('svg').outerHTML;
            const blob = new Blob([svgContent], {{ type: 'image/svg+xml' }});
            const link = document.createElement('a');
            
            link.href = URL.createObjectURL(blob);
            link.download = '{svg_download}';
            link.click();
            
            URL.revokeObjectURL(link.href);
        }}
    
        function saveAsPNG() {{
            const svgElement = document.querySelector('svg');
            const svgData = new XMLSerializer().serializeToString(svgElement);
            const canvas = document.createElement('canvas');
            const ctx = canvas.getContext('2d');
            const img = new Image();
        
            const svgRect = svgElement.getBoundingClientRect();
        
            // Define the desired DPI (dots per inch)
            const dpi = 300;
        
            // Calculate the adjusted dimensions based on the DPI
            // 96 is the default DPI of the browser
            canvas.width = (svgRect.width * dpi) / 96;
            canvas.height = (svgRect.height * dpi) / 96;
        
            img.onload = function() {{
                // Adjust the scaling to maintain quality
                ctx.drawImage(img, 0, 0, canvas.width, canvas.height);
                const pngLink = document.createElement('a');
                pngLink.href = canvas.toDataURL('image/png');
                pngLink.download = 'image.png';
                pngLink.click();
            }};
        
            // Encode the SVG data to handle UTF-8 characters
            const encodedSvgData = encodeURIComponent(svgData)
                .replace(/%([0-9A-F]{{2}})/g, (match, p1) => String.fromCharCode('0x' + p1));
        
            img.src = 'data:image/svg+xml;base64,' + btoa(encodedSvgData);
        }}
        
        // Adjust the SVG size when the page is loaded
        window.addEventListener('load', adjustSvgSize);
        
        function adjustSvgSize() {{
            var svg = document.getElementById('svgElement');
        
            // Check if the SVG element exists and has a viewBox attribute
            if (!svg || !svg.viewBox || !svg.viewBox.baseVal ||
                svg.viewBox.baseVal.width === 0 ||
                svg.viewBox.baseVal.height === 0) {{
                return; // Exit the function if no valid viewBox is present
            }}
        
            // Get the original dimensions of the SVG
            var svgWidth = svg.viewBox.baseVal.width;
            var svgHeight = svg.viewBox.baseVal.height;
        
            // Calculate the aspect ratio based on the original SVG dimensions
            var aspectRatio = svgWidth / svgHeight;
        
            // Get the viewport dimensions, adjusting for zoom using
        	// devicePixelRatio
            var viewportWidth = window.innerWidth * window.devicePixelRatio;
            var viewportHeight = window.innerHeight * window.devicePixelRatio;
        
            // Define the SVG dimensions based on the window's width
            var scale = 0.75;  
            var newWidth = viewportWidth * scale;
            var newHeight = newWidth / aspectRatio;
        
            // Adjust the SVG dimensions to fit within the viewport height if
            // necessary
            if (newHeight > viewportHeight * scale) {{
                newHeight = viewportHeight * scale;
                newWidth = newHeight * aspectRatio;
            }}
        
            // Update the SVG's width and height attributes with fixed values
            // in pixels
            svg.setAttribute('width', newWidth + 'px');
            svg.setAttribute('height', newHeight + 'px');
        
            // Adjust the viewBox to maintain the aspect ratio while fitting
            // the SVG
            svg.setAttribute('viewBox', '0 0 ' + svgWidth + ' ' + svgHeight);
        }}
        
        ///////////////////////////////////////////////////////////////////////
        // Function to toggle the stylesheet between "table_light.css" and "table_dark.css"
        function toggleTheme() {{
            // Retrieve the current theme setting
            let currentValue = getThemeSetting();
            // Convert the stored string to a boolean
            let isTrue = currentValue === 'true';
            // Invert the boolean value
            let newValue = !isTrue;
            // Store the new value
            setThemeSetting(newValue);

            // Call the function to apply the inverted theme
            html_tm_invert_theme();
        }}

        // Function to switch between light and dark themes
        function html_tm_invert_theme() {{
            // Get all elements with the class "theme-style-sheet"
            const linkElements = document.getElementsByClassName("theme-style-sheet");

            // Iterate over each element with the class
            Array.from(linkElements).forEach(linkElement => {{
                // Get the current href attribute value
                const currentHref = linkElement.getAttribute("href");

                // Extract the basePath from the current href
                // Finds the last "/" and takes the substring up to that point
                const basePath = currentHref.substring(0, currentHref.lastIndexOf("/") + 1);

                // Define the filenames for the light and dark themes
                const lightTheme = "table_light.css";
                const darkTheme = "table_dark.css";

                // Toggle between the light and dark themes
                if (currentHref === basePath + lightTheme) {{
                    // If the current theme is light, switch to dark
                    linkElement.setAttribute("href", basePath + darkTheme);
                }} else {{
                    // Otherwise, switch to light
                    linkElement.setAttribute("href", basePath + lightTheme);
                }}
            }});
        }}

        // Function to apply the theme when the page loads
        function applyThemeOnLoad() {{
            // Check the value stored in the theme setting
            let currentValue = getThemeSetting();
            // Convert the stored string to a boolean
            let isTrue = currentValue === 'true';

            // If the dark theme is enabled, apply the dark theme
            if (isTrue) {{
                html_tm_invert_theme();
            }}
        }}

        // Apply the theme when the page loads
        window.onload = applyThemeOnLoad;

        // Helper function to set a cookie
        function setCookie(name, value, days) {{
            let expires = "";
            if (days) {{
                let date = new Date();
                date.setTime(date.getTime() + (days * 24 * 60 * 60 * 1000));
                expires = "; expires=" + date.toUTCString();
            }}
            // Add SameSite and Secure attributes
            document.cookie = name + "=" + (value || "") + expires + "; path=/; SameSite=None; Secure";
        }}

        // Helper function to get a cookie
        function getCookie(name) {{
            let nameEQ = name + "=";
            let ca = document.cookie.split(';');
            for (let i = 0; i < ca.length; i++) {{
                let c = ca[i];
                while (c.charAt(0) === ' ') c = c.substring(1, c.length);
                if (c.indexOf(nameEQ) === 0) return c.substring(nameEQ.length, c.length);
            }}
            return null;
        }}

        // Function to detect if the browser is Firefox
        function isFirefox() {{
            return navigator.userAgent.toLowerCase().indexOf('firefox') > -1;
        }}

        // Function to get the theme setting (cookie or localStorage)
        function getThemeSetting() {{
            if (isFirefox()) {{
                // Use cookies in Firefox
                return getCookie('html_tm_invert_theme');
            }} else {{
                // Use localStorage in other browsers
                return localStorage.getItem('html_tm_invert_theme');
            }}
        }}

        // Function to set the theme setting (cookie or localStorage)
        function setThemeSetting(value) {{
            if (isFirefox()) {{
                // Use cookies in Firefox
                setCookie('html_tm_invert_theme', value, 365);
            }} else {{
                // Use localStorage in other browsers
                localStorage.setItem('html_tm_invert_theme', value);
            }}
        }}

        /*
        Reason for choosing between localStorage and cookies:
        - This application is designed to run using the `file://` protocol (local files).
        - Based on tests executed with the default configurations of the browsers:
          - In Chromium-based browsers (like Chrome, Edge, Brave, etc.),
            `localStorage` works reliably with the `file://` protocol.
          - In Firefox, `localStorage` does not work reliably with `file://`,
            but cookies do.
        Therefore, this approach ensures that the theme is stored and retrieved correctly
        when the application is accessed via `file://`.
         */
        """
        
        js_content = textwrap.dedent(js_content).strip()
        with open(js_path, 'w', encoding='utf-8') as js_file:
            js_file.write(js_content)

    @staticmethod
    def generate_html(svg_path, css_dir_rel, js_file_rel, html_path,
                      page_title="SVG Display", back_button_rel=None,
                      default_theme='dark'):
        if not os.path.isfile(svg_path):
            raise FileNotFoundError(f"The SVG file at {svg_path} does not exist.")
        
        back_button_html = ""
        if back_button_rel:
            back_button_html = f"""
            <!-- Back Button -->
            <a href="{back_button_rel}"><button id="backButton">Back</button></a>"""
        with open(svg_path, 'r', encoding='utf-8') as svg_file:
            svg_content = svg_file.read()
        
        svg_content = re.sub(r'<title>.*?</title>', '', svg_content)
        svg_content = re.sub(r'<svg ', '<svg id="svgElement" ',
                     svg_content)
        
        # Remove leading whitespace and dedent the SVG content to ensure
        # consistent formatting
        svg_content = textwrap.dedent(svg_content).strip()
        
        # Split the SVG content into individual lines for processing
        lines = svg_content.splitlines()
        
        # Skip the first line (to leave it unchanged) and add 16 spaces to the
        # beginning of all remaining lines.
        # The first line is skipped because it already receives extra spaces
        # in the formatting of the `html_content` string.
        svg_content = [lines[0]] + [" " * 20 + line for line in lines[1:]]
        
        # Join the lines back together into a single string with line breaks
        svg_content = "\n".join(svg_content)
        
        # Create the HTML content with the processed SVG embedded
        html_content = f"""
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>{page_title}</title>
            <link class="theme-style-sheet" rel="stylesheet" type="text/css" href="{css_dir_rel}/table_dark.css" media="(prefers-color-scheme: dark)">
            <link class="theme-style-sheet" rel="stylesheet" type="text/css" href="{css_dir_rel}/table_light.css" media="(prefers-color-scheme: light)">
            <script src="{js_file_rel}"></script>
        </head>
        <body class="svg-body">{back_button_html}
            <div id="top-right-corner-container">
                <button id="toggle-theme-button" onclick="toggleTheme()">Toggle Theme</button>
            </div>
            <div class="svg-container">
                <h1>{page_title}</h1>
                    {svg_content}
                <div id="button-container">
                    <button onclick="saveAsSVG()">Save as SVG</button>
                    <button onclick="saveAsPNG()">Save as PNG</button>
                </div>
            </div>
        </body>
        </html>
        """
        
        html_content = textwrap.dedent(html_content).strip()
        with open(html_path, 'w', encoding='utf-8') as html_file:
            html_file.write(html_content)