"""
JavaScript File Scanner

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
    """
    A class to scan and identify JavaScript files within a given web page.

    Attributes:
    url (str): The URL of the web page to be scanned.
    console (Console): Rich library console object for formatted output.

    Methods:
    find_javascript_files(): Finds and returns a list of JavaScript file URLs.
    display_results(js_files): Displays the JavaScript file URLs in a formatted table.
    """
    def __init__(self, url):
        """
        Initializes the JSScanner with a target URL.

        Parameters:
        url (str): The URL of the web page to be scanned.
        """
        self.url = url
        self.console = Console()

    def find_javascript_files(self):
        """
        Scans the specified URL to find JavaScript files.

        Returns:
        list: A list of JavaScript file URLs found on the web page.
        """
        js_files = []
        try:
            response = requests.get(self.url)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')
            script_tags = soup.find_all('script')

            for script in script_tags:
                if script.get('src'):
                    js_url = urljoin(self.url, script.get('src'))
                    js_files.append(js_url)
        except requests.RequestException as e:
            self.console.print(f"Error: {e}", style="red")
        return js_files

    def display_results(self, js_files):
        """
        Displays the JavaScript file URLs in a formatted table.

        Parameters:
        js_files (list): A list of JavaScript file URLs to be displayed.
        """
        table = Table(show_header=True, header_style="bold green", title="[bold]JavaScript Files[/bold]")
        table.add_column("File URL", style="blue")

        for js_file in js_files:
            table.add_row(js_file)
        
        self.console.print(table)
