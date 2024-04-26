"""
HTTP Headers Scanner

This script is designed to fetch and display the HTTP headers of a given URL. Leveraging the requests library to 
make HTTP requests and the rich library for output formatting, it aims to provide a quick and efficient way to 
inspect the HTTP headers that a web server returns. The inclusion of a custom text wrapping function enhances the 
readability of long header values, making it easier to analyze the headers in detail.

The HTTPHeadersScanner class encapsulates the functionality to retrieve HTTP headers and display them in a 
user-friendly table format. It handles network errors gracefully, ensuring that users are informed of any 
issues encountered during the header retrieval process. This tool is particularly useful for web developers, 
security researchers, and IT professionals who need to quickly assess the security headers or other HTTP 
header configurations of a website.

Features:
- Fetches HTTP headers for a specified URL.
- Displays headers and their values in a neatly formatted table.
- Automatically wraps long header values for improved readability.

Important:
This script is intended for informational and educational purposes. It can be used to evaluate the security 
and configuration of web servers. Always ensure you have the right to access and analyze the headers of the 
target URL.

Author: Fatih Küçükkarakurt <https://github.com/fkkarakurt>
Created: 2024-02-10
Last Updated: 2024-02-18
"""


import requests
import time

from src.textwrap import wrap_text

from rich.console import Console
from rich.table import Table

class HTTPHeadersScanner:
    def __init__(self, url):
        self.url = url
        self.console = Console()

    def get_http_headers(self):
        try:
            response = requests.get(self.url)
            headers = dict(response.headers)
            return headers
        except requests.exceptions.RequestException as e:
            self.console.print(f"Error retrieving HTTP headers: {e}", style="red")
            return {}
        
    def display_results(self, headers):
        table = Table(show_header=True, header_style="bold green", title="[bold]HTTP Headers Results[/bold]")
        table.add_column("Header", style="blue", no_wrap=True)
        table.add_column("Value", style="magenta")
        for header, value in headers.items():
            table.add_row(header, wrap_text(value, 40))
        self.console.print(table)