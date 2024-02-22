"""
SSL Certificate Scanner

This script is designed to fetch and display SSL certificate information for a given hostname and port, 
primarily focusing on secure (HTTPS) connections. It employs Python's ssl and socket modules to establish 
a secure connection and retrieve the certificate details from the server. The extracted information includes 
the issuer, subject, validity period, version, and serial number of the certificate.

The SSLCertScanner class encapsulates the functionality for connecting to the server, 
retrieving the SSL certificate, and parsing its details. 
It provides a user-friendly display of the certificate information using the Rich library, 
which formats the output in a readable table format.

Features:
- Fetches SSL certificate information over a secure connection.
- Parses and displays key certificate details such as issuer, subject, and validity.
- Utilizes the Rich library for enhanced output formatting.

Important:
This tool is valuable for security analysis, allowing users to quickly assess 
the SSL certificate details of a website or server. It's crucial for verifying the authenticity and 
validity period of certificates in security audits and compliance checks.

Example Use Case:
Can be used as part of a security audit toolkit to verify the SSL certificates of various company websites, 
ensuring they are up to date and issued by a trusted authority.

Author: Fatih Küçükkarakurt <https://github.com/fkkarakurt>
Created: 2024-02-17
Last Updated: 2024-02-18
"""


import ssl
import socket
from datetime import datetime
from rich.console import Console
from rich.table import Table

class SSLCertScanner:
    def __init__(self, hostname, port=443):
        self.hostname = hostname
        self.port = port
        self.console = Console()

    def get_ssl_certificate_info(self):
        ssl_info = {}
        context = ssl.create_default_context()
        try:
            with socket.create_connection((self.hostname, self.port), timeout=10) as sock:
                with context.wrap_socket(sock, server_hostname=self.hostname) as ssock:
                    certificate = ssock.getpeercert()

            # Reveal certificate information
            ssl_info['Issuer'] = dict(x[0] for x in certificate['issuer'])
            ssl_info['Subject'] = dict(x[0] for x in certificate['subject'])
            ssl_info['Valid From'] = datetime.strptime(certificate['notBefore'], '%b %d %H:%M:%S %Y %Z').strftime('%Y-%m-%d %H:%M:%S')
            ssl_info['Valid To'] = datetime.strptime(certificate['notAfter'], '%b %d %H:%M:%S %Y %Z').strftime('%Y-%m-%d %H:%M:%S')
            ssl_info['Version'] = certificate['version']
            ssl_info['Serial Number'] = certificate['serialNumber']
        except Exception as e:
            self.console.print(f"[red]Error scanning SSL for {self.hostname}: {e}[/red]")
            return None

        return ssl_info

    def display_results(self, ssl_info):
        if ssl_info is None:
            self.console.print(f"[yellow]No SSL information available for {self.hostname}.[/yellow]")
            return

        table = Table(show_header=True, header_style="bold green", title="[bold]SSL Certificate Information[/bold]")
        table.add_column("Field", style="blue")
        table.add_column("Value", style="magenta")
        for key, value in ssl_info.items():
            table.add_row(key, str(value))
        self.console.print(table)
