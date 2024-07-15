"""
Author: Fatih Küçükkarakurt <https://github.com/fkkarakurt>

This Python script provides functionality to scan subdomains of a given domain using the crt.sh database 
and check their availability by sending HTTP requests. It utilizes the aiohttp library for asynchronous 
HTTP requests and concurrent.futures for parallel processing. The script also filters unnecessary subdomains 
and provides progress updates to the user.

The SubdomainScanner class contains methods to fetch subdomains, check their availability, and display 
the results in a tabular format using the rich library for better visualization.

Important:
This tool is intended for educational purposes and ethical use only. 
Users are responsible for obtaining necessary permissions before scanning networks or systems.
"""

import aiohttp
import asyncio
import requests
from rich.console import Console
from rich.table import Table
import threading
import time

class SubdomainScanner:
    def __init__(self):
        self.console = Console()

    @staticmethod
    def get_subdomains(domain):
        """
        Fetches subdomains from crt.sh for a given domain. Filters and returns unique subdomains.
        """
        url = f"https://crt.sh/?q=%25.{domain}&output=json"
        try:
            response = requests.get(url, timeout=10)
            data = response.json()
            subdomain_set = set()
            subdomains = []
            for entry in data:
                name_value = entry['name_value'].strip().lower()
                for sub in name_value.split('\n'):
                    if sub.endswith(f".{domain}") and sub not in subdomain_set:
                        subdomain_set.add(sub)
                        subdomains.append({'subdomain': sub})
            return subdomains
        except Exception as e:
            print(f"Error fetching subdomains: {e}")
            return []

    async def check_subdomain(self, session, subdomain):
        """
        Checks if a subdomain is available by sending an HTTP request.
        """
        try:
            async with session.get(f"http://{subdomain}", timeout=10) as response:
                if response.status != 404:
                    return subdomain
        except Exception:
            return None

    async def check_subdomains(self, subdomains):
        """
        Asynchronously checks the availability of a list of subdomains.
        """
        async with aiohttp.ClientSession() as session:
            tasks = []
            for subdomain in subdomains:
                tasks.append(self.check_subdomain(session, subdomain['subdomain']))
            results = await asyncio.gather(*tasks)
            return [result for result in results if result is not None]

    def display_results(self, found_subdomains):
        """
        Displays the found subdomains in a formatted table using the Rich library.
        """
        self.console.print("[bold blue]Technology Scan Results:[/bold blue]")
        if not found_subdomains:
            self.console.print("[bold red]No subdomains found.[/bold red]")
            return

        table = Table(show_header=True, header_style="bold green", title="[bold]Subdomain Scan Results[/bold]")
        table.add_column("Subdomain", style="blue")

        for subdomain in found_subdomains:
            table.add_row(subdomain)

        self.console.print(table)

    def run(self, domain):
        """
        Main method to run the subdomain scanning process.
        """
        subdomains = self.get_subdomains(domain)
        if not subdomains:
            self.console.print("[bold red]No subdomains found or an error occurred.[/bold red]")
            return

        # Inform the user about the scanning process
        def show_progress():
            self.console.print("[yellow]Scanning subdomains, this may take a while...[/yellow]")
            while not done:
                time.sleep(10)
                self.console.print("[yellow]Still scanning... please wait...[/yellow]")

        done = False
        progress_thread = threading.Thread(target=show_progress)
        progress_thread.start()

        # Asynchronous subdomain scanning
        loop = asyncio.get_event_loop()
        found_subdomains = loop.run_until_complete(self.check_subdomains(subdomains))

        # Stop the progress thread
        done = True
        progress_thread.join()

        self.display_results(found_subdomains)
