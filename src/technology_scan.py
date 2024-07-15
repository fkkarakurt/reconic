"""
Author: Fatih Küçükkarakurt <https://github.com/fkkarakurt>
Created: 2024-07-15
Last Updated: 2024-07-15
"""

from Wappalyzer import Wappalyzer, WebPage
import requests
from rich.console import Console
from rich.table import Table
import warnings
import datetime

console = Console()

# Ignore user warnings
warnings.filterwarnings("ignore", category=UserWarning)

def get_cve_details_link(technology):
    return f"https://cve.mitre.org/cgi-bin/cvekey.cgi?keyword={technology.replace(' ', '%20')}"

class TechnologyScanner:
    def __init__(self, url):
        self.url = url
        self.technologies = {}

    def scan_technologies(self):
        wappalyzer = Wappalyzer.latest()
        try:
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36"
            }
            response = requests.get(self.url, headers=headers)
            webpage = WebPage.new_from_response(response)
            self.technologies = wappalyzer.analyze_with_versions_and_categories(webpage)
        except Exception as e:
            console.print(f"[bold red]Error scanning technologies: {e}[/bold red]")

    def display_results(self):
        console.print("[bold blue]Technology Scan Results:[/bold blue]")
        if not self.technologies:
            console.print("[bold red]No technologies found.[/bold red]")
        else:
            table = Table(show_header=True, header_style="bold green", title="[bold]Technology Scan Results[/bold]")
            table.add_column("Technology", style="blue", justify="center")
            table.add_column("Categories", style="magenta")

            for tech, details in self.technologies.items():
                name = tech
                categories = ", ".join(details.get("categories", []))
                table.add_row(name, categories)
            
            console.print(table)

    def get_results(self):
        if not self.technologies:
            return {"No technologies found."}
        return self.technologies

def display_cve_links(technologies):
    console.print("[bold blue]Possible Related CVE Links:[/bold blue]")
    if not technologies:
        console.print("[bold red]No technologies found.[/bold red]")
    else:
        table = Table(show_header=True, header_style="bold green", title="[bold]CVE Links for Technologies[/bold]")
        table.add_column("Technology", style="blue", justify="center")
        table.add_column("CVE Link", style="magenta")

        for tech in technologies.keys():
            details_link = get_cve_details_link(tech)
            table.add_row(tech, details_link)
        
        console.print(table)
