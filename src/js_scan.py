"""
JavaScript File Scanner

This Python script is designed to identify and list all JavaScript files linked within a given web page. 
Utilizing the powerful combination of the requests library for HTTP requests and BeautifulSoup for parsing 
HTML, it efficiently locates <script> tags and extracts the URLs of external JavaScript files. The results 
are presented in an aesthetically pleasing table format thanks to the rich library, making it easier for 
users to review and analyze the JavaScript resources included in a web page.

The JSScanner class is at the core of this script, providing methods to fetch the HTML content of the specified 
URL, parse it to find <script> tags with 'src' attributes, and compile a list of the absolute URLs of these 
JavaScript files. It also includes error handling to manage request failures gracefully.

Features:
- Automatic discovery of JavaScript files embedded in a web page.
- Extraction of both inline and external JavaScript file URLs.
- Presentation of findings in a clear and structured table format.

Important:
This tool is aimed at web developers, security auditors, and SEO specialists who need to assess the JavaScript 
assets of a web page for optimization, security analysis, or compliance purposes. It simplifies the process of 
auditing web page resources by automating the discovery of JavaScript files.

Please use this tool responsibly and ethically, ensuring permission is obtained before scanning websites.

Author: Fatih Küçükkarakurt <https://github.com/fkkarakurt>
Created: 2024-02-08
Last Updated: 2024-02-18
"""


import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from rich.console import Console
from rich.table import Table

class JSScanner:
    def __init__(self, url):
        self.url = url
        self.console = Console()

    def find_javascript_files(self):
        js_files = []
        try:
            response = requests.get(self.url)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')
            script_tags = soup.find_all('script')

            for script in script_tags:
                if script.get('src'):
                    js_url = urljoin(self.url, script.get('src'))
                    # Just add js_url to the list
                    js_files.append(js_url)  
        except requests.RequestException as e:
            self.console.print(f"Error: {e}", style="red")
        return js_files

    def display_results(self, js_files):
        table = Table(show_header=True, header_style="bold green", title="[bold]JavaScript Files[/bold]")
        table.add_column("File URL", style="blue")
        # Iterate directly on js_file
        for js_file in js_files:  
            # Add js file directly without using tuple unpacking
            table.add_row(js_file)  
        self.console.print(table)

