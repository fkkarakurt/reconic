"""
Subdomain Scanner

This script is aimed at identifying active subdomains of a given domain by utilizing a list of potential subdomain names and 
querying DNS records. It leverages the dns.resolver module to perform DNS lookups for A records associated with each subdomain, 
effectively uncovering live subdomains and their corresponding IP addresses.

The SubdomainScanner class encapsulates the scanning process, which involves reading a list of subdomain names from a file, 
performing DNS queries, and collecting the results. It utilizes 
the Rich library to present the findings in a well-structured table format, making it easier to interpret the scan outcomes.

Features:
- Scans for active subdomains using a predefined list of subdomain names.
- Resolves A records for discovered subdomains to find their IP addresses.
- Presents the scanning results in a readable table format using Rich.

Important:
This tool is particularly useful for penetration testers and 
security researchers who need to discover active subdomains of a target domain as part of their reconnaissance phase. 
It can help in mapping out the attack surface of a target by identifying various points of entry.

Example Use Case:
Can be employed in the early stages of a security assessment to enumerate subdomains 
that could reveal additional targets or expose vulnerabilities.

Author: Fatih Küçükkarakurt <https://github.com/fkkarakurt>
Created: 2024-02-16
Last Updated: 2024-02-18
"""


import dns.resolver
from rich.console import Console
from rich.table import Table

class SubdomainScanner:
    def __init__(self, domain):
        self.domain = domain
        self.console = Console()

    def scan_subdomains(self):
        found_subdomains = {}

        with open("wordlists/subdomains.txt", "r") as file:
            subdomains = [line.strip() for line in file]

        for subdomain in subdomains:
            try:
                full_domain = f"{subdomain}.{self.domain}"
                answers = dns.resolver.resolve(full_domain, 'A')
                found_subdomains[full_domain] = [answer.to_text() for answer in answers]
            except (dns.resolver.NoAnswer, dns.resolver.NXDOMAIN):
                continue
            except Exception as e:
                self.console.print(f"[red]Error during subdomain scanning: {e}[/red]")

        return found_subdomains

    def display_results(self, found_subdomains):
        table = Table(show_header=True, header_style="bold green", title="[bold]Subdomain Scan Results[/bold]")
        table.add_column("Subdomain", style="blue") 
        table.add_column("IP Addresses", style="magenta")

        for subdomain, ips in found_subdomains.items():
            ip_addresses = ', '.join(ips)
            table.add_row(subdomain, ip_addresses)

        self.console.print(table)
