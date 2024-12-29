"""
Technology Scanner

This script scans a given URL to identify the technologies used on the webpage. It utilizes the Wappalyzer 
library to analyze the webpage and extract information about the technologies. The results are presented 
in a user-friendly table format using the Rich library. Additionally, the script provides links to 
potentially related CVEs for each identified technology.

Features:
- Identifies technologies used on a webpage.
- Displays the technology details in a formatted table.
- Provides links to potentially related CVEs for each identified technology.

Important:
This tool is useful for web developers, security auditors, and SEO specialists who need to understand the 
technological stack of a website. It helps in performing security audits, optimization, and compliance checks.

Please use this tool responsibly and ethically, ensuring permission is obtained before scanning websites.

Author: Fatih Küçükkarakurt <https://github.com/fkkarakurt>
Created: 2024-07-15
Last Updated: 2024-07-15
"""

from Wappalyzer import Wappalyzer, WebPage
import requests
from rich.console import Console
from rich.table import Table
import warnings

# Create a console object for formatted output
console = Console()

# Ignore user warnings
warnings.filterwarnings("ignore", category=UserWarning)

def get_cve_details_link(technology):
    """
    Generates a CVE details link for the given technology.

    Parameters:
    technology (str): The name of the technology.

    Returns:
    str: A URL link to the CVE details page for the technology.
    """
    return f"https://cve.mitre.org/cgi-bin/cvekey.cgi?keyword={technology.replace(' ', '%20')}"

class TechnologyScanner:
    """
    A class to scan and identify technologies used on a webpage.

    Attributes:
    url (str): The URL of the webpage to be scanned.
    technologies (dict): A dictionary to store the identified technologies and their details.

    Methods:
    scan_technologies(): Scans the webpage and identifies the technologies used.
    display_results(): Displays the identified technologies in a formatted table.
    get_results(): Returns the identified technologies.
    """
    
    def __init__(self, url):
        """
        Initializes the TechnologyScanner with a target URL.

        Parameters:
        url (str): The URL of the webpage to be scanned.
        """
        self.url = url
        self.technologies = {}

    def scan_technologies(self):
        """
        Scans the specified URL to identify technologies used on the webpage.
        """
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
        """
        Displays the identified technologies in a formatted table.
        """
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
        """
        Returns the identified technologies.

        Returns:
        dict: A dictionary containing the identified technologies and their details.
        """
        if not self.technologies:
            return {"No technologies found."}
        return self.technologies

def display_cve_links(technologies):
    console.print("[bold blue]Possible Related CVE Links:[/bold blue]")
    
    if not technologies or len(technologies) == 0:
        console.print("[bold red]No technologies found.[/bold red]")
        return  

    table = Table(show_header=True, header_style="bold green", title="[bold]CVE Links for Technologies[/bold]")
    table.add_column("Technology", style="blue", justify="center")
    table.add_column("CVE Link", style="magenta")

    for tech in technologies:
        if tech == "No technologies found.":
            table.add_row(tech, "###")
        else:
            details_link = get_cve_details_link(tech)
            table.add_row(tech, details_link)

    console.print(table)

