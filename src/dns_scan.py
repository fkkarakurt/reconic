"""
DNS Reconnaissance Tool

This script facilitates the discovery of DNS records associated with a given domain. By querying A, MX, and NS records,
it gathers crucial DNS information that can be used for network reconnaissance purposes. Utilizing the dns.resolver 
module for DNS queries and the rich library for output visualization, this tool simplifies the process of DNS 
reconnaissance, presenting the results in an easy-to-read table format.

The DNSRecon class is the core of this tool, providing methods for querying different types of DNS records and 
a method for reverse DNS lookups. It handles exceptions gracefully, ensuring that the tool can continue running 
even if certain queries fail. This makes it an invaluable tool for network administrators and cybersecurity 
professionals looking to gain insights into the DNS setup of a domain.

Features:
- Queries for A (Address), MX (Mail Exchange), and NS (Name Server) records.
- Performs reverse DNS lookup to find the hostname associated with an IP address.
- Visual presentation of results in a table format for clear and concise review.

Important:
This tool is designed for legal and ethical use cases only, such as security assessments and network troubleshooting.
Always ensure you have authorization before conducting reconnaissance on any domain.

Author: Fatih Küçükkarakurt <https://github.com/fkkarakurt>
Created: 2024-02-14
Last Updated: 2024-02-18
"""


import dns.resolver
import socket
from rich.table import Table
from rich.console import Console

class DNSRecon:
    def __init__(self, domain):
        self.domain = domain
        self.console = Console()

    def perform_dns_recon(self):
        results = {
            'A': self.query_a_record(),
            'MX': self.query_mx_record(),
            'NS': self.query_ns_record()
        }
        return results

    def query_a_record(self):
        try:
            answers = dns.resolver.resolve(self.domain, 'A')
            return [rdata.address for rdata in answers]
        except Exception as e:
            return [f"Error: {e}"]

    def query_mx_record(self):
        try:
            answers = dns.resolver.resolve(self.domain, 'MX')
            return [str(rdata.exchange) for rdata in answers]
        except Exception as e:
            return [f"Error: {e}"]

    def query_ns_record(self):
        try:
            answers = dns.resolver.resolve(self.domain, 'NS')
            return [str(rdata.target) for rdata in answers]
        except Exception as e:
            return [f"Error: {e}"]

    def reverse_dns(self, ip_address):
        try:
            result = socket.gethostbyaddr(ip_address)
            return result[0]
        except Exception as e:
            return f"Error: {e}"

    def print_results(self):
        table = Table(show_header=True, header_style="bold green", title="[bold]DNS Recon Results[/bold]")

        table.add_column("Type", justify="center", style="blue", no_wrap=True)
        table.add_column("Value", style="magenta")

        # A Results
        for a_record in self.query_a_record():
            table.add_row("A", a_record)

        # MX Results
        for mx_record in self.query_mx_record():
            table.add_row("MX", mx_record)

        # NS Results
        for ns_record in self.query_ns_record():
            table.add_row("NS", ns_record)

        self.console.print(table)
