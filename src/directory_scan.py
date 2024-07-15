"""
Directory Scanner

This Python script is crafted to automate the process of scanning for accessible directories on a specified web server.
Utilizing a list of potential directory names (wordlist), it attempts to discover directories by making HTTP requests
and analyzing the responses. The script is optimized for performance through the use of concurrent requests,
leveraging Python's asyncio and aiohttp libraries for parallel execution. It further enhances user experience by visually displaying
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

import asyncio
import aiohttp
from rich.console import Console
from rich.table import Table

class DirectoryScanner:
    
    def __init__(self, base_url, wordlist_file, max_concurrent_tasks=100):
        self.console = Console()
        self.original_base_url = base_url
        self.wordlist_file = wordlist_file
        self.max_concurrent_tasks = max_concurrent_tasks

    async def initialize(self):
        self.base_url = await self.get_final_url(self.original_base_url)

    async def get_final_url(self, base_url):
        async with aiohttp.ClientSession() as session:
            try:
                async with session.get(base_url, timeout=20, ssl=False, allow_redirects=True) as response:
                    final_url = str(response.url).rstrip('/')
                    if len(response.history) > 0 and final_url != base_url.rstrip('/'):
                        self.console.print(f"Redirect detected: {base_url} -> {final_url}", style="yellow")
                    return final_url
            except aiohttp.ClientError as e:
                self.console.print(f"An error occurred while checking the URL: {e}", style="bold red")
                return base_url.rstrip('/')

    async def _scan_directory(self, session, directory):
        url = f"{self.base_url}/{directory}"
        try:
            async with session.get(url, timeout=20, ssl=False, allow_redirects=False) as response:
                if response.status == 200:
                    return url
                elif response.status in [301, 302, 303, 307, 308]:
                    redirected_url = response.headers.get('Location', '')
                    if not redirected_url.startswith(self.base_url):
                        return None
                    else:
                        return url
        except (aiohttp.ClientError, asyncio.TimeoutError):
            pass
        return None

    async def scan_directories(self):
        found_directories = []
        with open(self.wordlist_file, 'r') as file:
            directories = file.read().splitlines()

        async with aiohttp.ClientSession() as session:
            tasks = []
            for i, directory in enumerate(directories):
                if len(tasks) >= self.max_concurrent_tasks:
                    done, pending = await asyncio.wait(tasks, return_when=asyncio.FIRST_COMPLETED)
                    for task in done:
                        result = task.result()
                        if result:
                            found_directories.append(result)
                    tasks = [task for task in pending]
                tasks.append(asyncio.create_task(self._scan_directory(session, directory)))

                # Print progress every 100 directories
                if i % 100 == 0:
                    self.console.print(f"[yellow]Scanned {i}/{len(directories)} directories...[/yellow]")

            # Wait for any remaining tasks to complete
            if tasks:
                done, _ = await asyncio.wait(tasks)
                for task in done:
                    result = task.result()
                    if result:
                        found_directories.append(result)

        self.console.print(f"[green]Scanned all {len(directories)} directories.[/green]")
        return found_directories

    def display_results(self, results):
        print("\n")
        table = Table(show_header=True, header_style="bold green", title="[bold]Directory Scan Results[/bold]")
        table.add_column("Found Directories", style="blue")
        for result in results:
            table.add_row(result)
        self.console.print(table)
