"""
Directory Scanner

This Python script is crafted to automate the process of scanning for accessible directories on a specified web server. 
Utilizing a list of potential directory names (wordlist), it attempts to discover directories by making HTTP requests 
and analyzing the responses. The script is optimized for performance through the use of concurrent requests, 
leveraging Python's ThreadPoolExecutor for parallel execution. It further enhances user experience by visually displaying 
scan results in a tabular format using the Rich library.

The DirectoryScanner class encapsulates the scanning logic, offering methods to handle URL redirections, 
perform the directory scan based on the provided wordlist, and display found directories in a structured table. 
It gracefully handles network errors and suppresses SSL warnings to focus on the scanning process.

Key Components:
- URL finalization with redirection handling.
- Concurrent directory scanning with adjustable thread count for improved efficiency.
- Results presentation in a table format, providing a clear and concise overview of found directories.

Important:
This tool is intended for educational and ethical testing purposes only. 
Always seek permission before conducting scans on websites.

Author: Fatih Küçükkarakurt <https://github.com/fkkarakurt>
Created: 2024-02-15
Last Updated: 2024-02-18
"""


import requests
from concurrent.futures import ThreadPoolExecutor, as_completed
import urllib3
from rich.console import Console
from rich.table import Table

# To suppress security warnings
urllib3.disable_warnings()

class DirectoryScanner:
    
    def __init__(self, base_url, wordlist_file, max_threads=50):
        self.console = Console()
        self.original_base_url = base_url
         # Check redirects and get final URL
        self.base_url = self.get_final_url(base_url) 
        self.wordlist_file = wordlist_file
        self.max_threads = max_threads

    def get_final_url(self, base_url):
        try:
            response = requests.get(base_url, timeout=10, verify=False, allow_redirects=True)
            final_url = response.url
            # Remove extra '/' character at the end of URL
            final_url = final_url.rstrip('/')
            if response.history and final_url != base_url.rstrip('/'):
                self.console.print(f"Redirect detected: {base_url} -> {final_url}", style="yellow")
                return final_url
            return base_url.rstrip('/')
        except requests.RequestException as e:
            self.console.print(f"An error occurred while checking the URL: {e}", style="bold red")
            return base_url.rstrip('/')

    def _scan_directory(self, directory):
        url = f"{self.base_url}/{directory}"
        try:
            # Turn off following referrals
            response = requests.get(url, timeout=10, verify=False, allow_redirects=False)  
            if response.status_code == 200:
                # Accept URLs that directly receive a 200 status code
                return url  
            # Redirect status codes
            elif response.status_code in [301, 302, 303, 307, 308]:  
                # Get redirect URL
                redirected_url = response.headers.get('Location', '')  
                if not redirected_url.startswith(self.base_url):
                    return None
                else:
                    # Return the URL to further examine this situation
                    return url 
        except requests.RequestException:
            pass
        return None

    def scan_directories(self):
        found_directories = []
        with open(self.wordlist_file, 'r') as file:
            directories = file.read().splitlines()

        with ThreadPoolExecutor(max_workers=self.max_threads) as executor:
            futures = [executor.submit(self._scan_directory, directory) for directory in directories]

            for future in as_completed(futures):
                result = future.result()
                if result:
                    found_directories.append(result)

        return found_directories

    def display_results(self, results):
        print("\n")
        table = Table(show_header=True, header_style="bold green", title="[bold]Directory Scan Results[/bold]")
        table.add_column("Found Directories", style="blue")
        for result in results:
            table.add_row(result)
        self.console.print(table)
